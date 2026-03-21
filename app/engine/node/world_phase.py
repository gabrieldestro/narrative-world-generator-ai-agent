from app.llm import *
from app.tools.tools_schema import WORLD_TOOLS_SCHEMA


def world_phase(state):
    # quebrar em funções menores
    world_context = ""

    for i, line in enumerate(state["world"]["world_prompt"]):
        world_context += f"{i}: {line}\n"

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

    quests = [
        quest for quest in state["quests"].values()
        if
            quest["status"] == "active"
    ]

    quests_context = ""
    for quest in quests:
        quests_context += f"""
        ID: {quest['id']}
        Nome: {quest['name']}
        Nome: {quest['description']}
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

    Inventário do jogador:
        {", ".join(state['player_state']["inventory"])}

    Mundo atual:
        {world_context}

    Quests:
        {quests_context}

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
        O estado do mundo é representado como uma lista numerada de fatos.
        Sempre use o índice correto ao modificar ou remover fatos.

        Use ferramentas quando ocorrer:

        - criação de novos locais
        - criação de novos NPCs
        - movimento de NPCs ou do jogador entre locais
        - mudança de estado ou objetivos de NPCs
        - criação ou resolução de eventos do mundo
        - adicionar um novo fato usando add_world_fact
        - modificar um fato existente usando update_world_fact
        - remover um fato que não é mais verdadeiro usando remove_world_fact
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