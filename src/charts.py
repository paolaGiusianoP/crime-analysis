import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.constants import COLORS, CHART_PALETTES


def create_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = None,
    orientation: str = "h",
    color_col: str = None,
    show_values: bool = True,
    height: int = 500,
    color_scale: str = None
) -> go.Figure:
    """
    Crea un gráfico de barras horizontal o vertical
    
    Args:
        df: DataFrame con los datos
        x_col: Columna para el eje X
        y_col: Columna para el eje Y
        title: Título del gráfico
        orientation: 'h' (horizontal) o 'v' (vertical)
        color_col: Columna para el color (opcional)
        show_values: Mostrar valores en las barras
        height: Altura del gráfico
        color_scale: Escala de color (ej: 'Blues_r')
    """
    color_scale = color_scale or CHART_PALETTES["sequential"]
    
    if orientation == "h":
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            orientation="h",
            color=color_col or x_col,
            color_continuous_scale=color_scale,
            text=x_col if show_values else None
        )
        
        if show_values:
            fig.update_traces(
                texttemplate='%{text:,}',
                textposition='outside',
                marker=dict(line=dict(width=0))
            )
    else:
        fig = px.bar(
            df,
            x=y_col,
            y=x_col,
            color=color_col or y_col,
            color_continuous_scale=color_scale,
            text=y_col if show_values else None
        )
        
        if show_values:
            fig.update_traces(
                texttemplate='%{text:,}',
                textposition='outside',
                marker=dict(line=dict(width=0))
            )
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, weight="bold", color=COLORS["dark"])) if title else None,
        height=height,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(gridcolor=COLORS["gray_light"], showgrid=True),
        yaxis=dict(categoryorder="total ascending"),
        margin=dict(l=10, r=10, t=50 if title else 10, b=10),
        coloraxis_showscale=False
    )
    
    return fig


def create_donut_chart(
    values: list,
    labels: list,
    title: str = None,
    colors: list = None,
    height: int = 430,
    hole: float = 0.65
) -> go.Figure:
    """
    Crea un gráfico de donut
    
    Args:
        values: Lista de valores
        labels: Lista de etiquetas
        title: Título del gráfico
        colors: Lista de colores
        height: Altura del gráfico
        hole: Tamaño del agujero (0-1)
    """
    colors = colors or CHART_PALETTES["categorical"][:len(values)]
    
    fig = px.pie(
        values=values,
        names=labels,
        hole=hole,
        color_discrete_sequence=colors
    )
    
    total = sum(values)
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=COLORS["dark"])) if title else None,
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        annotations=[
            dict(
                text=f"Total<br>{total:,}",
                x=0.5, y=0.5,
                showarrow=False,
                font_size=18,
                font_weight="bold"
            )
        ] if title else []
    )
    
    fig.update_traces(
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Valor: %{value:,}<br>Porcentaje: %{percent}<extra></extra>"
    )
    
    return fig


def create_us_choropleth(
    df: pd.DataFrame,
    location_col: str = "state",
    value_col: str = "value",
    color_scale: str = "Reds",
    title: str = None,
    height: int = 600
) -> go.Figure:
    """
    Crea un mapa coroplético de Estados Unidos
    
    Args:
        df: DataFrame con datos
        location_col: Columna con nombres de estados
        value_col: Columna con valores numéricos
        color_scale: Escala de color (ej: 'Reds', 'Blues')
        title: Título del gráfico
        height: Altura del gráfico
    """
    # Función para formatear números
    def format_number(value):
        if isinstance(value, (int, float)):
            return f"{int(value):,}"
        return str(value)
    
    df = df.copy()
    df["formatted_value"] = df[value_col].apply(format_number)
    
    fig = px.choropleth(
        df,
        locations=location_col,
        locationmode="USA-states",
        color=value_col,
        scope="usa",
        color_continuous_scale=color_scale,
        title=title,
        labels={value_col: "Valor", location_col: "Estado"},
        hover_data={"formatted_value": True, location_col: True}
    )
    
    fig.update_layout(
        title_x=0.5,
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            lakecolor='#E2E8F0',
            landcolor='#F8FAFC',
            subunitcolor='#CBD5E1',
            showframe=False,
            showcoastlines=True,
            coastlinecolor='#CBD5E1'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        height=height,
        margin=dict(l=0, r=0, t=30 if title else 0, b=0)
    )
    
    fig.update_coloraxes(colorbar_title="Valor")
    
    return fig


def create_simple_bar(df: pd.DataFrame, x_col: str, y_col: str, title: str = None, height: int = 500):
    return create_bar_chart(df, x_col, y_col, title, orientation="h", height=height)


def add_risk_colors(fig: go.Figure, risk_levels: dict) -> go.Figure:
    """Añade colores personalizados para niveles de riesgo"""
    fig.update_traces(
        marker_color=[risk_levels.get(level, COLORS["gray"]) for level in fig.data[0].x]
    )
    return fig