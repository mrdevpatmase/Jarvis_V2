"""
Task model for Jarvis AI.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Task:
    """
    Represents a task selected by the router.
    """

    tool: str
    action: str
    parameters: Dict[str, Any]