import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import urllib.request
import json
import xml.etree.ElementTree as ET
from scipy.optimize import linprog

from agents.risk_agent import DynamicGeopoliticalRiskAgent
from agents.reserve_agent import StrategicReserveAgent

# Page Configuration
st.set_page_config(
    page_title="AegisEnergy AI - Maritime Supply Chain Digital Twin",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Risk Agent
@st.cache_resource
def get_risk_agent():
    return DynamicGeopoliticalRiskAgent()

risk_agent = get_risk_agent()

# Sidebar Setup
st.sidebar.title("⚙️ Engine Parameters")

if risk_agent.client:
    st.sidebar.success("Groq API Connected (Llama 3.3 / GPT-OSS)")
else:
    st.sidebar.warning("Groq Disconnected (Using Local Fallback)")

vessel_speed = st.sidebar.slider("Vessel Speed (Knots)", 10.0, 24.0, 14.0)
import_need = st.sidebar.slider("India Import Need (MBD)", 1.0, 8.0, 4.50)

st.title("⚓ Maritime Geopolitical Risk & SPR Digital Twin")

# --- NEWS FEED MODE SELECTOR ---
news_mode = st.radio(
    "Select News Data Source:",
    ["🌐 Live RSS Security Feed (Automatic)", "✍️ Manual News Input"],
    horizontal=True
)

def fetch_live_maritime_news():
    """Fetches real-time RSS news items covering maritime security."""
    rss_url = "https://news.google.com/rss/search?q=maritime+shipping+strait+red+sea+security&hl=en-US&gl=US&ceid=US:en"
    try:
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        items = root.findall('.//item')[:5]  # Get top 5 news items
        
        extracted_text = []
        for item in items:
            title = item.find('title').text if item.find('title') is not None else ""
            extracted_text.append(f"Headline: {title}")
            
        return " | ".join(extracted_text)
    except Exception as e:
        return f"Headline: Red Sea security disruption reported. Summary: Operational risks elevated in transit zones. (Fallback: {str(e)})"

if news_mode == "🌐 Live RSS Security Feed (Automatic)":
    with st.spinner("Fetching live maritime security news feeds..."):
        news_feed = fetch_live_maritime_news()
    st.info(f"**Fetched Live Stream:** {news_feed[:200]}...")
else:
    default_manual = (
        "Headline: Red Sea: Critical maritime corridor faces security challenges - Credendo. "
        "Summary: Red Sea: Critical maritime corridor faces security challenges | "
        "Headline: Deadly attack on Red Sea ship adds to global supply chain uncertainty - UN News."
    )
    news_feed = st.text_area("Live Maritime Security News Feed Input:", value=default_manual, height=100)

run_pipeline = st.button("⚡ Run Dynamic Supply Chain Pipeline", type="primary", use_container_width=True)

# --- PIPELINE EXECUTION ---
if run_pipeline or "risk_results" not in st.session_state:
    with st.spinner("Processing Risk Indices & Solving Supply Optimization..."):
        # 1. Geopolitical Risk Analysis
        st.session_state.risk_results = risk_agent.analyze_news_and_calculate_risk(news_feed)
        
        # 2. Linear Optimization
        corridors = ["Strait of Hormuz", "Red Sea / Bab-el-Mandeb", "Cape of Good Hope", "Malacca Strait"]
        base_costs = [65.0, 72.0, 85.0, 78.0]
        base_capacities = [2.50, 1.50, 1.00, 0.50]

        adjusted_costs = []
        adjusted_caps = []
        for i, corridor in enumerate(corridors):
            risk_val = st.session_state.risk_results.get(corridor, {}).get("score", 0.10)
            adjusted_costs.append(base_costs[i] * (1.0 + risk_val * 0.5))
            adjusted_caps.append(base_capacities[i] * (1.0 - risk_val * 0.7))

        res = linprog(adjusted_costs, A_eq=[[1.0, 1.0, 1.0, 1.0]], b_eq=[import_need], bounds=[(0, cap) for cap in adjusted_caps], method='highs')

        if res.success:
            allocations = res.x
            unmet = max(0.0, import_need - sum(allocations))
        else:
            allocations = [min(import_need * (cap / sum(adjusted_caps)), cap) for cap in adjusted_caps]
            unmet = max(0.0, import_need - sum(allocations))

        st.session_state.opt_results = {
            "corridors": corridors,
            "allocations": allocations,
            "adjusted_costs": adjusted_costs,
            "adjusted_caps": adjusted_caps,
            "unmet_demand": unmet
        }

        # 3. Reserve Calculation
        reserve_agent = StrategicReserveAgent(initial_reserve_mb=39.5, max_drawdown_mbd=1.2)
        st.session_state.drawdown_schedule = reserve_agent.calculate_drawdown_schedule(
            unmet_demand_mbd=st.session_state.opt_results["unmet_demand"]
        )

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🚨 Corridor Risk Indices", 
    "🗺️ Geospatial Digital Twin", 
    "📊 Procurement Optimization", 
    "🛡️ SPR Drawdown Schedule"
])

with tab1:
    cols = st.columns(4)
    corr_keys = list(st.session_state.risk_results.keys())
    for i, col in enumerate(cols):
        if i < len(corr_keys):
            c_name = corr_keys[i]
            data = st.session_state.risk_results[c_name]
            score_pct = int(data["score"] * 100)
            with col:
                st.subheader(c_name)
                st.metric(label="Risk Rating", value=f"{score_pct}% Risk")
                if score_pct >= 70:
                    st.error("↑ CRITICAL")
                elif score_pct >= 35:
                    st.warning("↑ ELEVATED")
                else:
                    st.success("↑ STABLE")
                st.caption(data["rationale"])
                
    with st.expander("🔍 Debug Live LLM News Payload"):
        st.code(news_feed, language="text")

# Tab 2, Tab 3, Tab 4 render same as previous layout...
with tab2:
    st.subheader("Maritime Digital Twin Corridor Map")
    locations = {
        "Strait of Hormuz": {"lat": 26.56, "lon": 56.25},
        "Red Sea / Bab-el-Mandeb": {"lat": 12.58, "lon": 43.33},
        "Cape of Good Hope": {"lat": -34.83, "lon": 20.00},
        "Malacca Strait": {"lat": 2.50, "lon": 101.50},
        "Mumbai/Jamnagar Port (India)": {"lat": 18.96, "lon": 72.82}
    }
    fig = go.Figure()
    dest = locations["Mumbai/Jamnagar Port (India)"]
    for corridor, loc in locations.items():
        if corridor == "Mumbai/Jamnagar Port (India)":
            continue
        risk_score = st.session_state.risk_results.get(corridor, {}).get("score", 0.1)
        line_color = "#FF4B4B" if risk_score >= 0.7 else ("#FFAA00" if risk_score >= 0.35 else "#00CC66")
        fig.add_trace(go.Scattergeo(
            lat=[loc["lat"], dest["lat"]],
            lon=[loc["lon"], dest["lon"]],
            mode='lines+markers',
            line=dict(width=3, color=line_color),
            name=f"{corridor} ({int(risk_score*100)}% Risk)"
        ))
    fig.update_layout(geo=dict(projection_type="natural earth", showland=True), margin=dict(l=0, r=0, t=10, b=0), height=450)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Linear Optimization & Cost Allocation Engine")
    opt = st.session_state.opt_results
    df_opt = pd.DataFrame({
        "Corridor": opt["corridors"],
        "Allocated Volume (MBD)": [round(x, 2) for x in opt["allocations"]],
        "Effective Capacity (MBD)": [round(x, 2) for x in opt["adjusted_caps"]],
        "Landed Cost ($/Bbl)": [round(x, 2) for x in opt["adjusted_costs"]]
    })
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.dataframe(df_opt, use_container_width=True, hide_index=True)
    with col_r:
        st.bar_chart(df_opt.set_index("Corridor")["Allocated Volume (MBD)"])

with tab4:
    st.subheader("Strategic Petroleum Reserve (SPR) Drawdown Analysis")
    df_schedule = pd.DataFrame(st.session_state.drawdown_schedule)
    col_s_left, col_s_right = st.columns([1, 1])
    with col_s_left:
        st.dataframe(df_schedule, use_container_width=True, hide_index=True)
    with col_s_right:
        st.line_chart(df_schedule.set_index("Day")[["Remaining Reserve (MB)", "Reserve Drawdown (MBD)"]])