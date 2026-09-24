# ADR-001 — GCP FAST DEMO Baseline

Status: Accepted

## Context
AgenteLegal requires a low-cost, low-operations runtime for its FAST DEMO.

`JuliusCordova/portafoliodatagob` already proves a delivery pattern on GCP using Cloud Run, Artifact Registry, dedicated service accounts, smoke testing and evidence-based promotion.

## Decision
Reuse:

```text
Project: proyectopersonal-480420
Region:  us-central1
```

FAST DEMO direction:

```text
Cloud Run
  ↓
single AgenteLegal application
  ↓
Google ADK (Sprint 2)
  ↓
Vertex AI / Gemini (Sprint 2)
  ↓
retrieval + citations (Sprint 1–2)
```

## Why
- proven project context;
- low operational overhead;
- scale-to-zero;
- no Kubernetes requirement;
- clean path to MVP;
- reuse of deployment/evidence practices.

## Deferred
- GKE;
- VPC/PSC;
- multi-agent;
- Pub/Sub/Eventarc;
- Worker Pools;
- GraphRAG;
- HA;
- DR.

A deferred capability is introduced only when security, scale, latency, asynchronous execution, legal-data sensitivity, operability, or cost evidence justifies it.
