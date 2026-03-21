from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class LLMResponse:
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    latency: float = 0.0


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, turn_id: str) -> LLMResponse:
        pass

    @abstractmethod
    def generate_with_tools(self, system_prompt, user_prompt, tools, turn_id) -> LLMResponse:
        pass