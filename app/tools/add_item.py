import traceback

from app.model.game_state import GameState


def add_item(state: GameState, item: str):
    try:
        print(f"add_item")
        
        state["player_state"]["inventory"].append(item)

        print(f"O jogador recebeu {item}")
    except:
        traceback.print_exc()

    return f"O jogador recebeu {item}"
