from app.llm import call_llm
from app.ui.print_terminal import print_npc
from app.logging.state_logger import log
from app.config import DEBUG
from app.consts import SCENE_LOG_MEMORY

def summary_phase(state):
    messages = state.get('messages', [])
    if len(messages) >= SCENE_LOG_MEMORY:
        # Pega as mensagens antigas para resumir (deixa as 2 últimas intactas para manter o contexto imediato)
        messages_to_summarize = messages[:-2]
        history = ""
        for msg in messages_to_summarize:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            history += f"{role}: {content}\n"

        system_prompt = f"""
            Você é o narrador de um mundo Sandbox seu objetivo é resumir os principais acontecimentos
            baseado neste log de conversa de modo que a história possa continuar a partir deste resumo.

            Destaque os principais acontecimentos de forma concisa.
            Não comece com "Resumo", apenas descreva os pontos.
            Não dê sugestões sobre o que o jogador pode fazer em seguida.
            """

        # Como a chamada llm precisará de 'messages', passamos como uma interação user para o resumo
        user_msg = [{"role": "user", "content": history}]
        response = call_llm(system_prompt, user_msg, "summary")

        # Mantemos o sumário como o contexto inicial e as 2 últimas interações completas
        new_messages = [{"role": "system", "content": f"Resumo do que aconteceu antes:\n{response}"}]
        new_messages.extend(messages[-2:])
        
        state["messages"] = new_messages

        if DEBUG:
            print(f"\nResumo criado: {response}")

        log("System", f"Resumo criado: {response}")

    return state