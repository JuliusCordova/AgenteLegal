from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    document_ids: list[str] = Field(default_factory=list)
    top_k: int = Field(default=5, ge=1, le=10)


class CompareRequest(BaseModel):
    question: str = Field(min_length=1)
    document_ids: list[str] = Field(min_length=2, max_length=5)
    top_k: int = Field(default=5, ge=1, le=10)


class Evidence(BaseModel):
    document_id: str
    document_name: str
    chunk_id: str
    section: str | None = None
    excerpt: str
    score: float
    graph_context: list[dict[str, Any]] = Field(default_factory=list)


class GroundedResponse(BaseModel):
    status: str
    answer: str
    evidence: list[Evidence] = Field(default_factory=list)
    requires_human_review: bool = True
