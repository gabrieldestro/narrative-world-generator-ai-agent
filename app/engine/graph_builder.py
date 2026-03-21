from app.config import SIMULATION_TYPE
from app.consts import COMPLETE_SIMULATION, LITE_SIMULATION
from app.engine.node.simulation_phase_lite import simulation_phase_lite
from app.tools.add_item import add_item
from app.tools.add_world_fact import add_world_fact
from app.tools.change_npc_status import change_npc_status
from app.tools.complete_quest import complete_quest
from app.tools.create_location import create_location
from app.tools.create_npc import create_npc
from app.tools.move_npc import move_npc
from app.tools.move_player import move_player
from app.tools.remove_item import remove_item
from app.tools.remove_world_fact import remove_world_fact
from app.tools.tool_executor import ToolExecutor
from app.tools.update_world_fact import update_world_fact
from langgraph.graph import END, StateGraph
from app.model.game_state import GameState
from app.engine.node.tools_phase import tools_phase
from app.engine.node.simulation_phase import simulation_phase
from app.engine.node.world_phase import world_phase
from app.engine.node.summary_phase import summary_phase

def build_graph():
    if (SIMULATION_TYPE == LITE_SIMULATION):
        return build_graph_lite()
    else:
        return build_graph_complete()

def has_tool_calls(state: GameState):
    return bool(state.get("pending_tool_calls"))

def should_run_tools(state: GameState):
    if state.get("pending_tool_calls"):
        return "tools"
    return "summary"

def build_graph_complete():

    builder = StateGraph(GameState)

    builder.add_node("simulation", simulation_phase)
    builder.add_node("summary", summary_phase)
    builder.add_node("tools", tools_phase)

    builder.set_entry_point("simulation")

    builder.add_edge("simulation", "summary")

    builder.add_conditional_edges(
        "simulation",
        should_run_tools,
        {
            "tools": "tools",
            "summary": "summary"
        }
    )

    builder.add_edge("summary", END)

    return builder.compile()


def build_graph_lite():

    builder = StateGraph(GameState)

    builder.add_node("simulation", simulation_phase_lite)
    builder.add_node("summary", summary_phase)

    builder.set_entry_point("simulation")

    builder.add_edge("simulation", "summary")

    return builder.compile()


def build_tools(state):
    if (SIMULATION_TYPE == COMPLETE_SIMULATION):
        tool_executor = ToolExecutor()
        tool_executor.register("create_location", create_location)
        tool_executor.register("create_npc", create_npc)
        tool_executor.register("change_npc_status", change_npc_status)
        tool_executor.register("move_npc", move_npc)
        tool_executor.register("move_player", move_player)
        tool_executor.register("add_item", add_item)
        tool_executor.register("remove_item", remove_item)
        tool_executor.register("complete_quest", complete_quest)
        tool_executor.register("add_world_fact", add_world_fact)
        tool_executor.register("update_world_fact", update_world_fact)
        tool_executor.register("remove_world_fact", remove_world_fact)

        state["tool_executor"] = tool_executor

    return state

