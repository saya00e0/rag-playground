"""Dense retrieval over an isolated Chroma collection (never the app's ``documents`` collection)."""

from __future__ import annotations

import hashlib
import time

import chromadb

from src.corpus import Chunk
from src.llm import LLMClient, Usage
from src.retrievers.base import RetrievalResult, RetrievedItem


class VectorRetriever:
    name = "vector"

    def __init__(self, chunks: list[Chunk], llm: LLMClient, persist_dir: str, top_k: int) -> None:
        self.llm = llm
        self.top_k = top_k
        self.chunks = {chunk.id: chunk for chunk in chunks}
        fingerprint = hashlib.sha256(
            (llm.embedding_model + "\0" + "\0".join(chunk.id + "\0" + chunk.text for chunk in chunks)).encode("utf-8")
        ).hexdigest()[:12]
        self.collection = chromadb.PersistentClient(path=persist_dir).get_or_create_collection(
            name=f"article1_{fingerprint}", metadata={"hnsw:space": "cosine"}
        )
        self.build_usage = Usage()
        existing = set(self.collection.get(include=[])["ids"])
        missing = [chunk for chunk in chunks if chunk.id not in existing]
        for start in range(0, len(missing), 100):
            batch = missing[start:start + 100]
            vectors, usage = llm.embed([chunk.text for chunk in batch])
            self.build_usage = self.build_usage + usage
            self.collection.upsert(
                ids=[chunk.id for chunk in batch],
                embeddings=vectors,
                documents=[chunk.text for chunk in batch],
                metadatas=[{"doc_id": chunk.doc_id, "chunk_idx": chunk.chunk_idx} for chunk in batch],
            )

    def retrieve(self, query: str) -> RetrievalResult:
        started = time.perf_counter()
        vectors, usage = self.llm.embed([query])
        result = self.collection.query(query_embeddings=vectors, n_results=self.top_k, include=["distances"])
        items = []
        for chunk_id, distance in zip(result["ids"][0], result["distances"][0]):
            chunk = self.chunks[chunk_id]
            items.append(RetrievedItem(chunk.id, chunk.doc_id, chunk.text, 1 - distance, chunk.section_ids))
        return RetrievalResult(self.name, items, (time.perf_counter() - started) * 1000, usage)
