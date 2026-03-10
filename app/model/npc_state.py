from typing import TypedDict, Dict, List, Optional


class NPCState(TypedDict):
    id: str
    name: str
    description: str
    goals: List[str]
    current_location: str
    status: str