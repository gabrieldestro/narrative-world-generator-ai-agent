from app.model.game_state import GameState
from app.logging.state_logger import log

def update_world_fact(state: GameState, index: int, fact: str):
    log("tools", f"calling update_world_fact {index}")

    facts = state["world"]["world_prompt"]

    if index < 0 or index >= len(facts):
        log("tools", "Índice inválido")
        return "Índice inválido"

    old = facts[index]
    facts[index] = fact

    log("tools", f"Fato atualizado: '{old}' -> '{fact}'")
    return f"Fato atualizado: '{old}' -> '{fact}'"