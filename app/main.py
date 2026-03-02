import os

from app.game_world.world import initialize_world
from app.engine.graph_builder import build_graph
from app.logging.state_logger import log_game_state, log
from app.tools.create_location import create_location
from app.tools.create_npc import create_npc
from app.tools.tool_executor import ToolExecutor
from app.ui.print_terminal import *
from app.repository.save_repository import *

from app.menu import *

def main():
    graph = build_graph()

    print_init_options()
    choice = input("> ").strip()

    state = None
    if (choice == "1"):
        state = load_world_template()
        state = graph.invoke(state)

    elif (choice == "2"):
        state = load_save()
        print_npc("NPCs", state["scene_log"][-1])
        
    else:
        print("Encerrando simulação")
        return
    
    tool_executor = ToolExecutor()
    tool_executor.register("create_location", create_location)
    tool_executor.register("create_npc", create_npc)
    state["tool_executor"] = tool_executor
    
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

        state["turn_number"] += 1

if __name__ == "__main__":
    main()