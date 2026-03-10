from app.engine.graph_builder import build_graph, build_tools
from app.logging.state_logger import log_game_state
from app.ui.print_terminal import *
from app.repository.save_repository import *

from app.menu import *

def main():
    print_simulation_mode()
    graph = build_graph()

    print_init_options()
    choice = input("> ").strip()

    state = None
    if (choice == "1"):
        state = load_world_template()
        state = build_tools(state)
        state = graph.invoke(state)

    elif (choice == "2"):
        state = load_save()
        state = build_tools(state)
        print_npc("NPCs", state["scene_log"][-1])
        
    else:
        print("Encerrando simulação")
        return

    while True:
        try:
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
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    main()