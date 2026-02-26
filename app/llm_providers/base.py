from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    content: str
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    latency: float


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, turn_id: str) -> LLMResponse:
        pass