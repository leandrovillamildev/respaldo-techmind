"""
app/main.py
Microservicio FastAPI — TechMind · Ciencia de Datos

Endpoints:
    POST /predecir   — inferencia (consumido internamente por Spring Boot)
    GET  /health     — health check
    GET  /categorias — lista las 8 categorías disponibles
    GET  /docs       — documentación Swagger (automática)

Uso:
    uvicorn app.main:app --reload --port 8000
"""

import hashlib
import os
import re
import secrets
from contextlib import asynccontextmanager

import joblib
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, field_validator

from app.database import init_db, get_predicciones, get_analytics_data, delete_prediccion

load_dotenv()

# ── Configuración y Estado de Autenticación Admin ─────────────────────────────
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
ADMIN_PASSWORD_HASH = hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest()

ACTIVE_TOKENS = set()


class LoginRequest(BaseModel):
    username: str
    password: str


def verificar_admin_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de autorización requerido")
    token = authorization.split("Bearer ")[1].strip()
    if token not in ACTIVE_TOKENS:
        raise HTTPException(status_code=401, detail="Token inválido o sesión expirada")
    return token


# ── Estado global del modelo ──────────────────────────────────────────────────
vectorizer = None
modelo = None

# ── Stopwords en español y ruido técnico ─────────────────────────────────────
try:
    import nltk
    nltk.download('stopwords', quiet=True)
    from nltk.corpus import stopwords
    STOPWORDS_ES = set(stopwords.words('spanish'))
except Exception:
    STOPWORDS_ES = {
        "el","la","los","las","un","una","unos","unas","de","del","al","a","en","y","o",
        "que","con","para","por","se","su","sus","es","son","este","esta","estos","estas",
        "como","más","mas","muy","entre","sobre","desde","hasta","tambien","también","ser",
        "utilizando","utiliza","permite","contenido","introduccion","introducción","tutorial",
        "cómo","como","así","asi","uso","usando","ejemplo","guia","guía"
    }

RUIDO_TECNICO = {
    "tutorial", "guia", "guía", "introduccion", "introducción", "explicacion", "explicación",
    "concepto", "conceptos", "basico", "básicos", "basicos", "básica", "basica", "avanzado",
    "avanzada", "desarrollo", "creacion", "creación", "uso", "usando", "ejemplo", "ejemplos",
    "practica", "práctica", "practicas", "prácticas", "paso", "pasos", "aplicacion", "aplicación",
    "aplicaciones", "sistema", "sistemas", "servicio", "servicios", "completo", "completa"
}
RUIDO_CONECTORES = {
    "mediante", "globalmente", "además", "ademas", "través", "traves", "debido", "según", "segun",
    "cada", "forma", "manera", "principalmente", "especialmente", "actualmente", "diferentes",
    "varios", "varias", "asimismo", "generalmente", "realmente", "nivel", "tipo", "tipos",
    "parte", "partes", "medio", "medios", "modo", "modos", "hacer", "hace", "hacen", "haciendo",
    "realizar", "realiza", "realizan", "realizando", "permite", "permiten", "permitiendo"
}
STOPWORDS_TOTAL = STOPWORDS_ES.union(RUIDO_TECNICO).union(RUIDO_CONECTORES)


# ── Funciones del pipeline ───────────────────────────────────────────────────

def limpiar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúñü0-9\s]", " ", texto)
    palabras = texto.split()
    palabras = [p for p in palabras if p not in STOPWORDS_TOTAL and len(p) > 2]
    return " ".join(palabras)


def extraer_keywords(texto_limpio: str, top_n: int = 5) -> list:
    vector = vectorizer.transform([texto_limpio])
    feature_names = vectorizer.get_feature_names_out()
    scores = vector.toarray()[0]
    top_indices = scores.argsort()[::-1][:top_n]
    return [feature_names[i] for i in top_indices if scores[i] > 0]


# ── Lifespan: carga el modelo al arrancar ─────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    global vectorizer, modelo
    
    # Búsqueda inteligente de rutas para los archivos .joblib
    env_path = os.getenv("MODEL_PATH")
    possible_paths = [
        env_path,
        os.path.join("data-science", "models"),
        os.path.join("..", "data-science", "models"),
        "./"
    ]
    
    model_path = None
    for p in possible_paths:
        if p and os.path.exists(os.path.join(p, "tfidf_vectorizer.joblib")):
            model_path = p
            break
            
    if not model_path:
        model_path = env_path or os.path.join("data-science", "models")

    try:
        vectorizer = joblib.load(os.path.join(model_path, "tfidf_vectorizer.joblib"))
        modelo     = joblib.load(os.path.join(model_path, "modelo_clasificador.joblib"))
        print(f"✅  Modelos cargados correctamente desde '{model_path}'")
    except FileNotFoundError as e:
        print(f"❌  No se encontraron los .joblib en '{model_path}': {e}")
        print("    Verificá que la carpeta data-science/models/ contenga los archivos .joblib.")
        raise
    init_db()
    yield
    vectorizer = None
    modelo = None


# ── Aplicación FastAPI ────────────────────────────────────────────────────────

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="TechMind — API de Ciencia de Datos",
    description="Microservicio interno de clasificación de contenidos técnicos. Consumido por Spring Boot.",
    version="0.4.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Schemas Pydantic ──────────────────────────────────────────────────────────

class ContenidoRequest(BaseModel):
    titulo: str
    texto:  str

    @field_validator("titulo", "texto")
    @classmethod
    def no_vacio(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v.strip()


class PrediccionResponse(BaseModel):
    categoria:               str
    probabilidad:            float
    informaciones_adicionales: list


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.post(
    "/predecir",
    response_model=PrediccionResponse,
    summary="Clasificar un contenido técnico",
    description="""
Recibe el **título** y **texto** de un contenido técnico y devuelve:
- `categoria` — una de las 8 categorías del modelo
- `probabilidad` — confianza del modelo (0 a 1)
- `informaciones_adicionales` — top 5 palabras clave por peso TF-IDF
""",
)
def predecir(req: ContenidoRequest):
    if vectorizer is None or modelo is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible. Revisá los .joblib.")

    texto_completo = f"{req.titulo}. {req.texto}"
    texto_limpio   = limpiar_texto(texto_completo)

    vector       = vectorizer.transform([texto_limpio])
    categoria    = modelo.predict(vector)[0]
    proba_arr    = modelo.predict_proba(vector)[0]
    probabilidad = float(proba_arr.max())
    informaciones_adicionales = extraer_keywords(texto_limpio)

    return PrediccionResponse(
        categoria=categoria,
        probabilidad=round(probabilidad, 4),
        informaciones_adicionales=informaciones_adicionales,
    )


@app.get(
    "/health",
    summary="Health check",
    description="Verificá que FastAPI y el modelo están operativos. Spring Boot debe llamar este endpoint antes de hacer predicciones.",
)
def health():
    return {
        "status":       "ok" if vectorizer is not None else "degraded",
        "model_loaded": vectorizer is not None,
        "version":      "0.4.0",
    }


@app.get(
    "/predicciones",
    summary="Historial de predicciones",
    description="Devuelve el historial de predicciones registradas en la base de datos PostgreSQL.",
)
def listar_predicciones(limit: int = 50):
    return get_predicciones(limit=limit)


@app.post(
    "/auth/login",
    summary="Login de Administrador",
    description="Valida las credenciales del administrador y genera un token de sesión.",
)
def login(req: LoginRequest):
    pwd_hash = hashlib.sha256(req.password.encode()).hexdigest()
    if req.username == ADMIN_USER and (req.password == ADMIN_PASSWORD or pwd_hash == ADMIN_PASSWORD_HASH):
        token = secrets.token_hex(32)
        ACTIVE_TOKENS.add(token)
        return {"status": "ok", "token": token, "username": req.username}
    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")


@app.post(
    "/auth/logout",
    summary="Logout de Administrador",
    description="Invalida el token de sesión del administrador en el servidor.",
)
def logout(authorization: str = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split("Bearer ")[1].strip()
        ACTIVE_TOKENS.discard(token)
    return {"status": "ok", "message": "Sesión cerrada correctamente"}


@app.delete(
    "/predicciones/{prediccion_id}",
    summary="Eliminar una consulta del historial (Solo Admin)",
    description="Elimina la predicción y su contenido en cascada. Requiere token de administrador.",
)
def eliminar_prediccion(prediccion_id: int, token: str = Depends(verificar_admin_token)):
    exito = delete_prediccion(prediccion_id)
    if not exito:
        raise HTTPException(status_code=404, detail=f"No se encontró la consulta ID {prediccion_id}")
    return {"status": "deleted", "id": prediccion_id}




@app.get(
    "/categorias",
    summary="Lista de categorías disponibles",
    description="Devuelve las 8 categorías en las que el modelo puede clasificar un contenido.",
)
def categorias():
    if modelo is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")
    return {"categorias": sorted(modelo.classes_.tolist())}


# ── Módulo de Métricas de Servidor OCI ───────────────────────────────────────

import time

START_TIME = time.time()

try:
    import psutil
except ImportError:
    psutil = None


def format_uptime(seconds: float) -> str:
    secs = int(seconds)
    days = secs // 86400
    hours = (secs % 86400) // 3600
    minutes = (secs % 3600) // 60
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m {secs % 60}s"


def obtener_metricas_sistema() -> dict:
    uptime_sec = time.time() - START_TIME
    if psutil is not None:
        try:
            if hasattr(psutil, "boot_time"):
                uptime_sec = time.time() - psutil.boot_time()
            cpu = psutil.cpu_percent(interval=0.1)
            vm = psutil.virtual_memory()
            swap = psutil.swap_memory()
            return {
                "uptime": format_uptime(uptime_sec),
                "cpu_percent": round(cpu, 1),
                "ram_total_mb": round(vm.total / (1024 * 1024), 1),
                "ram_used_mb": round(vm.used / (1024 * 1024), 1),
                "ram_free_mb": round(vm.available / (1024 * 1024), 1),
                "ram_percent": round(vm.percent, 1),
                "swap_total_mb": round(swap.total / (1024 * 1024), 1),
                "swap_used_mb": round(swap.used / (1024 * 1024), 1),
                "swap_percent": round(swap.percent, 1),
            }
        except Exception:
            pass

    load = 0.0
    if hasattr(os, "getloadavg"):
        try:
            load = round(os.getloadavg()[0] * 100 / (os.cpu_count() or 1), 1)
        except Exception:
            pass

    ram_total, ram_avail = 1024.0, 512.0
    if os.path.exists("/proc/meminfo"):
        try:
            mem = {}
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    parts = line.split(":")
                    if len(parts) == 2:
                        key = parts[0].strip()
                        val = parts[1].strip().split()[0]
                        mem[key] = int(val)
            ram_total = round(mem.get("MemTotal", 1048576) / 1024, 1)
            ram_avail = round(mem.get("MemAvailable", mem.get("MemFree", 524288)) / 1024, 1)
        except Exception:
            pass

    ram_used = round(ram_total - ram_avail, 1)
    ram_pct = round((ram_used / ram_total) * 100, 1) if ram_total > 0 else 0.0

    return {
        "uptime": format_uptime(uptime_sec),
        "cpu_percent": load,
        "ram_total_mb": ram_total,
        "ram_used_mb": ram_used,
        "ram_free_mb": ram_avail,
        "ram_percent": ram_pct,
        "swap_total_mb": 0.0,
        "swap_used_mb": 0.0,
        "swap_percent": 0.0,
    }


@app.get(
    "/system-stats",
    summary="Métricas de hardware del servidor OCI",
    description="Devuelve el consumo en tiempo real de CPU, RAM (total, usada, libre) y Swap de la instancia.",
)
def system_stats():
    return obtener_metricas_sistema()


@app.get(
    "/analytics",
    summary="Dashboard de estadísticas y análisis visual",
    description="Devuelve métricas agrupadas de la base de datos PostgreSQL: distribución por categoría, horas pico de actividad y top keywords.",
)
def analytics(tz_offset: int = 0):
    return get_analytics_data(tz_offset_minutes=tz_offset)
