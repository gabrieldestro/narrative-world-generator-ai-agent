from app.services.simulation_service import start_new_simulation, resume_simulation, process_turn, save_current_simulation
from app.services.story_service import generate_story, resume_story
from app.services.config_service import load_environment_variables, update_environment_variable, list_world_templates, get_world_template, save_world_template
from app.repository.save_repository import list_saves
from app.repository.story_generation_repository import list_story_saves

# ---- SIMULATION ROUTES ----
def api_start_simulation(template_filename: str):
    return start_new_simulation(template_filename)

def api_resume_simulation(save_filename: str):
    return resume_simulation(save_filename)

def api_process_turn(state: dict, action_payload: dict):
    return process_turn(state, action_payload)

def api_save_simulation(state: dict):
    save_current_simulation(state)
    return {"status": "success"}

def api_list_simulation_saves():
    return list_saves()

# ---- STORY ROUTES ----
def api_generate_story(template_filename: str):
    return generate_story(template_filename)

def api_resume_story(save_filename: str):
    return resume_story(save_filename)

def api_list_story_saves():
    return list_story_saves()

# ---- CONFIG & TEMPLATES ROUTES ----
def api_get_env():
    return load_environment_variables()

def api_update_env(key: str, value: str):
    update_environment_variable(key, value)
    return {"status": "success"}

def api_list_templates():
    return list_world_templates()

def api_get_template(filename: str):
    return get_world_template(filename)

def api_save_template(filename: str, data: dict):
    save_world_template(filename, data)
    return {"status": "success"}
