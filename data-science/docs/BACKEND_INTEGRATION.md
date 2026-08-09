# 🔌 Guía de Integración — Backend (Java / Spring Boot)

> **¿Para quién es este documento?**
> Para el equipo de Backend que implementa la API REST en Java/Spring Boot.
> Explica cómo conectarse al microservicio Python (FastAPI), cómo levantar el entorno y cómo utilizar la base de datos PostgreSQL.

---

## 🏗️ Arquitectura del sistema (visión general)

```
  Postman / Cliente
       │
       │  POST /contenido  { "titulo": "...", "texto": "..." }
       ▼
┌──────────────────────────────────────────┐
│         Spring Boot — Puerto 8080        │  ← Implementado por Backend
│                                          │
│  1. Validar el request                   │
│  2. Llamar a FastAPI (HTTP interno)      │
│  3. Guardar el resultado en PostgreSQL   │
│  4. Devolver el JSON al cliente          │
└────────────────┬─────────────────────────┘
                 │  POST http://localhost:8000/predecir
                 │  (llamada interna, no expuesta al cliente)
                 ▼
┌──────────────────────────────────────────┐
│         FastAPI (Python) — Puerto 8000   │  ← Implementado por DS (Ernesto)
│                                          │
│  • Carga los modelos .joblib al arrancar │
│  • Clasifica el texto                    │
│  • Devuelve categoria + probabilidad     │
│    + palabras clave                      │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│         PostgreSQL — Puerto 5432         │
│         Base de datos: techmind          │
│                                          │
│  • contenidos   — dataset de entrenamiento│
│  • predicciones — log de inferencias     │
└──────────────────────────────────────────┘
```

**Regla clave:** El cliente / Postman interactúa únicamente con Spring Boot.
FastAPI actúa como un microservicio interno de clasificación de contenidos técnicos.

---

## 🚀 Guía de Ejecución Paso a Paso

### Paso 1 — Levantar PostgreSQL con Docker

Desde la raíz del repositorio (`tech-mind/`):

```bash
docker-compose up -d
```

Verifica que el contenedor esté en ejecución:
```bash
docker ps
# Salida esperada: techmind-postgres (Puerto 5432)
```

### Paso 2 — Configurar variables de entorno

Copia la plantilla `.env.example` a `.env` en la raíz del proyecto:

```bash
cp .env.example .env
```

El archivo `.env` ya viene configurado para entorno local:
```env
PG_HOST=localhost
PG_PORT=5432
PG_DB=techmind
PG_USER=techmind_user
PG_PASSWORD=techmind_pass
MODEL_PATH=./data-science/models/
```

### Paso 3 — Instalar dependencias de Python

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

pip install -r data-science/requirements.txt
```

### Paso 4 — Iniciar Spring Boot para inicializar la base de datos (Flyway)

> ⚠️ **Orden estricto de arranque:** Spring Boot debe iniciarse antes de migrar los datos para que Flyway cree las tablas oficiales (`contenidos` y `predicciones`) con los tipos de datos correctos (`BIGINT` / `BIGSERIAL`).

```bash
cd backend/api
./mvnw spring-boot:run
```

### Paso 5 — Cargar el dataset inicial de entrenamiento en PostgreSQL

Ejecuta el script de migración para poblar la tabla `contenidos` con los 61 registros iniciales:

```bash
python3 data-science/src/migrate_to_postgres.py
```

### Paso 6 — Iniciar el microservicio FastAPI

```bash
uvicorn app.main:app --reload --port 8000
```

Salida esperada en consola:
```
✅  Modelos cargados correctamente
✅  Conexión a PostgreSQL verificada correctamente
INFO:     Uvicorn running on http://0.0.0.0:8000
```

> **Documentación interactiva Swagger:** Disponible en [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📬 Contrato del Endpoint Interno `/predecir`

### Request: `POST http://localhost:8000/predecir`

**Headers:** `Content-Type: application/json`

**Body:**
```json
{
  "titulo": "Introducción a Spring Boot",
  "texto": "Conceptos básicos para la creación de APIs REST con Java y Spring Boot."
}
```

### Response: `200 OK`

```json
{
  "categoria": "Backend",
  "probabilidad": 0.8879,
  "informaciones_adicionales": [
    "spring boot",
    "spring",
    "boot",
    "java spring",
    "rest java"
  ]
}
```

### Campos devueltos:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `categoria` | `string` | Nombre exacto de una de las 8 categorías |
| `probabilidad` | `float` | Confianza de la predicción (de `0.0000` a `1.0000`) |
| `informaciones_adicionales` | `list[str]` | Top 5 palabras clave extraídas del texto por TF-IDF |

---

## 🏷️ Las 8 Categorías Disponibles

1. `Backend`
2. `Frontend`
3. `Data Science`
4. `DevOps`
5. `Mobile`
6. `Bases de Datos`
7. `Seguridad`
8. `Cloud`

---

## 🩺 Endpoints Auxiliares

### Health Check: `GET http://localhost:8000/health`
```json
{
  "status": "ok",
  "model_loaded": true,
  "version": "0.4.0"
}
```

### Listado de Categorías: `GET http://localhost:8000/categorias`
```json
{
  "categorias": [
    "Backend",
    "Bases de Datos",
    "Cloud",
    "Data Science",
    "DevOps",
    "Frontend",
    "Mobile",
    "Seguridad"
  ]
}
```
