import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PROVIDER_NAME = os.getenv("PROVIDER_NAME")
DEBUG = os.getenv("DEBUG")

if not PROVIDER_NAME:
    raise ValueError("PROVIDER_NAME not defined in environment.")

MODEL_NAME = os.getenv("LLM_MODEL", "gpt-4o-mini")
BASE_URL = "https://models.inference.ai.azure.com"