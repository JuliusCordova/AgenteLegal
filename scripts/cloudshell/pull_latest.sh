#/usr/bin/env bash
set -euo pipefail

BRANCH="${1:-main}"

git fetch origin
git checkout "${BRANCH}"
git pull --ff-only origin "${BRANCH}"

echo "Updated to $(git rev-parse --short HEAD) on ${BRANCH}"
