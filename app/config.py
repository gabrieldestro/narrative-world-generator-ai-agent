import os
from dotenv import load_dotenv

load_dotenv()

'''
0 - LITE
1 - COMPLETE
'''
SIMULATION_TYPE = os.getenv("SIMULATION_TYPE")
DEBUG = os.getenv("DEBUG") == "1"
TEMPERATURE = float(os.getenv("TEMPERATURE")) if os.getenv("TEMPERATURE") else 0.7

PROVIDER_NAME = os.getenv("PROVIDER_NAME")
if not PROVIDER_NAME:
    raise ValueError("PROVIDER_NAME not defined in environment.")

API_TOKEN = os.getenv("TOKEN")
MODEL_NAME = os.getenv("LLM_MODEL", "gpt-4o-mini")
BASE_URL = os.getenv("BASE_URL", "https://models.inference.ai.azure.com")
