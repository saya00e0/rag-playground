import chromadb
from openai import OpenAI
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"},  # ingest.py と揃える（先に起動されてもL2にしない）
)

@dataclass
class RetrievedChunk:
    text: str
    source: str
    score: float      # 類似度スコア（ポートフォリオで可視化する）
    chunk_idx: int

def retrieve(query: str, top_k: int = 4) -> list[RetrievedChunk]:
    # クエリをembedding化
    q_vec = client.embeddings.create(
        input=[query],
        model="text-embedding-3-small",
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[q_vec],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append(RetrievedChunk(
            text=doc,
            source=meta["source"],
            score=1 - dist,   # コサイン距離 → 類似度に変換
            chunk_idx=meta["chunk_idx"],
        ))
    return chunks

def answer(query: str, chunks: list[RetrievedChunk]) -> str:
    context = "\n\n---\n\n".join(
        f"[出典: {c.source}]\n{c.text}" for c in chunks
    )
    prompt = f"""以下のコンテキストのみを使って質問に答えてください。
コンテキストに情報がない場合は「資料に記載がありません」と答えてください。

コンテキスト:
{context}

質問: {query}
回答:"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,   # RAGは再現性重視でtemp=0
    )
    return res.choices[0].message.content
