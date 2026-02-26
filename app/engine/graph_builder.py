from langgraph.graph import StateGraph
from app.model.game_state import GameState

from app.engine.player_phase import player_phase
from app.engine.npc_phase import npc_phase
from app.engine.world_phase import world_phase


def build_graph():

    builder = StateGraph(GameState)

    builder.add_node("player", player_phase)
    builder.add_node("npc", npc_phase)
    builder.add_node("world", world_phase)

    builder.set_entry_point("player")

    builder.add_edge("player", "npc")
    builder.add_edge("npc", "world")

    return builder.compile()