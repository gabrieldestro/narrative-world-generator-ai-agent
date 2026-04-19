import json
from app.model.story_state import StoryState
from app.llm import call_llm

SYSTEM_PROMPT = """Você é um especialista em planejamento narrativo e estruturação de roteiros.
Seu objetivo é analisar as definições do mundo fornecidas e criar um outline (esqueleto) para uma história completa com Começo, Meio e Fim.
Não escreva a história ainda. Defina:
- O Título provisório da história.
- O Conflito Principal.
- O Resumo dos grandes eventos, do incidente incitante ao clímax e conclusão.

Retorne em formato puramente textual e descritivo.
"""

def planning_node(state: StoryState) -> StoryState:
    print("\n--- INICIANDO PLANEJAMENTO DA HISTÓRIA ---")
    
    world_info = json.dumps(state.get("world", {}), indent=2, ensure_ascii=False)
    additional_info = state.get("additional_info", "")
    
    user_prompt = f"Informações do Mundo:\n{world_info}\n\n"
    if additional_info:
        user_prompt += f"Diretrizes Adicionais do Usuário:\n{additional_info}\n\n"
        
    user_prompt += "Crie o planejamento (outline) detalhado da narrativa baseando-se nestas informações."

    turn_id = f"{state['simulation_id']}_planning"
    
    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        turn_id=turn_id
    )
    
    # Tentaremos extrair um "título", mas como não é JSON restrito, vamos assumir o texto inteiro no outline
    # Em um node de afilamento ou no split chapters podemos tentar capturar.
    state["story_outline"] = response
    
    print("Planejamento concluído!")
    return state
