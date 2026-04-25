import json
from app.model.story_state import StoryState
from app.llm import call_llm
from app.config import AUTO_PLAY, STORY_CHAPTER_PARTS

SYSTEM_PROMPT = """Você é um talento nato como autor de livros, conhecido por sua narrativa envolvente, descrições vívidas e diálogos realistas.
Sua tarefa agora é escrever a narrativa da história baseando-se nas informações do mundo, no resumo do que aconteceu até o momento, e na sinopse específica deste capítulo.

Diretrizes:
- Escreva a narrativa com detalhes profundos, mantendo o tom e a imersão.
- Foque em qualidade literária, mostrando as ações em vez de apenas contar ("show, don't tell").
- Não resuma os diálogos, escreva-os integralmente.
- Adapte-se ao contexto passado a você, conectando ideias.
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
    
    base_prompt = f"Informações do Mundo:\n{world_info}\n\n"
    base_prompt += f"Resumo do que já aconteceu até antes deste capítulo:\n{summary}\n\n"
    base_prompt += f"MUITO IMPORTANTE: Você está redigindo O SEGUINTE CAPÍTULO:\nTítulo: {title}\nSinopse Geral do Capítulo: {synopsis}\n\n"

    turn_id = f"{state.get('simulation_id')}_write_{idx}"
    
    accumulated_feedback = ""
    attempt = 1
    
    while True:
        chapter_content = f"# {title}\n\n"
        
        for part in range(1, STORY_CHAPTER_PARTS + 1):
            print(f"Gerando parte {part} de {STORY_CHAPTER_PARTS} para o capítulo {idx+1}...")
            
            user_prompt = base_prompt
            if accumulated_feedback:
                user_prompt += f"Atenção, o usuário reprovou gerações anteriores. Aplique esse feedback rigorosamente no seu texto agora:\n{accumulated_feedback}\n\n"
                
            if STORY_CHAPTER_PARTS == 1:
                 # Se estiver configurado para gerar tudo de uma vez
                 user_prompt += "Instrução: Por favor, escreva a narrativa COMPLETA deste capítulo de uma só vez, baseando-se na sinopse."
            elif part == 1:
                user_prompt += f"Instrução: Por favor, escreva APENAS a PARTE 1 (o início) das {STORY_CHAPTER_PARTS} partes deste capítulo.\n"
                user_prompt += "Introduza os elementos, construa a atmosfera e inicie as ações descritas na sinopse. NÃO finalize o capítulo ainda."
            elif part == STORY_CHAPTER_PARTS:
                user_prompt += f"O capítulo já foi parcialmente escrito. Aqui está o texto redigido até o momento:\n\n---\n{chapter_content}\n---\n\n"
                user_prompt += f"Instrução: Por favor, escreva a ÚLTIMA PARTE (parte {part} de {STORY_CHAPTER_PARTS}) deste capítulo.\n"
                user_prompt += "Continue EXATAMENTE de onde o texto anterior parou, garantindo uma conexão fluida e que faça sentido imediato sem repeti-lo. Conclua os eventos da sinopse e forneça um encerramento adequado para este capítulo."
            else:
                user_prompt += f"O capítulo já foi parcialmente escrito. Aqui está o texto redigido até o momento:\n\n---\n{chapter_content}\n---\n\n"
                user_prompt += f"Instrução: Por favor, escreva APENAS O MEIO (parte {part} de {STORY_CHAPTER_PARTS}) deste capítulo.\n"
                user_prompt += "Continue EXATAMENTE de onde o texto anterior parou, garantindo conexão fluida sem repeti-lo. Desenvolva as ações da sinopse da melhor maneira. NÃO finalize o capítulo ainda."
                
            part_response = call_llm(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt,
                turn_id=f"{turn_id}_try_{attempt}_p{part}"
            )
            
            # A LLM pode as vezes injetar um título markdown, é bom limparmos se estiver repitindo, mas por ora concatena:
            chapter_content += part_response.strip() + "\n\n"

        if AUTO_PLAY:
            break
            
        print("\n=== REVISÃO DE CAPÍTULO CONCLUÍDO ===")
        print(chapter_content)
        print("======================================\n")
        print("Pressione [ENTER] para aprovar, ou digite um feedback e o capítulo será REESCRITO do zero em partes:")
        feedback = input("> ").strip()
        
        if not feedback:
            break
            
        print("\nSeu feedback foi anotado. O assistente reescreverá o capítulo novamente acatando as mudanças.")
        accumulated_feedback += f"- {feedback}\n"
        attempt += 1

    if "written_chapters" not in state:
        state["written_chapters"] = []
        
    state["written_chapters"].append(chapter_content)
    
    print(f"Capítulo {idx+1} concluído.")
    
    return state
