from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    node_type: str
    label: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class GraphEdge:
    source: str
    target: str
    relation: str
    provenance: str


class LegalGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, GraphNode] = {}
        self.edges: list[GraphEdge] = []

    def add_node(self, node: GraphNode) -> None:
        self.nodes[node.node_id] = node

    def add_edge(self, edge: GraphEdge) -> None:
        self.edges.append(edge)

    def neighbors(self, node_id: str, hops: int = 1) -> list[GraphNode]:
        visited = {node_id}
        frontier = {node_id}

        for _ in range(hops):
            next_frontier: set[str] = set()
            for edge in self.edges:
                if edge.source in frontier and edge.target not in visited:
                    next_frontier.add(edge.target)
                if edge.target in frontier and edge.source not in visited:
                    next_frontier.add(edge.source)
            visited.update(next_frontier)
            frontier = next_frontier

        visited.discard(node_id)
        return [self.nodes[nid] for nid in visited if nid in self.nodes]

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [asdict(node) for node in self.nodes.values()],
            "edges": [asdict(edge) for edge in self.edges],
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "LegalGraph":
        graph = cls()
        for node in payload.get("nodes", []):
            graph.add_node(GraphNode(**node))
        for edge in payload.get("edges", []):
            graph.add_edge(GraphEdge(**edge))
        return graph
