import os, glob, json
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from openai import OpenAI

load_dotenv()
client = OpenAI()
chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"},  # コサイン類似度を明示
)

CHUNK_SIZE = 500   # ← ポートフォリオで変えて見せるパラメータ
OVERLAP    = 50

def chunk_text(text: str) -> list[str]:
    chunks, start = [], 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start += CHUNK_SIZE - OVERLAP
    return [c for c in chunks if len(c.strip()) > 50]

def embed(texts: list[str]) -> list[list[float]]:
    res = client.embeddings.create(
        input=texts,
        model="text-embedding-3-small",  # コスパ最良
    )
    return [r.embedding for r in res.data]

def ingest_file(path: str):
    text = Path(path).read_text(encoding="utf-8")
    chunks = chunk_text(text)
    vectors = embed(chunks)
    ids = [f"{Path(path).stem}_{i}" for i in range(len(chunks))]
    
    collection.upsert(
        ids=ids,
        embeddings=vectors,
        documents=chunks,
        metadatas=[{"source": path, "chunk_idx": i} for i in range(len(chunks))],
    )
    print(f"✓ {path}: {len(chunks)} chunks ingested")

if __name__ == "__main__":
    for f in glob.glob("docs/*.txt"):
        ingest_file(f)
    print(f"\nTotal vectors: {collection.count()}")
