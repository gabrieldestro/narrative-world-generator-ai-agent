import os
from dotenv import load_dotenv

from game_world.world import initialize_game
from engine.graph_builder import build_graph

def main():
    state = initialize_game()
    graph = build_graph()

    print("=== SIMULADOR ===")

    # 🔥 PRIMEIRA CHAMADA AUTOMÁTICA
    state = graph.invoke(state)

    # 🎮 LOOP DE INTERAÇÃO
    while True:
        user_input = input("\n> ")

        if user_input.strip().lower() in ["sair", "exit", "quit"]:
            print("\nEncerrando simulação...")
            break

        # Atualiza input do jogador
        state["player_input"] = user_input

        # Invoca LLM
        state = graph.invoke(state)


if __name__ == "__main__":
    main()