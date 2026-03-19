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


def load_pdf(filepath: str) -> str:
    """
    Extract text from a PDF and return it as a single string.

    If a page has no extractable text (common for scanned image PDFs), this
    prints a warning and continues.
    """
    # Import inside the function so the module can be imported even if pypdf
    # isn't installed for some reason.
    from pypdf import PdfReader

    with open(filepath, "rb") as f:
        reader = PdfReader(f)

        all_pages_text: list[str] = []
        for page_index, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if not page_text or not page_text.strip():
                print(
                    f"Warning: Page {page_index + 1} in '{filepath}' has no extractable text. "
                    "This often means the page is a scanned image."
                )
                continue

            all_pages_text.append(page_text)

    return "\n".join(all_pages_text)


def dummy_pdf_roundtrip_demo() -> None:
    """
    Create a small dummy PDF using fpdf2, then load it back with load_pdf().
    Includes a blank page to demonstrate the "no extractable text" warning.
    """
    import tempfile

    # fpdf2 provides the FPDF class (import path is `fpdf`)
    from fpdf import FPDF

    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = f"{tmpdir}/dummy.pdf"

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Page 1: contains text
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 8, "This is a dummy PDF for testing text extraction.")

        # Page 2: intentionally blank (no extractable text expected)
        pdf.add_page()

        pdf.output(pdf_path)

        extracted_text = load_pdf(pdf_path)
        print(f"\nPDF load demo: extracted {len(extracted_text)} characters of text.")
        if extracted_text.strip():
            print("First 200 characters:\n", extracted_text[:200])


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

    # PDF self-test: create a dummy PDF and load it back.
    dummy_pdf_roundtrip_demo()

