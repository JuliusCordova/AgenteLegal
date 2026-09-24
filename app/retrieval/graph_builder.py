from __future__ import annotations

import re
from collections import defaultdict

from app.retrieval.graph import GraphEdge, GraphNode, LegalGraph
from app.retrieval.models import Chunk


TOPIC_KEYWORDS = {
    "confidentiality": ["confidencial", "reserva"],
    "personal_data": ["datos personales", "tratamiento", "seguridad", "encargo"],
    "digital_signature": ["firma digital", "firma electrónica", "certificado digital"],
    "liability": ["responsabilidad", "lucro cesante", "dolo", "fraude"],
    "termination": ["resolución", "resolver", "incumplimiento", "terminar"],
    "intellectual_property": ["propiedad intelectual", "código fuente", "licencia"],
    "consumer_protection": ["consumidor", "reclamo", "idoneidad"],
}

NORM_MATCHERS = {
    "norm:codigo_civil_dl_295": ["código civil", "decreto legislativo n.º 295", "decreto legislativo n. 295"],
    "norm:ley_29733": ["ley n.º 29733", "ley n. 29733", "ley 29733"],
    "norm:ds_016_2024_jus": ["016-2024-jus", "reglamento de la ley n.º 29733", "reglamento de la ley 29733"],
    "norm:ley_27269": ["ley n.º 27269", "ley n. 27269", "ley 27269"],
    "norm:ley_29571": ["ley n.º 29571", "ley n. 29571", "ley 29571"],
}

NORM_LABELS = {
    "norm:codigo_civil_dl_295": "Código Civil — Decreto Legislativo N.º 295",
    "norm:ley_29733": "Ley N.º 29733 — Protección de Datos Personales",
    "norm:ds_016_2024_jus": "DS N.º 016-2024-JUS — Reglamento de Datos Personales",
    "norm:ley_27269": "Ley N.º 27269 — Firmas y Certificados Digitales",
    "norm:ley_29571": "Ley N.º 29571 — Protección y Defensa del Consumidor",
}


def _slug(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return cleaned or "unknown"


def _topics(text: str) -> list[str]:
    lowered = text.lower()
    return [
        topic
        for topic, keywords in TOPIC_KEYWORDS.items()
        if any(keyword in lowered for keyword in keywords)
    ]


def build_legal_graph(chunks: list[Chunk]) -> LegalGraph:
    graph = LegalGraph()
    clauses_by_topic: dict[str, list[str]] = defaultdict(list)

    graph.add_node(GraphNode("jurisdiction:peru", "Jurisdiction", "Peru", {}))

    for norm_id, label in NORM_LABELS.items():
        graph.add_node(GraphNode(norm_id, "LegalNorm", label, {}))

    for chunk in chunks:
        document_node = f"document:{chunk.document_id}"
        graph.add_node(
            GraphNode(
                document_node,
                "Contract" if chunk.document_type == "contract" else "LegalDocument",
                chunk.title,
                {"source_path": chunk.source_path},
            )
        )
        graph.add_node(
            GraphNode(
                chunk.node_id,
                "Clause" if chunk.document_type == "contract" else "LegalTextUnit",
                chunk.section,
                {
                    "chunk_id": chunk.chunk_id,
                    "document_id": chunk.document_id,
                    "source_path": chunk.source_path,
                },
            )
        )
        graph.add_edge(GraphEdge(document_node, chunk.node_id, "HAS_CLAUSE", chunk.source_path))
        graph.add_edge(GraphEdge(document_node, "jurisdiction:peru", "GOVERNED_BY", chunk.source_path))

        combined = f"{chunk.section}\n{chunk.text}".lower()

        for topic in _topics(combined):
            topic_id = f"topic:{topic}"
            graph.add_node(GraphNode(topic_id, "LegalTopic", topic, {}))
            graph.add_edge(GraphEdge(chunk.node_id, topic_id, "ABOUT", chunk.source_path))
            clauses_by_topic[topic].append(chunk.node_id)

        for norm_id, matchers in NORM_MATCHERS.items():
            if any(matcher in combined for matcher in matchers):
                graph.add_edge(GraphEdge(chunk.node_id, norm_id, "REFERENCES", chunk.source_path))

    for norm_id, label in NORM_LABELS.items():
        norm_text = label.lower()
        for topic in _topics(norm_text):
            topic_id = f"topic:{topic}"
            graph.add_node(GraphNode(topic_id, "LegalTopic", topic, {}))
            graph.add_edge(GraphEdge(norm_id, topic_id, "REGULATES", "norm-catalog"))

    for topic, node_ids in clauses_by_topic.items():
        unique = sorted(set(node_ids))
        for idx, source in enumerate(unique):
            for target in unique[idx + 1 :]:
                graph.add_edge(GraphEdge(source, target, "SIMILAR_TO", f"topic:{topic}"))

    return graph
