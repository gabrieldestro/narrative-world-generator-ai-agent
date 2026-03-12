from app.model.game_state import GameState


def get_world_context(state: GameState):
    world_context = ""

    for i, line in enumerate(state["world"]["world_prompt"]):
        world_context += f"{i}: {line}\n"

    return world_context