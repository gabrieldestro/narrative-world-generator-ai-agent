from app.model.game_state import GameState


def create_location(state: GameState, name: str, description: str, connected_to: list[str]):
    print("calling create_location tool")
    
    if name in state["world"]["locations"]:
        return state

    state["world"]["locations"][name] = {
        "name": name,
        "description": description,
        "connected_to": connected_to
    }

    return state