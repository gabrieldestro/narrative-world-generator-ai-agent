from app.logging.state_logger import log
from app.model.game_state import GameState
import traceback


def create_npc(
    state: GameState,
    id: str,
    name: str,
    description: str,
    goals: list[str],
    current_location: str,
    status: str
):
    try:
        log("tools", f"calling create_npc tool: {id} {name} {description} {goals} {current_location} {status}")

        if id in state["npcs"]:
            return state

        if current_location not in state["world"]["locations"]:
            return state

        state["npcs"][id] = {
            "id": id,
            "name": name,
            "description": description,
            "goals": goals,
            "current_location": current_location,
            "status": status
        }

        log("tools", f"NPC criado!")
        print(f"NPC criado: {id} {name} {description} {goals} {current_location} {status}")
    except:
        traceback.print_exc()
    
    return state