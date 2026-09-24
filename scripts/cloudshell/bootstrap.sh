#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${LEGAL_GCP_PROJECT:-proyectopersonal-480420}"
REGION="${LEGAL_GCP_REGION:-us-central1}"

gcloud config set project "${PROJECT_ID}" >/dev/null

echo "Project: ${PROJECT_ID}"
echo "Region:  ${REGION}"
echo "Account: $(gcloud config get-value account)"

python -m pip install --user -r requirements.txt

echo
echo "Cloud Shell ready."
echo "Next:"
echo "  source config/gcp.env.example"
echo "  make cloud-evidence"
