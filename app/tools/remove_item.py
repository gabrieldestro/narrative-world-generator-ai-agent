from app.logging.state_logger import log
from app.model.game_state import GameState
import traceback

def remove_item(state: GameState, item: str):
    try:
        log("tools", f"reomve_item")
        
        if item in state["player_state"]["inventory"]:
            state["player_state"]["inventory"].remove(item)

            log("tools", f"O jogador perdeu/usou {item}")
            print(f"O jogador perdeu/usou {item}")
        else:
            log("tools", f"Item {item} não existe")
            print(f"Item {item} não existe")
    except:
        traceback.print_exc()

    return f"O jogador perdeu/usou {item}"