from llm import call_llm
from engine.ui import print_npc

def npc_phase(state):

    location = state["player_location"]

    npcs_here = [
        npc for npc in state["npcs"].values()
        if npc["current_location"] == location and npc["status"] == "active"
    ]

    if not npcs_here:
        return state

    npc_context = ""
    for npc in npcs_here:
        npc_context += f"""
        Nome: {npc['name']}
        Personalidade: {npc['personality']}
        Objetivos: {npc['goals']}
        """

    system_prompt = f"""
    Você simula NPCs em um RPG sandbox.

    Mundo:
    {state['world']['world_prompt']}

    Local atual:
    {location}

    NPCs presentes:
    {npc_context}

    NPCs podem falar entre si, reagir ao jogador ou agir conforme seus objetivos.
    """

    user_prompt = f"""
    O jogador fez:
    {state['turn_state']}

    Histórico recente:
    {state['scene_log'][-5:]}
    """

    response = call_llm(system_prompt, user_prompt, "1")

    state["scene_log"].append(response)

    for npc in npcs_here:
        npc["memory"].append(response)

    print("\nNPCs:")
    print_npc("NPCs", response)

    return state