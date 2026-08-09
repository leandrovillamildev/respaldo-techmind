# Arquitectura de TechMind

## Visión General

TechMind implementa una arquitectura de **dos microservicios** desacoplados:

1. **API Backend** (este repositorio) — Spring Boot, manejo de peticiones y persistencia
2. **Microservicio ML** (externo) — FastAPI Python, clasificación de contenidos

```
┌──────────────────────────────────────────────────────────────┐
│                      Cliente HTTP                            │
│                  (curl, Postman, frontend)                   │
└────────────────────────┬─────────────────────────────────────┘
                         │ POST /contenido
                         ▼
┌──────────────────────────────────────────────────────────────┐
│              Spring Boot API   :8080                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  ContenidoController  (@RestController)              │    │
│  └──────────────────────┬──────────────────────────────┘    │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────┐    │
│  │  PrediccionService  (@Service)                       │    │
│  │   1. Guarda Contenido                                │    │
│  │   2. Llama FastAPI /predecir (HttpClient Java)       │    │
│  │   3. Guarda Prediccion                               │    │
│  └───────┬──────────────────────────────┬──────────────┘    │
│           │                              │                   │
│  ┌────────▼──────────┐      ┌────────────▼────────────┐     │
│  │ ContenidoRepo     │      │ PrediccionRepo           │     │
│  │ (Spring Data JPA) │      │ (Spring Data JPA)        │     │
│  └────────┬──────────┘      └────────────┬────────────┘     │
└───────────┼──────────────────────────────┼───────────────────┘
            │                              │
            ▼                              ▼
┌──────────────────────────────────────────────────────────────┐
│                  PostgreSQL  :5432                           │
│   tablas: contenidos, predicciones                           │
└──────────────────────────────────────────────────────────────┘

            ───────────────────────────────────
            ↑ llamada HTTP POST /predecir
┌──────────────────────────────────────────────────────────────┐
│              FastAPI (Data Science)  :8000                   │
│   Modelo ML de clasificación de texto                        │
└──────────────────────────────────────────────────────────────┘
```

---

## Capas de la Aplicación Spring Boot

### Controller Layer
**Archivo:** [`ContenidoController.java`](../api/api/src/main/java/api/controller/ContenidoController.java)

- Único punto de entrada HTTP de la aplicación
- Recibe y valida el `ContenidoRequest` con `@Valid`
- Delega toda la lógica al `PrediccionService`
- Retorna `ResponseEntity<PrediccionResponse>` con HTTP 201

### Service Layer
**Archivo:** [`PrediccionService.java`](../api/api/src/main/java/api/service/PrediccionService.java)

- Orquesta el flujo completo de clasificación
- Gestiona la transacción de base de datos (`@Transactional`)
- Realiza la llamada HTTP al microservicio FastAPI usando `java.net.http.HttpClient` nativo (Java 11+)
- Parsea la respuesta JSON de FastAPI mediante expresiones regulares

### Repository Layer
**Archivos:** [`ContenidoRepository.java`](../api/api/src/main/java/api/repository/ContenidoRepository.java) · [`PrediccionRepository.java`](../api/api/src/main/java/api/repository/PrediccionRepository.java)

- Interfaces Spring Data JPA que extienden `JpaRepository`
- Proveen operaciones CRUD sin código adicional

### Model Layer
**Archivos:** [`Contenido.java`](../api/api/src/main/java/api/model/Contenido.java) · [`Prediccion.java`](../api/api/src/main/java/api/model/Prediccion.java)

- Entidades JPA mapeadas a tablas PostgreSQL
- `Contenido`: almacena titulo + texto + timestamp
- `Prediccion`: almacena la clasificación vinculada a un `Contenido` (relación ManyToOne)

### DTO Layer
**Archivos:** [`ContenidoRequest.java`](../api/api/src/main/java/api/dto/ContenidoRequest.java) · [`PrediccionResponse.java`](../api/api/src/main/java/api/dto/PrediccionResponse.java)

- Records Java inmutables
- Separan el contrato de la API de las entidades de base de datos

### Exception Handling
**Archivo:** [`GlobalExceptionHandler.java`](../api/api/src/main/java/api/controller/GlobalExceptionHandler.java)

- `@RestControllerAdvice` que centraliza el manejo de errores
- Convierte `MethodArgumentNotValidException` → 400 Bad Request
- Convierte `DsServiceUnavailableException` → 503 Service Unavailable

---

## Decisiones Técnicas

### ¿Por qué `java.net.http.HttpClient` en lugar de `RestTemplate`?

El `PrediccionService` usa el cliente HTTP nativo de Java 11+ para las llamadas a FastAPI. Aunque `RestTemplateConfig` declara un bean `RestTemplate`, el servicio no lo inyecta — esto es una inconsistencia del código actual. El `HttpClient` nativo es la implementación real activa.

### ¿Por qué Flyway para migraciones?

Flyway garantiza que el esquema de base de datos esté versionado y sea reproducible. Hibernate está configurado en modo `validate` (no modifica el esquema), por lo que Flyway es el único responsable de crear/alterar tablas.

### ¿Por qué palabras clave como string separado por coma?

La tabla `predicciones` guarda las keywords como `TEXT` con valores separados por coma (ej: `"AI,machine learning,Python"`). El modelo `Prediccion` expone el método `getPalabrasClaveList()` para convertirlas a `List<String>` en memoria. Esta elección simplifica el esquema pero limita las consultas por keyword individual.

### Parsing JSON con Regex

El `PrediccionService` parsea la respuesta de FastAPI con regex en lugar de usar Jackson u otra librería JSON. Esto funciona para respuestas bien formadas pero es frágil ante respuestas con whitespace inusual, caracteres especiales o campos anidados. Es un área de mejora identificada.

---

## Configuración

### `application.properties`

```properties
# Datasource
spring.datasource.url=jdbc:postgresql://localhost:5432/techmind
spring.datasource.username=techmind_user
spring.datasource.password=techmind_pass

# Hibernate — solo valida, Flyway gestiona el esquema
spring.jpa.hibernate.ddl-auto=validate

# Flyway
spring.flyway.enabled=true
spring.flyway.baseline-on-migrate=true

# URL del microservicio FastAPI
techmind.ds.api.url=http://localhost:8000

# Spring Boot Actuator — solo expone /actuator/health
management.endpoints.web.exposure.include=health
management.endpoint.health.show-details=never
management.endpoints.web.cors.allowed-origins=*
management.endpoints.web.cors.allowed-methods=GET
```

### `docker-compose.yml`

Levanta un contenedor PostgreSQL 16 Alpine con:
- Base de datos: `techmind`
- Usuario: `techmind_user` / Contraseña: `techmind_pass`
- Puerto: `5432`
- Volumen persistente: `techmind_postgres_data`
- Health check: `pg_isready` cada 5 segundos

---

## Flujo de Arranque de la Aplicación

```
1. Spring Boot inicia
2. Se conecta a PostgreSQL :5432
3. Flyway ejecuta migraciones pendientes (V1__create_tables.sql)
4. Hibernate valida que el esquema coincida con las entidades JPA
5. Se registran los beans (Controller, Service, Repositories, Config, Actuator)
6. La aplicación está lista en :8080
   - POST /contenido         → clasificación de contenido
   - GET  /actuator/health   → health check del servicio
```

---

## Endpoint de Health Check

**URL:** `GET http://localhost:8080/actuator/health`

Proveído por `spring-boot-starter-actuator`. El frontend lo consulta al cargar la página para mostrar el estado del servicio en tiempo real.

**Respuesta cuando el servicio está operativo (HTTP 200):**
```json
{ "status": "UP" }
```

> **Nota:** Configurado con `show-details=never` para no exponer información interna del servidor. Solo se expone el endpoint `health` (no métricas, no info, no env).
