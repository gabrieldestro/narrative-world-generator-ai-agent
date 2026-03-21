from app.engine.context.inventory_context import get_inventory_context
from app.engine.context.lcocations_context import get_locations_context
from app.engine.context.npc_context import get_npc_context
from app.engine.context.quests_context import get_quests_context
from app.engine.context.world_context import get_world_context
from app.llm import call_llm, call_llm_with_tools
from app.model.game_state import GameState
from app.repository.story_repository import append_story
from app.tools.tools_schema import WORLD_TOOLS_SCHEMA
from app.ui.print_terminal import print_npc
from app.logging.state_logger import log
from app.consts import SCENE_LOG_MEMORY

def simulation_phase(state: GameState):

    turn = state.get("turn_state")
    player_action = ""

    if turn:
        player_action = turn["player_content"]

    system_prompt = f"""
        Você é o narrador de um mundo sandbox.

        Simule a cena atual considerando o estado do mundo, NPCs e ação do jogador.

        NPCs podem:
        - falar
        - reagir ao jogador
        - agir de acordo com seus objetivos
        - mover-se entre locais
        - causar mudanças no mundo

        Se alguma ação alterar o estado estrutural do mundo,
        use as ferramentas apropriadas.

        Narrativa sozinha NÃO altera o estado do mundo.
        ---

        Gêneros:
        {", ".join(state['genres'])}

        Informações adicionais:
        {state['additional_info']}

        Jogador:
        {state['player_state']['name']}
        {state['player_state']['description']}

        Inventário:
        {get_inventory_context(state)}

        Local atual:
        {state['player_state']['current_location']}

        Locais:
        {get_locations_context(state)}

        NPCs:
        {get_npc_context(state)}

        Quests:
        {get_quests_context(state)}

        Estado do mundo:
        {get_world_context(state)}

        Histórico recente:
        {"\n".join(state["scene_log"][-SCENE_LOG_MEMORY:])}
        """

    user_prompt = f"""
        {state['player_state']['name']} fez:
        {player_action}

        Continue a simulação da cena.

        Se necessário, use ferramentas para atualizar o estado do mundo.
        """

    response = call_llm_with_tools(
        system_prompt,
        user_prompt,
        tools=WORLD_TOOLS_SCHEMA,
        turn_id=state["turn_number"]
    )

    # -------- SCENE LOG --------

    if turn:
        line = f"Jogador: {player_action}"
        state["scene_log"].append(line)
        append_story(state, line)

    state["scene_log"].append(response.content)
    append_story(state, response.content)

    print_npc("Simulação", response.content)
    log("Simulação", response.content)

    updates = {
        "last_llm_message": response.content
    }

    if response.tool_calls:
        updates["pending_tool_calls"] = response.tool_calls
    else:
        updates["pending_tool_calls"] = []

    return updates
