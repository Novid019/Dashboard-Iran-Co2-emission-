import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. Page Configuration ---
st.set_page_config(page_title="Global CO₂ Dashboard", page_icon="🌍", layout="wide")

# --- 2. Custom Professional UI Theme ---
st.markdown("""
    <style>
    /* Professional Background and Typography */
    .stApp {
        background-color: #f4f6f9 !important; 
    }
    
    [data-testid="stSidebar"] {
        background-color: #ffffff !important; 
        border-right: 1px solid #e0e0e0 !important;
    }
    
    /* Hide 'keyboard_double' tooltip/text bug on Streamlit sidebar collapse */
    [data-testid="collapsedControl"] span, 
    .material-symbols-rounded {
        display: none !important;
        color: transparent !important;
    }
    
    /* Clean, professional text colors */
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp label, .stApp span, .stMarkdown {
        color: #2b2b2b !important;
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    }
    
    /* FIXED DOWNLOAD BUTTON - Professional Blue */
    .stDownloadButton > button {
        background-color: #1976d2 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background-color: #115293 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* UNIFORM BORDERS: Metric Cards (KPIs) styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04) !important;
        border: 1px solid #e9ecef !important;
        text-align: center;
        margin-bottom: 25px !important;
    }
    
    /* Metric Values */
    [data-testid="stMetricValue"] div {
        color: #1976d2 !important;
        font-weight: 700 !important;
        font-size: 28px !important;
    }
    [data-testid="stMetricLabel"] div {
        color: #6c757d !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 13px !important;
    }
    
    /* UNIFORM BORDERS: Chart Containers */
    .chart-container {
        background-color: #ffffff !important;
        padding: 25px !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04) !important;
        margin-bottom: 30px !important; 
        border: 1px solid #e9ecef !important;
        height: 100%;
    }

    /* Clean up headers */
    h3 {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #343a40 !important;
        margin-bottom: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Shared Citation HTML
CITATION_HTML = "<p style='font-size: 11px; color: #868e96; text-align: right; margin-top: 15px; margin-bottom: 0px;'>Source: Our World in Data (OWID)</p>"

# --- 3. Data Loading ---
@st.cache_data
def load_data():
    # Make sure 'Final_Clean_Data.csv' is available in the directory
    try:
        return pd.read_csv('Final_Clean_Data.csv')
    except:
        # Fallback dummy dataframe in case of missing file to prevent crashes
        st.warning("Data file not found. Please ensure 'Final_Clean_Data.csv' is in the root directory.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- 4. Sidebar Controls ---
    st.sidebar.markdown("<h2 style='text-align: center; color: #1976d2 !important; font-weight: 700; margin-top: 20px;'>🌍 Climate Tracker</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; font-size: 12px; color: #6c757d !important;'>BS Analytics & Sustainability<br>TISS Mumbai</p>", unsafe_allow_html=True)
    st.sidebar.divider()

    st.sidebar.subheader("Dashboard Parameters")
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
    st.markdown(f"<h1 style='font-weight: 700; color: #212529 !important; text-align: center; margin-bottom: 5px;'>{target_country} Carbon Output Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 15px; color: #6c757d; margin-bottom: 30px;'>Evaluating historical carbon footprints, economic growth correlations, and regional comparisons.</p>", unsafe_allow_html=True)

    # KPIs
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric("Total CO₂ (Latest Year)", f"{latest_data['Total CO2 Emissions (Mt)']:.1f} Mt")
    with kpi2:
        st.metric("Per Capita Avg", f"{latest_data['Per Capita CO2 (Mt)']:.2f} t/person")
    with kpi3:
        st.metric("Global Contribution", f"{latest_data['Share of Global CO2 (%)']:.2f} %")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Plotly configuration
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso'],
    }

    # Base layout template for professional look (sized for 2 columns)
    layout_template = dict(
        height=400, 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#495057', family="Inter, sans-serif"),
        margin=dict(l=40, r=20, t=40, b=40)
    )

    # Professional Color palette
    C_MAIN = "#1976d2"   # Primary Blue
    C_COMP = "#2e7d32"   # Secondary Green
    C_WORLD = "#adb5bd"  # Neutral Gray
    C_TREND = "#d32f2f"  # Accent Red

    # ================= ROW 1 =================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown(f"<h3>1. Total CO₂ Emissions Trend</h3>", unsafe_allow_html=True)
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=df_target['Year'], y=df_target['Total CO2 Emissions (Mt)'], mode='lines', name=target_country, line=dict(color=C_MAIN, width=3)))

        if len(df_target) > 1:
            z = np.polyfit(df_target['Year'], df_target['Total CO2 Emissions (Mt)'], 1)
            p = np.poly1d(z)
            fig1.add_trace(go.Scatter(x=df_target['Year'], y=p(df_target['Year']), mode='lines', name='Trend', line=dict(color=C_TREND, width=2, dash='dot')))
            
        fig1.update_layout(**layout_template, 
                           xaxis=dict(showgrid=True, gridcolor='#f1f3f5'),
                           yaxis=dict(showgrid=True, gridcolor='#f1f3f5', title="Total CO₂ (Mt)"))
        st.plotly_chart(fig1, use_container_width=True, config=config)
        st.markdown(CITATION_HTML, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("<h3>2. Per Capita Emissions vs Global Average</h3>", unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df_target['Year'], y=df_target['Per Capita CO2 (Mt)'], mode='lines', name=target_country, line=dict(color=C_MAIN, width=3)))
        
        if not df_world.empty:
            fig2.add_trace(go.Scatter(x=df_world['Year'], y=df_world['Per Capita CO2 (Mt)'], mode='lines', name='World Avg', line=dict(color=C_WORLD, width=2, dash='dash')))

        fig2.update_layout(**layout_template, 
                           xaxis=dict(showgrid=True, gridcolor='#f1f3f5'),
                           yaxis=dict(showgrid=True, gridcolor='#f1f3f5', title="Per Capita (t/person)"))
        st.plotly_chart(fig2, use_container_width=True, config=config)
        st.markdown(CITATION_HTML, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ================= ROW 2 =================
    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown(f"<h3>3. Regional Peer Comparison ({selected_years[1]})</h3>", unsafe_allow_html=True)
        compare_full_list = [target_country] + compare_list
        df_latest_compare = df[(df['Year'] == selected_years[1]) & (df['Country'].isin(compare_full_list))].sort_values(by='Per Capita CO2 (Mt)', ascending=True)

        fig3 = px.bar(df_latest_compare, x='Per Capita CO2 (Mt)', y='Country', orientation='h', text_auto='.2f', color='Country', color_discrete_map={target_country: C_MAIN})
        fig3.update_traces(marker_color=[C_MAIN if c == target_country else '#90caf9' for c in df_latest_compare['Country']], textposition="outside")

        layout_bar = layout_template.copy()
        layout_bar['margin'] = dict(l=100, r=20, t=40, b=40)
        fig3.update_layout(**layout_bar, showlegend=False, xaxis_title="Per Capita (t/person)", yaxis_title="")
        st.plotly_chart(fig3, use_container_width=True, config=config)
        st.markdown(CITATION_HTML, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("<h3>4. Economic Growth vs Carbon Output</h3>", unsafe_allow_html=True)
        df_scatter = df_filtered[df_filtered['Country'].isin(compare_full_list)]

        fig4 = px.scatter(df_scatter, x='GDP per Capita (Constant US$)', y='Total CO2 Emissions (Mt)', 
                          color='Country', hover_name='Country', size='Population', size_max=45,
                          opacity=0.75, color_discrete_map={target_country: C_MAIN})

        # FIXED LOG SCALES: Using dtick=1 forces Plotly to show exactly 1 tick per decade block.
        # This resolves the overlapping, "restarting" axis tick marks seen previously.
        fig4.update_layout(
            **layout_template,
            xaxis=dict(
                type='log',
                dtick=1, 
                showgrid=True, 
                gridcolor='#f1f3f5', 
                title="GDP per Capita ($) - Log"
            ),
            yaxis=dict(
                type='log',
                dtick=1, 
                showgrid=True, 
                gridcolor='#f1f3f5', 
                title="Total CO₂ (Mt) - Log"
            ),
            legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99, bgcolor="rgba(255,255,255,0.8)")
        )
        st.plotly_chart(fig4, use_container_width=True, config=config)
        st.markdown(CITATION_HTML, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ================= ROW 3 =================
    col5, col6 = st.columns(2)

    with col5:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown(f"<h3>5. Global Share of Emissions ({selected_years[1]})</h3>", unsafe_allow_html=True)
        target_share = latest_data['Share of Global CO2 (%)'] if 'Share of Global CO2 (%)' in latest_data else 0
        pie_data = pd.DataFrame({'Category': [target_country, 'Rest of the World'], 'Share (%)': [target_share, max(0, 100 - target_share)]})
        
        # Color updated to Light Green as requested
        fig6 = px.pie(pie_data, names='Category', values='Share (%)', hole=0.6, color='Category', 
                      color_discrete_map={target_country: C_MAIN, 'Rest of the World': '#a5d6a7'})
        
        fig6.update_layout(**layout_template, margin=dict(l=20, r=20, t=20, b=20), showlegend=False)
        fig6.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#ffffff', width=2)))
        st.plotly_chart(fig6, use_container_width=True, config=config)
        st.markdown(CITATION_HTML, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col6:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown(f"<h3>6. Emission Sources Breakdown ({target_country})</h3>", unsafe_allow_html=True)
        sources = ['Coal CO2 (Mt)', 'Oil CO2 (Mt)', 'Gas CO2 (Mt)', 'Cement CO2 (Mt)', 'Flaring CO2 (Mt)']
        source_colors = ['#455a64', '#1976d2', '#2e7d32', '#f57c00', '#7b1fa2'] 

        # Filter out missing columns silently
        available_sources = [s for s in sources if s in df_target.columns]
        
        if available_sources:
            df_sources = df_target[['Year'] + available_sources].melt(id_vars='Year', var_name='Source', value_name='Emissions')
            fig5 = px.bar(df_sources, x='Year', y='Emissions', color='Source', color_discrete_sequence=source_colors)
            fig5.update_layout(**layout_template, barmode='stack', yaxis_title="Emissions (Mt)",
                               xaxis=dict(showgrid=True, gridcolor='#f1f3f5'),
                               yaxis=dict(showgrid=True, gridcolor='#f1f3f5'),
                               legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.8)", title=""))
            st.plotly_chart(fig5, use_container_width=True, config=config)
        else:
            st.info("Source breakdown data not available for this region.")
            
        st.markdown(CITATION_HTML, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Footer / Download ---
    st.markdown("<div style='text-align: center; margin-top: 30px; margin-bottom: 50px;'>", unsafe_allow_html=True)
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download Current Dashboard Data", data=csv, file_name='Dashboard_Data_Export.csv', mime='text/csv')
    st.markdown("</div>", unsafe_allow_html=True)
