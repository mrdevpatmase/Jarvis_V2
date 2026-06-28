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

        message = user_message.lower().strip()

        # ---------- Memory ----------
        if "my name is" in message:
            return "memory"

        if "what is my name" in message:
            return "memory"

        if "remember" in message:
            return "memory"

        # ---------- Browser ----------
        if any(word in message for word in [
            "open chrome",
            "open youtube",
            "open google",
            "open github",
            "open browser",
            "search"
        ]):
            return "browser"

        # ---------- Files ----------
        if any(word in message for word in [
            "create file",
            "create folder",
            "delete file",
            "rename file",
            "move file"
        ]):
            return "files"

        # ---------- System ----------
        if any(word in message for word in [
            "shutdown",
            "restart",
            "sleep",
            "lock",
            "volume"
        ]):
            return "system"

        # ---------- Coding ----------
        if any(word in message for word in [
            "write code",
            "python",
            "c++",
            "javascript",
            "bug",
            "leetcode"
        ]):
            return "coding"

        # ---------- Fallback to Gemini ----------
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
                return "chat"

            logger.info(f"Router selected by Gemini: {tool}")

            return tool

        except Exception as e:

            logger.warning(f"Gemini router unavailable: {e}")

            return "chat"


router = Router()