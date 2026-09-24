from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    document_id: str
    document_type: str
    title: str
    section: str
    text: str
    source_path: str
    node_id: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SearchHit:
    chunk_id: str
    score: float
    text: str
    metadata: dict[str, Any]
    graph_context: list[dict[str, Any]]
