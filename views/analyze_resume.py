"""Page 1 — Analyze Resume."""
from __future__ import annotations

import streamlit as st

from src import ui
from src.agents import analyze_resume
from src.llm import LLMError

from ._common import resume_input


def _render_results(result: dict) -> None:
    score = int(result.get("overall_score", 0) or 0)
    summary = result.get("summary", "")
    detected = result.get("detected", {}) or {}

    verdict = (
        "Recruiter-ready"
        if score >= 85
        else "Strong with polish"
        if score >= 70
        else "Needs improvement"
        if score >= 50
        else "Significant gaps"
    )
    ui.score_ring(score, verdict, summary, color=ui.verdict_color(score))

    col1, col2, col3 = st.columns(3)
    with col1:
        ui.stat_card("Candidate", detected.get("candidate_name") or "Not detected")
    with col2:
        ui.stat_card("Target role", detected.get("target_role") or "Not specified")
    with col3:
        ui.stat_card("Experience", detected.get("years_of_experience") or "Not detected")

    top_skills = detected.get("top_skills") or []
    if top_skills:
        ui.section_heading("Top Skills Detected")
        ui.chips(top_skills, variant="primary")

    section_scores = result.get("section_scores") or {}
    if section_scores:
        ui.section_heading("Section Scores")
        for key, value in section_scores.items():
            ui.bar_row(key, int(value), color=ui.verdict_color(int(value)))

    col_s, col_w = st.columns(2)
    with col_s:
        ui.section_heading("Strengths")
        for item in result.get("strengths", []) or []:
            ui.list_row("plus", item)
    with col_w:
        ui.section_heading("Weaknesses")
        for item in result.get("weaknesses", []) or []:
            ui.list_row("minus", item)

    ats_issues = result.get("ats_issues") or []
    if ats_issues:
        ui.section_heading("ATS Compatibility Issues")
        for item in ats_issues:
            ui.list_row("warn", item)

    suggestions = result.get("improvement_suggestions") or []
    if suggestions:
        ui.section_heading("Improvement Suggestions")
        for s in suggestions:
            area = s.get("area", "Suggestion")
            suggestion = s.get("suggestion", "")
            example = s.get("example") or ""
            with st.expander(area, expanded=False):
                st.write(suggestion)
                if example:
                    st.markdown("**Example rewrite**")
                    st.info(example)


def render() -> None:
    ui.hero(
        "Project 1 · Resume Analyzer",
        "Analyze Your Resume",
        "Upload your resume and receive a structured review: overall score, section-level breakdown, strengths, weaknesses, ATS compatibility, and concrete rewrite suggestions.",
    )

    resume_text = resume_input("analyze")

    submit = ui.center_button(
        "Analyze",
        key="analyze_submit",
        disabled=not resume_text,
    )

    if submit and resume_text:
        with st.spinner("Reviewing your resume..."):
            try:
                result = analyze_resume(resume_text)
            except LLMError as exc:
                st.error(str(exc))
                return
        st.session_state["analyze_result"] = result

    if "analyze_result" in st.session_state:
        st.divider()
        _render_results(st.session_state["analyze_result"])
