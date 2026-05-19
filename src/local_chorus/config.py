"""App configuration — single source of truth for runtime settings.

All env vars are LOCAL_CHORUS_*-prefixed so they don't collide with system
variables. A `.env` file at the repo root is loaded automatically.
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
CACHE_DIR = ROOT_DIR / ".cache"


class Settings(BaseSettings):
    """Runtime configuration, loaded from environment + .env file."""

    model_config = SettingsConfigDict(
        env_prefix="LOCAL_CHORUS_",
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Ollama ---
    ollama_url: str = Field(
        default="http://localhost:11434",
        description="Base URL of the local Ollama server.",
    )
    ollama_model: str = Field(
        default="llama3.1:8b",
        description="Default chat model tag (must be `ollama pull`-ed first).",
    )
    ollama_embed_model: str = Field(
        default="nomic-embed-text",
        description="Embedding model for RAG.",
    )

    # --- Behavior ---
    request_timeout_s: float = Field(default=60.0, ge=1.0)
    log_level: str = Field(default="INFO")

    # --- Paths ---
    data_dir: Path = DATA_DIR
    cache_dir: Path = CACHE_DIR


# Module-level singleton: import once, reuse everywhere.
settings = Settings()
