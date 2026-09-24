# FAST DEMO — GraphRAG + Multi-Agent

## Objective

Demonstrate connected legal reasoning across synthetic contracts and Peruvian legal norms without paying for a managed graph or vector database.

## Component architecture

~~~mermaid
flowchart TB
    U[Legal User] --> UI[Simple Web UI]
    UI --> CR[Cloud Run]

    CR --> ORCH[ADK Orchestrator Agent]
    ORCH --> RETA[Retrieval Agent]
    ORCH --> CLA[Contract Analysis Agent]
    ORCH --> NORMA[Legal Norm Agent]
    ORCH --> VAL[Legal Validation Agent]

    RETA --> GR[GraphRAG Retrieval Layer]
    CLA --> GR
    NORMA --> GR
    VAL --> GR

    GR --> VEC[Vector Retrieval in Memory]
    GR --> GRAPH[Graph Expansion in Memory]

    VEC --> GCS[(Cloud Storage)]
    GRAPH --> GCS

    GCS --> C[Contracts]
    GCS --> N[Peruvian Legal Knowledge Base]
    GCS --> A[Chunks + Embeddings + Graph]

    RETA --> GEM[Vertex AI / Gemini]
    CLA --> GEM
    NORMA --> GEM
    VAL --> GEM

    VAL --> CIT[Citations / Evidence]
    CIT --> UI
~~~

## Agent responsibilities

| Agent | Role |
|---|---|
| Orchestrator | Routes the request and synthesizes specialist results. |
| Retrieval Agent | Executes vector search and graph expansion. |
| Contract Analysis Agent | Compares clauses, obligations, exceptions and risk language. |
| Legal Norm Agent | Connects contractual clauses with relevant Peruvian legal norms. |
| Legal Validation Agent | Challenges unsupported conclusions and checks citation coverage. |

## Graph model

~~~mermaid
graph LR
    CO[Company] -->|SIGNS| CT[Contract]
    CT -->|HAS_CLAUSE| CL[Clause]
    CL -->|ABOUT| TP[Legal Topic]
    CL -->|REFERENCES| NR[Legal Norm]
    NR -->|REGULATES| TP
    CL -->|SIMILAR_TO| CL2[Clause]
    CT -->|GOVERNED_BY| PE[Peru]
~~~

## Low-cost storage

Cloud Storage persists:

~~~text
corpus/
  contracts/
  legal_norms/

index/
  chunks.jsonl
  embeddings.jsonl
  graph.json
  metadata.json

evals/
~~~

Cloud Storage is the durable object store, not the search engine.

At runtime the Cloud Run process loads the compact index into memory and executes cosine similarity plus graph expansion.

## Retrieval sequence

~~~text
Question
  ↓
Query embedding
  ↓
Vector top-k
  ↓
Map chunks to graph nodes
  ↓
Expand 1-hop / 2-hop legal relationships
  ↓
Re-score context
  ↓
Return clauses + norms + provenance
~~~

## Why GraphRAG here

The legal demo intentionally tests questions where relevant facts are distributed across contracts and norms. GraphRAG is designed to augment vector retrieval with explicit entities and relationships, which is useful for connecting the dots across a private corpus.

## Cost principle

> Demonstrate GraphRAG as a reasoning pattern without paying for GraphRAG as a managed infrastructure stack.

The demo therefore avoids:
- managed graph database;
- managed vector database;
- distributed agent deployment;
- A2A network calls between specialists.

All specialists run in-process inside one Cloud Run service for FAST DEMO.
