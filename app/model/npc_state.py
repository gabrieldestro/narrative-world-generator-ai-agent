from typing import TypedDict, Dict, List, Optional


class NPCState(TypedDict):
    id: str
    name: str
    personality: str
    goals: List[str]
    current_location: str
    memory: List[str]
    status: str