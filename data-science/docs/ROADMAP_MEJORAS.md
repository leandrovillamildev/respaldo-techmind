# 🗺️ TechMind — Roadmap de Mejoras

> Mejoras pendientes organizadas por impacto y esfuerzo estimado.
> Este documento se actualiza a medida que el proyecto avanza.
> Última actualización: 2026-07-28

---

## Leyenda

| Símbolo | Prioridad |
|---------|-----------|
| 🔴 | Crítico — impacta la calidad de la demo |
| 🟠 | Alto — mejora significativa del producto |
| 🟡 | Medio — mejora notable, post-demo |
| 🟢 | Bajo — nice-to-have a futuro |

| Estado | Significado |
|--------|-------------|
| ⬜ Pendiente | No iniciado |
| 🔄 En progreso | En desarrollo activo |
| ✅ Completado | Implementado |

---

## 🤖 Data Science (FastAPI / ML)

### 🔴 MEJORA-DS-001 — Ampliar el dataset (61 → 221+ registros)

| Campo | Valor |
|---|---|
| **Estado** | ✅ Completado |
| **Owner** | Ernesto |
| **Esfuerzo** | 2-3 horas |

**Resultado:** Dataset ampliado a 221 registros técnicos balanceados en `data-science/data/raw/contenidos_tecnicos.csv` e ingresados en PostgreSQL.

---

### 🎨 MEJORA-INFRA-001 — Diagrama de Arquitectura Infográfico en README.md

| Campo | Valor |
|---|---|
| **Estado** | ✅ Completado |
| **Owner** | Ernesto |
| **Esfuerzo** | 1 hora |

**Resultado:** Generada e integrada la infografía `assets/techmind_project_flow.png` en `README.md`.

---

### 🧪 MEJORA-QA-001 — Suite de Pruebas Automatizadas E2E (Sprint 2)

| Campo | Valor |
|---|---|
| **Estado** | ✅ Completado |
| **Owner** | QA Team / Assistant |
| **Esfuerzo** | 1 hora |

**Resultado:** Suite de 14 casos de prueba automatizados con 100% de tasa de éxito documentada en `qa/reportes/resultados-sprint-2.md`.

---

### 🔴 MEJORA-DS-002 — Reemplazar stopwords manuales por NLTK

| Campo | Valor |
|---|---|
| **Estado** | ✅ Completado |
| **Owner** | Ernesto |
| **Esfuerzo** | 30 min |

**Problema:** La lista manual de stopwords tiene ~30 palabras. NLTK incluye 154 stopwords en español, lo que mejora directamente la calidad de las keywords y la clasificación.

**Acción:** Reemplazar en `app/main.py` y en el notebook:
```python
# Antes (manual, ~30 palabras)
STOPWORDS_ES = {"el", "la", "los", ...}

# Después (NLTK, 154 palabras)
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
STOPWORDS_ES = set(stopwords.words('spanish'))
```

---

### 🟠 MEJORA-DS-003 — Agregar campo `confianza` en la respuesta

| Campo | Valor |
|---|---|
| **Estado** | ⬜ Pendiente |
| **Owner** | Ernesto |
| **Esfuerzo** | 30 min |

**Problema:** Cuando el modelo no reconoce el texto (idioma incorrecto, texto vacío), retorna ~12.5% de probabilidad (1/8 categorías), lo cual es engañoso.

**Acción:** Agregar campo `confianza` en `PrediccionResponse`:
```python
def get_confianza(probabilidad: float) -> str:
    if probabilidad >= 0.70:
        return "alta"
    elif probabilidad >= 0.45:
        return "media"
    else:
        return "baja"
```

**Respuesta mejorada:**
```json
{
  "categoria": "DevOps",
  "probabilidad": 0.74,
  "confianza": "alta",
  "informaciones_adicionales": ["kubernetes", "docker", "pods"]
}
```

---

### 🟠 MEJORA-DS-004 — Cross-validation con k-fold estratificado

| Campo | Valor |
|---|---|
| **Estado** | ⬜ Pendiente |
| **Owner** | Ernesto |
| **Esfuerzo** | 1 hora |

**Problema:** La evaluación usa un único split (75/25). Con ~60 filas, la métrica puede variar ±10pp según la semilla.

**Acción:** Implementar `StratifiedKFold(n_splits=5)` en el notebook para reportar `mean ± std` de accuracy y F1-macro.

---

### 🟡 MEJORA-DS-005 — Evaluar LinearSVC como alternativa al modelo actual

| Campo | Valor |
|---|---|
| **Estado** | ⬜ Pendiente |
| **Owner** | Ernesto |
| **Esfuerzo** | 1-2 horas |

**Contexto:** LinearSVC generalmente supera a LogisticRegression en clasificación de texto con TF-IDF. Comparar formalmente con `GridSearchCV`.

---

### 🟡 MEJORA-DS-006 — Sistema de recomendación de contenidos similares

| Campo | Valor |
|---|---|
| **Estado** | ⬜ Pendiente |
| **Owner** | Ernesto |
| **Esfuerzo** | 2-3 horas |

**Descripción:** Endpoint `POST /recomendar` que devuelve los K contenidos más similares usando cosine similarity sobre la matriz TF-IDF existente (sin dependencias adicionales).

```python
from sklearn.metrics.pairwise import cosine_similarity

def recomendar(texto_consulta: str, top_k: int = 3):
    vector = tfidf_vectorizer.transform([limpiar_texto(texto_consulta)])
    similitudes = cosine_similarity(vector, X_matrix).flatten()
    top_indices = similitudes.argsort()[::-1][:top_k]
    return df.iloc[top_indices][["titulo", "categoria"]].to_dict(orient="records")
```

---

### 🟡 MEJORA-DS-007 — Explicabilidad del modelo (XAI)

| Campo | Valor |
|---|---|
| **Estado** | ⬜ Pendiente |
| **Owner** | Ernesto |
| **Esfuerzo** | 2 horas |

**Descripción:** Agregar campo `explicacion` en la respuesta usando los coeficientes de la Regresión Logística (`modelo.coef_`) para mostrar los tokens que más influyeron en la predicción. No requiere dependencias extra.

```json
{
  "categoria": "DevOps",
  "probabilidad": 0.74,
  "informaciones_adicionales": ["kubernetes", "docker"],
  "explicacion": ["kubernetes (+0.42)", "despliegue (+0.31)", "contenedor (+0.27)"]
}
```

---

## 🔵 Backend (Spring Boot)

### 🔴 MEJORA-BE-001 — Agregar configuración CORS

| Campo | Valor |
|---|---|
| **Estado** | ✅ Completado |
| **Owner** | Equipo Backend |
| **Esfuerzo** | 15 min |

**Resultado:** `@CrossOrigin(origins = "*")` implementado en `ContenidoController`. CORS para el endpoint `/actuator/health` configurado vía `management.endpoints.web.cors.allowed-origins=*` en `application.properties`.

---

### 🟠 MEJORA-BE-002 — Exponer endpoint de salud para monitoreo

| Campo | Valor |
|---|---|
| **Estado** | ✅ Completado |
| **Owner** | Equipo Backend |
| **Esfuerzo** | 30 min |

**Resultado:** Agregado `spring-boot-starter-actuator` al `pom.xml`. El endpoint `GET /actuator/health` responde `{ "status": "UP" }` cuando el servicio está operativo. El frontend lo consume al cargar la página para actualizar el indicador LED en tiempo real. FastAPI sigue siendo verificado por Spring Boot vía `GET /health` antes de cada clasificación (comportamiento previo conservado).

---

### 🟠 MEJORA-BE-003 — Agregar endpoints GET para consultar predicciones

| Campo | Valor |
|---|---|
| **Estado** | ⬜ Pendiente |
| **Owner** | Equipo Backend |
| **Esfuerzo** | 1 hora |

**Descripción:** Actualmente no existe ningún endpoint GET. Agregar:
- `GET /predicciones` → lista paginada de predicciones
- `GET /predicciones/{id}` → detalle de una predicción
- `GET /predicciones?categoria=DevOps` → filtro por categoría

---

### 🟡 MEJORA-BE-004 — Procesar múltiples contenidos en batch

| Campo | Valor |
|---|---|
| **Estado** | ⬜ Pendiente |
| **Owner** | Ambos equipos |
| **Esfuerzo** | 3-4 horas |

**Descripción:** Endpoint `POST /contenido/batch` que recibe un array JSON y clasifica múltiples textos en una sola llamada, usando `vectorizer.transform` sobre el batch completo (más eficiente que N llamadas individuales).

---

## ☁️ Infraestructura / OCI

### 🟠 MEJORA-OCI-001 — Subir modelos `.joblib` a OCI Object Storage

| Campo | Valor |
|---|---|
| **Estado** | ⬜ Pendiente |
| **Owner** | Todo el equipo |
| **Esfuerzo** | 1 hora |

**Acción:** Subir `tfidf_vectorizer.joblib` y `modelo_clasificador.joblib` a OCI Object Storage y actualizar la variable `MODEL_PATH` para que FastAPI los descargue al iniciar.

---

### 🟡 MEJORA-OCI-002 — Dashboard de monitoreo

| Campo | Valor |
|---|---|
| **Estado** | ⬜ Pendiente |
| **Owner** | Todo el equipo |
| **Esfuerzo** | 4-8 horas |

**Descripción:** Dashboard con Streamlit o Metabase mostrando distribución de categorías predichas, distribución de probabilidades (alertar si muchas predicciones caen bajo 0.50) y drift de vocabulario.

---

*TechMind G9 LATAM Team 37 — Roadmap actualizado el 2026-07-30*
