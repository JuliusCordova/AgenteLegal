from pathlib import Path

from app.retrieval.chunker import chunk_markdown
from app.retrieval.embeddings import DeterministicTestEmbedder
from app.retrieval.graph_builder import build_legal_graph
from app.retrieval.graphrag import GraphRAGRetriever
from app.retrieval.vector_store import InMemoryVectorStore, VectorRecord


def test_chunk_graph_and_retrieval(tmp_path: Path) -> None:
    contract = tmp_path / "contract.md"
    contract.write_text(
        "# Contrato Demo\n"
        "## Datos personales\n"
        "El proveedor tratará datos personales y cumplirá la Ley 29733.\n"
        "## Firma\n"
        "Se admite firma digital conforme a la Ley 27269.\n",
        encoding="utf-8",
    )

    chunks = chunk_markdown(contract, "contract")
    assert len(chunks) == 2

    graph = build_legal_graph(chunks)
    assert any(e.relation == "REFERENCES" for e in graph.edges)
    assert any(e.relation == "ABOUT" for e in graph.edges)

    embedder = DeterministicTestEmbedder(dimensions=64)
    records = [
        VectorRecord(
            chunk=chunk,
            vector=embedder.embed_document(
                f"{chunk.title} {chunk.section} {chunk.text}"
            ),
        )
        for chunk in chunks
    ]

    retriever = GraphRAGRetriever(
        embedder=embedder,
        vector_store=InMemoryVectorStore(records),
        graph=graph,
    )

    hits = retriever.search("datos personales ley", top_k=1, graph_hops=1)
    assert len(hits) == 1
    assert hits[0].metadata["section"] == "Datos personales"
    assert any(
        ctx["node_type"] in {"LegalNorm", "LegalTopic"}
        for ctx in hits[0].graph_context
    )
