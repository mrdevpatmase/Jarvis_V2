from abc import ABC, abstractmethod
from typing import List, Dict


class BaseProvider(ABC):

    @abstractmethod
    def generate_response(
        self,
        messages: List[Dict[str, str]]
    ) -> str:
        pass