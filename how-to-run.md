# 🚀 Cómo Levantar el Microservicio Python — TechMind

> **Para:** Equipo de Backend (Java / Spring Boot) — **Windows**
> **Objetivo:** Tener la API de clasificación corriendo en `http://localhost:8000` para que Spring Boot pueda llamarla.

---

## ¿Qué es esto?

El componente de Data Science es un **microservicio** escrito en Python (FastAPI) que expone un endpoint:

```
POST http://localhost:8000/predecir
```

Spring Boot lo llama internamente cada vez que recibe un contenido para clasificar. **No necesitás entender Python** — solo tenés que levantarlo.

---

## ⚡ Opción rápida — Script automático (recomendado)

Si no querés hacer los pasos manualmente, el repositorio incluye un script que **hace todo por vos**:

### Primera vez
```powershell
python setup.py
```

El script verifica Python, crea el entorno virtual, instala dependencias, levanta Docker, migra la base de datos e inicia la API. Si algo falla, te dice exactamente qué está mal.

---

## 🐳 Opción 100% Dockerizada (Producción / Demo)

Si querés levantar los **4 componentes del sistema** (PostgreSQL + FastAPI + Spring Boot + Frontend Web UI) totalmente dentro de contenedores Docker con un solo comando (sin necesidad de tener Java ni Python instalados en la PC):

### Vía Script Automático:
```powershell
python setup.py --docker
```

### Vía Docker Compose directamente:
```powershell
docker-compose --profile full up -d --build
```

Esto compilará las imágenes y dejará todo el stack activo en:
* 🎨 **Frontend Web UI:** **[http://localhost:5173](http://localhost:5173)**
* ☕ **Spring Boot API:** `http://localhost:8080`
* 🤖 **FastAPI ML Service:** `http://localhost:8000`
* 📖 **Documentación Swagger:** `http://localhost:8000/docs`

Para detener todos los contenedores:
```powershell
docker-compose --profile full down
```

> ⚠️ Requiere tener **Python** y **Docker Desktop** instalados (ver requisitos abajo).

---

## 📋 Pasos manuales (alternativa)

Si preferís ejecutar cada paso vos mismo, seguí esta guía:

---

## ✅ Requisitos previos

Antes de empezar, verificá que tenés instalado:

| Herramienta | Versión mínima | ¿Cómo verificar? |
|-------------|----------------|------------------|
| **Python** | 3.10 o superior | Abrí PowerShell y escribí: `python --version` |
| **Docker Desktop** | cualquier versión reciente | Abrirlo y ver que el ícono esté verde |
| **Git** | cualquier versión | `git --version` |

### ¿No tenés Python instalado?

1. Entrá a [python.org/downloads](https://www.python.org/downloads/) y descargá la versión **3.12.x**
2. En el instalador, **marcá obligatoriamente** la opción **"Add Python to PATH"** (está abajo del todo)
3. Hacé click en "Install Now"
4. Cerrá y volvé a abrir PowerShell

### ¿No tenés Docker Desktop?

1. Entrá a [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Descargá e instalá la versión para Windows
3. Reiniciá la PC si te lo pide

---

## 📋 Pasos — Primera vez

> 💡 **Usá PowerShell** para todos los comandos (no el símbolo del sistema CMD).
> Podés abrirlo buscando "PowerShell" en el menú Inicio.

---

### Paso 1 — Clonar el repositorio

```powershell
git clone https://github.com/No-Country-simulation/g9-latam-techmind-team37.git
cd g9-latam-techmind-team37
```

---

### Paso 2 — Crear el entorno virtual de Python

Un "entorno virtual" es una carpeta aislada donde se instalan las dependencias del proyecto, sin afectar el resto de tu PC.

```powershell
python -m venv venv
venv\Scripts\activate
```

> ✅ Sabés que funcionó cuando el prompt de PowerShell muestra **(venv)** al principio de la línea, así:
> ```
> (venv) PS C:\Users\tu-usuario\g9-latam-techmind-team37>
> ```

> ⚠️ **Si PowerShell dice "no se puede ejecutar scripts"**, ejecutá esto una sola vez y después volvé a intentar:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

### Paso 3 — Instalar las dependencias de Python

```powershell
pip install -r data-science\requirements.txt
```

Esto descarga todos los paquetes necesarios (FastAPI, scikit-learn, etc.). Puede tardar **1-2 minutos** la primera vez.

---

### Paso 4 — Copiar el archivo de configuración

```powershell
copy .env.example .env
```

El archivo `.env` ya viene configurado para desarrollo local. **No necesitás modificar nada.**

---

### Paso 5 — Levantar PostgreSQL con Docker

Asegurate de que **Docker Desktop esté abierto** (el ícono de la ballena en la barra de tareas debe estar verde), luego ejecutá:

```powershell
docker-compose up -d
```

Verificá que el contenedor esté corriendo:
```powershell
docker ps
```
Deberías ver `techmind-postgres` en la lista con el puerto `5432`.

---

### Paso 6 — Iniciar Spring Boot para crear las tablas (Flyway)

> ⚠️ **Orden estricto de arranque:** Spring Boot debe iniciarse antes de migrar los datos para que Flyway cree las tablas con los tipos de datos correctos (`BIGINT` / `BIGSERIAL`).

En una terminal separada:
```powershell
cd backend\api
.\mvnw spring-boot:run
```

Una vez que veas `Started ApiApplication`, la base de datos tendrá el esquema oficial listo.

---

### Paso 7 — Cargar el dataset ampliado de entrenamiento en PostgreSQL

En tu terminal principal con el entorno `(venv)` activo:

```powershell
python data-science\src\migrate_to_postgres.py
```

Esto inserta los **221 registros de entrenamiento** en la tabla `contenidos`.

---

### Paso 8 — Iniciar el microservicio FastAPI

En la terminal principal:

```powershell
uvicorn app.main:app --reload --port 8000
```

Si todo salió bien, vas a ver esto en la consola:

```
✅  Modelos cargados correctamente
✅  Conexión a PostgreSQL verificada correctamente
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

> ✅ **Los modelos se auto-generan automáticamente** si no existen al ejecutar `setup.py` o `setup.py --docker`, y también están almacenados en `data-science\models\`.

---

### Paso 9 — Iniciar el Frontend Web UI

En una tercera terminal:

```powershell
python -m http.server 5173 --directory frontend
```

Abrí en tu navegador:
👉 **[http://localhost:5173](http://localhost:5173)**

---

## 🔁 Las veces siguientes (Cómo levantar el stack completo)

Una vez instalado todo, para levantar los 4 componentes del sistema:

```powershell
# 1. Base de Datos (Docker)
docker-compose up -d

# 2. Backend Java / Spring Boot (Terminal 1)
cd backend\api
.\mvnw spring-boot:run

# 3. Microservicio Python / FastAPI (Terminal 2 con venv activo)
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

# 4. Frontend Web UI (Terminal 3)
python -m http.server 5173 --directory frontend
```

---

## 🧪 Verificar que funciona

### Opción A — Desde el navegador

Abrí Chrome/Edge y entrá a:

```
http://localhost:8000/health
```

Deberías ver:
```json
{ "status": "ok", "model_loaded": true, "version": "0.4.0" }
```

### Opción B — Documentación interactiva (Swagger)

Abrí en el navegador:
```
http://localhost:8000/docs
```

Desde ahí podés probar todos los endpoints directamente, sin Postman.

### Opción C — Probar con PowerShell

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/predecir" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo": "Introduccion a Spring Boot", "texto": "Creacion de APIs REST con Java y Spring Boot."}'
```

Respuesta esperada:
```json
{
  "categoria": "Backend",
  "probabilidad": 0.8879,
  "informaciones_adicionales": ["spring boot", "java", "api rest", "creacion apis", "spring"]
}
```

---

## 📬 Contrato del endpoint — Lo que Spring Boot debe llamar

### `POST http://localhost:8000/predecir`

**Request body:**
```json
{
  "titulo": "string — título del contenido técnico",
  "texto":  "string — cuerpo del contenido técnico"
}
```

**Response 200 OK:**
```json
{
  "categoria":               "Backend",
  "probabilidad":            0.8879,
  "informaciones_adicionales": ["spring boot", "java", "api rest", "creacion apis", "spring"]
}
```

**Las 8 categorías posibles:**
`Backend` · `Frontend` · `Data Science` · `DevOps` · `Mobile` · `Bases de Datos` · `Seguridad` · `Cloud`

---

## 🛑 Errores comunes y soluciones

| Error que ves | Causa | Solución |
|---------------|-------|----------|
| `'python' is not recognized` | Python no está instalado o no está en el PATH | Reinstalar Python marcando "Add Python to PATH" |
| `(venv)` no aparece | El entorno virtual no está activado | Ejecutar `venv\Scripts\activate` |
| `cannot be loaded because running scripts is disabled` | Política de ejecución de PowerShell | Ejecutar `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `No module named 'fastapi'` | Las dependencias no se instalaron | Ejecutar `pip install -r data-science\requirements.txt` |
| `FileNotFoundError: .joblib` | Los archivos del modelo no existen | Pedirle los `.joblib` a Ernesto y ponerlos en `data-science\models\` |
| `Error: connect ECONNREFUSED 5432` | PostgreSQL no está corriendo | Ejecutar `docker-compose up -d` |
| `docker: command not found` | Docker Desktop no está instalado | Instalar Docker Desktop desde docker.com |
| Docker Desktop no arranca | WSL 2 no está habilitado | Seguir la guía oficial: [docs.docker.com/desktop/windows](https://docs.docker.com/desktop/windows/install/) |

---

## 📝 Nota para Ernesto (macOS)

Los mismos pasos aplican en macOS ejecutando:

```bash
# Paso 2 — Crear entorno virtual
python3 -m venv venv && source venv/bin/activate

# Paso 3 — Instalar dependencias
pip install -r data-science/requirements.txt

# Paso 4 — Configurar variables de entorno
cp .env.example .env

# Paso 5 — Levantar PostgreSQL
docker-compose up -d

# Paso 6 — Iniciar Spring Boot (Crea las tablas con Flyway)
cd backend/api && ./mvnw spring-boot:run

# Paso 7 — Cargar dataset de entrenamiento (221 registros)
python3 data-science/src/migrate_to_postgres.py

# Paso 8 — Iniciar FastAPI
uvicorn app.main:app --reload --port 8000

# Paso 9 — Iniciar Frontend Web UI (http://localhost:5173)
python3 -m http.server 5173 --directory frontend
```


---

*TechMind · Hackathon G9 LATAM · Equipo 37*
