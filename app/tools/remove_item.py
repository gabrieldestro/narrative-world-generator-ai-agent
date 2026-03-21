from app.logging.state_logger import log
from app.model.game_state import GameState
import traceback

def remove_item(state: GameState, item: str):
    try:
        log("tools", f"reomve_item")
        
        state["player_state"]["inventory"].remove(item)

        log("tools", f"O jogador perdeu/usou {item}")
    except:
        traceback.print_exc()

    return f"O jogador perdeu/usou {item}"