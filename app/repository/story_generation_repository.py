import os
import json
from datetime import datetime
from app.model.story_state import StoryState

SAVE_DIR = "saves"
STORY_DIR = "story"

def ensure_dirs():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    if not os.path.exists(STORY_DIR):
        os.makedirs(STORY_DIR)

def list_story_saves():
    ensure_dirs()
    files = os.listdir(SAVE_DIR)
    saves = [f for f in files if f.startswith("story_gen_") and f.endswith(".json")]
    return saves

def list_exported_stories():
    ensure_dirs()
    files = os.listdir(STORY_DIR)
    stories = [f for f in files if f.endswith(".txt")]
    return stories

def get_exported_story(filename):
    filepath = os.path.join(STORY_DIR, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def load_story_generation(save_filename) -> StoryState:
    filepath = os.path.join(SAVE_DIR, save_filename)

    if not os.path.exists(filepath):
        print("Save não encontrado!")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        story_state = json.load(f)

    return story_state

def save_story_generation(story_state: StoryState):
    ensure_dirs()
    # we don't save with a timestamp every time to avoid flooding, or we do specific checkpoints?
    # we can use simulation_id as the unique identifier
    simulation_id = story_state.get("simulation_id", "unknown")
    name = story_state.get("name", "world")
    
    filename = f"story_gen_{name}_{simulation_id}.json"
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(story_state, f, indent=4)

    return filepath

def export_final_story(story_state: StoryState):
    ensure_dirs()
    simulation_id = story_state.get("simulation_id", "unknown")
    name = story_state.get("name", "world")
    title = story_state.get("story_title", f"História de {name}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"story_{name}_{timestamp}.txt"
    filepath = os.path.join(STORY_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{title}\n")
        f.write("=" * len(title) + "\n\n")
        
        written_chapters = story_state.get("written_chapters", [])
        for i, chapter_text in enumerate(written_chapters):
            f.write(f"{chapter_text}\n\n")
            if i < len(written_chapters) - 1:
                f.write("---\n\n")

    print(f"História completa exportada para: {filepath}")
    return filepath
