from fastapi import Depends, FastAPI

from app.api_models import CompareRequest, EnterpriseQueryRequest, EnterpriseQueryResponse, GroundedResponse, QueryRequest
from app.config import settings
from app.runtime import GroundedLegalRuntime
from app.runtime_factory import build_runtime
from app.orchestration.domains import LegalDomainOrchestrator, PortfolioDomainOrchestrator
from app.orchestration.meta import EnterpriseMetaOrchestrator
from app.orchestration.registry import CapabilityRegistry

app = FastAPI(
    title="AgenteLegal",
    version="0.2.0",
    description="FAST DEMO enterprise agent gateway with Legal and Portfolio domains.",
)


def get_runtime() -> GroundedLegalRuntime:
    """Return the cached production retrieval runtime.

    Tests override this dependency with deterministic retrieval.
    """
    return build_runtime()


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


def get_meta_orchestrator() -> EnterpriseMetaOrchestrator:
    legal_runtime = build_runtime()
    return EnterpriseMetaOrchestrator(
        registry=CapabilityRegistry(),
        domains={
            "legal": LegalDomainOrchestrator(legal_runtime),
            "portfolio": PortfolioDomainOrchestrator(),
        },
    )


@app.get("/api/v1/capabilities")
def capabilities() -> list[dict[str, str]]:
    return CapabilityRegistry().catalog()


@app.post("/api/v1/ask", response_model=EnterpriseQueryResponse)
def ask_enterprise(
    request: EnterpriseQueryRequest,
    orchestrator: EnterpriseMetaOrchestrator = Depends(get_meta_orchestrator),
) -> EnterpriseQueryResponse:
    result = orchestrator.handle(request.question, request.context)
    return EnterpriseQueryResponse(
        status=result.status,
        answer=result.answer,
        consulted_domains=result.consulted_domains,
        routing_events=result.routing_events,
        domain_results=[item.model_dump() for item in result.domain_results],
    )
