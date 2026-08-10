import streamlit as st
import pandas as pd
import plotly.express as px
from utils.theme import inject_css, page_header, AMBER, MINT, MUTED, PLOTLY_TEMPLATE

st.set_page_config(page_title="Responsible AI & Roadmap — Aeon Command Center", page_icon="🛡️", layout="wide")
inject_css()

page_header(
    "SLIDE 3 · RESPONSIBLE AI + EXECUTION",
    "Responsible AI & Phased Roadmap",
    "Governance safeguards and the phased execution plan that make the Capability Loop feasible "
    "within 24 months, reusing Aeon's existing infrastructure.",
)

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Responsible AI Safeguards (TRUST)")
    st.markdown(
        """
        <div class="aeon-card">
        <ul style="font-size:0.92rem; line-height:1.7;">
        <li><b>Human-in-the-loop</b> for any promotion or compensation decision</li>
        <li><b>Explainable recommendations</b> — every AI suggestion shows its reasoning</li>
        <li><b>Private / data-sovereign architecture</b> for enterprise customer data</li>
        <li><b>Bias audits + human override</b> built into the Capability Loop pipeline</li>
        <li>Personality/behavioural data used for <b>development only</b>,
        never for automatic employment decisions</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown("#### AI Foundation (IMPLEMENT)")
    st.markdown(
        """
        <div class="aeon-card">
        <ul style="font-size:0.92rem; line-height:1.7;">
        <li>Reuse existing <b>SCORM/xAPI</b> infrastructure — no rebuild from scratch</li>
        <li><b>RAG</b> grounds the AI Tutor in Aeon's own verified content</li>
        <li><b>Specialised agents</b> for path curation, skill-gap diagnosis, nudges</li>
        <li><b>API-based LLMs</b> — no foundation model build required</li>
        <li>Phased investment keeps upfront capital risk low</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown("#### Phased Execution Roadmap")

roadmap = pd.DataFrame([
    dict(Phase="0–6 Months", Task="RAG + AI Tutor Pilot", Start=0, Duration=6),
    dict(Phase="6–12 Months", Task="Adaptive Paths + Skill-Gap Agent + LXP Pro", Start=6, Duration=6),
    dict(Phase="12–24 Months", Task="Capability Loop + ROI Engine + Command Center", Start=12, Duration=12),
])
fig = px.timeline(
    roadmap, x_start="Start", x_end=roadmap["Start"] + roadmap["Duration"], y="Task",
    template=PLOTLY_TEMPLATE, color="Phase", color_discrete_sequence=[MINT, AMBER, "#FF6F61"],
)
fig.update_yaxes(autorange="reversed", title=None)
fig.update_xaxes(title="Month")
fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=300,
                   paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                   showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("#### Likely Judge Questions — Prepared Answers")
qa = [
    ("What is innovative?", "Not AI personalisation itself — the closed loop from learning → "
     "demonstrated capability → business outcome → ROI."),
    ("Why will customers pay?", "Because L&D can move from completion metrics to capability "
     "closure and measurable training impact."),
    ("Can competitors copy it?", "Individual features can be copied; Aeon's advantage is its "
     "existing enterprise LMS footprint, SCORM/xAPI content, and relationships that feed the "
     "capability-data loop."),
    ("What about AI bias?", "AI recommends and explains; evidence supports; humans make "
     "consequential employment decisions."),
    ("Why is it feasible?", "Phase the investment, reuse existing content/infrastructure, and "
     "use API-based LLMs rather than building a foundation model."),
]
for q, a in qa:
    with st.expander(q):
        st.write(a)
