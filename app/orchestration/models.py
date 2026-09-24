from __future__ import annotations

from typing import Any, Protocol

from pydantic import BaseModel, Field


class DomainEvidence(BaseModel):
    domain: str
    source_id: str
    source_name: str
    excerpt: str
    score: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class DomainResult(BaseModel):
    domain: str
    status: str
    summary: str
    evidence: list[DomainEvidence] = Field(default_factory=list)
    requires_human_review: bool = False


class DomainOrchestrator(Protocol):
    domain: str

    def handle(self, question: str, context: dict[str, Any]) -> DomainResult: ...
