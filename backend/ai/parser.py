"""
Universal AI Parser for Jarvis AI.

Converts natural language into a Task object.
"""

import json
import re

import ollama

from backend.ai.prompts import PARSER_PROMPT
from backend.config.logger import logger
from backend.config.settings import settings
from backend.core.task import Task


class AIParser:

    def __init__(self):

        self.model = settings.OLLAMA_MODEL

    def parse(self, message: str) -> Task:
        """
        Convert a natural language request into a Task.
        """

        prompt = PARSER_PROMPT.replace(
            "<<MESSAGE>>",
            message
        )

        try:

            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            text = response["message"]["content"]

            logger.info(f"Raw Parser Output:\n{text}")

            match = re.search(
                r"\{.*\}",
                text,
                re.DOTALL
            )

            if not match:
                raise ValueError(
                    "No JSON object found in model response."
                )

            json_text = match.group(0)

            logger.info(
                f"Extracted JSON:\n{json_text}"
            )

            data = json.loads(json_text)

            task = Task(
                tool=data.get("tool", "chat"),
                action=data.get("action", "reply"),
                parameters=data.get("parameters", {})
            )

            logger.info(
                f"Parsed Task: {task}"
            )

            return task

        except Exception as e:

            logger.exception(
                f"Parser Error: {e}"
            )

            return Task(
                tool="chat",
                action="reply",
                parameters={
                    "message": "Sorry, I couldn't understand the request."
                }
            )


parser = AIParser()