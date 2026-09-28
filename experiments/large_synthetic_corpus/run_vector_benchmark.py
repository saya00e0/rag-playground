"""Build an isolated Vector index and evaluate the large synthetic corpus.

This runner never uses the application's ``chroma_db`` or ``documents`` collection.
Its artifacts are reproducible from the committed synthetic documents and dataset.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import chromadb
from openai import OpenAI

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from eval.dataset import load_dataset
from eval.evaluate_retrieval import corpus_hash, run_vector_evaluation, summarize


CHUNK_SIZE = 500
OVERLAP = 50


@dataclass(frozen=True)
class RetrievedChunk:
    text: str
    source: str
    score: float
    chunk_idx: int


def chunk_text(text: str) -> list[str]:
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start : start + CHUNK_SIZE])
        start += CHUNK_SIZE - OVERLAP
    return [chunk for chunk in chunks if len(chunk.strip()) > 50]


def source_documents(documents_dir: Path) -> list[Path]:
    documents = sorted(documents_dir.glob("*.txt"))
    if not documents:
        raise ValueError(f"no .txt documents found in {documents_dir}")
    return documents


def build_index(
    documents: list[Path], chroma_path: str, collection_name: str, model: str, reset: bool
) -> object:
    client = OpenAI()
    chroma = chromadb.PersistentClient(path=chroma_path)
    if reset:
        try:
            chroma.delete_collection(collection_name)
        except chromadb.errors.NotFoundError:
            pass
    try:
        chroma.get_collection(collection_name)
    except chromadb.errors.NotFoundError:
        pass
    else:
        raise ValueError(f"collection already exists: {collection_name}; rerun with --reset to replace it")
    collection = chroma.create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})

    texts: list[str] = []
    ids: list[str] = []
    metadatas: list[dict] = []
    for document in documents:
        for chunk_idx, text in enumerate(chunk_text(document.read_text(encoding="utf-8"))):
            texts.append(text)
            ids.append(f"{document.stem}_{chunk_idx}")
            metadatas.append({"source": str(document), "chunk_idx": chunk_idx})

    if not texts:
        raise ValueError("all documents produced zero chunks")
    for start in range(0, len(texts), 100):
        batch = texts[start : start + 100]
        embeddings = client.embeddings.create(input=texts[start : start + 100], model=model).data
        collection.add(
            ids=ids[start : start + 100],
            documents=texts[start : start + 100],
            embeddings=[item.embedding for item in embeddings],
            metadatas=metadatas[start : start + 100],
        )
    return collection


def retriever_for(collection: object, model: str):
    client = OpenAI()

    def retrieve(question: str, top_k: int) -> list[RetrievedChunk]:
        query_embedding = client.embeddings.create(input=[question], model=model).data[0].embedding
        result = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        return [
            RetrievedChunk(text=text, source=metadata["source"], score=1 - distance, chunk_idx=metadata["chunk_idx"])
            for text, metadata, distance in zip(
                result["documents"][0], result["metadatas"][0], result["distances"][0]
            )
        ]

    return retrieve


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--documents-dir", default="experiments/large_synthetic_corpus/docs")
    parser.add_argument("--dataset", default="experiments/large_synthetic_corpus/eval/dataset.jsonl")
    parser.add_argument("--chroma-path", default="experiments/large_synthetic_corpus/chroma_db")
    parser.add_argument("--collection", default="large_synthetic_documents")
    parser.add_argument("--output-dir", default="experiments/large_synthetic_corpus/results")
    parser.add_argument("--model", default="text-embedding-3-small")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--reset", action="store_true", help="replace only this experiment collection")
    args = parser.parse_args()
    if args.top_k < 5:
        parser.error("--top-k must be at least 5 to calculate Recall@5")

    documents = source_documents(Path(args.documents_dir))
    collection = build_index(documents, args.chroma_path, args.collection, args.model, args.reset)
    dataset = load_dataset(args.dataset)
    rows = run_vector_evaluation(dataset, args.top_k, retriever_for(collection, args.model))
    summary = {
        "system": "vector",
        "dataset_path": args.dataset,
        "dataset_question_count": len(dataset),
        "relevance_unit": "document_id",
        "top_k": args.top_k,
        "embedding_model": args.model,
        "chunk_count": collection.count(),
        "corpus_sha256": corpus_hash(str(path) for path in documents),
        **summarize(rows),
    }
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "vector_raw.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / "vector_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
