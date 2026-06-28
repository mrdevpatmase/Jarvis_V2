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

            prompt_lines = []

            for message in messages:

                role = "User" if message["role"] == "user" else "Jarvis"

                prompt_lines.append(
                    f"{role}: {message['content']}"
                )

            prompt = "\n".join(prompt_lines)

            response = self.client.models.generate_content(
                model=self.model,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                ),
                contents=prompt,
            )

            logger.info("LLM response generated successfully.")

            logger.info(f"Gemini Response: {response}")
            logger.info(f"Gemini Text: {response.text}")


            text = response.text

            if not text:
                logger.error("Gemini returned an empty response.")
                return "I'm sorry, I couldn't generate a response."

            return text

        except Exception as e:

            logger.error(f"LLM Error: {e}")

            return "Sorry, I couldn't process your request."


llm = LLM()