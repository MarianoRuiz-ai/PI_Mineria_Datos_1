import streamlit as st

st.set_page_config(
    page_title="Proyecto Integrador — Minería de Datos 1",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Análisis de Costos Médicos")
st.subheader("Proyecto Integrador — Minería de Datos 1")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("###  Información del proyecto")
    st.markdown("""
    **Materia:** Minería de Datos 1  
    **Comisión:** Nueva Esperanza - Turno Mañana  
    **Fecha de entrega:** [Completar]  
    **Alumno:**
    - Ruiz Mariano

    """)

with col2:
    st.markdown("###  Contexto")
    st.markdown("""
    Este proyecto analiza un dataset de costos médicos de pacientes con el objetivo de
    identificar los factores que más influyen en el valor de los cargos médicos y detectar
    grupos diferenciados de pacientes según su perfil de riesgo.

    El análisis incluye inspección inicial, limpieza de datos, análisis exploratorio (EDA),
    reducción de dimensionalidad mediante PCA y comunicación de resultados.
    """)

st.markdown("---")
st.markdown("### ❓ Preguntas de análisis")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Pregunta 1**\n\n¿Fumar es el factor que más influye en los costos médicos?")
with col2:
    st.info("**Pregunta 2**\n\n¿A mayor IMC y edad, mayores costos? ¿Se potencian entre sí?")
with col3:
    st.info("**Pregunta 3**\n\n¿Existen grupos diferenciados de pacientes según su perfil de riesgo?")

st.markdown("---")
st.markdown("### 🔗 Repositorio")
st.markdown("📁 [Ver repositorio en GitHub](https://github.com/[usuario]/PI_Mineria_Datos_1)")

st.markdown("---")
st.caption("Navegar por las secciones usando el menú lateral.")
