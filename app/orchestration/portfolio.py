from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.orchestration.models import DomainEvidence, DomainResult


@dataclass(frozen=True)
class PortfolioProject:
    project_id: str
    name: str
    status: str
    progress_pct: int
    executive_health: str
    next_milestone: str
    milestone_date: str
    risks: list[str]
    dependencies: list[str]
    source: str


class PortfolioDemoRepository:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.projects = [PortfolioProject(**item) for item in json.loads(path.read_text(encoding="utf-8"))]

    def search(self, question: str, context: dict[str, Any]) -> list[PortfolioProject]:
        text = question.lower()
        explicit = str(context.get("project_id", "")).lower()
        matches = [
            project for project in self.projects
            if (explicit and project.project_id.lower() == explicit)
            or project.project_id.lower() in text
            or project.name.lower() in text
        ]
        if matches:
            return matches

        # FAST DEMO convenience: if the question asks broadly about portfolio,
        # return the controlled demo portfolio rather than inventing a project.
        if any(token in text for token in ("portafolio", "proyectos", "proyecto")):
            return self.projects
        return []


class GroundedPortfolioOrchestrator:
    domain = "portfolio"

    def __init__(self, repository: PortfolioDemoRepository) -> None:
        self.repository = repository

    def handle(self, question: str, context: dict[str, Any]) -> DomainResult:
        projects = self.repository.search(question, context)
        if not projects:
            return DomainResult(
                domain=self.domain,
                status="no_evidence",
                summary="No existe evidencia suficiente en el portafolio demo para sustentar una respuesta.",
                evidence=[],
            )

        lines: list[str] = []
        evidence: list[DomainEvidence] = []
        for project in projects:
            risks = "; ".join(project.risks)
            dependencies = "; ".join(project.dependencies)
            summary = (
                f"{project.project_id} — {project.name}: {project.status}, "
                f"{project.progress_pct}% de avance, salud ejecutiva {project.executive_health}. "
                f"Próximo hito: {project.next_milestone} ({project.milestone_date}). "
                f"Riesgos: {risks}. Dependencias: {dependencies}."
            )
            lines.append(summary)
            evidence.append(
                DomainEvidence(
                    domain=self.domain,
                    source_id=project.project_id,
                    source_name=project.name,
                    excerpt=summary,
                    score=1.0,
                    metadata={
                        "status": project.status,
                        "progress_pct": project.progress_pct,
                        "executive_health": project.executive_health,
                        "source": project.source,
                    },
                )
            )

        return DomainResult(
            domain=self.domain,
            status="grounded",
            summary="\n".join(lines),
            evidence=evidence,
        )
