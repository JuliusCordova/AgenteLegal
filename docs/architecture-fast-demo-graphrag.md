# FAST DEMO — Enterprise Meta-Orchestrator + Domain Orchestrators

## Executive objective
Demonstrate one conversational enterprise entry point that understands a user's need and coordinates the appropriate agent domains. Legal is the first evidence-backed domain; Portfolio Management is the second reference domain for the Primax C-Level demo.

~~~mermaid
flowchart TB
    U[Executive / Business User] --> UI[React: ¿En qué te ayudo?]
    UI --> API[FastAPI / Cloud Run]
    API --> META[Enterprise Meta-Orchestrator - Google ADK]
    META --> REG[Capability Registry]

    REG --> LEGAL[Legal Domain Orchestrator]
    REG --> PORT[Portfolio Domain Orchestrator]

    LEGAL --> RET[Retrieval Specialist]
    LEGAL --> CLA[Contract Analysis Specialist]
    LEGAL --> NORM[Legal Knowledge Specialist]
    LEGAL --> LVAL[Legal Validation Specialist]

    RET --> GR[Legal GraphRAG]
    CLA --> GR
    NORM --> GR
    LVAL --> GR
    GR --> GCS[(GCS: Legal Corpus + Index)]

    PORT --> PST[Portfolio Status Specialist]
    PORT --> PRISK[Portfolio Risk Specialist]
    PORT --> PDEPS[Dependencies / Demand Specialist]
    PST --> PDATA[(Portfolio Demo Data)]
    PRISK --> PDATA
    PDEPS --> PDATA

    LEGAL --> META
    PORT --> META
    META --> SYN[Grounded Cross-Domain Synthesis]
    SYN --> UI

    META --> GEM[Vertex AI / Gemini]
    LEGAL --> GEM
    PORT --> GEM
~~~

## Responsibility boundaries

| Layer | Responsibility |
|---|---|
| Meta-Orchestrator | Intent, capability discovery, bounded context, domain coordination and final cross-domain synthesis. |
| Capability Registry | Describes available domains and contracts; avoids hardcoded routing branches. |
| Legal Orchestrator | Owns legal specialists, legal tools, GraphRAG and legal evidence. |
| Portfolio Orchestrator | Owns portfolio/project specialists, tools and evidence. |
| Specialists | Execute narrow domain tasks. |
| Knowledge/Tools | Deterministic retrieval, APIs and domain data. |

## Orchestration rule
The Meta-Orchestrator is the only coordinator of cross-domain work in FAST DEMO. Domain Orchestrators return structured results to it; they do not form an uncontrolled peer-to-peer agent mesh.

## Example executive flow

~~~text
“¿Cuál es el estado del proyecto X?”
  → Portfolio

“¿Qué riesgos tiene su contrato?”
  → context keeps Project X
  → Legal

“Dame una visión ejecutiva completa.”
  → Portfolio + Legal
  → Meta-Orchestrator consolidates
  → one response with domain provenance
~~~

## FAST DEMO deployment
All logical orchestrators and specialists run in-process behind one FastAPI/Cloud Run deployment. Logical boundaries are designed now; physical separation, A2A and independent runtimes are deferred until evidence, security, scale or ownership justify them.

## Legal GraphRAG
GraphRAG remains an experimental capability inside the Legal domain. It connects contracts, clauses, topics and replaceable jurisdiction/legal knowledge packs while preserving source provenance. Cloud Storage remains the durable artifact store; the compact index is loaded in memory at runtime.

## Cost principle
> One enterprise experience, multiple logical domains, minimum physical infrastructure.

The demo avoids managed graph/vector databases, distributed agent deployment, service mesh and unnecessary agent-to-agent LLM hops.
