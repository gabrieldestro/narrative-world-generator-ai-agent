import logging
import json
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


class JsonFormatter(logging.Formatter):
    def format(self, record):

        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # 👇 forma segura
        extra_data = getattr(record, "extra_data", None)
        if extra_data:
            log_record.update(extra_data)

        return json.dumps(log_record, ensure_ascii=False)


def setup_logger(name: str, file_name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # ⚠️ evita duplicação de handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = RotatingFileHandler(
        LOG_DIR / file_name,
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8"
    )

    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)

    return logger


game_logger = setup_logger("game_logger", "game_state.json")
llm_logger = setup_logger("llm_logger", "llm_calls.json")
story_logger = setup_logger("story_logger", "story.log")