# FAST DEMO Implementation Plan

## Sprint 0 — Foundation
Repository, FastAPI runtime skeleton, GCP baseline and test harness.

## Sprint 1 — Legal Retrieval + Experimental GraphRAG
- representative cross-industry/synthetic corpus
- replaceable jurisdiction/legal knowledge packs
- ingestion and structure-aware chunking
- metadata and embeddings/search
- vector RAG baseline
- experimental GraphRAG
- retrieval benchmark and citation mapping

### Gate 1
> Can the system retrieve the correct legal evidence, and does GraphRAG materially improve connected-knowledge cases?

## Sprint 2 — Evidence-Driven Development Loop
- GitHub Actions validation
- Cloud Shell authenticated validation
- GCS artifact-store check
- deterministic retrieval smoke
- versioned evidence bundles
- candidate -> evidence -> merge workflow

### Gate 2
> Can cloud-affecting changes be validated against real GCP and leave reproducible evidence?

## Sprint 3 — Grounded Runtime Contract
- FastAPI API contract
- Google ADK / Gemini runtime
- retrieval tool contract
- grounded response contract
- citations/evidence
- uncertainty/abstention
- clause comparison API
- experimental in-process specialist routing
- single/simple behavior retained as comparison baseline

### Gate 3
> Can the backend answer and compare without inventing evidence, and is extra agentic complexity justified by measurements?

## Sprint 4 — React Legal Workbench
- React frontend
- FastAPI integration
- Nielsen usability baseline
- loading/success/no-evidence/error/retry states
- document selection
- source inspection
- clause comparison
- human legal-review boundary

### Gate 4
> Can a legal user complete the main demo flow clearly and verify the evidence?

## Sprint 5 — Golden Evals + Cloud Run Demo
- 20-30 representative legal eval cases
- vector RAG vs GraphRAG evidence
- single/simple vs multi-agent evidence where measurable
- groundedness/citation evaluation
- regression cases
- latency
- cost per successful legal outcome
- Cloud Run candidate
- smoke evidence
- executive demo script

### Gate 5
> Is quality, traceability, latency and cost sufficient to promote selected capabilities toward MVP?

> Evidence, not architectural sophistication or calendar time, determines promotion.
