"""Reusable UI helpers (cards, score rings, chips, bars) — centered, modern design."""
from __future__ import annotations

import html
from pathlib import Path
from typing import Iterable

import streamlit as st

_CSS_PATH = Path(__file__).resolve().parent.parent / "assets" / "styles.css"


def inject_styles() -> None:
    if _CSS_PATH.exists():
        st.markdown(f"<style>{_CSS_PATH.read_text()}</style>", unsafe_allow_html=True)


def _safe(text: str) -> str:
    """HTML-escape user text and convert newlines to <br> so embedded
    line breaks can never terminate a markdown HTML block."""
    if not text:
        return ""
    return html.escape(str(text)).replace("\r\n", "\n").replace("\n", "<br>")


def _render(html_str: str) -> None:
    """Render a single-line HTML string via st.markdown.

    Streamlit's CommonMark parser terminates HTML blocks at the first blank
    line. Multi-line f-string templates with optional/empty sections can
    accidentally produce whitespace-only lines, which breaks rendering and
    leaks raw <div> tags to the page. Collapsing to a single line avoids it.
    """
    st.markdown(html_str, unsafe_allow_html=True)


def hero(eyebrow: str, title: str, subtitle: str) -> None:
    _render(
        '<div class="acm-hero">'
        f'<div class="acm-hero-eyebrow">{_safe(eyebrow)}</div>'
        f'<h1>{_safe(title)}</h1>'
        f'<p>{_safe(subtitle)}</p>'
        '</div>'
    )


def score_ring(score: int, verdict: str, caption: str = "", color: str = "#4f46e5") -> None:
    score = max(0, min(100, int(score)))
    _render(
        '<div class="acm-score-wrap">'
        '<div class="acm-score-card">'
        f'<div class="acm-score-ring" style="--pct: {score}; --ring: {color};">'
        f'<span>{score}</span>'
        '</div>'
        f'<div class="acm-score-verdict">{_safe(verdict)}</div>'
        f'<div class="acm-score-caption">{_safe(caption)}</div>'
        '</div>'
        '</div>'
    )


def stat_card(title: str, value: str, description: str = "", *, centered: bool = True) -> None:
    cls = "acm-card acm-stat-center" if centered else "acm-card"
    desc_html = f'<p>{_safe(description)}</p>' if description else ""
    _render(
        f'<div class="{cls}">'
        f'<div class="acm-card-title">{_safe(title)}</div>'
        f'<div class="acm-card-value">{_safe(str(value))}</div>'
        f'{desc_html}'
        '</div>'
    )


def chips(items: Iterable[str], variant: str = "") -> None:
    cls = f"acm-chip {variant}".strip()
    items_list = list(items)
    if not items_list:
        _render('<div class="acm-chips"><span class="acm-chip">None</span></div>')
        return
    chips_html = "".join(f'<span class="{cls}">{_safe(str(i))}</span>' for i in items_list)
    _render(f'<div class="acm-chips">{chips_html}</div>')


def bar_row(label: str, value: int, color: str = "") -> None:
    value = max(0, min(100, int(value)))
    pretty_label = label.replace("_", " ").title()
    style = f"background:{color};" if color else ""
    fill_style = f' style="width:{value}%; {style}"' if color else f' style="width:{value}%"'
    _render(
        '<div class="acm-bar-row">'
        f'<div class="acm-bar-label"><b>{_safe(pretty_label)}</b><span>{value}/100</span></div>'
        f'<div class="acm-bar-track"><div class="acm-bar-fill"{fill_style}></div></div>'
        '</div>'
    )


def list_row(variant: str, title: str, text: str = "", meta: str = "") -> None:
    icons = {"plus": "+", "minus": "−", "warn": "!", "info": "i"}
    icon = icons.get(variant, "·")
    meta_html = f'<div class="acm-row-meta">{_safe(meta)}</div>' if meta else ""
    text_html = f'<div class="acm-row-text">{_safe(text)}</div>' if text else ""
    _render(
        '<div class="acm-row">'
        f'<div class="acm-row-icon {variant}">{icon}</div>'
        '<div class="acm-row-body">'
        f'<div class="acm-row-title">{_safe(title)}</div>'
        f'{meta_html}{text_html}'
        '</div>'
        '</div>'
    )


def compare_block(original: str, improved: str, rationale: str = "") -> None:
    rationale_html = (
        f'<div class="acm-rationale">{_safe(rationale)}</div>' if rationale else ""
    )
    _render(
        '<div class="acm-compare">'
        '<div>'
        '<div class="acm-compare-title">Original</div>'
        f'<div>{_safe(original)}</div>'
        '</div>'
        '<div class="improved">'
        '<div class="acm-compare-title">Improved</div>'
        f'<div>{_safe(improved)}</div>'
        '</div>'
        '</div>'
        f'{rationale_html}'
    )


def verdict_color(score: int) -> str:
    if score >= 80:
        return "#15803d"
    if score >= 60:
        return "#4f46e5"
    if score >= 40:
        return "#b45309"
    return "#b91c1c"


def section_heading(title: str, subtitle: str = "") -> None:
    sub_html = f'<p>{_safe(subtitle)}</p>' if subtitle else ""
    _render(f'<div class="acm-section"><h3>{_safe(title)}</h3>{sub_html}</div>')


def center_button(label: str, *, key: str, disabled: bool = False) -> bool:
    """Render a horizontally centered, modern primary button with an arrow affordance."""
    state_class = "acm-cta-btn" + (" is-disabled" if disabled else "")
    st.markdown(
        f'<div class="acm-cta {state_class}">',
        unsafe_allow_html=True,
    )
    cols = st.columns([3, 2, 3])
    with cols[1]:
        clicked = st.button(
            f"{label.title()}  →",
            key=key,
            type="primary",
            disabled=disabled,
            use_container_width=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
    return clicked


def footer() -> None:
    _render(
        '<div class="acm-footer">'
        'AI Career Mentor · Built for Deep Learning (CSE638)'
        '</div>'
    )
