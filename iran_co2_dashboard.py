import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. Page Configuration ---
st.set_page_config(page_title="Iran CO₂ Dashboard", page_icon="🌍", layout="wide")

# --- 2. Custom UI (Forced Light Mode, Green/Red Theme, Fixed Borders & Spacing) ---
st.markdown("""
    <style>
    /* Force Main Background to a shade of Green */
    .stApp {
        background-color: #e8f5e9 !important; /* Soft Green */
    }
    
    /* Force Sidebar (Panel) to a shade of Red */
    [data-testid="stSidebar"] {
        background-color: #ffebee !important; /* Soft Red */
        border-right: 1px solid #e5cacc !important;
    }
    
    /* Force all text to be dark so it never vanishes in Dark Mode */
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp label, .stApp span, .stMarkdown {
        color: #1a1a1a !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Metric Cards (KPIs) styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 20px !important; /* Rounded */
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
        border: 2px solid #b71c1c !important; /* Dark Red border */
        text-align: center;
    }
    
    /* Metric Values */
    [data-testid="stMetricValue"] div {
        color: #1b5e20 !important; /* Dark Green text */
        font-weight: 800 !important;
    }
    
    /* Custom CSS for Chart Containers (Fixed Border, Radius, and Spacing) */
    .chart-container {
        background-color: #ffffff !important;
        padding: 25px !important;
        border-radius: 20px !important; /* Round border */
        box-shadow: 0 6px 15px rgba(0,0,0,0.08) !important;
        margin-bottom: 35px !important; /* Equal distance between rows */
        border: 2px solid #1b5e20 !important; /* Colored border (Dark Green) */
    }

    /* Force dropdown menus to stay readable in dark mode */
    .stSelectbox div[data-baseweb="select"] > div, 
    .stMultiSelect div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border-color: #cccccc !important;
    }
    </style>
""", unsafe_allow_html=True)

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
st.markdown(f"<h2 style='font-weight: 800; color: #1b5e20 !important;'>{target_country} CO₂ Emissions Analysis</h2>", unsafe_allow_html=True)
st.caption("Investigating historical carbon footprints, economic growth, and climate responsibility.")
st.markdown("<br>", unsafe_allow_html=True)

# KPIs on Main Layout
st.markdown(f"#### 📈 Overview ({selected_years[1]})")
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Total CO₂", f"{latest_data['Total CO2 Emissions (Mt)']:.1f} Mt")
with kpi2:
    st.metric("Per Capita", f"{latest_data['Per Capita CO2 (Mt)']:.2f} t/person")
with kpi3:
    st.metric("Global Share", f"{latest_data['Share of Global CO2 (%)']:.2f} %")
st.markdown("<br>", unsafe_allow_html=True)

# Plotly configuration for clean UI and downloading
config = {
    'displaylogo': False,
    'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso'],
    'toImageButtonOptions': {'format': 'png', 'filename': 'TISS_Chart', 'height': 600, 'width': 1000, 'scale': 2}
}

# FIXED: Clean Chart Layout Template (Uniform height, angled X-axis to prevent clutter)
layout_template = dict(
    height=450, # Uniform height for perfect proportions
    paper_bgcolor='rgba(255,255,255,1)',
    plot_bgcolor='rgba(255,255,255,1)',
    font=dict(color='#1a1a1a', family="Segoe UI"),
    margin=dict(l=20, r=20, t=50, b=60), # Extra bottom margin for angled text
    xaxis=dict(
        showgrid=True, gridcolor='#e0e0e0', 
        title_font=dict(size=14, color='#333333'), 
        tickfont=dict(color='#1a1a1a', size=11),
        tickangle=-45, # Tilts the text to prevent overlapping
        nticks=10      # Prevents too many labels from squishing together
    ),
    yaxis=dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(size=14, color='#333333'), tickfont=dict(color='#1a1a1a'))
)

# Dark Contrasting COLOR PALETTE for Charts
C_MAIN = "#b71c1c"   # Dark Red
C_COMP = "#1b5e20"   # Dark Green
C_WORLD = "#424242"  # Dark Grey
C_TREND = "#000000"  # Black

col1, col2 = st.columns(2)

# --- Chart 1: Total CO2 Emissions ---
with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 📈 Total CO₂ Emissions Trend")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_target['Year'], y=df_target['Total CO2 Emissions (Mt)'], mode='lines+markers', name=target_country, line=dict(color=C_MAIN, width=3), marker=dict(size=8)))
    
    if len(df_target) > 1:
        z = np.polyfit(df_target['Year'], df_target['Total CO2 Emissions (Mt)'], 1)
        p = np.poly1d(z)
        fig1.add_trace(go.Scatter(x=df_target['Year'], y=p(df_target['Year']), mode='lines', name='Trend', line=dict(color=C_TREND, width=2, dash='dot')))
        
    fig1.update_layout(**layout_template, yaxis_title="Total CO₂ (Mt)")
    st.plotly_chart(fig1, use_container_width=True, config=config, theme=None)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Chart 2: Per Capita CO2 Emissions ---
with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 👤 Per Capita Emissions vs Global Average")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_target['Year'], y=df_target['Per Capita CO2 (Mt)'], mode='lines+markers', name=target_country, line=dict(color=C_COMP, width=3), marker=dict(size=8)))
    fig2.add_trace(go.Scatter(x=df_world['Year'], y=df_world['Per Capita CO2 (Mt)'], mode='lines', name='World Avg', line=dict(color=C_WORLD, width=2, dash='dash')))
    
    if len(df_target) > 1:
        z = np.polyfit(df_target['Year'], df_target['Per Capita CO2 (Mt)'], 1)
        p = np.poly1d(z)
        fig2.add_trace(go.Scatter(x=df_target['Year'], y=p(df_target['Year']), mode='lines', name='Trend', line=dict(color=C_TREND, width=2, dash='dot')))

    fig2.update_layout(**layout_template, yaxis_title="Per Capita CO₂ (t/person)")
    st.plotly_chart(fig2, use_container_width=True, config=config, theme=None)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Chart 3: Peer Comparison ---
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown(f"#### ⚖️ Regional & Global Peer Comparison ({selected_years[1]})")
compare_full_list = [target_country] + compare_list
df_latest_compare = df[(df['Year'] == selected_years[1]) & (df['Country'].isin(compare_full_list))].sort_values(by='Per Capita CO2 (Mt)', ascending=True)

fig3 = px.bar(df_latest_compare, x='Per Capita CO2 (Mt)', y='Country', orientation='h', text_auto='.2f', color='Country', color_discrete_map={target_country: C_MAIN})
fig3.update_traces(marker_color=[C_MAIN if c == target_country else C_COMP for c in df_latest_compare['Country']], textposition="outside")
# Use layout template but remove x-axis angle since this is a horizontal bar chart
layout_bar = layout_template.copy()
layout_bar['xaxis'] = dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(size=14, color='#333333'), tickfont=dict(color='#1a1a1a'))
fig3.update_layout(**layout_bar, showlegend=False, xaxis_title="Per Capita CO₂ (t/person)", yaxis_title="")
st.plotly_chart(fig3, use_container_width=True, config=config, theme=None)
st.markdown('</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

# --- Chart 4: GDP vs Emissions Scatter ---
with col3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 💰 Economic Growth vs Carbon Output")
    df_scatter = df_filtered[df_filtered['Country'].isin(compare_full_list)]
    fig4 = px.scatter(df_scatter, x='GDP per Capita (Constant US$)', y='Total CO2 Emissions (Mt)', 
                      color='Country', hover_name='Country', size='Population', size_max=45,
                      log_x=True, log_y=True, opacity=0.9)
    # Remove angle for log-scaled X axis for cleaner look
    layout_scatter = layout_template.copy()
    layout_scatter['xaxis'] = dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(size=14, color='#333333'), tickfont=dict(color='#1a1a1a'))
    fig4.update_layout(**layout_scatter)
    st.plotly_chart(fig4, use_container_width=True, config=config, theme=None)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Chart 6: Global Share Pie Chart ---
with col4:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f"#### 🌐 Global Share of Emissions ({selected_years[1]})")
    target_share = latest_data['Share of Global CO2 (%)'] if 'Share of Global CO2 (%)' in latest_data else 0
    pie_data = pd.DataFrame({'Category': [target_country, 'Rest of the World'], 'Share (%)': [target_share, max(0, 100 - target_share)]})
    fig6 = px.pie(pie_data, names='Category', values='Share (%)', hole=0.5, color='Category', color_discrete_map={target_country: C_MAIN, 'Rest of the World': '#9e9e9e'})
    fig6.update_layout(height=450, paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)', margin=dict(l=20, r=20, t=40, b=20), font=dict(color='#1a1a1a'))
    fig6.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig6, use_container_width=True, config=config, theme=None)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Chart 5: Stacked Bar by Source ---
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown(f"#### 🏭 Sector Breakdown: Sources of Emissions ({target_country})")
sources = ['Coal CO2 (Mt)', 'Oil CO2 (Mt)', 'Gas CO2 (Mt)', 'Cement CO2 (Mt)', 'Flaring CO2 (Mt)']
source_colors = ['#1b5e20', '#b71c1c', '#0d47a1', '#e65100', '#4a148c'] # Dark, highly contrasting colors

df_sources = df_target[['Year'] + sources].melt(id_vars='Year', var_name='Source', value_name='Emissions')
fig5 = px.bar(df_sources, x='Year', y='Emissions', color='Source', color_discrete_sequence=source_colors)
fig5.update_layout(**layout_template, barmode='stack', yaxis_title="CO₂ Emissions (Mt)")
st.plotly_chart(fig5, use_container_width=True, config=config, theme=None)
st.markdown('</div>', unsafe_allow_html=True)

# --- Download Data Option ---
st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(label="📥 Download Dataset (CSV)", data=csv, file_name='TISS_CO2_Data.csv', mime='text/csv')
st.caption("Data: Our World in Data (OWID) — Global Carbon Project. Rendered for academic analysis.")
st.markdown("</div>", unsafe_allow_html=True)
