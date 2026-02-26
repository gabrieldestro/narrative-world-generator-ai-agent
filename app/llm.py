import os
from pydoc import text
import time
from dotenv import load_dotenv
from engine.ui import stream_panel
from openai import OpenAI
from llm_providers.factory import get_llm_provider
from config import MODEL_NAME, BASE_URL, PROVIDER_NAME
from logging_config import llm_logger
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

'''
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN não encontrado nas variáveis de ambiente")

client = OpenAI(
    base_url=BASE_URL,
    api_key=GITHUB_TOKEN,
)

def call_llm(system_prompt: str, user_prompt: str) -> str:

    start_time = time.time()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.8,
    )

    latency = time.time() - start_time

    content = response.choices[0].message.content

    # Token usage (GitHub models também retornam usage)
    usage = response.usage

    llm_logger.info(
        "LLM Call",
        extra={
            "extra_data": {
                "turn_id": 1,
                "model": MODEL_NAME,
                "latency_seconds": round(latency, 4),
                "prompt_tokens": usage.prompt_tokens if usage else None,
                "completion_tokens": usage.completion_tokens if usage else None,
                "total_tokens": usage.total_tokens if usage else None,
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "response": content,
            }
        }
    )

    return content
'''