import streamlit as st
import plotly.express as px
from utils.theme import inject_css, page_header, PLOTLY_TEMPLATE
from utils.data_loader import load_skill_gap_matrix, load_employees

st.set_page_config(page_title="Workforce Intelligence — Aeon Command Center", page_icon="🧠", layout="wide")
inject_css()

page_header(
    "SLIDE 1 · STRATEGIC SHIFT",
    "Workforce Intelligence",
    "Learning Management → Learning Intelligence → Capability Intelligence → Workforce Intelligence. "
    "This is the top of that ladder: gaps visible across the whole organisation, not one course at a time.",
)

gaps = load_skill_gap_matrix()
df = load_employees()

st.markdown("#### Skill-Gap Heatmap by Department")
pivot = gaps.pivot(index="skill", columns="department", values="gap_score")
fig = px.imshow(
    pivot, text_auto=".0f", aspect="auto", template=PLOTLY_TEMPLATE,
    color_continuous_scale=["#3ED9A4", "#F2A950", "#FF6F61"],
)
fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=440,
                   paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)
st.caption("Higher score = larger capability gap relative to role requirements. "
           "Darker red cells are where the Capability Loop should prioritise interventions next quarter.")

st.markdown("#### Top Priority Gaps")
top_gaps = gaps.sort_values("gap_score", ascending=False).head(10)
st.dataframe(
    top_gaps.rename(columns={"department": "Department", "skill": "Skill",
                              "gap_score": "Gap Score", "priority": "Priority"}),
    use_container_width=True, hide_index=True,
)

st.markdown("---")
st.markdown("#### Headcount & Capability Snapshot by Department")
dept_summary = df.groupby("department", as_index=False).agg(
    learners=("employee_id", "count"),
    avg_cpi=("cpi", "mean"),
    completion_rate=("course_completed", "mean"),
    application_rate=("applied_on_job", "mean"),
)
dept_summary["avg_cpi"] = dept_summary["avg_cpi"].round(1)
dept_summary["completion_rate"] = (dept_summary["completion_rate"] * 100).round(1)
dept_summary["application_rate"] = (dept_summary["application_rate"] * 100).round(1)
st.dataframe(
    dept_summary.rename(columns={
        "department": "Department", "learners": "Learners", "avg_cpi": "Avg CPI",
        "completion_rate": "Completion %", "application_rate": "Applied on Job %",
    }),
    use_container_width=True, hide_index=True,
)
