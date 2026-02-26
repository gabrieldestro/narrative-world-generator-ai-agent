import time
from openai import OpenAI
from app.llm_providers.base import BaseLLMProvider, LLMResponse


class LocalProvider(BaseLLMProvider):

    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:1234/v1",
            api_key="not-needed"
        )
        self.model = "local-model"

    def generate(self, system_prompt, user_prompt, turn_id):

        start = time.time()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )

        latency = time.time() - start

        return LLMResponse(
            content=response.choices[0].message.content,
            prompt_tokens=None,
            completion_tokens=None,
            total_tokens=None,
            latency=latency
        )