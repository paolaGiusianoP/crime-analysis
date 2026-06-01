import streamlit as st
from src.styles import load_css
from src.components import (
    render_page_header, render_section_title, render_kpi_grid,
    render_insight_card, render_footer
)

st.set_page_config(
    page_title="FBI Hate Crime Analysis",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 3rem;">⚖️</div>
        <div style="font-weight: 700; font-size: 1.2rem; color: #0F172A;">FBI Hate Crime</div>
        <div style="font-size: 0.8rem; color: #64748B;">Statistics 2020</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="background: #F8FAFC; border-radius: 0.75rem; padding: 1rem;">
        <div style="font-weight: 600; margin-bottom: 0.75rem;">📊 Dataset Overview</div>
        <div style="font-size: 0.85rem; line-height: 1.6;">
            • 8,263 Incidents<br>
            • 11,129 Offenses<br>
            • 11,472 Victims<br>
            • 6,780 Offenders
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.7rem; color: #94A3B8; text-align: center;">
        📅 FBI UCR Program • Hate Crime Statistics 2020
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# MAIN CONTENT
# ======================================================

# Hero Section
st.markdown("""
<div class="hero-card">
    <h1>⚖️ FBI Hate Crime Statistics 2020</h1>
    <p>
        Interactive dashboard to explore, visualize, and analyze hate crime incidents 
        reported by the FBI. Includes exploratory analysis, geographic visualization,
        risk classification, and actionable insights.
    </p>
</div>
""", unsafe_allow_html=True)

# Executive Summary KPIs
render_section_title("📊 Executive Summary")

kpis = [
    {"icon": "🚨", "value": 8263, "label": "Incidents"},
    {"icon": "📋", "value": 11129, "label": "Offenses"},
    {"icon": "👥", "value": 11472, "label": "Victims"},
    {"icon": "🔍", "value": 6780, "label": "Known Offenders"}
]
render_kpi_grid(kpis)

st.markdown("<br>", unsafe_allow_html=True)

# Dashboard Sections
render_section_title("📋 Dashboard Sections")

col1, col2, col3, col4 = st.columns(4)

sections = [
    {"icon": "📊", "title": "Overview", "desc": "Executive summary and key KPIs"},
    {"icon": "📈", "title": "Exploration", "desc": "Bias motivations and offense patterns"},
    {"icon": "🗺️", "title": "Risk Map", "desc": "Geographic visualization & risk classification"},
    {"icon": "💡", "title": "Insights", "desc": "Key findings and recommendations"}
]

for col, section in zip([col1, col2, col3, col4], sections):
    with col:
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2.5rem;">{section['icon']}</div>
            <h4 style="color: #0EA5E9; margin-bottom: 0.5rem;">{section['title']}</h4>
            <p style="font-size: 0.85rem; color: #64748B;">{section['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Key Highlights
render_section_title("🔍 Key Highlights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="insight-card">
        <h4>🏷️ Predominant Bias</h4>
        <p>Race and ethnicity motivated incidents represent the most frequent category (63.3% of total).</p>
        <div style="background: #E0F2FE; border-radius: 0.75rem; padding: 0.75rem; margin-top: 1rem;">
            <strong>5,227 incidents</strong> <span style="color: #64748B;">(63.3% of total)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="insight-card">
        <h4>📍 Geographic Concentration</h4>
        <p>Hate crimes are concentrated in California, Texas, and New York.</p>
        <div style="background: #FEF3C7; border-radius: 0.75rem; padding: 0.75rem; margin-top: 1rem;">
            <strong>Top 3 states</strong> <span style="color: #64748B;">represent 28% of all offenses</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Quick Statistics
render_section_title("📈 Quick Statistics")

col1, col2, col3 = st.columns(3)

quick_stats = [
    {"icon": "🏷️", "value": "63.3%", "label": "Race/Ethnicity Bias", "sub": "Most common bias"},
    {"icon": "👥", "value": "1.39", "label": "Victims per Incident", "sub": "Average victims"},
    {"icon": "📋", "value": "4,119", "label": "Intimidation Offenses", "sub": "Most common offense"}
]

for col, stat in zip([col1, col2, col3], quick_stats):
    with col:
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2rem;">{stat['icon']}</div>
            <div style="font-size: 2rem; font-weight: 700; color: #0EA5E9;">{stat['value']}</div>
            <div style="color: #64748B;">{stat['label']}</div>
            <div style="font-size: 0.7rem; color: #94A3B8; margin-top: 0.5rem;">{stat['sub']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# About Section
render_section_title("📖 About This Project")

with st.expander("📋 Click to view details", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📌 Data Source
        | Aspect | Details |
        |--------|---------|
        | **Source** | FBI Uniform Crime Reporting (UCR) |
        | **Year** | 2020 |
        | **Dataset** | Hate Crime Statistics |
        | **Coverage** | National |
        """)
    
    with col2:
        st.markdown("""
        ### 🛠 Technologies
        | Stack | Technology |
        |-------|------------|
        | **Language** | Python 3.11+ |
        | **Framework** | Streamlit |
        | **Data Processing** | Pandas, NumPy |
        | **Visualization** | Plotly, Matplotlib |
        """)

render_footer()