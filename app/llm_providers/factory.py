from .github_provider import GitHubProvider
from .gemini_provider import GeminiProvider
from .local_provider import LocalProvider


def get_llm_provider(provider_name: str):

    if provider_name == "github":
        return GitHubProvider()

    elif provider_name == "gemini":
        return GeminiProvider()

    elif provider_name == "local":
        return LocalProvider()

    else:
        raise ValueError(f"Unknown provider: {provider_name}")