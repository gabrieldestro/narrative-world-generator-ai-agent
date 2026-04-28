import uuid
from app.story_generator.graph_builder import build_story_graph
from app.repository.worlds_repository import load_world
from app.repository.story_generation_repository import load_story_generation, export_final_story

def generate_story(template_filename: str) -> dict:
    world_data = load_world(template_filename)
    if not world_data:
        raise ValueError(f"Template {template_filename} não encontrado.")
        
    state = {
        "world": world_data.get("world", {}),
        "name": world_data.get("name", "Mundo Desconhecido"),
        "additional_info": world_data.get("additional_info", ""),
        "simulation_id": str(uuid.uuid4())
    }
    
    graph = build_story_graph()
    final_state = graph.invoke(state)
    
    export_final_story(final_state)
    return final_state

def resume_story(save_filename: str) -> dict:
    state = load_story_generation(save_filename)
    if not state:
        raise ValueError(f"Save {save_filename} não encontrado.")
        
    graph = build_story_graph()
    final_state = graph.invoke(state)
    
    export_final_story(final_state)
    return final_state
