"""
Context Manager for Jarvis AI.

Responsible for preparing the context that will be sent to the LLM.
Currently it uses only the active conversation history.

Future versions will also include:
- Long-term memory
- Active tasks
- User preferences
- System state
"""

from typing import Dict, List

from backend.ai.conversation import conversation
from backend.config.logger import logger


class ContextManager:
    """
    Builds the context used by the LLM.
    """

    def build_context(self) -> List[Dict[str, str]]:
        """
        Build the complete context for the LLM.

        Returns:
            List of conversation messages.
        """

        history = conversation.get_history()

        logger.info(
            f"Context built with {len(history)} messages."
        )

        return history.copy()

    def context_size(self) -> int:
        """
        Return the number of messages currently in context.
        """

        return len(conversation.get_history())

    def clear_context(self) -> None:
        """
        Clear the current context.
        """

        conversation.clear_history()

        logger.info("Context cleared.")


context = ContextManager()