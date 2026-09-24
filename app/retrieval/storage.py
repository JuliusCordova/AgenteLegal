from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from google.cloud import storage


class GCSArtifactStore:
    def __init__(self, bucket_name: str, project: str) -> None:
        self.client = storage.Client(project=project)
        self.bucket = self.client.bucket(bucket_name)

    def upload_file(self, local_path: Path, object_name: str) -> None:
        blob = self.bucket.blob(object_name)
        blob.upload_from_filename(str(local_path))

    def download_text(self, object_name: str) -> str:
        blob = self.bucket.blob(object_name)
        return blob.download_as_text()

    def upload_json(self, payload: dict[str, Any], object_name: str) -> None:
        blob = self.bucket.blob(object_name)
        blob.upload_from_string(
            json.dumps(payload, ensure_ascii=False),
            content_type="application/json",
        )
