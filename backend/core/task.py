"""
Task model for Jarvis.

Represents a parsed user request.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Task:

    tool: str

    action: str

    parameters: Dict[str, Any] = field(default_factory=dict)