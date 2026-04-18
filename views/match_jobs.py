"""Page 2 — Match Jobs."""
from __future__ import annotations

import streamlit as st

from src import ui
from src.agents import match_job
from src.llm import LLMError

from ._common import resume_input


def _render_results(result: dict) -> None:
    score = int(result.get("match_score", 0) or 0)
    verdict = result.get("verdict", "")
    summary = result.get("summary", "")
    ui.score_ring(score, verdict, summary, color=ui.verdict_color(score))

    role_summary = result.get("role_summary", "")
    if role_summary:
        ui.section_heading("Role Summary")
        st.write(role_summary)

    matched = result.get("matched_skills") or []
    missing = result.get("missing_skills") or []
    partial = result.get("partial_skills") or []

    col_a, col_b = st.columns(2)
    with col_a:
        ui.stat_card("Matched skills", str(len(matched)))
    with col_b:
        ui.stat_card("Missing skills", str(len(missing)))

    tab_matched, tab_missing, tab_partial, tab_keywords = st.tabs(
        ["Matched", "Missing", "Partial", "Keywords"]
    )

    with tab_matched:
        if not matched:
            st.caption("No skill matches detected.")
        for item in matched:
            ui.list_row(
                "plus",
                item.get("skill", ""),
                text=item.get("evidence", ""),
            )

    with tab_missing:
        if not missing:
            st.caption("No missing skills identified.")
        for item in missing:
            importance = (item.get("importance") or "").lower()
            variant = "minus" if importance == "must-have" else "warn"
            ui.list_row(
                variant,
                item.get("skill", ""),
                meta=importance.replace("-", " ").title() if importance else "",
                text=item.get("why", ""),
            )

    with tab_partial:
        if not partial:
            st.caption("No partial matches.")
        for item in partial:
            ui.list_row(
                "warn",
                item.get("skill", ""),
                text=item.get("gap", ""),
            )

    with tab_keywords:
        coverage = result.get("keyword_coverage") or {}
        present = coverage.get("present") or []
        absent = coverage.get("absent") or []
        st.markdown("**Present in resume**")
        ui.chips(present, variant="success")
        st.markdown("**Missing from resume**")
        ui.chips(absent, variant="danger")

    recommendations = result.get("recommendations") or []
    if recommendations:
        ui.section_heading("Recommendations")
        for rec in recommendations:
            ui.list_row("info", rec)


def render() -> None:
    ui.hero(
        "Project 2 · Job Match AI",
        "Match Your Resume to a Job",
        "Paste a job description alongside your resume and get a match score, matched and missing skills, keyword coverage, and recruiter-style recommendations.",
    )

    col_resume, col_job = st.columns(2)

    with col_resume:
        ui.section_heading("Resume")
        resume_text = resume_input("match")

    with col_job:
        ui.section_heading("Job Description")
        job_text = st.text_area(
            "Job description",
            height=360,
            placeholder="Paste the full job description here...",
            label_visibility="collapsed",
            key="match_job_desc",
        )

    job_text = (job_text or "").strip()

    # Enable as soon as the resume is loaded, matching Analyze and Optimize.
    submit = ui.center_button(
        "Match",
        key="match_submit",
        disabled=not resume_text,
    )

    if submit:
        if not job_text:
            st.error("Please paste a job description before matching.")
            return
        with st.spinner("Scoring the match..."):
            try:
                result = match_job(resume_text, job_text)
            except LLMError as exc:
                st.error(str(exc))
                return
        st.session_state["match_result"] = result

    if "match_result" in st.session_state:
        st.divider()
        _render_results(st.session_state["match_result"])
