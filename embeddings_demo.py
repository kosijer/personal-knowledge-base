"""
Embedding demo: get vectors with the Gemini embedding API and compare them.

We use the supported `google-genai` package (import: `from google import genai`).
The older `google-generativeai` package is deprecated; embedding calls map to the
same model names and behave the same for this script.
"""

from __future__ import annotations

import math
import os

# Load GOOGLE_API_KEY from .env
from dotenv import load_dotenv

load_dotenv()

from google import genai
from google.genai import errors as genai_errors

# Create a client (uses GOOGLE_API_KEY from the environment)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Requested model name from the learning guide (legacy naming).
# On the current Gemini Developer API, some accounts only expose newer embedding
# models (e.g. gemini-embedding-001). If text-embedding-004 is unavailable, we fall back.
PRIMARY_EMBEDDING_MODEL = "models/text-embedding-004"
FALLBACK_EMBEDDING_MODEL = "models/gemini-embedding-001"

# Remember which model worked so we do not retry PRIMARY on every batch call.
_resolved_embedding_model: str | None = None


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Cosine similarity between two equal-length vectors:
    cos(theta) = (a · b) / (||a|| * ||b||)

    Returns a value in [-1, 1] for typical embeddings (often ~0 to 1 for text).
    """
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same length")
    dot = sum(x * y for x, y in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(x * x for x in vec_a))
    norm_b = math.sqrt(sum(x * x for x in vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def embed_sentences(sentences: list[str]) -> tuple[str, list[list[float]]]:
    """
    Return (model_used, list of embedding vectors), one per sentence in order.
    Tries PRIMARY_EMBEDDING_MODEL first, then FALLBACK_EMBEDDING_MODEL on 404.
    """
    global _resolved_embedding_model

    if _resolved_embedding_model:
        model = _resolved_embedding_model
        response = client.models.embed_content(
            model=model,
            contents=sentences,
        )
        vectors = [emb.values for emb in response.embeddings]
        return model, vectors

    for model in (PRIMARY_EMBEDDING_MODEL, FALLBACK_EMBEDDING_MODEL):
        try:
            response = client.models.embed_content(
                model=model,
                contents=sentences,
            )
            vectors = [emb.values for emb in response.embeddings]
            _resolved_embedding_model = model
            return model, vectors
        except genai_errors.ClientError as exc:
            if exc.code == 404 and model == PRIMARY_EMBEDDING_MODEL:
                print(
                    f"Note: {PRIMARY_EMBEDDING_MODEL} was not available on this API. "
                    f"Using {FALLBACK_EMBEDDING_MODEL} instead."
                )
                continue
            raise
    raise RuntimeError("No embedding model available")


if __name__ == "__main__":
    # --- Part 1: single sentence (original demo) ---
    model_used, vectors_one = embed_sentences(["The moon orbits the Earth."])
    vector = vectors_one[0]
    print(f"Embedding model: {model_used}")

    print("First 5 numbers of the embedding vector:", vector[:5])
    print("Total length (dimensions) of the vector:", len(vector))

    # Conceptually, each number is one coordinate of a high-dimensional vector that
    # represents the *meaning* of the text in embedding space. Similar sentences end
    # up with vectors that point in similar directions (high cosine similarity).
    # The model learned these coordinates from training so that semantic similarity
    # in language corresponds to geometric closeness in this space.

    # --- Part 2: cosine similarity across three sentences ---
    s1 = "The moon orbits the Earth."
    s2 = "Earth's natural satellite is the Moon."
    s3 = "I enjoy eating pasta for dinner."

    _, vecs = embed_sentences([s1, s2, s3])
    v1, v2, v3 = vecs

    pairs = [
        ("s1 vs s2", v1, v2, s1, s2),
        ("s1 vs s3", v1, v3, s1, s3),
        ("s2 vs s3", v2, v3, s2, s3),
    ]

    print("\n--- Cosine similarity between sentence pairs ---")
    scores: list[tuple[str, float]] = []
    for label, a, b, ta, tb in pairs:
        score = cosine_similarity(a, b)
        scores.append((label, score))
        print(f"{label}: {score:.4f}")
        print(f"  A: {ta}")
        print(f"  B: {tb}")

    best = max(scores, key=lambda x: x[1])
    print("\nHighest similarity:", best[0], f"({best[1]:.4f})")

    # Why these results:
    # - s1 and s2 are about the same fact (Earth–Moon) with different wording, so their
    #   vectors align most closely → highest cosine similarity.
    # - s3 is unrelated (food), so both (s1,s3) and (s2,s3) score lower.
    #
    # Why cosine similarity works here:
    # - Embeddings are high-dimensional vectors where *direction* encodes semantic
    #   "topic." Cosine similarity measures the angle between two vectors, ignoring
    #   vector length (magnitude), so it focuses on whether two texts "point the same
    #   way" in meaning-space — which is what we want for semantic comparison.
