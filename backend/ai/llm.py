"""
LLM interface for Jarvis AI.

Responsible only for communicating with the language model.
"""

from google import genai
from google.genai import types

from backend.config.settings import settings
from backend.config.logger import logger
from backend.ai.prompts import SYSTEM_PROMPT
from typing import List, Dict


class LLM:

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.MODEL_NAME

    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a response using the conversation history.
        """

        try:

            prompt = ""

            for message in messages:

                if message["role"] == "user":
                    prompt += f"User: {message['content']}\n"

                else:
                    prompt += f"Jarvis: {message['content']}\n"

            response = self.client.models.generate_content(
                model=self.model,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                ),
                contents=prompt,
            )

            logger.info("LLM response generated successfully.")

            return response.text

        except Exception as e:

            logger.error(f"LLM Error: {e}")

            return "Sorry, I couldn't process your request."


llm = LLM()