# 🧠 Guía de Entrenamiento y Ejecución del Modelo

> Documentación completa sobre cómo ejecutar los entornos, entrenar el modelo de ML, procesar datasets e ingestar documentos en TechMind.

---

## 📋 Índice

1. [Requisitos Previos](#1-requisitos-previos)
2. [Migración del Dataset a PostgreSQL](#2-migración-del-dataset-a-postgresql)
3. [Entrenamiento del Modelo en Jupyter Notebook](#3-entrenamiento-del-modelo-en-jupyter-notebook)
4. [Re-entrenamiento Automático vía Línea de Comandos](#4-re-entrenamiento-automático-vía-línea-de-comandos)
5. [Ingesta de Nuevos Documentos (PDF / DOCX)](#5-ingesta-de-nuevos-documentos-pdf--docx)
6. [Ubicación de Artefactos Generados](#6-ubicación-de-artefactos-generados)

---

## 1. Requisitos Previos

Asegúrate de instalar las dependencias de Python listadas en el proyecto desde la raíz:

```bash
# Crear e ingresar al entorno virtual
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# Instalar dependencias
pip install -r data-science/requirements.txt
```

Asegúrate también de tener la base de datos levantada con Docker:

```bash
docker-compose up -d
```

---

## 2. Migración del Dataset a PostgreSQL

El dataset inicial de 61 contenidos técnicos se encuentra en `data-science/data/raw/contenidos_tecnicos.csv`.

Para cargarlo en PostgreSQL:

```bash
python3 data-science/src/migrate_to_postgres.py
```

El script creará las tablas `contenidos` y `predicciones` en la base de datos PostgreSQL e insertará los registros Semilla.

---

## 3. Entrenamiento del Modelo en Jupyter Notebook

El proceso principal de Exploración de Datos (EDA), Vectorización TF-IDF y Entrenamiento (Regresión Logística) reside en el notebook Jupyter:

```bash
jupyter notebook data-science/notebooks/TechMind_DataScience.ipynb
```

### Pasos ejecutados internamente por el Notebook:

1. **Carga de Datos:** Conexión a PostgreSQL y lectura de la tabla `contenidos`.
2. **Análisis Exploratorio (EDA):** Distribución de clases y longitud de palabras.
3. **Preprocesamiento:** Limpieza de puntuación, stopwords y conversión a minúsculas.
4. **Vectorización:** `TfidfVectorizer` (unigramas y bigramas).
5. **Entrenamiento:** Modelo `LogisticRegression(class_weight='balanced')`.
6. **Evaluación:** Matriz de confusión y métricas `classification_report`.
7. **Exportación:** Serialización de los archivos `.joblib` en `data-science/models/`.

---

## 4. Re-entrenamiento Automático vía Línea de Comandos

Si no deseas abrir la interfaz web de Jupyter y prefieres re-entrenar el modelo en background (por ejemplo, tras incorporar nuevos datos):

```bash
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=120 --output data-science/notebooks/TechMind_DataScience.ipynb data-science/notebooks/TechMind_DataScience.ipynb
```

Esto ejecutará todas las celdas del notebook y sobrescribirá los modelos binarios en `data-science/models/`.

---

## 5. Ingesta de Nuevos Documentos (PDF / DOCX)

Para ampliar el dataset con nuevos archivos técnicos o apuntes del equipo:

1. Coloca los archivos PDF o DOCX en la carpeta `documentos/`.
2. Ejecuta el script de ingesta interactivo:

```bash
python3 data-science/src/ingest_documents.py
```

El script procesará los documentos, extraerá el texto, te permitirá etiquetarlo temáticamente e insertará las nuevas filas en PostgreSQL. Si ingestás más de 3 documentos, el script te ofrecerá re-entrenar el modelo automáticamente.

---

## 6. Ubicación de Artefactos Generados

Al finalizar el entrenamiento, se generan dos archivos esenciales para que FastAPI realice la inferencia:

- `data-science/models/tfidf_vectorizer.joblib`: Transforma nuevos textos en vectores TF-IDF.
- `data-science/models/modelo_clasificador.joblib`: Realiza la predicción de la categoría y probabilidades.

Ambos modelos son cargados automáticamente por FastAPI (`app/main.py`) al iniciar el servidor.

> ✅ **Nota (v0.6.0):** Las rutas de serialización en el notebook fueron corregidas a `"../models/tfidf_vectorizer.joblib"` y `"../models/modelo_clasificador.joblib"`, lo que garantiza que los `.joblib` se generen siempre en `data-science/models/` independientemente del directorio desde donde se ejecute el notebook.

---

## 7. Nota sobre el cálculo de probabilidad

En `app/main.py`, el endpoint `POST /predecir` calcula la probabilidad de la siguiente forma:

```python
proba_arr    = modelo.predict_proba(vector)[0]   # distribución de probabilidad por clase
probabilidad = float(proba_arr.max())            # toma la probabilidad de la clase ganadora
```

Esto garantiza que el campo `probabilidad` en la respuesta JSON siempre refleja la confianza del modelo en la categoría predicha (un valor entre 0.0 y 1.0).
