from pathlib import Path

from app.orchestration.portfolio import GroundedPortfolioOrchestrator, PortfolioDemoRepository


def build_portfolio():
    return GroundedPortfolioOrchestrator(
        PortfolioDemoRepository(Path("data/demo/portfolio/projects.json"))
    )


def test_portfolio_project_is_grounded():
    result = build_portfolio().handle("Cuál es el avance de DEMO-PROJ-001", {})
    assert result.status == "grounded"
    assert result.evidence[0].source_id == "DEMO-PROJ-001"
    assert "68%" in result.summary


def test_portfolio_context_can_select_project():
    result = build_portfolio().handle("Cuál es su próximo hito", {"project_id": "DEMO-PROJ-002"})
    assert result.status == "grounded"
    assert result.evidence[0].source_id == "DEMO-PROJ-002"


def test_portfolio_abstains_without_matching_evidence():
    result = build_portfolio().handle("Dime el estado de ALPHA-999", {})
    assert result.status == "no_evidence"
    assert result.evidence == []
