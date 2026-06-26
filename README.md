# Proyecto Integrador — Minería de Datos 1

**Integrante:** Ruiz Mariano 
**Comisión:** Nueva Esperanza-Turno Mañana  
**Fecha:** 30/06/26

---

## Información general

Proyecto integrador de la materia Minería de Datos 1. Análisis de un dataset de costos médicos de pacientes con el objetivo de identificar los factores que más influyen en los cargos médicos y detectar grupos diferenciados de pacientes. El trabajo incluye inspección inicial, limpieza de datos, análisis exploratorio, escalamiento, reducción de dimensionalidad mediante PCA y comunicación de resultados a través de una aplicación Streamlit.

---

## Objetivo del proyecto

Aplicar los contenidos de Minería de Datos 1 para construir un análisis de datos con decisiones justificadas, trazabilidad del proceso y comunicación clara de los resultados. Las preguntas de análisis definidas son:

1. ¿Fumar es el factor que más influye en los costos médicos?
2. ¿A mayor IMC y edad, mayores costos? ¿Se potencian entre sí?
3. ¿Existen grupos diferenciados de pacientes según su perfil de riesgo?

El alcance no incluye modelado predictivo. El enfoque es exploratorio y descriptivo.

---

## Dataset

El dataset `reporte_clinica.csv` contiene 1363 registros de pacientes con 8 columnas: `age` (edad), `sex` (sexo), `bmi` (índice de masa corporal), `children` (cantidad de hijos en cobertura), `smoker` (condición de fumador), `region` (región geográfica) y `charges` (costo médico en USD).

La variable objetivo del análisis es `charges`. Se detectaron problemas de calidad: 102 nulos en `age`, 50 nulos en `bmi`, valores imposibles en `bmi` (999.0) y `children` (-1, 99), e inconsistencias de capitalización en `sex`, `smoker` y `region`.

El dataset original se preservó sin modificaciones en `data/raw/`. El dataset procesado se encuentra en `data/processed/`.

---

## Estructura del repositorio

```
PI_Mineria_Datos_1/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/           ← dataset original sin modificaciones
│   └── processed/     ← dataset procesado utilizado en el análisis
├── notebooks/
│   ├── 01_inspeccion_inicial.ipynb
│   ├── 02_calidad_y_limpieza.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_pca.ipynb
│   └── 05_conclusiones.ipynb
├── app/
│   ├── Home.py
│   └── pages/
│       ├── 01_Dataset.py
│       ├── 02_EDA.py
│       ├── 03_PCA.py
│       └── 04_Conclusiones.py
├── reports/
│   └── informe_final.pdf
└── logs/
    └── pipeline_log.csv
```

---

## Preparación y calidad de datos

Ver desarrollo completo en [`notebooks/02_calidad_y_limpieza.ipynb`](notebooks/02_calidad_y_limpieza.ipynb) y registro en [`logs/pipeline_log.csv`](logs/pipeline_log.csv).

Las decisiones tomadas fueron: eliminación de la columna de índice redundante (`Unnamed: 0`); normalización de capitalización en `sex`, `smoker` y `region`; eliminación de registros con `bmi >= 100` (valor 999, error de carga evidente); eliminación de registros con `children < 0` o `children > 20` (valores imposibles o inverosímiles); imputación de nulos en `age` y `bmi` con la mediana (justificada por la distribución aproximadamente simétrica de ambas variables).

El dataset final contiene 1301 registros (retención: 95.5% del original) y no presenta valores nulos.

---

## Resumen del análisis exploratorio

Ver desarrollo completo en [`notebooks/03_eda.ipynb`](notebooks/03_eda.ipynb).

La distribución de `charges` presenta asimetría positiva con indicios de estructura bimodal. El hallazgo principal del análisis bivariado es que los pacientes fumadores tienen costos medios casi 4 veces superiores a los no fumadores (~32.000 USD vs ~8.400 USD), con una correlación r≈0.79 entre `smoker_num` y `charges`.

La edad (r≈0.30) y el IMC (r≈0.20) muestran relaciones positivas moderadas con los costos. El análisis multivariado confirma que el efecto del tabaquismo es consistente en todas las regiones geográficas, lo que descarta mediación regional. Los scatterplots revelan que dentro del grupo de fumadores, la edad y el IMC potencian los costos.

---

## Reducción de dimensionalidad

Ver desarrollo completo en [`notebooks/04_pca.ipynb`](notebooks/04_pca.ipynb).

Se aplicó PCA sobre las variables `age`, `bmi`, `children`, `smoker_num` y `charges`, escaladas con StandardScaler. Las dos primeras componentes explican aproximadamente el 60-65% de la varianza total. PC1 está dominada por `smoker_num` y `charges` (perfil de costo y riesgo); PC2 captura principalmente `age` y `bmi` (perfil demográfico). La proyección en PC1-PC2 evidencia una separación clara entre fumadores y no fumadores, confirmando la existencia de grupos diferenciados.

---

## Visualización interactiva

Aplicación pública disponible en: [https://[app].streamlit.app](https://[app].streamlit.app)

La aplicación incluye: descripción del dataset y resumen de calidad (página Dataset); 5 visualizaciones con interpretaciones sobre el EDA (página EDA); scree plot, loadings y proyección PCA con interpretaciones (página PCA); y síntesis de conclusiones, limitaciones y mejoras futuras (página Conclusiones).

---

## Cómo ejecutar localmente

```bash
git clone https://github.com/[usuario]/PI_Mineria_Datos_1.git
cd PI_Mineria_Datos_1
pip install -r requirements.txt
streamlit run app/Home.py
```

Los notebooks pueden ejecutarse en orden (01 al 05) desde la carpeta `notebooks/`.

---

## Conclusiones

El tabaquismo es el factor con mayor influencia sobre los costos médicos en este dataset: los fumadores generan costos casi 4 veces superiores a los no fumadores, patrón consistente en todas las regiones. La edad y el IMC tienen un efecto positivo moderado, que se potencia dentro del grupo de fumadores. El análisis PCA confirma la existencia de al menos dos grupos estructuralmente diferenciados, con el tabaquismo como eje principal de separación.

Las conclusiones están condicionadas por la información disponible y las decisiones documentadas. El análisis es de carácter exploratorio y no establece causalidad. Ver [`reports/informe_final.pdf`](reports/informe_final.pdf) para la síntesis completa.
