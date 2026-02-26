import os
from pydoc import text
import time
from dotenv import load_dotenv
from openai import OpenAI
from app.logging_config import llm_logger
from app.engine.ui import stream_panel
from app.llm_providers.factory import get_llm_provider
from app.config import MODEL_NAME, BASE_URL, PROVIDER_NAME
import json

def call_llm(
    system_prompt: str,
    user_prompt: str,
    turn_id: str
):
    provider = get_llm_provider(PROVIDER_NAME)

    stream_panel("Sistema", "Processando. Aguarde ...", "magenta")
    response = provider.generate(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        turn_id=turn_id
    )

    # 🔥 Log estruturado
    llm_logger.info(
        "LLM Call",
        extra={
            "extra_data": {
                "turn_id": turn_id,
                "provider": PROVIDER_NAME,
                "model_class": provider.__class__.__name__,
                "latency_seconds": round(response.latency, 4),
                "prompt_tokens": response.prompt_tokens,
                "completion_tokens": response.completion_tokens,
                "total_tokens": response.total_tokens,
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "response": response.content,
            }
        }
    )

    return response.content