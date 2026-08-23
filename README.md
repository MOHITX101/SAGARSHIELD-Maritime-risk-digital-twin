Markdown# ⚓ SAGARSHIELD: Maritime Supply Chain & Strategic Petroleum Reserve Digital Twin

> **An AI-Driven Decision Intelligence Engine for Geopolitical Risk Assessment, Dynamic Route Optimization, and Emergency Strategic Petroleum Reserve (SPR) Planning.**

---

## 📌 Executive Summary

Global energy supply chains are highly vulnerable to geopolitical flashpoints across critical maritime chokepoints—such as the **Strait of Hormuz**, **Red Sea / Bab-el-Mandeb**, **Cape of Good Hope**, and **Malacca Strait**. Security incidents, drone attacks, or regional blockades in these corridors immediately cause shipping delays, elevated freight costs, and supply shortfalls.

**SAGARSHIELD** is an end-to-end Digital Twin built to safeguard crude oil supply chains. It continuously ingests real-time security news feeds, quantifies corridor risk using accelerated **Groq LLM inference**, dynamically calculates risk-adjusted procurement routes via **Linear Programming (SciPy)**, and simulates emergency **Strategic Petroleum Reserve (SPR)** drawdowns when severe supply shortfalls occur.

---

## 🎯 The Problem & Our Solution

### The Challenge
1. **Unstructured & Volatile Information:** Maritime intelligence is locked inside continuous news feeds and geopolitical alerts, making manual risk tracking too slow.
2. **Dynamic Cost vs. Capacity Trade-Offs:** Re-routing vessels around high-risk zones (e.g., around the Cape of Good Hope) adds transit time and cost premiums, requiring optimal allocation under capacity constraints.
3. **Emergency Reserve Calibration:** When primary routes are compromised, energy authorities lack real-time visibility into exact daily supply deficits and SPR depletion trajectories.

### The SAGARSHIELD Solution
* **Automated Risk Scoring:** Converts raw security headlines into standardized threat indices ($0.0$ to $1.0$).
* **Mathematical Procurement Optimization:** Solves for the lowest landed cost per barrel while respecting risk-constrained throughput limits.
* **SPR Digital Twin:** Automatically models multi-day reserve extraction schedules when total safe corridor capacity falls below national import requirements.
* **Interactive Command Center:** Provides an executive dashboard with geospatial route maps, procurement breakdowns, and reserve stock projections.

---

## 🏗️ System Architecture & Workflow

SAGARSHIELD is structured into modular decision layers:

```text
       ┌─────────────────────────────────────────┐
       │     Live RSS Feed / Manual Input        │
       └────────────────────┬────────────────────┘
                            │
                            ▼
       ┌─────────────────────────────────────────┐
       │   1. Dynamic Geopolitical Risk Agent   │
       │     (Groq API / Llama 3.3 / GPT-OSS)    │
       └────────────────────┬────────────────────┘
                            │  [Outputs Corridor Risk Scores]
                            ▼
       ┌─────────────────────────────────────────┐
       │     2. Linear Procurement Optimizer     │
       │       (SciPy HiGHS LP Engine)           │
       └────────────────────┬────────────────────┘
                            │  [Calculates Unmet Import Deficit]
                            ▼
       ┌─────────────────────────────────────────┐
       │   3. Strategic Petroleum Reserve Agent   │
       │     (Multi-Day Drawdown Simulator)      │
       └────────────────────┬────────────────────┘
                            │
                            ▼
       ┌─────────────────────────────────────────┐
       │     4. Streamlit Interactive Twin       │
       │   (Plotly Maps, Risk Cards, Schedules)  │
       └─────────────────────────────────────────┘
🛠️ Core Engine Deep Dive1. Dynamic Risk Scoring (agents/risk_agent.py)Ingests news streams using an automated Google News RSS parser or manual text input.Passes raw text payloads to Groq (openai/gpt-oss-120b) to generate structured JSON outputs containing localized threat scores and reasoning for key chokepoints.Resilience Built-In: Includes automated fallback heuristics to ensure system continuity even during network disruptions or API outages.2. Linear Procurement Optimizer (core/optimizer.py)Formulates supply distribution as a constrained Linear Program solved via scipy.optimize.linprog:$$\text{Minimize } \sum_{i} \left( \text{Base Cost}_i \times (1 + \text{Risk}_i \times 0.5) \right) \times x_i$$$$\text{Subject to: } \sum x_i = \text{Import Need}, \quad 0 \le x_i \le \text{Base Capacity}_i \times (1 - \text{Risk}_i \times 0.7)$$Risk Premiums: As threat ratings rise, route landed costs increase (insurance/fuel surcharges) while throughput capacities shrink.3. Strategic Reserve Simulation Engine (agents/reserve_agent.py)Monitors real-time import deficits ($\text{Unmet Demand} = \text{Import Need} - \sum \text{Delivered}$).Models daily extraction limits ($1.2\text{ MBD}$) against total reserve capacity ($39.5\text{ MB}$).Generates a daily 14-day depletion schedule and outputs visual burn-rate projections.🛠️ Tech StackLanguage: Python 3.10+Dashboard & Framework: StreamlitLLM Orchestration & Inference: Groq API Client (openai/gpt-oss-120b)Optimization & Math: SciPy (scipy.optimize.linprog), NumPyData & Visualization: Pandas, Plotly Express, Plotly Graph ObjectsData Acquisition: Python urllib, xml.etree.ElementTree (RSS Parsing)📂 Repository StructurePlaintextSAGARSHIELD-Maritime-risk-digital-twin/
├── .streamlit/
│   ├── config.toml        # Streamlit dashboard theme configurations
│   └── secrets.toml       # Local API keys (Ignored by git)
├── agents/
│   ├── __init__.py
│   ├── risk_agent.py      # Groq LLM integration & news threat evaluation
│   └── reserve_agent.py   # Multi-day SPR drawdown simulation engine
├── core/
│   ├── __init__.py
│   ├── network_graph.py   # Maritime network topology definitions
│   └── optimizer.py       # Linear programming cost & route optimizer
├── app.py                 # Main orchestration dashboard & UI layout
├── requirements.txt       # Project dependencies
├── .gitignore             # Git exclusion parameters
└── README.md              # Project documentation
⚙️ Installation & Local Setup1. Clone the RepositoryBashgit clone [https://github.com/MOHITX101/SAGARSHIELD-Maritime-risk-digital-twin.git](https://github.com/MOHITX101/SAGARSHIELD-Maritime-risk-digital-twin.git)
cd SAGARSHIELD-Maritime-risk-digital-twin
2. Create and Activate Virtual EnvironmentBash# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
3. Install Required PackagesBashpip install -r requirements.txt
4. Configure API SecretsCreate a .streamlit/secrets.toml file in the root directory:Ini, TOMLGROQ_API_KEY = "your_groq_api_key_here"
5. Launch the ApplicationBashstreamlit run app.py
🎮 How to Test & DemoTest Live News Mode: Launch the app, keep the feed selector on 🌐 Live RSS Security Feed, and click ⚡ Run Dynamic Supply Chain Pipeline.Simulate a High-Risk Incident: Switch to ✍️ Manual News Input, paste a critical scenario (e.g., "Hormuz blocked due to active missile escalation"), and re-run.Inspect Supply Deficits: Observe the 🚨 Corridor Risk Indices jump to CRITICAL, watch capacities drop in 📊 Procurement Optimization, and navigate to 🛡️ SPR Drawdown Schedule to review the reserve extraction trajectory.