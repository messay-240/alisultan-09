import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SolarX Pro - Global Energy Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PROFESSIONAL STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { border: 1px solid #30363d; padding: 15px; border-radius: 12px; background-color: #161b22; }
    div.stButton > button:first-child { background-color: #238636; color: white; border-radius: 8px; width: 100%; }
    .status-card { padding: 20px; border-radius: 15px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1px solid #334155; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- EXPANDED 60+ COUNTRIES DATABASE ---
# Format: Country: [Optimal Angle, Currency, Sell Rate, Buy Rate]
db = {
    "Pakistan": [30, "PKR", 42.0, 65.0], "India": [22, "INR", 5.0, 9.0], "USA": [35, "USD", 0.12, 0.28],
    "United Kingdom": [50, "GBP", 0.15, 0.45], "Germany": [48, "EUR", 0.08, 0.40], "Canada": [45, "CAD", 0.05, 0.15],
    "Australia": [35, "AUD", 0.07, 0.32], "UAE": [24, "AED", 0.15, 0.35], "Saudi Arabia": [25, "SAR", 0.10, 0.20],
    "China": [35, "CNY", 0.40, 0.60], "Japan": [35, "JPY", 16.0, 30.0], "France": [40, "EUR", 0.10, 0.25],
    "Italy": [38, "EUR", 0.12, 0.30], "Brazil": [20, "BRL", 0.45, 0.95], "Turkey": [38, "TRY", 2.5, 4.5],
    "South Africa": [28, "ZAR", 1.2, 2.8], "Russia": [55, "RUB", 2.0, 5.0], "Mexico": [23, "MXN", 1.5, 3.0],
    "Spain": [37, "EUR", 0.15, 0.30], "Egypt": [27, "EGP", 0.8, 1.6], "Nigeria": [15, "NGN", 50, 100],
    "Indonesia": [10, "IDR", 1500, 3000], "Qatar": [25, "QAR", 0.1, 0.25], "Kuwait": [29, "KWD", 0.02, 0.05],
    "Norway": [60, "NOK", 0.5, 1.5], "Sweden": [58, "SEK", 0.6, 1.8], "Iran": [32, "IRR", 5000, 15000],
    "Iraq": [33, "IQD", 50, 120], "Bangladesh": [23, "BDT", 5.0, 10.0], "Malaysia": [5, "MYR", 0.3, 0.5],
    "Singapore": [1, "SGD", 0.2, 0.3], "Netherlands": [52, "EUR", 0.1, 0.4], "Switzerland": [47, "CHF", 0.15, 0.35],
    "Austria": [46, "EUR", 0.12, 0.38], "Belgium": [51, "EUR", 0.08, 0.42], "Denmark": [55, "DKK", 0.6, 2.5],
    "Finland": [60, "EUR", 0.1, 0.3], "Greece": [38, "EUR", 0.15, 0.3], "Portugal": [37, "EUR", 0.1, 0.25],
    "Ireland": [53, "EUR", 0.18, 0.45], "New Zealand": [-40, "NZD", 0.08, 0.3], "South Korea": [36, "KRW", 150, 280],
    "Thailand": [15, "THB", 2.2, 4.5], "Vietnam": [18, "VND", 2000, 3500], "Philippines": [14, "PHP", 5.0, 11.0],
    "Argentina": [-34, "ARS", 15, 40], "Chile": [-33, "CLP", 60, 150], "Colombia": [4, "COP", 300, 600],
    "Peru": [-12, "PEN", 0.2, 0.5], "Poland": [52, "PLN", 0.3, 0.8], "Ukraine": [49, "UAH", 4.0, 7.0],
    "Kazakhstan": [48, "KZT", 15, 25], "Oman": [23, "OMR", 0.02, 0.05], "Jordan": [31, "JOD", 0.08, 0.15],
    "Sri Lanka": [7, "LKR", 20, 45], "Morocco": [32, "MAD", 0.8, 1.5], "Kenya": [1, "KES", 12, 25],
    "Ethiopia": [9, "ETB", 0.5, 1.2], "Ghana": [5, "GHS", 0.5, 1.0], "Tanzania": [-6, "TZS", 100, 350]
}

# --- SIDEBAR PRO PANEL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3222/3222672.png", width=80)
    st.title("SolarX Control")
    
    country = st.selectbox("🌍 Select Market", sorted(db.keys()), index=0)
    c_data = db[country]
    
    st.header("⚡ System Architecture")
    p_watt = st.number_input("Panel Rating (W)", value=580)
    p_num = st.number_input("Panel Count", value=15)
    orientation = st.selectbox("Mounting Type", ["Fixed - Optimal", "Fixed - Horizontal", "Single Axis Tracker"])
    
    st.header("🔋 Storage (Optional)")
    has_battery = st.checkbox("Include Battery Bank?")
    batt_cap = st.slider("Battery Capacity (kWh)", 0, 50, 10) if has_battery else 0
    
    st.header("🌡️ Environment")
    weather = st.select_slider("Sky Condition", ["Stormy", "Overcast", "Hazy", "Clear Sky"], value="Clear Sky")
    soiling = st.slider("Dust/Soiling Loss (%)", 0, 20, 5)

# --- CA
