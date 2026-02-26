from app.llm_providers.github_provider import GitHubProvider
from app.llm_providers.gemini_provider import GeminiProvider
from app.llm_providers.local_provider import LocalProvider


def get_llm_provider(provider_name: str):

    if provider_name == "github":
        return GitHubProvider()

    elif provider_name == "gemini":
        return GeminiProvider()

    elif provider_name == "local":
        return LocalProvider()

    else:
        raise ValueError(f"Unknown provider: {provider_name}")