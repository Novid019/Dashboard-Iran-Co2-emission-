import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. Page Configuration (Locked Sidebar Open) ---
st.set_page_config(page_title="Iran CO₂ Dashboard", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

# --- 2. Custom UI (Shiny App Structure + Original Colors + LEFT SIDEBAR + LIGHT GREEN BUTTON) ---
st.markdown("""
    <style>
    /* Force Main Background to a shade of Green */
    .stApp {
        background-color: #e8f5e9 !important; 
    }
    
    /* Force Sidebar (Panel) to a shade of Red, Border on RIGHT */
    [data-testid="stSidebar"] {
        background-color: #ffebee !important; 
        border-right: 1px solid #e5cacc !important;
    }
    
    /* Force all text to be dark */
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp label, .stApp span, .stMarkdown {
        color: #1a1a1a !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Top Navigation / Radio style to mimic Shiny sidebar menu */
    div.row-widget.stRadio > div {
        background-color: transparent;
        gap: 0px;
    }
    div.row-widget.stRadio > div > label {
        padding: 12px 15px;
        border-radius: 4px;
        margin-bottom: 2px;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    div.row-widget.stRadio > div > label:hover {
        background-color: #fce4e4 !important;
    }
    /* Active menu tab */
    div.row-widget.stRadio > div > label[data-checked="true"] {
        background-color: #b71c1c !important;
        color: white !important;
        border-left: 4px solid #1b5e20 !important;
    }
    div.row-widget.stRadio > div > label[data-checked="true"] p {
        color: white !important;
    }
    
    /* FIXED DOWNLOAD BUTTON (NOW LIGHT GREEN) */
    .stDownloadButton > button {
        background-color: #a5d6a7 !important; /* Light Green */
        color: #1a1a1a !important; /* Dark text for contrast against light green */
        border: 1px solid #81c784 !important;
        border-radius: 4px !important;
        font-weight: 700 !important;
        width: 100%;
        margin-top: 20px;
    }
    .stDownloadButton > button:hover {
        background-color: #81c784 !important; /* Slightly more saturated light green on hover */
        color: #1a1a1a !important;
    }
    
    /* UNIFORM BORDERS: Metric Cards (KPIs) styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08) !important;
        border-top: 4px solid #b71c1c !important;
        text-align: center;
        margin-bottom: 25px !important;
    }
    
    /* Metric Values */
    [data-testid="stMetricValue"] div {
        color: #b71c1c !important;
        font-weight: 800 !important;
    }
    
    /* Shiny-style Chart Containers */
    .chart-container {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08) !important;
        margin-bottom: 30px !important; 
        border-top: 4px solid #1b5e20 !important;
    }
    .chart-container h3 {
        margin-top: 0;
        font-size: 1.3rem;
        color: #1b5e20 !important;
        border-bottom: 1px solid #f0f0f0;
        padding-bottom: 10px;
        font-weight: 600;
    }

    /* --- AGGRESSIVELY REMOVE SIDEBAR HIDE FUNCTION --- */
    /* Targets the 'closed' state button */
    [data-testid="collapsedControl"] { 
        display: none !important; 
    }
    /* Targets the 'open' state button inside the sidebar */
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }
    /* Fallback for older/newer Streamlit versions */
    section[data-testid="stSidebar"] button[kind="header"] {
        display: none !important;
    }
    
    hr { border-color: #e5cacc !important; }
    </style>
""", unsafe_allow_html=True)

# Shared Citation HTML
CITATION_HTML = "<p style='font-size: 12px; color: #424242; text-align: right; margin-top: 10px; margin-bottom: 0px; font-style: italic;'>Data: Our World in Data (OWID)</p>"

# --- 3. Data Loading ---
@st.cache_data
def load_data():
    return pd.read_csv('Final_Clean_Data.csv')

df = load_data()

all_countries = sorted([c for c in df['Country'].unique() if c != 'World'])
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())

# --- 4. Sidebar Controls (Shiny Menu Layout + Original Titles) ---
st.sidebar.markdown("<h1 style='text-align: center; font-size: 40px; margin-top: 0px;'>🌍</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align: center; color: #b71c1c !important; font-weight: 700;'>Climate Dashboard</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 13px; color: #424242 !important;'>BS Analytics & Sustainability<br>TISS Mumbai | M2024BSASS019</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Shiny-style Navigation mapped to Original Chart Groupings
menu = st.sidebar.radio("Navigation", 
    ["📈 Emissions Trends", "⚖️ Peer Comparison", "💰 Economic Growth", "🏭 Sector & Global Share"], 
    label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Parameters")
target_country = st.sidebar.selectbox("🎯 Target Region:", ['Iran'] + [c for c in all_countries if c != 'Iran'])
compare_list = st.sidebar.multiselect("📊 Peer Comparison:", all_countries, default=["India", "Saudi Arabia", "Iraq", "United Arab Emirates"])
selected_years = st.sidebar.slider("📅 Timeline:", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# --- Data Slicing ---
df_filtered = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
df_target = df_filtered[df_filtered['Country'] ==
