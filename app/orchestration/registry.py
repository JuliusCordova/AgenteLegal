from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Capability:
    domain: str
    description: str
    keywords: tuple[str, ...]


DEFAULT_CAPABILITIES = (
    Capability(
        domain="legal",
        description="Contratos, cláusulas, obligaciones, normativa y riesgos legales.",
        keywords=("contrato", "contractual", "cláusula", "clausula", "legal", "norma", "confidencial", "obligación", "obligacion"),
    ),
    Capability(
        domain="portfolio",
        description="Estado de proyectos, portafolio, demanda, hitos, dependencias y riesgos de proyecto.",
        keywords=("proyecto", "portafolio", "demanda", "hito", "avance", "dependencia", "cronograma", "pmo"),
    ),
)


class CapabilityRegistry:
    def __init__(self, capabilities=DEFAULT_CAPABILITIES) -> None:
        self.capabilities = tuple(capabilities)

    def discover(self, question: str) -> list[str]:
        normalized = question.lower()
        selected: list[str] = []
        for capability in self.capabilities:
            if any(re.search(rf"\b{re.escape(keyword)}\w*\b", normalized) for keyword in capability.keywords):
                selected.append(capability.domain)
        return selected

    def catalog(self) -> list[dict[str, str]]:
        return [{"domain": item.domain, "description": item.description} for item in self.capabilities]
