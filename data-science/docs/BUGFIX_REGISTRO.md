# 📋 TechMind — Registro Técnico de Bugs Corregidos

> Registro detallado (causa, síntoma, solución y código) de todos los bugs identificados y corregidos durante la integración.
> Para el historial de versiones del proyecto, ver el [`CHANGELOG.md`](../../../CHANGELOG.md) en la raíz del repositorio.
> Última actualización: 2026-07-30

---

## [v1.0.0] — 2026-07-27 — Sprint de Integración

### Resumen

En la sesión de integración del 2026-07-27 se realizó un análisis cruzado del código de ambos equipos (FastAPI + Spring Boot) y se identificaron y corrigieron **5 bugs** que habrían causado fallos en la demo.

---

## 🔴 Bugs Críticos Corregidos

### BUG-1 — Conflicto de `docker-compose.yml` duplicados

| Campo | Valor |
|---|---|
| **Severidad** | 🔴 Crítica |
| **Archivo afectado** | `backend/docker-compose.yml` |
| **Estado** | ✅ Resuelto |
| **Fecha** | 2026-07-27 |

**Descripción:** Existían dos archivos `docker-compose.yml` idénticos en la raíz del proyecto y en `backend/`. Ambos declaraban el contenedor `techmind-postgres` en el puerto `5432` con el mismo volumen `techmind_postgres_data`. Si algún miembro del equipo ejecutaba el `docker-compose up` desde `backend/`, generaba un conflicto de puertos o corrupción de datos con el PostgreSQL ya levantado por el equipo de DS.

**Síntoma:** `Error: port is already allocated` o datos inconsistentes entre equipos.

**Solución aplicada:** El `backend/docker-compose.yml` fue marcado como **DEPRECADO** con un comentario claro al inicio del archivo indicando que se debe usar el `docker-compose.yml` de la raíz del proyecto. El archivo se conserva como referencia pero no debe ejecutarse directamente.

**Archivo de referencia:** `docker-compose.yml` en la raíz del proyecto (única fuente de verdad).

---

### BUG-2 — Credenciales hardcodeadas en `application.properties`

| Campo | Valor |
|---|---|
| **Severidad** | 🔴 Crítica |
| **Archivo afectado** | `backend/api/api/src/main/resources/application.properties` |
| **Estado** | ✅ Resuelto |
| **Fecha** | 2026-07-27 |

**Descripción:** El archivo `application.properties` tenía los valores de conexión a PostgreSQL y la URL de FastAPI escritos directamente en el código (`localhost:5432`, `techmind_user`, etc.), sin leer variables de entorno. El equipo de Backend tenía un archivo `.env` definido pero Spring Boot no lo procesaba.

**Síntoma:** Al cambiar de entorno (local → Docker → OCI) era necesario modificar el código fuente, lo que es una mala práctica y fuente de errores en producción.

**Solución aplicada:** Se parametrizaron todas las propiedades usando la sintaxis `${VARIABLE:valor_por_defecto}` de Spring:

```properties
# Antes
spring.datasource.url=jdbc:postgresql://localhost:5432/techmind
spring.datasource.username=techmind_user

# Después
spring.datasource.url=jdbc:postgresql://${PG_HOST:localhost}:${PG_PORT:5432}/${PG_DB:techmind}
spring.datasource.username=${PG_USER:techmind_user}
```

Los valores por defecto siguen funcionando para desarrollo local sin cambios de configuración.

---

### BUG-3 — Regex frágil en el parser JSON de `PrediccionService`

| Campo | Valor |
|---|---|
| **Severidad** | 🔴 Crítica |
| **Archivo afectado** | `backend/api/api/src/main/java/api/service/PrediccionService.java` |
| **Estado** | ✅ Resuelto |
| **Fecha** | 2026-07-27 |

**Descripción:** El método `parseResponse()` en `PrediccionService` usaba regex para parsear la respuesta JSON de FastAPI. Se identificaron dos bugs:

1. La regex `[0-9.]+` para `probabilidad` fallaba con el valor `0` (entero sin decimal) y con notación científica (`1.0e-2`). Retornaba `null` y el posterior `Double.valueOf(null)` causaba `NullPointerException`.
2. No había validación de null: si `categoria` o `probabilidad` no se encontraban en el JSON, el sistema lanzaba un `NullPointerException` genérico con HTTP 500, sin información útil para el debugging.

**Síntoma:** HTTP 500 opaco cuando FastAPI devolvía una respuesta con probabilidad `0.0` o con formato inesperado.

**Solución aplicada:**
- Se corrigió la regex de `extractDouble` para aceptar enteros, decimales y notación científica: `[0-9]*\.?[0-9]+(?:[eE][+-]?[0-9]+)?`
- Se agregaron null-checks en `parseResponse()` que lanzan `DsServiceUnavailableException` (→ HTTP 503) con un mensaje descriptivo que incluye el JSON recibido.

---

### BUG-4 — `@Transactional` envolvía la llamada HTTP a FastAPI

| Campo | Valor |
|---|---|
| **Severidad** | 🔴 Crítica |
| **Archivo afectado** | `backend/api/api/src/main/java/api/service/PrediccionService.java` |
| **Estado** | ✅ Resuelto |
| **Fecha** | 2026-07-27 |

**Descripción:** El método `clasificar()` estaba anotado con `@Transactional`, lo que mantenía la conexión a PostgreSQL abierta durante toda la llamada HTTP a FastAPI (hasta 10 segundos). Con múltiples requests simultáneos, el pool de conexiones se agotaba y los nuevos requests colgaban indefinidamente.

**Síntoma:** La aplicación se colgaba bajo carga concurrente. En una demo con el jurado probando el sistema simultáneamente, esto habría causado un timeout catastrófico.

**Solución aplicada:** Se separó el método en tres partes con responsabilidades acotadas:

1. `guardarContenido()` — `@Transactional`, dura milisegundos
2. `llamarFastApi()` — sin transacción, puede tardar hasta 10 s
3. `guardarPrediccion()` — `@Transactional`, dura milisegundos

El método público `clasificar()` orquesta las tres sin estar él mismo anotado con `@Transactional`.

---

### BUG-5 — Schemas incompatibles de la tabla `predicciones` entre FastAPI y Spring Boot

| Campo | Valor |
|---|---|
| **Severidad** | 🟠 Alta |
| **Archivos afectados** | `app/database.py` |
| **Estado** | ✅ Resuelto |
| **Fecha** | 2026-07-27 |

**Descripción:** Ambos servicios intentaban crear y escribir en la tabla `predicciones` de la misma base de datos PostgreSQL, pero con schemas incompatibles:

| Campo | Schema FastAPI (incorrecto) | Schema Spring Boot/Flyway (correcto) |
|---|---|---|
| Keywords | `informaciones_adicionales TEXT[]` | `palabras_clave TEXT` (comma-separated) |
| FK | Sin foreign key | `contenido_id BIGINT REFERENCES contenidos(id)` |
| Timestamps | `TIMESTAMPTZ` | `TIMESTAMP` |

Si FastAPI arrancaba primero, creaba la tabla con su propio schema. Cuando Spring Boot iniciaba, Flyway detectaba que el schema no coincidía con `V1__create_tables.sql` y podía fallar con error de validación, o peor: creaba una segunda tabla parcial causando inconsistencias silenciosas.

**Síntoma:** Error de Hibernate durante el arranque de Spring Boot: `Schema-validation: missing column`, o inserciones fallidas en tiempo de ejecución.

**Solución aplicada:** Se modificó `app/database.py` para que `init_db()` ya **no cree ni gestione la tabla `predicciones`**. Esa responsabilidad es exclusiva de Flyway (Spring Boot). FastAPI ahora solo verifica la conexión al arrancar con un `SELECT 1`. La tabla `predicciones` es creada por Flyway con el schema correcto antes de que FastAPI intente escribir en ella.

---

| ID | Descripción | Resuelto en |
|----|-------------|-------------|
| FIX-005 | Faltaba `requirements.txt` — equipo de Backend no podía reproducir el entorno | v0.5.0 |
| FIX-007 | CSV como fuente de verdad obsoleta — PostgreSQL reemplazó al CSV | v0.5.0 |
| FIX-008 | `NameError` en `log_prediccion()` por variable `probabilidad` no calculada | v0.6.0 |
| FIX-009 | Rutas incorrectas de `.joblib` en el notebook (guardaban en `notebooks/` en lugar de `models/`) | v0.6.0 |
| FIX-010 | Columna `keywords` vs `informaciones_adicionales` — renombrada vía `ALTER TABLE` | v0.6.0 |

---

## 🔴 BUG-6 — Volumen Docker con schema anterior (detectado en testing)

| Campo | Valor |
|---|---|
| **Severidad** | 🔴 Crítica |
| **Archivos afectados** | `data-science/src/migrate_to_postgres.py` · `app/database.py` |
| **Estado** | ✅ Resuelto |
| **Fecha** | 2026-07-27 |

**Descripción:** Durante el testing de integración se detectó que la tabla `predicciones` se creaba con el schema incorrecto de FastAPI en **dos lugares adicionales** además de `app/database.py` (ya corregido en BUG-5):

1. **`data-science/src/migrate_to_postgres.py`** — El script de migración creaba `predicciones` con columnas `titulo`, `texto`, `informaciones_adicionales TEXT[]` en lugar del schema de Flyway (`contenido_id BIGINT REFERENCES`, `palabras_clave TEXT`).
2. El volumen Docker `techmind_postgres_data` **sobrevivía entre sesiones** con el schema incorrecto, haciendo que Flyway fallara al intentar validar el schema con `V1__create_tables.sql`.

**Síntoma:** Al ejecutar `migrate_to_postgres.py` con un volumen ya existente, la tabla `predicciones` quedaba con el schema de FastAPI. Cuando el equipo de Backend levantaba Spring Boot, Hibernate encontraba un schema incompatible y lanzaba `Schema-validation: missing column [contenido_id]`.

**Solución aplicada:**

1. Se corrigió `migrate_to_postgres.py` para que **solo cree la tabla `contenidos`** (dataset de entrenamiento). Eliminadas las líneas 50-58 que creaban `predicciones`.

2. Se realizó un reset completo del volumen Docker:
```bash
docker-compose down -v   # elimina el volumen con schema incorrecto
docker-compose up -d     # recrea el volumen limpio
python3 data-science/src/migrate_to_postgres.py  # restaura solo contenidos
```

**Estado final de la DB después del fix:**
- ✅ Solo existe la tabla `contenidos` (61 registros de entrenamiento)
- ✅ La tabla `predicciones` **no existe** — será creada por Flyway al arrancar Spring Boot con el schema correcto
- ✅ `log_prediccion()` en FastAPI falla silenciosamente (warning controlado) hasta que Spring Boot cree la tabla — comportamiento esperado y correcto

---

## 🔴 BUG-7 — Mismatch en tipo de columna `id` (`SERIAL` vs `BIGSERIAL`) y orden de arranque

| Campo | Valor |
|---|---|
| **Severidad** | 🔴 Crítica |
| **Archivos afectados** | `data-science/src/migrate_to_postgres.py` |
| **Estado** | ✅ Resuelto |
| **Fecha** | 2026-07-27 |

**Descripción:** Durante la prueba end-to-end con Spring Boot, Hibernate rechazó el schema de la tabla `contenidos` creada por `migrate_to_postgres.py`. El script creaba `id` como `SERIAL` (`INTEGER` - 4 bytes) y agregaba la columna `categoria`, mientras que el modelo JPA `Contenido.java` de Spring Boot mapea `id` como `Long` (`BIGINT` - 8 bytes) y no mapea la columna `categoria` en esa tabla.

**Síntoma:** Error de validación de JPA al arrancar Spring Boot: `Schema validation: wrong column type encountered in column [id] in table [contenidos]; found [serial (Types#INTEGER)], but expecting [bigint (Types#BIGINT)]`.

**Solución aplicada:**
1. Se removió la creación estática de la estructura de `contenidos` de `migrate_to_postgres.py`.
2. Se programó el script para verificar que la tabla ya exista (creada por Flyway con `BIGSERIAL`) antes de insertar los registros.
3. Se ajustó la consulta de inserción y de reporte para omitir la columna `categoria` en `contenidos`.
4. Se documentó y aplicó el **orden estricto de arranque**:
   ```bash
   1. docker-compose up -d                             # 1. Base de datos
   2. cd backend/api/api && ./mvnw spring-boot:run     # 2. Flyway crea tablas (BIGSERIAL)
   3. python3 data-science/src/migrate_to_postgres.py # 3. Carga 61 registros de entrenamiento
   4. uvicorn app.main:app --port 8000                 # 4. Inicia servicio de ML
   ```

---

---

## 🔴 BUG-8 — Bloqueo de solicitudes CORS en Spring Boot y FastAPI desde el Frontend

| Campo | Valor |
|---|---|
| **Severidad** | 🟠 Alta |
| **Archivos afectados** | `backend/.../ContenidoController.java` · `app/main.py` |
| **Estado** | ✅ Resuelto |
| **Fecha** | 2026-07-27 |

**Descripción:** Al intentar consumir la API REST desde el frontend web (`http://localhost:5173`), el navegador bloqueaba las peticiones por falta de cabeceras CORS (`Access-Control-Allow-Origin`).

**Síntoma:** Error en consola del navegador `CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource`. El indicador de estado de FastAPI en el header mostraba `Desconectado`.

**Solución aplicada:**
1. Agregada la anotación `@CrossOrigin(origins = "*")` en `ContenidoController.java` de Spring Boot.
2. Agregado `CORSMiddleware` en `app/main.py` de FastAPI.

---

## 🔴 BUG-9 — Error de parseo de fechas ISO con microsegundos en el Historial del Frontend

| Campo | Valor |
|---|---|
| **Severidad** | 🟡 Media |
| **Archivos afectados** | `frontend/app.js` · `app/database.py` |
| **Estado** | ✅ Resuelto |
| **Fecha** | 2026-07-27 |

**Descripción:** Al hacer click en el botón de **Historial** en la interfaz web, el script intentaba convertir la fecha ISO enviada por PostgreSQL (`2026-07-27T20:24:02.448830`) directamente con `new Date()`. En motores JS estrictos, los 6 dígitos de microsegundos producían `Invalid Date`, haciendo que la renderización del grid fallara.

**Síntoma:** Al hacer click en "Historial", las tarjetas no se actualizaban ni mostraban la lista de predicciones.

**Solución aplicada:**
1. Creada la función sanitizadora `formatTimeString()` en `frontend/app.js` para limpiar cadenas microsegundos antes de parsear.
2. Agregadas validaciones nulas en `entry.probabilidad` y `entry.categoria`.
3. Creado el modal completo `#history-modal` para visualizar todas las predicciones registradas en la base de datos PostgreSQL.

## 🔴 BUG-10 — Mismatch de nombres de variables de entorno de Spring Boot en `docker-compose.yml`

| Campo | Valor |
|---|---|
| **Severidad** | 🔴 Crítica |
| **Archivos afectados** | `docker-compose.yml` |
| **Estado** | ✅ Resuelto |
| **Fecha** | 2026-07-28 |

**Descripción:** En `docker-compose.yml`, el servicio `springboot` tenía variables como `SPRING_DATASOURCE_URL` y `FASTAPI_URL`. Sin embargo, `application.properties` en Java lee explícitamente `PG_HOST`, `PG_PORT`, `PG_DB`, `PG_USER`, `PG_PASSWORD` y `TECHMIND_DS_API_URL`. Al no coincidir las claves, Spring Boot asumía `PG_HOST=localhost` por defecto e intentaba conectarse a una BD dentro de su propio contenedor en lugar del contenedor `postgres`.

**Síntoma:** Error de conexión a la base de datos e inicio fallido del backend Spring Boot al ejecutar `python setup.py --docker`.

**Solución aplicada:** Se corrigieron los nombres de variables de entorno en `docker-compose.yml` bajo el servicio `springboot`:
```yaml
environment:
  - PG_HOST=postgres
  - PG_PORT=5432
  - PG_DB=techmind
  - PG_USER=techmind_user
  - PG_PASSWORD=techmind_pass
  - TECHMIND_DS_API_URL=http://fastapi:8000
```

---

## 🔴 BUG-11 — Regla de `.gitignore` bloqueando los modelos serializados `.joblib`

| Campo | Valor |
|---|---|
| **Severidad** | 🔴 Crítica |
| **Archivos afectados** | `.gitignore` |
| **Estado** | ✅ Resuelto |
| **Fecha** | 2026-07-28 |

**Descripción:** En `.gitignore`, una regla global excluyó la carpeta `data-science/models/` impidiendo que los archivos `.joblib` (modelo clasificador y vectorizador TF-IDF) fueran rastreados e incluyeran en el repositorio al clonar en nuevas máquinas.

**Síntoma:** FastAPI fallaba al iniciar en Docker con `Missing ML model files: tfidf_vectorizer.joblib`.

**Solución aplicada:** Se ajustó `.gitignore` agregando excepciones explícitas para rastrear el directorio y los binarios de Machine Learning:
```gitignore
data-science/models/
!data-science/models/
!data-science/models/*.joblib
```

---

## 🔴 BUG-12 — Ausencia de auto-generación de modelos y schema drift en volúmenes Docker

| Campo | Valor |
|---|---|
| **Severidad** | 🟠 Alta |
| **Archivos afectados** | `setup.py` · `data-science/src/generate_models.py` |
| **Estado** | ✅ Resuelto |
| **Fecha** | 2026-07-28 |

**Descripción:** Si un usuario ejecutaba `python setup.py --docker` en un repositorio recién clonado sin los archivos `.joblib` o con un volumen Docker legacy de PostgreSQL que contenía el schema anterior (`serial` en lugar de `BIGSERIAL`), la compilación abortaba.

**Solución aplicada:**
1. Creado `data-science/src/generate_models.py` para entrenar y exportar los modelos `.joblib` de forma offline en 2 segundos.
2. Actualizado `setup.py` (`run_full_docker`) para detectar si faltan los `.joblib` y generarlos automáticamente sobre la marcha.
3. Agregado detector y prompt de limpieza de volumen en `setup.py` (`docker-compose --profile full down -v`) para forzar la recreación limpia del schema por Flyway.

---

### BUG-13 — Intento de inserción directa a PostgreSQL desde FastAPI sin `contenido_id`

| Campo | Valor |
|---|---|
| **Severidad** | 🟠 Alta |
| **Archivos afectados** | `app/main.py` · `app/database.py` |
| **Estado** | ✅ Resuelto |
| **Fecha** | 2026-07-28 |

**Descripción:** Al realizar inferencias en `POST /predecir`, FastAPI ejecutaba la función `log_prediccion()` que intentaba hacer `INSERT INTO predicciones (categoria, probabilidad, palabras_clave, created_at)` sin especificar `contenido_id`. Como la tabla `predicciones` creada por Flyway requiere `contenido_id BIGINT NOT NULL REFERENCES contenidos(id)`, PostgreSQL arrojaba un error de restricción `null value in column "contenido_id" violates not-null constraint` en cada petición.

**Solución aplicada:** Se eliminó la llamada a `log_prediccion()` en `app/main.py` y se removió la función obsoleta en `app/database.py`. FastAPI pasó a ser un microservicio predictivo 100% sin estado (stateless), dejando la responsabilidad de persistencia relacional exclusivamente a Spring Boot (que asigna el `contenido_id` al guardar la entidad `Contenido`).

---

### BUG-14 — Incompatibilidad de imagen Docker `eclipse-temurin:17-jdk-alpine` en macOS Apple Silicon (ARM64)

| Campo | Valor |
|---|---|
| **Severidad** | 🔴 Crítica (en macOS M1/M2/M3/M4) |
| **Archivo afectado** | `backend/Dockerfile` |
| **Estado** | ✅ Resuelto |
| **Fecha** | 2026-07-29 |

**Descripción:** Al ejecutar `python3 setup.py --docker` en sistemas macOS con procesador Apple Silicon (ARM64), la compilación del contenedor de Spring Boot fallaba con el error: `no match for platform in manifest: not found` para la imagen base `eclipse-temurin:17-jdk-alpine`. La variante Alpine oficial de Eclipse Temurin en Docker Hub no publicaba manifiestos para la plataforma `linux/arm64`.

**Síntoma:** `target springboot: failed to solve: eclipse-temurin:17-jdk-alpine: failed to resolve source metadata for docker.io/library/eclipse-temurin:17-jdk-alpine: no match for platform in manifest: not found`.

**Solución aplicada:** Se actualizaron las imágenes base en `backend/Dockerfile` a las etiquetas estándar multi-arquitectura:
- Etapa de build: `eclipse-temurin:17-jdk`
- Etapa de ejecución: `eclipse-temurin:17-jre`

Estas etiquetas oficiales cuentan con soporte nativo tanto para `linux/amd64` (Windows/Linux x86_64) como para `linux/arm64` (macOS Apple Silicon y servidores ARM64 en OCI).

---

## 📊 Resumen de Impacto

| Bug | Riesgo en demo | Componente |
|-----|---------------|-----------|
| BUG-1 (docker-compose) | Conflicto de puertos al levantar el entorno | Infraestructura |
| BUG-2 (hardcoded config) | Fallo al desplegar en OCI | Spring Boot |
| BUG-3 (regex + nulls) | HTTP 500 con probabilidad = 0.0 | Spring Boot |
| BUG-4 (@Transactional) | Cuelgue bajo carga concurrente | Spring Boot |
| BUG-5 (schema conflict init_db) | Fallo al arrancar Spring Boot | FastAPI · database.py |
| BUG-6 (schema conflict migrate) | Fallo al arrancar Spring Boot | FastAPI · migrate_to_postgres.py |
| BUG-7 (columna INTEGER vs BIGINT) | Fallo al validar schema JPA | FastAPI · migrate_to_postgres.py |
| BUG-8 (bloqueo CORS) | Interfaz web no puede llamar a las APIs | Spring Boot · FastAPI |
| BUG-9 (date parse historial) | Botón de historial no renderiza resultados | Frontend · app.js |
| BUG-10 (springboot env vars) | Fallo de conexión BD en modo Docker | Docker Compose · Spring Boot |
| BUG-11 (gitignore .joblib) | FastAPI caía por modelos faltantes | Git · FastAPI |
| BUG-12 (auto-healing setup.py) | Aborto en instalaciones frescas | setup.py · Data Science |
| BUG-13 (FastAPI null contenido_id) | Error de log en PostgreSQL por inserción redundante | FastAPI · app/main.py |
| BUG-14 (Docker manifest ARM64) | Fallo al compilar contenedor Spring Boot en macOS | backend/Dockerfile |

---

*TechMind G9 LATAM Team 37 — Registro técnico actualizado el 2026-07-30*


