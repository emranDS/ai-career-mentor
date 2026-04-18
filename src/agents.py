"""Single-agent analyzers and multi-agent orchestration for page 3."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Any

from . import prompts
from .llm import chat_json


def analyze_resume(resume_text: str) -> dict[str, Any]:
    return chat_json(
        prompts.ANALYZER_SYSTEM,
        prompts.ANALYZER_USER.format(resume=resume_text),
        temperature=0.3,
        max_tokens=2200,
    )


def match_job(resume_text: str, job_description: str) -> dict[str, Any]:
    return chat_json(
        prompts.MATCH_SYSTEM,
        prompts.MATCH_USER.format(resume=resume_text, job=job_description),
        temperature=0.2,
        max_tokens=2200,
    )


def optimize_resume(resume_text: str, role: str) -> dict[str, Any]:
    return chat_json(
        prompts.OPTIMIZER_SYSTEM,
        prompts.OPTIMIZER_USER.format(resume=resume_text, role=role),
        temperature=0.4,
        max_tokens=2400,
    )


def analyze_skill_gap(resume_text: str, role: str) -> dict[str, Any]:
    return chat_json(
        prompts.SKILL_GAP_SYSTEM,
        prompts.SKILL_GAP_USER.format(resume=resume_text, role=role),
        temperature=0.3,
        max_tokens=2400,
    )


def prepare_interview(resume_text: str, role: str) -> dict[str, Any]:
    return chat_json(
        prompts.INTERVIEW_SYSTEM,
        prompts.INTERVIEW_USER.format(resume=resume_text, role=role),
        temperature=0.5,
        max_tokens=2600,
    )


def run_career_agents(resume_text: str, role: str) -> dict[str, Any]:
    """Run the three career agents in parallel and return their outputs."""
    tasks = {
        "optimizer": (optimize_resume, resume_text, role),
        "skill_gap": (analyze_skill_gap, resume_text, role),
        "interview": (prepare_interview, resume_text, role),
    }
    results: dict[str, Any] = {}
    errors: dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            name: pool.submit(fn, *args) for name, (fn, *args) in tasks.items()
        }
        for name, future in futures.items():
            try:
                results[name] = future.result()
            except Exception as exc:
                errors[name] = str(exc)

    return {"results": results, "errors": errors}
