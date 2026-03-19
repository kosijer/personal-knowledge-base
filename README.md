# Personal Knowledge Base Assistant

Ever had a folder full of notes, PDFs, and saved articles that you never actually go back to because finding anything is a pain? That's what this project is trying to fix.

This is a local AI assistant that you feed your own documents — research notes, meeting transcripts, saved web pages, CSV exports, whatever — and then you just ask it questions in plain English. It finds the relevant parts and gives you an actual answer, with sources.

Built this as a learning project to get hands-on with LLMs, embeddings, and RAG pipelines. It grew into something I actually use.

## How it works

The core idea is called **RAG (Retrieval-Augmented Generation)**. Instead of asking an AI to answer from memory (which can hallucinate or go off-topic), you first retrieve the relevant pieces from *your own documents*, then hand those to the model as context. The model answers based on what you gave it — nothing more.

In practice it goes like this:

1. You add a document. It gets split into small chunks and each chunk is converted into a vector (a list of numbers representing its meaning) using Google's embedding model.
2. Those vectors are stored locally in ChromaDB.
3. When you ask a question, the question is also converted to a vector and the database finds the chunks whose meaning is closest to your question.
4. Those chunks are sent to Gemini along with your question, and you get a grounded answer with the source cited.

No cloud storage. Everything lives on your machine.

## What it does

- Ingest documents (`.txt`, `.pdf`, `.csv`) and web URLs into a local vector database
- Ask questions in natural language and get answers grounded in your documents
- Multi-turn conversation with memory — follow-up questions just work
- CLI for daily use, Streamlit web interface for a more comfortable experience

## Stack

- **LLM & Embeddings** — Google Gemini (`gemini-1.5-flash` + `text-embedding-004`)
- **Vector store** — ChromaDB (local, persistent)
- **Pipeline** — LangChain
- **Interface** — CLI + Streamlit

## Setup

```bash
git clone <repo-url>
cd personal-kb
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Gemini API key:

```
GOOGLE_API_KEY=your_key_here
```

Get a free key at [aistudio.google.com](https://aistudio.google.com/app/apikey).

## Usage

```bash
# Ask questions
python cli.py ask

# Add a file
python cli.py ingest --file notes.pdf

# Add a web page
python cli.py ingest --url https://example.com

# Launch web interface
streamlit run app.py
```

## Project structure

```
personal-kb/
├── documents/          # Drop your files here
├── chroma_db/          # Vector database (auto-created)
├── document_loader.py  # File parsers (txt, pdf, csv)
├── web_scraper.py      # URL scraping
├── vector_store.py     # ChromaDB helpers
├── rag_pipeline.py     # LangChain RAG chain
├── cli.py              # Command-line interface
└── app.py              # Streamlit web app
```

## Roadmap

Things I want to add when I get around to it:

- [ ] Re-ranking retrieved chunks for better answer quality
- [ ] Support for `.docx` and Notion exports
- [ ] REST API so other tools can query the knowledge base
- [ ] Metadata filters — query only a specific document or date range
- [ ] Switch to a fully local model via Ollama (no API key needed at all)
- [ ] Simple evaluation script to score answer quality
