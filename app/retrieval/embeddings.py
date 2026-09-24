from __future__ import annotations

import hashlib
import math
from typing import Protocol

from google import genai
from google.genai import types


class Embedder(Protocol):
    def embed_document(self, text: str) -> list[float]: ...
    def embed_query(self, text: str) -> list[float]: ...


class GeminiEmbedder:
    def __init__(
        self,
        model: str,
        project: str,
        location: str,
        output_dimensionality: int = 768,
    ) -> None:
        self.model = model
        self.output_dimensionality = output_dimensionality
        self.client = genai.Client(
            vertexai=True,
            project=project,
            location=location,
        )

    def _embed(self, text: str, task_type: str) -> list[float]:
        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(
                task_type=task_type,
                output_dimensionality=self.output_dimensionality,
                auto_truncate=True,
            ),
        )
        return list(response.embeddings[0].values)

    def embed_document(self, text: str) -> list[float]:
        return self._embed(text, "RETRIEVAL_DOCUMENT")

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text, "RETRIEVAL_QUERY")


class DeterministicTestEmbedder:
    """Offline deterministic embedder used only by tests and local smoke checks."""

    def __init__(self, dimensions: int = 64) -> None:
        self.dimensions = dimensions

    def _embed(self, text: str) -> list[float]:
        vec = [0.0] * self.dimensions
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            idx = int.from_bytes(digest[:2], "big") % self.dimensions
            vec[idx] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def embed_document(self, text: str) -> list[float]:
        return self._embed(text)

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)
