import os
import json
from datetime import datetime

STORY_DIR = "story"

def ensure_story_dir():
    if not os.path.exists(STORY_DIR):
        os.makedirs(STORY_DIR)

def append_story(game_state, text):
    ensure_story_dir()

    filename = f"{game_state['name']}_{game_state['simulation_id']}.txt"
    filepath = os.path.join(STORY_DIR, filename)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(text.strip())
        f.write("\n\n") 