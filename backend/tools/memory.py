"""
Memory Tool for Jarvis AI.

Stores and retrieves user information.
"""

import re

from backend.tools.base_tool import BaseTool
from backend.config.logger import logger


class MemoryTool(BaseTool):

    def __init__(self):
        self.memory = {}

    def execute(self, user_message: str):

        message = user_message.lower().strip()

        # Store user's name
        if "my name is" in message:

            match = re.search(r"my name is (.+)", message)

            if match:

                name = match.group(1).strip().title()

                self.memory["name"] = name

                logger.info(f"Stored name: {name}")

                return f"Nice to meet you, {name}. I'll remember your name."

        # Retrieve user's name
        if "what is my name" in message:

            name = self.memory.get("name")

            if name:

                return f"Your name is {name}."

            return "I don't know your name yet."

        return "Memory tool couldn't understand the request."


memory_tool = MemoryTool()