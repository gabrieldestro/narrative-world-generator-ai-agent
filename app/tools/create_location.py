from app.logging.state_logger import log
from app.model.game_state import GameState


def create_location(state: GameState, name: str, description: str, connected_to: list[str]):
    log("tools", f"calling create_location tool: {name} {connected_to}")

    if name in state["world"]["locations"]:
        return state

    state["world"]["locations"][name] = {
        "name": name,
        "description": description,
        "connected_to": connected_to
    }

    log("tools", "Location criada!")
    return state