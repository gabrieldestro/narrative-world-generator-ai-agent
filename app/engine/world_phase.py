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
        ID: {npc['id']}
        Nome: {npc['name']}
        Local antes do ultimo histórico: {npc['current_location']}
        """

    locations_context = ""
    for location in state['world']['locations'].values():
        locations_context += f"""
        Nome: {location['name']}
        """

    history = "\n".join(state['scene_log'][-2:])

    system_prompt = f"""
    Baseado na ultima rodada de iterações:

    Locais atuais:
        {locations_context}

    NPCs atuais:
        {npc_context}

    Local atual do jogador antes do útiimo histórico:
        {state['player_state']['current_location']}

    Mundo atual:
        {state['world']['world_prompt']}
            
    Histórico recente:
        {history}
    """

    user_prompt = f"""
        Decida se alguma mudança no estado do mundo precisa ocorrer.

        IMPORTANTE:
        Se um personagem ou NPC se mover de um local para outro,
        você DEVE usar a ferramenta move_npc ou move_player para
        atualizar o estado do mundo.

        A narrativa sozinha não altera o estado do mundo.

        Use ferramentas quando ocorrer:

        - criação de novos locais
        - criação de novos NPCs
        - movimento de NPCs ou do jogador entre locais
        - mudança de estado ou objetivos de NPCs
        - criação ou resolução de eventos do mundo
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