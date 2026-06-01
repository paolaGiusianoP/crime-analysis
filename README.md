# 🚨 FBI Hate Crime Analysis Dashboard


## 📊 Vista Previa

| Sección         | Descripción                                                   |
| --------------- | ------------------------------------------------------------- |
| **Overview**    | Resumen ejecutivo y KPIs principales                          |
| **Exploration** | Análisis exploratorio de bias motivations y ofensas           |
| **Risk Map**    | Visualización geográfica y clasificación de riesgo por estado |
| **Insights**    | Hallazgos clave y recomendaciones estratégicas                |

---

## 📁 Estructura del Proyecto

```text
crime-analysis/
├── app.py                        # Página principal del dashboard
├── pages/
│   ├── 1_Overview.py             # Resumen general y KPIs
│   ├── 2_Exploration.py          # Análisis exploratorio
│   ├── 4_Risk_Map.py             # Mapas de calor y riesgo
│   └── 5_Insights.py             # Insights y recomendaciones
├── src/
│   ├── constants.py              # Constantes (colores, categorías)
│   ├── styles.py                 # Estilos CSS
│   ├── components.py             # Componentes UI reutilizables
│   ├── charts.py                 # Funciones de gráficos Plotly
│   ├── data_loader.py            # Carga de datos Excel
│   └── utils.py                  # Funciones de utilidad
├── data/
│   ├── Table_1_Incidents_...xlsx
│   ├── Table_2_Offenses_...xlsx
│   ├── Table_10_Incidents_...xlsx
│   └── Table_11_Offenses_...xlsx
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

El dashboard utiliza las estadísticas oficiales del **FBI Uniform Crime Reporting (UCR) Program** para el año 2020:

| Métrica                 | Valor  |
| ----------------------- | ------ |
| **Incidentes**          | 8,263  |
| **Ofensas**             | 11,129 |
| **Víctimas**            | 11,472 |
| **Ofensores Conocidos** | 6,780  |

### Tablas incluidas

* `Table 1`: Incidentes, ofensas, víctimas y ofensores por bias motivation
* `Table 2`: Incidentes, ofensas, víctimas y ofensores por offense type
* `Table 3`: Ofensas por raza/etnia del ofensor y tipo de ofensa
* `Table 4`: Ofensas por tipo de ofensa y bias motivation
* `Table 5`: Ofensas por raza/etnia del ofensor y bias motivation
* `Table 6`: Ofensas por tipo de víctima y tipo de ofensa
* `Table 7`: Víctimas por tipo de ofensa y bias motivation
* `Table 8`: Incidentes por tipo de víctima y bias motivation
* `Table 9`: Ofensores conocidos por raza, etnia y edad
* `Table 10`: Incidentes por bias motivation y ubicación
* `Table 11`: Ofensas por tipo de ofensa, estado y agencias federales

---

## 🚀 Instalación y Ejecución

### Requisitos previos

* Python 3.11 o superior
* pip (gestor de paquetes de Python)

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/crime-analysis.git
cd crime-analysis
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Colocar los datos

Asegúrate de que los archivos Excel del FBI estén en la carpeta `data/`.

### Paso 4: Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación estará disponible en:

```text
http://localhost:8501
```

---

## 🛠 Tecnologías Utilizadas

| Tecnología | Versión | Propósito                         |
| ---------- | ------- | --------------------------------- |
| Streamlit  | ≥1.28.0 | Framework principal del dashboard |
| Pandas     | ≥2.0.0  | Manipulación y análisis de datos  |
| NumPy      | ≥1.24.0 | Operaciones numéricas             |
| Plotly     | ≥5.17.0 | Visualizaciones interactivas      |
| Matplotlib | ≥3.7.0  | Gráficos estáticos                |
| openpyxl   | ≥3.1.0  | Lectura de archivos Excel         |

---

## 📈 Características

### 1. Overview (Resumen General)

* KPIs principales (incidentes, ofensas, víctimas, ofensores)
* Distribución de incidentes (Single vs Multiple Bias)
* Top 10 motivaciones de bias
* Análisis de ratios

### 2. Exploration (Análisis Exploratorio)

* Top 20 motivaciones de bias
* Resumen por categoría (raza, religión, orientación sexual, etc.)
* Distribución de tipos de ofensas
* Top 15 estados por ofensas

### 3. Risk Map (Mapa de Riesgo)

* Mapa de calor de ofensas por estado
* Clasificación de estados por nivel de riesgo (Alto/Medio/Bajo)
* Top 10 estados con mayor riesgo
* Mapa de riesgo clasificado por colores

### 4. Insights (Hallazgos y Recomendaciones)

* Patrones principales identificados
* Bias más frecuentes
* Recomendaciones estratégicas
* Limitaciones del análisis

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---
