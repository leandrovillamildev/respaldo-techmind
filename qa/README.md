# 🧪 Guía de QA, Testing e Informe de Resultados — TechMind

Este documento describe la estrategia integral de **Aseguramiento de Calidad (QA)**, los requisitos de entorno, la guía de ejecución mediante el orquestador `setup.py` y el **Informe Final de Resultados** sobre los 57 Casos de Prueba (CP) ejecutados a lo largo de los 4 Sprints del proyecto **TechMind**.

---

## 📋 Tabla de Contenidos

1. [Requisitos Previos y Herramientas](#-1-requisitos-previos-y-herramientas)
2. [Instalación y Ejecución Rápida (`setup.py`)](#-2-instalación-y-ejecución-rápida-setuppy)
3. [Configuración del Entorno de Pruebas (Postman)](#-3-configuración-del-entorno-de-pruebas-postman)
4. [Resumen Ejecutivo de Resultados QA](#-4-resumen-ejecutivo-de-resultados-qa)
5. [Desglose por Módulo y Tipo de Prueba](#-5-desglose-por-módulo-y-tipo-de-prueba)
6. [Detalle Completo de Casos de Prueba (CP-01 a CP-57)](#-6-detalle-completo-de-casos-de-prueba)
   - [Sprint 1: Microservicio FastAPI & NLP](#-sprint-1-microservicio-fastapi--nlp-25-casos)
   - [Sprint 2: Data QA — PostgreSQL (`techmind`)](#-sprint-2-data-qa--postgresql-techmind-17-casos)
   - [Sprint 3: Backend Spring Boot & ML](#-sprint-3-backend-spring-boot--ml-6-casos)
   - [Sprint 4: Frontend (Vanilla JS / Tailwind)](#-sprint-4-frontend-vanilla-js--tailwind-9-casos)
7. [Assertions Automatizadas en Postman](#-7-assertions-automatizadas-en-postman)
8. [Registro y Reporte de Evidencias](#-8-registro-y-reporte-de-evidencias)

---

## 🛠️ 1. Requisitos Previos y Herramientas

Para levantar el entorno completo y ejecutar la suite de pruebas necesitás contar con los siguientes elementos:

* **Python 3.10+** (para FastAPI, dependencias NLP y ejecución de `setup.py`).
* **Java 17 / Maven** (para la API Backend en Spring Boot).
* **Docker Desktop & Docker Compose** (para PostgreSQL o ejecución containerizada completa).
* **Postman** (Client Desktop o Web) para las colecciones automatizadas de API.
* **Navegador Web** (Chrome/Firefox/Edge) para acceso a Swagger UI y pruebas e2e en Frontend.

---

## 🚀 2. Instalación y Ejecución Rápida (`setup.py`)

El repositorio incluye el orquestador universal `setup.py` que instala dependencias y pone en marcha todos los microservicios en Windows, macOS o Linux.

```bash
# Modo A: Desarrollo local (Docker para PostgreSQL + APIs y Frontend nativos)
python setup.py

# Modo B: Inicio rápido de servicios previamente instalados
python setup.py --start

# Modo C: 100% Dockerizado (PostgreSQL + FastAPI + Spring Boot + Frontend)
python setup.py --docker
```

### Mapas de Puertos y Servicios Activos:

| Servicio | URL / Host | Descripción |
|---|---|---|
| **Frontend** | `http://localhost:5173` | Interfaz de Usuario (Vanilla JS + Tailwind) |
| **Backend Spring Boot** | `http://localhost:8080` | Core API, Validación & Persistencia |
| **Microservicio FastAPI** | `http://localhost:8000` | Documentación Swagger (`http://localhost:8000/docs`) |
| **PostgreSQL (`techmind`)** | `localhost:5432` | Base de datos relacional del proyecto |

---

## ⚙️ 3. Configuración del Entorno de Pruebas (Postman)

1. Abrí **Postman**.
2. Hacé clic en **Import** (esquina superior izquierda).
3. Seleccioná y cargá los archivos ubicados en la carpeta `postman/`:
   * `techmind_collection.json` *(Colección de peticiones y assertions)*.
   * `techmind_environment.json` *(Variables de entorno)*.
4. Seleccioná el entorno **TechMind - Local** en el desplegable superior derecho.
5. Verificá la variable `base_url`:
   * `http://localhost:8000` (para pruebas directas sobre FastAPI).
   * `http://localhost:8080` (para pruebas de integración sobre Spring Boot).

---

## 📊 4. Resumen Ejecutivo de Resultados QA

**Proyecto:** TechMind — Organización Inteligente del Conocimiento Técnico  
**Responsable QA:** Federico G. Gutierrez  
**Fecha de Ejecución:** 04 de Agosto de 2026  

Durante los Sprints 1, 2, 3 y 4 se ejecutaron de manera exhaustiva las suites de pruebas funcionales, de integridad, seguridad, resiliencia y UX sobre el stack completo.

### Métricas Consolidadas:

| Planificados | Ejecutados | Pasó | Falló | % Éxito |
|:---:|:---:|:---:|:---:|:---:|
| **57** | **57** | **57** | **0** | **100%** |

---

## 📑 5. Desglose por Módulo y Tipo de Prueba

### 🐍 Microservicio FastAPI

| Categoría | Planificados | PASÓ | FALLÓ | % Éxito |
|---|:---:|:---:|:---:|:---:|
| Funcionales (Flujo Feliz) | 8 | 8 | 0 | 100% |
| Casos Borde / Encoding (UTF-8) | 3 | 3 | 0 | 100% |
| Validación de Esquema / Tipos | 3 | 3 | 0 | 100% |
| Seguridad (Inyección SQL / Content-Type) | 2 | 2 | 0 | 100% |
| Endpoints Complementarios | 3 | 3 | 0 | 100% |
| Integridad de Datos | 6 | 6 | 0 | 100% |
| **SUBTOTAL FASTAPI** | **25** | **25** | **0** | **100%** |

---

### 🐘 PostgreSQL — Base de Datos `techmind`

| Categoría | Planificados | PASÓ | FALLÓ | % Éxito |
|---|:---:|:---:|:---:|:---:|
| Completitud | 5 | 5 | 0 | 100% |
| Integridad y Estructura | 6 | 6 | 0 | 100% |
| Formato y Calidad de Texto | 3 | 3 | 0 | 100% |
| Edge Cases (Límites y Vacíos) | 2 | 2 | 0 | 100% |
| Rendimiento e Inserción Masiva | 1 | 1 | 0 | 100% |
| **SUBTOTAL POSTGRESQL** | **17** | **17** | **0** | **100%** |

---

### 🍃 Backend Spring Boot API

| Categoría | Planificados | PASÓ | FALLÓ | % Éxito |
|---|:---:|:---:|:---:|:---:|
| Clasificación y Persistencia Core | 1 | 1 | 0 | 100% |
| Codificación y Caracteres (UTF-8) | 1 | 1 | 0 | 100% |
| Validación de Campos y Esquema | 2 | 2 | 0 | 100% |
| Seguridad y Sanitización | 1 | 1 | 0 | 100% |
| Edge Cases (Textos de Gran Longitud) | 1 | 1 | 0 | 100% |
| **SUBTOTAL SPRING BOOT** | **6** | **6** | **0** | **100%** |

---

### 💻 Frontend (Vanilla JS / Tailwind)

| Categoría | Planificados | PASÓ | FALLÓ | % Éxito |
|---|:---:|:---:|:---:|:---:|
| Funcional / Pipeline & Modales | 2 | 2 | 0 | 100% |
| Validación de Controles e Interfaz | 1 | 1 | 0 | 100% |
| Persistencia y Reactividad de Estado (UI) | 1 | 1 | 0 | 100% |
| Seguridad y Sanitización Frontend (XSS) | 1 | 1 | 0 | 100% |
| UX / Control de Performance (Debounce) | 1 | 1 | 0 | 100% |
| Navegación & UI/UX (Light/Dark Mode) | 3 | 3 | 0 | 100% |
| **SUBTOTAL FRONTEND** | **9** | **9** | **0** | **100%** |

---

## 🔍 6. Detalle Completo de Casos de Prueba

### 🐍 Sprint 1: Microservicio FastAPI & NLP (25 Casos)

* **Pruebas Funcionales / Flujo Feliz:**
  * `CP-FASTAPI-01`: Valida clasificación de texto técnico y respuesta HTTP 200.
  * `CP-FASTAPI-02`: Extracción y retorno correcto de la lista de palabras clave relevantes.
  * `CP-FASTAPI-03`: Score de probabilidad de clasificación válido entre 0 y 1.
  * `CP-FASTAPI-09`: Estructura del contrato JSON devuelto con todas sus claves y tipos de datos.
  * `CP-FASTAPI-10`: Carga e inicialización correcta de modelos serializados (`.joblib`).
  * `CP-FASTAPI-11`: Medición de tiempo de respuesta asegurando inferencia en menos de 2000 ms.
  * `CP-FASTAPI-20`: Normalización y procesamiento de textos ingresados con tildes y mayúsculas sostenidas.
  * `CP-FASTAPI-22`: Evaluación de latencia y tasa de error 0% ante 100 peticiones concurrentes en ráfaga.

* **Casos Borde y Encoding (UTF-8):**
  * `CP-FASTAPI-12`: Comportamiento y gestión de memoria ante payloads extensos (+500k caracteres).
  * `CP-FASTAPI-13`: Sanitización y soporte UTF-8 procesando caracteres especiales, etiquetas y emojis.
  * `CP-FASTAPI-21`: Resiliencia de la API ante entradas no técnicas o sin sentido semántico.

* **Validación de Esquema y Tipos:**
  * `CP-FASTAPI-14`: Rechazo inmediato (HTTP 422) por parte de Pydantic ante tipos de datos no válidos.
  * `CP-FASTAPI-23`: Rechazo de payloads nulos devolviendo HTTP 422 Unprocessable Entity.
  * `CP-FASTAPI-24`: Detección de errores de sintaxis JSON y rechazo con HTTP 422.

* **Seguridad y Robustez:**
  * `CP-FASTAPI-15`: Inmunidad ante intentos de inyección SQL guardando comandos como texto plano.
  * `CP-FASTAPI-16`: Rechazo de solicitudes con formatos no soportados como XML (HTTP 422/415).

* **Endpoints Complementarios:**
  * `CP-FASTAPI-17`: Verificación de disponibilidad del microservicio mediante `GET /health`.
  * `CP-FASTAPI-18`: Consulta del catálogo completo con las 8 categorías en `GET /categorias`.
  * `CP-FASTAPI-25`: Consulta del historial de inferencias en `GET /predicciones`.

* **Integridad de Datos:**
  * `CP-FASTAPI-04`: Control de rechazo (HTTP 422) cuando el campo `titulo` se envía vacío.
  * `CP-FASTAPI-05`: Control de rechazo (HTTP 422) cuando el campo `texto` no contiene información.
  * `CP-FASTAPI-06`: Respuesta de error adecuada al enviar título y texto vacíos simultáneamente.
  * `CP-FASTAPI-07`: Intercepción y manejo de excepciones ante la recepción de JSON mal formado.
  * `CP-FASTAPI-08`: Rechazo con HTTP 405 Method Not Allowed al enviar `GET` al endpoint `POST /predecir`.
  * `CP-FASTAPI-19`: Rechazo por omisión de claves obligatorias dentro del cuerpo JSON.

---

### 🐘 Sprint 2: Data QA — PostgreSQL `techmind` (17 Casos)

* **Completitud:**
  * `CP-DB-01`: Verificación de ausencia de filas incompletas en la tabla `contenidos`.
  * `CP-DB-02`: Prevención de registros de texto idénticos sobrecargando la base de datos.
  * `CP-DB-03`: Validación de distribución sobre las 8 categorías temáticas del modelo.
  * `CP-DB-04`: Coincidencia del 100% entre la respuesta JSON de la API y el registro en `predicciones`.
  * `CP-DB-05`: Rango numérico de probabilidad strictly acotado en [0.0, 1.0].

* **Integridad y Estructura:**
  * `CP-DB-08`: Unicidad del 100% en la columna `id` de `predicciones` con secuencia autoincremental coherente.
  * `CP-DB-09`: Fechas de la columna `created_at` válidas, no nulas y alineadas a la zona horaria.
  * `CP-DB-10`: Confirmación de cadenas válidas sin nulos ni espacios aislados.
  * `CP-DB-11`: Categorías predichas pertenecientes de forma estricta al dominio semántico.
  * `CP-DB-13`: Integridad referencial y coincidencia en campos clave con la tabla de origen `contenidos`.
  * `CP-DB-14`: Verificación de restricciones PRIMARY KEY sobre la tabla `contenidos`.

* **Formato y Calidad de Texto:**
  * `CP-DB-06`: Valida el tipo de dato `text[]` para palabras clave e inferencias con arreglos vacíos `{}`.
  * `CP-DB-07`: Sanitización e inserción exitosa de texto con comandos destructivos (ej. `; DROP TABLE...`).
  * `CP-DB-15`: Evaluación cualitativa de textos cortos garantizando significancia técnica para NLP.

* **Límites y Rendimiento:**
  * `CP-DB-16`: Rechazo y ausencia de registros con longitud 0 o `TRIM` nulo.
  * `CP-DB-17`: Persistencia íntegra de payloads extensos en tipo `TEXT` sin truncamiento.
  * `CP-DB-12`: Resistencia y persistencia exitosa ante carga masiva de hasta 300 peticiones/minuto.

---

### 🍃 Sprint 3: Backend Spring Boot & ML (6 Casos)

* `CP-SPRINGBOOT-01` **(Clasificación y Persistencia Core):** Invocación del modelo ML, respuesta HTTP 201 y persistencia exitosa del contenido en PostgreSQL.
* `CP-SPRINGBOOT-02` **(Codificación UTF-8):** Preservación de codificación UTF-8, tildes y emojis en la respuesta JSON y en la base de datos.
* `CP-SPRINGBOOT-03` **(Validación de Campos):** Rechazo de peticiones sin el campo obligatorio `titulo`, devolviendo HTTP 400 Bad Request.
* `CP-SPRINGBOOT-04` **(Esquema @NotBlank):** Invalidación y rechazo de cadenas vacías o compuestas únicamente por espacios.
* `CP-SPRINGBOOT-05` **(Seguridad y ORM):** Sanitización contra inyecciones SQL mediante consultas parametrizadas con JPA/Hibernate.
* `CP-SPRINGBOOT-06` **(Edge Cases):** Procesamiento e inserción sin truncamiento de payloads de más de 50.000 caracteres dentro de los tiempos tolerados.

---

### 💻 Sprint 4: Frontend (Vanilla JS / Tailwind) (9 Casos)

* `CP-FRONTEND-01` **(Pipeline & Modales):** Ejecución de clasificación asíncrona y despliegue del resultado (categoría, probabilidad y palabras clave) en el panel derecho.
* `CP-FRONTEND-02` **(Validación de Interfaz):** Bloqueo de envío de formularios incompletos con avisos visuales en rojo evitando llamadas innecesarias a la API.
* `CP-FRONTEND-03` **(Modal JSON):** Despliegue del modal formateado con la sintaxis de respuesta JSON cruda devuelta por el servidor.
* `CP-FRONTEND-04` **(Reactividad UI):** Inserción inmediata de la nueva clasificación en el feed de recortes recientes sin recargar la página.
* `CP-FRONTEND-05` **(Seguridad XSS):** Inmunidad ante scripts, etiquetas HTML o inyecciones JS en los campos de entrada, escapándolos como texto plano en el DOM.
* `CP-FRONTEND-06` **(Control Debounce):** Deshabilitación del botón de envío tras el primer clic pasando a estado "Cargando...", evitando peticiones duplicadas.
* `CP-FRONTEND-07` **(Light/Dark Mode):** Alternancia fluida entre temas, manteniendo contraste, accesibilidad y persistencia del tema tras recargar (`localStorage`).
* `CP-FRONTEND-08` **(Navegación Sidebar en Dark Mode):** Correcta redirección e interacción con los elementos de navegación en modo oscuro.
* `CP-FRONTEND-09` **(Navegación Sidebar en Light Mode):** Correcta redirección e interacción con los elementos de navegación en modo claro.

---

## 🔍 7. Assertions Automatizadas en Postman

Cada petición dentro de la colección automatizada de Postman contiene scripts en JavaScript (pestaña **Tests**) para validar contratos, códigos HTTP y latencia:

```javascript
// 1. Validación de código de respuesta HTTP 200 / 201
pm.test("Código de Estado es 200 OK o 201 Created", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 201]);
});

// 2. Validación de Latencia SLA (< 2000 ms)
pm.test("Tiempo de respuesta menor a 2000 ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

// 3. Validación de Contrato JSON
pm.test("Respuesta contiene el esquema esperado", function () {
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property("categoria");
    pm.expect(responseJson).to.have.property("probabilidad");
    pm.expect(responseJson).to.have.property("informaciones_adicionales");
});

// 4. Validación de Rango Numérico (Probabilidad)
pm.test("La probabilidad es un número válido entre 0 y 1", function () {
    const responseJson = pm.response.json();
    pm.expect(responseJson.probabilidad).to.be.a('number');
    pm.expect(responseJson.probabilidad).to.be.within(0, 1);
});
```

---

## 📂 8. Registro y Reporte de Evidencias

Todas las evidencias generadas durante las corridas de QA están ordenadas en el repositorio bajo la siguiente estructura:

```
├── casos-de-prueba/            
├── evidencias/             
│   ├── Capturas de Pantalla/
│   └── JSON/
├── reportes/                          
│   ├── informes/                  
│   ├── Reporte de BUGS/
│   ├── resultados-sprint-1.md
│   ├── resultados-sprint-2.md
│   ├── resultados-sprint-3.md
│   └── resultados-sprint-4.md
```

---

_QA Guía de pruebas e informe de ejecución — TechMind Project v4.0 — Hackathon G9 LATAM (Equipo 37)_