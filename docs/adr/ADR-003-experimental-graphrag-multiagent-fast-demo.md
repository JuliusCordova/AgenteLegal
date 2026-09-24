# ADR-003 — Experimental GraphRAG + Multi-Agent in FAST DEMO

Status: Accepted as experiment  
Maturity: FAST DEMO

## Context

DevPattern defaults to the simplest architecture that can prove the use case. AgenteLegal already contains a low-cost GraphRAG retrieval layer and an in-process multi-agent topology. Removing them before measuring their value would discard useful implementation evidence; treating them as mandatory architecture would violate progressive SDD.

## Decision

GraphRAG and multi-agent remain in the FAST DEMO as **experimental capabilities**, not as default requirements for future legal implementations.

The baseline comparison remains:
- Vector RAG vs GraphRAG for retrieval quality.
- Single coherent runtime behavior vs specialist multi-agent routing for answer quality, traceability, latency and cost.

All specialists remain in-process. No A2A/network-separated agents are introduced.

## Promotion rule

A capability is promoted to MVP only when evidence demonstrates material value that justifies its added complexity.

GraphRAG must show improvement on cases requiring connected legal relationships, provenance or cross-document/norm traversal.

Multi-agent must show improvement in specialist quality, validation/citation coverage or maintainability that outweighs added latency, token use and failure modes.

If evidence does not justify a capability, simplify.

## Cross-industry boundary

The product core is cross-industry. Peruvian legal norms are a demo knowledge pack, not hardcoded product behavior. Client/jurisdiction-specific knowledge must be replaceable through corpus/configuration.

## Consequences

- Existing work is preserved.
- Complexity becomes testable rather than assumed.
- Golden evaluations must identify which cases are expected to benefit from GraphRAG or specialist routing.
- Architecture evolution is evidence-driven.
