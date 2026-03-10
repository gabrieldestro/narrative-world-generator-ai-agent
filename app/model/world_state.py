from typing import TypedDict, Dict, List
from app.model.location_state import LocationState

class WorldState(TypedDict):
    world_prompt: str
    locations: Dict[str, LocationState]
