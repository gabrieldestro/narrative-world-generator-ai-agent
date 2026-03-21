from app.logging.state_logger import log
from app.model.game_state import GameState

def remove_world_fact(state: GameState, index: int):
    log("tools", f"calling remove_world_fact {index}")

    facts = state["world"]["world_prompt"]

    if index < 0 or index >= len(facts):
        log("tools", f"Índice inválido")
        return "Índice inválido"

    removed = facts.pop(index)

    log("tools", f"Fato removido: {removed}")
    return f"Fato removido: {removed}"