import os
import json
from datetime import datetime

SAVE_DIR = "saves"

def ensure_save_dir():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

def list_saves():
    ensure_save_dir()
    files = os.listdir(SAVE_DIR)
    saves = [f for f in files if f.endswith(".json")]
    return saves

def load_game(save_filename):
    filepath = os.path.join(SAVE_DIR, save_filename)

    if not os.path.exists(filepath):
        print("Save não encontrado!")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        game_state = json.load(f)

    return game_state

def save_game(game_state):
    ensure_save_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filepath = os.path.join(SAVE_DIR, f"{game_state["name"]}_{timestamp}.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(game_state, f, indent=4)

    print(f"Jogo salvo em: {filepath}")