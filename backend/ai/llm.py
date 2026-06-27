"""
LLM interface for Jarvis AI.

Responsible only for communicating with the language model.
"""

from google import genai
from google.genai import types

from backend.config.settings import settings
from backend.config.logger import logger
from backend.ai.prompts import SYSTEM_PROMPT


class LLM:

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.MODEL_NAME

    def generate_response(self, user_message: str) -> str:
        """
        Generate a response from Gemini.
        """

        try:

            response = self.client.models.generate_content(
                model=self.model,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                ),
                contents=user_message,
            )

            logger.info("LLM response generated successfully.")

            return response.text

        except Exception as e:

            logger.error(f"LLM Error: {e}")

            return "Sorry, I couldn't process your request."


llm = LLM()