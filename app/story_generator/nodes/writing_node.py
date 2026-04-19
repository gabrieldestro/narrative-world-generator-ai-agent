import json
from app.model.story_state import StoryState
from app.llm import call_llm

SYSTEM_PROMPT = """Você é um talento nato como autor de livros, conhecido por sua narrativa envolvente, descrições vívidas e diálogos realistas.
Sua tarefa agora é escrever O PRÓXIMO CAPÍTULO da história baseando-se nas informações do mundo, no resumo do que aconteceu até o momento, e na sinopse específica deste capítulo.

Diretrizes:
- Escreva a narrativa completa para o capítulo, com detalhes profundos, mantendo o tom e a imersão.
- Foque em qualidade literária, mostrando as ações em vez de apenas contar ("show, don't tell").
- Inclua o nome do capítulo no início como título.
- Não resuma, escreva a ação fluindo naturalmente.
"""

def writing_node(state: StoryState) -> StoryState:
    idx = state.get("current_chapter_index", 0)
    chapters = state.get("chapters_plan", [])
    
    if idx >= len(chapters):
        return state
        
    current_chapter = chapters[idx]
    
    print(f"\n--- ESCREVENDO: {current_chapter['title']} ---")
    
    world_info = json.dumps(state.get("world", {}), indent=2, ensure_ascii=False)
    summary = state.get("story_summary", "(Nenhum evento anterior. Este é o começo da história.)")
    synopsis = current_chapter.get("synopsis", "")
    title = current_chapter.get("title", "")
    
    user_prompt = f"Informações do Mundo:\n{world_info}\n\n"
    user_prompt += f"Resumo do que já aconteceu até antes deste capítulo:\n{summary}\n\n"
    user_prompt += f"Agora, escreva a narrativa DESTE capítulo:\nTítulo: {title}\nSinopse: {synopsis}\n"

    turn_id = f"{state.get('simulation_id')}_write_{idx}"
    
    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        turn_id=turn_id
    )
    
    # Save the written text
    if "written_chapters" not in state:
        state["written_chapters"] = []
        
    state["written_chapters"].append(response)
    
    print(f"Capítulo {idx+1} concluído.")
    
    return state
