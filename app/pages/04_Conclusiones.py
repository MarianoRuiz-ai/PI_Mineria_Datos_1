import streamlit as st

st.set_page_config(page_title="Conclusiones", page_icon="✅", layout="wide")
st.title("✅ Conclusiones")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ❓ Pregunta 1")
    st.markdown("*¿Fumar es el factor que más influye en los costos médicos?*")
    st.success("""
**Conclusión: Sí.**

Los pacientes fumadores generan costos médicos casi 4 veces superiores a los no fumadores
(~32.000 USD vs ~8.400 USD). La correlación de `smoker_num` con `charges` es r≈0.79,
la más alta de todas las variables. El patrón es consistente en todas las regiones geográficas
y se confirma como el eje de mayor varianza en el análisis PCA.
    """)

with col2:
    st.markdown("### ❓ Pregunta 2")
    st.markdown("*¿A mayor IMC y edad, mayores costos? ¿Se potencian entre sí?*")
    st.success("""
**Conclusión: Sí, pero de forma moderada.**

La edad (r≈0.30) y el IMC (r≈0.20) tienen relaciones positivas con los costos, pero
secundarias respecto al tabaquismo. La potenciación entre ambas variables ocurre principalmente
dentro del grupo de fumadores: un fumador mayor con IMC elevado representa el perfil de
mayor costo en el dataset.
    """)

with col3:
    st.markdown("### ❓ Pregunta 3")
    st.markdown("*¿Existen grupos diferenciados de pacientes según su perfil de riesgo?*")
    st.success("""
**Conclusión: Sí.**

El análisis PCA confirma la existencia de al menos dos grupos estructuralmente diferenciados:
pacientes de bajo riesgo (no fumadores, costos bajos) y de alto riesgo (fumadores, costos elevados).
Dentro de cada grupo, la edad y el IMC introducen variación adicional. La separación es
visible tanto en el análisis descriptivo como en el espacio de componentes principales.
    """)

st.markdown("---")
st.markdown("## ⚠️ Limitaciones")
st.warning("""
- El alcance de las conclusiones está condicionado por la información disponible y las decisiones documentadas. No se dispone de datos clínicos adicionales.
- La imputación por mediana en `age` y `bmi` introduce una simplificación que puede subestimar la variabilidad real.
- El análisis es exploratorio: las relaciones observadas indican asociación estadística, no causalidad.
- El dataset no incluye información temporal, lo que impide analizar evolución de costos.
""")

st.markdown("---")
st.markdown("## 🚀 Mejoras futuras")
st.info("""
- Incorporar variables clínicas adicionales para ampliar el análisis de perfiles de riesgo.
- Aplicar técnicas de clustering (k-means, DBSCAN) en el espacio PCA para formalizar la segmentación de pacientes.
- Explorar modelos predictivos de costos una vez consolidada la comprensión del dataset.
""")

st.markdown("---")
st.markdown("### 🔗 Referencias")
st.markdown("""
- 📁 [Repositorio GitHub](https://github.com/[usuario]/PI_Mineria_Datos_1)
- 🌐 [Aplicación Streamlit Cloud](https://[app].streamlit.app)
- 📓 Notebooks: `notebooks/` (01 al 05)
- 📄 Informe final: `reports/informe_final.pdf`
- 📋 Log ETL: `logs/pipeline_log.csv`
""")
