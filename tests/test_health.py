from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "agente-legal"
    assert payload["gcp_project"] == "proyectopersonal-480420"
    assert payload["gcp_region"] == "us-central1"
