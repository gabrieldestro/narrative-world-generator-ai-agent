from typing import TypedDict, Dict, List, Optional
from model.world_state import WorldState
from .location_state import LocationState
from .npc_state import NPCState
from .turn_state import TurnState   

class GameState(TypedDict):
    world: WorldState
    npcs: Dict[str, NPCState]
    player_location: str
    turn_state: Optional[TurnState]
    scene_log: List[str]
    turn_number: int