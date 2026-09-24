import json

from app.retrieval.embeddings import DeterministicTestEmbedder
from app.retrieval.loader import _build


def test_loader_rehydrates_retriever():
    embedder = DeterministicTestEmbedder(dimensions=64)
    chunk = {
        "chunk_id": "c1",
        "document_id": "d1",
        "document_type": "contract",
        "title": "Contrato Demo",
        "section": "Confidencialidad",
        "text": "La información confidencial debe protegerse.",
        "source_path": "demo.md",
        "node_id": "chunk:c1",
    }
    vector = embedder.embed_document("Contrato Demo Confidencialidad La información confidencial debe protegerse.")
    graph = {
        "nodes": [
            {"node_id": "chunk:c1", "node_type": "Clause", "label": "Confidencialidad", "metadata": {}}
        ],
        "edges": [],
    }
    retriever = _build(
        json.dumps(chunk) + "\n",
        json.dumps({"chunk_id": "c1", "vector": vector}) + "\n",
        json.dumps(graph),
        embedder,
    )
    hits = retriever.search("información confidencial", top_k=1)
    assert len(hits) == 1
    assert hits[0].chunk_id == "c1"
