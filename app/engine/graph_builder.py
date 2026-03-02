from langgraph.graph import StateGraph
from app.engine.tools_phase import tools_phase
from app.model.game_state import GameState

from app.engine.player_phase import player_phase
from app.engine.npc_phase import npc_phase
from app.engine.world_phase import world_phase
from app.engine.summary_phase import summary_phase

def has_tool_calls(state: GameState):
    return bool(state.get("pending_tool_calls"))

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
        has_tool_calls,
        {
            True: "tools",
            False: "summary"
        }
    )

    builder.add_edge("tools", "summary")

    return builder.compile()