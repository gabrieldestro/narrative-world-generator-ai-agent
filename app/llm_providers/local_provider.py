import time
import json
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

        usage = response.usage

        return LLMResponse(
            content=response.choices[0].message.content,
            tool_calls=None,
            prompt_tokens=getattr(usage, "prompt_tokens", None),
            completion_tokens=getattr(usage, "completion_tokens", None),
            total_tokens=getattr(usage, "total_tokens", None),
            latency=latency
        )


    def generate_with_tools(self, system_prompt, user_prompt, tools, turn_id):

        start = time.time()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            tools=tools,
            tool_choice="auto"
        )

        latency = time.time() - start
        message = response.choices[0].message

        tool_calls = None

        if message.tool_calls:
            tool_calls = []
            for call in message.tool_calls:
                tool_calls.append({
                    "id": call.id,
                    "name": call.function.name,
                    "arguments": json.loads(call.function.arguments)
                })

        usage = response.usage

        return LLMResponse(
            content=message.content or "",
            tool_calls=tool_calls,
            prompt_tokens=getattr(usage, "prompt_tokens", None),
            completion_tokens=getattr(usage, "completion_tokens", None),
            total_tokens=getattr(usage, "total_tokens", None),
            latency=latency
        )