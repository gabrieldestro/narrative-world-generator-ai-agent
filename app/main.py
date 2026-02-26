import os
from dotenv import load_dotenv

from game_world.world import initialize_game
from engine.graph_builder import build_graph

def main():
    state = initialize_game()
    graph = build_graph()

    print("=== SIMULADOR ===")

    # Primeira chamada automática
    state = graph.invoke(state)

    while True:
        print("\nTurno", state["turn_number"])
        print("Local:", state["player_location"])
        print("\n1 - Agir")
        print("2 - Falar")
        print("3 - Não fazer nada")
        print("0 - Sair")

        choice = input("> ").strip()

        if choice == "0":
            print("\nEncerrando simulação...")
            return  # encerra totalmente

        if choice == "1":
            action = input("Descreva sua ação: ")
            state["turn_state"] = {
                "player_choice_type": "act",
                "player_content": action,
                "target_npc_id": None
            }

        elif choice == "2":
            speech = input("O que você quer dizer? ")
            target = input("Para quem? ")

            target_id = None
            for npc_id, npc in state["npcs"].items():
                if npc["name"].lower() == target.lower():
                    target_id = npc_id

            state["turn_state"] = {
                "player_choice_type": "speak",
                "player_content": speech,
                "target_npc_id": target_id
            }

        else:
            state["turn_state"] = {
                "player_choice_type": "wait",
                "player_content": "",
                "target_npc_id": None
            }

        state = graph.invoke(state)

if __name__ == "__main__":
    main()