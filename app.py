"""AI Career Mentor — main Streamlit entry point with centered top navigation."""
from __future__ import annotations

import streamlit as st

from src import ui
from src.config import get_settings
from views import analyze_resume, match_jobs, optimize_resume

PAGES = {
    "analyze": {"label": "Analyze Resume", "render": analyze_resume.render},
    "match": {"label": "Match Jobs", "render": match_jobs.render},
    "optimize": {"label": "Optimize Resume", "render": optimize_resume.render},
}


def _init_state() -> None:
    if "active_page" not in st.session_state:
        st.session_state.active_page = "analyze"


def _go(page_key: str) -> None:
    st.session_state.active_page = page_key


def _render_navigation() -> None:
    settings = get_settings()

    st.markdown(
        f"""
        <div class="acm-nav">
          <a class="acm-brand" href="#" onclick="return false;">
            <span class="acm-brand-mark" aria-hidden="true">
              <svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="none">
                <defs>
                  <linearGradient id="acm-spark" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="#fde68a"/>
                    <stop offset="100%" stop-color="#f59e0b"/>
                  </linearGradient>
                </defs>
                <path d="M7 29 L15 12 L20 22 L25 12 L33 29"
                      stroke="white" stroke-width="3"
                      stroke-linecap="round" stroke-linejoin="round"
                      fill="none" opacity="0.96"/>
                <circle cx="31" cy="10" r="2.6" fill="url(#acm-spark)"/>
                <circle cx="31" cy="10" r="4.6" fill="url(#acm-spark)" opacity="0.3"/>
              </svg>
            </span>
            <span class="acm-brand-wordmark">
              <span class="acm-brand-name">{settings.app_name}</span>
              <span class="acm-brand-tag">Built with Claude</span>
            </span>
          </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Centered pill navigation — 5-column layout leaves space on both sides
    nav_cols = st.columns([1, 1.2, 1.2, 1.2, 1])
    for idx, (key, meta) in enumerate(PAGES.items(), start=1):
        with nav_cols[idx]:
            is_active = st.session_state.active_page == key
            st.button(
                meta["label"],
                key=f"nav_{key}",
                on_click=_go,
                args=(key,),
                type="primary" if is_active else "secondary",
                use_container_width=True,
            )


def _render_missing_key_banner() -> None:
    settings = get_settings()
    if settings.api_key:
        return
    st.warning(
        "OPENROUTER_API_KEY is not configured. Add it to a local `.env` file or to "
        "`.streamlit/secrets.toml` before running analyses.",
        icon=None,
    )


def main() -> None:
    st.set_page_config(
        page_title="AI Career Mentor",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    ui.inject_styles()
    _init_state()
    _render_navigation()
    _render_missing_key_banner()

    page = PAGES[st.session_state.active_page]
    page["render"]()

    ui.footer()


if __name__ == "__main__":
    main()
