import json
import re
from app.model.story_state import StoryState
from app.llm import call_llm
from app.config import AUTO_PLAY

SYSTEM_PROMPT = """Você é um estruturador de capítulos.
Dado o outline de uma história e as informações do mundo, sua tarefa é dividir a narrativa em uma lista estruturada de capítulos.
Cada capítulo deve ter um título e uma sinopse detalhada do que acontecerá nele.

Você deve retornar APENAS um JSON válido no formato de lista de dicionários, sem blocos de markdown ou texto adicional. Exemplo:
[
    {
        "title": "Capítulo 1: O Despertar",
        "synopsis": "O protagonista acorda e descobre sobre seus poderes."
    },
    {
        "title": "Capítulo 2: A Jornada",
        "synopsis": "Ele sai de casa em direção à capital."
    }
]
"""

def extract_json(text: str):
    # Tenta achar um array JSON via regex se houver markdown
    match = re.search(r'\[\s*\{.*?\}\s*\]', text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    # Fallback
    return json.loads(text)

def chapter_split_node(state: StoryState) -> StoryState:
    print("\n--- DIVIDINDO EM CAPÍTULOS ---")
    
    story_outline = state.get("story_outline", "")
    additional_info = state.get("additional_info", "")
    
    base_user_prompt = f"Outline da História:\n{story_outline}\n\n"
    
    if additional_info:
        base_user_prompt += f"Considere estas diretrizes do usuário ao decidir a quantidade de capítulos:\n{additional_info}\n\n"
        
    base_user_prompt += "Retorne o JSON listando os capítulos."

    turn_id = f"{state.get('simulation_id')}_split"
    
    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=base_user_prompt,
        turn_id=turn_id
    )
    
    if not AUTO_PLAY:
        attempt = 1
        while True:
            try:
                parsed_chapters = extract_json(response)
                formatted_response = json.dumps(parsed_chapters, indent=2, ensure_ascii=False)
            except Exception:
                formatted_response = response + "\n[Aviso: O texto gerado não é um JSON válido. Requer regeração.]"

            print("\n=== REVISÃO DE CAPÍTULOS ===")
            print(formatted_response)
            print("============================\n")
            print("Pressione [ENTER] para aprovar, ou digite um feedback para o assistente refazer a divisão:")
            feedback = input("> ").strip()
            
            if not feedback:
                break
                
            print("\nRegerando com feedback...")
            attempt += 1
            user_prompt_feedback = f"{base_user_prompt}\n\nAtenção, o usuário repassou o seguinte feedback sobre a sua primeira sugestão:\n{feedback}\nPor favor, retorne o JSON novamente aplicando as mudanças."
            
            response = call_llm(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt_feedback,
                turn_id=f"{turn_id}_retry_{attempt}"
            )
    
    try:
        chapters = extract_json(response)
        state["chapters_plan"] = chapters
        state["current_chapter_index"] = 0
        state["story_title"] = "História Gerada" # Será sobrescrita se tivermos o titulo
        state["story_summary"] = ""
        state["written_chapters"] = []
        
        print(f"Dividido em {len(chapters)} capítulos.")
    except Exception as e:
        print(f"Erro ao processar o JSON dos capítulos: {e}")
        # dummy fallback
        state["chapters_plan"] = [{"title": "Capítulo Único", "synopsis": story_outline}]
        state["current_chapter_index"] = 0
        state["story_summary"] = ""
        state["written_chapters"] = []
        
    return state
