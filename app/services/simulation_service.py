import uuid
from app.engine.graph_builder import build_graph, build_tools
from app.repository.worlds_repository import load_world
from app.repository.save_repository import load_game, save_game
from app.repository.story_repository import save_story
from app.logging.state_logger import log_game_state

def start_new_simulation(template_filename: str) -> dict:
    state = load_world(template_filename)
    if not state:
        raise ValueError(f"Template {template_filename} não encontrado.")
    
    state['simulation_id'] = str(uuid.uuid4())
    state['messages'] = []
    if 'scene_log' not in state:
        state['scene_log'] = []
    state = build_tools(state)
    
    graph = build_graph()
    state = graph.invoke(state)
    
    return state

def resume_simulation(save_filename: str) -> dict:
    state = load_game(save_filename)
    if not state:
        raise ValueError(f"Save {save_filename} não encontrado.")
        
    state = build_tools(state)
    return state

def process_turn(state: dict, action_payload: dict) -> dict:
    """
    action_payload deve conter:
    {
        "player_choice_type": "act" | "speak" | "move" | "continue" | "finish" | "save",
        "player_content": "texto da ação",
        "target_npc_id": None
    }
    """
    
    # Se a ação for de salvar, não precisa invocar o grafo
    if action_payload.get("player_choice_type") == "save":
        save_current_simulation(state)
        return state
        
    # Se for de encerrar, apenas retorna
    if action_payload.get("player_choice_type") == "finish":
        return state
        
    # Prepara o state para o proximo turno
    state["turn_state"] = action_payload
    
    graph = build_graph()
    state = graph.invoke(state)
    log_game_state(state)
    
    state["turn_number"] += 1
    return state

def save_current_simulation(state: dict):
    save_game(state)
    save_story(state)
