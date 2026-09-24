from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.orchestration.models import DomainEvidence, DomainResult
from app.runtime import GroundedLegalRuntime


@dataclass
class LegalDomainOrchestrator:
    runtime: GroundedLegalRuntime
    domain: str = "legal"

    def handle(self, question: str, context: dict[str, Any]) -> DomainResult:
        result = self.runtime.query(question=question)
        return DomainResult(
            domain=self.domain,
            status=result.status,
            summary=result.answer,
            evidence=[
                DomainEvidence(
                    domain=self.domain,
                    source_id=item.chunk_id,
                    source_name=item.document_name,
                    excerpt=item.excerpt,
                    score=item.score,
                    metadata={"document_id": item.document_id, "section": item.section},
                )
                for item in result.evidence
            ],
            requires_human_review=True,
        )

