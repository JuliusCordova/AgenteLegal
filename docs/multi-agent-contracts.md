# Multi-Agent Contracts — FAST DEMO

The FAST DEMO uses a small in-process multi-agent topology.

## Orchestrator Agent

Input:
- user question
- conversation context

Responsibilities:
- classify intent;
- decide which specialists to invoke;
- synthesize outputs;
- preserve citations;
- never invent legal authority.

## Retrieval Agent

Input:
- normalized legal question

Output:
- ranked chunks;
- graph-connected context;
- provenance;
- retrieval scores.

Tools:
- vector retrieval;
- graph expansion.

## Contract Analysis Agent

Input:
- contract clauses and related context.

Output:
- clause interpretation;
- cross-contract comparison;
- obligations/exceptions;
- uncertainty.

Must not:
- provide final legal approval.

## Legal Norm Agent

Input:
- clause/topic plus connected norms.

Output:
- relevant Peruvian norms;
- explanation of relevance;
- caveats about applicability.

Must distinguish:
- explicit contractual reference;
- inferred topical relevance.

## Legal Validation Agent

Input:
- draft analysis;
- evidence/citations.

Output:
- validated response or challenge;
- unsupported claims;
- missing evidence;
- citation coverage.

## FAST DEMO deployment rule

All agents run in the same Cloud Run process.

A2A/network-separated agents are deferred until independent scale, security, ownership, or release lifecycle justifies them.
