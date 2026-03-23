"""
Embedding demo: get a vector for a sentence using the Gemini embedding API.

We use the supported `google-genai` package (import: `from google import genai`).
The older `google-generativeai` package is deprecated; embedding calls map to the
same model names and behave the same for this script.
"""

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

try:
    response = client.models.embed_content(
        model=PRIMARY_EMBEDDING_MODEL,
        contents=["The moon orbits the Earth."],
    )
except genai_errors.ClientError as exc:
    if exc.code == 404:
        print(
            f"Note: {PRIMARY_EMBEDDING_MODEL} was not available on this API. "
            f"Using {FALLBACK_EMBEDDING_MODEL} instead."
        )
        response = client.models.embed_content(
            model=FALLBACK_EMBEDDING_MODEL,
            contents=["The moon orbits the Earth."],
        )
    else:
        raise

vector = response.embeddings[0].values

# Print the first 5 components and the full dimensionality
print("First 5 numbers of the embedding vector:", vector[:5])
print("Total length (dimensions) of the vector:", len(vector))

# Conceptually, each number is one coordinate of a high-dimensional vector that
# represents the *meaning* of the text in embedding space. Similar sentences end
# up with vectors that point in similar directions (high cosine similarity).
# The model learned these coordinates from training so that semantic similarity
# in language corresponds to geometric closeness in this space.
