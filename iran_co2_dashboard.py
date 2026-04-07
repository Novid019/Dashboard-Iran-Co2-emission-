import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. Page Configuration ---
st.set_page_config(page_title="Climate Dashboard", page_icon="🌍", layout="wide")

# --- 2. Custom UI (Shiny App Layout + Original Colors) ---
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
    
    /* FIXED DOWNLOAD BUTTON */
    .stDownloadButton > button {
        background-color: #b71c1c !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
        width: 100%;
        margin-top: 20px;
    }
    .stDownloadButton > button:hover {
        background-color: #9a0007 !important;
        color: white !important;
    }
    
    /* Shiny-style Insight Cards */
    .insight-card {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08) !important;
        border-top: 4px solid #b71c1c !important;
        height: 100%;
        margin-bottom: 25px;
    }
    .insight-card h4 {
        color: #1a1a1a !important;
        font-weight: 700;
        font-size: 1.1rem;
        margin-top: 0;
        text-transform: uppercase;
        border-bottom: 1px solid #f0f0f0;
        padding-bottom: 10px;
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
    .chart-container h4 {
        margin-top: 0;
        font-size: 1.2rem;
        color: #1a1a1a !important;
        border-bottom: 1px solid #f0f0f0;
        padding-bottom: 10px;
        font-weight: 600;
    }

    /* HIDE KEYBOARD_DOUBLE TOOLTIP */
    [data-testid="collapsedControl"] { pointer-events: none; }
    [data-testid="collapsedControl"] svg { pointer-events: auto; }
    div[data-testid="stTooltipContent"], .stTooltipIcon { display: none !important; }
    
    hr { border-color: #e5cacc !important; }
    </style>
""", unsafe_allow_html=True)

# Shared Citation HTML
CITATION_HTML = "<p style='font-size: 12px; color: #757575; text-align: right; margin-top: 10px; margin-bottom: 0px; font-style: italic;'>Data Source: Our World in Data (OWID)</p>"

# --- 3. Data Loading ---
@st.cache_data
def load_data():
    return pd.read_csv('Final_Clean_Data.csv')

df = load_data()

all_countries = sorted([c for c in df['Country'].unique() if c != 'World'])
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())

# --- 4. Sidebar Controls (Shiny Menu Layout) ---
st.sidebar.markdown("<h2 style='text-align: center; color: #b71c1c; font-weight: 800; margin-top: 0px;'>📊 TISS ANALYTICS</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Shiny-style Navigation
menu = st.sidebar.radio("Navigation", 
    ["Executive Summary", "Trends Analysis", "Economic Trajectory", "Sector Breakdown"], 
    label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("<h6 style='color: #b71c1c; font-weight: 700; margin-bottom: 5px;'>FILTER REGION</h6>", unsafe_allow_html=True)
target_country = st.sidebar.selectbox("Select Target Region", ['Iran'] + [c for c in all_countries if c != 'Iran'], label_visibility="collapsed")

st.sidebar.markdown("<br><h6 style='color: #b71c1c; font-weight: 700; margin-bottom: 5px;'>PEER COMPARISON</h6>", unsafe_allow_html=True)
compare_list = st.sidebar.multiselect("Select Peers", all_countries, default=["India", "Saudi Arabia", "Iraq", "United Arab Emirates"], label_visibility="collapsed")

st.sidebar.markdown("<br><h6 style='color: #b71c1c; font-weight: 700; margin-bottom: 5px;'>YEAR RANGE</h6>", unsafe_allow_html=True)
selected_years = st.sidebar.slider("Select Timeline", min_value=min_year, max_value=max_year, value=(min_year, max_year), label_visibility="collapsed")

# --- Data Slicing ---
df_filtered = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
df_target = df_filtered[df_filtered['Country'] == target_country]
df_world = df_filtered[df_filtered['Country'] == 'World']
compare_full_list = [target_country] + compare_list

latest_year_data = df_target[df_target['Year'] == df_target['Year'].max()]
latest_data = latest_year_data.iloc[0] if not latest_year_data.empty else {'Total CO2 Emissions (Mt)': 0, 'Per Capita CO2 (Mt)': 0, 'Share of Global CO2 (%)': 0}

# File Download Button in Sidebar
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(label="📥 Download Data (CSV)", data=csv, file_name='TISS_CO2_Data.csv', mime='text/csv')

# --- 5. Main Layout ---
# Shiny-style Main Header
st.markdown(f"<h2 style='font-weight: 800; color: #1a1a1a; margin-bottom: 0px;'>SDG 13: Climate Action Dashboard</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size: 16px; color: #424242;'>Monitoring the disconnect between economic expansion and carbon output in <b>{target_country}</b>.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Top Insight Cards
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="insight-card">
        <h4>Automated Insight</h4>
        <div style="font-size: 16px; margin-top: 15px; color: #1a1a1a;">
            <strong>Total CO₂ Emissions:</strong> <span style="color: #b71c1c; font-weight: bold;">{latest_data['Total CO2 Emissions (Mt)']:.1f} Mt</span><br><br>
            <strong>Per Capita Average:</strong> <span style="color: #b71c1c; font-weight: bold;">{latest_data['Per Capita CO2 (Mt)']:.2f} t/person</span><br><br>
            <strong>Global Share:</strong> <span style="color: #b71c1c; font-weight: bold;">{latest_data['Share of Global CO2 (%)']:.2f} %</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="insight-card">
        <h4>Strategic Implications</h4>
        <div style="font-size: 15px; margin-top: 15px; line-height: 1.5; color: #1a1a1a;">
            The selected timeline ({selected_years[0]} - {selected_years[1]}) reflects the structural nature of <b>{target_country}'s</b> carbon footprint.<br><br>
            Comparing the region against dynamic peers helps identify shifts in economic reliance on fossil fuels versus active decarbonization strategies.
        </div>
    </div>
    """, unsafe_allow_html=True)


# Plotly Configuration & Theme Colors
config = {'displaylogo': False, 'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso']}
layout_template = dict(
    height=550, paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)',
    font=dict(color='#1a1a1a', family="Segoe UI"), margin=dict(l=60, r=40, t=40, b=60)
)
C_MAIN = "#b71c1c"   
C_COMP = "#1b5e20"   
C_WORLD = "#424242"  
C_TREND = "#000000"  

# --- TAB ROUTING ---
# ALL charts are full width (stacked vertically) per your instruction.

if menu == "Executive Summary":
    # Chart 1
    st.markdown('<div class="chart-container"><h4>Historical Trajectory (Total Emissions)</h4>', unsafe_allow_html=True)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_target['Year'], y=df_target['Total CO2 Emissions (Mt)'], mode='lines+markers', name=target_country, line=dict(color=C_MAIN, width=4), marker=dict(size=10)))
    if len(df_target) > 1:
        p = np.poly1d(np.polyfit(df_target['Year'], df_target['Total CO2 Emissions (Mt)'], 1))
        fig1.add_trace(go.Scatter(x=df_target['Year'], y=p(df_target['Year']), mode='lines', name='Trend', line=dict(color=C_TREND, width=2, dash='dot')))
    fig1.update_layout(**layout_template, yaxis_title="Total CO₂ (Mt)", xaxis_title="Year",
                       xaxis=dict(showgrid=True, gridcolor='#f0f0f0'), yaxis=dict(showgrid=True, gridcolor='#f0f0f0'))
    st.plotly_chart(fig1, use_container_width=True, config=config, theme=None)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Chart 2
    st.markdown('<div class="chart-container"><h4>Per Capita vs Global Benchmark</h4>', unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_target['Year'], y=df_target['Per Capita CO2 (Mt)'], mode='lines+markers', name=target_country, line=dict(color=C_COMP, width=4), marker=dict(size=10)))
    fig2.add_trace(go.Scatter(x=df_world['Year'], y=df_world['Per Capita CO2 (Mt)'], mode='lines', name='World Avg', line=dict(color=C_WORLD, width=3, dash='dash')))
    fig2.update_layout(**layout_template, yaxis_title="Per Capita CO₂ (t/person)", xaxis_title="Year",
                       xaxis=dict(showgrid=True, gridcolor='#f0f0f0'), yaxis=dict(showgrid=True, gridcolor='#f0f0f0'))
    st.plotly_chart(fig2, use_container_width=True, config=config, theme=None)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


elif menu == "Trends Analysis":
    # Chart 3
    st.markdown(f'<div class="chart-container"><h4>Regional Peer Comparison (Year: {selected_years[1]})</h4>', unsafe_allow_html=True)
    df_latest_compare = df[(df['Year'] == selected_years[1]) & (df['Country'].isin(compare_full_list))].sort_values(by='Per Capita CO2 (Mt)', ascending=True)
    fig3 = px.bar(df_latest_compare, x='Per Capita CO2 (Mt)', y='Country', orientation='h', text_auto='.2f')
    fig3.update_traces(marker_color=[C_MAIN if c == target_country else C_COMP for c in df_latest_compare['Country']], textposition="outside")
    layout_bar = layout_template.copy()
    layout_bar['margin'] = dict(l=150, r=40, t=40, b=60)
    fig3.update_layout(**layout_bar, showlegend=False, xaxis_title="Per Capita CO₂ (t/person)", yaxis_title="", xaxis=dict(showgrid=True, gridcolor='#f0f0f0'))
    st.plotly_chart(fig3, use_container_width=True, config=config, theme=None)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


elif menu == "Economic Trajectory":
    # Chart 4
    st.markdown('<div class="chart-container"><h4>Economic Trajectory (Path Analysis)</h4>', unsafe_allow_html=True)
    df_scatter = df_filtered[df_filtered['Country'].isin(compare_full_list)]
    
    fig4 = px.scatter(df_scatter, x='GDP per Capita (Constant US$)', y='Total CO2 Emissions (Mt)', 
                      color='Country', hover_name='Country', size='Population', size_max=60,
                      log_x=True, log_y=True, opacity=0.9, color_discrete_map={target_country: C_MAIN})

    # DTICK=1 enforces absolute log scale stability (no random 2,3,4 overlapping ticks)
    fig4.update_layout(
        **layout_template,
        xaxis_title="GDP per Capita (Constant US$) - Log Scale",
        yaxis_title="Total CO₂ Emissions (Mt) - Log Scale",
        xaxis=dict(type='log', dtick=1, showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(type='log', dtick=1, showgrid=True, gridcolor='#f0f0f0'),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.01)
    )
    st.plotly_chart(fig4, use_container_width=True, config=config, theme=None)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


elif menu == "Sector Breakdown":
    # Chart 5 (Pie)
    st.markdown(f'<div class="chart-container"><h4>Global Share of Emissions ({selected_years[1]})</h4>', unsafe_allow_html=True)
    target_share = latest_data['Share of Global CO2 (%)'] if 'Share of Global CO2 (%)' in latest_data else 0
    pie_data = pd.DataFrame({'Category': [target_country, 'Rest of the World'], 'Share (%)': [target_share, max(0, 100 - target_share)]})
    fig6 = px.pie(pie_data, names='Category', values='Share (%)', hole=0.5, color='Category', color_discrete_map={target_country: C_MAIN, 'Rest of the World': '#a5d6a7'})
    fig6.update_layout(height=500, paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)', margin=dict(l=40, r=40, t=40, b=40))
    fig6.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#ffffff', width=2)))
    st.plotly_chart(fig6, use_container_width=True, config=config, theme=None)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Chart 6 (Stacked Bar)
    st.markdown(f'<div class="chart-container"><h4>Sector Breakdown: Sources of Emissions</h4>', unsafe_allow_html=True)
    sources = ['Coal CO2 (Mt)', 'Oil CO2 (Mt)', 'Gas CO2 (Mt)', 'Cement CO2 (Mt)', 'Flaring CO2 (Mt)']
    source_colors = ['#1b5e20', '#b71c1c', '#0d47a1', '#e65100', '#4a148c'] 
    df_sources = df_target[['Year'] + sources].melt(id_vars='Year', var_name='Source', value_name='Emissions')
    
    fig5 = px.bar(df_sources, x='Year', y='Emissions', color='Source', color_discrete_sequence=source_colors)
    fig5.update_layout(**layout_template, barmode='stack', yaxis_title="CO₂ Emissions (Mt)", xaxis_title="Year",
                       xaxis=dict(showgrid=True, gridcolor='#f0f0f0'), yaxis=dict(showgrid=True, gridcolor='#f0f0f0'))
    st.plotly_chart(fig5, use_container_width=True, config=config, theme=None)
    st.markdown(CITATION_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
