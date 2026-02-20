from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

# Load API key from .env file
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

# Test the connection
print("Testing Groq connection...")
response = llm.invoke("Say hello in exactly one sentence.")

print("✅ SUCCESS — Groq LLM Connected!")
print("Model response:", response.content)