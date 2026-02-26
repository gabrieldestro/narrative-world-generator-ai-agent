from typing import TypedDict, Optional

class TurnState(TypedDict):
    player_choice_type: str
    player_content: str
    target_npc_id: Optional[str]