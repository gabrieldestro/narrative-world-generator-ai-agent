from app.engine.context.inventory_context import get_inventory_context
from app.engine.context.npc_context import get_npc_context
from app.engine.context.world_context import get_world_context
from app.llm import call_llm
from app.model.game_state import GameState
from app.repository.story_repository import append_story
from app.ui.print_terminal import print_npc
from app.logging.state_logger import log
from app.consts import SCENE_LOG_MEMORY

def simulation_phase_lite(state):
    turn = state.get("turn_state")
    player_action = ""
    if turn:
        player_action = f"{turn['player_content']}"

    user_prompt = f"""
    O jogador fez:
        {player_action}

    """

    response = call_llm(_get_system_prompt(state), user_prompt, state["turn_number"])

    if (turn):
        state["scene_log"].append(f"Jogador: {player_action}")
        append_story(state, f"Jogador: {player_action}")
    state["scene_log"].append(response)
    append_story(state, response)

    print_npc("NPCs", response)
    log("NPCs", response)

    return state

def _get_system_prompt(state: GameState):
    location = state["player_state"]["current_location"]
    history = "\n".join(state['scene_log'][-SCENE_LOG_MEMORY:])

    world_context = get_world_context(state)
    npc_context = get_npc_context(state)
    inventory = get_inventory_context(state)

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
    {world_context}

    Local atual:
    {location}

    NPCs presentes:
    {npc_context}

    NPCs podem falar entre si, reagir ao jogador ou agir conforme seus objetivos.
    Faça os NPCs serem ativos participantes que movem a história, não apenas rejam as ações do jogador.
    """


    if (SCENE_LOG_MEMORY > 0):
        system_prompt += f"""
        Histórico recente:
            {history}
        """

    return system_prompt
