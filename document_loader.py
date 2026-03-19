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


if __name__ == "__main__":
    # Basic self-test requested by the prompt
    load_text_file("sample.txt")

