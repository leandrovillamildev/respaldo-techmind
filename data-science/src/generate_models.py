#!/usr/bin/env python3
"""
generate_models.py — Generación rápida y offline de modelos .joblib para TechMind
"""

import os
import re
import joblib
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

BASE_DIR = Path(__file__).parent.parent
RAW_CSV_PATH = BASE_DIR / "data" / "raw" / "contenidos_tecnicos.csv"
MODELS_DIR = BASE_DIR / "models"

STOPWORDS_ES = {
    "el","la","los","las","un","una","unos","unas","de","del","al","a","en","y","o",
    "que","con","para","por","se","su","sus","es","son","este","esta","estos","estas",
    "como","más","mas","muy","entre","sobre","desde","hasta","tambien","también","ser",
    "utilizando","utiliza","permite","contenido","introduccion","introducción","tutorial",
    "cómo","como","así","asi","para","con","por","del","los","las","una","un","ante",
    "bajo","cabe","con","contra","desde","hacia","hasta","para","por","segun","según",
    "sin","so","sobre","tras","durante","mediante"
}

def limpiar_texto(texto: str) -> str:
    texto = str(texto).lower()
    texto = re.sub(r"[^a-záéíóúñü0-9\s]", " ", texto)
    palabras = texto.split()
    palabras = [p for p in palabras if p not in STOPWORDS_ES and len(p) > 2]
    return " ".join(palabras)

def generate():
    print("🤖 Entrenando y generando modelos ML (.joblib)...")
    if not RAW_CSV_PATH.is_file():
        raise FileNotFoundError(f"No se encontró el dataset CSV en {RAW_CSV_PATH}")
    
    df = pd.read_csv(RAW_CSV_PATH)
    df["texto_completo"] = df["titulo"].fillna("") + ". " + df["texto"].fillna("")
    df["texto_limpio"] = df["texto_completo"].apply(limpiar_texto)
    
    vectorizer = TfidfVectorizer(
        max_features=3000,
        ngram_range=(1, 2),
        min_df=1,
    )
    X = vectorizer.fit_transform(df["texto_limpio"])
    y = df["categoria"]
    
    modelo = LogisticRegression(max_iter=1000, class_weight="balanced", C=1.5)
    modelo.fit(X, y)
    
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, MODELS_DIR / "tfidf_vectorizer.joblib")
    joblib.dump(modelo, MODELS_DIR / "modelo_clasificador.joblib")
    print(f"✅ Artefactos .joblib generados exitosamente en {MODELS_DIR}")

if __name__ == "__main__":
    generate()
