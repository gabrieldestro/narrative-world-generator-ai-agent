from app.logging.state_logger import log
from app.model.game_state import GameState


def move_npc(state: GameState, npc_id: str, to_location: str):
    log("tools", f"calling move_npc {npc_id} {to_location}")

    destination = to_location

    npc = state["npcs"].get(npc_id)

    if not npc:
        log("tools", f"NPC {npc_id} não existe")
        return f"NPC {npc_id} não existe"

    current = npc["current_location"]

    location = state["world"]["locations"][current]

    if destination not in location["connected_to"]:
        log("tools", f"{npc['name']} não pode ir para {destination}")
        return f"{npc['name']} não pode ir para {destination}"

    npc["current_location"] = destination

    log("tools", f"{npc['name']} moveu-se para {destination}")
    return f"{npc['name']} moveu-se para {destination}"