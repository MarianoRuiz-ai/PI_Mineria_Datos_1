import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from matplotlib.patches import Patch

st.set_page_config(page_title="PCA", page_icon="🔬", layout="wide")
st.title("🔬 Reducción de Dimensionalidad — PCA")

@st.cache_data
def load_and_compute():
    df = pd.read_csv("../data/processed/reporte_clinica_clean.csv")
    df['smoker_num'] = df['smoker'].map({'yes': 1, 'no': 0})
    variables_pca = ['age', 'bmi', 'children', 'smoker_num', 'charges']
    X = df[variables_pca].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    pca = PCA(n_components=5)
    X_pca = pca.fit_transform(X_scaled)
    return df, X_pca, pca, variables_pca

df, X_pca, pca, variables_pca = load_and_compute()

st.markdown("## Variables y escalamiento")
st.markdown("""
**Variables incluidas:** `age`, `bmi`, `children`, `smoker_num`, `charges`

**Justificación de la selección:** Se incluyeron las variables numéricas continuas y `smoker_num`
(codificación binaria de la condición de fumador), ya que el EDA mostró que es la variable
con mayor correlación con `charges`. Se excluyó `sex` (correlación casi nula con `charges`)
y `region` (categórica nominal sin orden).

**Escalamiento aplicado:** StandardScaler (media=0, desviación estándar=1 por variable).
Sin escalamiento, `charges` (en miles de USD) dominaría las componentes por su magnitud,
ocultando la contribución del resto de las variables.
""")

st.markdown("---")
st.markdown("## Varianza explicada")

varianza = pca.explained_variance_ratio_
varianza_acum = np.cumsum(varianza)

col1, col2, col3 = st.columns(3)
col1.metric("PC1 explica", f"{varianza[0]*100:.1f}%")
col2.metric("PC2 explica", f"{varianza[1]*100:.1f}%")
col3.metric("PC1+PC2 acumulado", f"{varianza_acum[1]*100:.1f}%")

# VIZ 1: Scree plot
st.markdown("### Visualización 1 — Varianza explicada (Scree plot)")
fig1, axes1 = plt.subplots(1, 2, figsize=(12, 4))
axes1[0].bar(range(1, 6), varianza * 100, color='steelblue', edgecolor='white')
axes1[0].set_title('Varianza explicada por componente')
axes1[0].set_xlabel('Componente principal')
axes1[0].set_ylabel('Varianza explicada (%)')
for i, v in enumerate(varianza * 100):
    axes1[0].text(i + 1, v + 0.3, f'{v:.1f}%', ha='center', fontsize=9)
axes1[1].plot(range(1, 6), varianza_acum * 100, 'o-', color='steelblue')
axes1[1].axhline(80, linestyle='--', color='coral', label='80%')
axes1[1].set_title('Varianza acumulada')
axes1[1].set_xlabel('Número de componentes')
axes1[1].set_ylabel('Varianza acumulada (%)')
axes1[1].legend()
plt.tight_layout()
st.pyplot(fig1)
st.info("""
**Interpretación:** Las dos primeras componentes explican aproximadamente el 60-65% de la varianza.
Para superar el 80% se requieren 3 componentes. Se trabaja con PC1 y PC2 para la visualización
bidimensional, que captura la mayor parte de la estructura del dataset.
""")

st.markdown("---")
st.markdown("## Interpretación de componentes")

loadings = pd.DataFrame(
    pca.components_.T,
    index=variables_pca,
    columns=[f'PC{i+1}' for i in range(5)]
)
st.dataframe(loadings[['PC1','PC2']].round(3), use_container_width=False)
st.markdown("""
- **PC1** recibe las contribuciones más altas de `smoker_num` y `charges`: representa el **perfil de costo y riesgo por tabaquismo**.
- **PC2** recibe contribuciones principalmente de `age` y `bmi`: representa el **perfil demográfico y físico**.
""")

st.markdown("---")
# VIZ 2: Proyección
st.markdown("### Visualización 2 — Proyección de pacientes en PC1-PC2")
fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))
colors_smoker = df['smoker'].map({'yes': 'coral', 'no': 'steelblue'})
axes2[0].scatter(X_pca[:, 0], X_pca[:, 1], c=colors_smoker, alpha=0.5, s=15)
axes2[0].set_title('PC1 vs PC2 — coloreado por fumador')
axes2[0].set_xlabel('PC1 (riesgo/costo)')
axes2[0].set_ylabel('PC2 (edad/IMC)')
legend_elements = [Patch(facecolor='coral', label='Fumador'),
                   Patch(facecolor='steelblue', label='No fumador')]
axes2[0].legend(handles=legend_elements)
sc = axes2[1].scatter(X_pca[:, 0], X_pca[:, 1],
                      c=df['charges'], cmap='YlOrRd', alpha=0.5, s=15)
axes2[1].set_title('PC1 vs PC2 — coloreado por nivel de charges')
axes2[1].set_xlabel('PC1 (riesgo/costo)')
axes2[1].set_ylabel('PC2 (edad/IMC)')
plt.colorbar(sc, ax=axes2[1], label='charges (USD)')
plt.tight_layout()
st.pyplot(fig2)
st.info("""
**Interpretación:** La proyección en PC1-PC2 confirma la existencia de grupos diferenciados.
Los fumadores se concentran claramente en valores positivos de PC1, separados del grupo de
no fumadores. El gradiente de costos está alineado con PC1, lo que confirma que la separación
espacial refleja diferencias reales en el nivel de costos. Esto responde afirmativamente
la pregunta 3: existen grupos diferenciados, y el tabaquismo es el principal eje de separación.
""")
