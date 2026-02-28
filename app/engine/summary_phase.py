from app.llm import call_llm
from app.ui.print_terminal import print_npc
from app.logging.state_logger import log
from app.config import DEBUG
from app.consts import SCENE_LOG_MEMORY

def summary_phase(state):

    if (len(state['scene_log']) >= SCENE_LOG_MEMORY):
        system_prompt = f"""
            Você é o narrador de um mundo Sandbox seu objetivo é resumir os principais acontecimentos até agora
            baseado em um log de eventos de modo que a história possa continuar a partir deste resumo.

            Destaque os principais acontecimentos em ordem cronológica.

            Não começe com "Resumo", apenas descreva os pontos.

            Não de sugestões sobre o que o jogador pode fazer em seguida.
            """

        user_prompt = f"""
            {state['scene_log']}
            """

        response = call_llm(system_prompt, user_prompt, "1")

        state["scene_log"] = []
        state["scene_log"].append(response)

        if (DEBUG):
            print(f"\nResumo até agora: {response}")

        log("NPCs", response)

    return state