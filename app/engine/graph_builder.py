from langgraph.graph import END, StateGraph
from app.engine.tools_phase import tools_phase
from app.model.game_state import GameState

from app.engine.player_phase import player_phase
from app.engine.npc_phase import npc_phase
from app.engine.world_phase import world_phase
from app.engine.summary_phase import summary_phase

def has_tool_calls(state: GameState):
    return bool(state.get("pending_tool_calls"))

def should_run_tools(state: GameState):
    if state.get("pending_tool_calls"):
        return "tools"
    return "summary"

def build_graph():

    builder = StateGraph(GameState)

    builder.add_node("player", player_phase)
    builder.add_node("npc", npc_phase)
    builder.add_node("world", world_phase)
    builder.add_node("summary", summary_phase)
    builder.add_node("tools", tools_phase)

    builder.set_entry_point("player")

    builder.add_edge("player", "npc")
    builder.add_edge("npc", "world")
    builder.add_edge("world", "summary")

    builder.add_conditional_edges(
        "world",
        should_run_tools,
        {
            "tools": "tools",
            "summary": "summary"
        }
    )

    builder.add_edge("summary", END)

    return builder.compile()