from app.logging.state_logger import log
from app.model.game_state import GameState


def change_npc_status(state: GameState, npc_id: str, status: str):
    log("tools", f"calling set_npc_status {npc_id} -> {status}")

    npc = state["npcs"].get(npc_id)

    if not npc:
        log("tools", f"NPC {npc_id} não existe")
        return f"NPC {npc_id} não existe"

    old_status = npc["status"]
    npc["status"] = status
    
    log("tools", f"{npc['name']} mudou de status {old_status} para {status}")
    return f"{npc['name']} mudou de status {old_status} para {status}"