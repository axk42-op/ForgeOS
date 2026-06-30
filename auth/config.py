"""Auth configuration from environment and optional .env file."""

import os
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_env() -> None:
    """Load Forge/.env if python-dotenv is available."""
    env_path = _project_root() / ".env"
    if not env_path.is_file():
        return
    try:
        from dotenv import load_dotenv

        load_dotenv(env_path)
    except ImportError:
        pass


def get_supabase_url() -> str | None:
    load_env()
    value = os.environ.get("FORGEOS_SUPABASE_URL", "").strip()
    return value or None


def get_supabase_key() -> str | None:
    load_env()
    value = os.environ.get("FORGEOS_SUPABASE_KEY", "").strip()
    return value or None


def is_supabase_configured() -> bool:
    return bool(get_supabase_url() and get_supabase_key())
