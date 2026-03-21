from app.llm_providers.openai_provider import OpenAiProvider
from app.llm_providers.gemini_provider import GeminiProvider
from app.llm_providers.local_provider import LocalProvider


def get_llm_provider(provider_name: str):

    if provider_name == "openai":
        return OpenAiProvider()

    elif provider_name == "gemini":
        return GeminiProvider()

    elif provider_name == "local":
        return LocalProvider()

    else:
        raise ValueError(f"Unknown provider: {provider_name}")