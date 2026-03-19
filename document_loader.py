"""
Document loading helpers.
"""

from __future__ import annotations


def load_text_file(filepath: str) -> str:
    """
    Load a UTF-8 text file, print character/word counts, and return the raw text.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    char_count = len(text)
    word_count = len(text.split())

    print(f"Character count: {char_count}")
    print(f"Word count: {word_count}")
    return text


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into character-based chunks with overlap.

    Chunking by characters is simple and predictable. Overlap ensures that if an
    idea/sentence straddles the boundary between two chunks, it still appears in
    both chunks (so downstream retrieval has more context).
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be less than chunk_size")

    step = chunk_size - overlap
    chunks: list[str] = []

    i = 0
    n = len(text)
    while i < n:
        end = min(i + chunk_size, n)
        chunks.append(text[i:end])
        if end == n:
            break
        i += step

    return chunks


if __name__ == "__main__":
    # Basic self-test: load sample.txt, chunk it, then print chunk stats.
    text = load_text_file("sample.txt")
    chunks = chunk_text(text)

    print(f"How many chunks were created: {len(chunks)}")

    if chunks:
        print("\n--- First chunk ---")
        print(chunks[0])

        print("\n--- Last chunk ---")
        print(chunks[-1])

