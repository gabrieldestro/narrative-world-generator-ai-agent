from typing import TypedDict, Dict, List, Optional
from app.model.world_state import WorldState
from app.model.location_state import LocationState
from app.model.player_state import PlayerState
from app.model.npc_state import NPCState
from app.model.turn_state import TurnState   

class GameState(TypedDict):
    world: WorldState
    npcs: Dict[str, NPCState]
    player_state: PlayerState
    turn_state: Optional[TurnState]
    scene_log: List[str]
    turn_number: int