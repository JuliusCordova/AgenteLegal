from __future__ import annotations

import json
import os
from pathlib import Path

from app.retrieval.chunker import chunk_markdown
from app.retrieval.embeddings import GeminiEmbedder
from app.retrieval.graph_builder import build_legal_graph


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "data" / "contracts"
NORMS = ROOT / "data" / "legal_norms"
OUTPUT = ROOT / "data" / "processed"


def main() -> None:
    project = os.getenv("LEGAL_GCP_PROJECT", "proyectopersonal-480420")
    region = os.getenv("LEGAL_GCP_REGION", "us-central1")
    model = os.getenv("LEGAL_EMBEDDING_MODEL", "gemini-embedding-001")
    dimensions = int(os.getenv("LEGAL_EMBEDDING_DIMENSIONS", "768"))

    chunks = []
    for path in sorted(CONTRACTS.glob("*.md")):
        chunks.extend(chunk_markdown(path, "contract"))
    for path in sorted(NORMS.glob("*.md")):
        chunks.extend(chunk_markdown(path, "legal_norm"))

    graph = build_legal_graph(chunks)
    embedder = GeminiEmbedder(
        model=model,
        project=project,
        location=region,
        output_dimensionality=dimensions,
    )

    OUTPUT.mkdir(parents=True, exist_ok=True)

    with (OUTPUT / "chunks.jsonl").open("w", encoding="utf-8") as fh:
        for chunk in chunks:
            fh.write(json.dumps(chunk.to_dict(), ensure_ascii=False) + "\n")

    with (OUTPUT / "embeddings.jsonl").open("w", encoding="utf-8") as fh:
        for chunk in chunks:
            vector = embedder.embed_document(
                f"{chunk.title}\n{chunk.section}\n{chunk.text}"
            )
            fh.write(
                json.dumps(
                    {
                        "chunk_id": chunk.chunk_id,
                        "vector": vector,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

    (OUTPUT / "graph.json").write_text(
        json.dumps(graph.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    metadata = {
        "project": project,
        "region": region,
        "embedding_model": model,
        "embedding_dimensions": dimensions,
        "chunk_count": len(chunks),
        "graph_nodes": len(graph.nodes),
        "graph_edges": len(graph.edges),
    }
    (OUTPUT / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
