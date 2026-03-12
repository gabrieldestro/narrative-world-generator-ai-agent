from app.config import SIMULATION_TYPE
from app.consts import COMPLETE_SIMULATION
from app.model.game_state import GameState


def get_inventory_context(state: GameState):
    inventory = ""
    if (SIMULATION_TYPE == COMPLETE_SIMULATION):
        inventory = f"Inventário: {", ".join(state['player_state']["inventory"])}"
    
    return inventory