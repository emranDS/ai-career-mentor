"""Runtime configuration loaded from Streamlit secrets or environment."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "arcee-ai/trinity-large-preview:free"


def _get(key: str, default: str | None = None) -> str | None:
    try:
        import streamlit as st

        if key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.getenv(key, default)


@dataclass(frozen=True)
class Settings:
    api_key: str | None
    model: str
    app_url: str
    app_name: str


def get_settings() -> Settings:
    return Settings(
        api_key=_get("OPENROUTER_API_KEY"),
        model=_get("OPENROUTER_MODEL", DEFAULT_MODEL) or DEFAULT_MODEL,
        app_url=_get("APP_URL", "http://localhost:8501") or "http://localhost:8501",
        app_name=_get("APP_NAME", "AI Career Mentor") or "AI Career Mentor",
    )
