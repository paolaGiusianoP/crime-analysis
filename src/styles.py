import streamlit as st
import datetime

def load_css():
    version = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    st.markdown(
        f"""
<style>
/* Version: {version} */

@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;400;500;600;700;800&display=swap');

* {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background-color: #F8FAFC;
}}

#MainMenu, header, footer {{
    visibility: hidden;
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #FFFFFF 0%, #F1F5F9 100%);
    border-right: 1px solid #E2E8F0;
}}

[data-testid="stSidebar"] * {{
    color: #334155;
}}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {{
    color: #0F172A !important;
}}

h1, h2, h3, h4, h5, h6 {{
    font-weight: 600;
    letter-spacing: -0.02em;
}}

.page-title {{
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #0F172A 0%, #0EA5E9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}}

.section-title {{
    font-size: 1.5rem;
    font-weight: 700;
    color: #0F172A;
    border-left: 5px solid #0EA5E9;
    padding-left: 1rem;
    margin: 1.5rem 0 1.5rem 0;
    letter-spacing: -0.01em;
}}

.card {{
    background: #FFFFFF;
    border-radius: 1rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    transition: all 0.2s ease;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}}

.card:hover {{
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.08);
    transform: translateY(-2px);
}}

.hero-card {{
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    border-radius: 1.5rem;
    padding: 2.5rem;
    margin-bottom: 2rem;
    border: none;
}}

.hero-card h1, .hero-card h2 {{
    color: white;
    font-size: 2.2rem;
    margin-bottom: 1rem;
    background: none;
    -webkit-text-fill-color: white;
}}

.hero-card p {{
    color: #CBD5E1;
    font-size: 1rem;
    max-width: 80%;
}}

.metric-card {{
    background: white;
    border-radius: 1rem;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid #E2E8F0;
    transition: all 0.2s;
}}

.metric-icon {{
    font-size: 2rem;
    margin-bottom: 0.75rem;
}}

.metric-value {{
    font-size: 2rem;
    font-weight: 800;
    color: #0EA5E9;
    margin-bottom: 0.25rem;
}}

.metric-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    font-weight: 600;
    color: #64748B;
    letter-spacing: 0.05em;
}}

.insight-card {{
    background: #F0F9FF;
    border-left: 4px solid #0EA5E9;
    border-radius: 0.75rem;
    padding: 1.25rem;
    margin: 1rem 0;
}}

.insight-card h4 {{
    color: #0369A1;
    margin-bottom: 0.5rem;
}}

.info-card {{
    background: #F8FAFC;
    border-radius: 0.75rem;
    padding: 1.25rem;
    margin: 1rem 0;
    border: 1px solid #E2E8F0;
}}

.warning-card {{
    background: #FFFBEB;
    border-left: 4px solid #F59E0B;
    border-radius: 0.75rem;
    padding: 1.25rem;
}}

.stTabs [data-baseweb="tab-list"] {{
    background: white;
    border-radius: 0.75rem;
    padding: 0.5rem;
    gap: 0.5rem;
    border: 1px solid #E2E8F0;
    margin-bottom: 1.5rem;
}}

.stTabs [data-baseweb="tab"] {{
    border-radius: 0.5rem;
    padding: 0.5rem 1.5rem;
    font-weight: 500;
    color: #475569;
}}

.stTabs [aria-selected="true"] {{
    background: #0EA5E9 !important;
    color: white !important;
    box-shadow: none;
}}

[data-testid="stDataFrame"] {{
    border-radius: 0.75rem;
    overflow: hidden;
    border: 1px solid #E2E8F0;
}}

.stButton > button {{
    background: #0EA5E9;
    color: white;
    border-radius: 0.5rem;
    font-weight: 500;
    border: none;
}}

.stButton > button:hover {{
    background: #0284C7;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}}

[data-testid="stMetric"] {{
    background: white;
    border-radius: 0.75rem;
    padding: 1rem;
    border: 1px solid #E2E8F0;
}}

[data-testid="stMetricValue"] {{
    color: #0EA5E9;
    font-weight: 700;
}}

.custom-footer {{
    margin-top: 3rem;
    text-align: center;
    color: #94A3B8;
    font-size: 0.75rem;
    padding-top: 1.5rem;
    border-top: 1px solid #E2E8F0;
}}

@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.metric-card, .card, .hero-card, .insight-card {{
    animation: fadeInUp 0.3s ease-out;
}}

@media (max-width: 768px) {{
    .hero-card h1, .hero-card h2 {{ font-size: 1.8rem; }}
    .hero-card {{ padding: 1.5rem; }}
    .metric-value {{ font-size: 1.5rem; }}
    .section-title {{ font-size: 1.2rem; }}
    .page-title {{ font-size: 1.8rem; }}
}}
</style>
""",
        unsafe_allow_html=True,
    )
