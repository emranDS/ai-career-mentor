"""Shared widgets for all pages."""
from __future__ import annotations

import hashlib

import streamlit as st

from src.resume_parser import UnsupportedFileError, extract_text


def _file_fingerprint(uploaded) -> str:
    name = getattr(uploaded, "name", "")
    size = getattr(uploaded, "size", 0)
    # getvalue() doesn't advance the buffer, so safe to hash on every rerun
    data = uploaded.getvalue() if hasattr(uploaded, "getvalue") else b""
    digest = hashlib.md5(data[:4096] if data else b"").hexdigest()
    return f"{name}:{size}:{digest}"


def resume_input(key_prefix: str) -> str | None:
    """Render upload + paste tabs. Returns extracted resume text or None."""
    cache_key = f"{key_prefix}_parsed_cache"
    if cache_key not in st.session_state:
        st.session_state[cache_key] = {}

    tab_upload, tab_paste = st.tabs(["Upload file", "Paste text"])

    with tab_upload:
        uploaded = st.file_uploader(
            "Resume file (PDF, DOCX, TXT, MD)",
            type=["pdf", "docx", "txt", "md"],
            key=f"{key_prefix}_upload",
            label_visibility="collapsed",
        )
        if uploaded is not None:
            try:
                fp = _file_fingerprint(uploaded)
                cache = st.session_state[cache_key]
                if fp not in cache:
                    cache[fp] = extract_text(uploaded)
                text = cache[fp]
                st.caption(f"Parsed {len(text.split()):,} words from {uploaded.name}")
                return text
            except UnsupportedFileError as exc:
                st.error(str(exc))
                return None

    with tab_paste:
        pasted = st.text_area(
            "Paste resume text",
            height=260,
            key=f"{key_prefix}_paste",
            placeholder="Paste your resume text here...",
            label_visibility="collapsed",
        )
        if pasted and pasted.strip():
            return pasted.strip()

    return None
