import random
from urllib import response
from app.consts import RANDOM_EVENT_CHANCE
from app.llm import call_llm
from app.engine.ui import print_world
from app.engine.state_logger import log_game_state

def world_phase(state):

    if random.random() < RANDOM_EVENT_CHANCE:

        system_prompt = f"""
        Gere um pequeno evento emergente no mundo.

        Mundo:
        {state['world']['world_prompt']}

        Local atual:
        {state['player_location']}

        O evento deve ser sutil e natural.
        """

        response = call_llm(system_prompt, "", "")

        state["scene_log"].append(response)
        state["world"]["global_events"].append(response)

        print("\nMundo:")
        print_world(response)

    log_game_state(state)

    return state