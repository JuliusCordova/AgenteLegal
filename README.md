# AgenteLegal

Primer caso real de validación end-to-end de **DevPattern**.

Objetivo inicial: construir un agente legal en GCP para consulta y análisis de contratos/documentos legales, empezando por **FAST DEMO** y evolucionando por evidencia hacia **MVP** y **PRODUCT**.

> Start lean. Scale by evidence.

## GCP baseline

Reutiliza el baseline probado de `JuliusCordova/portafoliodatagob`:

- Project: `proyectopersonal-480420`
- Region: `us-central1`
- Runtime: Cloud Run
- Registry: Artifact Registry
- Delivery direction: candidate → smoke → evidence → promotion

## Sprint 0

Estado: foundation implemented.

Incluye:
- FastAPI skeleton;
- `/health`;
- configuración externa;
- Dockerfile compatible con Cloud Run;
- test smoke;
- límites iniciales para agent, retrieval y tools;
- ADR del baseline GCP;
- plan FAST DEMO por sprints.

## Local run

```bash
python -m pip install -r requirements.txt
make test
make dev
```

Health:

```bash
curl http://localhost:8080/health
```

## Roadmap

```text
Sprint 0  Foundation
   ↓
Sprint 1  Legal Retrieval
   ↓
Sprint 2  ADK Agent + Gemini + Grounded Answers
   ↓
Sprint 3  Clause Comparison + UI
   ↓
Sprint 4  Evals + Cloud Run Evidence
```

See:
- `SPEC.md`
- `docs/architecture.md`
- `docs/implementation-plan.md`
- `docs/sprints/sprint-0.md`
