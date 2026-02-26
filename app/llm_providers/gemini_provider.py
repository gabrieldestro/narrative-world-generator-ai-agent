import os
import time
from google import genai
from .base import BaseLLMProvider, LLMResponse


class GeminiProvider(BaseLLMProvider):

    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate(self, system_prompt, user_prompt, turn_id):

        start = time.time()

        response = self.model.generate_content(
            f"{system_prompt}\n\n{user_prompt}"
        )

        latency = time.time() - start

        return LLMResponse(
            content=response.text,
            prompt_tokens=None,
            completion_tokens=None,
            total_tokens=None,
            latency=latency
        )