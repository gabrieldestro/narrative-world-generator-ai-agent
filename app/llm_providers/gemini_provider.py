import os
import time
from google import genai
from app.llm_providers.base import BaseLLMProvider, LLMResponse

class GeminiProvider(BaseLLMProvider):

    def __init__(self):
        genai.configure(api_key="YOUR_GEMINI_KEY")
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def generate(self, system_prompt, messages, turn_id, stream_callback=None):

        start = time.time()
        
        prompt = system_prompt + "\n\n"
        for msg in messages:
            prompt += f"{msg.get('role', 'user')}: {msg.get('content', '')}\n"

        response = self.model.generate_content(
            prompt,
            stream=bool(stream_callback)
        )
        
        full_content = ""
        if stream_callback:
            for chunk in response:
                if chunk.text:
                    full_content += chunk.text
                    stream_callback(chunk.text)
        else:
            full_content = response.text

        latency = time.time() - start

        return LLMResponse(
            content=full_content,
            tool_calls=None,
            prompt_tokens=None,
            completion_tokens=None,
            total_tokens=None,
            latency=latency
        )

    def generate_with_tools(self, system_prompt, messages, tools, turn_id, stream_callback=None):

        start = time.time()
        
        prompt = system_prompt + "\n\n"
        for msg in messages:
            prompt += f"{msg.get('role', 'user')}: {msg.get('content', '')}\n"

        # Note: Gemini may have limitations with stream=True + tools, but we'll attempt it
        response = self.model.generate_content(
            prompt,
            tools=tools,
            stream=bool(stream_callback)
        )
        
        full_content = ""
        tool_calls = None
        
        if stream_callback:
            for chunk in response:
                # Accumulate text
                if hasattr(chunk, "text") and chunk.text:
                    full_content += chunk.text
                    stream_callback(chunk.text)
                
                # In streaming, tools calls are usually in the final chunk for Gemini
                if hasattr(chunk, "candidates"):
                    for candidate in chunk.candidates:
                        if candidate.content.parts:
                            for part in candidate.content.parts:
                                if hasattr(part, "function_call"):
                                    tool_calls = [{
                                        "id": "gemini-call",
                                        "name": part.function_call.name,
                                        "arguments": dict(part.function_call.args)
                                    }]
        else:
            full_content = response.text if hasattr(response, "text") else ""
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

        latency = time.time() - start

        return LLMResponse(
            content=full_content,
            tool_calls=tool_calls,
            prompt_tokens=None,
            completion_tokens=None,
            total_tokens=None,
            latency=latency
        )