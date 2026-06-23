import os
from dotenv import load_dotenv

load_dotenv("app/.env")

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)