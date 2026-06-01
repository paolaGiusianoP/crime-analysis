import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_bias_chart(data):
    """Genera gráfico de incidentes por tipo de bias"""
    incidents_df = data["incidents"]

    bias_df = incidents_df.copy()
    bias_df = bias_df[~bias_df["Bias motivation"].isin(
        ["Total", "Single-Bias Incidents", "Multiple-Bias Incidents3"]
    )]
    bias_df["Incidents"] = pd.to_numeric(bias_df["Incidents"], errors="coerce").fillna(0)

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(bias_df)))

    bars = ax.barh(bias_df["Bias motivation"], bias_df["Incidents"], color=colors)
    ax.invert_yaxis()
    ax.set_xlabel("Número de incidentes", fontsize=11)
    ax.set_title("Incidentes de crímenes de odio por tipo de bias (2020)", fontsize=13)

    for bar, val in zip(bars, bias_df["Incidents"]):
        if val > 0:
            ax.text(val + 50, bar.get_y() + bar.get_height() / 2,
                    f'{int(val):,}', va='center', fontsize=8)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return fig


def plot_offenses_chart(data):
    """Genera gráfico de tipos de ofensas"""
    offenses_df = data["offenses_by_type"].copy()

    offenses_df = offenses_df[~offenses_df["Offense type"].isin(
        ["Total", "Crimes against persons:", "Crimes against property:", "Crimes against society5"]
    )]
    offenses_df["Offenses"] = pd.to_numeric(offenses_df["Offenses"], errors="coerce").fillna(0)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(offenses_df["Offense type"], offenses_df["Offenses"], color='#45B7D1')
    ax.invert_yaxis()
    ax.set_xlabel("Número de ofensas", fontsize=11)
    ax.set_title("Tipos de ofensas en crímenes de odio (2020)", fontsize=13)

    for bar, val in zip(bars, offenses_df["Offenses"]):
        if val > 0:
            ax.text(val + 50, bar.get_y() + bar.get_height() / 2,
                    f'{int(val):,}', va='center', fontsize=8)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return fig