# AgenteLegal / Enterprise Agent Gateway — Minimum Sufficient Specification

## 1. Business Intent

### Problem
Business users should not need to know which agent, application or domain owns the answer. As enterprise agents grow, fragmented entry points create friction and make cross-domain questions harder to resolve.

### Desired Outcome
Provide one conversational entry point — **“¿En qué te ayudo?”** — that understands intent, discovers the relevant enterprise capability and delegates to one or more domain orchestrators while preserving each domain's evidence, rules and human-review boundaries.

AgenteLegal becomes the **first domain implementation**, not the enterprise entry point itself. Portfolio Management is the second reference domain for the Enterprise executive demo.

### North Star
Reduce the path from a business question to a coordinated, evidence-backed answer across enterprise agent domains.

## 2. Scope — FAST DEMO

### In Scope
- single conversational entry point;
- Enterprise Meta-Orchestrator;
- Capability Registry;
- intent/domain routing;
- Legal Domain Orchestrator;
- Portfolio Domain Orchestrator;
- single-domain and cross-domain requests;
- shared conversation context;
- evidence/provenance in domain results;
- observable routing in the UI;
- human-review boundary;
- React + FastAPI + Google ADK/Gemini on GCP;
- one low-cost Cloud Run runtime for the FAST DEMO.

### Out of Scope
- autonomous business or legal approvals;
- arbitrary peer-to-peer agent calls;
- distributed A2A deployment;
- production enterprise IAM/ABAC;
- enterprise-wide ingestion;
- irreversible/write actions;
- service mesh or separate runtime per agent.

## 3. Actors
- Executive / Business User
- Legal Specialist
- Portfolio / PMO User
- Administrator

## 4. Core User Stories

### US-001 — Unified entry
As a business user, I want to ask “¿En qué te ayudo?” in natural language without choosing an agent.

### US-002 — Domain delegation
As a business user, I want the platform to identify the relevant domain and delegate transparently.

### US-003 — Context continuity
As a business user, I want follow-up questions to retain the relevant business context.

### US-004 — Cross-domain coordination
As an executive, I want one question to coordinate Legal and Portfolio when both domains are required.

### US-005 — Traceability
As a reviewer, I want to see which domains were consulted and the evidence supporting material findings.

## 5. Functional Requirements
- FR-001: expose a single conversational API/UI entry point.
- FR-002: classify the request against registered capabilities.
- FR-003: select one or more Domain Orchestrators.
- FR-004: delegate only the minimum context required by the selected domain.
- FR-005: support Legal as the first evidence-backed domain.
- FR-006: support Portfolio as the second demo domain.
- FR-007: consolidate multi-domain results into one executive response without losing provenance.
- FR-008: expose routing status/events for UI feedback.
- FR-009: preserve safe abstention when no registered capability/evidence can support the request.
- FR-010: keep domain-specific rules, tools and knowledge behind each Domain Orchestrator.
- FR-011: keep final legal/business approvals human.

## 6. Relevant NFRs
- NFR-001 Traceability: material claims must retain domain and evidence provenance.
- NFR-002 Security boundary: the Meta-Orchestrator must not bypass a domain's authorization boundary.
- NFR-003 Least context: share only context needed by the selected domain.
- NFR-004 Cost: FAST DEMO uses one scale-to-zero runtime and avoids unnecessary LLM hops.
- NFR-005 Extensibility: adding a domain should primarily register a capability contract, not rewrite routing logic.
- NFR-006 Observability: selected domains, latency, failures and abstention must be observable.
- NFR-007 UX: user must receive visible progress while orchestration is occurring.

## 7. Acceptance Criteria

### AC-001 Single-domain routing
Given a legal question
When the user submits it through the unified entry
Then the Meta-Orchestrator selects Legal
And returns evidence-backed output.

### AC-002 Portfolio routing
Given a portfolio/project question
When submitted through the same entry
Then the Meta-Orchestrator selects Portfolio
And the user does not need to change agents.

### AC-003 Cross-domain
Given a question requiring project status and contractual risk
When the Meta-Orchestrator evaluates the request
Then it coordinates Portfolio and Legal
And returns one consolidated response preserving each domain's provenance.

### AC-004 Follow-up context
Given the user established a project or contract context
When a follow-up refers to it implicitly
Then the relevant context is retained without forcing the user to repeat it.

### AC-005 Unknown capability
Given no registered domain can support a request
When it is submitted
Then the system states that no available capability can support it
And does not fabricate an answer.

### AC-006 Observable routing
Given orchestration is running
Then the UI can show states such as understanding request, identifying domain, consulting Legal/Portfolio and preparing response.

## 8. Business Rules
- BR-001: the Meta-Orchestrator coordinates; it does not own domain expertise.
- BR-002: Domain Orchestrators own their specialist agents, tools, knowledge and domain rules.
- BR-003: Domain Orchestrators do not call each other arbitrarily; cross-domain coordination returns through the Meta-Orchestrator.
- BR-004: evidence-backed answers are preferred over unsupported synthesis.
- BR-005: no source means no authoritative legal conclusion.
- BR-006: final approvals remain human.
- BR-007: GraphRAG remains an experimental Legal-domain capability measured against vector RAG.
- BR-008: all FAST DEMO orchestrators/agents may run in-process in one Cloud Run service.
- BR-009: Enterprise is the executive demo context, not a hardcoded dependency of the reusable core.

## 9. Orchestration Model

~~~text
User / React
     ↓
Enterprise Meta-Orchestrator
     ↓
Capability Registry
     ├── Legal Domain Orchestrator
     │      └── Legal Specialists → GraphRAG / Contracts / Legal Knowledge
     └── Portfolio Domain Orchestrator
            └── Portfolio Specialists → Project / Portfolio Demo Data
     ↓
Cross-domain synthesis when required
     ↓
Answer + consulted domains + evidence + human-review boundary
~~~

## 10. Capability Contract
Each domain registers at minimum:
- id and domain;
- description;
- supported capabilities/intents;
- input/context contract;
- output contract;
- evidence/provenance contract;
- permissions/security scope;
- human-approval requirements;
- health/availability metadata.

The Meta-Orchestrator routes by capability, not hardcoded client-specific logic.

## 11. Agent Contracts

### Enterprise Meta-Orchestrator
May:
- understand intent;
- query the Capability Registry;
- select one or more domains;
- coordinate domain results;
- maintain bounded conversation context;
- synthesize an executive response with provenance.

May not:
- bypass domain security;
- invent domain evidence;
- make final legal/business approvals;
- directly replace specialist domain logic.

### Legal Domain Orchestrator
Owns legal retrieval, contract analysis, legal knowledge/norm analysis and legal validation. Existing grounded query/compare APIs remain valid internal domain capabilities.

### Portfolio Domain Orchestrator
Owns project/portfolio status, demand, dependencies and portfolio risk for the demo corpus. It must return structured findings and provenance rather than ungrounded narrative.

## 12. FAST DEMO Success Criteria
The demo is successful when:
- the user starts from one “¿En qué te ayudo?” experience;
- Legal-only questions route to Legal;
- Portfolio-only questions route to Portfolio;
- at least one executive scenario coordinates both domains;
- routing is visible and inspectable;
- evidence remains attributable to its originating domain;
- unsupported requests abstain safely;
- the architecture remains one low-cost GCP runtime while preserving logical boundaries.
