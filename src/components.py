import streamlit as st
import pandas as pd

from src.constants import COLORS, BIAS_CATEGORIES, BIAS_DISPLAY_NAMES


def format_number(value) -> str:
    if isinstance(value, (int, float)):
        return f"{int(value):,}"
    return str(value)


def render_page_header(title: str, description: str, icon: str = "📊"):
    st.markdown(f"""
    <div class="page-header">
        <h1 class="page-title">{icon} {title}</h1>
        <p style="color: {COLORS['gray']}; margin-top: 0.5rem;">{description}</p>
    </div>
    """, unsafe_allow_html=True)


def render_section_title(title: str):
    st.markdown(f'<h2 class="section-title">{title}</h2>', unsafe_allow_html=True)


def render_metric_card(icon: str, value, label: str, color: str = None):
    color = color or COLORS["primary"]
    formatted_value = format_number(value)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value" style="color: {color};">{formatted_value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_grid(kpis: list, cols: int = 4):
    columns = st.columns(cols)
    for idx, kpi in enumerate(kpis):
        with columns[idx % cols]:
            render_metric_card(kpi["icon"], kpi["value"], kpi["label"])


def render_info_card(content: str, title: str = None):
    st.markdown(f"""
    <div class="info-card">
        {f"<h4>{title}</h4>" if title else ""}
        {content}
    </div>
    """, unsafe_allow_html=True)


def render_insight_card(content: str, title: str = "💡 Insight Clave"):
    st.markdown(f"""
    <div class="insight-card">
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


def render_warning_card(content: str, title: str = "⚠️ Atención"):
    st.markdown(f"""
    <div class="warning-card">
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


def render_footer(text: str = None):
    default_text = "📊 FBI Uniform Crime Reporting (UCR) Program • Hate Crime Statistics 2020 • Built with Streamlit"
    st.markdown(f"""
    <div class="custom-footer">
        {text or default_text}
    </div>
    """, unsafe_allow_html=True)


def render_bias_category_summary(bias_df: pd.DataFrame):
    total_all = bias_df["Incidents"].sum()
    
    for category_key, keywords in BIAS_CATEGORIES.items():
        category_total = bias_df[
            bias_df["Bias motivation"].str.contains("|".join(keywords), case=False, na=False)
        ]["Incidents"].sum()
        
        display = BIAS_DISPLAY_NAMES.get(category_key, {"icon": "📌", "name": category_key})
        
        st.markdown(f"""
        <div class="info-card">
            <strong>{display['icon']} {display['name']}</strong><br>
            <span style="font-size: 1.5rem; font-weight: 700; color: {COLORS['primary']};">{format_number(category_total)}</span>
            <span style="color: {COLORS['gray']};"> ({category_total/total_all*100:.1f}%)</span>
        </div>
        """, unsafe_allow_html=True)


def render_loading_spinner(message: str = "Cargando datos..."):
    return st.spinner(message)