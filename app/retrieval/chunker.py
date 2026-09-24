from __future__ import annotations

import hashlib
from pathlib import Path

from app.retrieval.models import Chunk


def _stable_id(*parts: str) -> str:
    raw = "::".join(parts).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def chunk_markdown(path: Path, document_type: str) -> list[Chunk]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = path.stem.replace("_", " ").title()
    section = "document"
    buffer: list[str] = []
    chunks: list[Chunk] = []

    def flush() -> None:
        nonlocal buffer
        body = "\n".join(buffer).strip()
        if not body:
            buffer = []
            return
        chunk_id = _stable_id(str(path), section, body)
        node_id = f"chunk:{chunk_id}"
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                document_id=_stable_id(str(path)),
                document_type=document_type,
                title=title,
                section=section,
                text=body,
                source_path=str(path),
                node_id=node_id,
            )
        )
        buffer = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            continue
        if stripped.startswith("## "):
            flush()
            section = stripped[3:].strip()
            continue
        buffer.append(line)

    flush()
    return chunks
