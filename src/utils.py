import pandas as pd
from src.constants import EXCLUDE_PATTERNS


def clean_numeric(df, column):
    """Convierte una columna a numérico y elimina nulos"""
    df = df.copy()
    df[column] = pd.to_numeric(df[column], errors="coerce")
    return df.dropna(subset=[column])


def get_total_row(df, bias_col="Bias motivation", total_value="Total"):
    """Obtiene la fila de totales de un DataFrame"""
    return df[df[bias_col] == total_value].iloc[0]


def filter_exclude(df, column, exclude_values=None):
    df = df.copy()
    exclude_values = exclude_values or EXCLUDE_PATTERNS
    
    for value in exclude_values:
        df = df[
            ~df[column]
            .astype(str)
            .str.contains(value, na=False, case=False)
        ]
    
    return df


def filter_bias_data(df):
    df = df.copy()
    df = filter_exclude(df, "Bias motivation")
    df["Incidents"] = pd.to_numeric(df["Incidents"], errors="coerce").fillna(0)
    return df[df["Incidents"] > 0]


def filter_state_data(df):
    df = df.copy()
    
    state_col = df.columns[0]
    total_col = None
    
    for col in df.columns:
        if "total" in col.lower():
            total_col = col
            break
    
    if total_col:
        df[total_col] = pd.to_numeric(df[total_col], errors="coerce")
        df = df.dropna(subset=[total_col])
        df = filter_exclude(df, state_col)
        df = df[df[total_col] > 0]
    
    return df, state_col, total_col


def get_kpi_data(incidents_df):
    total_row = incidents_df[incidents_df["Bias motivation"] == "Total"].iloc[0]
    
    return {
        "incidents": int(total_row["Incidents"]),
        "offenses": int(total_row["Offenses"]),
        "victims": int(total_row["Victims1"]),
        "offenders": int(total_row["Known Offenders2"])
    }


def get_bias_summary(incidents_df):
    df = filter_bias_data(incidents_df)
    total = df["Incidents"].sum()
    
    from src.constants import BIAS_CATEGORIES
    
    summary = {}
    for category, keywords in BIAS_CATEGORIES.items():
        category_total = df[
            df["Bias motivation"].str.contains("|".join(keywords), case=False, na=False)
        ]["Incidents"].sum()
        summary[category] = {
            "total": int(category_total),
            "percentage": category_total / total * 100 if total > 0 else 0
        }
    
    return summary, total


def get_top_bias(incidents_df, n=10):
    """Obtiene los top N bias"""
    df = filter_bias_data(incidents_df)
    return df.nlargest(n, "Incidents")[["Bias motivation", "Incidents"]]


def get_single_vs_multiple(incidents_df):
    """Obtiene datos de single vs multiple bias"""
    single = incidents_df[incidents_df["Bias motivation"] == "Single-Bias Incidents"]
    multiple = incidents_df[incidents_df["Bias motivation"] == "Multiple-Bias Incidents3"]
    
    return {
        "single": int(single.iloc[0]["Incidents"]) if not single.empty else 0,
        "multiple": int(multiple.iloc[0]["Incidents"]) if not multiple.empty else 0
    }


def format_number(value) -> str:
    """Formatea números con comas"""
    if isinstance(value, (int, float)):
        return f"{int(value):,}"
    return str(value)