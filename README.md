# Aeon Command Center

**A working Streamlit prototype of the "Aeon Command Center" — the Premium-tier product
proposed in the AEON LXP 360 case solution (La Conquista'26, SDA Bocconi Asia Center × Aeon Software).**

> "Stop measuring whether employees completed training — start measuring whether
> training changed capability and created business value."

This app turns the 3-slide solution deck into something a judge (or Aeon's own leadership)
can click through: the Capability Loop, the Capability Progress Index (CPI), the Training ROI
Engine, workforce-level skill-gap intelligence, and the Responsible AI + phased rollout plan.

All data in this build is **synthetic and seeded** — it stands in for Aeon's real SCORM/xAPI
event stream and HRIS feed so the product experience can be demoed without customer data.

---

## How this maps to the case solution

| Solution Doc Element | Where It Lives in This App |
|---|---|
| Slide 1 — The Problem + Strategic Insight | `app.py` (hero funnel + thesis), `pages/4_Workforce_Intelligence.py` |
| Slide 2 — AEON LXP 360 + Capability Loop | `pages/1_Capability_Loop.py`, `pages/2_Capability_Progress_Index.py` |
| Slide 3 — Business Model + Execution + Responsible AI | `pages/3_Training_ROI_Engine.py`, `pages/5_Responsible_AI_and_Roadmap.py` |

---

## Project structure

```
aeon-command-center/
├── app.py                              # Home — Command Center overview
├── pages/
│   ├── 1_Capability_Loop.py            # 7-step loop diagram + live stage distribution
│   ├── 2_Capability_Progress_Index.py  # CPI distributions, drill-downs, learner lookup
│   ├── 3_Training_ROI_Engine.py        # ROI trend + interactive ROI scenario calculator
│   ├── 4_Workforce_Intelligence.py     # Skill-gap heatmap, department snapshot
│   └── 5_Responsible_AI_and_Roadmap.py # Governance safeguards + phased rollout timeline
├── utils/
│   ├── data_loader.py                  # Synthetic data generation (swap for real connectors)
│   └── theme.py                        # Shared "Midnight Executive" visual identity
├── .streamlit/
│   └── config.toml                     # Dark theme matching the slide deck's palette
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## Run it locally

```bash
# 1. Clone and enter the repo
git clone https://github.com/<your-org>/aeon-command-center.git
cd aeon-command-center

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch
streamlit run app.py
```

The app opens at `http://localhost:8501`. Use the sidebar to move between the Command Center
home, Capability Loop, CPI, Training ROI Engine, Workforce Intelligence, and Responsible AI pages.

---

## Deploy for free (Streamlit Community Cloud)

1. Push this repo to GitHub (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** → select this repo → set the main file path to `app.py`.
4. Deploy. No secrets or API keys are required for the demo build.

---

## Swapping in real data

Every page imports data exclusively through `utils/data_loader.py`. To connect Aeon's real
systems, replace the internals of the `load_*()` functions with actual connectors — for
example:

- `load_employees()` → pull from the HRIS + xAPI learning-record store, join on employee ID
- `load_skill_gap_matrix()` → output of the Diagnose stage of the Capability Loop
- `load_roi_timeseries()` → Training ROI Engine's attribution pipeline output
- `load_funnel()` → aggregate counts per Learning-to-Performance funnel stage

No page code needs to change — only the data layer.

---

## Design notes

- **Palette:** matches the "Midnight Executive" identity used across the case slide deck
  (`#16204F` navy, `#F2A950` amber, `#3ED9A4` mint, `#FF6F61` coral) — set globally in
  `.streamlit/config.toml` and `utils/theme.py`.
- **Charting:** [Plotly](https://plotly.com/python/) for interactivity (hover, zoom, filter)
  appropriate to a leadership dashboard rather than a static report.
- **CPI is explicitly framed as a development metric, not a performance-review score**,
  consistent with the Responsible AI safeguards in the solution's governance section —
  see the notice on the CPI page and the safeguards list on the Responsible AI page.

---

## Roadmap for this prototype

- [ ] Wire `data_loader.py` to a real SCORM/xAPI Learning Record Store
- [ ] Add authentication (e.g. `streamlit-authenticator`) before any real employee data is loaded
- [ ] Add export-to-PDF for the ROI Scenario Calculator results (board-ready one-pagers)
- [ ] Add a manager-facing view scoped to direct reports only (role-based access)

---

## License

MIT — see [`LICENSE`](LICENSE). Solution content (case strategy, framework names) developed
for the La Conquista'26 case competition submission.
