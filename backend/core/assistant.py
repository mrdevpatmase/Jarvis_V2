"""
Main Assistant Orchestrator.

This is the heart of Jarvis.
Every user request flows through this class.
"""
from backend.core.context import context
from backend.ai.conversation import conversation
from backend.ai.llm import llm
from backend.config.logger import logger


class Assistant:
    """
    Main Jarvis Assistant.
    Coordinates conversation and AI responses.
    """

    def process_message(self, user_message: str) -> str:
        """
        Process a user message.

        Args:
            user_message: User input.

        Returns:
            Assistant response.
        """

        logger.info(f"User: {user_message}")

        # Store user message
        conversation.add_user_message(user_message)

        # Ask LLM

        response = llm.generate_response(
            context.build_context()
        )

        # Store assistant response
        conversation.add_assistant_message(response)

        logger.info("Assistant response generated.")

        return response

    def reset_conversation(self) -> None:
        """
        Start a new conversation.
        """

        conversation.clear_history()

        logger.info("Conversation reset.")

    def get_conversation(self):
        """
        Return current conversation.
        """

        return conversation.get_history()


assistant = Assistant()