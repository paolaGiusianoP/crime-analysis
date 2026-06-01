COLORS = {
    "primary": "#0EA5E9",      
    "secondary": "#F59E0B",    
    "success": "#10B981",      
    "danger": "#EF4444",       
    "dark": "#0F172A",         
    "light": "#F8FAFC",       
    "gray": "#64748B",         
    "gray_light": "#E2E8F0",   
}

# Paletas para gráficos
CHART_PALETTES = {
    "sequential": "Blues_r",
    "categorical": ["#0EA5E9", "#F59E0B", "#10B981", "#EF4444", "#8B5CF6"],
    "risk": {
        "Alto Riesgo": "#EF4444",
        "Riesgo Medio": "#F59E0B",
        "Bajo Riesgo": "#10B981"
    }
}

# Palabras clave para categorizar biases
BIAS_CATEGORIES = {
    "race_ethnicity": [
        "Anti-White", "Anti-Black", "Anti-American Indian", 
        "Anti-Asian", "Anti-Native Hawaiian", "Anti-Multiple Races",
        "Anti-Arab", "Anti-Hispanic", "Anti-Other Race"
    ],
    "religion": [
        "Anti-Jewish", "Anti-Catholic", "Anti-Protestant", 
        "Anti-Islamic", "Anti-Other Religion", "Anti-Multiple Religions",
        "Anti-Mormon", "Anti-Jehovah", "Anti-Eastern Orthodox",
        "Anti-Other Christian", "Anti-Buddist", "Anti-Hindu", 
        "Anti-Sikh", "Anti-Atheism"
    ],
    "sexual_orientation": [
        "Anti-Gay", "Anti-Lesbian", "Anti-Lesbian, Gay, Bisexual",
        "Anti-Heterosexual", "Anti-Bisexual"
    ],
    "disability": ["Anti-Physical", "Anti-Mental"],
    "gender": ["Anti-Male", "Anti-Female"],
    "gender_identity": ["Anti-Transgender", "Anti-Gender Non-Conforming"]
}

# Patrones para excluir filas no válidas
EXCLUDE_PATTERNS = [
    "Total", "Federal", "FBI", "Pentagon", "Marine", 
    "Participating", "Single-Bias", "Multiple-Bias"
]

BIAS_DISPLAY_NAMES = {
    "race_ethnicity": {"icon": "🏷️", "name": "Raza / Etnia"},
    "religion": {"icon": "⛪", "name": "Religión"},
    "sexual_orientation": {"icon": "🌈", "name": "Orientación Sexual"},
    "disability": {"icon": "♿", "name": "Discapacidad"},
    "gender": {"icon": "⚥", "name": "Género"},
    "gender_identity": {"icon": "🏳️‍⚧️", "name": "Identidad de Género"}
}

# Nombres de secciones para tabs
TAB_NAMES = {
    "bias": "🏷️ Motivaciones de Bias",
    "offenses": "📋 Tipos de Ofensas",
    "states": "🗺️ Análisis por Estado"
}