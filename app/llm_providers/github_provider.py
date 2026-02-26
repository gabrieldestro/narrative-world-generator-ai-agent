import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from .base import BaseLLMProvider, LLMResponse
from config import GITHUB_TOKEN, MODEL_NAME, BASE_URL

load_dotenv()

class GitHubProvider(BaseLLMProvider):

    def __init__(self):
        self.client = OpenAI(
            base_url=BASE_URL,
            api_key=GITHUB_TOKEN
        )
        self.model = MODEL_NAME

    def generate(self, system_prompt, user_prompt, turn_id):

        start = time.time()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
        )

        latency = time.time() - start

        usage = response.usage

        return LLMResponse(
            content=response.choices[0].message.content,
            prompt_tokens=usage.prompt_tokens if usage else None,
            completion_tokens=usage.completion_tokens if usage else None,
            total_tokens=usage.total_tokens if usage else None,
            latency=latency
        )