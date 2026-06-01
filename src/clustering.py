import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def cluster_states(df, n_clusters=3):
    """Realiza clustering de estados basado en ofensas"""
    df = df.copy()

    state_col = None
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ["state", "participating"]):
            state_col = col
            break

    if state_col is None:
        state_col = df.columns[0]

    total_col = None
    for col in df.columns:
        if "total" in col.lower():
            total_col = col
            break

    if total_col is None:
        total_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]

    data = df[[state_col, total_col]].dropna()
    data[total_col] = pd.to_numeric(data[total_col], errors="coerce")
    data = data.dropna()

    scaler = StandardScaler()
    X = scaler.fit_transform(data[[total_col]])

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    data["cluster"] = kmeans.fit_predict(X)

    cluster_means = data.groupby("cluster")[total_col].mean().sort_values()
    risk_map = {cluster: i for i, cluster in enumerate(cluster_means.index)}

    risk_levels = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
    data["risk_level"] = data["cluster"].map(lambda x: risk_levels.get(risk_map.get(x, x), "Unknown"))

    data = data.rename(columns={state_col: "state", total_col: "total_offenses"})

    return data, kmeans, scaler