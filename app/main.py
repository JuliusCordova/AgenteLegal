from fastapi import Depends, FastAPI

from app.api_models import CompareRequest, GroundedResponse, QueryRequest
from app.config import settings
from app.runtime import GroundedLegalRuntime

app = FastAPI(
    title="AgenteLegal",
    version="0.2.0",
    description="Cross-industry FAST DEMO for evidence-backed legal intelligence.",
)


def get_runtime() -> GroundedLegalRuntime:
    """Runtime dependency.

    The production GraphRAG/ADK wiring is attached behind this boundary.
    Tests override it with deterministic retrieval.
    """
    raise RuntimeError("Grounded runtime is not configured yet")


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
        "message": "Grounded FastAPI contract available under /api/v1.",
    }


@app.post("/api/v1/query", response_model=GroundedResponse)
def query_legal(
    request: QueryRequest,
    runtime: GroundedLegalRuntime = Depends(get_runtime),
) -> GroundedResponse:
    return runtime.query(
        question=request.question,
        top_k=request.top_k,
        document_ids=request.document_ids,
    )


@app.post("/api/v1/compare", response_model=GroundedResponse)
def compare_legal(
    request: CompareRequest,
    runtime: GroundedLegalRuntime = Depends(get_runtime),
) -> GroundedResponse:
    return runtime.compare(
        question=request.question,
        document_ids=request.document_ids,
        top_k=request.top_k,
    )
