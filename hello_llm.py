"""
Hello LLM: Load API key, call Gemini, and print the response.
Uses the supported google-genai package (not the deprecated google-generativeai).
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
