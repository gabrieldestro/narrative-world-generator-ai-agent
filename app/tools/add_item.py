import traceback

from app.logging.state_logger import log
from app.model.game_state import GameState


def add_item(state: GameState, item: str):
    try:        
        state["player_state"]["inventory"].append(item)

        print(f"O jogador recebeu {item}")
        log("tools", f"O jogador recebeu {item}")
    except:
        traceback.print_exc()

    return f"O jogador recebeu {item}"
