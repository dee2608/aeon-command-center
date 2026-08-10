import streamlit as st
import plotly.express as px
from utils.theme import inject_css, page_header, AMBER, MINT, CORAL, PLOTLY_TEMPLATE
from utils.data_loader import load_employees

st.set_page_config(page_title="CPI — Aeon Command Center", page_icon="📈", layout="wide")
inject_css()

page_header(
    "SLIDE 2 · THE SOLUTION",
    "Capability Progress Index (CPI)",
    "CPI measures demonstrated development — not employee worth. It's the number "
    "that replaces 'completed: yes/no' as Aeon's core learning metric.",
)

df = load_employees()

with st.sidebar:
    st.markdown("### Filters")
    dept = st.multiselect("Department", sorted(df["department"].unique()),
                           default=sorted(df["department"].unique()))
    skill = st.multiselect("Primary skill", sorted(df["primary_skill"].unique()),
                            default=sorted(df["primary_skill"].unique()))

f = df[df["department"].isin(dept) & df["primary_skill"].isin(skill)]

c1, c2, c3 = st.columns(3)
c1.metric("Average CPI", f"{f['cpi'].mean():.1f}")
c2.metric("Median Capability Lift", f"+{f['capability_lift'].median():.1f} pts")
c3.metric("Learners ≥ 70 CPI", f"{(f['cpi'] >= 70).sum():,} of {len(f):,}")

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### CPI Distribution")
    fig = px.histogram(f, x="cpi", nbins=24, template=PLOTLY_TEMPLATE,
                        color_discrete_sequence=[AMBER])
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=340,
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Average CPI by Department")
    dept_avg = f.groupby("department", as_index=False)["cpi"].mean().sort_values("cpi", ascending=False)
    fig2 = px.bar(dept_avg, x="cpi", y="department", orientation="h", template=PLOTLY_TEMPLATE,
                  color_discrete_sequence=[MINT], text="cpi")
    fig2.update_traces(texttemplate="%{text:.1f}")
    fig2.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=340,
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("#### Pre → Post Capability, by Skill")
skill_avg = f.groupby("primary_skill", as_index=False)[["pre_capability_score", "post_capability_score"]].mean()
skill_avg = skill_avg.melt(id_vars="primary_skill", var_name="stage", value_name="score")
skill_avg["stage"] = skill_avg["stage"].map({
    "pre_capability_score": "Before Intervention", "post_capability_score": "After Intervention"
})
fig3 = px.bar(skill_avg, x="score", y="primary_skill", color="stage", barmode="group",
              orientation="h", template=PLOTLY_TEMPLATE,
              color_discrete_sequence=[CORAL, MINT])
fig3.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=420,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    legend=dict(orientation="h", y=1.08))
st.plotly_chart(fig3, use_container_width=True)

st.markdown("#### Individual Learner Lookup")
emp_id = st.selectbox("Employee ID", f["employee_id"].sort_values())
row = f[f["employee_id"] == emp_id].iloc[0]
c1, c2, c3, c4 = st.columns(4)
c1.metric("CPI", row["cpi"])
c2.metric("Capability Lift", f"+{row['capability_lift']} pts")
c3.metric("Loop Stage", row["loop_stage"])
c4.metric("Applied on Job", "Yes" if row["applied_on_job"] else "Not yet")

st.info(
    "**Governance note:** CPI is a development signal, not a performance-review score. "
    "Per Aeon's Responsible AI safeguards, capability data feeds coaching and content "
    "recommendations automatically — it never triggers employment decisions without human review.",
    icon="🛡️",
)
