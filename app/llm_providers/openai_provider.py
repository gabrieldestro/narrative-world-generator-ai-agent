# app/llm_providers/github_provider.py

import time
import json
from openai import OpenAI
from app.config import *
from app.llm_providers.base import BaseLLMProvider, LLMResponse


class OpenAiProvider(BaseLLMProvider):

    def __init__(self):
        self.client = OpenAI(
            base_url=BASE_URL,
            api_key=API_TOKEN
        )
        self.model = MODEL_NAME

    def generate(self, system_prompt, messages, turn_id, stream_callback=None):

        start = time.time()
        
        api_messages = [{"role": "system", "content": system_prompt}]
        api_messages.extend(messages)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=api_messages,
            temperature=TEMPERATURE,
            stream=bool(stream_callback)
        )
        
        full_content = ""
        usage = None
        
        if stream_callback:
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content_piece = chunk.choices[0].delta.content
                    full_content += content_piece
                    stream_callback(content_piece)
        else:
            full_content = response.choices[0].message.content
            usage = response.usage

        latency = time.time() - start
        usage = response.usage

        return LLMResponse(
            content=full_content,
            tool_calls=None,
            prompt_tokens=getattr(usage, "prompt_tokens", None) if usage else None,
            completion_tokens=getattr(usage, "completion_tokens", None) if usage else None,
            total_tokens=getattr(usage, "total_tokens", None) if usage else None,
            latency=latency
        )


    def generate_with_tools(self, system_prompt, messages, tools, turn_id, stream_callback=None):

        start = time.time()
        
        api_messages = [{"role": "system", "content": system_prompt}]
        api_messages.extend(messages)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=api_messages,
            tools=tools,
            tool_choice="auto",
            stream=bool(stream_callback)
        )

        full_content = ""
        tool_calls = None
        usage = None

        if stream_callback:
            tool_calls_dict = {}
            for chunk in response:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta
                if delta.content:
                    content_piece = delta.content
                    full_content += content_piece
                    stream_callback(content_piece)
                if delta.tool_calls:
                    for tc in delta.tool_calls:
                        if tc.index not in tool_calls_dict:
                            tool_calls_dict[tc.index] = {"id": tc.id, "name": tc.function.name, "arguments": ""}
                        if tc.function.arguments:
                            tool_calls_dict[tc.index]["arguments"] += tc.function.arguments
                            
            if tool_calls_dict:
                tool_calls = []
                for idx, tc in tool_calls_dict.items():
                    tool_calls.append({
                        "id": tc["id"],
                        "name": tc["name"],
                        "arguments": json.loads(tc["arguments"])
                    })
        else:
            message = response.choices[0].message
            full_content = message.content or ""
            if message.tool_calls:
                tool_calls = []
                for call in message.tool_calls:
                    tool_calls.append({
                        "id": call.id,
                        "name": call.function.name,
                        "arguments": json.loads(call.function.arguments)
                    })
            usage = response.usage

        latency = time.time() - start

        return LLMResponse(
            content=full_content,
            tool_calls=tool_calls,
            prompt_tokens=getattr(usage, "prompt_tokens", None) if usage else None,
            completion_tokens=getattr(usage, "completion_tokens", None) if usage else None,
            total_tokens=getattr(usage, "total_tokens", None) if usage else None,
            latency=latency
        )