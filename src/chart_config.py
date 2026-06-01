import plotly.graph_objects as go
import plotly.express as px

def apply_chart_theme(fig, title=None, height=500, showgrid=True):
    """Aplica un tema consistente a todos los gráficos Plotly"""
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, weight="bold", color="#0F172A"),
            x=0.5,
            xanchor="center"
        ),
        height=height,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif", size=12, color="#334155"),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Inter"
        ),
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="#E2E8F0",
            borderwidth=1,
            font=dict(size=11)
        )
    )
    
    if showgrid:
        fig.update_xaxis(
            showgrid=True,
            gridcolor="#F1F5F9",
            gridwidth=1,
            title_font=dict(size=12, weight="bold"),
            tickfont=dict(size=11)
        )
        fig.update_yaxis(
            showgrid=True,
            gridcolor="#F1F5F9",
            gridwidth=1,
            title_font=dict(size=12, weight="bold"),
            tickfont=dict(size=11)
        )
    
    return fig

def create_gradient_bar_chart(df, x_col, y_col, title, color_scale="Blues", orientation="h"):
    if orientation == "h":
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            orientation="h",
            color=x_col,
            color_continuous_scale=color_scale,
            text=x_col
        )
        
        fig.update_yaxes(categoryorder="total ascending", title="")
        fig.update_xaxes(title="Número de Incidentes", showgrid=True)
        
    else:
        fig = px.bar(
            df,
            x=y_col,
            y=x_col,
            orientation="v",
            color=x_col,
            color_continuous_scale=color_scale,
            text=x_col
        )
        
        fig.update_xaxes(title="", showgrid=True)
        fig.update_yaxes(title="Número de Incidentes")
    
    fig.update_traces(
        texttemplate='%{text:,}',
        textposition='outside',
        marker=dict(line=dict(width=0), opacity=0.9)
    )
    
    fig = apply_chart_theme(fig, title, height=600)
    fig.update_coloraxes(showscale=False)
    
    return fig

def create_donut_chart(values, names, title, colors=None):
    """Crea un gráfico de donut moderno"""
    
    if colors is None:
        colors = ["#0EA5E9", "#F59E0B", "#10B981", "#8B5CF6", "#EF4444"]
    
    fig = go.Figure(data=[go.Pie(
        values=values,
        labels=names,
        hole=0.65,
        marker=dict(colors=colors),
        textinfo='percent+label',
        textposition='auto',
        hoverinfo='label+value+percent',
        hovertemplate='<b>%{label}</b><br>Valor: %{value:,}<br>Porcentaje: %{percent}<extra></extra>'
    )])
    
    total = sum(values)
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, weight="bold", color="#0F172A"),
            x=0.5
        ),
        height=450,
        plot_bgcolor="white",
        paper_bgcolor="white",
        annotations=[
            dict(
                text=f"Total<br>{total:,}",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=18, weight="bold", color="#0F172A")
            )
        ]
    )
    
    return fig

def create_choropleth_map(df, locations_col, color_col, title, color_scale="Reds"):
    fig = px.choropleth(
        df,
        locations=locations_col,
        locationmode="USA-states",
        color=color_col,
        scope="usa",
        color_continuous_scale=color_scale,
        title="",
        labels={color_col: "Número de Ofensas"}
    )
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, weight="bold", color="#0F172A"),
            x=0.5
        ),
        height=600,
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
        margin=dict(l=0, r=0, t=60, b=0)
    )
    
    fig.update_coloraxes(
        colorbar_title="Número de Ofensas",
        colorbar=dict(
            title_font=dict(size=12, weight="bold"),
            tickfont=dict(size=10)
        )
    )
    
    return fig

def create_line_chart(df, x_col, y_col, title, color=None):
    
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        color=color,
        markers=True
    )
    
    fig.update_traces(
        line=dict(width=2),
        marker=dict(size=6, symbol="circle")
    )
    
    fig = apply_chart_theme(fig, title, height=400)
    
    return fig