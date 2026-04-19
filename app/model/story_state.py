from typing import TypedDict, List, Optional
from app.model.world_state import WorldState

class ChapterPlan(TypedDict):
    title: str
    synopsis: str

class StoryState(TypedDict):
    # World descriptor
    world: WorldState
    name: str
    additional_info: str
    
    # Story generation properties
    simulation_id: str
    story_title: Optional[str]
    story_outline: Optional[str]
    chapters_plan: List[ChapterPlan] # List of chapters with title and synopsis
    current_chapter_index: int
    story_summary: str
    written_chapters: List[str]
