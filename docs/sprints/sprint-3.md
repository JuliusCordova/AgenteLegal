# Sprint 3 — Grounded Runtime Contract

## Objective

Connect the proven retrieval foundation to a testable FastAPI runtime contract before building the React experience.

## Scope

1. Reconcile the cross-industry product boundary with the existing GraphRAG/multi-agent experiment.
2. Expose a stable FastAPI contract:
   - GET /health
   - GET /api/v1/documents
   - POST /api/v1/query
   - POST /api/v1/compare
3. Connect query/compare requests to grounded retrieval and agent behavior.
4. Return explicit evidence objects.
5. Return an explicit no-evidence/abstention state.
6. Keep the browser/model boundary server-side: React will never call Gemini directly.
7. Preserve GraphRAG and multi-agent as experiments measured against simpler baselines.
8. Generate tests and Cloud Shell evidence before merge.

## API response principles

A grounded response must expose:
- answer;
- status;
- evidence[];
- document identity;
- section/chunk identity where available;
- retrieval/provenance metadata required for inspection.

No-evidence must be a first-class response state, not a fabricated answer.

## Gate 3A

> Can FastAPI execute the legal flow end-to-end and return inspectable evidence or safe abstention without a UI?

## Required evidence

- unit tests;
- API contract tests;
- retrieval smoke;
- known grounded query;
- known unsupported query;
- comparison query;
- compile;
- Cloud Shell GCP checks.

## Deferred

- React implementation;
- visual styling;
- enterprise authentication;
- OCR;
- managed vector/graph infrastructure;
- network-separated agents;
- client-specific integrations.

## Exit criteria

Sprint is complete when the API can demonstrate:
Question -> retrieval -> grounded reasoning -> answer + evidence

and:
Unsupported question -> explicit abstention

and:
Comparison -> evidence from each compared document.

## Implementation checkpoint

The FastAPI contract is now wired to persisted GraphRAG artifacts. Runtime loads the compact index from GCS when LEGAL_GCS_BUCKET is configured, otherwise from data/processed for local development. Query embeddings use Vertex AI/Gemini through the existing GeminiEmbedder. Generation/synthesis remains the next increment; current answers deliberately expose retrieved evidence rather than inventing synthesis.
