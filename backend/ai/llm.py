from backend.config.settings import settings

from backend.ai.providers.gemini import GeminiProvider
from backend.ai.providers.ollama import OllamaProvider


class LLM:

    def __init__(self):

        if settings.LLM_PROVIDER.lower() == "ollama":
            self.provider = OllamaProvider()

        else:
            self.provider = GeminiProvider()

    def generate_response(self, messages):

        return self.provider.generate_response(messages)


llm = LLM()