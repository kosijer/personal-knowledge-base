"""
Hello LLM: Load API key, call Gemini, and print the response.
Uses the supported google-genai package (not the deprecated google-generativeai).
Also prints response metadata: model, token counts, and finish reason.
"""

import os

# Load environment variables from .env so GOOGLE_API_KEY is available
from dotenv import load_dotenv
load_dotenv()

from google import genai

# Create a client; it uses GOOGLE_API_KEY from the environment (set by load_dotenv)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Send the prompt to Gemini 2.5 Flash and get the response
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is a knowledge base?",
)

# Print the model's reply as plain text to the terminal
print(response.text)

# --- Response metadata (understanding the full response object) ---
usage = response.usage_metadata
prompt_tokens = getattr(usage, "prompt_token_count", None) or "N/A"
response_tokens = getattr(usage, "candidates_token_count", None) or "N/A"
finish_reason = "N/A"
if response.candidates:
    finish_reason = getattr(response.candidates[0], "finish_reason", None) or "N/A"

print("\n--- Response metadata ---")
print(f"Model used:          {getattr(response, 'model_version', None) or 'gemini-2.5-flash'}")
print(f"Prompt tokens:       {prompt_tokens}")
print(f"Response tokens:     {response_tokens}")
print(f"Finish reason:       {finish_reason}")

# --- What are tokens and why do they matter for costs? ---
# Tokens are the basic units the model reads and writes: roughly 4 characters or ~0.75 words
# in English. The API counts:
#   - Prompt tokens: everything you send (your question + any context). You pay for input.
#   - Response (candidate) tokens: everything the model generates. You pay for output.
# Pricing is usually per token (input often cheaper than output). So longer prompts and
# longer answers cost more. Tracking these numbers helps you estimate cost and stay within
# free-tier limits (e.g. requests per minute / per day).
