import json
from app.logging_config import game_logger, story_logger
from app.config import DEBUG


def log_game_state(state):
    try:
        serialized = json.dumps(state, ensure_ascii=False)
    except TypeError:
        serialized = str(state)

    game_logger.info(serialized)

def log(type: str, text: str):
    if (DEBUG):
        print(f"{type}\n{text}\n")
    story_logger.info(f"{type}\n{text}\n\n")