import random
from urllib import response
from app.config import PROVIDER_NAME
from app.consts import RANDOM_EVENT_CHANCE
from app.llm import *
from app.llm_providers.factory import get_llm_provider
from app.model.game_state import GameState
from app.tools.tools_schema import WORLD_TOOLS_SCHEMA
from app.ui.print_terminal import print_world
from app.logging.state_logger import log


def world_phase(state):
    print("world_phase")
    npcs = [
        npc for npc in state["npcs"].values()
        if npc["status"] == "active"
    ]

    if not npcs:
        return state

    npc_context = ""
    for npc in npcs:
        npc_context += f"""
        Nome: {npc['name']}
        """

    locations_context = ""
    for location in state['world']['locations'].values():
        locations_context += f"""
        Nome: {location['name']}
        """

    system_prompt = f"""
    Baseado na ultima rodada de iterações:

    Locais atuais:
        {locations_context}

    NPCs atuais:
        {npc_context}
        
    Histórico recente:
        {state['scene_log'][-2:]}

    Mundo atual:
    {state['world']['world_prompt']}

    Local atual do jogador:
    {state['player_state']['current_location']}
    """

    user_prompt = f"""
        Decida:
        Se precisar criar um novo local, use a ferramenta create_location.
        Se precisar criar um novo NPC, use create_npc.
        Caso contrário, não faça nada.

        Instruções:
        Somente crie ferramentas e Npcs relevantes, não polua a história com personagens ou locais demais, se for um personagem ou local não importante, não o crie.
        SOMENTE USE AS FERRAMENTAS SE O HíSTÓRICO APRESENTAR UM LOCAL OU NPC Não existente!
    """
    response = call_llm_with_tools(system_prompt, user_prompt, tools=WORLD_TOOLS_SCHEMA, turn_id=state["turn_number"])

    updates = {
        "last_llm_message": response.content
    }

    if response.tool_calls:
        updates["pending_tool_calls"] = response.tool_calls
    else:
        updates["pending_tool_calls"] = []
#        updates["scene_log"] = state["scene_log"] + [response.content]

    return updates