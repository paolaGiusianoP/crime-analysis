import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.data_loader import load_all_tables
from src.styles import load_css
from src.utils import get_kpi_data, get_single_vs_multiple, get_top_bias, format_number
from src.components import (
    render_page_header, render_section_title, render_kpi_grid,
    render_insight_card, render_footer
)
from src.charts import create_donut_chart, create_bar_chart

st.set_page_config(
    page_title="Overview - FBI Hate Crime",
    page_icon="⚖️",
    layout="wide"
)

load_css()
render_page_header(
    "Resumen General",
    "Vista completa de las estadísticas de crímenes de odio reportadas por el FBI durante 2020",
    "📊"
)

# LOAD DATA

with st.spinner("Cargando datos del FBI..."):
    data = load_all_tables()
    incidents = data.get("incidents")

if incidents is not None and not incidents.empty:
    
    # KPIs principales
    kpis = get_kpi_data(incidents)
    render_section_title("📊 Estadísticas Clave")
    
    render_kpi_grid([
        {"icon": "🚨", "value": kpis["incidents"], "label": "Incidentes"},
        {"icon": "📋", "value": kpis["offenses"], "label": "Ofensas"},
        {"icon": "👥", "value": kpis["victims"], "label": "Víctimas"},
        {"icon": "🔍", "value": kpis["offenders"], "label": "Ofensores Conocidos"}
    ])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    bias_data = get_single_vs_multiple(incidents)
    
    if bias_data["single"] > 0:
        render_section_title("📊 Distribución de Incidentes")
        
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            fig = create_donut_chart(
                values=[bias_data["single"], bias_data["multiple"]],
                labels=["Bias Único", "Múltiples Bias"],
                title="Incidentes por tipo de bias",
                colors=["#0EA5E9", "#F59E0B"]
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            total = bias_data["single"] + bias_data["multiple"]
            single_pct = bias_data["single"] / total * 100
            multi_pct = bias_data["multiple"] / total * 100
            
            st.markdown(f"""
            <div class="insight-card">
                <h4>✅ Incidentes de Bias Único</h4>
                <div style="font-size: 2rem; font-weight: 700; color: #0EA5E9;">{format_number(bias_data['single'])}</div>
                <p>{single_pct:.1f}% del total</p>
            </div>
            <div class="warning-card" style="margin-top: 1rem;">
                <h4>⚠️ Incidentes de Múltiples Bias</h4>
                <div style="font-size: 2rem; font-weight: 700; color: #F59E0B;">{format_number(bias_data['multiple'])}</div>
                <p>{multi_pct:.1f}% del total</p>
            </div>
            """, unsafe_allow_html=True)
        
        render_insight_card(
            "La mayoría de los crímenes de odio están asociados con una única motivación de bias. "
            "El bias racial y étnico sigue siendo la categoría dominante en todo el conjunto de datos.",
            "💡 Insight Clave"
        )
    
    # Top Bias Motivations
    render_section_title("🏷️ Principales Motivaciones de Bias")
    
    top_bias_df = get_top_bias(incidents, n=10)
    
    if not top_bias_df.empty:
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            fig = create_bar_chart(
                top_bias_df,
                x_col="Incidents",
                y_col="Bias motivation",
                title="Top 10 Motivaciones de Bias",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown('<div class="card"><h4>📋 Top 10 Bias</h4></div>', unsafe_allow_html=True)
            display_df = top_bias_df.copy()
            display_df["Incidents"] = display_df["Incidents"].apply(format_number)
            display_df.columns = ["Motivación", "Incidentes"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    render_section_title("📊 Análisis de Ratios")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2rem;">📋</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #0EA5E9;">{kpis['offenses']/kpis['incidents']:.2f}</div>
            <div>Ofensas por Incidente</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2rem;">👥</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #0EA5E9;">{kpis['victims']/kpis['incidents']:.2f}</div>
            <div>Víctimas por Incidente</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        victims_per_offender = kpis['victims'] / kpis['offenders'] if kpis['offenders'] > 0 else 0
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2rem;">⚖️</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #0EA5E9;">{victims_per_offender:.2f}</div>
            <div>Víctimas por Ofensor</div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.error("No se pudieron cargar los datos. Verifica que los archivos Excel estén en la carpeta 'data'.")

render_footer()