# Building a Personal Knowledge Base Assistant
### A guided journey from zero to a working AI-powered app

---

> **How to use this guide**
>
> Each section below is a self-contained chapter. You will read a short explanation of *what is happening and why*, then find a list of prompts you can paste directly into an AI assistant (Claude, ChatGPT, Cursor, etc.) to build that part of the project. Every prompt includes a note on what to expect and how to verify it worked.
>
> You do not need to memorize anything. The goal is that you *understand* what is being built at each step, even if the AI is writing most of the code.

---

## Prerequisites

Before you start, make sure you have:

- Python 3.10+ installed (`python --version` in your terminal)
- A code editor (VS Code is recommended)
- A Google Gemini API key — get one for free at [Google AI Studio](https://aistudio.google.com/app/apikey)
- Basic comfort with a terminal (running commands, navigating folders)

You do **not** need to know LangChain, embeddings, or vector databases yet. That is what this guide is for.

---

## Part 1 — Project Setup and First API Call

### What is happening here?

Before writing any "AI code", you need a clean workspace. In Python this means a **virtual environment** — a private box where you install only the packages your project needs, isolated from everything else on your system.

After setting that up, you will make your first call to a language model. No frameworks, no libraries except the official SDK. Just you, a Python script, and the model. This is important: seeing the raw API response before adding abstractions helps you understand what every framework is actually doing under the hood.

At the end of this part, you will have a working script that sends a question to a real LLM and prints the answer.

---

### Prompts

---

**Prompt 1.1 — Project scaffold**

```
I am starting a Python project called "personal-kb". Please:
1. Give me the terminal commands to create a project folder, set up a Python virtual environment, and activate it.
2. Create a requirements.txt with these packages: google-generativeai, python-dotenv
3. Create a .env file template with a placeholder GOOGLE_API_KEY variable
4. Create a .gitignore that excludes .env, __pycache__, and the venv folder

Explain what each step does in plain language.
```

> **What to expect:** A set of shell commands and three files. After running them, your folder should look like: `personal-kb/ ├── .env ├── .gitignore ├── requirements.txt └── venv/`
>
> **How to test:** Run `pip list` inside the activated venv. You should see `google-generativeai` and `python-dotenv` listed.

---

**Prompt 1.2 — First LLM call**

```
Inside my "personal-kb" project, create a file called hello_llm.py.
It should:
1. Load the GOOGLE_API_KEY from the .env file using python-dotenv
2. Create a Google Generative AI client using the google-generativeai library
3. Send the message "What is a knowledge base?" to the gemini-1.5-flash model
4. Print the response text to the terminal

Add a comment above each block of code explaining what it does.
```

> **What to expect:** A ~20-line script. Run it with `python hello_llm.py`. You should see the model's answer printed in your terminal within a few seconds.
>
> **How to test:** Change the question in the script to something else and run it again. If it answers, the API connection is working perfectly.
>
> **Note on the free tier:** `gemini-1.5-flash` is free with a limit of 15 requests per minute and 1,500 requests per day — more than enough for this entire project.

---

**Prompt 1.3 — Understanding the response object**

```
I ran my hello_llm.py and got a response. Now I want to understand what the full response object looks like.
Modify hello_llm.py to also print:
- The model that was used
- The number of prompt tokens consumed
- The number of response tokens consumed
- The finish reason

Use the google-generativeai SDK. Then explain what "tokens" are and why they matter for costs.
```

> **What to expect:** The same script, now printing extra metadata after the answer. This is not strictly necessary for the project, but it teaches you how the API response is structured — knowledge you will use constantly.

---

## Part 2 — Documents, Text, and Chunking

### What is happening here?

Language models have a **context window** — a maximum amount of text they can read at once. A large PDF might be 50,000 words. You cannot feed the entire thing to the model with every question. Even if you could, it would be expensive and slow.

The solution is **chunking**: splitting your documents into small, overlapping pieces. Later (in Part 3), you will store these chunks in a way that lets you find only the relevant ones before asking a question.

This part also covers loading different file types: plain text, PDFs, and CSV files. Each format requires a different approach.

---

### Prompts

---

**Prompt 2.1 — Loading and reading a text file**

```
Create a file called document_loader.py in my personal-kb project.
Write a function called load_text_file(filepath) that:
1. Reads a .txt file
2. Prints the total character count and word count
3. Returns the raw text as a string

Also create a small sample file called sample.txt with 3 paragraphs of any text about space exploration (make it up).
Then call load_text_file on sample.txt at the bottom of the script to show it works.
```

> **What to expect:** A function and a test run. You should see character/word counts printed when you run the script.

---

**Prompt 2.2 — Chunking text**

```
In document_loader.py, add a function called chunk_text(text, chunk_size=500, overlap=50) that:
1. Splits the text into chunks of approximately chunk_size characters
2. Each chunk overlaps with the previous one by overlap characters (so context is not lost at boundaries)
3. Returns a list of strings

After defining the function, load sample.txt, chunk it, and print:
- How many chunks were created
- The first chunk
- The last chunk

Add a comment explaining WHY overlap is important.
```

> **What to expect:** The sample text split into several overlapping pieces. You should see that the end of chunk 1 and the start of chunk 2 share some words — that is the overlap working.
>
> **How to test:** Try changing chunk_size to 100 and notice you get more, smaller chunks.

---

**Prompt 2.3 — Loading a PDF**

```
I want to add PDF support to document_loader.py.
1. Add pypdf to my requirements.txt and show me the install command
2. Write a function called load_pdf(filepath) that extracts all text from a PDF and returns it as a single string
3. Handle the case where a page has no extractable text (scanned image pages) gracefully — print a warning but continue
4. Test it by creating a dummy function that generates a simple PDF using the fpdf2 library, saves it, then loads it back

Explain what "extractable text" means and when PDFs don't have it.
```

> **What to expect:** Two new functions and a small test. The key concept here is understanding that not all PDFs contain actual text — scanned documents are just images.

---

**Prompt 2.4 — Loading a CSV**

```
Add a function called load_csv(filepath) to document_loader.py that:
1. Reads a CSV file using Python's built-in csv module (no pandas needed yet)
2. Converts each row into a human-readable sentence like: "Row 5: name=Alice, age=30, city=London"
3. Returns all rows as a list of strings, where each string is one row-sentence

Create a sample employees.csv with 5 fictional rows (name, department, salary) and test the function on it.

Explain why we convert rows to sentences instead of keeping them as dictionaries.
```

> **What to expect:** A CSV reader and a list of sentence-strings. The reason for the conversion will become clear in Part 3: embeddings work on natural language text, not structured data.

---

## Part 3 — Embeddings and Vector Search

### What is happening here?

This is the conceptual heart of the project. An **embedding** is a way of turning a piece of text into a list of numbers (a vector) that captures its *meaning*. Two pieces of text about similar topics will have similar vectors, even if they use different words.

A **vector database** stores these vectors and can instantly find the ones most similar to a given query vector. This is how the assistant will work: when you ask a question, your question is converted to a vector, and the database finds the document chunks whose vectors are closest to it. Only those chunks are sent to the LLM.

This approach is called **RAG — Retrieval-Augmented Generation**. The model's answer is *augmented* by retrieved documents.

---

### Prompts

---

**Prompt 3.1 — Your first embedding**

```
Create a new file called embeddings_demo.py.
Using the google-generativeai library, call the embedding API with the model "models/text-embedding-004"
to get the embedding vector for the sentence "The moon orbits the Earth."
Print:
- The first 5 numbers of the vector
- The total length (dimensions) of the vector

Then explain in a comment what these numbers represent conceptually.
```

> **What to expect:** A list of 768 floats. The numbers themselves look meaningless — that is normal. What matters is that similar sentences produce similar lists.
>
> **Note:** Google's `text-embedding-004` model produces 768-dimensional vectors and is included in the free tier.

---

**Prompt 3.2 — Measuring similarity**

```
In embeddings_demo.py, add a function called cosine_similarity(vec_a, vec_b) that computes the cosine similarity between two vectors.
Then create embeddings for these three sentences:
- "The moon orbits the Earth."
- "Earth's natural satellite is the Moon."
- "I enjoy eating pasta for dinner."

Compare all three pairs and print their similarity scores.
Explain the results: which pair is most similar and why does cosine similarity work for this?
```

> **What to expect:** Three similarity scores. The first two sentences (same topic, different words) should score very high (~0.95+). The third should be much lower for both. This is the core intuition behind semantic search.

---

**Prompt 3.3 — Setting up ChromaDB**

```
I want to use ChromaDB as my local vector database, with Google's embedding model.
1. Add chromadb to requirements.txt and show the install command
2. Create a file called vector_store.py
3. In it, write a function called create_collection(name) that creates a persistent ChromaDB collection stored in a local folder called "chroma_db"
4. Write a function called add_chunks(collection, chunks, source_name) that:
   - Takes a list of text strings
   - Generates embeddings for each chunk using Google's "models/text-embedding-004" model via google-generativeai
   - Adds them to the collection with those embeddings
   - Tags each chunk with the source_name as metadata
5. Write a simple test that creates a collection called "test", adds 3 sentences, and prints the count of stored items.

Explain what "persistent" means here and why it matters.
```

> **What to expect:** A `chroma_db/` folder will appear after running the script. This is your database saved to disk — it survives between runs.

---

**Prompt 3.4 — Querying the vector store**

```
In vector_store.py, add a function called search(collection, query, n_results=3) that:
1. Takes a natural language query string
2. Returns the top n_results most semantically similar chunks from the collection
3. Also returns the metadata (source name) for each result

Test it by:
1. Adding 10 sentences about different topics to the collection (space, cooking, sports, history — mix them up)
2. Querying with "Who won the championship?" and printing the results
3. Querying with "How do rockets work?" and printing the results

Show that the results match the topic even when the query words don't exactly match any stored sentence.
```

> **What to expect:** Relevant results returned even without keyword matching. This is the "magic" moment — the system understanding meaning, not just pattern-matching words.

---

## Part 4 — The RAG Pipeline with LangChain

### What is happening here?

In the previous parts you built each piece manually: load documents, chunk them, embed them, search them. Now you will assemble these into a **pipeline** using LangChain.

LangChain is a framework that connects these pieces together with standardized interfaces. A `DocumentLoader` loads files. A `TextSplitter` chunks them. A `VectorStore` handles embeddings and retrieval. A `Chain` wires the retrieved context to the LLM and formats the final answer.

Think of it like plumbing: the same water flows through pipes of different shapes. LangChain provides the pipes.

---

### Prompts

---

**Prompt 4.1 — Install and explore LangChain**

```
I want to add LangChain to my project. I am using the Google Gemini API.
1. Show me which packages to add to requirements.txt for: langchain, langchain-google-genai, langchain-chroma, and langchain-community
2. Create a file called rag_pipeline.py with just the imports at the top and a comment explaining what each import is for
3. Briefly explain the difference between langchain, langchain-core, and langchain-community — why are they split into separate packages?
```

> **What to expect:** An updated requirements.txt and a skeleton file. Understanding the package split helps you read LangChain documentation without getting confused.

---

**Prompt 4.2 — Loading documents with LangChain**

```
In rag_pipeline.py, write a function called load_documents(folder_path) that:
1. Scans a folder for .txt and .pdf files
2. Uses LangChain's TextLoader for .txt files and PyPDFLoader for .pdf files
3. Returns a list of LangChain Document objects
4. Prints how many documents were loaded and their file names

Create a folder called "documents/" and put 2 .txt files in it (you can generate sample content about any two topics).
Then test load_documents("documents/").

Explain what a LangChain Document object contains (page_content and metadata).
```

> **What to expect:** A list of Document objects printed to the terminal. The key insight is that LangChain wraps your raw text in objects that carry metadata (filename, page number, etc.) alongside the content.

---

**Prompt 4.3 — Splitting and indexing with LangChain**

```
In rag_pipeline.py, add a function called build_index(documents, persist_dir="chroma_db") that:
1. Uses RecursiveCharacterTextSplitter with chunk_size=500 and chunk_overlap=50
2. Splits all the loaded documents into chunks
3. Creates a Chroma vector store using GoogleGenerativeAIEmbeddings with model "models/text-embedding-004"
4. Persists the vector store to persist_dir
5. Returns the vector store object

Also add a function called load_index(persist_dir="chroma_db") that loads an existing index from disk without re-embedding.

Explain why we separate build_index and load_index — what is the practical benefit?
```

> **What to expect:** After running build_index, a `chroma_db/` folder appears with database files inside. load_index should load instantly compared to build_index which calls the embeddings API.

---

**Prompt 4.4 — The retrieval chain**

```
In rag_pipeline.py, write a function called create_qa_chain(vector_store) that:
1. Creates a retriever from the vector store that returns the top 4 most relevant chunks
2. Builds a RetrievalQA chain using ChatGoogleGenerativeAI with model "gemini-1.5-flash"
3. Uses this prompt template:
   "Use the following context to answer the question. If the answer is not in the context, say 'I don't know based on the provided documents.'
   Context: {context}
   Question: {question}"
4. Returns the chain

Then write a main() function that:
1. Loads documents from "documents/"
2. Builds or loads the index
3. Creates the QA chain
4. Asks two test questions and prints the answers

Explain what "retriever" means in this context and how it differs from a direct vector search.
```

> **What to expect:** A working end-to-end Q&A system. Ask questions about the content in your documents folder — the system should answer based on what's in the files, not general knowledge.
>
> **How to test:** Ask a question whose answer is clearly in one of your documents. Then ask something completely unrelated — the system should say it doesn't know.

---

## Part 5 — Web Scraping as a Document Source

### What is happening here?

Your knowledge base does not have to be limited to files on your computer. Web pages are also valid sources. You will add the ability to scrape a URL, extract the meaningful text (ignoring menus, ads, footers), and add it to your index.

This is where **BeautifulSoup** comes in — a library for parsing HTML and extracting text. The scraped content goes through the same pipeline: chunk → embed → store → retrieve.

---

### Prompts

---

**Prompt 5.1 — Basic web scraping**

```
Add beautifulsoup4 and requests to requirements.txt.
Create a file called web_scraper.py with a function called scrape_url(url) that:
1. Fetches the HTML of a URL using requests
2. Parses it with BeautifulSoup
3. Removes script tags, style tags, and navigation elements
4. Extracts only the main body text
5. Returns the cleaned text as a string

Also add a User-Agent header to avoid being blocked by basic bot detection.
Test it on https://en.wikipedia.org/wiki/Retrieval-augmented_generation and print the first 500 characters.

Explain what BeautifulSoup does and why we need to remove script/style tags.
```

> **What to expect:** Clean readable text from the Wikipedia article, without HTML tags. The first 500 characters should look like the article's introduction.

---

**Prompt 5.2 — Integrating web content into the pipeline**

```
Modify rag_pipeline.py to add a function called add_url_to_index(url, vector_store) that:
1. Calls scrape_url(url) from web_scraper.py
2. Creates a LangChain Document from the scraped text with the URL as metadata
3. Splits it using the same text splitter as before
4. Adds the new chunks to the existing vector store

Update main() to:
1. Load from the documents folder as before
2. Also scrape one Wikipedia article of your choice
3. Ask a question that can only be answered by the scraped content

Show me how to verify that the answer came from the web source (hint: inspect the source metadata in the result).
```

> **What to expect:** The system now answers questions about web content it scraped. You can verify the source by printing the `source` metadata from the retrieved chunks.

---

## Part 6 — CLI Interface

### What is happening here?

Right now, your script runs questions hardcoded in `main()`. To make this actually useful, you need an interface where you can type questions freely.

You will build a **command-line interface (CLI)** — a simple loop that accepts your input, queries the system, and prints the answer. This is the fastest path to having something you can actually use day-to-day before adding a visual interface.

---

### Prompts

---

**Prompt 6.1 — Interactive question loop**

```
Create a file called cli.py that:
1. On startup, loads the existing index from chroma_db (do NOT rebuild — load the existing one)
2. Creates the QA chain
3. Enters a loop that:
   - Prints "Ask a question (or 'quit' to exit): "
   - Reads input from the user
   - Runs the question through the chain
   - Prints the answer
   - Also prints which source documents were used to generate the answer
4. Exits cleanly when the user types "quit"

Add a startup message that says how many documents are in the index.
```

> **What to expect:** A simple interactive session in your terminal. You type a question, press Enter, read the answer. This is your knowledge base assistant in its first usable form.

---

**Prompt 6.2 — Ingestion command**

```
Add a second mode to cli.py using argparse:
- python cli.py ask → starts the interactive question loop (default)
- python cli.py ingest --file path/to/file.pdf → loads one file, adds it to the index
- python cli.py ingest --url https://example.com → scrapes a URL and adds it to the index

After ingestion, print a confirmation with the number of chunks added.

Explain what argparse is and why it is better than reading sys.argv manually.
```

> **What to expect:** You can now add new documents without touching the code. Run `python cli.py ingest --file mynotes.pdf` and the document becomes queryable immediately.

---

## Part 7 — Multi-Turn Chat with Memory

### What is happening here?

The current system treats every question as independent. Ask "Who is the CEO?" then "What did she say last year?" — the second question fails because the system does not know who "she" refers to.

**Conversational memory** solves this by maintaining a history of the dialogue and passing it to the model alongside retrieved context. The model can then resolve references like "she", "that", "the previous answer" correctly.

LangChain provides `ConversationBufferMemory` for this. The full pipeline becomes: retrieve relevant chunks + attach conversation history + generate answer.

---

### Prompts

---

**Prompt 7.1 — Adding memory to the chain**

```
In rag_pipeline.py, create a new function called create_conversational_chain(vector_store) that:
1. Uses ConversationalRetrievalChain instead of RetrievalQA
2. Attaches a ConversationBufferMemory that stores both questions and answers
3. Uses the same ChatGoogleGenerativeAI model and prompt as before

Explain the difference between RetrievalQA and ConversationalRetrievalChain — why do we need a different chain type?
```

> **What to expect:** A chain that keeps context between questions. The change in code is small, but the behavior difference is significant.

---

**Prompt 7.2 — Update the CLI for multi-turn conversation**

```
Update cli.py to use create_conversational_chain instead of create_qa_chain.
Test it with a multi-turn conversation like:
1. "What topics are covered in my documents?"
2. "Tell me more about the first one."
3. "Can you summarize that in one sentence?"

Show that question 2 correctly refers back to question 1 without the user repeating themselves.

Also add a "clear" command that resets the conversation history without exiting.
```

> **What to expect:** A conversation that flows naturally. The "clear" command lets you start a fresh session when switching topics.

---

## Part 8 — Streamlit Web Interface (Optional)

### What is happening here?

The CLI is functional, but a web interface is more comfortable for daily use and easier to share with others. **Streamlit** lets you build a clean web app in Python with almost no HTML or CSS knowledge.

In about 50 lines of code, you will have a browser-based chat interface backed by your entire knowledge base.

---

### Prompts

---

**Prompt 8.1 — Basic Streamlit app**

```
Add streamlit to requirements.txt.
Create a file called app.py that:
1. Shows a title "Personal Knowledge Base"
2. Has a text input field for questions
3. When a question is submitted, calls the QA chain and displays the answer
4. Shows a sidebar with the list of source documents used

Use st.session_state to keep the chain and vector store loaded between interactions (so it doesn't reload on every question).

Give me the command to run the app.
```

> **What to expect:** Running `streamlit run app.py` opens a browser tab with a simple chat interface. No HTML needed.

---

**Prompt 8.2 — Chat history and file upload**

```
Upgrade app.py to:
1. Display a full chat history (previous questions and answers in the session)
2. Add a file uploader in the sidebar that accepts .txt and .pdf files
3. When a file is uploaded, ingest it into the index and show a success message
4. Use the ConversationalRetrievalChain so the chat has memory

Style the chat so user messages appear on the right and assistant messages on the left.
```

> **What to expect:** A polished chat UI in your browser. You can drag and drop a PDF into the sidebar and immediately ask questions about it.

---

## Part 9 — Review and What to Build Next

### What you have built

By completing this guide, your project contains:

- **Document ingestion** for `.txt`, `.pdf`, `.csv`, and live web URLs
- **Semantic search** using embeddings and ChromaDB
- **A RAG pipeline** that grounds LLM answers in your documents
- **Multi-turn memory** for natural conversations
- **A CLI** for daily use
- **A Streamlit web app** for a polished experience

This is not a tutorial project — it is a fully functional tool you can use. Load your own notes, research papers, meeting transcripts, or any text you want to query.

---

### Where to go from here

---

**Prompt 9.1 — Improving retrieval quality**

```
My RAG pipeline sometimes retrieves irrelevant chunks. What are 3 techniques to improve retrieval quality?
For each technique, show me how to implement it in my existing rag_pipeline.py.
Focus on: re-ranking results, using a larger chunk overlap, and adding a metadata filter.
```

---

**Prompt 9.2 — Switching to a local model**

```
I want to run this entire pipeline locally without sending data to any external API.
Show me how to replace the Google Gemini API with a local Ollama model.
What changes in rag_pipeline.py? What are the trade-offs in quality and speed compared to Gemini?
```

---

**Prompt 9.3 — Adding a REST API**

```
I want to expose my knowledge base as a REST API so other apps can query it.
Using FastAPI, create an api.py file with two endpoints:
- POST /ingest — accepts a file upload or URL and adds it to the index
- POST /ask — accepts a question and returns the answer with source citations

Show me how to run it and test it with curl.
```

---

**Prompt 9.4 — Evaluating your system**

```
How do I know if my RAG pipeline is giving good answers?
Create a simple evaluation script that:
1. Takes a list of question + expected_answer pairs
2. Runs each question through the pipeline
3. Uses an LLM to score whether the generated answer matches the expected answer (1-5 scale)
4. Prints an average score

Create 5 test cases based on content in my documents folder.
```

---

*End of guide. Good luck, and remember: the goal is not to memorize the code — it is to understand what each piece does so you can modify, extend, and debug it yourself.*
