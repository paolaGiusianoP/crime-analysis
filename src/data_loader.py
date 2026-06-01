import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data"

def clean_columns(cols):
    return (
        cols.astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace("  ", " ", regex=False)
        .str.replace("Unnamed: ", "", regex=False)
    )

def load_excel(file_path, skiprows=None, header=0):
    df = pd.read_excel(file_path, skiprows=skiprows, header=header)
    df.columns = clean_columns(df.columns)
    return df

def load_all_tables():
    print("📂 Cargando datos del FBI Hate Crime Statistics 2020...")

    tables = {}

    # Tablas base
    config = {
        "incidents": ("Table_1_Incidents_Offenses_Victims_and_Known_Offenders_by_Bias_Motivation_2020.xlsx", 4),
        "offenses_by_type": ("Table_2_Incidents_Offenses_Victims_and_Known_Offenders_by_Offense_Type_2020.xlsx", 4),
        "offenders_race_by_offense": ("Table_3_Offenses_Known_Offenders_Race_and_Ethnicity_by_Offense_Type_2020.xlsx", 4),
        "offenses_by_bias": ("Table_4_Offenses_Offense_Type_by_Bias_Motivation_2020.xlsx", 4),
        "offenders_race_by_bias": ("Table_5_Offenses_Known_Offenders_Race_and_Ethnicity_by_Bias_Motivation_2020.xlsx", 4),
        "victims_by_offense": ("Table_6_Offenses_Victim_Type_by_Offense_Type_2020.xlsx", 4),
        "victims_by_bias": ("Table_7_Victims_Offense_Type_by_Bias_Motivation_2020.xlsx", 4),
        "incidents_by_victim_type": ("Table_8_Incidents_Victim_Type_by_Bias_Motivation_2020.xlsx", 4),
        "offenders": ("Table_9_Known_Offenders_Known_Offenders_Race_Ethnicity_and_Age_2020.xlsx", 4),
    }

    for name, (file, skip) in config.items():
        path = DATA_PATH / file
        if path.exists():
            tables[name] = load_excel(path, skiprows=skip)
            print(f"   ✓ {name}: {tables[name].shape}")
        else:
            print(f"   ✗ {name}: archivo no encontrado - {file}")

    # Tabla 10 - Locations
    path10 = DATA_PATH / "Table_10_Incidents_Bias_Motivation_by_Location_2020.xlsx"
    if path10.exists():
        df10 = load_excel(path10, skiprows=5)
        df10 = df10.dropna(axis=1, how="all")
        tables["incidents_by_location"] = df10
        print(f"   ✓ incidents_by_location: {df10.shape}")

    # Tabla 11 - States 
    path11 = DATA_PATH / "Table_11_Offenses_Offense_Type_by_Participating_State_and_Federal_2020.xlsx"
    if path11.exists():
        df11 = pd.read_excel(path11, skiprows=4)
        
        df11.columns = clean_columns(df11.columns)
        
        # Eliminar columnas vacías
        df11 = df11.dropna(axis=1, how="all")
        
        # Renombrar primera columna
        first_col = df11.columns[0]
        df11 = df11.rename(columns={first_col: "State"})
        
        df11 = df11.dropna(subset=["State"], how="all")
        
        df11 = df11[~df11["State"].astype(str).str.contains("Participating state", case=False, na=False)]
        df11 = df11[~df11["State"].astype(str).str.contains("Table", case=False, na=False)]
        
        # Asegurar que las columnas numéricas sean números
        for col in df11.columns:
            if col != "State":
                df11[col] = pd.to_numeric(df11[col], errors="coerce")
        
        # Crear columna Total de ofensas sumando todas las columnas numéricas
        numeric_cols = df11.select_dtypes(include=['float64', 'int64']).columns
        df11["Total offenses"] = df11[numeric_cols].sum(axis=1)
        
        tables["offenses_by_state"] = df11
        print(f"   ✓ offenses_by_state: {df11.shape}")
        
        print(f"   Columnas: {df11.columns.tolist()[:5]}...")

    return tables