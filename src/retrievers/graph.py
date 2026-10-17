"""Adapter around the existing ``graph/`` package (extraction cache, builder, traversal).

The graph is built once from the article1 chunks; extraction results are cached by chunk
hash so re-runs make no extraction calls.
"""

from __future__ import annotations

import time
from pathlib import Path

from graph.build_graph import chunk_digest, load_or_extract
from graph.builder import ChunkRef, GraphBuilder, graph_statistics
from graph.extractor import EXTRACTION_PROMPT_VERSION
from graph.retriever import GraphRetriever as Traversal
from graph.store import save_graph
from src.corpus import Chunk
from src.retrievers.base import RetrievalResult, RetrievedItem


class GraphRetriever:
    name = "graph"

    def __init__(self, chunks: list[Chunk], model: str, cache_dir: str, top_k: int, depth: int, max_seeds: int, max_extraction_chunks: int) -> None:
        if len(chunks) > max_extraction_chunks:
            raise RuntimeError(f"{len(chunks)} chunks exceed the approved extraction limit {max_extraction_chunks}")
        self.top_k = top_k
        self.depth = depth
        self.max_seeds = max_seeds
        extraction_dir = Path(cache_dir) / "extraction"
        builder = GraphBuilder()
        self.new_extraction_calls = 0
        for chunk in chunks:
            if not (extraction_dir / EXTRACTION_PROMPT_VERSION / f"{chunk_digest(chunk.text)}.json").exists():
                self.new_extraction_calls += 1
            extraction = load_or_extract(ChunkRef(chunk.doc_id, chunk.chunk_idx), chunk.text, extraction_dir, model)
            builder.add_extraction(ChunkRef(chunk.doc_id, chunk.chunk_idx), extraction)
        graph = builder.build()
        self.statistics = graph_statistics(graph)
        save_graph(Path(cache_dir) / "graph.json", graph, {"model": model, "prompt_version": EXTRACTION_PROMPT_VERSION, "statistics": self.statistics})
        self.traversal = Traversal(graph)
        self.chunks = {f"{chunk.doc_id}#{chunk.chunk_idx}": chunk for chunk in chunks}

    def retrieve(self, query: str) -> RetrievalResult:
        started = time.perf_counter()
        results = self.traversal.retrieve(query, depth=self.depth, max_entities=self.max_seeds, max_chunks=self.top_k)
        items = []
        for result in results:
            chunk = self.chunks[f"{result.source}#{result.chunk_idx}"]
            items.append(RetrievedItem(chunk.id, chunk.doc_id, chunk.text, result.score, chunk.section_ids))
        note = "" if items else "no seed entity in the query matched a graph node"
        return RetrievalResult(self.name, items, (time.perf_counter() - started) * 1000, note=note)
