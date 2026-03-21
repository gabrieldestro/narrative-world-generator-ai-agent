from app.logging.state_logger import log
from app.model.game_state import GameState


def add_world_fact(state: GameState, fact: str):
    log("tools", "calling add_world_fact")

    state["world"]["world_prompt"].append(fact)

    log("tools", f"Novo fato adicionado ao mundo: {fact}")
    return f"Novo fato adicionado ao mundo: {fact}"