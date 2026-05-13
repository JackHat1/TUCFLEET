import os
import time
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pydeck as pdk
import streamlit as st


# =============================================================================
# CONFIG
# =============================================================================

st.set_page_config(
    page_title="TUCFLEET | Fleet Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

LOGO_PATH = "logo.png"

RED = "#E61B1F"
WHITE = "#FFFFFF"
BLACK = "#000000"


# =============================================================================
# CSS
# =============================================================================

st.markdown(
    """
<style>
.stApp {
    background:
        radial-gradient(circle at top left, rgba(230, 27, 31, 0.16), transparent 32%),
        radial-gradient(circle at top right, rgba(230, 27, 31, 0.09), transparent 36%),
        radial-gradient(circle at bottom right, rgba(255, 255, 255, 0.035), transparent 25%),
        #000000;
    color: #FFFFFF;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1520px;
    padding-top: 1.25rem;
    padding-bottom: 3rem;
}

/* SIDEBAR — PREMIUM GRAPHITE CONTROL PANEL */
[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #121212 0%, #080808 52%, #030303 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.075);
    box-shadow:
        18px 0 50px rgba(0,0,0,0.52),
        inset -1px 0 0 rgba(230,27,31,0.18);
}

[data-testid="stSidebar"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 21rem;
    height: 100vh;
    pointer-events: none;
    background:
        radial-gradient(circle at 50% 0%, rgba(230,27,31,0.13), transparent 28%),
        radial-gradient(circle at 10% 35%, rgba(255,255,255,0.035), transparent 24%);
    z-index: 0;
}

[data-testid="stSidebar"] > div {
    position: relative;
    z-index: 2;
}

[data-testid="stSidebar"] * {
    color: #F5F5F5 !important;
}

[data-testid="stSidebar"] img {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    box-shadow: none !important;
    margin-bottom: 18px;
}

[data-testid="stSidebar"] label {
    color: rgba(255,255,255,0.58) !important;
    font-weight: 850 !important;
    letter-spacing: 0.085em !important;
    text-transform: uppercase;
    font-size: 0.69rem !important;
    margin-bottom: 4px !important;
}

[data-testid="stSidebar"] input {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    background-color: transparent !important;
}

[data-testid="stSidebar"] [data-baseweb="input"] > div,
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background:
        linear-gradient(145deg, rgba(255,255,255,0.075), rgba(255,255,255,0.025)) !important;
    border: 1px solid rgba(255,255,255,0.105) !important;
    border-radius: 16px !important;
    min-height: 45px !important;
    box-shadow:
        inset 0 0 0 1px rgba(255,255,255,0.025),
        0 10px 24px rgba(0,0,0,0.20);
}

[data-testid="stSidebar"] [data-baseweb="input"] > div:focus-within,
[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
    border: 1px solid rgba(230,27,31,0.55) !important;
    box-shadow:
        0 0 0 2px rgba(230,27,31,0.12),
        0 10px 24px rgba(0,0,0,0.25);
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: rgba(255,255,255,0.74) !important;
    color: rgba(255,255,255,0.74) !important;
}

[data-baseweb="popover"] {
    background-color: #080808 !important;
}

[data-baseweb="menu"] {
    background:
        linear-gradient(180deg, #111111, #050505) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 14px !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.55);
}

[data-baseweb="menu"] li,
[data-baseweb="menu"] div {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    background-color: transparent !important;
}

[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] div:hover {
    background: rgba(230, 27, 31, 0.16) !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Sidebar buttons — less aggressive, more professional */
[data-testid="stSidebar"] .stButton > button {
    background:
        linear-gradient(135deg, rgba(255,255,255,0.105), rgba(255,255,255,0.035)) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 16px !important;
    min-height: 45px !important;
    font-weight: 900 !important;
    letter-spacing: 0.045em !important;
    box-shadow:
        0 12px 28px rgba(0,0,0,0.28),
        inset 0 0 0 1px rgba(255,255,255,0.025);
    transition: all 0.18s ease-in-out;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background:
        linear-gradient(135deg, rgba(230,27,31,0.30), rgba(95,18,20,0.28)) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(230,27,31,0.42) !important;
    transform: translateY(-1px);
    box-shadow:
        0 16px 34px rgba(0,0,0,0.35),
        0 0 22px rgba(230,27,31,0.10);
}

/* First sidebar button = Login */
[data-testid="stSidebar"] .stButton:first-of-type > button {
    background:
        linear-gradient(135deg, rgba(230,27,31,0.22), rgba(90,16,18,0.22)) !important;
    border: 1px solid rgba(230,27,31,0.35) !important;
}

/* Brand / cards */
.sidebar-brand-card {
    background:
        linear-gradient(145deg, rgba(255,255,255,0.070), rgba(255,255,255,0.022));
    border: 1px solid rgba(255,255,255,0.095);
    border-radius: 22px;
    padding: 16px;
    margin-bottom: 15px;
    box-shadow:
        0 18px 42px rgba(0,0,0,0.34),
        inset 0 0 0 1px rgba(255,255,255,0.022);
    position: relative;
    overflow: hidden;
}

.sidebar-brand-card::after {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 90px;
    height: 90px;
    background: radial-gradient(circle, rgba(230,27,31,0.13), transparent 67%);
    pointer-events: none;
}

.sidebar-brand-title {
    color: #FFFFFF !important;
    font-size: 1.24rem;
    font-weight: 950;
    letter-spacing: -0.035em;
    margin-top: 2px;
    margin-bottom: 5px;
}

.sidebar-brand-subtitle {
    color: rgba(255,255,255,0.56) !important;
    font-size: 0.75rem;
    line-height: 1.48;
}

.sidebar-section-title {
    color: rgba(255,255,255,0.46) !important;
    font-size: 0.66rem;
    font-weight: 950;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin: 18px 0 8px 2px;
}

.sidebar-section-title::before {
    content: "";
    display: inline-block;
    width: 7px;
    height: 7px;
    background: #E61B1F;
    border-radius: 999px;
    margin-right: 8px;
    box-shadow: 0 0 12px rgba(230,27,31,0.55);
}

.sidebar-box {
    background:
        linear-gradient(145deg, rgba(255,255,255,0.060), rgba(255,255,255,0.020));
    border: 1px solid rgba(255,255,255,0.085);
    border-radius: 18px;
    padding: 14px;
    margin-top: 12px;
    box-shadow:
        0 14px 32px rgba(0,0,0,0.25),
        inset 0 0 0 1px rgba(255,255,255,0.018);
    position: relative;
    overflow: hidden;
}

.sidebar-box::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 3px;
    height: 100%;
    background: linear-gradient(180deg, rgba(230,27,31,0.86), rgba(230,27,31,0.16));
}

.sidebar-title {
    color: rgba(255,255,255,0.92) !important;
    font-size: 0.70rem;
    font-weight: 950;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.sidebar-row {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.065);
    font-size: 0.80rem;
}

.sidebar-row:last-child {
    border-bottom: none;
}

.sidebar-row span {
    color: rgba(255,255,255,0.50) !important;
}

.sidebar-row strong {
    color: rgba(255,255,255,0.92) !important;
    font-weight: 850;
    text-align: right;
}

.sidebar-mini-pill {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(255,255,255,0.055);
    color: rgba(255,255,255,0.78) !important;
    border: 1px solid rgba(255,255,255,0.09);
    font-size: 0.64rem;
    font-weight: 900;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    margin-top: 10px;
}

.sidebar-red-pill {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(230,27,31,0.13);
    color: rgba(255,255,255,0.88) !important;
    border: 1px solid rgba(230,27,31,0.25);
    font-size: 0.64rem;
    font-weight: 900;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    margin-top: 10px;
}

/* MAIN UI */
h1, h2, h3, h4, h5, h6, p, span, label {
    color: #FFFFFF;
}

.hero {
    background:
        radial-gradient(circle at top right, rgba(230, 27, 31, 0.26), transparent 36%),
        radial-gradient(circle at bottom left, rgba(255,255,255,0.04), transparent 34%),
        linear-gradient(135deg, rgba(10,10,10,0.99), rgba(0,0,0,0.97));
    border: 1px solid rgba(230, 27, 31, 0.34);
    border-radius: 30px;
    padding: 38px;
    box-shadow: 0 28px 90px rgba(0,0,0,0.68);
    margin-bottom: 24px;
}

.hero-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.6fr) minmax(280px, 0.75fr);
    gap: 26px;
    align-items: center;
}

.brand-kicker {
    color: #E61B1F;
    font-size: 0.76rem;
    font-weight: 950;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-bottom: 9px;
}

.brand-title {
    color: #FFFFFF;
    font-size: 3.35rem;
    font-weight: 950;
    letter-spacing: -0.065em;
    line-height: 1.0;
    margin-bottom: 13px;
}

.brand-title-small {
    color: #FFFFFF;
    font-size: 2.55rem;
    font-weight: 950;
    letter-spacing: -0.055em;
    line-height: 1.0;
    margin-bottom: 10px;
}

.brand-subtitle {
    color: rgba(255,255,255,0.76);
    font-size: 1.02rem;
    line-height: 1.65;
    max-width: 1000px;
}

.hero-panel {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 22px;
    padding: 20px;
}

.app-shell {
    background:
        radial-gradient(circle at top right, rgba(230, 27, 31, 0.16), transparent 35%),
        linear-gradient(135deg, rgba(10,10,10,0.98), rgba(0,0,0,0.96));
    border: 1px solid rgba(230, 27, 31, 0.28);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 20px 70px rgba(0,0,0,0.55);
    margin-bottom: 22px;
}

.top-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    margin-bottom: 18px;
}

.header-side {
    min-width: 280px;
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(230, 27, 31, 0.24);
    border-radius: 18px;
    padding: 16px;
}

.soft-label {
    color: rgba(255,255,255,0.58);
    font-size: 0.72rem;
    font-weight: 850;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.soft-value {
    color: #FFFFFF;
    font-size: 1rem;
    font-weight: 900;
}

.premium-card {
    background: linear-gradient(145deg, rgba(8,8,8,0.98), rgba(18,18,18,0.94));
    border: 1px solid rgba(230, 27, 31, 0.22);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 12px 34px rgba(0,0,0,0.35);
    margin-bottom: 16px;
}

.premium-card-red {
    background:
        radial-gradient(circle at top right, rgba(230, 27, 31, 0.20), transparent 36%),
        linear-gradient(145deg, rgba(8,8,8,0.99), rgba(18,18,18,0.95));
    border: 1px solid rgba(230, 27, 31, 0.40);
    border-left: 4px solid #E61B1F;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 12px 38px rgba(230,27,31,0.10);
    margin-bottom: 16px;
}

.upgrade-card {
    background:
        radial-gradient(circle at top right, rgba(230, 27, 31, 0.18), transparent 36%),
        linear-gradient(145deg, rgba(15,15,15,0.99), rgba(5,5,5,0.96));
    border: 1px dashed rgba(230, 27, 31, 0.58);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 12px 38px rgba(230,27,31,0.10);
    margin-bottom: 16px;
}

.card-title {
    color: #FFFFFF;
    font-size: 0.98rem;
    font-weight: 900;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.card-text {
    color: rgba(255,255,255,0.74);
    font-size: 0.92rem;
    line-height: 1.58;
}

.metric-card {
    background:
        radial-gradient(circle at top right, rgba(230, 27, 31, 0.18), transparent 38%),
        linear-gradient(145deg, rgba(7,7,7,0.99), rgba(18,18,18,0.96));
    border: 1px solid rgba(230, 27, 31, 0.24);
    border-left: 4px solid #E61B1F;
    border-radius: 16px;
    padding: 16px 18px;
    min-height: 124px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
    margin-bottom: 12px;
}

.metric-label {
    color: rgba(255,255,255,0.68);
    font-size: 0.74rem;
    font-weight: 850;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.metric-value {
    color: #FFFFFF;
    font-size: 2rem;
    font-weight: 950;
    letter-spacing: -0.04em;
    line-height: 1.0;
    margin-bottom: 8px;
}

.metric-detail {
    color: rgba(255,255,255,0.68);
    font-size: 0.78rem;
    font-weight: 650;
}

.status-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    color: #FFFFFF;
    font-size: 0.90rem;
}

.status-row span {
    color: rgba(255,255,255,0.70);
}

.status-row strong {
    color: #FFFFFF;
    font-weight: 850;
}

.pill {
    display: inline-block;
    padding: 7px 11px;
    border-radius: 999px;
    background: rgba(230, 27, 31, 0.14);
    color: #FFFFFF;
    border: 1px solid rgba(230, 27, 31, 0.36);
    font-size: 0.72rem;
    font-weight: 900;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    margin-bottom: 12px;
    margin-right: 6px;
}

.pill-white {
    display: inline-block;
    padding: 7px 11px;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    color: #FFFFFF;
    border: 1px solid rgba(255,255,255,0.18);
    font-size: 0.72rem;
    font-weight: 900;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    margin-right: 6px;
    margin-bottom: 12px;
}

.feature-list {
    color: rgba(255,255,255,0.76);
    font-size: 0.90rem;
    line-height: 1.72;
    margin-top: 8px;
}

.terminal-log {
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
    font-size: 0.78rem;
    color: #FFFFFF;
    background: #050505;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid rgba(230, 27, 31, 0.26);
    height: 330px;
    overflow-y: hidden;
    line-height: 1.55;
}

.log-time { color: rgba(255,255,255,0.48); margin-right: 8px; }
.log-warning { color: #E61B1F; }
.log-error { color: #E61B1F; font-weight: 900; }
.log-success { color: #FFFFFF; font-weight: 750; }

div[data-testid="stMetric"] {
    background:
        radial-gradient(circle at top right, rgba(230, 27, 31, 0.16), transparent 40%),
        linear-gradient(145deg, rgba(8, 8, 8, 0.98), rgba(18, 18, 18, 0.96));
    border: 1px solid rgba(230, 27, 31, 0.22);
    border-left: 4px solid #E61B1F;
    border-radius: 15px;
    padding: 14px 16px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.30);
}

div[data-testid="stMetric"] label {
    color: rgba(255,255,255,0.70) !important;
    font-weight: 850 !important;
    letter-spacing: 0.03em;
}

div[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: 950 !important;
}

div[data-testid="stMetricDelta"] {
    color: #FFFFFF !important;
}

.stButton > button {
    border-radius: 13px;
    font-weight: 900;
    letter-spacing: 0.04em;
    background-color: #E61B1F !important;
    color: white !important;
    border: 1px solid #E61B1F !important;
    min-height: 44px;
}

.stButton > button:hover {
    background-color: #FFFFFF !important;
    color: #E61B1F !important;
    border: 1px solid #FFFFFF !important;
}

.stTabs [data-baseweb="tab"] {
    color: white !important;
    font-weight: 850;
    letter-spacing: 0.03em;
}

.stTabs [aria-selected="true"] {
    color: #E61B1F !important;
}

div[data-testid="stDataFrame"] {
    border: 1px solid rgba(230, 27, 31, 0.24);
    border-radius: 14px;
    overflow: hidden;
}

@media (max-width: 900px) {
    .hero-grid {
        grid-template-columns: 1fr;
    }

    .top-header {
        flex-direction: column;
        align-items: stretch;
    }

    .brand-title {
        font-size: 2.4rem;
    }
}
</style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# DATA
# =============================================================================

VEHICLE_OPTIONS = [
    "FX-8801 (Heavy Haul)",
    "FX-8802 (Transit)",
    "FX-8803 (Logistics)",
]

vehicle_specs = {
    "FX-8801": {
        "type": "Heavy Haul",
        "driver": "Driver A",
        "monthly_liters": 1250,
        "avg_consumption": 31.5,
        "tank_capacity": 420,
        "monthly_km": 3970,
        "fuel_reduction": 12.4,
        "health": 91.2,
        "safety": 94.8,
    },
    "FX-8802": {
        "type": "Transit",
        "driver": "Driver B",
        "monthly_liters": 720,
        "avg_consumption": 18.8,
        "tank_capacity": 260,
        "monthly_km": 3830,
        "fuel_reduction": 14.1,
        "health": 96.1,
        "safety": 92.5,
    },
    "FX-8803": {
        "type": "Logistics",
        "driver": "Driver C",
        "monthly_liters": 940,
        "avg_consumption": 24.6,
        "tank_capacity": 320,
        "monthly_km": 3820,
        "fuel_reduction": 10.8,
        "health": 87.9,
        "safety": 88.4,
    },
}

plans_personal = {
    "Personal Basic": {
        "price": 4.90,
        "description": "GPS tracking, route history, basic vehicle data and movement alerts.",
        "best_for": "Everyday drivers",
        "features": ["GPS tracking", "Route history", "Movement alerts"],
    },
    "Personal Pro": {
        "price": 9.90,
        "description": "Basic + OBD/CAN data, fault codes, battery voltage, engine temperature and maintenance reminders.",
        "best_for": "Car owners who want diagnostics",
        "features": ["Everything in Basic", "OBD/CAN data", "Fault codes", "Maintenance reminders"],
    },
    "Personal Premium": {
        "price": 14.90,
        "description": "Pro + advanced driving analytics, fuel estimation, export reports and extended data history.",
        "best_for": "Power users and enthusiasts",
        "features": ["Everything in Pro", "Fuel intelligence", "Driving analytics", "Reports"],
    },
}

plans_fleet = {
    "Fleet Basic": {
        "price": 249,
        "vehicles": 30,
        "description": "GPS tracking, 30-day route history and basic fleet reports.",
        "best_for": "Small fleets",
        "features": ["Fleet GPS", "30-day route history", "Basic reports"],
    },
    "Fleet Pro": {
        "price": 399,
        "vehicles": 50,
        "description": "GPS, OBD/CAN data, fault codes, fuel estimation, maintenance alerts and 6-month history.",
        "best_for": "Growing companies",
        "features": ["Everything in Basic", "OBD/CAN data", "Maintenance alerts", "Fuel intelligence"],
    },
    "Fleet Enterprise": {
        "price": 699,
        "vehicles": 100,
        "description": "Pro + advanced analytics, API access, custom reports and priority support.",
        "best_for": "Large fleet operators",
        "features": ["Everything in Pro", "API access", "Custom reports", "Priority support"],
    },
}

plan_features = {
    "Personal Basic": ["gps", "history", "movement_alerts"],
    "Personal Pro": ["gps", "history", "movement_alerts", "obd", "fault_codes", "maintenance"],
    "Personal Premium": [
        "gps",
        "history",
        "movement_alerts",
        "obd",
        "fault_codes",
        "maintenance",
        "analytics",
        "reports",
        "fuel",
    ],
    "Fleet Basic": ["fleet_gps", "history", "basic_reports"],
    "Fleet Pro": ["fleet_gps", "history", "basic_reports", "obd", "maintenance", "fuel", "reports"],
    "Fleet Enterprise": [
        "fleet_gps",
        "history",
        "basic_reports",
        "obd",
        "maintenance",
        "fuel",
        "reports",
        "api",
        "custom_reports",
        "priority_support",
        "admin_tools",
    ],
    "Admin": [
        "fleet_gps",
        "history",
        "basic_reports",
        "obd",
        "maintenance",
        "fuel",
        "reports",
        "api",
        "custom_reports",
        "priority_support",
        "admin_tools",
        "revenue",
        "users",
        "devices",
    ],
}

hardware_price = 129
hardware_cost_low = 60
hardware_cost_high = 70

diesel_price_base = 1.64
diesel_price_day_low = 1.58
diesel_price_alert_threshold = 1.59

time_points = np.arange(0, 50, 1)
rpm_base = 2300 + np.sin(time_points / 5) * 600
speed_base = 65 + np.cos(time_points / 8) * 15
fuel_base = 8.9 - np.sin(time_points / 9) * 0.35
fuel_reduction_base = 12.4 + np.sin(time_points / 7) * 1.1

categories = [
    "Braking Smoothness",
    "Cornering",
    "Speed Compliance",
    "Acceleration",
    "Lane Discipline",
]

route_waypoints = [
    (37.77490, -122.41940),
    (37.77380, -122.41830),
    (37.77230, -122.41680),
    (37.77060, -122.41500),
    (37.76880, -122.41300),
    (37.76710, -122.41110),
    (37.76520, -122.40940),
    (37.76320, -122.40760),
    (37.76100, -122.40590),
    (37.75850, -122.40400),
    (37.75580, -122.40200),
    (37.75310, -122.40010),
    (37.75020, -122.39810),
    (37.74730, -122.39620),
    (37.74420, -122.39420),
    (37.74100, -122.39210),
    (37.73780, -122.39000),
    (37.73460, -122.38790),
    (37.73130, -122.38570),
    (37.72800, -122.38350),
    (37.72460, -122.38130),
    (37.72130, -122.37910),
    (37.71780, -122.37690),
    (37.71420, -122.37480),
    (37.71060, -122.37270),
    (37.70680, -122.37050),
    (37.70290, -122.36830),
    (37.69900, -122.36630),
    (37.69500, -122.36430),
    (37.69080, -122.36230),
    (37.68640, -122.36030),
    (37.68200, -122.35850),
    (37.67740, -122.35680),
    (37.67280, -122.35510),
    (37.66800, -122.35350),
    (37.66300, -122.35230),
    (37.65700, -122.35110),
    (37.65000, -122.35000),
]


# =============================================================================
# SESSION STATE
# =============================================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = "demo@tucfleet.com"

if "user_role" not in st.session_state:
    st.session_state.user_role = "Fleet Manager"

if "user_plan" not in st.session_state:
    st.session_state.user_plan = "Fleet Pro"

if "selected_vehicle" not in st.session_state:
    st.session_state.selected_vehicle = VEHICLE_OPTIONS[0]


# =============================================================================
# HELPERS
# =============================================================================

def interpolate_route(waypoints, points_per_segment=4):
    route_points = []

    for i in range(len(waypoints) - 1):
        lat1, lon1 = waypoints[i]
        lat2, lon2 = waypoints[i + 1]

        for t in np.linspace(0, 1, points_per_segment, endpoint=False):
            lat = lat1 + (lat2 - lat1) * t
            lon = lon1 + (lon2 - lon1) * t
            route_points.append((lat, lon))

    route_points.append(waypoints[-1])
    return pd.DataFrame(route_points, columns=["lat", "lon"])


route_data = interpolate_route(route_waypoints, points_per_segment=4)


def get_asset_id():
    return st.session_state.selected_vehicle.split(" ")[0]


def get_profile():
    return vehicle_specs[get_asset_id()]


def current_plan():
    if st.session_state.user_role == "Admin":
        return "Admin"
    return st.session_state.user_plan


def has_feature(feature):
    return feature in plan_features.get(current_plan(), [])


def status_row(label, value):
    return f'<div class="status-row"><span>{label}</span><strong>{value}</strong></div>'


def sidebar_row(label, value):
    return f'<div class="sidebar-row"><span>{label}</span><strong>{value}</strong></div>'


def metric_card(label, value, detail):
    return f"""
<div class="metric-card">
<div class="metric-label">{label}</div>
<div class="metric-value">{value}</div>
<div class="metric-detail">{detail}</div>
</div>
"""


def premium_card(title, text):
    return f"""
<div class="premium-card">
<div class="card-title">{title}</div>
<div class="card-text">{text}</div>
</div>
"""


def plan_card(title, price, description, best_for, type_label, features=None):
    features = features or []
    feature_html = "".join([f"✓ {feature}<br>" for feature in features])

    return f"""
<div class="premium-card-red">
<span class="pill">{type_label}</span>
<div class="card-title">{title}</div>
<div class="metric-value">{price}</div>
<div class="card-text">{description}</div>
<div class="feature-list">{feature_html}</div>
<br>
{status_row("Best for", best_for)}
</div>
"""


def upgrade_card(feature_name, required_plan, description):
    st.markdown(
        f"""
<div class="upgrade-card">
<span class="pill">Upgrade Required</span>
<div class="card-title">{feature_name} Locked</div>
<div class="card-text">
{description}
<br><br>
Current plan: <strong>{current_plan()}</strong><br>
Required plan: <strong>{required_plan}</strong>
</div>
</div>
        """,
        unsafe_allow_html=True,
    )


def current_diesel_price(iteration=0, live=False):
    if live:
        price = diesel_price_base + np.sin(iteration / 8) * 0.045 + np.random.uniform(-0.012, 0.012)
    else:
        price = diesel_price_base

    return max(1.50, min(1.78, price))


def fuel_calculations(price):
    profile = get_profile()

    monthly_liters = profile["monthly_liters"]
    avg_consumption = profile["avg_consumption"]
    tank_capacity = profile["tank_capacity"]
    monthly_km = profile["monthly_km"]
    reduction = profile["fuel_reduction"]

    liters_saved = monthly_liters * reduction / 100
    money_saved_month = liters_saved * price
    annual_saving = money_saved_month * 12

    full_tank_now = tank_capacity * price
    full_tank_low = tank_capacity * diesel_price_day_low
    tank_saving = max(0, full_tank_now - full_tank_low)

    cost_100_now = avg_consumption * price
    cost_100_optimized = cost_100_now * (1 - reduction / 100)

    return {
        "monthly_liters": monthly_liters,
        "avg_consumption": avg_consumption,
        "tank_capacity": tank_capacity,
        "monthly_km": monthly_km,
        "reduction": reduction,
        "liters_saved": liters_saved,
        "money_saved_month": money_saved_month,
        "annual_saving": annual_saving,
        "full_tank_now": full_tank_now,
        "tank_saving": tank_saving,
        "cost_100_now": cost_100_now,
        "cost_100_optimized": cost_100_optimized,
    }


def render_header(title, subtitle):
    profile = get_profile()
    price = current_diesel_price(live=False)
    fuel = fuel_calculations(price)

    user_status = "Authenticated" if st.session_state.logged_in else "Guest"

    st.markdown(
        f"""
<div class="app-shell">
<div class="top-header">
<div>
<div class="brand-kicker">{title}</div>
<div class="brand-title-small">TUCFLEET</div>
<div class="brand-subtitle">{subtitle}</div>
</div>
<div class="header-side">
<div class="soft-label">User Session</div>
<div class="soft-value">{user_status} · {st.session_state.user_role}</div>
<br>
<div class="soft-label">Active Plan</div>
<div class="soft-value">{current_plan()}</div>
<br>
<div class="soft-label">Selected Asset</div>
<div class="soft-value">{get_asset_id()} · {profile["type"]}</div>
<br>
<div class="soft-label">Estimated Monthly Saving</div>
<div class="soft-value">{fuel["money_saved_month"]:.0f} €</div>
</div>
</div>
<span class="pill">Investor Demo</span>
<span class="pill-white">Plan-Based UI</span>
<span class="pill-white">Cloud Sync Active</span>
</div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# CHARTS
# =============================================================================

def render_telemetry_chart(target, iteration=0, live=False):
    if live:
        rpm = np.roll(rpm_base, -iteration) + np.random.randn(50) * 40
        speed = np.roll(speed_base, -iteration) + np.random.randn(50) * 2
        fuel_use = np.roll(fuel_base, -iteration) + np.random.randn(50) * 0.04
    else:
        rpm = rpm_base
        speed = speed_base
        fuel_use = fuel_base

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=rpm,
            name="Engine RPM",
            fill="tozeroy",
            line=dict(color=RED, width=3, shape="spline"),
            fillcolor="rgba(230,27,31,0.14)",
        )
    )

    fig.add_trace(
        go.Scatter(
            y=speed * 35,
            name="Speed Scaled",
            line=dict(color=WHITE, width=3, shape="spline"),
        )
    )

    fig.add_trace(
        go.Scatter(
            y=fuel_use * 250,
            name="Fuel Use Scaled",
            line=dict(color=RED, width=2, dash="dot", shape="spline"),
        )
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=WHITE),
        margin=dict(l=0, r=0, t=8, b=0),
        height=360,
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.10)"),
        xaxis=dict(showgrid=False, showticklabels=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    target.plotly_chart(fig, use_container_width=True, key=f"telemetry_{iteration}_{live}_{id(target)}")


def render_fuel_chart(target, iteration=0, live=False):
    profile = get_profile()

    if live:
        reduction = np.roll(fuel_reduction_base, -iteration) + np.random.randn(50) * 0.2
        liters_100 = profile["avg_consumption"] + np.sin(time_points / 8 + iteration / 10) * 1.2
        diesel_price_line = diesel_price_base + np.sin((time_points + iteration) / 8) * 0.045
    else:
        reduction = fuel_reduction_base
        liters_100 = profile["avg_consumption"] + np.sin(time_points / 8) * 1.2
        diesel_price_line = diesel_price_base + np.sin(time_points / 8) * 0.045

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=reduction,
            name="Fuel Reduction %",
            line=dict(color=RED, width=4, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(230,27,31,0.16)",
        )
    )

    fig.add_trace(
        go.Scatter(
            y=liters_100,
            name="L / 100km",
            line=dict(color=WHITE, width=3, shape="spline"),
        )
    )

    fig.add_trace(
        go.Scatter(
            y=diesel_price_line * 10,
            name="Diesel Price x10",
            line=dict(color=WHITE, width=2, dash="dash", shape="spline"),
        )
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=WHITE),
        margin=dict(l=0, r=0, t=8, b=0),
        height=360,
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.10)"),
        xaxis=dict(showgrid=False, showticklabels=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    target.plotly_chart(fig, use_container_width=True, key=f"fuel_{iteration}_{live}_{id(target)}")


def render_radar(target, iteration=0, live=False):
    if live:
        radar_vals = [
            95 + np.random.randint(-3, 3),
            88 + np.random.randint(-2, 2),
            92 + np.random.randint(-2, 2),
            85 + np.random.randint(-5, 5),
            98 + np.random.randint(-2, 1),
        ]
    else:
        radar_vals = [95, 88, 92, 85, 98]

    fig = go.Figure(
        data=go.Scatterpolar(
            r=radar_vals,
            theta=categories,
            fill="toself",
            line=dict(color=RED, width=3),
            fillcolor="rgba(230,27,31,0.28)",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(255,255,255,0.12)",
                tickfont=dict(color=WHITE),
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.12)",
                tickfont=dict(color=WHITE),
            ),
        ),
        showlegend=False,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=WHITE),
        margin=dict(l=30, r=30, t=20, b=20),
        height=360,
    )

    target.plotly_chart(fig, use_container_width=True, key=f"radar_{iteration}_{live}_{id(target)}")


def render_map(target, iteration=0, live=False):
    idx = min(iteration, len(route_data) - 1)

    full_route = route_data[["lon", "lat"]].values.tolist()
    past_route = route_data.iloc[: idx + 1][["lon", "lat"]].values.tolist()

    start = route_data.iloc[0]
    current = route_data.iloc[idx]
    end = route_data.iloc[-1]

    marker_data = pd.DataFrame(
        [
            {
                "lon": start["lon"],
                "lat": start["lat"],
                "label": "Start",
                "color": [255, 255, 255, 220],
                "radius": 90,
            },
            {
                "lon": current["lon"],
                "lat": current["lat"],
                "label": "Current Vehicle",
                "color": [230, 27, 31, 245],
                "radius": 145,
            },
            {
                "lon": end["lon"],
                "lat": end["lat"],
                "label": "Destination",
                "color": [34, 197, 94, 235],
                "radius": 100,
            },
        ]
    )

    layers = [
        pdk.Layer(
            "PathLayer",
            data=[{"path": full_route}],
            get_path="path",
            get_color=[100, 100, 100, 140],
            width_scale=20,
            width_min_pixels=3,
        ),
        pdk.Layer(
            "PathLayer",
            data=[{"path": past_route}],
            get_path="path",
            get_color=[230, 27, 31, 230],
            width_scale=20,
            width_min_pixels=5,
        ),
        pdk.Layer(
            "ScatterplotLayer",
            data=marker_data,
            get_position="[lon, lat]",
            get_fill_color="color",
            get_radius="radius",
            pickable=True,
        ),
    ]

    if live:
        center_lat = current["lat"]
        center_lon = current["lon"]
        zoom = 12
    else:
        center_lat = route_data["lat"].mean()
        center_lon = route_data["lon"].mean()
        zoom = 10.8

    try:
        deck = pdk.Deck(
            map_provider="carto",
            map_style=pdk.map_styles.ROAD,
            initial_view_state=pdk.ViewState(
                latitude=float(center_lat),
                longitude=float(center_lon),
                zoom=zoom,
                pitch=0,
                bearing=0,
            ),
            layers=layers,
            tooltip={
                "html": "<b>{label}</b>",
                "style": {
                    "backgroundColor": "rgba(0,0,0,0.88)",
                    "color": "white",
                    "border": "1px solid #E61B1F",
                },
            },
        )
    except Exception:
        deck = pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=float(center_lat),
                longitude=float(center_lon),
                zoom=zoom,
                pitch=0,
                bearing=0,
            ),
            layers=layers,
        )

    target.pydeck_chart(deck, use_container_width=True)


def render_route_panel(target, iteration=0, live=False):
    idx = min(iteration, len(route_data) - 1)
    progress = idx / (len(route_data) - 1) * 100
    current = route_data.iloc[idx]

    if live:
        speed = max(38, int(64 + np.random.randint(-7, 9)))
        eta = max(4, int((len(route_data) - idx) * 0.25))
        traffic = np.random.choice(["Light", "Normal", "Moderate"], p=[0.25, 0.50, 0.25])
        route_score = 92 + np.random.randint(-2, 3)
    else:
        speed = 0
        eta = 42
        traffic = "Standby"
        route_score = 94

    target.markdown(
        f"""
<div class="premium-card-red">
<div class="card-title">Route Intelligence</div>
{status_row("Vehicle", get_asset_id())}
{status_row("Latitude", f"{current['lat']:.5f}")}
{status_row("Longitude", f"{current['lon']:.5f}")}
{status_row("Progress", f"{progress:.1f}%")}
{status_row("Speed", f"{speed} km/h")}
{status_row("ETA", f"{eta} min")}
{status_row("Traffic", traffic)}
{status_row("Eco Route Score", f"{route_score}/100")}
{status_row("Geofence", "Inside corridor" if live else "Awaiting stream")}
</div>
        """,
        unsafe_allow_html=True,
    )


def render_fuel_intelligence(target, iteration=0, live=False):
    price = current_diesel_price(iteration, live)
    fuel = fuel_calculations(price)

    is_low_price = price <= diesel_price_alert_threshold
    price_distance = price - diesel_price_alert_threshold

    price_x = np.arange(0, 32)
    if live:
        price_y = diesel_price_base + np.sin((price_x + iteration) / 8) * 0.045
    else:
        price_y = diesel_price_base + np.sin(price_x / 8) * 0.045

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=price_x,
            y=price_y,
            mode="lines",
            name="Diesel Price",
            line=dict(color=RED, width=4, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(230,27,31,0.16)",
        )
    )

    fig.add_hline(
        y=diesel_price_alert_threshold,
        line_dash="dash",
        line_color=WHITE,
        annotation_text="Buy threshold",
        annotation_font_color=WHITE,
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=WHITE),
        margin=dict(l=0, r=0, t=10, b=0),
        height=230,
        showlegend=False,
        yaxis=dict(title="€/L", showgrid=True, gridcolor="rgba(255,255,255,0.10)"),
        xaxis=dict(showgrid=False, showticklabels=False),
    )

    with target.container():
        if is_low_price:
            st.success("BUY WINDOW ACTIVE — Diesel price is low. Recommend refuel now.")
        else:
            st.warning(f"MONITORING — {price_distance:.3f} €/L above buy threshold.")

        top1, top2, top3 = st.columns(3)
        top1.metric("Current Diesel Price", f"{price:.3f} €/L", f"Threshold {diesel_price_alert_threshold:.3f}")
        top2.metric("Monthly Saving", f"{fuel['money_saved_month']:.0f} €", f"{fuel['liters_saved']:.0f} L saved")
        top3.metric("Annual Saving", f"{fuel['annual_saving']:.0f} €", f"{fuel['reduction']:.1f}% reduction")

        st.plotly_chart(fig, use_container_width=True, key=f"price_fig_{iteration}_{live}_{id(target)}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Cost / 100km Now", f"{fuel['cost_100_now']:.1f} €")
        c2.metric(
            "Optimized / 100km",
            f"{fuel['cost_100_optimized']:.1f} €",
            f"-{fuel['cost_100_now'] - fuel['cost_100_optimized']:.1f} €",
        )
        c3.metric("Full Tank Now", f"{fuel['full_tank_now']:.0f} €")
        c4.metric("Tank Saving Window", f"{fuel['tank_saving']:.0f} €")

    return is_low_price, price, fuel["money_saved_month"]


# =============================================================================
# PLAN / BUSINESS MODEL
# =============================================================================

def render_plan_calculator(key_prefix="plans"):
    st.markdown(
        """
<div class="premium-card-red">
<div class="card-title">Plans and Business Model</div>
<div class="card-text">
TUCFLEET combines one-time hardware revenue with recurring monthly software revenue.
The model supports individual users and fleet companies.
</div>
</div>
        """,
        unsafe_allow_html=True,
    )

    plan_mode = st.radio(
        "Select customer category",
        ["Personal Users", "Fleet Companies"],
        horizontal=True,
        key=f"{key_prefix}_plan_mode",
    )

    if plan_mode == "Personal Users":
        p1, p2, p3 = st.columns(3)
        personal_items = list(plans_personal.items())

        for col, (name, data) in zip([p1, p2, p3], personal_items):
            with col:
                st.markdown(
                    plan_card(
                        name,
                        f"{data['price']:.2f} €/month",
                        data["description"],
                        data["best_for"],
                        "Personal",
                        data["features"],
                    ),
                    unsafe_allow_html=True,
                )

        st.markdown("---")

        selected_personal_plan = st.selectbox(
            "Choose personal plan",
            list(plans_personal.keys()),
            key=f"{key_prefix}_personal_plan",
        )

        selected_data = plans_personal[selected_personal_plan]
        yearly_software = selected_data["price"] * 12
        first_year_total = hardware_price + yearly_software

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Hardware Price", f"{hardware_price:.0f} €")
        c2.metric("Software / Month", f"{selected_data['price']:.2f} €")
        c3.metric("Software / Year", f"{yearly_software:.0f} €")
        c4.metric("First Year Revenue", f"{first_year_total:.0f} €")

    else:
        f1, f2, f3 = st.columns(3)
        fleet_items = list(plans_fleet.items())

        for col, (name, data) in zip([f1, f2, f3], fleet_items):
            with col:
                st.markdown(
                    plan_card(
                        name,
                        f"{data['price']:.0f} €/month",
                        data["description"],
                        data["best_for"],
                        f"Up to {data['vehicles']} vehicles",
                        data["features"],
                    ),
                    unsafe_allow_html=True,
                )

        st.markdown("---")

        calc_col1, calc_col2, calc_col3 = st.columns(3)

        with calc_col1:
            fleet_vehicles = st.number_input(
                "Number of vehicles",
                min_value=1,
                max_value=300,
                value=40,
                step=1,
                key=f"{key_prefix}_fleet_vehicles",
            )

        with calc_col2:
            selected_fleet_plan = st.selectbox(
                "Fleet plan",
                list(plans_fleet.keys()),
                index=1,
                key=f"{key_prefix}_fleet_plan",
            )

        with calc_col3:
            contract_years = st.number_input(
                "Contract years",
                min_value=1,
                max_value=5,
                value=1,
                step=1,
                key=f"{key_prefix}_contract_years",
            )

        plan_data = plans_fleet[selected_fleet_plan]

        hardware_revenue = fleet_vehicles * hardware_price
        estimated_hardware_cost = fleet_vehicles * ((hardware_cost_low + hardware_cost_high) / 2)
        estimated_hardware_profit = hardware_revenue - estimated_hardware_cost

        software_monthly = plan_data["price"]
        software_yearly = software_monthly * 12
        software_contract_value = software_yearly * contract_years

        first_year_revenue = hardware_revenue + software_yearly
        total_contract_revenue = hardware_revenue + software_contract_value
        recurring_after_year_1 = software_yearly

        if fleet_vehicles <= 30:
            recommendation = "Fleet Basic"
        elif fleet_vehicles <= 50:
            recommendation = "Fleet Pro"
        else:
            recommendation = "Fleet Enterprise"

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Hardware Revenue", f"{hardware_revenue:,.0f} €")
        m2.metric("Software / Year", f"{software_yearly:,.0f} €")
        m3.metric("First Year Revenue", f"{first_year_revenue:,.0f} €")
        m4.metric("Contract Revenue", f"{total_contract_revenue:,.0f} €")

        m5, m6, m7, m8 = st.columns(4)
        m5.metric("Hardware Cost", f"{estimated_hardware_cost:,.0f} €")
        m6.metric("Hardware Profit", f"{estimated_hardware_profit:,.0f} €")
        m7.metric("Recurring After Year 1", f"{recurring_after_year_1:,.0f} €/year")
        m8.metric("Recommended Plan", recommendation)

        st.markdown(
            f"""
<div class="premium-card-red">
<div class="card-title">Example Business Case</div>
<div class="card-text">
For a company with <strong>{fleet_vehicles}</strong> vehicles using
<strong>{selected_fleet_plan}</strong>:
<br><br>
Hardware: {fleet_vehicles} × {hardware_price}€ =
<strong>{hardware_revenue:,.0f}€</strong><br>
Software: {software_monthly}€ × 12 =
<strong>{software_yearly:,.0f}€/year</strong><br>
First-year revenue:
<strong>{first_year_revenue:,.0f}€</strong><br>
Recurring revenue after year one:
<strong>{recurring_after_year_1:,.0f}€/year</strong>
</div>
</div>
            """,
            unsafe_allow_html=True,
        )


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=210)
    else:
        st.markdown(
        """
    <div class="sidebar-brand-card">
    <div class="sidebar-brand-title">Control Center</div>
    <div class="sidebar-brand-subtitle">
    Configure the demo account, subscription tier and live fleet stream.
    </div>
    <span class="sidebar-red-pill">TUCFLEET OS</span>
    </div>
        """,
        unsafe_allow_html=True,
        )

    st.markdown(
        """
<div class="sidebar-brand-card">
<div class="sidebar-brand-title">Mission Control</div>
<div class="sidebar-brand-subtitle">
Select a demo user profile and unlock a plan-based dashboard experience.
</div>
<span class="sidebar-mini-pill">Demo Environment</span>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section-title">Access</div>', unsafe_allow_html=True)

    username_input = st.text_input("Email", value=st.session_state.username)

    role_input = st.selectbox(
        "User Type",
        ["Personal User", "Fleet Manager", "Admin"],
        index=["Personal User", "Fleet Manager", "Admin"].index(st.session_state.user_role),
    )

    if role_input == "Personal User":
        available_plans = list(plans_personal.keys())
        default_plan = st.session_state.user_plan if st.session_state.user_plan in available_plans else "Personal Pro"
    elif role_input == "Fleet Manager":
        available_plans = list(plans_fleet.keys())
        default_plan = st.session_state.user_plan if st.session_state.user_plan in available_plans else "Fleet Pro"
    else:
        available_plans = ["Admin"]
        default_plan = "Admin"

    plan_input = st.selectbox(
        "Plan",
        available_plans,
        index=available_plans.index(default_plan),
    )

    login_col1, login_col2 = st.columns(2)

    with login_col1:
        if st.button("LOGIN", width="stretch"):
            st.session_state.logged_in = True
            st.session_state.username = username_input
            st.session_state.user_role = role_input
            st.session_state.user_plan = plan_input
            st.toast(f"Logged in as {username_input}")
            st.rerun()

    with login_col2:
        if st.button("LOGOUT", width="stretch"):
            st.session_state.logged_in = False
            st.toast("Logged out")
            st.rerun()

    login_status = "Online" if st.session_state.logged_in else "Guest"

    st.markdown(
        f"""
<div class="sidebar-box">
<div class="sidebar-title">Session</div>
{sidebar_row("Status", login_status)}
{sidebar_row("User", st.session_state.username)}
{sidebar_row("Role", st.session_state.user_role)}
{sidebar_row("Plan", current_plan())}
</div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.logged_in:
        st.markdown('<div class="sidebar-section-title">Vehicle</div>', unsafe_allow_html=True)

        st.session_state.selected_vehicle = st.selectbox(
            "Target Asset",
            VEHICLE_OPTIONS,
            index=VEHICLE_OPTIONS.index(st.session_state.selected_vehicle),
        )

        profile = get_profile()

        st.markdown(
            f"""
<div class="sidebar-box">
<div class="sidebar-title">Asset Snapshot</div>
{sidebar_row("Vehicle", get_asset_id())}
{sidebar_row("Type", profile["type"])}
{sidebar_row("Driver", profile["driver"])}
{sidebar_row("Health", f"{profile['health']:.1f}%")}
{sidebar_row("Safety", f"{profile['safety']:.1f}")}
</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sidebar-section-title">Stream</div>', unsafe_allow_html=True)

        run_simulation = st.button(
            "LIVE STREAM",
            width="stretch",
        )

        st.markdown(
            """
<div class="sidebar-box">
<div class="sidebar-title">System Link</div>
<div class="sidebar-row"><span>Gateway</span><strong>Connected</strong></div>
<div class="sidebar-row"><span>Telemetry</span><strong>Ready</strong></div>
<div class="sidebar-row"><span>Latency</span><strong>12 ms</strong></div>
<div class="sidebar-row"><span>Cloud Sync</span><strong>Active</strong></div>
</div>
            """,
            unsafe_allow_html=True,
        )
    else:
        run_simulation = False

        st.markdown(
            """
<div class="sidebar-box">
<div class="sidebar-title">Preview Mode</div>
<div class="sidebar-row"><span>Landing</span><strong>Active</strong></div>
<div class="sidebar-row"><span>Dashboard</span><strong>Locked</strong></div>
<div class="sidebar-row"><span>Login</span><strong>Required</strong></div>
</div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
<div class="sidebar-box">
<div class="sidebar-title">Runtime</div>
{sidebar_row("SYS TIME", datetime.now().strftime("%H:%M:%S"))}
{sidebar_row("Build", "V4.2")}
</div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# LANDING PAGE
# =============================================================================

def render_landing_page():
    hero_html = f"""
<div class="hero">
<div class="hero-grid">
<div>
<div class="brand-kicker">Fleet Intelligence Platform</div>
<div class="brand-title">TUCFLEET</div>
<div class="brand-subtitle">
A connected black-box telemetry and fleet intelligence platform for
GPS tracking, OBD/CAN diagnostics, predictive maintenance, driver behavior,
diesel price monitoring and subscription-based fleet management.
<br><br>
Built for individual users, commercial fleets and operators who need
real-time visibility, lower fuel costs and fewer unexpected breakdowns.
</div>
<br>
<span class="pill">Hardware + SaaS</span>
<span class="pill-white">Personal Users</span>
<span class="pill-white">Fleet Companies</span>
<span class="pill-white">Admin Platform</span>
</div>
<div class="hero-panel">
<div class="card-title">Business Model</div>
<div class="card-text">
Hardware is sold per vehicle. Software is billed monthly as a recurring
subscription. Fleet companies can choose fixed packages for 30, 50 or
100 vehicles.
</div>
<br>
<div class="status-row"><span>Hardware</span><strong>{hardware_price} € / vehicle</strong></div>
<div class="status-row"><span>Fleet Pro</span><strong>399 € / month</strong></div>
<div class="status-row"><span>Personal Pro</span><strong>9.90 € / month</strong></div>
<div class="status-row"><span>Revenue Model</span><strong>Recurring SaaS</strong></div>
</div>
</div>
</div>
"""
    st.markdown(hero_html, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(metric_card("Hardware", "129 €", "Per vehicle device"), unsafe_allow_html=True)
    c2.markdown(metric_card("Fleet Pro", "399 €/mo", "Up to 50 vehicles"), unsafe_allow_html=True)
    c3.markdown(metric_card("Personal Pro", "9.90 €/mo", "Diagnostics plan"), unsafe_allow_html=True)
    c4.markdown(metric_card("Recurring Revenue", "SaaS", "Monthly subscription"), unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(
        """
<div class="premium-card-red">
<div class="card-title">Problem → Solution</div>
<div class="card-text">
Fleets lose money from fuel waste, delayed maintenance, poor driving behavior
and lack of real-time vehicle visibility. TUCFLEET connects each vehicle to
a single intelligence layer where operators can monitor, predict and optimize
fleet operations.
</div>
</div>
        """,
        unsafe_allow_html=True,
    )

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        st.markdown(
            premium_card(
                "Live Telemetry",
                "Stream OBD/CAN data, RPM, speed, battery voltage, engine temperature and vehicle status.",
            ),
            unsafe_allow_html=True,
        )

    with f2:
        st.markdown(
            premium_card(
                "Predictive Maintenance",
                "Detect fault codes, service windows and vehicle health risk before breakdowns happen.",
            ),
            unsafe_allow_html=True,
        )

    with f3:
        st.markdown(
            premium_card(
                "Fuel Intelligence",
                "Estimate monthly savings, detect diesel price windows and optimize refueling decisions.",
            ),
            unsafe_allow_html=True,
        )

    with f4:
        st.markdown(
            premium_card(
                "Fleet Reports",
                "Generate operational reports for safety, maintenance, fuel use and vehicle utilization.",
            ),
            unsafe_allow_html=True,
        )

    st.markdown("---")

    render_plan_calculator(key_prefix="landing")


# =============================================================================
# PERSONAL DASHBOARD
# =============================================================================

def render_personal_dashboard():
    render_header(
        "Personal Vehicle Intelligence",
        "A simplified dashboard for individual users with plan-based access to GPS, diagnostics, fuel insights and driving analytics.",
    )

    profile = get_profile()
    price = current_diesel_price()
    fuel = fuel_calculations(price)

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(metric_card("My Vehicle", get_asset_id(), profile["type"]), unsafe_allow_html=True)
    k2.markdown(metric_card("Driving Score", f"{profile['safety']:.1f}", "Personal score"), unsafe_allow_html=True)
    k3.markdown(metric_card("Health", f"{profile['health']:.1f}%", "Vehicle condition"), unsafe_allow_html=True)
    k4.markdown(metric_card("Plan", current_plan(), "Active subscription"), unsafe_allow_html=True)

    tabs = st.tabs(["MY VEHICLE", "GPS", "DIAGNOSTICS", "FUEL", "REPORTS", "PLAN"])

    with tabs[0]:
        c1, c2 = st.columns([1, 1])

        with c1:
            st.markdown(
                f"""
<div class="premium-card-red">
<div class="card-title">My Vehicle</div>
{status_row("Vehicle ID", get_asset_id())}
{status_row("Vehicle Type", profile["type"])}
{status_row("Monthly Distance", f"{profile['monthly_km']:,} km")}
{status_row("Average Consumption", f"{profile['avg_consumption']:.1f} L/100km")}
{status_row("Current Plan", current_plan())}
</div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            st.metric("Estimated Monthly Fuel Saving", f"{fuel['money_saved_month']:.0f} €")
            st.metric("Annual Fuel Saving", f"{fuel['annual_saving']:.0f} €")
            st.metric("Cost / 100km", f"{fuel['cost_100_now']:.1f} €")

    with tabs[1]:
        if has_feature("gps"):
            map_box = st.empty()
            render_map(map_box, live=False)
        else:
            upgrade_card(
                "GPS Tracking",
                "Personal Basic",
                "View your vehicle location, route history and basic movement alerts.",
            )

    with tabs[2]:
        if has_feature("obd"):
            c1, c2 = st.columns([1.2, 1])

            with c1:
                telemetry_box = st.empty()
                render_telemetry_chart(telemetry_box, live=False)

            with c2:
                st.markdown(
                    f"""
<div class="premium-card-red">
<div class="card-title">Diagnostics</div>
{status_row("Fault Codes", "0 active")}
{status_row("Battery Voltage", "12.7 V")}
{status_row("Engine Temp", "89 °C")}
{status_row("Maintenance", "Due in 18 days")}
</div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            upgrade_card(
                "OBD/CAN Diagnostics",
                "Personal Pro",
                "Unlock vehicle diagnostics, fault codes, battery voltage, engine temperature and maintenance reminders.",
            )

    with tabs[3]:
        if has_feature("fuel"):
            fuel_box = st.empty()
            render_fuel_intelligence(fuel_box, live=False)
        else:
            upgrade_card(
                "Fuel Intelligence",
                "Personal Premium",
                "Unlock diesel price monitoring, fuel saving estimates and refuel recommendations.",
            )

    with tabs[4]:
        if has_feature("reports"):
            report_data = pd.DataFrame(
                [
                    ["Fuel saved", "155 L/month", "Based on estimated reduction"],
                    ["Driving score", f"{profile['safety']:.1f}/100", "Personal score"],
                    ["Maintenance", "18 days", "Next reminder"],
                    ["Route history", "30 days", "Available"],
                ],
                columns=["Metric", "Value", "Notes"],
            )
            st.dataframe(report_data, use_container_width=True, hide_index=True)
        else:
            upgrade_card(
                "Personal Reports",
                "Personal Premium",
                "Unlock exportable reports for fuel, driving score and maintenance history.",
            )

    with tabs[5]:
        st.markdown(
            f"""
<div class="premium-card-red">
<div class="card-title">Current Subscription</div>
{status_row("User", st.session_state.username)}
{status_row("Role", st.session_state.user_role)}
{status_row("Plan", current_plan())}
{status_row("Hardware", f"{hardware_price} € / vehicle")}
</div>
            """,
            unsafe_allow_html=True,
        )
        render_plan_calculator(key_prefix="personal")


# =============================================================================
# FLEET DASHBOARD
# =============================================================================

def render_fleet_dashboard():
    render_header(
        "Fleet Manager Dashboard",
        "Full fleet monitoring with plan-based access to GPS, OBD/CAN telemetry, predictive maintenance, fuel intelligence and reports.",
    )

    profile = get_profile()
    price = current_diesel_price()
    fuel = fuel_calculations(price)

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.markdown(metric_card("Fleet Units", "48 / 50", "96% online"), unsafe_allow_html=True)
    k2.markdown(metric_card("Safety Index", f"{profile['safety']:.1f}", "Driver behavior"), unsafe_allow_html=True)
    k3.markdown(metric_card("Health", f"{profile['health']:.1f}%", "Predictive model"), unsafe_allow_html=True)
    k4.markdown(metric_card("Fuel Saving", f"{fuel['money_saved_month']:.0f} €", "Monthly estimate"), unsafe_allow_html=True)
    k5.markdown(metric_card("Diesel Price", f"{price:.3f} €/L", "Market monitor"), unsafe_allow_html=True)
    k6.markdown(metric_card("Plan", current_plan(), "Fleet subscription"), unsafe_allow_html=True)

    maintenance_tab, fuel_tab, reports_tab, overview_tab, live_tab, map_tab, enterprise_tab, plan_tab = st.tabs(
        [
            "MAINTENANCE",
            "FUEL",
            "REPORTS",
            "OVERVIEW",
            "LIVE TELEMETRY",
            "MAP INTELLIGENCE",
            "ENTERPRISE",
            "PLAN",
        ]
    )

    with maintenance_tab:
        if has_feature("maintenance"):
            m1, m2 = st.columns([1.2, 1])

            radar_box = m1.empty()
            render_radar(radar_box, live=False)

            with m2:
                st.markdown(
                    f"""
<div class="premium-card-red">
<div class="card-title">Predictive Maintenance Engine</div>
{status_row("Engine", "Nominal")}
{status_row("Transmission", "Notice")}
{status_row("Brakes", "62% Wear")}
{status_row("DPF", "Regeneration due in 380 km")}
{status_row("Battery", "Stable")}
{status_row("Edge Gateway", "Synced")}
</div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            upgrade_card(
                "Predictive Maintenance",
                "Fleet Pro",
                "Unlock maintenance alerts, health scoring, fault trends and service planning.",
            )

    with fuel_tab:
        if has_feature("fuel"):
            f1, f2 = st.columns([1.1, 1])
            fuel_box = f1.empty()
            fuel_chart_box = f2.empty()

            render_fuel_intelligence(fuel_box, live=False)
            render_fuel_chart(fuel_chart_box, live=False)
        else:
            upgrade_card(
                "Fuel Intelligence",
                "Fleet Pro",
                "Unlock fuel savings, diesel price monitoring and refuel-window notifications.",
            )

    with reports_tab:
        if has_feature("reports"):
            alert_data = pd.DataFrame(
                [
                    ["09:20", "FX-8801", "Transmission torque drift", "High", "320 km"],
                    ["08:54", "FX-8803", "Harsh braking event", "Medium", "Immediate"],
                    ["08:16", "FX-8804", "Fuel efficiency deviation", "Medium", "Route active"],
                    ["07:41", "FX-8805", "Brake wear threshold", "Low", "3,125 km"],
                    ["06:15", "FX-8802", "Battery voltage drift", "Medium", "720 km"],
                ],
                columns=["Timestamp", "Asset", "Alert", "Severity", "ETA"],
            )

            vehicle_data = pd.DataFrame(
                [
                    ["FX-8801", "Warning", 86, "10.8%", "3 days", "Medium"],
                    ["FX-8802", "Healthy", 93, "14.1%", "18 days", "Low"],
                    ["FX-8803", "Review", 79, "8.9%", "5 days", "High"],
                    ["FX-8804", "Healthy", 91, "15.6%", "22 days", "Low"],
                    ["FX-8805", "Warning", 84, "11.7%", "7 days", "Medium"],
                ],
                columns=["Asset", "Status", "Driver Score", "Fuel Reduction", "Next Service", "Risk"],
            )

            r1, r2 = st.columns(2)
            r1.dataframe(alert_data, use_container_width=True, hide_index=True)
            r2.dataframe(vehicle_data, use_container_width=True, hide_index=True)
        else:
            upgrade_card(
                "Fleet Reports",
                "Fleet Pro",
                "Unlock operational reports, alert summaries, fuel performance and maintenance exports.",
            )

    with overview_tab:
        o1, o2, o3 = st.columns([1.2, 1, 1])

        with o1:
            chart_box = st.empty()
            render_fuel_chart(chart_box, live=False)

        with o2:
            st.metric("Monthly Fuel Saved", "3,840 L", "+12.4%")
            st.metric("Estimated CO₂ Reduction", "9.6 t", "Current month")
            st.metric("Open Alerts", "5", "2 high priority")

        with o3:
            st.metric("Connected Units", "48 / 50", "96% online")
            st.metric("AI Alert Rate", "4.3 / hr", "Active monitoring")
            st.metric("Avg Driver Score", "88 / 100", "+0.6 pts")

    with live_tab:
        if has_feature("obd"):
            live_col1, live_col2 = st.columns([2.3, 1])
            telemetry_box = live_col1.empty()
            log_box = live_col2.empty()

            render_telemetry_chart(telemetry_box, live=False)

            log_box.markdown(
                """
<div class="terminal-log">
<span class="log-time">[SYS]</span>
Standing by. Click START LIVE STREAM to start telemetry simulation.
</div>
                """,
                unsafe_allow_html=True,
            )

            if run_simulation:
                log_lines = []

                for i in range(len(route_data)):
                    render_telemetry_chart(telemetry_box, iteration=i, live=True)

                    current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    hex_code = hex(np.random.randint(4096, 65535)).upper()[2:]

                    if i == int(len(route_data) * 0.60):
                        log_str = (
                            f"<span class='log-time'>[{current_time}]</span>"
                            f"<span class='log-error'> CRITICAL 0x{hex_code} : HARD BRAKE PREDICTED</span><br>"
                        )
                    elif np.random.rand() > 0.86:
                        log_str = (
                            f"<span class='log-time'>[{current_time}]</span>"
                            f"<span class='log-warning'> WARN 0x{hex_code} : TQ_SHIFT_LATENCY</span><br>"
                        )
                    else:
                        log_str = (
                            f"<span class='log-time'>[{current_time}]</span>"
                            f" INFO 0x{hex_code} : CAN_BUS_SYNC_OK<br>"
                        )

                    log_lines.append(log_str)

                    if len(log_lines) > 13:
                        log_lines.pop(0)

                    log_box.markdown(
                        f"""
<div class="terminal-log">
{''.join(log_lines)}
</div>
                        """,
                        unsafe_allow_html=True,
                    )

                    time.sleep(0.06)
        else:
            upgrade_card(
                "Live OBD/CAN Telemetry",
                "Fleet Pro",
                "Unlock RPM, speed, fuel use, fault data and live CAN bus telemetry across the fleet.",
            )

    with map_tab:
        if has_feature("fleet_gps"):
            map_col, route_col = st.columns([2.2, 1])
            map_box = map_col.empty()
            route_box = route_col.empty()

            render_map(map_box, live=False)
            render_route_panel(route_box, live=False)

            if run_simulation:
                for i in range(len(route_data)):
                    render_map(map_box, iteration=i, live=True)
                    render_route_panel(route_box, iteration=i, live=True)
                    time.sleep(0.05)
        else:
            upgrade_card(
                "Fleet GPS Tracking",
                "Fleet Basic",
                "Unlock route monitoring, vehicle position, geofence status and fleet movement history.",
            )

    with enterprise_tab:
        if has_feature("api"):
            st.markdown(
                f"""
<div class="premium-card-red">
<div class="card-title">Enterprise Access</div>
{status_row("API Access", "Enabled")}
{status_row("Custom Reports", "Enabled")}
{status_row("Priority Support", "Enabled")}
{status_row("Data Retention", "24 months")}
{status_row("SLA", "Enterprise")}
</div>
                """,
                unsafe_allow_html=True,
            )
        else:
            upgrade_card(
                "Enterprise Tools",
                "Fleet Enterprise",
                "Unlock API access, custom reports, long-term data retention and priority support.",
            )

    with plan_tab:
        render_plan_calculator(key_prefix="fleet")
# =============================================================================
# ADMIN DASHBOARD
# =============================================================================

def render_admin_dashboard():
    render_header(
        "Admin Platform",
        "Business administration dashboard for users, subscriptions, devices, revenue and system operations.",
    )

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.markdown(metric_card("Active Users", "1,284", "+18% MoM"), unsafe_allow_html=True)
    k2.markdown(metric_card("Fleet Customers", "42", "B2B accounts"), unsafe_allow_html=True)
    k3.markdown(metric_card("Devices Online", "918", "94% online"), unsafe_allow_html=True)
    k4.markdown(metric_card("MRR", "18,420 €", "Monthly recurring"), unsafe_allow_html=True)
    k5.markdown(metric_card("ARR", "221,040 €", "Annual recurring"), unsafe_allow_html=True)

    tabs = st.tabs(["OVERVIEW", "CUSTOMERS", "PLANS", "REVENUE", "DEVICES", "SYSTEM"])

    with tabs[0]:
        c1, c2 = st.columns([1.2, 1])

        with c1:
            revenue_x = np.arange(1, 13)
            revenue_y = np.array([4.2, 5.1, 6.4, 7.2, 8.9, 10.4, 11.8, 13.2, 14.8, 16.1, 17.4, 18.4])

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=revenue_x,
                    y=revenue_y,
                    mode="lines+markers",
                    line=dict(color=RED, width=4, shape="spline"),
                    fill="tozeroy",
                    fillcolor="rgba(230,27,31,0.16)",
                    name="MRR",
                )
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color=WHITE),
                height=360,
                margin=dict(l=0, r=0, t=10, b=0),
                yaxis=dict(title="MRR k€", gridcolor="rgba(255,255,255,0.10)"),
                xaxis=dict(title="Month", gridcolor="rgba(255,255,255,0.05)"),
            )

            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown(
                f"""
<div class="premium-card-red">
<div class="card-title">Business Snapshot</div>
{status_row("Hardware price", f"{hardware_price} €")}
{status_row("Avg hardware cost", f"{(hardware_cost_low + hardware_cost_high) / 2:.0f} €")}
{status_row("Gross hardware margin", f"{hardware_price - ((hardware_cost_low + hardware_cost_high) / 2):.0f} €")}
{status_row("Main B2B plan", "Fleet Pro")}
{status_row("Recurring model", "Monthly SaaS")}
</div>
                """,
                unsafe_allow_html=True,
            )

    with tabs[1]:
        customers = pd.DataFrame(
            [
                ["Alpha Logistics", "Fleet Pro", 40, "399 €/mo", "Active"],
                ["Beta Transport", "Fleet Enterprise", 82, "699 €/mo", "Active"],
                ["City Rentals", "Fleet Basic", 22, "249 €/mo", "Trial"],
                ["Personal Users", "Mixed", 980, "Subscription", "Active"],
            ],
            columns=["Customer", "Plan", "Vehicles", "Subscription", "Status"],
        )
        st.dataframe(customers, use_container_width=True, hide_index=True)

    with tabs[2]:
        render_plan_calculator(key_prefix="admin_plans")

    with tabs[3]:
        fleet_vehicles = st.number_input(
            "Vehicles in deal",
            min_value=1,
            max_value=300,
            value=40,
            key="admin_revenue_vehicles",
        )

        selected_fleet_plan = st.selectbox(
            "Fleet plan",
            list(plans_fleet.keys()),
            index=1,
            key="admin_revenue_plan",
        )

        contract_years = st.number_input(
            "Contract years",
            min_value=1,
            max_value=5,
            value=1,
            key="admin_revenue_years",
        )

        plan_data = plans_fleet[selected_fleet_plan]
        hardware_revenue = fleet_vehicles * hardware_price
        estimated_hardware_cost = fleet_vehicles * ((hardware_cost_low + hardware_cost_high) / 2)
        estimated_hardware_profit = hardware_revenue - estimated_hardware_cost
        software_yearly = plan_data["price"] * 12
        total_contract = hardware_revenue + software_yearly * contract_years

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Hardware Revenue", f"{hardware_revenue:,.0f} €")
        r2.metric("Hardware Profit", f"{estimated_hardware_profit:,.0f} €")
        r3.metric("Software / Year", f"{software_yearly:,.0f} €")
        r4.metric("Contract Value", f"{total_contract:,.0f} €")

    with tabs[4]:
        devices = pd.DataFrame(
            [
                ["FX-8801", "Online", "Firmware 1.2.4", "12 ms", "Fleet Pro"],
                ["FX-8802", "Online", "Firmware 1.2.4", "15 ms", "Fleet Pro"],
                ["FX-8803", "Warning", "Firmware 1.2.1", "24 ms", "Fleet Basic"],
                ["FX-8804", "Online", "Firmware 1.2.4", "13 ms", "Enterprise"],
            ],
            columns=["Device", "Status", "Firmware", "Latency", "Plan"],
        )
        st.dataframe(devices, use_container_width=True, hide_index=True)

    with tabs[5]:
        st.markdown(
            f"""
<div class="premium-card-red">
<div class="card-title">System Health</div>
{status_row("API Gateway", "Online")}
{status_row("Telemetry Ingestion", "99.7%")}
{status_row("Database", "Healthy")}
{status_row("Billing Engine", "Active")}
{status_row("Notification Service", "Active")}
{status_row("Last Sync", datetime.now().strftime("%H:%M:%S"))}
</div>
            """,
            unsafe_allow_html=True,
        )


# =============================================================================
# ROUTER
# =============================================================================

if not st.session_state.logged_in:
    render_landing_page()
else:
    if st.session_state.user_role == "Personal User":
        render_personal_dashboard()
    elif st.session_state.user_role == "Fleet Manager":
        render_fleet_dashboard()
    elif st.session_state.user_role == "Admin":
        render_admin_dashboard()