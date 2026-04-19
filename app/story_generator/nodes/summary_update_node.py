from app.model.story_state import StoryState
from app.llm import call_llm
from app.repository.story_generation_repository import save_story_generation

SYSTEM_PROMPT = """Você é um assistente de resumo narrativo de alta precisão.
Sua tarefa é ler um resumo anterior da história (se existir) e o texto do capítulo mais recente, e produzir um novo resumo consolidado da história até o momento.
Esse resumo servirá de memória para a geração dos próximos capítulos, então:
- Preserve o essencial da trama, decisões de personagens, mortes ou conquistas.
- Seja objetivo mas mantenha a continuidade lógica (causa e efeito).
- Mantenha o texto resultante relativamente curto (1 a 3 parágrafos).
"""

def summary_update_node(state: StoryState) -> StoryState:
    idx = state.get("current_chapter_index", 0)
    written = state.get("written_chapters", [])
    
    if not written or idx >= len(written):
        return state
        
    print("\n--- ATUALIZANDO RESUMO DA HISTÓRIA ---")
        
    last_chapter_text = written[-1]
    old_summary = state.get("story_summary", "")
    
    user_prompt = f"Resumo Antigo:\n{old_summary}\n\n" if old_summary else "Resumo Antigo: (Início da história)\n\n"
    user_prompt += f"Texto do Capítulo {idx+1}:\n{last_chapter_text}\n\n"
    user_prompt += "Gere o novo resumo atualizado de tudo o que aconteceu até agora."

    turn_id = f"{state.get('simulation_id')}_summary_{idx}"
    
    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        turn_id=turn_id
    )
    
    state["story_summary"] = response
    
    # Incrementa o index para o próximo capítulo
    state["current_chapter_index"] += 1
    
    # Checkpoint (salvamento automático a cada capítulo)
    save_story_generation(state)
    
    return state
