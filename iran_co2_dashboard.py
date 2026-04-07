import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. Page Configuration ---
st.set_page_config(page_title="Iran CO₂ Dashboard", page_icon="🌍", layout="wide")

# --- 2. Custom UI (Forced Light Mode, Green/Red Theme, Uniform Borders, FIXED DOWNLOAD BUTTON) ---
st.markdown("""
    <style>
    /* Force Main Background to a shade of Green */
    .stApp {
        background-color: #e8f5e9 !important; 
    }
    
    /* Force Sidebar (Panel) to a shade of Red */
    [data-testid="stSidebar"] {
        background-color: #ffebee !important; 
        border-right: 1px solid #e5cacc !important;
    }
    
    /* Force all text to be dark */
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp label, .stApp span, .stMarkdown {
        color: #1a1a1a !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* FIXED DOWNLOAD BUTTON - Always dark red background with white text */
    .stDownloadButton > button {
        background-color: #b71c1c !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    
    .stDownloadButton > button:hover {
        background-color: #9a0007 !important;
        color: white !important;
    }
    
    /* UNIFORM BORDERS: Metric Cards (KPIs) styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 20px !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.08) !important;
        border: 2px solid #1b5e20 !important;
        text-align: center;
        margin-bottom: 25px !important;
    }
    
    /* Metric Values */
    [data-testid="stMetricValue"] div {
        color: #b71c1c !important;
        font-weight: 800 !important;
    }
    
    /* UNIFORM BORDERS: Chart Containers */
    .chart-container {
        background-color: #ffffff !important;
        padding: 30px !important;
        border-radius: 20px !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.08) !important;
        margin-bottom: 40px !important; 
        border: 2px solid #1b5e20 !important;
        height: 100%;
    }

    /* Force dropdown menus to stay readable */
    .stSelectbox div[data-baseweb="select"] > div, 
    .stMultiSelect div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border-color: #cccccc !important;
    }

    /* HIDE KEYBOARD_DOUBLE TOOLTIP */
    [data-testid="collapsedControl"] {
        pointer-events: none; /* Disable the glitchy hover completely */
    }
    [data-testid="collapsedControl"] svg {
        pointer-events: auto; /* Keep the icon itself clickable */
    }
    div[data-testid="stTooltipContent"], .stTooltipIcon {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Shared Citation HTML
CITATION_HTML = "<p style='font-size: 12px; color: #424242; text-align: right; margin-top: 10px; margin-bottom: 0px; font-style: italic;'>Data: Our World in Data (OWID)</p>"

# --- 3. Data Loading ---
@st.cache_data
def load_data():
    return pd.read_csv('Final_Clean_Data.csv')

df = load_data()

# --- 4. Sidebar Controls ---
st.sidebar.markdown("<h1 style='text-align: center; font-size: 40px;'>🌍</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align: center; color: #b71c1c !important; font-weight: 700;'>Climate Dashboard</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 13px; color: #424242 !important;'>BS Analytics & Sustainability<br>TISS Mumbai | M2024BSASS019</p>", unsafe_allow_html=True)
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
st.markdown(f"<h1 style='font-weight: 800; color: #1b5e20 !important; text-align: center;'>{target_country} CO₂ Emissions Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; color: #424242;'>Investigating historical carbon footprints, economic growth, and climate responsibility.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

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
config = {
    'displaylogo': False,
    'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso'],
    'toImageButtonOptions': {'format': 'png', 'filename': 'TISS_Chart', 'height': 700, 'width': 1200, 'scale': 2}
}

# Base layout template
layout_template = dict(
    height=550, 
    paper_bgcolor='rgba(255,255,255,1)',
    plot_bgcolor='rgba(255,255,255,1)',
    font=dict(color='#1a1a1a', family="Segoe UI"),
    margin=dict(l=60, r=40, t=60, b=80)
)

# Color palette
C_MAIN = "#b71c1c"   
C_COMP = "#1b5e20"   
C_WORLD = "#424242"  
C_TREND = "#000000"  

# ----------------- CHARTS 1 & 2 (SIDE BY SIDE) -----------------
col1, col2 = st.columns(2)

with col1:
    # --- Chart 1: Total CO2 Emissions ---
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #1b5e20;'>📈 1. Total CO₂ Emissions Trend ({target_country})</h3>", unsafe_allow_html=True)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_target['Year'], y=df_target['Total CO2 Emissions (Mt)'], mode='lines+markers', name=target_country, line=dict(color=C_MAIN, width=4), marker=dict(size=10)))

    if len(df_target) > 1:
        z = np.polyfit(df_target['Year'], df_target['Total CO2 Emissions (Mt)'], 1)
        p = np.poly1d(z)
        fig1.add_trace(go.Scatter(x=df_target['Year'], y=p(df_target['Year']), mode='lines', name='Trend', line=dict(color=C_TREND, width=2, dash='dot')))
        
    fig1.update_layout(**layout_template, yaxis_title="Total CO₂ (Mt)", xaxis_title="Year",
                       xaxis=dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(size=16, color='#1a1a1a', family="Segoe UI", weight="bold"), tickfont=dict(color='#1a1a1a', size=13), tickangle=0, nticks=15),
                       yaxis=dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(size=16, color='#1a1a1a', family="Segoe UI", weight="bold"), tickfont=dict(color='#1a1a1a', size=13)))
    st.plotly_chart(fig1, use_container_width=True, config=config, theme=None)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # --- Chart 2: Per Capita ---
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #1b5e20;'>👤 2. Per Capita Emissions vs Global Average</h3>", unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_target['Year'], y=df_target['Per Capita CO2 (Mt)'], mode='lines+markers', name=target_country, line=dict(color=C_COMP, width=4), marker=dict(size=10)))
    fig2.add_trace(go.Scatter(x=df_world['Year'], y=df_world['Per Capita CO2 (Mt)'], mode='lines', name='World Avg', line=dict(color=C_WORLD, width=3, dash='dash')))

    if len(df_target) > 1:
        z = np.polyfit(df_target['Year'], df_target['Per Capita CO2 (Mt)'], 1)
        p = np.poly1d(z)
        fig2.add_trace(go.Scatter(x=df_target['Year'], y=p(df_target['Year']), mode='lines', name='Trend', line=dict(color=C_TREND, width=2, dash='dot')))

    fig2.update_layout(**layout_template, yaxis_title="Per Capita CO₂ (t/person)", xaxis_title="Year",
                       xaxis=dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(size=16, color='#1a1a1a', family="Segoe UI", weight="bold"), tickfont=dict(color='#1a1a1a', size=13), tickangle=0, nticks=15),
                       yaxis=dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(size=16, color='#1a1a1a', family="Segoe UI", weight="bold"), tickfont=dict(color='#1a1a1a', size=13)))
    st.plotly_chart(fig2, use_container_width=True, config=config, theme=None)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------- CHARTS 3 & 4 (FULL WIDTH) -----------------
# --- Chart 3: Peer Comparison ---
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown(f"<h3 style='color: #1b5e20;'>⚖️ 3. Regional Peer Comparison ({selected_years[1]})</h3>", unsafe_allow_html=True)
compare_full_list = [target_country] + compare_list
df_latest_compare = df[(df['Year'] == selected_years[1]) & (df['Country'].isin(compare_full_list))].sort_values(by='Per Capita CO2 (Mt)', ascending=True)

fig3 = px.bar(df_latest_compare, x='Per Capita CO2 (Mt)', y='Country', orientation='h', text_auto='.2f', color='Country', color_discrete_map={target_country: C_MAIN})
fig3.update_traces(marker_color=[C_MAIN if c == target_country else C_COMP for c in df_latest_compare['Country']], textposition="outside", textfont=dict(size=14, color="#1a1a1a"))

layout_bar = layout_template.copy()
layout_bar['margin'] = dict(l=150, r=40, t=60, b=80)
fig3.update_layout(**layout_bar, showlegend=False, xaxis_title="Per Capita CO₂ (t/person)", yaxis_title="")
st.plotly_chart(fig3, use_container_width=True, config=config, theme=None)
st.markdown(CITATION_HTML, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Chart 4: GDP vs Emissions Scatter (FIXED LOG AXIS) ---
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("<h3 style='color: #1b5e20;'>💰 4. Economic Growth vs Carbon Output</h3>", unsafe_allow_html=True)
df_scatter = df_filtered[df_filtered['Country'].isin(compare_full_list)]

fig4 = px.scatter(df_scatter, x='GDP per Capita (Constant US$)', y='Total CO2 Emissions (Mt)', 
                  color='Country', hover_name='Country', size='Population', size_max=60,
                  log_x=True, log_y=True, opacity=0.9, color_discrete_map={target_country: C_MAIN})

# Removed tickmode='auto' and nticks to prevent Plotly from messing up the log scales
fig4.update_layout(
    **layout_template,
    xaxis_title="GDP per Capita (Constant US$) - Log Scale",
    yaxis_title="Total CO₂ Emissions (Mt) - Log Scale",
    xaxis=dict(
        type='log',
        showgrid=True, 
        gridcolor='#e0e0e0', 
        title_font=dict(size=16, color='#1a1a1a', family="Segoe UI", weight="bold"), 
        tickfont=dict(color='#1a1a1a', size=13)
    ),
    yaxis=dict(
        type='log',
        showgrid=True, 
        gridcolor='#e0e0e0', 
        title_font=dict(size=16, color='#1a1a1a', family="Segoe UI", weight="bold"), 
        tickfont=dict(color='#1a1a1a', size=13)
    ),
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.01
    )
)
st.plotly_chart(fig4, use_container_width=True, config=config, theme=None)
st.markdown(CITATION_HTML, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ----------------- CHARTS 5 & 6 (SIDE BY SIDE) -----------------
col3, col4 = st.columns(2)

with col3:
    # --- Chart 5: Global Share Pie ---
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #1b5e20;'>🌐 5. Global Share of Emissions ({selected_years[1]})</h3>", unsafe_allow_html=True)
    target_share = latest_data['Share of Global CO2 (%)'] if 'Share of Global CO2 (%)' in latest_data else 0
    pie_data = pd.DataFrame({'Category': [target_country, 'Rest of the World'], 'Share (%)': [target_share, max(0, 100 - target_share)]})
    
    # Changed 'Rest of the World' color to Light Green (#a5d6a7)
    fig6 = px.pie(pie_data, names='Category', values='Share (%)', hole=0.5, color='Category', color_discrete_map={target_country: C_MAIN, 'Rest of the World': '#a5d6a7'})
    fig6.update_layout(height=550, paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)', margin=dict(l=40, r=40, t=60, b=40), font=dict(color='#1a1a1a', size=16))
    fig6.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#ffffff', width=2)))
    st.plotly_chart(fig6, use_container_width=True, config=config, theme=None)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    # --- Chart 6: Stacked Bar ---
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #1b5e20;'>🏭 6. Sector Breakdown: Sources of Emissions ({target_country})</h3>", unsafe_allow_html=True)
    sources = ['Coal CO2 (Mt)', 'Oil CO2 (Mt)', 'Gas CO2 (Mt)', 'Cement CO2 (Mt)', 'Flaring CO2 (Mt)']
    source_colors = ['#1b5e20', '#b71c1c', '#0d47a1', '#e65100', '#4a148c'] 

    df_sources = df_target[['Year'] + sources].melt(id_vars='Year', var_name='Source', value_name='Emissions')
    fig5 = px.bar(df_sources, x='Year', y='Emissions', color='Source', color_discrete_sequence=source_colors)
    fig5.update_layout(**layout_template, barmode='stack', yaxis_title="CO₂ Emissions (Mt)", xaxis_title="Year",
                       xaxis=dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(size=16, color='#1a1a1a', family="Segoe UI", weight="bold"), tickfont=dict(color='#1a1a1a', size=13), tickangle=0, nticks=15),
                       yaxis=dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(size=16, color='#1a1a1a', family="Segoe UI", weight="bold"), tickfont=dict(color='#1a1a1a', size=13)))
    st.plotly_chart(fig5, use_container_width=True, config=config, theme=None)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# --- FIXED Download Button ---
st.markdown("<div style='text-align: center; margin-top: 20px; margin-bottom: 50px;'>", unsafe_allow_html=True)
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(label="📥 Download Filtered Dataset (CSV)", data=csv, file_name='TISS_CO2_Data.csv', mime='text/csv')
st.markdown("</div>", unsafe_allow_html=True)
