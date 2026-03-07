import os

from app.game_world.world import initialize_world
from app.engine.graph_builder import build_graph
from app.logging.state_logger import log_game_state, log
from app.tools.add_item import add_item
from app.tools.complet_quest import complete_quest
from app.tools.create_location import create_location
from app.tools.create_npc import create_npc
from app.tools.move_npc import move_npc
from app.tools.move_player import move_player
from app.tools.remove_item import remove_item
from app.tools.tool_executor import ToolExecutor
from app.ui.print_terminal import *
from app.repository.save_repository import *

from app.menu import *

def create_tools(state):
    tool_executor = ToolExecutor()
    tool_executor.register("create_location", create_location)
    tool_executor.register("create_npc", create_npc)
    tool_executor.register("move_npc", move_npc)
    tool_executor.register("move_player", move_player)
    tool_executor.register("add_item", add_item)
    tool_executor.register("remove_item", remove_item)
    tool_executor.register("complete_quest", complete_quest)

    state["tool_executor"] = tool_executor

    return state


def main():
    graph = build_graph()

    print_init_options()
    choice = input("> ").strip()

    state = None
    if (choice == "1"):
        state = load_world_template()
        state = create_tools(state)
        state = graph.invoke(state)

    elif (choice == "2"):
        state = load_save()
        state = create_tools(state)
        print_npc("NPCs", state["scene_log"][-1])
        
    else:
        print("Encerrando simulação")
        return

    while True:
        state = ask_player_choice(state)
        if (state["turn_state"]["player_choice_type"] == "finish"):
            print("Encerrando simulação")
            return
        
        if (state["turn_state"]["player_choice_type"] == "save"):
            save_game(state)
            continue
        
        state = graph.invoke(state)
        log_game_state(state)
        
        print(f"End turn {state["turn_number"]}")
        state["turn_number"] += 1

if __name__ == "__main__":
    main()