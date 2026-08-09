# 📄 Ingesta de Documentos — TechMind

> Guía para ampliar el dataset de entrenamiento con archivos PDF o DOCX.
> Cuantos más documentos reales agregues, mejor clasifica el modelo.

---

## ¿Por qué hacer esto?

El modelo inicial fue entrenado con **61 registros sintéticos** → accuracy ~0.69.
Con **≥250 registros reales** el accuracy estimado sube a **≥0.82**.

Esta herramienta te permite subir cualquier artículo técnico, guía, documentación oficial o apunte del equipo en formato PDF o DOCX, y el sistema lo procesa automáticamente.

---

## Setup (solo la primera vez)

```bash
pip install -r data-science/requirements.txt
```

---

## Uso — Formas de ejecutar

### Forma 1 — Procesar la carpeta documentos/ (recomendado)

```bash
# 1. Colocá tus PDFs y DOCXs en la carpeta documentos/
cp mis_guias/*.pdf documentos/

# 2. Ejecutar
python3 data-science/src/ingest_documents.py
```

### Forma 2 — Procesar un archivo específico

```bash
python3 data-science/src/ingest_documents.py --archivo documentos/guia_spring_boot.pdf
```

### Forma 3 — Archivo con categoría ya definida (sin preguntas)

```bash
python3 data-science/src/ingest_documents.py --archivo documentos/docker_intro.pdf --categoria DevOps
```

---

## Re-entrenamiento del Modelo

Una vez ingeridos los nuevos documentos, podés re-entrenar el modelo ejecutando:

```bash
cd data-science/notebooks
jupyter nbconvert --to notebook --execute --inplace TechMind_DataScience.ipynb
cd ../..
```

Los artefactos `.joblib` en `data-science/models/` se actualizarán automáticamente.
