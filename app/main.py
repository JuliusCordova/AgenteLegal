from fastapi import FastAPI

from app.config import settings

app = FastAPI(
    title="AgenteLegal",
    version="0.1.0",
    description="FAST DEMO foundation for an evidence-backed legal assistant.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "agente-legal",
        "environment": settings.environment,
        "gcp_project": settings.gcp_project,
        "gcp_region": settings.gcp_region,
    }


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "AgenteLegal",
        "stage": "FAST DEMO",
        "message": "Sprint 0 foundation ready. Retrieval and agent behavior arrive in subsequent sprints.",
    }
