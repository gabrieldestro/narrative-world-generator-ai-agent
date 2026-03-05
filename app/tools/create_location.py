from app.model.game_state import GameState


def create_location(state: GameState, name: str, description: str, connected_to: list[str]):
    print(f"calling create_location tool: {name} {connected_to}")

    if name in state["world"]["locations"]:
        return state

    state["world"]["locations"][name] = {
        "name": name,
        "description": description,
        "connected_to": connected_to
    }

    print("Location criada!")
    return state