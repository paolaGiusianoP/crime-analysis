import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


def prepare_features(df):
    """Prepara features para el modelo"""
    df = df.copy()
    df = df.select_dtypes(include="number")
    df = df.dropna()
    return df


def train_state_model(df, target_col=None):
    """Entrena modelos para predecir ofensas por estado"""
    df = df.copy()
    df = df.dropna()

    if target_col is None:
        for col in df.columns:
            if "total" in col.lower():
                target_col = col
                break

    if target_col is None:
        raise ValueError("No se encontró columna objetivo")

    X = df.select_dtypes(include="number").drop(columns=[target_col], errors="ignore")
    y = df[target_col]

    if X.empty or y.empty:
        raise ValueError("No hay suficientes datos para entrenar")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Modelos
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
    }

    results = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        results[name] = {
            "model": model,
            "mae": mean_absolute_error(y_test, preds),
            "r2": r2_score(y_test, preds)
        }

    return results


def get_best_model(results):
    """Devuelve el mejor modelo basado en R²"""
    best_name = max(results.keys(), key=lambda x: results[x]["r2"])
    return best_name, results[best_name]