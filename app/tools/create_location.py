from app.logging.state_logger import log
from app.model.game_state import GameState
import traceback


def create_location(state: GameState, id: str, name: str, description: str, connected_to: list[str]):
    try:
        log("tools", f"calling create_location tool: {id} {name} {connected_to}")

        if name in state["world"]["locations"]:
            return state

        state["world"]["locations"][id] = {
            "id": id,
            "name": name,
            "description": description,
            "connected_to": connected_to
        }

        log("tools", "Location criada!")
        print(f"Localização criada: {id} {name} {connected_to}")
    except:
        traceback.print_exc()

    return state
