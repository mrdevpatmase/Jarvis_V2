"""
Task Executor for Jarvis AI.

Receives the selected tool from the router and executes it.
"""

from backend.config.logger import logger


class Executor:

    def __init__(self):
        self.tools = {}

    def register_tool(self, name: str, tool):
        """
        Register a tool.
        """

        self.tools[name] = tool

        logger.info(f"Registered tool: {name}")

    def execute(self, tool_name: str, user_message: str):
        """
        Execute the selected tool.

        Args:
            tool_name: Tool selected by the router.
            user_message: Original user request.
        """

        logger.info(f"Executing tool: {tool_name}")

        tool = self.tools.get(tool_name)

        if tool is None:

            logger.error(f"Tool '{tool_name}' not found.")

            return f"Tool '{tool_name}' not found."

        return tool.execute(user_message)


executor = Executor()