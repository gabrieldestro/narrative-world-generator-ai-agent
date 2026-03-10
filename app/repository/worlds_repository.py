import os
import json
import uuid

WORLDS_DIR = "worlds"

def ensure_worlds_dir():
    if not os.path.exists(WORLDS_DIR):
        os.makedirs(WORLDS_DIR)

def list_worlds():
    ensure_worlds_dir()
    files = os.listdir(WORLDS_DIR)
    saves = [f for f in files if f.endswith(".json")]
    return saves

def load_world(filename):
    filepath = os.path.join(WORLDS_DIR, filename)

    if not os.path.exists(filepath):
        print("Template não encontrado!")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        game_state = json.load(f)

    # set an id for this simulation
    game_state["simulation_id"] = uuid.uuid4()

    return game_state