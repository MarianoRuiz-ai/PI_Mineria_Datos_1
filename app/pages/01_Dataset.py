import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dataset", page_icon="📂", layout="wide")
st.title("📂 Dataset")

@st.cache_data
def load_data():
    raw = pd.read_csv("../data/raw/reporte_clinica.csv")
    clean = pd.read_csv("../data/processed/reporte_clinica_clean.csv")
    return raw, clean

raw, clean = load_data()

st.markdown("## Descripción general")
st.markdown("""
El dataset contiene registros de pacientes con variables demográficas, físicas y de hábitos,
junto con el costo médico asociado (`charges`). Fue provisto por la cátedra como base para
el análisis exploratorio y la reducción de dimensionalidad.

**Variables del dataset:**
- `age`: edad del paciente (numérica)
- `sex`: sexo biológico (categórica: male / female)
- `bmi`: índice de masa corporal (numérica continua)
- `children`: cantidad de hijos cubiertos por el seguro (numérica entera)
- `smoker`: condición de fumador (categórica: yes / no)
- `region`: región geográfica (categórica: northeast / northwest / southeast / southwest)
- `charges`: costo médico total en USD (variable objetivo)
""")

st.markdown("---")
st.markdown("## Calidad del dataset original")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Filas originales", f"{raw.shape[0]:,}")
col2.metric("Columnas", raw.shape[1])
col3.metric("Nulos detectados", f"{raw.isnull().sum().sum()}")
col4.metric("Filas procesadas", f"{clean.shape[0]:,}")

st.markdown("### Problemas detectados en datos originales")
problemas = pd.DataFrame({
    "Variable": ["age", "bmi", "bmi", "sex", "smoker", "region", "children", "children"],
    "Problema": [
        "102 valores nulos (7.5%)",
        "50 valores nulos (3.7%)",
        "6 registros con bmi=999 (error de carga)",
        "Inconsistencia de capitalización (Female/female)",
        "Inconsistencia de capitalización (Yes/yes, No/no)",
        "Mezcla de abreviaciones (SE, NE, SW, NW) y nombres completos",
        "2 registros con children=-1 (imposible)",
        "1 registro con children=99 (inverosímil)"
    ],
    "Acción tomada": [
        "Imputación con mediana",
        "Imputación con mediana (tras eliminar outliers)",
        "Eliminación del registro",
        "Normalización a minúsculas",
        "Normalización a minúsculas",
        "Mapeo a nombre completo",
        "Eliminación del registro",
        "Eliminación del registro"
    ]
})
st.dataframe(problemas, use_container_width=True)

st.markdown("---")
st.markdown("## Vista previa del dataset procesado")
st.dataframe(clean.head(20), use_container_width=True)
st.caption(f"Mostrando 20 de {len(clean)} registros. Dataset completo disponible en `data/processed/reporte_clinica_clean.csv`")
