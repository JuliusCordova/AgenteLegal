from __future__ import annotations

import json
from pathlib import Path

from app.retrieval.embeddings import GeminiEmbedder
from app.retrieval.graph import LegalGraph
from app.retrieval.graphrag import GraphRAGRetriever
from app.retrieval.models import Chunk
from app.retrieval.storage import GCSArtifactStore
from app.retrieval.vector_store import InMemoryVectorStore, VectorRecord


ARTIFACTS = ("chunks.jsonl", "embeddings.jsonl", "graph.json")


def _chunk(payload: dict) -> Chunk:
    return Chunk(**payload)


def _build(chunks_text: str, embeddings_text: str, graph_text: str, embedder: GeminiEmbedder) -> GraphRAGRetriever:
    chunks = {
        item["chunk_id"]: _chunk(item)
        for item in (json.loads(line) for line in chunks_text.splitlines() if line.strip())
    }
    vectors = {
        item["chunk_id"]: item["vector"]
        for item in (json.loads(line) for line in embeddings_text.splitlines() if line.strip())
    }
    records = [
        VectorRecord(chunk=chunk, vector=vectors[chunk_id])
        for chunk_id, chunk in chunks.items()
        if chunk_id in vectors
    ]
    if not records:
        raise RuntimeError("Retrieval index contains no vector records")
    return GraphRAGRetriever(
        embedder=embedder,
        vector_store=InMemoryVectorStore(records),
        graph=LegalGraph.from_dict(json.loads(graph_text)),
    )


def load_local(processed_dir: Path, embedder: GeminiEmbedder) -> GraphRAGRetriever:
    return _build(
        (processed_dir / "chunks.jsonl").read_text(encoding="utf-8"),
        (processed_dir / "embeddings.jsonl").read_text(encoding="utf-8"),
        (processed_dir / "graph.json").read_text(encoding="utf-8"),
        embedder,
    )


def load_gcs(bucket: str, project: str, embedder: GeminiEmbedder) -> GraphRAGRetriever:
    store = GCSArtifactStore(bucket_name=bucket, project=project)
    return _build(
        store.download_text("index/chunks.jsonl"),
        store.download_text("index/embeddings.jsonl"),
        store.download_text("index/graph.json"),
        embedder,
    )
