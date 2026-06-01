import streamlit as st
import sys
from pathlib import Path
import pandas as pd 

sys.path.append(str(Path(__file__).parent.parent))

from src.data_loader import load_all_tables
from src.styles import load_css
from src.utils import filter_bias_data, filter_state_data, format_number
from src.components import (
    render_page_header, render_section_title, render_metric_card,
    render_insight_card, render_footer, render_bias_category_summary
)
from src.charts import create_bar_chart
from src.constants import TAB_NAMES

st.set_page_config(
    page_title="Exploratory Analysis - FBI Hate Crime",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()
render_page_header(
    "Análisis Exploratorio",
    "Exploración profunda de las estadísticas de crímenes de odio del FBI 2020. "
    "Analiza motivaciones, patrones de ofensas y distribución geográfica.",
    "📈"
)

# LOAD DATA

with st.spinner("Cargando datos del FBI..."):
    data = load_all_tables()

incidents = data.get("incidents")

# KPI SECTION
if incidents is not None and not incidents.empty:
    
    bias_df = filter_bias_data(incidents)
    total_incidents = int(bias_df["Incidents"].sum())
    top_bias = bias_df.sort_values("Incidents", ascending=False).iloc[0]["Bias motivation"]
    total_categories = bias_df["Bias motivation"].nunique()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_metric_card("📊", total_incidents, "Total Incidentes")
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🏷️</div>
            <div class="metric-value">{top_bias[:30]}</div>
            <div class="metric-label">Motivación Principal</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        render_metric_card("📂", total_categories, "Categorías de Bias")
    
    st.markdown("<br>", unsafe_allow_html=True)

# TABS
tab1, tab2, tab3 = st.tabs([
    TAB_NAMES["bias"],
    TAB_NAMES["offenses"],
    TAB_NAMES["states"]
])

# TAB 1: BIAS MOTIVATIONS
with tab1:
    render_section_title("Análisis de Motivaciones de Bias")
    
    if incidents is not None and not incidents.empty:
        
        bias_df = filter_bias_data(incidents)
        
        if not bias_df.empty:
            
            top20_df = bias_df.nlargest(20, "Incidents")
            
            fig = create_bar_chart(
                top20_df,
                x_col="Incidents",
                y_col="Bias motivation",
                title="Top 20 Motivaciones de Bias",
                height=700
            )
            st.plotly_chart(fig, width='stretch')
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="card"><h4>📊 Resumen por Categoría</h4></div>', unsafe_allow_html=True)
                render_bias_category_summary(bias_df)
            
            with col2:
                st.markdown('<div class="card"><h4>📋 Tabla de Datos</h4></div>', unsafe_allow_html=True)
                
                display_df = bias_df[["Bias motivation", "Incidents"]].copy()
                display_df.columns = ["Motivación de Bias", "Incidentes"]
                display_df["Incidentes"] = display_df["Incidentes"].apply(format_number)
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )
            
            render_insight_card(
                "Las motivaciones basadas en raza y etnia representan la mayoría de los incidentes "
                "de crímenes de odio. El bias anti-negro o afroamericano sigue siendo la categoría "
                "más frecuentemente reportada, seguida por anti-blanco y anti-judío."
            )
        
        else:
            st.warning("No hay datos de bias disponibles")
    else:
        st.error("No se encontró la tabla de incidentes")

# TAB 2: OFFENSE TYPES
with tab2:
    render_section_title("Análisis de Tipos de Ofensas")
    
    offenses = data.get("offenses_by_type")
    
    if offenses is not None and not offenses.empty:
        
        off_df = offenses.copy()
        off_df = off_df[~off_df["Offense type"].isin([
            "Total", "Crimes against persons:", "Crimes against property:", 
            "Crimes against society5"
        ])]
        off_df["Offenses"] = pd.to_numeric(off_df["Offenses"], errors="coerce").fillna(0)
        off_df = off_df[off_df["Offenses"] > 0]
        off_df = off_df.sort_values("Offenses", ascending=False)
        
        if not off_df.empty:
            
            col1, col2 = st.columns([1.2, 1])
            
            with col1:
                fig = create_bar_chart(
                    off_df,
                    x_col="Offenses",
                    y_col="Offense type",
                    title="Distribución de Tipos de Ofensas",
                    height=600
                )
                st.plotly_chart(fig, width='stretch')
            
            with col2:
                st.markdown('<div class="card"><h4>📋 Top 10 Ofensas</h4></div>', unsafe_allow_html=True)
                
                display_off = off_df.head(10)[["Offense type", "Offenses"]].copy()
                display_off.columns = ["Tipo de Ofensa", "Número de Ofensas"]
                display_off["Número de Ofensas"] = display_off["Número de Ofensas"].apply(format_number)
                
                st.dataframe(
                    display_off,
                    use_container_width=True,
                    hide_index=True
                )
            
            # Estadísticas adicionales
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            # Buscar valores específicos
            intimidation = off_df[off_df["Offense type"] == "Intimidation"]["Offenses"].values[0] if len(off_df[off_df["Offense type"] == "Intimidation"]) > 0 else 0
            vandalism = off_df[off_df["Offense type"] == "Destruction/damage/vandalism"]["Offenses"].values[0] if len(off_df[off_df["Offense type"] == "Destruction/damage/vandalism"]) > 0 else 0
            assault = off_df[off_df["Offense type"] == "Simple assault"]["Offenses"].values[0] if len(off_df[off_df["Offense type"] == "Simple assault"]) > 0 else 0
            
            with col1:
                st.markdown(f"""
                <div class="info-card" style="text-align: center;">
                    <div style="font-size: 2rem;">😨</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #0EA5E9;">{format_number(intimidation)}</div>
                    <div>Ofensas por Intimidación</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="info-card" style="text-align: center;">
                    <div style="font-size: 2rem;">💔</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #0EA5E9;">{format_number(vandalism)}</div>
                    <div>Destrucción/Vandalismo</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="info-card" style="text-align: center;">
                    <div style="font-size: 2rem;">👊</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #0EA5E9;">{format_number(assault)}</div>
                    <div>Asaltos Simples</div>
                </div>
                """, unsafe_allow_html=True)
            
            render_insight_card(
                "La intimidación es, con diferencia, el tipo de ofensa más común, seguida por "
                "vandalismo/destrucción de propiedad y asalto simple. Esto sugiere que muchos "
                "crímenes de odio involucran amenazas y daños a la propiedad más que violencia física severa."
            )
        
        else:
            st.warning("No hay datos de ofensas disponibles")
    else:
        st.error("No se encontró la tabla de ofensas")

# TAB 3: STATES ANALYSIS
with tab3:
    render_section_title("Análisis por Estado")
    
    state_df = data.get("offenses_by_state")
    
    if state_df is not None and not state_df.empty:
        
        state_df, state_col, total_col = filter_state_data(state_df)
        
        if total_col and not state_df.empty:
            
            top_states = state_df.nlargest(15, total_col)
            
            col1, col2 = st.columns([1.2, 1])
            
            with col1:
                fig = create_bar_chart(
                    top_states,
                    x_col=total_col,
                    y_col=state_col,
                    title="Top 15 Estados por Ofensas de Odio",
                    height=600
                )
                st.plotly_chart(fig, width='stretch')
            
            with col2:
                st.markdown('<div class="card"><h4>📋 Top 15 Estados</h4></div>', unsafe_allow_html=True)
                
                display_states = top_states[[state_col, total_col]].copy()
                display_states.columns = ["Estado", "Ofensas"]
                display_states["Ofensas"] = display_states["Ofensas"].apply(format_number)
                
                st.dataframe(
                    display_states,
                    use_container_width=True,
                    hide_index=True
                )
            
            total_offenses_all = state_df[total_col].sum()
            top3_total = top_states.head(3)[total_col].sum()
            top5_total = top_states.head(5)[total_col].sum()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="info-card" style="text-align: center;">
                    <div style="font-size: 2rem;">🏆</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #0EA5E9;">{top3_total/total_offenses_all*100:.1f}%</div>
                    <div>Top 3 Estados concentran</div>
                    <div style="font-size: 0.85rem; color: #64748B;">({format_number(top3_total)} de {format_number(total_offenses_all)} ofensas)</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="info-card" style="text-align: center;">
                    <div style="font-size: 2rem;">📊</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #0EA5E9;">{top5_total/total_offenses_all*100:.1f}%</div>
                    <div>Top 5 Estados concentran</div>
                    <div style="font-size: 0.85rem; color: #64748B;">({format_number(top5_total)} de {format_number(total_offenses_all)} ofensas)</div>
                </div>
                """, unsafe_allow_html=True)
            
            render_insight_card(
                "California, Texas y Nueva York reportan el mayor número de ofensas por crímenes de odio. "
                "Un análisis ajustado por población proporcionaría una comparación más precisa entre estados, "
                "ya que estos tres estados también se encuentran entre los más poblados del país."
            )
        
        else:
            st.warning("No hay información de estados disponible después del filtrado")
    else:
        st.warning("No se encontró el dataset de estados")

render_footer()