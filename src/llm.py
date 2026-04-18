"""OpenRouter LLM client with JSON-mode helper."""
from __future__ import annotations

import json
import re
from typing import Any

from openai import OpenAI

from .config import get_settings

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class LLMError(RuntimeError):
    pass


def _client() -> OpenAI:
    settings = get_settings()
    if not settings.api_key:
        raise LLMError(
            "OPENROUTER_API_KEY is not set. Add it to .env locally or to Streamlit secrets when deployed."
        )
    return OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=settings.api_key,
        default_headers={
            "HTTP-Referer": settings.app_url,
            "X-Title": settings.app_name,
        },
    )


def chat(
    system: str,
    user: str,
    *,
    temperature: float = 0.4,
    max_tokens: int = 2048,
) -> str:
    settings = get_settings()
    client = _client()

    try:
        response = client.chat.completions.create(
            model=settings.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as exc:
        raise LLMError(f"LLM request failed ({settings.model}): {exc}") from exc

    content = (response.choices[0].message.content or "").strip()
    if not content:
        raise LLMError(f"Model {settings.model} returned an empty response.")
    return content


_JSON_FENCE = re.compile(r"```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```", re.DOTALL)


def _extract_json(text: str) -> str:
    match = _JSON_FENCE.search(text)
    if match:
        return match.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text


def chat_json(
    system: str,
    user: str,
    *,
    temperature: float = 0.2,
    max_tokens: int = 2048,
) -> Any:
    guarded_system = (
        system
        + "\n\nRespond with a single valid JSON document only. No prose, no markdown fences."
    )
    raw = chat(guarded_system, user, temperature=temperature, max_tokens=max_tokens)
    payload = _extract_json(raw)
    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise LLMError(f"Model did not return valid JSON. Raw output: {raw[:400]}") from exc
