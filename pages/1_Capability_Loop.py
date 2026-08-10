import streamlit as st
import plotly.express as px
import pandas as pd
from utils.theme import inject_css, page_header, AMBER, MINT, MUTED, PLOTLY_TEMPLATE
from utils.data_loader import load_employees, LOOP_STAGES

st.set_page_config(page_title="Capability Loop — Aeon Command Center", page_icon="🔁", layout="wide")
inject_css()

page_header(
    "SLIDE 2 · THE SOLUTION",
    "The Capability Loop",
    "Aeon's differentiating intelligence engine — the 7-step cycle every learner "
    "moves through, replacing a one-way content-delivery pipe with a closed loop.",
)

STEP_DESC = {
    "Assess": "Knowledge, role skills, learning activity + relevant performance evidence",
    "Diagnose": "AI identifies and prioritises capability gaps",
    "Intervene": "RAG-grounded AI Tutor + adaptive path + microlearning + assessment",
    "Apply": "Simulation / role-play / real-world task",
    "Measure": "Pre/post capability + workplace KPI where appropriate",
    "CPI": "Capability Progress Index shows demonstrated improvement",
    "Reassess": "System continuously updates the capability profile",
}

# ---- Loop diagram (simple radial layout using Plotly) ----
import numpy as np
n = len(LOOP_STAGES)
angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
xs = np.cos(angles)
ys = np.sin(angles)

fig = px.scatter(
    x=xs, y=ys, text=LOOP_STAGES, template=PLOTLY_TEMPLATE,
)
fig.update_traces(
    marker=dict(size=54, color=AMBER, line=dict(color="white", width=2)),
    textposition="middle center", textfont=dict(size=13, color="#16204F", family="Arial Black"),
)
# connecting loop line
loop_x = list(xs) + [xs[0]]
loop_y = list(ys) + [ys[0]]
fig.add_scatter(x=loop_x, y=loop_y, mode="lines", line=dict(color=MUTED, width=2, dash="dot"),
                 showlegend=False)
fig.update_layout(
    height=460, margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(visible=False, range=[-1.5, 1.5]), yaxis=dict(visible=False, range=[-1.5, 1.5]),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
)

col1, col2 = st.columns([1.1, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.markdown("#### Step-by-Step")
    for i, stage in enumerate(LOOP_STAGES, start=1):
        st.markdown(f"**{i}. {stage}** — {STEP_DESC[stage]}")

st.markdown("---")

# ---- Where is the workforce in the loop right now? ----
st.markdown("#### Where Is the Workforce in the Loop Right Now?")
df = load_employees()
dept_filter = st.multiselect("Filter by department", sorted(df["department"].unique()),
                              default=sorted(df["department"].unique()))
filtered = df[df["department"].isin(dept_filter)]

stage_counts = filtered["loop_stage"].value_counts().reindex(LOOP_STAGES).fillna(0).reset_index()
stage_counts.columns = ["stage", "employees"]

bar = px.bar(stage_counts, x="stage", y="employees", template=PLOTLY_TEMPLATE,
             color_discrete_sequence=[MINT], text="employees")
bar.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=340,
                   paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(bar, use_container_width=True)
st.caption(
    "Employees clustering in early stages (Assess/Diagnose) signal onboarding backlog; "
    "clustering in Apply/Measure signals a coaching or workplace-application bottleneck — "
    "exactly the failure point most LMS dashboards can't see."
)

with st.expander("AI Foundation Behind This Loop"):
    st.markdown(
        "- **RAG (Retrieval-Augmented Generation)** grounds the AI Tutor in Aeon's own "
        "verified content — not open-web answers.\n"
        "- **Specialised agents** handle path curation, skill-gap diagnosis, and nudges.\n"
        "- The Capability Loop — not 'agents' — is the headline. AI is the engine under the hood, "
        "not the pitch."
    )
