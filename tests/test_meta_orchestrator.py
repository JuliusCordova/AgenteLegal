from dataclasses import dataclass

from app.orchestration.meta import EnterpriseMetaOrchestrator
from app.orchestration.models import DomainEvidence, DomainResult
from app.orchestration.registry import CapabilityRegistry


@dataclass
class FakeDomain:
    domain: str

    def handle(self, question, context):
        return DomainResult(
            domain=self.domain,
            status="grounded",
            summary=f"{self.domain} result",
            evidence=[DomainEvidence(domain=self.domain, source_id="1", source_name="demo", excerpt="evidence")],
        )


def build_meta():
    return EnterpriseMetaOrchestrator(
        CapabilityRegistry(),
        {"legal": FakeDomain("legal"), "portfolio": FakeDomain("portfolio")},
    )


def test_routes_legal_question():
    result = build_meta().handle("Revisa la cláusula del contrato")
    assert result.consulted_domains == ["legal"]
    assert result.status == "grounded"


def test_routes_portfolio_question():
    result = build_meta().handle("Cuál es el avance del proyecto")
    assert result.consulted_domains == ["portfolio"]


def test_coordinates_cross_domain_question():
    result = build_meta().handle("Cuál es el avance del proyecto y el riesgo del contrato")
    assert result.consulted_domains == ["legal", "portfolio"]
    assert len(result.domain_results) == 2


def test_abstains_when_no_capability_exists():
    result = build_meta().handle("Cuál es el clima de mañana")
    assert result.status == "unsupported"
    assert result.consulted_domains == []


def test_routes_contractual_project_risk_to_both_domains():
    result = build_meta().handle("Resume el avance del proyecto y su riesgo contractual")
    assert result.consulted_domains == ["legal", "portfolio"]
