import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. Page Configuration ---
st.set_page_config(page_title="CO₂ Emissions Dashboard", page_icon="🌍", layout="wide")

# --- 2. Custom UI (Professional Theme & Layout Fixes) ---
st.markdown("""
    <style>
    /* Clean, Professional Background */
    .stApp {
        background-color: #f4f6f8 !important; 
    }
    
    /* Professional Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important; 
        border-right: 1px solid #e0e4e8 !important;
    }
    
    /* FIXED: Removed 'span' from this list. 
       Overriding 'span' fonts destroys Streamlit's Material Icons, 
       which caused the "keyboard_double" text to appear! */
    .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp label, .stMarkdown {
        color: #2c3e50 !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background-color: #b71c1c !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background-color: #9a0007 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Uniform Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        border-top: 4px solid #1b5e20 !important;
        text-align: center;
        margin-bottom: 20px !important;
    }
    
    [data-testid="stMetricValue"] div {
        color: #2c3e50 !important;
        font-weight: 700 !important;
    }
    
    /* Chart Containers for Side-by-Side layout */
    .chart-container {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        margin-bottom: 20px !important; 
        border: 1px solid #e0e4e8 !important;
        height: 100%;
    }

    /* Titles inside chart containers */
    .chart-title {
        color: #1b5e20; 
        font-size: 1.1rem; 
        font-weight: 600; 
        margin-bottom: 10px;
        border-bottom: 1px solid #eee;
        padding-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Shared Citation HTML
CITATION_HTML = "<p style='font-size: 11px; color: #7f8c8d; text-align: right; margin-top: 5px; margin-bottom: 0px; font-style: italic;'>Data: Our World in Data (OWID)</p>"

# --- 3. Data Loading ---
@st.cache_data
def load_data():
    return pd.read_csv('Final_Clean_Data.csv')

try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: 'Final_Clean_Data.csv' not found. Please ensure the file is in the same directory.")
    st.stop()

# --- 4. Sidebar Controls ---
st.sidebar.markdown("<h1 style='text-align: center; font-size: 40px; margin-bottom: 0;'>🌍</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align: center; color: #b71c1c !important; font-weight: 700; margin-top: 0;'>Climate Dashboard</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 12px; color: #7f8c8d !important;'>BS Analytics & Sustainability<br>TISS Mumbai | M2024BSASS019</p>", unsafe_allow_html=True)
st.sidebar.divider()

st.sidebar.subheader("🎛️ Parameters")
all_countries = sorted([c for c in df['Country'].unique() if c != 'World'])

target_country = st.sidebar.selectbox("🎯 Target Region:", ['Iran'] + [c for c in all_countries if c != 'Iran'])
compare_list = st.sidebar.multiselect("📊 Peer Comparison:", all_countries, default=["India", "Saudi Arabia", "Iraq", "United Arab Emirates"])

min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
selected_years = st.sidebar.slider("📅 Timeline:", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# --- Data Slicing ---
df_filtered = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
df_target = df_filtered[df_filtered['Country'] == target_country]
df_world = df_filtered[df_filtered['Country'] == 'World']

latest_year_data = df_target[df_target['Year'] == df_target['Year'].max()]
latest_data = latest_year_data.iloc[0] if not latest_year_data.empty else {'Total CO2 Emissions (Mt)': 0, 'Per Capita CO2 (Mt)': 0, 'Share of Global CO2 (%)': 0}

# --- 5. Main Layout ---
st.markdown(f"<h2 style='font-weight: 800; color: #1b5e20 !important; text-align: center; margin-bottom: 5px;'>{target_country} CO₂ Emissions Analysis</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 15px; color: #7f8c8d;'>Investigating historical carbon footprints, economic growth, and climate responsibility.</p>", unsafe_allow_html=True)

# KPIs
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Total CO₂ (Latest)", f"{latest_data['Total CO2 Emissions (Mt)']:.1f} Mt")
with kpi2:
    st.metric("Per Capita (Latest)", f"{latest_data['Per Capita CO2 (Mt)']:.2f} t/person")
with kpi3:
    st.metric("Global Share (Latest)", f"{latest_data['Share of Global CO2 (%)']:.2f} %")
st.markdown("<br>", unsafe_allow_html=True)

# Plotly configuration
config = {'displaylogo': False, 'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso']}

# Base layout template for side-by-side charts
layout_template = dict(
    height=400, # Reduced height for side-by-side view
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#2c3e50', family="Segoe UI"),
    margin=dict(l=50, r=20, t=30, b=50)
)

# Color palette
C_MAIN = "#b71c1c"   
C_COMP = "#1b5e20"   
C_WORLD = "#7f8c8d"  
C_TREND = "#2c3e50"  

# ----------------- ROW 1 -----------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f"<div class='chart-title'>📈 1. Total CO₂ Emissions Trend ({target_country})</div>", unsafe_allow_html=True)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_target['Year'], y=df_target['Total CO2 Emissions (Mt)'], mode='lines', name=target_country, line=dict(color=C_MAIN, width=3)))
    
    if len(df_target) > 1:
        z = np.polyfit(df_target['Year'], df_target['Total CO2 Emissions (Mt)'], 1)
        p = np.poly1d(z)
        fig1.add_trace(go.Scatter(x=df_target['Year'], y=p(df_target['Year']), mode='lines', name='Trend', line=dict(color=C_TREND, width=2, dash='dot')))
        
    fig1.update_layout(**layout_template, yaxis_title="Total CO₂ (Mt)", xaxis_title="Year",
                       xaxis=dict(showgrid=True, gridcolor='#f0f2f6'),
                       yaxis=dict(showgrid=True, gridcolor='#f0f2f6'))
    st.plotly_chart(fig1, use_container_width=True, config=config)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>👤 2. Per Capita Emissions vs Global Average</div>", unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_target['Year'], y=df_target['Per Capita CO2 (Mt)'], mode='lines', name=target_country, line=dict(color=C_COMP, width=3)))
    fig2.add_trace(go.Scatter(x=df_world['Year'], y=df_world['Per Capita CO2 (Mt)'], mode='lines', name='World Avg', line=dict(color=C_WORLD, width=2, dash='dash')))
    
    if len(df_target) > 1:
        z = np.polyfit(df_target['Year'], df_target['Per Capita CO2 (Mt)'], 1)
        p = np.poly1d(z)
        fig2.add_trace(go.Scatter(x=df_target['Year'], y=p(df_target['Year']), mode='lines', name='Trend', line=dict(color=C_TREND, width=2, dash='dot')))

    fig2.update_layout(**layout_template, yaxis_title="Per Capita CO₂ (t/person)", xaxis_title="Year",
                       xaxis=dict(showgrid=True, gridcolor='#f0f2f6'),
                       yaxis=dict(showgrid=True, gridcolor='#f0f2f6'))
    st.plotly_chart(fig2, use_container_width=True, config=config)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- ROW 2 -----------------
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f"<div class='chart-title'>⚖️ 3. Regional Peer Comparison ({selected_years[1]})</div>", unsafe_allow_html=True)
    compare_full_list = [target_country] + compare_list
    df_latest_compare = df[(df['Year'] == selected_years[1]) & (df['Country'].isin(compare_full_list))].sort_values(by='Per Capita CO2 (Mt)', ascending=True)

    fig3 = px.bar(df_latest_compare, x='Per Capita CO2 (Mt)', y='Country', orientation='h', text_auto='.2f', color='Country', color_discrete_map={target_country: C_MAIN})
    fig3.update_traces(marker_color=[C_MAIN if c == target_country else C_COMP for c in df_latest_compare['Country']], textposition="outside")

    layout_bar = layout_template.copy()
    layout_bar['margin'] = dict(l=100, r=20, t=30, b=50)
    fig3.update_layout(**layout_bar, showlegend=False, xaxis_title="Per Capita CO₂ (t/person)", yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True, config=config)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>💰 4. Economic Growth vs Carbon Output</div>", unsafe_allow_html=True)
    df_scatter = df_filtered[df_filtered['Country'].isin(compare_full_list)]

    fig4 = px.scatter(df_scatter, x='GDP per Capita (Constant US$)', y='Total CO2 Emissions (Mt)', 
                      color='Country', hover_name='Country', size='Population', size_max=45,
                      log_x=True, log_y=True, opacity=0.8, color_discrete_map={target_country: C_MAIN})

    # FIXED: tickformat="~s" forces 1k, 10k, 1M instead of restarting counts. Removed nticks.
    fig4.update_layout(
        **layout_template,
        xaxis=dict(type='log', title="GDP per Capita (US$) - Log", showgrid=True, gridcolor='#f0f2f6', tickformat="~s"),
        yaxis=dict(type='log', title="Total CO₂ (Mt) - Log", showgrid=True, gridcolor='#f0f2f6', tickformat="~s"),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.8)")
    )
    st.plotly_chart(fig4, use_container_width=True, config=config)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- ROW 3 -----------------
col5, col6 = st.columns(2)

with col5:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f"<div class='chart-title'>🌐 5. Global Share of Emissions ({selected_years[1]})</div>", unsafe_allow_html=True)
    target_share = latest_data['Share of Global CO2 (%)'] if 'Share of Global CO2 (%)' in latest_data else 0
    pie_data = pd.DataFrame({'Category': [target_country, 'Rest of the World'], 'Share (%)': [target_share, max(0, 100 - target_share)]})
    
    # FIXED: Rest of the world is now Light Green (#a5d6a7)
    fig6 = px.pie(pie_data, names='Category', values='Share (%)', hole=0.5, color='Category', color_discrete_map={target_country: C_MAIN, 'Rest of the World': '#a5d6a7'})
    fig6.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=30, b=20), font=dict(color='#2c3e50'))
    fig6.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#ffffff', width=2)))
    st.plotly_chart(fig6, use_container_width=True, config=config)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f"<div class='chart-title'>🏭 6. Sector Breakdown ({target_country})</div>", unsafe_allow_html=True)
    sources = ['Coal CO2 (Mt)', 'Oil CO2 (Mt)', 'Gas CO2 (Mt)', 'Cement CO2 (Mt)', 'Flaring CO2 (Mt)']
    source_colors = ['#2e7d32', '#b71c1c', '#1565c0', '#e65100', '#6a1b9a'] 

    # Handle missing columns gracefully
    existing_sources = [s for s in sources if s in df_target.columns]
    
    if existing_sources:
        df_sources = df_target[['Year'] + existing_sources].melt(id_vars='Year', var_name='Source', value_name='Emissions')
        fig5 = px.bar(df_sources, x='Year', y='Emissions', color='Source', color_discrete_sequence=source_colors)
        fig5.update_layout(**layout_template, barmode='stack', yaxis_title="CO₂ Emissions (Mt)", xaxis_title="Year",
                           xaxis=dict(showgrid=True, gridcolor='#f0f2f6'),
                           yaxis=dict(showgrid=True, gridcolor='#f0f2f6'),
                           legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.8)"))
        st.plotly_chart(fig5, use_container_width=True, config=config)
    else:
        st.info("Detailed sector data not available for this region.")
        
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Download Button ---
st.markdown("<div style='text-align: center; margin-top: 20px; margin-bottom: 40px;'>", unsafe_allow_html=True)
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(label="📥 Download Filtered Dataset (CSV)", data=csv, file_name='Climate_Data_Export.csv', mime='text/csv')
st.markdown("</div>", unsafe_allow_html=True)
