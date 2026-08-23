⚓SAGARSHIELD
⚓SAGARSHIELD :  Maritime Supply Chain & Strategic Petroleum Reserve Digital Twin
An AI-driven decision intelligence engine that evaluates real-time geopolitical maritime security risks, simulates supply disruptions across transit corridors, optimizes crude oil procurement using linear programming, and models multi-day Strategic Petroleum Reserve (SPR) drawdown trajectories.

🚀 Key Features & Capabilities
Real-Time Geopolitical Risk Engine: Leverages Groq-accelerated LLM inference (openai/gpt-oss-120b) to parse live news feeds and evaluate risk scores (0.0 to 1.0) across key maritime bottlenecks (Strait of Hormuz, Red Sea / Bab-el-Mandeb, Cape of Good Hope, and Malacca Strait).

Linear Procurement Optimization Engine: Runs a Scipy Highs Linear Programming Solver to re-route crude procurement dynamically. It balances risk premiums and throughput capacity limits to minimize landed cost while fulfilling India's import demand.

Strategic Petroleum Reserve (SPR) Digital Twin: Calculates daily supply deficits and models a multi-day drawdown schedule (39.5 MB base capacity at up to 1.2 MBD daily extraction limit) when maritime bottlenecks stall vessel throughput.

Interactive Geospatial Visualizations: Features interactive Plotly maps showing active shipping lanes, color-coded risk severity, and real-time route health indicators.

Hybrid Data Ingestion: Supports both automated real-time RSS security feed fetching and manual scenario injection for custom stress-testing.

🛠️ Tech Stack & Architecture
Frontend & UI: Streamlit Engine

LLM & Reasoning: Groq API SDK (openai/gpt-oss-120b)

Optimization Solver: SciPy (scipy.optimize.linprog)

Geospatial & Analytics: Plotly Express / Graph Objects, Pandas

Data Processing & Scraping: Python urllib, xml.etree.ElementTree

📂 Repository Structure
Plaintext
Hackathon/
├── .streamlit/
│   ├── config.toml        # Streamlit UI theme configurations
│   └── secrets.toml       # API credentials (GROQ_API_KEY)
├── agents/
│   ├── __init__.py
│   ├── risk_agent.py      # Groq LLM integration & risk index generation
│   └── reserve_agent.py   # Multi-day SPR drawdown simulation engine
├── core/
│   ├── __init__.py
│   ├── network_graph.py   # Maritime network topology definitions
│   └── optimizer.py       # Linear programming cost & route optimizer
├── app.py                 # Main Streamlit orchestration dashboard
├── requirements.txt       # Project dependencies
├── .gitignore             # Git exclusion rules
└── README.md              # Project documentation
⚙️ Installation & Local Setup
1. Clone the Repository & Setup Environment
Bash
git clone https://github.com/your-username/your-repo-name.git
cd Hackathon

# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
2. Install Dependencies
Bash
pip install -r requirements.txt
3. Set Up API Credentials
Create a .streamlit/secrets.toml file in the root directory and add your Groq API key:

Ini, TOML
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
4. Run the Dashboard
Bash
streamlit run app.py
💡 How It Works (Pipeline Workflow)
News Acquisition: Live RSS feeds or manual news feeds are passed to risk_agent.py.

LLM Evaluation: Groq evaluates localized threats and outputs structured JSON ratings for each corridor.

Capacity & Cost Penalties: High risk scores scale up shipping landed costs (risk premiums) and scale down effective corridor throughput.

Scipy LP Solving: app.py runs linear programming to find the cheapest route allocation satisfying total import need.

SPR Deficit Trigger: If total safe corridor capacity falls below total import need, the remaining deficit triggers reserve_agent.py to plot a 14-day SPR emergency extraction trajectory.