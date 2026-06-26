import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="EDA", page_icon="📊", layout="wide")
st.title("📊 Análisis Exploratorio de Datos")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/reporte_clinica_clean.csv")

df = load_data()
sns.set_theme(style="whitegrid", palette="muted")

st.markdown("---")
st.markdown("## Análisis univariado")

# VIZ 1: Distribución de charges
st.markdown("### Visualización 1 — Distribución de costos médicos")
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(df['charges'], bins=40, color='steelblue', edgecolor='white')
axes[0].set_title('Distribución de charges')
axes[0].set_xlabel('Costo médico (USD)')
axes[0].set_ylabel('Frecuencia')
axes[1].boxplot(df['charges'], vert=True, patch_artist=True,
                boxprops=dict(facecolor='steelblue', alpha=0.6))
axes[1].set_title('Boxplot de charges')
axes[1].set_ylabel('Costo médico (USD)')
plt.tight_layout()
st.pyplot(fig)
st.info("""
**Interpretación:** La distribución de `charges` presenta una asimetría positiva marcada.
La mayoría de los pacientes tiene costos bajos (mediana ~9.300 USD), pero existe una cola derecha
con casos de hasta ~63.000 USD. Esta estructura sugiere la existencia de al menos dos grupos
con perfiles de riesgo diferenciados, lo cual es explorado en las preguntas 1 y 3.
""")

# VIZ 2: Fumadores
st.markdown("### Visualización 2 — Distribución de fumadores")
fig2, axes2 = plt.subplots(1, 2, figsize=(10, 4))
conteo = df['smoker'].value_counts()
axes2[0].bar(conteo.index, conteo.values, color=['steelblue', 'coral'], edgecolor='white')
axes2[0].set_title('Cantidad de fumadores y no fumadores')
axes2[0].set_xlabel('Fumador')
axes2[0].set_ylabel('Cantidad')
for i, v in enumerate(conteo.values):
    axes2[0].text(i, v + 5, str(v), ha='center', fontweight='bold')
axes2[1].pie(conteo.values, labels=conteo.index, autopct='%1.1f%%',
             colors=['steelblue', 'coral'], startangle=90)
axes2[1].set_title('Proporción de fumadores')
plt.tight_layout()
st.pyplot(fig2)
st.info("""
**Interpretación:** Aproximadamente el 20% de los pacientes son fumadores. Esta proporción
implica que, si el tabaquismo tiene un impacto fuerte sobre los costos, ese 20% podría
explicar una parte desproporcionada de la varianza en `charges`.
""")

st.markdown("---")
st.markdown("## Análisis bivariado")

# VIZ 3: Charges por smoker
st.markdown("### Visualización 3 — Costos médicos según condición de fumador")
fig3, axes3 = plt.subplots(1, 2, figsize=(12, 5))
df.boxplot(column='charges', by='smoker', ax=axes3[0], patch_artist=True,
           boxprops=dict(facecolor='steelblue', alpha=0.5))
axes3[0].set_title('Distribución de charges por fumador')
axes3[0].set_xlabel('Fumador')
axes3[0].set_ylabel('Costo médico (USD)')
plt.sca(axes3[0])
plt.title('charges por smoker')
medias = df.groupby('smoker')['charges'].mean()
axes3[1].bar(medias.index, medias.values, color=['steelblue', 'coral'], edgecolor='white')
axes3[1].set_title('Costo promedio por condición de fumador')
axes3[1].set_xlabel('Fumador')
axes3[1].set_ylabel('Costo medio (USD)')
for i, (k, v) in enumerate(medias.items()):
    axes3[1].text(i, v + 200, f'${v:,.0f}', ha='center', fontweight='bold')
plt.tight_layout()
st.pyplot(fig3)
st.info("""
**Interpretación (Pregunta 1):** Los pacientes fumadores tienen un costo medio ~4 veces mayor
al de los no fumadores. Esta diferencia se mantiene en el análisis multivariado y es confirmada
por la correlación de `smoker_num` con `charges` (r≈0.79), la más alta del dataset.
El tabaquismo es el factor de mayor impacto individual sobre los costos médicos.
""")

# VIZ 4: Scatter BMI / Age
st.markdown("### Visualización 4 — IMC y edad vs costos médicos")
fig4, axes4 = plt.subplots(1, 2, figsize=(13, 5))
sc1 = axes4[0].scatter(df['bmi'], df['charges'],
                       c=df['smoker'].map({'yes': 1, 'no': 0}),
                       cmap='coolwarm', alpha=0.5, s=20)
axes4[0].set_title('IMC vs Costos (color: fumador)')
axes4[0].set_xlabel('IMC (bmi)')
axes4[0].set_ylabel('Costo médico (USD)')
plt.colorbar(sc1, ax=axes4[0], label='Fumador (1=sí)')
sc2 = axes4[1].scatter(df['age'], df['charges'],
                       c=df['smoker'].map({'yes': 1, 'no': 0}),
                       cmap='coolwarm', alpha=0.5, s=20)
axes4[1].set_title('Edad vs Costos (color: fumador)')
axes4[1].set_xlabel('Edad (age)')
axes4[1].set_ylabel('Costo médico (USD)')
plt.colorbar(sc2, ax=axes4[1], label='Fumador (1=sí)')
plt.tight_layout()
st.pyplot(fig4)
st.info("""
**Interpretación (Pregunta 2):** La edad y el IMC tienen una relación positiva con los costos
(correlaciones r≈0.30 y r≈0.20 respectivamente), pero su efecto es secundario al del tabaquismo.
Dentro del grupo de fumadores, los costos más altos corresponden a pacientes mayores con mayor IMC,
lo que indica una potenciación del efecto.
""")

st.markdown("---")
st.markdown("## Análisis multivariado")

# VIZ 5: Heatmap + región
st.markdown("### Visualización 5 — Correlaciones y costos por región y fumador")
df_num = df.copy()
df_num['smoker_num'] = df['smoker'].map({'yes': 1, 'no': 0})
df_num['sex_num'] = df['sex'].map({'male': 1, 'female': 0})
fig5, axes5 = plt.subplots(1, 2, figsize=(14, 5))
corr = df_num[['age','bmi','children','smoker_num','sex_num','charges']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            ax=axes5[0], linewidths=0.5)
axes5[0].set_title('Mapa de correlaciones')
pivot = df.groupby(['region', 'smoker'])['charges'].mean().unstack()
pivot.plot(kind='bar', ax=axes5[1], color=['steelblue', 'coral'], edgecolor='white')
axes5[1].set_title('Costo medio por región y condición de fumador')
axes5[1].set_xlabel('Región')
axes5[1].set_ylabel('Costo medio (USD)')
axes5[1].legend(title='Fumador')
axes5[1].tick_params(axis='x', rotation=30)
plt.tight_layout()
st.pyplot(fig5)
st.info("""
**Interpretación (Pregunta 3):** El mapa de correlaciones confirma que `smoker_num` tiene
la mayor correlación con `charges` (r≈0.79). El gráfico por región muestra que el patrón
es consistente en todas las regiones: los fumadores tienen costos 3-4 veces superiores sin
importar la ubicación geográfica. Esta consistencia estructural anticipa la separación
de grupos que se confirmará en el análisis PCA.
""")
