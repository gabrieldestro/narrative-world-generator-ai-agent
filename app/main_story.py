import traceback
import uuid
import json

from app.story_generator.graph_builder import build_story_graph
from app.repository.story_generation_repository import load_story_generation, list_story_saves, export_final_story
from app.menu import load_world_template

def print_story_init_options():
    print("\n===============================")
    print(" GERADOR DE HISTÓRIAS COMPLETAS")
    print("===============================\n")
    print("1 - Nova Geração de História")
    print("2 - Retomar Geração Interrompida")
    print("0 - Sair")

def load_save():
    saves = list_story_saves()
    if not saves:
        print("Nenhuma geração interrompida encontrada.")
        return None

    print("\nSaves disponíveis:")
    for i, save in enumerate(saves):
        print(f"{i + 1}. {save}")

    try:
        choice = int(input("Escolha um save: ")) - 1
        if 0 <= choice < len(saves):
            return load_story_generation(saves[choice])
        else:
            print("Opção inválida.")
    except Exception as e:
        print(f"Entrada inválida. ({e})")
        
    return None

def main():
    graph = build_story_graph()

    print_story_init_options()
    choice = input("> ").strip()

    state = None
    if choice == "1":
        # load_world_template already asks the user via terminal for the world JSON
        world_data = load_world_template()
        
        # O worlds_repository retorna o dicionário inteiro do .json
        # Vamos estruturar no StoryState
        state = {
            "world": world_data.get("world", {}),
            "name": world_data.get("name", "Mundo Desconhecido"),
            "additional_info": world_data.get("additional_info", ""),
            "simulation_id": str(uuid.uuid4())
        }
        
    elif choice == "2":
        state = load_save()
        if not state:
            return
    else:
        print("Encerrando gerador.")
        return

    print("\n--- INCIANDO THREAD DE GERAÇÃO ---")
    try:
        # Começa (ou continua) o fluxo de geração de história até chegar no nó END
        # Usamos stream mode ou invoke direto? Invoke é mais unificado.
        # Os nos de print vao atualizando a logica
        final_state = graph.invoke(state)
        
        print("\n--- GERAÇÃO CONCLUÍDA ---")
        
        export_final_story(final_state)
        
    except Exception as e:
        print("Um erro ocorreu durante a geração na rede LangGraph:", e)
        traceback.print_exc()

if __name__ == "__main__":
    main()
