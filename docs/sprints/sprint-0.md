# Sprint 0 — Foundation

## Objective
Prepare AgenteLegal to begin implementation of the FAST DEMO using the proven GCP baseline from `JuliusCordova/portafoliodatagob`, while keeping the architecture intentionally lean.

## Reused GCP baseline
- GCP project: `proyectopersonal-480420`
- Region: `us-central1`
- Runtime baseline: Cloud Run
- Container registry pattern: Artifact Registry
- Delivery pattern: build → deploy candidate → smoke → evidence
- Identity pattern: dedicated service account
- Principle: evidence before promotion

## Sprint 0 scope
- repository structure;
- Python application skeleton;
- health endpoint;
- configuration management;
- GCP environment template;
- Dockerfile;
- local developer commands;
- unit smoke test;
- placeholders for agent, retrieval and tools;
- architecture decision record;
- readiness checklist for Sprint 1.

## Explicitly out of scope
- document ingestion;
- chunking;
- embeddings;
- vector index;
- ADK agent implementation;
- Gemini model invocation;
- Cloud Run deployment;
- Terraform;
- private networking;
- multi-agent;
- GraphRAG.

## Exit criteria
- [x] runnable application skeleton;
- [x] health endpoint defined;
- [x] configuration externalized;
- [x] GCP project baseline recorded;
- [x] Docker container definition;
- [x] test command defined;
- [x] future agent/retrieval/tool boundaries represented;
- [x] Sprint 1 entry criteria documented.

## Sprint 1 entry criteria
1. representative legal corpus selected;
2. supported file types confirmed;
3. chunking strategy defined;
4. retrieval baseline selected;
5. evaluation questions available.

> Sprint 0 prepares the runway. It does not prematurely build production infrastructure.
