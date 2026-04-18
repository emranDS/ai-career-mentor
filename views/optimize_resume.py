"""Page 3 — Optimize Resume (3 agents: Optimizer, Skill Gap, Interview Prep)."""
from __future__ import annotations

import streamlit as st

from src import ui
from src.agents import run_career_agents
from src.llm import LLMError

from ._common import resume_input


def _render_optimizer(data: dict) -> None:
    if not data:
        st.info("Resume optimizer did not return a result.")
        return
    headline = data.get("headline", "")
    if headline:
        ui.stat_card("Suggested Headline", headline)

    summary_rewrite = data.get("summary_rewrite", "")
    if summary_rewrite:
        ui.section_heading("Rewritten Professional Summary")
        st.info(summary_rewrite)

    bullets = data.get("bullet_rewrites") or []
    if bullets:
        ui.section_heading("Bullet Rewrites")
        for b in bullets:
            ui.compare_block(
                original=b.get("original", ""),
                improved=b.get("improved", ""),
                rationale=b.get("rationale", ""),
            )

    keywords = data.get("keyword_injections") or []
    if keywords:
        ui.section_heading("Keywords to Include")
        ui.chips(keywords, variant="primary")

    tips = data.get("formatting_tips") or []
    if tips:
        ui.section_heading("Formatting Tips")
        for t in tips:
            ui.list_row("info", t)

    checklist = data.get("ats_checklist") or []
    if checklist:
        ui.section_heading("ATS Checklist")
        for item in checklist:
            status = (item.get("status") or "warn").lower()
            variant = {"pass": "plus", "fail": "minus"}.get(status, "warn")
            ui.list_row(
                variant,
                item.get("item", ""),
                meta=status.title(),
                text=item.get("note", ""),
            )


def _render_skill_gap(data: dict) -> None:
    if not data:
        st.info("Skill gap analyzer did not return a result.")
        return

    score = int(data.get("readiness_score", 0) or 0)
    ui.score_ring(
        score,
        f"{data.get('current_level', 'Unclear')} · Readiness {score}%",
        f"Target role: {data.get('target_role', '')}",
        color=ui.verdict_color(score),
    )

    strengths = data.get("strengths") or []
    if strengths:
        ui.section_heading("Strengths")
        ui.chips(strengths, variant="success")

    gaps = data.get("critical_gaps") or []
    if gaps:
        ui.section_heading("Critical Gaps")
        for g in gaps:
            priority = (g.get("priority") or "medium").lower()
            variant = {"high": "minus", "medium": "warn", "low": "info"}.get(priority, "warn")
            ui.list_row(
                variant,
                g.get("skill", ""),
                meta=f"{priority.title()} priority",
                text=g.get("why_it_matters", ""),
            )

    plan = data.get("learning_plan") or []
    if plan:
        ui.section_heading("Learning Plan")
        for p in plan:
            skill = p.get("skill", "")
            weeks = p.get("estimated_weeks", "?")
            with st.expander(f"{skill}  ·  ~{weeks} weeks", expanded=False):
                milestones = p.get("milestones") or []
                if milestones:
                    st.markdown("**Milestones**")
                    for m in milestones:
                        st.markdown(f"- {m}")
                resources = p.get("resources") or []
                if resources:
                    st.markdown("**Resources**")
                    for r in resources:
                        kind = r.get("type", "resource").title()
                        name = r.get("name", "")
                        provider = r.get("provider")
                        provider_str = f" — {provider}" if provider else ""
                        st.markdown(f"- **{kind}**: {name}{provider_str}")

    projects = data.get("portfolio_projects") or []
    if projects:
        ui.section_heading("Portfolio Project Ideas")
        for proj in projects:
            ui.list_row(
                "info",
                proj.get("title", ""),
                text=proj.get("description", ""),
                meta=", ".join(proj.get("skills_demonstrated") or []),
            )


def _render_interview(data: dict) -> None:
    if not data:
        st.info("Interview preparation agent did not return a result.")
        return

    sub_tabs = st.tabs(["Behavioral", "Technical", "Role-specific", "Ask back", "Checklist"])

    with sub_tabs[0]:
        for q in data.get("behavioral_questions") or []:
            with st.expander(q.get("question", ""), expanded=False):
                assesses = q.get("what_they_assess", "")
                if assesses:
                    st.caption(f"Assesses: {assesses}")
                answer = q.get("suggested_answer", "")
                if answer:
                    st.markdown("**Suggested STAR answer**")
                    st.write(answer)

    with sub_tabs[1]:
        for q in data.get("technical_questions") or []:
            with st.expander(q.get("question", ""), expanded=False):
                topic = q.get("topic", "")
                if topic:
                    st.caption(f"Topic: {topic}")
                outline = q.get("ideal_answer_outline") or []
                if outline:
                    st.markdown("**Answer outline**")
                    for b in outline:
                        st.markdown(f"- {b}")

    with sub_tabs[2]:
        for q in data.get("role_specific_questions") or []:
            with st.expander(q.get("question", ""), expanded=False):
                st.write(q.get("why_it_is_asked", ""))

    with sub_tabs[3]:
        ask_back = data.get("questions_to_ask_interviewer") or []
        if not ask_back:
            st.caption("No recommendations.")
        for q in ask_back:
            ui.list_row("info", q)

    with sub_tabs[4]:
        red_flags = data.get("red_flags_to_avoid") or []
        if red_flags:
            ui.section_heading("Red Flags to Avoid")
            for r in red_flags:
                ui.list_row("minus", r)
        checklist = data.get("preparation_checklist") or []
        if checklist:
            ui.section_heading("Preparation Checklist")
            for c in checklist:
                ui.list_row("plus", c)


def render() -> None:
    ui.hero(
        "Project 3 · AI Career Agent",
        "Optimize Your Resume with AI",
        "Three specialist agents run in parallel: a Resume Optimizer rewrites your bullets, a Skill Gap Analyzer builds a learning plan, and an Interview Prep agent generates a mock question bank — all tailored to your target role.",
    )

    col_resume, col_role = st.columns([1.2, 1])

    with col_resume:
        ui.section_heading("Resume")
        resume_text = resume_input("optimize")

    with col_role:
        ui.section_heading("Target Role")
        role = st.text_input(
            "Target role",
            placeholder="e.g. Senior Machine Learning Engineer",
            label_visibility="collapsed",
            key="optimize_role",
        )
        st.caption("Optional: paste a job description below for tighter tailoring.")
        job_context = st.text_area(
            "Job description (optional)",
            height=180,
            placeholder="Paste target job description for stronger tailoring...",
            label_visibility="collapsed",
            key="optimize_job",
        )

    effective_role = role.strip() or "target role inferred from resume"
    if job_context and job_context.strip():
        effective_role = f"{effective_role}\n\nContext from job description:\n{job_context.strip()}"

    submit = ui.center_button(
        "Optimize",
        key="optimize_submit",
        disabled=not resume_text,
    )

    if submit and resume_text:
        with st.spinner("Running Resume Optimizer, Skill Gap Analyzer, and Interview Prep agents in parallel..."):
            try:
                outputs = run_career_agents(resume_text, effective_role)
            except LLMError as exc:
                st.error(str(exc))
                return
        st.session_state["optimize_result"] = outputs

    if "optimize_result" in st.session_state:
        outputs = st.session_state["optimize_result"]
        errors = outputs.get("errors") or {}
        results = outputs.get("results") or {}

        if errors:
            for name, msg in errors.items():
                st.error(f"{name.replace('_', ' ').title()} agent failed: {msg}")

        st.divider()
        agent_tabs = st.tabs(["Resume Optimizer", "Skill Gap Analyzer", "Interview Preparation"])
        with agent_tabs[0]:
            _render_optimizer(results.get("optimizer") or {})
        with agent_tabs[1]:
            _render_skill_gap(results.get("skill_gap") or {})
        with agent_tabs[2]:
            _render_interview(results.get("interview") or {})
