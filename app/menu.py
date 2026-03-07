from app.game_world.world import initialize_world
from app.engine.graph_builder import build_graph
from app.logging.state_logger import log_game_state, log
from app.ui.print_terminal import *
from app.repository.save_repository import *
from app.repository.worlds_repository import *
from app.game_world.world import DEFAULT_WORLD

def ask_player_choice(state):
    print_player_options(state)

    choice = input("> ").strip()

    if choice == "0":
        state = choose_finish(state)

    elif choice == "1":
        state = choose_action(state)

    elif choice == "2":
        state = choose_speak(state)

    elif choice == "4":
        state = choose_save(state)

    else:
        state = choose_wait(state)

    return state


def choose_action(state):
    action = input("Descreva sua ação: ")
    state["turn_state"] = {
        "player_choice_type": "act",
        "player_content": action,
        "target_npc_id": None
    }
    log("Player", f"1 - {action}")
    
    return state

def choose_speak(state):
    speech = input("O que você quer dizer? ")

    target_id = None
    '''for npc_id, npc in state["npcs"].items():
        if npc["name"].lower() == target.lower():
            target_id = npc_id'''

    state["turn_state"] = {
        "player_choice_type": "speak",
        "player_content": speech,
        "target_npc_id": None
    }
    log("Player", f"2: {speech}")
    
    return state

def choose_move(state):
    location = input("Para onde você quer se mover? ")
    state["player_state"]["current_location"] = location

    state["turn_state"] = {
        "player_choice_type": "move",
        "player_content": f"O jogador se move para {location}",
        "target_npc_id": None
    }

    log("Player", f"3: O jogador se move para {location}")
    
    return state

def choose_wait(state):
    state["turn_state"] = {
            "player_choice_type": "continue",
            "player_content": "",
            "target_npc_id": None
        }
    
    return state

def choose_save(state):
    state["turn_state"] = {
            "player_choice_type": "save",
            "player_content": None,
            "target_npc_id": None
        }
    
    return state

def choose_finish(state):
    state["turn_state"] = {
            "player_choice_type": "finish",
            "player_content": None,
            "target_npc_id": None
        }
    
    return state

def load_world_template():
    worlds = list_worlds()

    if not worlds:
        print("Nenhuma template encontrado.")
        return DEFAULT_WORLD

    print("Templates disponíveis:")
    for i, save in enumerate(worlds):
        print(f"{i + 1}. {save}")

    choice = int(input("Escolha um template: ")) - 1

    if 0 <= choice < len(worlds):
        return load_world(worlds[choice])
    else:
        print("Opção inválida, escolhendo a padrão.")
        return DEFAULT_WORLD
    
def load_save():
    saves = list_saves()

    if not saves:
        print("Nenhum save encontrado.")
        return None

    print("Saves disponíveis:")
    for i, save in enumerate(saves):
        print(f"{i + 1}. {save}")

    choice = int(input("Escolha um save: ")) - 1

    if 0 <= choice < len(saves):
        return load_game(saves[choice])
    else:
        print("Opção inválida.")
        return None
    
def print_player_options(state):
    print("\nTurno", state["turn_number"])
    print("Local:", state["player_state"]["current_location"])
    print("\n1 - Agir")
    print("2 - Falar")
    print("3 - Continuar")
    print("4 - Salvar narrativa")
    print("0 - Sair")

def print_init_options():
    print("\nEscolha uma opção:")
    print("\n1 - Nova narrativa")
    print("2 - Carregar")
    print("0 - Sair")
