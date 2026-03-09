from app.logging.state_logger import log
from app.model.game_state import GameState


def complete_quest(state: GameState, quest_id: str):
    log("tools", "complete_quest")
    
    quest = state["quests"].get(quest_id)

    if not quest:
        return f"Quest {quest_id} não existe"

    quest["status"] = "completed"

    log("tools", f"Quest {quest['name']} foi completada")
    return f"Quest {quest['name']} foi completada"