from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from app.config import settings
from app.retrieval.embeddings import GeminiEmbedder
from app.retrieval.loader import load_gcs, load_local
from app.runtime import GroundedLegalRuntime


@lru_cache(maxsize=1)
def build_runtime() -> GroundedLegalRuntime:
    model = os.getenv("LEGAL_EMBEDDING_MODEL", "gemini-embedding-001")
    dimensions = int(os.getenv("LEGAL_EMBEDDING_DIMENSIONS", "768"))
    embedder = GeminiEmbedder(
        model=model,
        project=settings.gcp_project,
        location=settings.gcp_region,
        output_dimensionality=dimensions,
    )

    bucket = os.getenv("LEGAL_GCS_BUCKET", "").strip()
    if bucket:
        retriever = load_gcs(bucket, settings.gcp_project, embedder)
    else:
        retriever = load_local(Path("data/processed"), embedder)

    minimum_score = float(os.getenv("LEGAL_MINIMUM_RETRIEVAL_SCORE", "0.15"))
    return GroundedLegalRuntime(retriever=retriever, minimum_score=minimum_score)
