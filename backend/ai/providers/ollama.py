from typing import Dict, List
import ollama

from backend.ai.providers.base import BaseProvider


class OllamaProvider(BaseProvider):

    def __init__(self):

        self.model = "phi3"

    def generate_response(
        self,
        messages: List[Dict[str, str]]
    ) -> str:

        ollama_messages = []

        for message in messages:

            role = (
                "assistant"
                if message["role"] == "assistant"
                else "user"
            )

            ollama_messages.append(
                {
                    "role": role,
                    "content": message["content"]
                }
            )

        response = ollama.chat(
            model=self.model,
            messages=ollama_messages
        )

        return response["message"]["content"]