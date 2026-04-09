from app.logging.state_logger import log
from app.model.game_state import GameState
import traceback


def move_player(state: GameState, to_location: str):
    destination = ""

    try:
        log("tools", f"calling move_player {to_location}")

        destination = to_location
        current = state["player_state"]["current_location"]

        location = state["world"]["locations"][current]

        if destination not in location["connected_to"]:
            return f"O jogador não pode ir para {destination}"

        state["player_state"]["current_location"] = destination

        log("tools", f"Jogador moveu-se de {current} para {destination}!")
        print(f"Jogador moveu-se de {current} para {destination}!")
    except:
        traceback.print_exc()

    return f"Jogador moveu-se para {destination}"