# Sprint 1 — Legal Retrieval + GraphRAG Foundation

## Objective

Build a low-cost retrieval layer that combines semantic vector search with a legal knowledge graph over:
- four synthetic technology-service contracts;
- a curated Peruvian legal knowledge base.

## Deliverables

- synthetic contract corpus;
- Peruvian legal-norm knowledge cards;
- structure-aware Markdown chunking;
- metadata model;
- embedding provider abstraction;
- Gemini embedding provider;
- local/in-memory cosine vector search;
- legal graph builder;
- GraphRAG retrieval;
- Cloud Storage artifact sync;
- baseline vector-vs-GraphRAG evaluation dataset;
- tests with deterministic fake embeddings.

## Graph entities

- Company
- Contract
- Clause
- LegalTopic
- LegalNorm
- Jurisdiction

## Graph relations

- SIGNS
- HAS_CLAUSE
- ABOUT
- REFERENCES
- REGULATES
- SIMILAR_TO
- GOVERNED_BY

## Gate 1

> Can the retrieval layer find the correct clause and its connected legal norm, with provenance?

## Success criteria

- every indexed chunk has document + section metadata;
- every graph edge has source provenance;
- vector retrieval works without a managed vector database;
- GraphRAG can enrich a vector result with related norm/topic nodes;
- artifacts can be persisted to GCS;
- tests run without calling GCP;
- benchmark contains both questions that vector RAG should answer and questions designed to benefit from graph traversal.

## Cost controls

- embeddings are precomputed;
- embedding dimension is configurable;
- index is compact JSON/JSONL;
- graph is loaded into memory;
- one Cloud Run service;
- Cloud Storage as durable store.
