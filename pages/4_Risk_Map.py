import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px

sys.path.append(str(Path(__file__).parent.parent))

from src.data_loader import load_all_tables
from src.styles import load_css
from src.utils import filter_state_data, format_number
from src.components import (
    render_page_header, render_section_title, render_metric_card,
    render_insight_card, render_footer
)
from src.charts import create_us_choropleth
from src.constants import COLORS

st.set_page_config(
    page_title="Risk Map - FBI Hate Crime",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()
render_page_header(
    "Mapa de Riesgo y Clustering",
    "Visualización geoespacial de crímenes de odio por estado y clasificación de niveles de riesgo",
    "🗺️"
)

# LOAD DATA
with st.spinner("Cargando datos y generando visualizaciones..."):
    data = load_all_tables()
    state_df = data.get("offenses_by_state")

if state_df is not None:
    
    state_df, state_col, total_col = filter_state_data(state_df)
    
    if total_col and not state_df.empty:
        
        # Preparar datos para el mapa
        map_df = state_df[[state_col, total_col]].copy()
        map_df.columns = ["state", "offenses"]
        map_df["offenses_formatted"] = map_df["offenses"].apply(format_number)
        
        # MAPA 
        render_section_title("🗺️ Mapa de Calor: Crímenes de Odio por Estado")
        
        fig_map = create_us_choropleth(
            map_df,
            location_col="state",
            value_col="offenses",
            color_scale="Reds",
            height=600
        )
        st.plotly_chart(fig_map, width='stretch')
        
        # Estadísticas del mapa
        col1, col2, col3 = st.columns(3)
        
        max_state = map_df.loc[map_df['offenses'].idxmax(), 'state']
        max_value = int(map_df['offenses'].max())
        
        min_state = map_df.loc[map_df['offenses'].idxmin(), 'state']
        min_value = int(map_df['offenses'].min())
        
        avg_offenses = int(map_df['offenses'].mean())
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🔴</div>
                <div class="metric-value">{max_state}</div>
                <div class="metric-label">{format_number(max_value)} ofensas</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🟢</div>
                <div class="metric-value">{min_state}</div>
                <div class="metric-label">{format_number(min_value)} ofensas</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            render_metric_card("📊", avg_offenses, "Promedio por estado")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # CLASIFICACIÓN POR RIESGO
        render_section_title("📊 Clasificación de Estados por Nivel de Riesgo")
        
        # Calcular percentiles para riesgo
        high_risk_threshold = state_df[total_col].quantile(0.75)
        medium_risk_threshold = state_df[total_col].quantile(0.5)
        
        def get_risk_level(offenses):
            if offenses >= high_risk_threshold:
                return "Alto Riesgo"
            elif offenses >= medium_risk_threshold:
                return "Riesgo Medio"
            else:
                return "Bajo Riesgo"
        
        state_df["Nivel de Riesgo"] = state_df[total_col].apply(get_risk_level)
        
        # Resumen de riesgo
        col1, col2, col3 = st.columns(3)
        
        risk_stats = {}
        for risk_level in ["Alto Riesgo", "Riesgo Medio", "Bajo Riesgo"]:
            risk_stats[risk_level] = {
                "count": len(state_df[state_df['Nivel de Riesgo'] == risk_level]),
                "offenses": state_df[state_df['Nivel de Riesgo'] == risk_level][total_col].sum()
            }
        
        total_offenses = sum(s["offenses"] for s in risk_stats.values())
        
        risk_colors = {
            "Alto Riesgo": ("🔴", "#EF4444"),
            "Riesgo Medio": ("🟡", "#F59E0B"),
            "Bajo Riesgo": ("🟢", "#10B981")
        }
        
        cols = [col1, col2, col3]
        for idx, (risk_level, stats) in enumerate(risk_stats.items()):
            icon, color = risk_colors[risk_level]
            with cols[idx]:
                st.markdown(f"""
                <div class="card" style="text-align: center; border-top: 4px solid {color};">
                    <div style="font-size: 2rem;">{icon}</div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: {color};">{stats['count']}</div>
                    <div>{risk_level}</div>
                    <div style="font-size: 0.8rem; color: #64748B;">{stats['offenses']/total_offenses*100:.1f}% de ofensas</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Top 10 estados con más ofensas
        render_section_title("🏆 Top 10 Estados con Mayor Riesgo")
        
        top_10 = state_df.nlargest(10, total_col)[[state_col, total_col, "Nivel de Riesgo"]]
        top_10.columns = ["Estado", "Ofensas", "Nivel de Riesgo"]
        top_10["Ofensas"] = top_10["Ofensas"].apply(format_number)
        
        st.dataframe(
            top_10,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráfico de barras por riesgo
        render_section_title("📊 Distribución de Ofensas por Nivel de Riesgo")
        
        risk_summary = state_df.groupby("Nivel de Riesgo")[total_col].sum().sort_values(ascending=False)
        
        risk_colors_map = {
            "Alto Riesgo": "#EF4444",
            "Riesgo Medio": "#F59E0B",
            "Bajo Riesgo": "#10B981"
        }
        
        fig_risk = px.bar(
            x=risk_summary.index,
            y=risk_summary.values,
            color=risk_summary.index,
            color_discrete_map=risk_colors_map,
            text=risk_summary.values,
            labels={"x": "Nivel de Riesgo", "y": "Total de Ofensas"}
        )
        
        fig_risk.update_traces(
            texttemplate='%{text:,}',
            textposition='outside'
        )
        
        fig_risk.update_layout(
            title=dict(
                text="Concentración de Crímenes de Odio por Nivel de Riesgo",
                font=dict(size=16, weight="bold", color="#0F172A")
            ),
            height=450,
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            xaxis=dict(title="", gridcolor="#F1F5F9"),
            yaxis=dict(title="Total de Ofensas", gridcolor="#F1F5F9")
        )
        
        st.plotly_chart(fig_risk, width='stretch')
        
        render_insight_card(
            "Los estados de Alto Riesgo, aunque son una minoría (aproximadamente el 25% de los estados), "
            "concentran una proporción desproporcionada de los crímenes de odio. Esto sugiere que los "
            "esfuerzos de prevención e intervención deberían priorizar estas jurisdicciones para "
            "maximizar el impacto de los recursos disponibles."
        )
        
        # Mapa de riesgo clasificado
        render_section_title("Mapa de Riesgo por Estado")
        
        risk_map_df = state_df[[state_col, "Nivel de Riesgo"]].copy()
        risk_map_df.columns = ["state", "risk_level"]
        
        fig_risk_map = px.choropleth(
            risk_map_df,
            locations="state",
            locationmode="USA-states",
            color="risk_level",
            scope="usa",
            title="",
            color_discrete_map=risk_colors_map,
            hover_data={"state": True}
        )
        
        fig_risk_map.update_layout(
            title_x=0.5,
            geo=dict(
                bgcolor='rgba(0,0,0,0)',
                lakecolor='#E2E8F0',
                landcolor='#F8FAFC',
                subunitcolor='#CBD5E1',
                showframe=False
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            height=550,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        st.plotly_chart(fig_risk_map, width='stretch')
        
    else:
        st.error("No se encontró la columna de total de ofensas en el dataset")
else:
    st.error("No se encontraron datos de estados. Verifica que Table_11 esté en la carpeta 'data'")

# FOOTER
render_footer(
    "🗺️ Clasificación basada en percentiles • Alto Riesgo > P75 • Riesgo Medio P50-P75 • Bajo Riesgo < P50"
)