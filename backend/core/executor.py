"""
Task Executor for Jarvis AI.

Executes parsed Task objects using the appropriate tool.
"""

from backend.config.logger import logger
from backend.core.task import Task


class Executor:

    def __init__(self):

        self.tools = {}

    def register_tool(self, name: str, tool) -> None:
        """
        Register a tool.
        """

        self.tools[name] = tool

        logger.info(f"Registered tool: {name}")

    def execute(self, task: Task):
        """
        Execute a parsed task.
        """

        logger.info(
            f"Executing {task.tool}.{task.action}"
        )

        tool = self.tools.get(task.tool)

        if tool is None:

            logger.warning(
                f"Tool '{task.tool}' not found."
            )

            return f"Tool '{task.tool}' is not available."

        return tool.execute(task)


executor = Executor()