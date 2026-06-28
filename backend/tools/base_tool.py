from abc import ABC, abstractmethod


class BaseTool(ABC):

    @abstractmethod
    def execute(self, user_message: str):
        """
        Execute the tool.
        """
        pass