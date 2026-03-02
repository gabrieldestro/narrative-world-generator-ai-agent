import random
from urllib import response
from app.config import PROVIDER_NAME
from app.consts import RANDOM_EVENT_CHANCE
from app.llm import call_llm
from app.llm_providers.factory import get_llm_provider
from app.model.game_state import GameState
from app.tools.tools_schema import WORLD_TOOLS_SCHEMA
from app.ui.print_terminal import print_world
from app.logging.state_logger import log


def world_phase(state):

    provider = get_llm_provider(PROVIDER_NAME)

    system_prompt = f"""
    Baseado na ultima rodada de iterações:

    Histórico recente:
        {state['scene_log'][-2:]}

    Decida:
    Se precisar criar um novo local, use a ferramenta create_location.
    Se precisar criar um novo NPC, use create_npc.
    Caso contrário, não faça nada.
    """

    user_prompt = f"""
    Mundo atual:
    {state['world']['world_prompt']}

    Local atual do jogador:
    {state['player_state']['current_location']}
    """

    response = provider.generate_with_tools(
        system_prompt,
        user_prompt,
        tools=WORLD_TOOLS_SCHEMA,
        turn_id=state["turn_number"]
    )

    updates = {
        "last_llm_message": response.content
    }

    if response.tool_calls:
        updates["pending_tool_calls"] = response.tool_calls
    else:
        updates["pending_tool_calls"] = []
        updates["scene_log"] = state["scene_log"] + [response.content]

    return updates