import streamlit as st
from utils.theme import inject_css, page_header, AMBER, MINT, CORAL, MUTED, PLOTLY_TEMPLATE
from utils.data_loader import load_employees, kpi_summary, load_funnel
import plotly.express as px

st.set_page_config(
    page_title="Aeon Command Center",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("### AEON LXP 360")
    st.caption("Powered by the Capability Loop")
    st.markdown("---")
    st.markdown(
        "**Navigate:**\n\n"
        "- 🏠 Command Center (this page)\n"
        "- 🔁 Capability Loop\n"
        "- 📈 Capability Progress Index\n"
        "- 💰 Training ROI Engine\n"
        "- 🧠 Workforce Intelligence\n"
        "- 🛡️ Responsible AI & Roadmap"
    )
    st.markdown("---")
    st.caption("Demo build · synthetic data · La Conquista'26 case submission")

# ---------------- Header ----------------
page_header(
    "AEON COMMAND CENTER",
    "From Course Completed → Capability Proven → Business Value",
    "A live view for L&D and HR leaders into capability gaps, demonstrated improvement, "
    "and the business ROI training investment is actually creating.",
)

df = load_employees()
kpis = kpi_summary(df)

# ---------------- KPI row ----------------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Active Learners", f"{kpis['learners']:,}")
c2.metric("Avg. Capability Progress Index", f"{kpis['avg_cpi']}")
c3.metric("Course Completion Rate", f"{kpis['completion_rate']}%")
c4.metric("On-the-Job Application Rate", f"{kpis['application_rate']}%")
c5.metric("Avg. Capability Lift", f"+{kpis['avg_lift']} pts")

st.markdown("")

col_a, col_b = st.columns([1.3, 1])

with col_a:
    st.markdown("#### The Learning-to-Performance Funnel")
    funnel = load_funnel()
    fig = px.funnel(funnel, x="count", y="stage", template=PLOTLY_TEMPLATE,
                     color_discrete_sequence=[AMBER])
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=340,
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Most LMS dashboards stop at 'Training Participation'. Aeon Command Center "
        "tracks every stage through to ROI Realised — this is the Learning-to-Performance Gap made visible."
    )

with col_b:
    st.markdown("#### The Strategic Thesis")
    st.markdown(
        """
        <div class="aeon-card">
        <p style="margin-top:0;"><b>"Stop measuring whether employees completed training —
        start measuring whether training changed capability and created business value."</b></p>
        <p style="font-size:0.9rem;">Do not compete by adding another generic AI chatbot or
        course recommender. Aeon's existing LMS/LXP foundation becomes a closed-loop system
        connecting learning, demonstrated capability, workplace application, and business outcomes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")
    st.markdown("#### The Winning Architecture")
    st.markdown(
        "- **AEON LXP 360** — the AI-powered learning experience platform\n"
        "- **Capability Loop** — the differentiating intelligence engine\n"
        "- **Capability Progress Index (CPI)** — measures demonstrated development\n"
        "- **Training ROI Engine** — connects learning spend to business outcomes\n"
        "- **Aeon Command Center** — this dashboard: visibility for L&D/HR leaders"
    )

st.markdown("---")
st.caption(
    "🧭 Use the sidebar to explore the Capability Loop, drill into the CPI by department/skill, "
    "model Training ROI scenarios, review workforce skill gaps, or check the Responsible AI safeguards "
    "and phased execution roadmap."
)
