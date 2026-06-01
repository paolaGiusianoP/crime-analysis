import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px

sys.path.append(str(Path(__file__).parent.parent))

from src.data_loader import load_all_tables
from src.styles import load_css
from src.utils import get_kpi_data, get_single_vs_multiple, filter_state_data, format_number
from src.components import (
    render_page_header, render_section_title, render_metric_card,render_footer
)
from src.charts import create_bar_chart, create_donut_chart
from src.constants import COLORS

st.set_page_config(
    page_title="Insights - FBI Hate Crime",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()
render_page_header(
    "Insights y Recomendaciones",
    "Hallazgos clave, tendencias y recomendaciones estratégicas derivadas del análisis de crímenes de odio del FBI 2020",
    "💡"
)

# LOAD DATA
with st.spinner("Cargando datos del FBI..."):
    data = load_all_tables()

incidents = data.get("incidents")
offenses_by_state = data.get("offenses_by_state")

# MAIN KPIs
if incidents is not None and not incidents.empty:
    kpis = get_kpi_data(incidents)
    
    render_section_title("📊 Estadísticas Clave")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card("🚨", kpis["incidents"], "Incidentes")
    with col2:
        render_metric_card("📋", kpis["offenses"], "Ofensas")
    with col3:
        render_metric_card("👥", kpis["victims"], "Víctimas")
    with col4:
        render_metric_card("🔍", kpis["offenders"], "Ofensores Conocidos")
    
    st.markdown("<br>", unsafe_allow_html=True)

# INCIDENT DISTRIBUTION
if incidents is not None:
    bias_data = get_single_vs_multiple(incidents)
    
    if bias_data["single"] > 0:
        render_section_title("📈 Distribución de Incidentes")
        
        total_val = bias_data["single"] + bias_data["multiple"]
        single_pct = bias_data["single"] / total_val * 100
        multi_pct = bias_data["multiple"] / total_val * 100
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            fig = create_donut_chart(
                values=[bias_data["single"], bias_data["multiple"]],
                labels=["Bias Único", "Múltiples Bias"],
                title=None,
                colors=[COLORS["primary"], COLORS["secondary"]]
            )
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            st.markdown(f"""
            <div class="info-card">
                <strong>✅ Incidentes de Bias Único</strong>
                <div style="font-size:1.8rem;font-weight:bold;color:{COLORS['primary']};margin:10px 0;">
                    {format_number(bias_data['single'])}
                </div>
                <span style="color:#64748b;">({single_pct:.1f}% del total)</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="warning-card">
                <strong>⚠️ Incidentes de Múltiples Bias</strong>
                <div style="font-size:1.8rem;font-weight:bold;color:{COLORS['secondary']};margin:10px 0;">
                    {format_number(bias_data['multiple'])}
                </div>
                <span style="color:#64748b;">({multi_pct:.1f}% del total)</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

# TOP STATES
if offenses_by_state is not None:
    render_section_title("🏆 Estados con Mayor Actividad")
    
    state_df, state_col, total_col = filter_state_data(offenses_by_state)
    
    if total_col and not state_df.empty:
        top_states = state_df.nlargest(10, total_col)[[state_col, total_col]].copy()
        top_states.columns = ["Estado", "Ofensas"]
        
        fig = create_bar_chart(
            top_states,
            x_col="Ofensas",
            y_col="Estado",
            title="Top 10 Estados por Ofensas",
            height=500
        )
        st.plotly_chart(fig, width='stretch')
        
        st.markdown("<br>", unsafe_allow_html=True)

render_section_title("🔍 Hallazgos Clave")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <strong>📊 Patrones Principales</strong>
        <ul style="margin: 0.5rem 0 0 1.2rem; padding-left: 0; line-height: 1.6;">
            <li>La mayoría de los incidentes registrados están asociados con una única motivación de bias</li>
            <li>La actividad de crímenes de odio se concentra en un grupo reducido de estados</li>
            <li>El número de víctimas supera al de incidentes, evidenciando eventos con múltiples afectados</li>
            <li>Existe una distribución geográfica desigual que permite focalizar programas preventivos</li>
            <li>La intimidación es el tipo de ofensa más común, seguida por vandalismo y daños a la propiedad</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if incidents is not None:
        bias_df = incidents.copy()
        bias_df = bias_df[~bias_df["Bias motivation"].isin(
            ["Total", "Single-Bias Incidents", "Multiple-Bias Incidents3"]
        )]
        bias_df["Incidents"] = pd.to_numeric(bias_df["Incidents"], errors="coerce")
        bias_df = bias_df.dropna()
        top3 = bias_df.nlargest(3, "Incidents")
        
        st.markdown("""
        <div class="info-card">
            <strong>🎯 Bias Más Frecuentes</strong>
        </div>
        """, unsafe_allow_html=True)
        
        for _, row in top3.iterrows():
            st.metric(row["Bias motivation"], format_number(row["Incidents"]))
        
        st.info("ℹ️ El bias racial y étnico representa la mayor proporción de incidentes reportados (>63%)")

# RECOMMENDATIONS 
render_section_title("💡 Recomendaciones Estratégicas")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <strong>🎓 Educación y Concientización</strong><br><br>
        Expandir programas educativos sobre diversidad, inclusión y prevención de conductas discriminatorias en escuelas y comunidades.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <strong>📍 Asignación Estratégica de Recursos</strong><br><br>
        Dirigir recursos policiales y programas de prevención a estados y comunidades con mayor concentración de incidentes (California, Texas, Nueva York).
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <strong>📊 Mejora de Calidad de Datos</strong><br><br>
        Incentivar una mayor participación de agencias locales y federales para mejorar la cobertura estadística y obtener datos más precisos.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <strong>🔬 Investigación y Análisis Futuro</strong><br><br>
        Incorporar análisis per cápita y tendencias multianuales para obtener conclusiones más robustas sobre la evolución de los crímenes de odio.
    </div>
    """, unsafe_allow_html=True)


if incidents is not None:
    kpis = get_kpi_data(incidents)
    
    render_section_title("📊 Análisis de Ratios")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        offenses_ratio = kpis["offenses"] / kpis["incidents"]
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2rem;">📋</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: {COLORS['primary']};">{offenses_ratio:.2f}</div>
            <div>Ofensas por Incidente</div>
            <div style="font-size: 0.7rem; color: #64748B;">Cada incidente genera múltiples ofensas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        victims_ratio = kpis["victims"] / kpis["incidents"]
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2rem;">👥</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: {COLORS['primary']};">{victims_ratio:.2f}</div>
            <div>Víctimas por Incidente</div>
            <div style="font-size: 0.7rem; color: #64748B;">Incidentes con múltiples víctimas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if kpis["offenders"] > 0:
            offenders_ratio = kpis["victims"] / kpis["offenders"]
            st.markdown(f"""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2rem;">⚖️</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: {COLORS['primary']};">{offenders_ratio:.2f}</div>
                <div>Víctimas por Ofensor</div>
                <div style="font-size: 0.7rem; color: #64748B;">Ofensores con múltiples víctimas</div>
            </div>
            """, unsafe_allow_html=True)


render_section_title("📌 Resumen Ejecutivo")

summary_col1, summary_col2 = st.columns([1.2, 1])

with summary_col1:
    st.markdown("""
    <div class="insight-card">
        <h4>📌 Conclusión General</h4>
        <p>
        El análisis evidencia que los crímenes de odio registrados por el FBI durante 2020 estuvieron
        fuertemente concentrados en motivaciones raciales y étnicas, representando más del 63% de todos los incidentes.
        </p>
        <p>
        Asimismo, una cantidad reducida de estados (California, Texas y Nueva York) concentró gran parte de las ofensas reportadas,
        sugiriendo la necesidad de intervenciones focalizadas.
        </p>
        <p>
        Los resultados destacan la importancia de fortalecer programas educativos, mejorar los mecanismos de reporte
        y ampliar la cobertura de los datos nacionales para combatir efectivamente este problema social.
        </p>
    </div>
    """, unsafe_allow_html=True)

with summary_col2:
    if incidents is not None:
        kpis = get_kpi_data(incidents)
        st.markdown(f"""
        <div class="card" style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 1.2rem; font-weight: 600;">Total Incidentes</div>
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS['primary']};">{format_number(kpis['incidents'])}</div>
        </div>
        <div class="card" style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 1.2rem; font-weight: 600;">Total Ofensas</div>
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS['primary']};">{format_number(kpis['offenses'])}</div>
        </div>
        <div class="card" style="text-align: center;">
            <div style="font-size: 1.2rem; font-weight: 600;">Total Víctimas</div>
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS['primary']};">{format_number(kpis['victims'])}</div>
        </div>
        """, unsafe_allow_html=True)

# LIMITATIONS
render_section_title("⚠️ Limitaciones del Análisis")

with st.expander("📋 Ver limitaciones del análisis", expanded=False):
    st.markdown("""
    - **Dependencia de agencias participantes:** Los datos dependen de la participación voluntaria de agencias locales y federales.
    - **Subreporte significativo:** Muchos crímenes de odio no son reportados debido al miedo, desconfianza o desconocimiento.
    - **Cobertura limitada:** Algunas jurisdicciones reportaron cero incidentes, lo que no necesariamente refleja la realidad.
    - **Análisis de un solo año:** El análisis cubre únicamente el año 2020, que fue atípico debido a la pandemia de COVID-19.
    - **Sin ajuste poblacional:** No se consideran métricas ajustadas por población para comparación justa entre estados.
    - **Diferencias en reportes:** Los resultados pueden verse afectados por diferencias en los mecanismos de reporte entre jurisdicciones.
    """)

render_footer()