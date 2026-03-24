"""
ChromaDB vector store helpers with Google (Gemini) embeddings.

Embeddings are produced with the supported `google-genai` SDK (same as
`embeddings_demo.py`). The learning guide names `google-generativeai` and
`models/text-embedding-004`; we call that model first and fall back to
`models/gemini-embedding-001` when the API returns 404.

Persistent storage:
  Chroma writes its database under ./chroma_db (next to this file). That means
  vectors and metadata survive after your Python process exits. Without
  persistence, everything would live in memory only and disappear on restart—bad
  for a real knowledge base you query across sessions.
"""

from __future__ import annotations

import os
import uuid

import chromadb

# Reuse embedding batching + model fallback from embeddings_demo
from embeddings_demo import embed_sentences

# Folder on disk where Chroma stores SQLite + index files (created automatically).
CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

_chroma_client: chromadb.PersistentClient | None = None


def _get_chroma_client() -> chromadb.PersistentClient:
    """Single shared client so all collections use the same on-disk store."""
    global _chroma_client
    if _chroma_client is None:
        os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
        _chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    return _chroma_client


def create_collection(name: str) -> chromadb.Collection:
    """
    Create or open a Chroma collection backed by persistent storage under chroma_db/.

    Cosine space matches typical semantic search with normalized embedding geometry.
    """
    return _get_chroma_client().get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"},
    )


def add_chunks(
    collection: chromadb.Collection,
    chunks: list[str],
    source_name: str,
) -> None:
    """
    Embed each text chunk with Google's embedding API (via google-genai) and
    insert into Chroma with precomputed vectors.

    Each row is tagged with metadata source_name=<source_name> for filtering and UI.
    """
    if not chunks:
        return

    _model, embeddings = embed_sentences(chunks)

    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"source_name": source_name} for _ in chunks]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )


if __name__ == "__main__":
    # Simple test: fresh "test" collection, three sentences, print count.
    client = _get_chroma_client()
    try:
        client.delete_collection("test")
    except Exception:
        pass

    test_col = create_collection("test")
    add_chunks(
        test_col,
        [
            "The moon orbits the Earth.",
            "Mars is often called the Red Planet.",
            "Saturn is famous for its ring system.",
        ],
        source_name="demo_sentences",
    )
    print("Stored item count in collection 'test':", test_col.count())
