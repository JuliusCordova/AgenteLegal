# Sprint 3 — Enterprise Meta-Orchestrator + Grounded Domain Contracts

## Objective
Turn the existing Legal grounded runtime into the first domain behind a reusable enterprise conversational gateway, and establish Portfolio as the second demo domain.

## Scope
1. Unified FastAPI conversational entry.
2. Enterprise Meta-Orchestrator using Google ADK/Gemini.
3. Capability Registry with Legal and Portfolio domain contracts.
4. Preserve existing Legal query/compare and GraphRAG runtime behind Legal Domain Orchestrator.
5. Add a minimal evidence-backed Portfolio demo adapter/orchestrator.
6. Support single-domain routing and one Legal + Portfolio cross-domain scenario.
7. Return consulted domains, routing events and evidence/provenance.
8. Safe abstention for unsupported capabilities.
9. Keep all components in-process in one Cloud Run runtime.
10. Produce deterministic tests and Cloud Shell evidence before merge.

## Gate 3A
> Can the unified backend route a request to the correct domain and preserve inspectable evidence?

## Gate 3B
> Can a cross-domain executive question coordinate Legal + Portfolio and return one response without losing provenance?

## Required evidence
- unit and API contract tests;
- Legal routing test;
- Portfolio routing test;
- cross-domain routing test;
- unknown-capability abstention;
- Legal grounded/no-evidence tests;
- compile;
- Cloud Shell GCP checks.

## Deferred
- distributed A2A;
- separate Cloud Run services per domain;
- enterprise IAM/ABAC;
- write/approval actions;
- production portfolio integrations;
- React visual implementation until backend orchestration contract is stable.

## Exit criteria
One entry point demonstrates:

Question → capability discovery → domain orchestration → evidence-backed response

and:

Cross-domain question → Legal + Portfolio → consolidated response + domain provenance

and:

Unsupported question → explicit abstention.
