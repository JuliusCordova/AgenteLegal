from __future__ import annotations

from app.retrieval.embeddings import Embedder
from app.retrieval.graph import LegalGraph
from app.retrieval.models import SearchHit
from app.retrieval.vector_store import InMemoryVectorStore


class GraphRAGRetriever:
    def __init__(
        self,
        embedder: Embedder,
        vector_store: InMemoryVectorStore,
        graph: LegalGraph,
    ) -> None:
        self.embedder = embedder
        self.vector_store = vector_store
        self.graph = graph

    def search(
        self,
        query: str,
        top_k: int = 5,
        graph_hops: int = 1,
    ) -> list[SearchHit]:
        query_vector = self.embedder.embed_query(query)
        ranked = self.vector_store.search(query_vector, top_k=top_k)

        hits: list[SearchHit] = []
        for record, score in ranked:
            neighbors = self.graph.neighbors(record.chunk.node_id, hops=graph_hops)
            graph_context = [
                {
                    "node_id": node.node_id,
                    "node_type": node.node_type,
                    "label": node.label,
                    "metadata": node.metadata,
                }
                for node in neighbors
            ]
            hits.append(
                SearchHit(
                    chunk_id=record.chunk.chunk_id,
                    score=score,
                    text=record.chunk.text,
                    metadata=record.chunk.to_dict(),
                    graph_context=graph_context,
                )
            )
        return hits
