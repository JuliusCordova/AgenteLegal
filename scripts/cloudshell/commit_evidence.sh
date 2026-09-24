#!/usr/bin/env bash
set -euo pipefail

if ! git diff --quiet -- docs/evidence/generated || [ -n "$(git ls-files --others --exclude-standard docs/evidence/generated)" ]; then
  git add docs/evidence/generated
  git commit -m "evidence: Cloud Shell validation"
  git push
  echo "Evidence committed and pushed."
else
  echo "No new evidence to commit."
fi
