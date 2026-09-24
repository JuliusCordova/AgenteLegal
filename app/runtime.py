from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.api_models import Evidence, GroundedResponse


class LegalSearch(Protocol):
    def search(self, query: str, top_k: int = 5, graph_hops: int = 1): ...


@dataclass
class GroundedLegalRuntime:
    retriever: LegalSearch
    minimum_score: float = 0.15

    def _evidence(self, question: str, top_k: int, document_ids: list[str]) -> list[Evidence]:
        hits = self.retriever.search(question, top_k=top_k, graph_hops=1)
        evidence: list[Evidence] = []
        allowed = set(document_ids)
        for hit in hits:
            metadata = hit.metadata
            document_id = str(metadata.get("document_id", ""))
            if allowed and document_id not in allowed:
                continue
            if hit.score < self.minimum_score:
                continue
            evidence.append(
                Evidence(
                    document_id=document_id,
                    document_name=str(metadata.get("title") or document_id),
                    chunk_id=hit.chunk_id,
                    section=metadata.get("section"),
                    excerpt=hit.text,
                    score=round(float(hit.score), 4),
                    graph_context=hit.graph_context,
                )
            )
        return evidence

    def query(self, question: str, top_k: int = 5, document_ids: list[str] | None = None) -> GroundedResponse:
        evidence = self._evidence(question, top_k, document_ids or [])
        if not evidence:
            return GroundedResponse(
                status="no_evidence",
                answer="No existe evidencia suficiente en el corpus habilitado para sustentar una respuesta.",
                evidence=[],
            )

        # Sprint 3 first vertical slice: deterministic grounded response.
        # Gemini/ADK synthesis is plugged in behind this contract next, without changing the API.
        excerpts = " ".join(item.excerpt for item in evidence[:3])
        return GroundedResponse(
            status="grounded",
            answer=excerpts,
            evidence=evidence,
        )

    def compare(self, question: str, document_ids: list[str], top_k: int = 5) -> GroundedResponse:
        evidence: list[Evidence] = []
        for document_id in document_ids:
            evidence.extend(self._evidence(question, top_k, [document_id]))

        represented = {item.document_id for item in evidence}
        missing = [doc for doc in document_ids if doc not in represented]
        if missing:
            return GroundedResponse(
                status="no_evidence",
                answer="No existe evidencia suficiente para comparar todos los documentos solicitados.",
                evidence=evidence,
            )

        excerpts = " ".join(
            f"[{item.document_name} / {item.section or 'sección'}] {item.excerpt}"
            for item in evidence[:6]
        )
        return GroundedResponse(status="grounded", answer=excerpts, evidence=evidence)
