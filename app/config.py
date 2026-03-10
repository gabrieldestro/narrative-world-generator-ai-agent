import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG") == "1"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PROVIDER_NAME = os.getenv("PROVIDER_NAME")

'''
0 - LITE
1 - COMPLETE
'''
SIMULATION_TYPE = os.getenv("SIMULATION_TYPE")

if not PROVIDER_NAME:
    raise ValueError("PROVIDER_NAME not defined in environment.")

MODEL_NAME = os.getenv("LLM_MODEL", "gpt-4o-mini")
BASE_URL = "https://models.inference.ai.azure.com"
