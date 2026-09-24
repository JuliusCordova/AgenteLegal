from __future__ import annotations

import os
from pathlib import Path

from app.retrieval.storage import GCSArtifactStore


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def main() -> None:
    project = os.getenv("LEGAL_GCP_PROJECT", "proyectopersonal-480420")
    bucket = os.environ["LEGAL_GCS_BUCKET"]
    store = GCSArtifactStore(bucket_name=bucket, project=project)

    for name in ("chunks.jsonl", "embeddings.jsonl", "graph.json", "metadata.json"):
        local = PROCESSED / name
        if not local.exists():
            raise FileNotFoundError(f"Missing artifact: {local}")
        object_name = f"index/{name}"
        store.upload_file(local, object_name)
        print(f"uploaded gs://{bucket}/{object_name}")


if __name__ == "__main__":
    main()
