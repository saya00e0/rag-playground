"""Okapi BM25 over chunks, standard library only.

Compound identifiers such as ``HX-4417``, ``ingest.max_batch_bytes`` and ``4.12.3`` are
kept as one token and also split into their parts, so exact identifiers match strongly.
"""

from __future__ import annotations

import math
import re
import time
from collections import Counter

from src.corpus import Chunk
from src.retrievers.base import RetrievalResult, RetrievedItem

TOKEN = re.compile(r"[a-z0-9]+(?:[-._][a-z0-9]+)*")
STOPWORDS = frozenset(
    "a an and are as at be by can do does for from has have how i in is it its my of on or "
    "the their them they this to was what when where which who whom why will with".split()
)


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for match in TOKEN.findall(text.lower()):
        parts = [part for part in re.split(r"[-._]", match) if part]
        if len(parts) > 1:
            tokens.append(match)
        tokens.extend(parts)
    return [token for token in tokens if token not in STOPWORDS]


class BM25Retriever:
    name = "bm25"

    def __init__(self, chunks: list[Chunk], top_k: int, k1: float, b: float) -> None:
        self.chunks = chunks
        self.top_k = top_k
        self.k1 = k1
        self.b = b
        self.term_counts = [Counter(tokenize(chunk.text)) for chunk in chunks]
        self.lengths = [sum(counts.values()) for counts in self.term_counts]
        self.average_length = sum(self.lengths) / len(self.lengths)
        document_frequency: Counter = Counter()
        for counts in self.term_counts:
            document_frequency.update(counts.keys())
        total = len(chunks)
        self.idf = {
            term: math.log(1 + (total - df + 0.5) / (df + 0.5))
            for term, df in document_frequency.items()
        }

    def retrieve(self, query: str) -> RetrievalResult:
        started = time.perf_counter()
        terms = tokenize(query)
        scores = []
        for index, counts in enumerate(self.term_counts):
            norm = self.k1 * (1 - self.b + self.b * self.lengths[index] / self.average_length)
            score = sum(
                self.idf[term] * counts[term] * (self.k1 + 1) / (counts[term] + norm)
                for term in terms if term in counts
            )
            if score > 0:
                scores.append((score, index))
        scores.sort(key=lambda item: (-item[0], item[1]))
        items = [
            RetrievedItem(self.chunks[i].id, self.chunks[i].doc_id, self.chunks[i].text, score, self.chunks[i].section_ids)
            for score, i in scores[: self.top_k]
        ]
        return RetrievalResult(self.name, items, (time.perf_counter() - started) * 1000, note="" if items else "no query term matched")
