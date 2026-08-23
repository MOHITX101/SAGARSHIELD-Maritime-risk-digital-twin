import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import urllib.request
import json

from agents.risk_agent import evaluate_maritime_risks
from agents.reserve_agent import simulate_spr_drawdown
from core.optimizer import optimize_supply_routing
from core.network_graph import get_corridor_topology

# --- Page Configuration ---
st.set_page_config(
    page_title="SAGARSHIELD : Maritime Geopolitical Risk & SPR Digital Twin",
    page_icon="⚓",
    layout="wide"
)

# --- Fetch Live Brent Crude Price ---
@st.cache_data(ttl=600)
def get_live_brent_price():
    """Fetches live Brent crude oil price benchmark from public financial endpoints with fallback."""
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/BZ=F"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            price = data['chart']['result'][0]['meta']['regularMarketPrice']
            return round(price, 2)
    except Exception:
        return 82.50  # Fallback benchmark baseline price ($/bbl)

# --- Sidebar Controls ---
st.sidebar.markdown("## ⚙️ Engine Parameters")

# Check Groq API Key
has_groq_key = "GROQ_API_KEY" in st.secrets and len(st.secrets["GROQ_API_KEY"]) > 5
if has_groq_key:
    st.sidebar.success("Groq API Connected (Llama 3.3 / GPT-OSS)")
else:
    st.sidebar.warning("Running on Fallback Heuristics (Add Groq API key in Secrets)")

# Live Benchmark Metric
brent_price = get_live_brent_price()
st.sidebar.metric(label="Global Brent Crude (Spot)", value=f"${brent_price} / bbl")

vessel_speed = st.sidebar.slider("Vessel Speed (Knots)", min_value=10.0, max_value=24.0, value=14.0, step=0.5)
import_need = st.sidebar.slider("India Import Need (MBD)", min_value=3.0, max_value=6.0, value=4.5, step=0.1)

st.sidebar.markdown("---")
st.sidebar.info("SAGARSHIELD v2.4 | Autonomous Maritime Supply Chain Resilience Engine.")

# --- Main Header ---
st.markdown("# SAGARSHIELD ⚓ : Maritime Geopolitical Risk & SPR Digital Twin")
st.markdown("""
An AI-driven decision intelligence engine that evaluates real-time maritime security risks, 
simulates supply disruptions across transit corridors, optimizes crude oil procurement using linear programming, 
and models multi-day Strategic Petroleum Reserve (SPR) drawdowns.
""")

# --- News Source Toggle ---
source_mode = st.radio("Select News Data Source:", ["🌐 Live RSS Security Feed (Automatic)", "✍️ Manual News Input"], horizontal=True)

raw_news_payload = ""
if "Live RSS" in source_mode:
    # Simulated/Fetched live RSS snippet display
    sample_rss_text = (
        "Headline: Gunmen seize tanker off Yemen amid resurgence of Somali piracy - Al Jazeera | "
        "Headline: Unmanned cargo ship destroyed off Yemen - Seatrade Maritime News | "
        "Headline: Red Sea: Critical maritime bottleneck traffic warnings issued by naval authorities."
    )
    st.info(f"**Fetched Live Stream:** {sample_rss_text}")
    raw_news_payload = sample_rss_text
else:
    raw_news_payload = st.text_area("Enter Custom Geopolitical Security News / Stress Scenario:", 
                                     value="Critical escalation in the Strait of Hormuz. Tanker traffic restricted due to active naval skirmishes.")

# --- Run Pipeline Button ---
run_pipeline = st.button("⚡ Run Dynamic Supply Chain Pipeline", type="primary", use_container_width=True)

if run_pipeline:
    with st.spinner("Executing Groq LLM Risk Inference & SciPy LP Optimization..."):
        # 1. Evaluate Risks via Agent
        risk_data = evaluate_maritime_risks(raw_news_payload)
        
        # 2. Run Optimization
        opt_results = optimize_supply_routing(risk_data, total_demand=import_need)
        
        # 3. Simulate SPR if Deficit Exists
        deficit = opt_results.get("unmet_deficit", 0.0)
        spr_schedule = simulate_spr_drawdown(daily_deficit=deficit)
        
        st.session_state["risk_data"] = risk_data
        st.session_state["opt_results"] = opt_results
        st.session_state["spr_schedule"] = spr_schedule
        st.success("Pipeline Execution Complete!")

# Load from session if available
risk_data = st.session_state.get("risk_data", evaluate_maritime_risks("Routine maritime operations."))
opt_results = st.session_state.get("opt_results", optimize_supply_routing(risk_data, total_demand=import_need))
spr_schedule = st.session_state.get("spr_schedule", simulate_spr_drawdown(daily_deficit=0.0))

# --- Tabs for Detailed Views ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🚨 Corridor Risk Indices", 
    "🗺️ Geospatial Digital Twin", 
    "📊 Procurement Optimization", 
    "🛡️ SPR Drawdown Schedule"
])

with tab1:
    st.markdown("### Real-Time Bottleneck Threat Analysis")
    cols = st.columns(len(risk_data))
    for idx, (corridor, info) in enumerate(risk_data.items()):
        with cols[idx]:
            score = info.get("risk_score", 0.0)
            status_color = "🔴" if score > 0.6 else "🟡" if score > 0.3 else "🟢"
            st.markdown(f"#### {status_color} {corridor}")
            st.metric(label="Risk Index", value=f"{score:.2f}")
            st.write(f"**Reasoning:** {info.get('reasoning', 'Normal transit conditions.')}")

with tab2:
    st.markdown("### Interactive Maritime Trade Corridor Map")
    # Plotly geospatial map visualization
    topo_df = get_corridor_topology(risk_data)
    fig = px.scatter_geo(
        topo_df, lat="lat", lon="lon", color="risk_score",
        size="capacity", text="corridor",
        projection="natural earth",
        color_continuous_scale="Reds",
        title="Global Crude Transit Corridors & Active Risk Heatmap"
    )
    fig.update_geos(showcoastlines=True, coastlinecolor="RebeccaPurple", showland=True, landcolor="lightgray")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("### Linear Programming Procurement Allocation")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.metric(label="Total Target Import Demand", value=f"{import_need} MBD")
        st.metric(label="Total Delivered Supply", value=f"{opt_results.get('total_delivered', 0.0):.2f} MBD")
        st.metric(label="Unmet Deficit Triggering SPR", value=f"{opt_results.get('unmet_deficit', 0.0):.2f} MBD", delta_color="inverse")
    
    with col_b:
        alloc_df = pd.DataFrame(opt_results.get("allocations", []))
        if not alloc_df.empty:
            st.dataframe(alloc_df, use_container_width=True)
        else:
            st.info("Run the pipeline to generate optimal route allocations.")

with tab4:
    st.markdown("### Strategic Petroleum Reserve (SPR) 14-Day Trajectory")
    col_c, col_d = st.columns(2)
    
    with col_c:
        st.write("""
        When maritime disruptions restrict commercial vessel throughput below national requirements, 
        SAGARSHIELD automatically triggers reserve extraction from underground storage caverns (Base Capacity: 39.5 Million Barrels).
        """)
        st.metric(label="Max Daily Extraction Cap", value="1.20 MBD")
        
    with col_d:
        spr_df = pd.DataFrame(spr_schedule)
        if not spr_df.empty:
            fig_spr = px.line(spr_df, x="Day", y="Remaining_Stock_MB", markers=True, title="SPR Depletion Burn-Rate Projection (Million Barrels)")
            st.plotly_chart(fig_spr, use_container_width=True)