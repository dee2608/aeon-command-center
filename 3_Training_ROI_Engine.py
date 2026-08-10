import streamlit as st
import plotly.express as px
from utils.theme import inject_css, page_header, AMBER, MINT, MUTED, PLOTLY_TEMPLATE
from utils.data_loader import load_roi_timeseries, load_employees

st.set_page_config(page_title="Training ROI Engine — Aeon Command Center", page_icon="💰", layout="wide")
inject_css()

page_header(
    "SLIDE 3 · BUSINESS MODEL",
    "Training ROI Engine",
    "Connects learning investment to measurable business outcomes — the engine that "
    "turns learning data into a recurring-revenue, analytics-as-a-service story.",
)

ts = load_roi_timeseries()
df = load_employees()

c1, c2, c3 = st.columns(3)
total_spend = ts["training_spend"].sum()
total_value = ts["business_value_created"].sum()
roi_pct = (total_value - total_spend) / total_spend * 100
c1.metric("Training Spend (12mo)", f"${total_spend:,.0f}")
c2.metric("Business Value Created (12mo)", f"${total_value:,.0f}")
c3.metric("Realised ROI", f"{roi_pct:,.0f}%")

st.markdown("#### Training Spend vs. Business Value Created")
melted = ts.melt(id_vars="month", value_vars=["training_spend", "business_value_created"],
                  var_name="series", value_name="usd")
melted["series"] = melted["series"].map({
    "training_spend": "Training Spend", "business_value_created": "Business Value Created"
})
fig = px.line(melted, x="month", y="usd", color="series", template=PLOTLY_TEMPLATE,
              color_discrete_sequence=[MUTED, AMBER], markers=True)
fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=380,
                   paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                   legend=dict(orientation="h", y=1.1))
st.plotly_chart(fig, use_container_width=True)
st.caption("Synthetic 12-month trend illustrating the Training ROI Engine's core output: "
           "the gap between what Aeon customers spend on training and the business value "
           "the platform can now attribute to it.")

st.markdown("---")
st.markdown("#### ROI Scenario Calculator")
st.caption("Model a hypothetical enterprise rollout to see how CPI-driven capability gains "
           "translate into an ROI estimate for a customer pitch.")

colA, colB, colC = st.columns(3)
with colA:
    headcount = st.number_input("Learners in program", min_value=10, max_value=50_000, value=1_000, step=50)
    cost_per_learner = st.number_input("Training cost per learner ($)", min_value=10, max_value=5_000, value=180, step=10)
with colB:
    capability_lift_pct = st.slider("Avg. capability lift (%)", 0, 60, 18)
    application_rate = st.slider("On-the-job application rate (%)", 0, 100, 58)
with colC:
    productivity_value_per_pt = st.number_input(
        "Est. productivity value per capability-lift point per learner ($)",
        min_value=1, max_value=500, value=22, step=1,
    )
    time_horizon_months = st.slider("Time horizon (months)", 3, 24, 12)

total_cost = headcount * cost_per_learner
value_created = (
    headcount * (application_rate / 100) * capability_lift_pct * productivity_value_per_pt
    * (time_horizon_months / 12)
)
scenario_roi = (value_created - total_cost) / total_cost * 100 if total_cost else 0

r1, r2, r3 = st.columns(3)
r1.metric("Total Program Cost", f"${total_cost:,.0f}")
r2.metric("Estimated Business Value Created", f"${value_created:,.0f}")
r3.metric("Estimated ROI", f"{scenario_roi:,.0f}%")

st.markdown("---")
st.markdown("#### Monetisation Tiers (Slide 3 — Business Model)")
tier_cols = st.columns(4)
tiers = [
    ("Core LMS", "Existing base", "Today's revenue floor — SCORM/xAPI content management."),
    ("LXP Pro", "AI Tutor + adaptive learning", "First upsell: RAG-grounded tutoring, adaptive paths."),
    ("Enterprise AI+", "Capability Loop + workforce analytics", "The differentiator — capability data becomes a product."),
    ("Premium", "Training ROI + Command Center + analytics-as-a-service", "This dashboard, sold as a subscription."),
]
for col, (name, feat, desc) in zip(tier_cols, tiers):
    with col:
        st.markdown(
            f"""<div class="aeon-card" style="min-height:150px;">
            <b>{name}</b><br><span style="color:{AMBER};font-size:0.85rem;">{feat}</span>
            <p style="font-size:0.82rem;">{desc}</p></div>""",
            unsafe_allow_html=True,
        )
