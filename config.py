import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={"api_version": "v1beta"},
)

MODELS = ["gemini-4-hydrogen", "gemini-2.5-flash"]

PERSONAS = {
    "Concise Assistant": "You are a helpful, concise personal AI agent. Use your tools whenever you need real-time facts or exact calculations.",
    "Detailed Analyst": "You are a thorough analytical AI assistant. Use your tools for live facts and explain your reasoning clearly with structured bullet points.",
    "Friendly Tutor": "You are a warm, encouraging AI tutor. Use your tools for real-time facts and explain concepts in simple, everyday language.",
}
