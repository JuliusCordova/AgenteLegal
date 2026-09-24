from dataclasses import dataclass

from app.orchestration.meta import EnterpriseMetaOrchestrator
from app.orchestration.models import DomainEvidence, DomainResult
from app.orchestration.registry import CapabilityRegistry


@dataclass
class EvidenceDomain:
    domain: str

    def handle(self, question, context):
        if self.domain == "portfolio":
            return DomainResult(
                domain="portfolio",
                status="grounded",
                summary="DEMO-PROJ-001 está en ejecución con 68% de avance y depende de aprobación contractual.",
                evidence=[
                    DomainEvidence(
                        domain="portfolio",
                        source_id="DEMO-PROJ-001",
                        source_name="Modernización de Abastecimiento",
                        excerpt="68% de avance; dependencia: Contrato DEMO-LEGAL-001.",
                        score=1.0,
                    )
                ],
            )
        return DomainResult(
            domain="legal",
            status="grounded",
            summary="La ampliación del piloto requiere aprobación escrita y puede afectar el cronograma.",
            evidence=[
                DomainEvidence(
                    domain="legal",
                    source_id="demo-contract-chunk",
                    source_name="DEMO-LEGAL-001",
                    excerpt="La ampliación a una siguiente fase requiere aprobación escrita.",
                    score=0.95,
                    metadata={"related_project": "DEMO-PROJ-001"},
                )
            ],
            requires_human_review=True,
        )


def test_executive_cross_domain_scenario_preserves_provenance():
    meta = EnterpriseMetaOrchestrator(
        CapabilityRegistry(),
        {
            "legal": EvidenceDomain("legal"),
            "portfolio": EvidenceDomain("portfolio"),
        },
    )

    result = meta.handle(
        "Cuál es el avance del proyecto DEMO-PROJ-001 y qué riesgos tiene su contrato",
        {"project_id": "DEMO-PROJ-001"},
    )

    assert result.status == "grounded"
    assert result.consulted_domains == ["legal", "portfolio"]
    assert {item.domain for item in result.domain_results} == {"legal", "portfolio"}
    assert all(item.evidence for item in result.domain_results)
    assert "68%" in result.answer
    assert "aprobación escrita" in result.answer
