"""
Persistent Memory Tool for Jarvis AI.
"""

import json
import re
from pathlib import Path

from backend.tools.base_tool import BaseTool
from backend.config.logger import logger


class MemoryTool(BaseTool):

    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parent.parent

        self.memory_file = BASE_DIR / "data" / "memory.json"

        self.memory = self.load_memory()

    def load_memory(self):

        try:

            if not self.memory_file.exists():

                logger.info("memory.json not found. Creating new memory.")

                return {}

            with open(self.memory_file, "r", encoding="utf-8") as file:

                data = json.load(file)

                logger.info(f"Loaded memory: {data}")

                return data

        except Exception as e:

            logger.exception(f"Memory Load Error: {e}")

            return {}

    def save_memory(self):

        try:

            self.memory_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.memory_file, "w", encoding="utf-8") as file:

                json.dump(
                    self.memory,
                    file,
                    indent=4
                )

            logger.info(f"Memory saved successfully: {self.memory}")

        except Exception as e:

            logger.exception(f"Memory Save Error: {e}")

    def execute(self, task):

        action = task.action

        if action == "store":

            key = task.parameters.get("key")
            value = task.parameters.get("value")

            self.memory[key] = value

            self.save_memory()

            logger.info(f"Stored {key}: {value}")

            return f"I'll remember your {key}."

        elif action == "retrieve":

            key = task.parameters.get("key")

            value = self.memory.get(key)

            if value is None:
                return f"I don't know your {key} yet."

            return f"Your {key} is {value}."

        elif action == "delete":

            key = task.parameters.get("key")

            if key in self.memory:

                del self.memory[key]

                self.save_memory()

                return f"I forgot your {key}."

            return f"I don't know your {key}."

        return "Unknown memory action."


memory_tool = MemoryTool()