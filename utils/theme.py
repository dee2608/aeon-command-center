"""Shared visual identity for the Aeon Command Center, matching the AEON LXP 360
solution deck (Midnight Executive palette)."""

import streamlit as st

NAVY = "#16204F"
NAVY_CARD = "#212C63"
ICE = "#CADCFC"
AMBER = "#F2A950"
CORAL = "#FF6F61"
MINT = "#3ED9A4"
MUTED = "#8FA0D6"
WHITE = "#FFFFFF"

PLOTLY_TEMPLATE = "plotly_dark"


def inject_css():
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {NAVY}; }}
        [data-testid="stSidebar"] {{ background-color: {NAVY_CARD}; }}
        h1, h2, h3, h4 {{ color: {WHITE} !important; }}
        p, li, span, label {{ color: {ICE}; }}
        [data-testid="stMetricValue"] {{ color: {AMBER}; }}
        [data-testid="stMetricLabel"] {{ color: {MUTED}; }}
        .aeon-badge {{
            display:inline-block; padding:2px 10px; border-radius:999px;
            background:{NAVY_CARD}; color:{AMBER}; font-size:0.75rem;
            font-weight:700; letter-spacing:0.05em; border:1px solid {AMBER};
        }}
        .aeon-card {{
            background:{NAVY_CARD}; border-radius:12px; padding:1.1rem 1.3rem;
            border:1px solid #2A3670;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(eyebrow: str, title: str, subtitle: str = ""):
    st.markdown(f'<span class="aeon-badge">{eyebrow}</span>', unsafe_allow_html=True)
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"<p style='color:{MUTED}; font-size:1.05rem;'>{subtitle}</p>", unsafe_allow_html=True)
    st.divider()
