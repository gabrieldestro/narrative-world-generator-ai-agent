import random
from urllib import response
from app.consts import RANDOM_EVENT_CHANCE
from app.llm import call_llm
from app.ui.print_terminal import print_world
from app.logging.state_logger import log

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
        log("World", response)

    return state