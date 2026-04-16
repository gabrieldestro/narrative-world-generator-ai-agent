import json

from app.llm import call_llm
from app.consts import SCENE_LOG_MEMORY


def auto_play_phase(state):
    last_events = "\n".join(state["scene_log"][-SCENE_LOG_MEMORY:])
    player = state["player_state"]

    system_prompt = _get_auto_play_system_prompt(state)

    user_prompt = f"""
    Últimos eventos da história:
    {last_events}

    Gere a próxima ação do jogador que esteja de acordo com a história e o seu objetivo.
    
    Objetivo: {player['objective']}
    """

    response = call_llm(system_prompt, user_prompt, state["turn_number"])

    turn_state = _parse_turn_response(response)

    state["turn_state"] = turn_state

    return state

def _get_auto_play_system_prompt(state):
    player = state["player_state"]

    # aqui talvez seja interessante converter o input de resposta para um json estruturado
    return f"""
    Você controla o personagem do jogador em um RPG narrativo.

    Gere a próxima ação do jogador de forma curta e objetiva.

    Regras:
    - Não narre consequências
    - Não escreva como narrador
    - Apenas descreva a ação do jogador
    - Seja consistente com a personalidade do personagem
    - Leve em conta o contexto atual da história

    Formato de resposta (JSON válido):
    {{
        "player_choice_type": "action | dialogue",
        "player_content": "ação ou fala do jogador",
        "target_npc_id": "id ou null"
    }}
    
    Personagem:
    Nome: {player['name']}
    Descrição: {player['description']}
    """

def _parse_turn_response(response: str):
    try:
        data = json.loads(response)

        return {
            "player_choice_type": data.get("player_choice_type", "action"),
            "player_content": data.get("player_content", "").strip(),
            "target_npc_id": data.get("target_npc_id"),
        }

    except Exception:
        return {
            "player_choice_type": "action",
            "player_content": response.strip(),
            "target_npc_id": None,
        }