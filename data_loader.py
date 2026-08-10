"""
Aeon Command Center — synthetic data layer.

Everything here is deterministic, seeded, synthetic demo data standing in for
Aeon's real LMS/xAPI event stream, HRIS roster, and performance-KPI feeds.
Swap `load_*()` internals for real connectors (SCORM/xAPI store, HRIS API,
data warehouse) without touching any page code — every page only imports
from this module.
"""

import numpy as np
import pandas as pd
import streamlit as st

SEED = 42

DEPARTMENTS = ["Engineering", "Sales", "Customer Success", "Operations", "Product"]
ROLES = {
    "Engineering": ["Software Engineer", "QA Engineer", "DevOps Engineer"],
    "Sales": ["Account Executive", "Sales Development Rep", "Solutions Consultant"],
    "Customer Success": ["CSM", "Support Specialist", "Onboarding Lead"],
    "Operations": ["Ops Analyst", "Process Lead", "Vendor Manager"],
    "Product": ["Product Manager", "UX Designer", "Product Analyst"],
}
SKILLS = [
    "Data Analysis", "Stakeholder Communication", "Technical Troubleshooting",
    "Negotiation", "Process Optimisation", "AI Tool Fluency",
    "Customer Discovery", "Compliance & Governance",
]
LOOP_STAGES = ["Assess", "Diagnose", "Intervene", "Apply", "Measure", "CPI", "Reassess"]

N_EMPLOYEES = 420


@st.cache_data
def load_employees() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    dept = rng.choice(DEPARTMENTS, N_EMPLOYEES, p=[0.28, 0.24, 0.20, 0.16, 0.12])
    role = [rng.choice(ROLES[d]) for d in dept]
    tenure_months = rng.integers(1, 96, N_EMPLOYEES)

    # Pre/post capability scores (0-100) — post is pre + a training lift with noise
    pre_score = np.clip(rng.normal(52, 14, N_EMPLOYEES), 10, 95)
    lift = np.clip(rng.normal(16, 9, N_EMPLOYEES), -5, 40)
    post_score = np.clip(pre_score + lift, 0, 100)

    completion = rng.choice([1, 1, 1, 0], N_EMPLOYEES)  # ~75% completion baseline
    applied_on_job = np.where(
        completion == 1, rng.choice([1, 0], N_EMPLOYEES, p=[0.58, 0.42]), 0
    )
    loop_stage = rng.choice(LOOP_STAGES, N_EMPLOYEES, p=[0.05, 0.08, 0.22, 0.18, 0.15, 0.22, 0.10])

    df = pd.DataFrame({
        "employee_id": [f"AEO-{i:04d}" for i in range(1, N_EMPLOYEES + 1)],
        "department": dept,
        "role": role,
        "tenure_months": tenure_months,
        "primary_skill": rng.choice(SKILLS, N_EMPLOYEES),
        "pre_capability_score": pre_score.round(1),
        "post_capability_score": post_score.round(1),
        "capability_lift": (post_score - pre_score).round(1),
        "course_completed": completion,
        "applied_on_job": applied_on_job,
        "loop_stage": loop_stage,
    })
    df["cpi"] = (df["capability_lift"] / (100 - df["pre_capability_score"]).clip(lower=1) * 100).clip(0, 100).round(1)
    return df


@st.cache_data
def load_skill_gap_matrix() -> pd.DataFrame:
    rng = np.random.default_rng(SEED + 1)
    rows = []
    for d in DEPARTMENTS:
        for s in SKILLS:
            gap = np.clip(rng.normal(35, 18), 2, 90)
            priority = "High" if gap > 55 else ("Medium" if gap > 30 else "Low")
            rows.append({"department": d, "skill": s, "gap_score": round(gap, 1), "priority": priority})
    return pd.DataFrame(rows)


@st.cache_data
def load_roi_timeseries() -> pd.DataFrame:
    rng = np.random.default_rng(SEED + 2)
    months = pd.date_range("2025-09-01", periods=12, freq="MS")
    spend = np.clip(rng.normal(48_000, 6_000, 12).cumsum() / np.arange(1, 13), 30_000, 70_000)
    value_created = spend * np.linspace(1.1, 2.4, 12) + rng.normal(0, 8_000, 12)
    return pd.DataFrame({
        "month": months,
        "training_spend": spend.round(0),
        "business_value_created": value_created.round(0),
    })


@st.cache_data
def load_funnel() -> pd.DataFrame:
    # Training participation -> capability improvement -> workplace application -> business KPI lift -> ROI realised
    stages = [
        "Training Participation", "Capability Improvement Verified",
        "Workplace Application Observed", "Business KPI Lift Attributed", "ROI Realised",
    ]
    counts = [N_EMPLOYEES, int(N_EMPLOYEES * 0.81), int(N_EMPLOYEES * 0.55),
              int(N_EMPLOYEES * 0.37), int(N_EMPLOYEES * 0.29)]
    return pd.DataFrame({"stage": stages, "count": counts})


def kpi_summary(df: pd.DataFrame) -> dict:
    return {
        "learners": len(df),
        "avg_cpi": round(df["cpi"].mean(), 1),
        "completion_rate": round(df["course_completed"].mean() * 100, 1),
        "application_rate": round(df["applied_on_job"].mean() * 100, 1),
        "avg_lift": round(df["capability_lift"].mean(), 1),
    }
