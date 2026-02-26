import json
from app.logging_config import game_logger


def log_game_state(state):
    try:
        serialized = json.dumps(state, ensure_ascii=False)
    except TypeError:
        serialized = str(state)

    game_logger.info(serialized)