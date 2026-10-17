"""Load the article1 Markdown corpus into documents, sections, and character chunks."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Union


@dataclass(frozen=True)
class Section:
    id: str
    doc_id: str
    heading: str
    text: str
    start: int
    end: int


@dataclass(frozen=True)
class Document:
    id: str
    path: str
    title: str
    text: str
    sections: tuple[Section, ...]


@dataclass(frozen=True)
class Chunk:
    id: str
    doc_id: str
    chunk_idx: int
    text: str
    start: int
    end: int
    section_ids: tuple[str, ...]


@dataclass(frozen=True)
class Query:
    id: str
    query: str
    query_type: str
    gold_answer: str
    key_facts: tuple[str, ...]
    relevant_docs: tuple[str, ...]
    relevant_sections: tuple[str, ...]

    @property
    def evidence_units(self) -> tuple[str, ...]:
        """Sections when the label names them, otherwise whole documents."""
        return self.relevant_sections or self.relevant_docs


HEADING_NUMBER = re.compile(r"^(?:(\d+)|Appendix ([A-Z]))\.")


def _section_key(heading: str, position: int) -> str:
    match = HEADING_NUMBER.match(heading)
    if match:
        return match.group(1) or match.group(2)
    return str(position)


def parse_document(path: Path) -> Document:
    text = path.read_text(encoding="utf-8")
    doc_id = path.stem
    title_match = re.match(r"# (.+)\n", text)
    if not title_match:
        raise ValueError(f"{path}: document must start with a '# ' title")
    headings = list(re.finditer(r"^## (.+)$", text, flags=re.MULTILINE))
    sections: list[Section] = []
    preamble_end = headings[0].start() if headings else len(text)
    sections.append(Section(f"{doc_id}#0", doc_id, title_match.group(1), text[:preamble_end].strip(), 0, preamble_end))
    for position, match in enumerate(headings, 1):
        end = headings[position].start() if position < len(headings) else len(text)
        heading = match.group(1).strip()
        sections.append(
            Section(f"{doc_id}#{_section_key(heading, position)}", doc_id, heading, text[match.start():end].strip(), match.start(), end)
        )
    return Document(doc_id, str(path), title_match.group(1).strip(), text, tuple(sections))


def load_corpus(corpus_dir: Union[str, Path]) -> list[Document]:
    documents = [parse_document(path) for path in sorted(Path(corpus_dir).glob("*.md"))]
    if not documents:
        raise ValueError(f"no documents in {corpus_dir}")
    return documents


def chunk_document(document: Document, size: int, overlap: int) -> list[Chunk]:
    """Character windows, matching ingest.py's scheme with configurable size/overlap."""
    if not 0 <= overlap < size:
        raise ValueError("overlap must be in [0, size)")
    chunks: list[Chunk] = []
    start = 0
    while start < len(document.text):
        end = min(start + size, len(document.text))
        piece = document.text[start:end]
        if len(piece.strip()) > 50:
            covered = tuple(
                section.id for section in document.sections
                if section.start < end and start < section.end
            )
            idx = len(chunks)
            chunks.append(Chunk(f"{document.id}#c{idx}", document.id, idx, piece, start, end, covered))
        start += size - overlap
    return chunks


def corpus_sha256(documents: list[Document]) -> str:
    digest = hashlib.sha256()
    for document in sorted(documents, key=lambda doc: doc.id):
        digest.update(document.id.encode("utf-8") + b"\0" + document.text.encode("utf-8") + b"\0")
    return digest.hexdigest()


def load_queries(path: Union[str, Path], documents: list[Document]) -> list[Query]:
    doc_ids = {document.id for document in documents}
    section_ids = {section.id for document in documents for section in document.sections}
    queries: list[Query] = []
    for line_number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        raw = json.loads(line)
        query = Query(
            id=raw["id"],
            query=raw["query"],
            query_type=raw["query_type"],
            gold_answer=raw["gold_answer"],
            key_facts=tuple(raw["key_facts"]),
            relevant_docs=tuple(raw["relevant_docs"]),
            relevant_sections=tuple(raw.get("relevant_sections", [])),
        )
        unknown = set(query.relevant_docs) - doc_ids or set(query.relevant_sections) - section_ids
        if unknown:
            raise ValueError(f"line {line_number}: unknown evidence ids {sorted(unknown)}")
        queries.append(query)
    if len({query.id for query in queries}) != len(queries):
        raise ValueError("duplicate query ids")
    return queries
