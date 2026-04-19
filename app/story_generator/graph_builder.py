from langgraph.graph import StateGraph, END
from app.model.story_state import StoryState
from app.story_generator.nodes.planning_node import planning_node
from app.story_generator.nodes.chapter_split_node import chapter_split_node
from app.story_generator.nodes.writing_node import writing_node
from app.story_generator.nodes.summary_update_node import summary_update_node

def should_continue(state: StoryState):
    idx = state.get("current_chapter_index", 0)
    chapters = state.get("chapters_plan", [])
    
    if idx < len(chapters):
        return "writing"
    return END

def initial_route(state: StoryState):
    # If we already have the chapter plan and are resuming, go to writing directly
    if state.get("chapters_plan") and len(state.get("chapters_plan")) > 0:
        return "writing"
    # Otherwise fresh start
    return "planning"

def build_story_graph():
    builder = StateGraph(StoryState)
    
    builder.add_node("planning", planning_node)
    builder.add_node("chapter_split", chapter_split_node)
    builder.add_node("writing", writing_node)
    builder.add_node("summary_update", summary_update_node)
    
    # Use conditional entry point based on the state payload
    builder.set_conditional_entry_point(
        initial_route,
        {
            "planning": "planning",
            "writing": "writing"
        }
    )
    
    builder.add_edge("planning", "chapter_split")
    builder.add_edge("chapter_split", "writing")
    builder.add_edge("writing", "summary_update")
    
    builder.add_conditional_edges(
        "summary_update",
        should_continue,
        {
            "writing": "writing",
            END: END
        }
    )
    
    return builder.compile()
