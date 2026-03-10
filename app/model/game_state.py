import operator
from typing import Annotated, TypedDict, Dict, List, Optional
import uuid
from app.model.quest_state import QuestState
from app.model.world_state import WorldState
from app.model.location_state import LocationState
from app.model.player_state import PlayerState
from app.model.npc_state import NPCState
from app.model.turn_state import TurnState
from app.tools.tool_executor import ToolExecutor   

class GameState(TypedDict):
    # world descriptor
    name: str
    additional_info: str
    world: WorldState
    genres: List[str]
    quests: Dict[str, QuestState]
    npcs: Dict[str, NPCState]
    player_state: PlayerState
    turn_state: Optional[TurnState]
    scene_log: List[str]
    turn_number: int

    # simulation engine properties
    simulation_id: uuid.UUID
    pending_tool_calls: Optional[List[dict]]
    last_llm_message: Optional[str]
    tool_executor: ToolExecutor