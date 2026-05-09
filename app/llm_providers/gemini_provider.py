import os
import time
from google import genai
from app.llm_providers.base import BaseLLMProvider, LLMResponse

class GeminiProvider(BaseLLMProvider):

    def __init__(self):
        genai.configure(api_key="YOUR_GEMINI_KEY")
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def generate(self, system_prompt, messages, turn_id):

        start = time.time()
        
        prompt = system_prompt + "\n\n"
        for msg in messages:
            prompt += f"{msg.get('role', 'user')}: {msg.get('content', '')}\n"

        response = self.model.generate_content(
            prompt
        )

        latency = time.time() - start

        return LLMResponse(
            content=response.text,
            tool_calls=None,
            prompt_tokens=None,
            completion_tokens=None,
            total_tokens=None,
            latency=latency
        )

    def generate_with_tools(self, system_prompt, messages, tools, turn_id):

        start = time.time()
        
        prompt = system_prompt + "\n\n"
        for msg in messages:
            prompt += f"{msg.get('role', 'user')}: {msg.get('content', '')}\n"

        response = self.model.generate_content(
            prompt,
            tools=tools
        )

        latency = time.time() - start

        tool_calls = None

        # Gemini retorna function_calls em outro formato
        if hasattr(response, "candidates"):
            for candidate in response.candidates:
                if candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, "function_call"):
                            tool_calls = [{
                                "id": "gemini-call",
                                "name": part.function_call.name,
                                "arguments": dict(part.function_call.args)
                            }]

        return LLMResponse(
            content=response.text if hasattr(response, "text") else "",
            tool_calls=tool_calls,
            prompt_tokens=None,
            completion_tokens=None,
            total_tokens=None,
            latency=latency
        )