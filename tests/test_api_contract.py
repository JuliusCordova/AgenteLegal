from dataclasses import dataclass

from fastapi.testclient import TestClient

from app.main import app, get_runtime
from app.runtime import GroundedLegalRuntime


@dataclass
class Hit:
    chunk_id: str
    score: float
    text: str
    metadata: dict
    graph_context: list


class FakeRetriever:
    def search(self, query: str, top_k: int = 5, graph_hops: int = 1):
        if "desconocido" in query.lower():
            return []
        return [
            Hit(
                chunk_id="c-1",
                score=0.91,
                text="La obligación de confidencialidad permanece vigente por tres años.",
                metadata={
                    "document_id": "contract-a",
                    "title": "Contrato A",
                    "section": "Confidencialidad",
                },
                graph_context=[],
            ),
            Hit(
                chunk_id="c-2",
                score=0.88,
                text="La obligación de confidencialidad permanece vigente por cinco años.",
                metadata={
                    "document_id": "contract-b",
                    "title": "Contrato B",
                    "section": "Confidencialidad",
                },
                graph_context=[],
            ),
        ]


def client() -> TestClient:
    app.dependency_overrides[get_runtime] = lambda: GroundedLegalRuntime(FakeRetriever())
    return TestClient(app)


def test_query_returns_grounded_evidence():
    response = client().post("/api/v1/query", json={"question": "¿Cuál es la confidencialidad?"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "grounded"
    assert payload["evidence"][0]["document_id"] == "contract-a"
    assert payload["requires_human_review"] is True


def test_query_abstains_without_evidence():
    response = client().post("/api/v1/query", json={"question": "dato desconocido"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "no_evidence"
    assert payload["evidence"] == []


def test_compare_requires_evidence_for_both_documents():
    response = client().post(
        "/api/v1/compare",
        json={
            "question": "Compara confidencialidad",
            "document_ids": ["contract-a", "contract-b"],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "grounded"
    assert {item["document_id"] for item in payload["evidence"]} == {"contract-a", "contract-b"}
