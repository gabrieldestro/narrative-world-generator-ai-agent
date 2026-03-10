from app.config import SIMULATION_TYPE
from app.llm import call_llm
from app.repository.story_repository import append_story
from app.ui.print_terminal import print_npc
from app.logging.state_logger import log
from app.consts import COMPLETE_SIMULATION, SCENE_LOG_MEMORY

def npc_phase(state):
    location = state["player_state"]["current_location"]

    turn = state.get("turn_state")
    player_action = ""
    if turn:
        player_action = f"{turn['player_content']}"

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

    inventory = ""
    if (SIMULATION_TYPE == COMPLETE_SIMULATION):
        inventory = f"Inventário: {", ".join(state['player_state']["inventory"])}"
    
    history = "\n".join(state['scene_log'][-SCENE_LOG_MEMORY:])

    system_prompt = f"""
    Você é o narrador de um mundo Sandbox, nunca interaja com o jogador fora do contexto da história. 
    Simule o comportamento e diálogo dos personagens conforme suas características e as interações com o jogador.
    Trate o jogador pela descrição de seu personagem e nunca pelo termo 'Jogador'. Não de sugestões sobre o que o jogador pode fazer.
    
    Gêneros da história: 
    {", ".join(state['genres'])}

    Informações adicionais:
    {state['additional_info']}

    jogador:
    {state['player_state']['name']}
    {state['player_state']['description']}
    {inventory}
        
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
        {player_action}

    """

    if (SCENE_LOG_MEMORY > 0):
        system_prompt += f"""
        Histórico recente:
            {history}
        """

    response = call_llm(system_prompt, user_prompt, state["turn_number"])

    if (turn):
        state["scene_log"].append(f"Jogador: {player_action}")
        append_story(state, f"Jogador: {player_action}")
    state["scene_log"].append(response)
    append_story(state, response)

    print_npc("NPCs", response)
    log("NPCs", response)

    return state