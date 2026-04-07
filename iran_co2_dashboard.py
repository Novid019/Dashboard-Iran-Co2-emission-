import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. Page Configuration ---
st.set_page_config(page_title="Iran CO₂ Dashboard", page_icon="🌍", layout="wide")

# --- 2. PROFESSIONAL UI DESIGN (Enhanced) ---
st.markdown("""
    <style>
    /* Professional Main Background - Clean Light Green */
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%) !important;
    }
    
    /* Professional Sidebar - Deep Red with subtle gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffebee 0%, #ffcdd2 100%) !important;
        border-right: 3px solid #c62828 !important;
        box-shadow: 2px 0 10px rgba(182,28,28,0.1) !important;
    }
    
    /* Professional Typography */
    .stApp *, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp label, .stApp span {
        color: #1a1a1a !important;
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
    }
    
    /* Title Styling */
    h1 {
        font-weight: 800 !important;
        font-size: 2.8rem !important;
        background: linear-gradient(90deg, #1b5e20, #2e7d32) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    /* FIXED DOWNLOAD BUTTON - Professional Red */
    .stDownloadButton > button {
        background: linear-gradient(145deg, #b71c1c, #d32f2f) !important;
        color: white !important;
        border: 2px solid #a52714 !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 12px 32px !important;
        box-shadow: 0 4px 15px rgba(183,28,28,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(145deg, #9a0007, #b71c1c) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(183,28,28,0.4) !important;
    }
    
    /* Enhanced Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%) !important;
        padding: 25px !important;
        border-radius: 24px !important;
        box-shadow: 0 8px 32px rgba(27,94,32,0.12) !important;
        border: 2px solid #1b5e20 !important;
        text-align: center !important;
        margin-bottom: 30px !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 40px rgba(27,94,32,0.2) !important;
    }
    
    /* Metric Values */
    [data-testid="stMetricValue"] div {
        color: #b71c1c !important;
        font-weight: 900 !important;
        font-size: 2.2em !important;
    }
    
    /* Professional Chart Containers */
    .chart-container {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafb 100%) !important;
        padding: 35px !important;
        border-radius: 24px !important;
        box-shadow: 0 10px 40px rgba(27,94,32,0.15) !important;
        margin-bottom: 45px !important;
        border: 2px solid #1b5e20 !important;
        position: relative !important;
        transition: all 0.3s ease !important;
    }
    
    .chart-container:hover {
        box-shadow: 0 15px 50px rgba(27,94,32,0.25) !important;
    }
    
    /* Chart Headers */
    .chart-header {
        color: #1b5e20 !important;
        font-weight: 700 !important;
        font-size: 1.4rem !important;
        margin-bottom: 20px !important;
        padding-bottom: 10px !important;
        border-bottom: 3px solid #c8e6c9 !important;
    }
    
    /* Controls */
    .stSelectbox, .stMultiSelect, .stSlider {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 8px !important;
    }
    
    /* Sidebar Header */
    .css-1d391kg {
        background: linear-gradient(90deg, #1b5e20, #2e7d32) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Shared Citation HTML
CITATION_HTML = "<p style='font-size: 13px; color: #666; text-align: right; margin-top: 15px; margin-bottom: 0; font-style: italic; font-family: Inter, sans-serif;'>Data Source: Our World in Data (OWID)</p>"

# --- 3. Data Loading ---
@st.cache_data
def load_data():
    return pd.read_csv('Final_Clean_Data.csv')

df = load_data()

# --- 4. Enhanced Sidebar ---
with st.sidebar:
    st.markdown("## 🌍 Climate Dashboard", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 14px;'>BS Analytics & Sustainability<br>TISS Mumbai | M2024BSASS019</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### 🎛️ Control Panel")
    all_countries = sorted([c for c in df['Country'].unique() if c != 'World'])

    target_country = st.selectbox("🎯 Target Region:", ['Iran'] + [c for c in all_countries if c != 'Iran'])
    compare_list = st.multiselect("📊 Peer Comparison:", all_countries, default=["India", "Saudi Arabia", "Iraq", "United Arab Emirates"])

    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    selected_years = st.slider("📅 Timeline:", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# --- Data Slicing ---
df_filtered = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
df_target = df_filtered[df_filtered['Country'] == target_country]
df_world = df_filtered[df_filtered['Country'] == 'World']

latest_year_data = df_target[df_target['Year'] == df_target['Year'].max()]
latest_data = latest_year_data.iloc[0] if not latest_year_data.empty else {'Total CO2 Emissions (Mt)': 0, 'Per Capita CO2 (Mt)': 0, 'Share of Global CO2 (%)': 0}

# --- 5. Main Layout ---
st.markdown(f"# {target_country} CO₂ Emissions Analysis")
st.markdown("<p style='text-align: center; font-size: 18px; color: #555; max-width: 800px; margin: 0 auto;'>Comprehensive analysis of historical carbon footprints, economic growth, and climate responsibility.</p>", unsafe_allow_html=True)
st.markdown("---")

# Enhanced KPIs
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Total CO₂ (Latest)", f"{latest_data['Total CO2 Emissions (Mt)']:.1f} Mt")
with kpi2:
    st.metric("Per Capita (Latest)", f"{latest_data['Per Capita CO2 (Mt)']:.2f} t/person")
with kpi3:
    st.metric("Global Share (Latest)", f"{latest_data['Share of Global CO2 (%)']:.2f} %")

# Plotly configuration
config = {
    'displaylogo': False,
    'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso'],
    'toImageButtonOptions': {'format': 'png', 'filename': 'TISS_Chart', 'height': 700, 'width': 1200, 'scale': 2}
}

# Professional layout template
layout_template = dict(
    height=580,
    paper_bgcolor='rgba(255,255,255,1)',
    plot_bgcolor='rgba(255,255,255,1)',
    font=dict(color='#1a1a1a', family="Inter, Segoe UI"),
    margin=dict(l=80, r=50, t=70, b=90)
)

# Color palette
C_MAIN = "#b71c1c"   
C_COMP = "#1b5e20"   
C_WORLD = "#424242"  
C_TREND = "#000000"  
C_LIGHT_GREEN = "#a5d6a7"  # Light green for Rest of World

# Chart 1-3 (keeping existing logic, just enhanced styling)
def create_chart_container(title):
    st.markdown(f'<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-header">{title}</div>', unsafe_allow_html=True)
    return True

def close_chart_container():
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Chart 1
if create_chart_container(f"📈 1. Total CO₂ Emissions Trend ({target_country})"):
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_target['Year'], y=df_target['Total CO2 Emissions (Mt)'], mode='lines+markers', name=target_country, line=dict(color=C_MAIN, width=5), marker=dict(size=12)))
    if len(df_target) > 1:
        z = np.polyfit(df_target['Year'], df_target['Total CO2 Emissions (Mt)'], 1)
        p = np.poly1d(z)
        fig1.add_trace(go.Scatter(x=df_target['Year'], y=p(df_target['Year']), mode='lines', name='Trend', line=dict(color=C_TREND, width=3, dash='dot')))
    fig1.update_layout(**layout_template, yaxis_title="Total CO₂ (Mt)", xaxis_title="Year")
    st.plotly_chart(fig1, use_container_width=True, config=config)
    close_chart_container()

# Chart 2
if create_chart_container("👤 2. Per Capita Emissions vs Global Average"):
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_target['Year'], y=df_target['Per Capita CO2 (Mt)'], mode='lines+markers', name=target_country, line=dict(color=C_COMP, width=5), marker=dict(size=12)))
    fig2.add_trace(go.Scatter(x=df_world['Year'], y=df_world['Per Capita CO2 (Mt)'], mode='lines', name='World Avg', line=dict(color=C_WORLD, width=4, dash='dash')))
    if len(df_target) > 1:
        z = np.polyfit(df_target['Year'], df_target['Per Capita CO2 (Mt)'], 1)
        p = np.poly1d(z)
        fig2.add_trace(go.Scatter(x=df_target['Year'], y=p(df_target['Year']), mode='lines', name='Trend', line=dict(color=C_TREND, width=3, dash='dot')))
    fig2.update_layout(**layout_template, yaxis_title="Per Capita CO₂ (t/person)", xaxis_title="Year")
    st.plotly_chart(fig2, use_container_width=True, config=config)
    close_chart_container()

# Chart 3
if create_chart_container(f"⚖️ 3. Regional Peer Comparison ({selected_years[1]})"):
    compare_full_list = [target_country] + compare_list
    df_latest_compare = df[(df['Year'] == selected_years[1]) & (df['Country'].isin(compare_full_list))].sort_values(by='Per Capita CO2 (Mt)', ascending=True)
    fig3 = px.bar(df_latest_compare, x='Per Capita CO2 (Mt)', y='Country', orientation='h', text_auto='.2f', color='Country', color_discrete_map={target_country: C_MAIN})
    fig3.update_traces(marker_color=[C_MAIN if c == target_country else C_COMP for c in df_latest_compare['Country']], textposition="outside", textfont=dict(size=16, color="#1a1a1a"))
    fig3.update_layout(**layout_template, showlegend=False, xaxis_title="Per Capita CO₂ (t/person)", yaxis_title="", margin=dict(l=200, r=50, t=70, b=90))
    st.plotly_chart(fig3, use_container_width=True, config=config)
    close_chart_container()

# FIXED Chart 4 - SINGLE CONTINUOUS LOG SCALE
if create_chart_container("💰 4. Economic Growth vs Carbon Output"):
    df_scatter = df_filtered[df_filtered['Country'].isin([target_country] + compare_list)]
    
    # FIXED: Proper continuous log scales
    fig4 = px.scatter(df_scatter, x='GDP per Capita (Constant US$)', y='Total CO2 Emissions (Mt)', 
                      color='Country', hover_name='Country', size='Population', size_max=65,
                      log_x=True, log_y=True, opacity=0.85, color_discrete_map={target_country: C_MAIN})
    
    fig4.update_layout(
        **layout_template,
        xaxis_title="GDP per Capita (Constant US$)",
        yaxis_title="Total CO₂ Emissions (Mt)",
        xaxis=dict(
            type='log',
            showgrid=True, 
            gridcolor='rgba(224,224,224,0.5)',
            gridwidth=1,
            zeroline=False,
            title_font=dict(size=18, color='#1a1a1a', family="Inter", weight="bold"), 
            tickfont=dict(color='#1a1a1a', size=14),
            ticks="outside",
            ticklen=8,
            tickwidth=2,
            tickcolor="#1b5e20",
            showticklabels=True,
            autorange=True  # CONTINUOUS SCALE - No restart!
        ),
        yaxis=dict(
            type='log',
            showgrid=True, 
            gridcolor='rgba(224,224,224,0.5)',
            gridwidth=1,
            zeroline=False,
            title_font=dict(size=18, color='#1a1a1a', family="Inter", weight="bold"), 
            tickfont=dict(color='#1a1a1a', size=14),
            ticks="outside",
            ticklen=8,
            tickwidth=2,
            tickcolor="#1b5e20",
            showticklabels=True,
            autorange=True  # CONTINUOUS SCALE - No restart!
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="#e0e0e0",
            borderwidth=1
        )
    )
    st.plotly_chart(fig4, use_container_width=True, config=config)
    close_chart_container()

# FIXED Chart 5 - Light Green Rest of World
if create_chart_container(f"🌐 5. Global Share of Emissions ({selected_years[1]})"):
    target_share = latest_data['Share of Global CO2 (%)'] if 'Share of Global CO2 (%)' in latest_data else 0
    pie_data = pd.DataFrame({'Category': [target_country, 'Rest of the World'], 'Share (%)': [target_share, max(0, 100 - target_share)]})
    fig6 = px.pie(pie_data, names='Category', values='Share (%)', hole=0.4, 
                  color='Category', color_discrete_map={target_country: C_MAIN, 'Rest of the World': C_LIGHT_GREEN})
    fig6.update_layout(
        height=580, 
        paper_bgcolor='rgba(255,255,255,1)', 
        plot_bgcolor='rgba(255,255,255,1)', 
        margin=dict(l=60, r=60, t=60, b=60), 
        font=dict(color='#1a1a1a', size=18, family="Inter")
    )
    fig6.update_traces(textposition='inside', textinfo='percent+label', 
                       marker=dict(line=dict(color='#ffffff', width=4)))
    st.plotly_chart(fig6, use_container_width=True, config=config)
    close_chart_container()

# Chart 6
if create_chart_container(f"🏭 6. Sector Breakdown: Sources of Emissions ({target_country})"):
    sources = ['Coal CO2 (Mt)', 'Oil CO2 (Mt)', 'Gas CO2 (Mt)', 'Cement CO2 (Mt)', 'Flaring CO2 (Mt)']
    source_colors = ['#1b5e20', '#b71c1c', '#0d47a1', '#e65100', '#4a148c'] 
    df_sources = df_target[['Year'] + sources].melt(id_vars='Year', var_name='Source', value_name='Emissions')
    fig5 = px.bar(df_sources, x='Year', y='Emissions', color='Source', color_discrete_sequence=source_colors)
    fig5.update_layout(**layout_template, barmode='stack', yaxis_title="CO₂ Emissions (Mt)", xaxis_title="Year")
    st.plotly_chart(fig5, use_container_width=True, config=config)
    close_chart_container()

# Professional Download Section
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("### 📊 Export Data")
with col2:
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Dataset (CSV)", 
        data=csv, 
        file_name=f'{target_country}_CO2_Data_{selected_years[0]}_{selected_years[1]}.csv', 
        mime='text/csv'
    )
