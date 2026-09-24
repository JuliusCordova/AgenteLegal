# AgenteLegal — DevPattern Reference Architecture

## FAST DEMO — GCP

### Executive Purpose

> Prove that legal users can obtain evidence-backed answers from a controlled legal corpus with the minimum viable architecture.

```mermaid
flowchart LR
    U[Legal User] --> UI[Simple Web UI]
    UI --> CR[Cloud Run]
    CR --> ADK[Google ADK - Single Agent]
    ADK --> GEM[Vertex AI / Gemini]
    ADK --> RET[Legal Retrieval Tool]
    RET --> DOC[(Controlled Legal Corpus)]
    RET --> IDX[(Vector / Search Index)]
    ADK --> CIT[Citations / Evidence]
```

| Component | C-Level explanation | Why now |
|---|---|---|
| Simple Web UI | Gives legal users a simple entry point. | Enough to validate usability without overbuilding. |
| Cloud Run | Executes the agent on demand. | Low operational cost and scale-to-zero. |
| Google ADK | Structures agent behavior and tool use. | Keeps orchestration explicit and reusable. |
| Gemini / Vertex AI | Interprets legal questions and synthesizes grounded responses. | Core reasoning capability. |
| Legal Retrieval Tool | Finds relevant legal evidence. | Retrieval must be controlled and testable. |
| Controlled Legal Corpus | Limits the demo to trusted content. | Reduces ambiguity and risk during validation. |
| Vector/Search Index | Accelerates relevant retrieval. | Required for semantic search over documents. |
| Citations / Evidence | Lets legal reviewers verify answers. | Critical trust mechanism for legal use. |

### Why not more?

FAST DEMO intentionally avoids:
- multi-agent;
- GraphRAG;
- Eventarc/PubSub;
- GKE;
- complex private networking;
- dedicated clusters;
- production HA.

These appear only when evidence shows a concrete need.

---

## MVP

### Executive Purpose

> Make the legal assistant repeatable, measurable, integrated and supportable.

```mermaid
flowchart TB
    U[Legal User] --> UI[Web App]
    UI --> CR[Cloud Run Agent API]
    CR --> ADK[ADK Agent]
    ADK --> GEM[Vertex AI]
    ADK --> RET[Hybrid Legal Retrieval]
    RET --> GCS[(Cloud Storage Documents)]
    RET --> IDX[(Managed Search / Vector Index)]
    ADK --> CMP[Clause Comparison Tool]
    CR --> SA[Dedicated Service Account]
    CR --> SM[Secret Manager]
    CR --> OBS[Logging / Monitoring]
    OBS --> EVAL[Legal Eval Dataset]
    CI[Cloud Build] --> AR[Artifact Registry]
    AR --> CR
```

Key MVP additions:
- hybrid retrieval where benchmarked;
- repeatable ingestion;
- dedicated identity;
- secrets management;
- observability;
- legal eval dataset;
- CI/CD;
- regression evidence.

---

## PRODUCT

### Executive Purpose

> Operate legal AI as a governed enterprise capability with permission-aware retrieval, auditability and controlled releases.

```mermaid
flowchart TB
    CH[Enterprise Channels] --> IN[Controlled Ingress]
    IN --> CR[Cloud Run Agent Runtime]
    CR --> ADK[ADK Orchestrator]
    ADK --> RAG[Permission-Aware Legal RAG]
    RAG --> DOC[(Enterprise Legal Sources)]
    RAG --> IDX[(Managed Search / Vector)]
    ADK --> TOOLS[Governed Legal Tools]
    ADK --> HITL[Human Legal Approval]
    CR --> OBS[AgentOps / FinOps / Trace]
    OBS --> EVID[Evidence Pack]
    EVID --> GATE[Promotion Gate]
```

Add only when justified:
- permission-aware retrieval;
- private connectivity;
- enterprise SSO/IAM;
- stronger ingestion lifecycle;
- GraphRAG if benchmark evidence proves value;
- multi-agent only if specialist/security/context boundaries justify it;
- formal promotion/rollback;
- AgentOps/FinOps.

## Evolution Rule

> Start with single-agent RAG. Add architectural complexity only when measured legal quality, security, scale or operability requires it.
