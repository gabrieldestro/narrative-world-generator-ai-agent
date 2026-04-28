import os
import json
from dotenv import load_dotenv, set_key

ENV_PATH = ".env"
WORLDS_DIR = "worlds"

def load_environment_variables() -> dict:
    if os.path.exists(ENV_PATH):
        load_dotenv(ENV_PATH)
    
    # Lista de chaves importantes para o app
    keys = [
        "LLM_MODEL", "PROVIDER_NAME", "BASE_URL", "TOKEN", 
        "SIMULATION_TYPE", "DEBUG", "AUTO_PLAY", 
        "STORY_CHAPTER_PARTS", "TEMPERATURE"
    ]
    return {k: os.environ.get(k, "") for k in keys}

def update_environment_variable(key: str, value: str):
    if not os.path.exists(ENV_PATH):
        open(ENV_PATH, 'a').close()
    
    set_key(ENV_PATH, key, value)
    os.environ[key] = value

def list_world_templates() -> list:
    if not os.path.exists(WORLDS_DIR):
        os.makedirs(WORLDS_DIR)
    
    return [f for f in os.listdir(WORLDS_DIR) if f.endswith(".json")]

def get_world_template(filename: str) -> dict:
    filepath = os.path.join(WORLDS_DIR, filename)
    if not os.path.exists(filepath):
        return {}
        
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_world_template(filename: str, data: dict):
    if not os.path.exists(WORLDS_DIR):
        os.makedirs(WORLDS_DIR)
        
    filepath = os.path.join(WORLDS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
