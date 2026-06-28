"""
Application configuration.

Loads environment variables and provides a single source of truth
for application settings.
"""

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env file
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    """
    Global application settings.
    """

    APP_NAME: str = "Jarvis AI"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    HOST: str = os.getenv("HOST", "127.0.0.1")

    PORT: int = int(os.getenv("PORT", "5000"))

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    LLM_PROVIDER = "ollama"
    OLLAMA_MODEL = "phi3"

    MODEL_NAME: str = os.getenv(
        "MODEL_NAME",
        "gemini-2.5-flash",
    )

    DATABASE_NAME: str = os.getenv(
        "DATABASE_NAME",
        "jarvis.db",
    )

    LOG_LEVEL: str = os.getenv(
        "LOG_LEVEL",
        "INFO",
    )

    MEMORY_LIMIT: int = int(
        os.getenv("MEMORY_LIMIT", "20")
    )


settings = Settings()