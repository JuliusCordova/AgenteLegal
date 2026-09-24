from __future__ import annotations

import math
from dataclasses import dataclass

from app.retrieval.models import Chunk


@dataclass(frozen=True)
class VectorRecord:
    chunk: Chunk
    vector: list[float]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


class InMemoryVectorStore:
    def __init__(self, records: list[VectorRecord]) -> None:
        self.records = records

    def search(self, query_vector: list[float], top_k: int = 5) -> list[tuple[VectorRecord, float]]:
        ranked = [
            (record, cosine_similarity(query_vector, record.vector))
            for record in self.records
        ]
        ranked.sort(key=lambda item: item[1], reverse=True)
        return ranked[:top_k]
