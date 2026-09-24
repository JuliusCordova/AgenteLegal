# Development Loop — GitHub + Actions + GCP Cloud Shell

## Objective

Accelerate implementation while keeping source code and GCP validation evidence traceable in the repository.

## Loop

```mermaid
flowchart LR
    DEV[Development Branch] --> PUSH[Push GitHub]
    PUSH --> CI[GitHub Actions]
    CI --> PR[Pull Request]
    PR --> CS[Cloud Shell git pull]
    CS --> GCP[Real GCP Validation]
    GCP --> EVID[Evidence in Repository]
    EVID --> PUSH2[Commit + Push]
    PUSH2 --> CI2[GitHub Actions Re-run]
    CI2 --> MERGE[Merge]
```

## Responsibility split

### GitHub Actions
Fast, deterministic validation without cloud secrets:
- unit tests;
- Python compilation;
- Docker build;
- offline GraphRAG smoke;
- evidence directory validation.

### GCP Cloud Shell
Real-cloud validation:
- authenticated GCP context;
- GCS access;
- Vertex AI / Gemini calls;
- retrieval index build/upload;
- later Cloud Run deploy/smoke.

Google Cloud client libraries use Application Default Credentials. Cloud Shell already provides the authenticated cloud context, so this FAST DEMO does not require storing broad GCP credentials in GitHub.

## One-time setup

```bash
git clone https://github.com/JuliusCordova/AgenteLegal.git
cd AgenteLegal

git checkout feature/sprint-2-dev-loop
source config/gcp.env.example
make cloud-bootstrap
```

## Daily development sync

```bash
cd ~/AgenteLegal
bash scripts/cloudshell/pull_latest.sh feature/sprint-2-dev-loop
source config/gcp.env.example
```

## Generate evidence

```bash
make cloud-evidence
```

Evidence is written to:

```text
docs/evidence/generated/YYYYMMDDTHHMMSSZ/
```

Each evidence bundle records the exact Git SHA and branch.

## Commit evidence

```bash
bash scripts/cloudshell/commit_evidence.sh
```

The push triggers GitHub Actions again, so the branch is validated both locally in GCP and centrally in GitHub.

## Development rule

> Cloud-affecting implementation should not merge until the exact candidate commit has Cloud Shell evidence.

## FAST DEMO security posture

For now, GitHub Actions does not receive GCP service-account keys.

If automated cloud deployment becomes useful later, prefer Workload Identity Federation rather than long-lived service-account JSON keys.
