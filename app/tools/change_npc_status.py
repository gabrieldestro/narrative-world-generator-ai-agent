from app.logging.state_logger import log
from app.model.game_state import GameState
import traceback


def change_npc_status(state: GameState, npc_id: str, status: str):
    message = ""

    try:
        log("tools", f"calling set_npc_status {npc_id} -> {status}")

        npc = state["npcs"].get(npc_id)

        if not npc:
            log("tools", f"NPC {npc_id} não existe")
            return f"NPC {npc_id} não existe"

        old_status = npc["status"]
        npc["status"] = status
        
        log("tools", f"{npc['name']} mudou de status {old_status} para {status}")
        message = f"{npc['name']} mudou de status {old_status} para {status}"
        print(message)
    except:
        traceback.print_exc()


    return message