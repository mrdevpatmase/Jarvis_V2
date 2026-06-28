"""
Router for Jarvis AI.

Uses the LLM to determine which tool should handle a request.
"""

from google import genai
from google.genai import types

from backend.ai.prompts import ROUTER_PROMPT
from backend.config.logger import logger
from backend.config.settings import settings


class Router:

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.MODEL_NAME

        self.valid_tools = {
            "browser",
            "system",
            "files",
            "memory",
            "coding",
            "chat",
        }

    def route(self, user_message: str) -> str:
        """
        Decide which tool should handle the request.
        """

        try:

            response = self.client.models.generate_content(
                model=self.model,
                config=types.GenerateContentConfig(
                    system_instruction=ROUTER_PROMPT
                ),
                contents=user_message,
            )

            tool = response.text.strip().lower()

            if tool not in self.valid_tools:

                logger.warning(
                    f"Unknown tool '{tool}', using chat."
                )

                return "chat"

            logger.info(
                f"Router selected: {tool}"
            )

            return tool

        except Exception as e:

            logger.error(f"Router Error: {e}")

            return "chat"


router = Router()