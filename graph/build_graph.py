"""Extract a cached graph from the existing Chroma corpus."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import chromadb

from graph.builder import ChunkRef, GraphBuilder, graph_statistics
from graph.extractor import EXTRACTION_PROMPT_VERSION, Extraction, Entity, Relation, extract_chunk
from graph.store import save_graph


def chunk_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extraction_to_dict(extraction: Extraction) -> dict:
    return {
        "entities": [{"name": entity.name, "type": entity.type} for entity in extraction.entities],
        "relations": [
            {"source": relation.source, "target": relation.target, "type": relation.type}
            for relation in extraction.relations
        ],
        "rejected_relations": [
            {"source": relation.source, "target": relation.target, "type": relation.type}
            for relation in extraction.rejected_relations
        ],
    }


def extraction_from_dict(raw: dict) -> Extraction:
    return Extraction(
        entities=tuple(Entity(**entity) for entity in raw["entities"]),
        relations=tuple(Relation(**relation) for relation in raw["relations"]),
        rejected_relations=tuple(Relation(**relation) for relation in raw.get("rejected_relations", [])),
    )


def load_or_extract(chunk: ChunkRef, text: str, cache_dir: Path, model: str) -> Extraction:
    digest = chunk_digest(text)
    cache_path = cache_dir / EXTRACTION_PROMPT_VERSION / f"{digest}.json"
    if cache_path.exists():
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        if (
            cached.get("chunk_sha256") == digest
            and cached.get("model") == model
            and cached.get("prompt_version") == EXTRACTION_PROMPT_VERSION
        ):
            return extraction_from_dict(cached["extraction"])

    extraction = extract_chunk(text, model=model)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps(
            {
                "source": chunk.source,
                "chunk_idx": chunk.chunk_idx,
                "chunk_sha256": digest,
                "model": model,
                "prompt_version": EXTRACTION_PROMPT_VERSION,
                "extraction": extraction_to_dict(extraction),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return extraction


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--max-chunks", type=int, default=10)
    parser.add_argument("--cache-dir", default="eval/results/extraction_cache")
    parser.add_argument("--graph-path", default="eval/results/graph.json")
    parser.add_argument("--chroma-path", default="./chroma_db")
    parser.add_argument("--collection", default="documents")
    args = parser.parse_args()
    if args.max_chunks < 1:
        parser.error("--max-chunks must be positive")

    collection = chromadb.PersistentClient(path=args.chroma_path).get_collection(args.collection)
    records = collection.get(include=["documents", "metadatas"])
    chunks = sorted(
        zip(records["documents"], records["metadatas"]),
        key=lambda item: (item[1]["source"], item[1]["chunk_idx"]),
    )
    if len(chunks) > args.max_chunks:
        raise RuntimeError(
            f"corpus has {len(chunks)} chunks, exceeding approved limit {args.max_chunks}"
        )

    builder = GraphBuilder()
    cache_dir = Path(args.cache_dir)
    rejected_relation_count = 0
    for text, metadata in chunks:
        chunk = ChunkRef(source=metadata["source"], chunk_idx=metadata["chunk_idx"])
        extraction = load_or_extract(chunk, text, cache_dir, args.model)
        rejected_relation_count += len(extraction.rejected_relations)
        builder.add_extraction(chunk, extraction)

    graph = builder.build()
    metadata = {
        "model": args.model,
        "prompt_version": EXTRACTION_PROMPT_VERSION,
        "chunk_count": len(chunks),
        "rejected_relation_count": rejected_relation_count,
        "statistics": graph_statistics(graph),
    }
    save_graph(args.graph_path, graph, metadata)
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
