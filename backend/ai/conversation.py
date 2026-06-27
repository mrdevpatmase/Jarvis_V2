"""
Conversation manager for Jarvis AI.

Maintains the current conversation session between the user and Jarvis.
"""

from typing import Dict, List, Optional

from backend.config.settings import settings


class ConversationManager:
    """
    Manages the current conversation history.
    """

    def __init__(self) -> None:
        self._messages: List[Dict[str, str]] = []
        self._max_messages = settings.MEMORY_LIMIT * 2

    def _trim_history(self) -> None:
        """
        Keep only the latest messages.
        """

        while len(self._messages) > self._max_messages:
            self._messages.pop(0)

    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation.

        Args:
            role: "user" or "assistant"
            content: Message text
        """

        self._messages.append(
            {
                "role": role,
                "content": content.strip()
            }
        )

        self._trim_history()

    def add_user_message(self, message: str) -> None:
        """
        Add a user message.
        """

        self.add_message("user", message)

    def add_assistant_message(self, message: str) -> None:
        """
        Add an assistant message.
        """

        self.add_message("assistant", message)

    def get_history(self) -> List[Dict[str, str]]:
        """
        Return a copy of the conversation history.
        """

        return self._messages.copy()

    def get_last_message(self) -> Optional[Dict[str, str]]:
        """
        Return the most recent message.
        """

        if not self._messages:
            return None

        return self._messages[-1]

    def message_count(self) -> int:
        """
        Return the total number of stored messages.
        """

        return len(self._messages)

    def clear_history(self) -> None:
        """
        Clear the conversation history.
        """

        self._messages.clear()


conversation = ConversationManager()