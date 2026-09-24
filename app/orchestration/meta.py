from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.orchestration.models import DomainOrchestrator, DomainResult
from app.orchestration.registry import CapabilityRegistry


@dataclass
class OrchestrationResult:
    status: str
    answer: str
    consulted_domains: list[str]
    routing_events: list[str]
    domain_results: list[DomainResult]


class EnterpriseMetaOrchestrator:
    def __init__(
        self,
        registry: CapabilityRegistry,
        domains: dict[str, DomainOrchestrator],
    ) -> None:
        self.registry = registry
        self.domains = domains

    def handle(self, question: str, context: dict[str, Any] | None = None) -> OrchestrationResult:
        context = context or {}
        selected = self.registry.discover(question)
        if not selected:
            return OrchestrationResult(
                status="unsupported",
                answer="No encuentro una capacidad empresarial habilitada para responder esta solicitud.",
                consulted_domains=[],
                routing_events=["intent_received", "no_capability_found"],
                domain_results=[],
            )

        results: list[DomainResult] = []
        events = ["intent_received", *[f"domain_selected:{domain}" for domain in selected]]
        for domain in selected:
            orchestrator = self.domains.get(domain)
            if orchestrator is None:
                continue
            results.append(orchestrator.handle(question, context))
            events.append(f"domain_completed:{domain}")

        if not results:
            return OrchestrationResult(
                status="unsupported",
                answer="Las capacidades identificadas no están disponibles en este runtime.",
                consulted_domains=selected,
                routing_events=events,
                domain_results=[],
            )

        grounded = [item for item in results if item.status == "grounded"]
        if grounded:
            answer = "\n\n".join(f"[{item.domain.upper()}] {item.summary}" for item in results)
            status = "grounded" if len(grounded) == len(results) else "partial"
        else:
            answer = "\n\n".join(f"[{item.domain.upper()}] {item.summary}" for item in results)
            status = "no_evidence"

        return OrchestrationResult(
            status=status,
            answer=answer,
            consulted_domains=[item.domain for item in results],
            routing_events=events,
            domain_results=results,
        )
