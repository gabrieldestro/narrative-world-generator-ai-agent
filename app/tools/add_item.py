from app.model.game_state import GameState


def add_item(state: GameState, item: str):
    print(f"add_item")
    
    state["player_state"]["inventory"].append(item)

    print(f"O jogador recebeu {item}")
    return f"O jogador recebeu {item}"