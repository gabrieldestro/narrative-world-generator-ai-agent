from app.llm import call_llm
from app.ui.print_terminal import print_npc
from app.logging.state_logger import log
from app.consts import SCENE_LOG_MEMORY

def npc_phase(state):
    print("npc_phase")
    location = state["player_state"]["current_location"]

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
        Descrição: {npc['description']}
        Objetivos: {npc['goals']}
        """

    system_prompt = f"""
    Você é o narrador de um mundo Sandbox, nunca interaja com o jogador fora do contexto da história. 
    Simule o comportamento e diálogo dos personagens conforme suas características e as interações com o jogador.
    Trate o jogador pela descrição de seu personagem e nunca pelo termo 'Jogador'. Não de sugestões sobre o que o jogador pode fazer.
    
    Gêneros da história: 
    {state['genres']}

    Informações adicionais:
    {state['additional_info']}

    jogador:
    {state['player_state']['name']}
    {state['player_state']['description']}1

    Mundo:
    {state['world']['world_prompt']}

    Local atual:
    {location}

    NPCs presentes:
    {npc_context}

    NPCs podem falar entre si, reagir ao jogador ou agir conforme seus objetivos.
    Faça os NPCs serem ativos participantes que movem a história, não apenas rejam as ações do jogador.
    """

    user_prompt = f"""
    O jogador fez:
    {state['turn_state']}

    """

    # indicado para modelos mais robustos
    if (SCENE_LOG_MEMORY > 0):
        system_prompt += f"""
            Histórico recente:
            {state['scene_log'][-SCENE_LOG_MEMORY:]}
        """

    response = call_llm(system_prompt, user_prompt, state["turn_number"])

    state["scene_log"].append(user_prompt)
    state["scene_log"].append(response)

    for npc in npcs_here:
        npc["memory"].append(response)

    print("\nNPCs:")
    print_npc("NPCs", response)
    log("NPCs", response)

    return state