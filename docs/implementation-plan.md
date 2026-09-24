# FAST DEMO Implementation Plan

## Sprint 0 — Foundation
Repository, runtime skeleton, GCP baseline and test harness.

## Sprint 1 — Legal Retrieval
- representative corpus
- ingestion
- structure-aware chunking
- metadata
- embeddings/search
- retrieval benchmark
- citation mapping

### Gate 1
> Can the system retrieve the correct legal evidence?

## Sprint 2 — Agent + Grounded Answers
- Google ADK single agent
- Vertex AI / Gemini
- retrieval tool contract
- grounded response contract
- citations
- uncertainty behavior

### Gate 2
> Can the agent answer without inventing evidence?

## Sprint 3 — Clause Comparison + UI
- clause comparison
- simple legal review UI
- Nielsen baseline
- loading/error/success states
- source inspection
- human review boundary

### Gate 3
> Can legal users compare material clauses reliably?

## Sprint 4 — Evals + Cloud Run Evidence
- representative legal eval set
- groundedness/citation evaluation
- regression cases
- latency
- cost per successful legal outcome
- Cloud Run candidate
- smoke evidence

### Gate 4
> Is quality, latency and cost good enough to continue to MVP?

> Evidence, not calendar time, determines promotion.
