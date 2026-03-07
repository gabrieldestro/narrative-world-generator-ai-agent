from app.model.game_state import GameState

def remove_item(state: GameState, item: str):
    print(f"reomve_item")
    
    state["player_state"]["inventory"].remove(item)

    print(f"O jogador perdeu/usou {item}")
    return f"O jogador perdeu/usou {item}"