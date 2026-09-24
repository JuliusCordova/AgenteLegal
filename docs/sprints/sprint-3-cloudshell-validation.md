# Sprint 3 — Cloud Shell Validation

Run this only from an authenticated Google Cloud Shell or another environment with valid GCP credentials.

~~~bash
git fetch origin
git checkout feature/sprint-3-grounded-api
git pull --ff-only origin feature/sprint-3-grounded-api

source config/gcp.env.example
make cloud-bootstrap

# Rebuild Legal GraphRAG artifacts, including the neutral synthetic contract.
make build-index

# Publish the exact candidate artifacts used by the runtime.
make upload-index

# Run unit, orchestration, retrieval and authenticated GCP evidence.
make cloud-evidence
~~~

## Expected gates

The evidence bundle under `docs/evidence/generated/<timestamp>/` must show PASS for:
- unit_tests
- compile
- retrieval_smoke
- meta_orchestrator
- portfolio_grounding
- cross_domain_demo
- gcp_project
- gcp_account
- gcs_bucket
- gcs_index_metadata

## Candidate integrity

Before merge, record:
~~~bash
git rev-parse HEAD
gcloud storage cat gs://$LEGAL_GCS_BUCKET/index/metadata.json
~~~

The GraphRAG metadata must reflect a non-zero chunk count and the evidence bundle must refer to the same Git candidate being promoted.

## Important boundary

The repository contains only synthetic, client-neutral demo data. Rebuilding the index must not introduce customer documents.
