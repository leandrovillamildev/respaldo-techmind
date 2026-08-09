# Funcionalidades de TechMind

## Descripción General

TechMind expone una única API REST que recibe contenidos textuales, los clasifica mediante un modelo de Machine Learning (servicio FastAPI externo) y persiste tanto el contenido como la predicción en PostgreSQL.

---

## Endpoints Disponibles

### `POST /contenido` — Clasificar Contenido

Recibe un título y un texto, ejecuta la clasificación ML y retorna el resultado.

**URL:** `http://localhost:8080/contenido`  
**Método:** `POST`  
**Content-Type:** `application/json`

#### Request Body

```json
{
  "titulo": "string (obligatorio, no vacío)",
  "texto":  "string (obligatorio, no vacío)"
}
```

| Campo | Tipo | Validación |
|-------|------|-----------|
| `titulo` | `string` | Requerido, no puede ser blank |
| `texto` | `string` | Requerido, no puede ser blank |

#### Response — `201 Created`

```json
{
  "categoria": "string",
  "probabilidad": 0.94,
  "informaciones_adicionales": ["keyword1", "keyword2", "keyword3"]
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `categoria` | `string` | Categoría predicha por el modelo (ej: `"tecnología"`) |
| `probabilidad` | `float` | Confianza del modelo entre 0.0 y 1.0 |
| `informaciones_adicionales` | `string[]` | Palabras clave relevantes del contenido |

#### Ejemplo completo

```bash
curl -X POST http://localhost:8080/contenido \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "OpenAI lanza GPT-5 con capacidades multimodales",
    "texto": "La empresa de inteligencia artificial presentó su nuevo modelo..."
  }'
```

```json
{
  "categoria": "tecnología",
  "probabilidad": 0.97,
  "informaciones_adicionales": ["OpenAI", "GPT-5", "inteligencia artificial", "multimodal"]
}
```

---

## Flujo de Procesamiento

```
1. Cliente envía POST /contenido
        │
        ▼
2. Validación de campos (titulo y texto @NotBlank)
        │
        ▼
3. Persistencia del contenido en tabla `contenidos`
        │
        ▼
4. Llamada HTTP POST al microservicio FastAPI → /predecir
        │
        ▼
5. Parseo de la respuesta del modelo ML
        │
        ▼
6. Persistencia de la predicción en tabla `predicciones`
        │
        ▼
7. Retorno del resultado al cliente (HTTP 201)
```

---

## Manejo de Errores

### `400 Bad Request` — Validación fallida

Cuando `titulo` o `texto` están vacíos o ausentes.

```json
{
  "titulo": "El título es obligatorio",
  "texto": "El texto es obligatorio"
}
```

### `503 Service Unavailable` — Microservicio ML no disponible

Cuando FastAPI no responde en el tiempo límite o retorna un error.

```json
{
  "error": "No se pudo contactar al servicio de clasificación (FastAPI): Connection refused"
}
```

```json
{
  "error": "El servicio de clasificación respondió con error 500: Internal Server Error"
}
```

---

## Esquema de Base de Datos

### Tabla `contenidos`

Almacena cada contenido textual recibido.

```sql
CREATE TABLE contenidos (
    id         BIGSERIAL PRIMARY KEY,
    titulo     VARCHAR(255) NOT NULL,
    texto      TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);
```

### Tabla `predicciones`

Almacena el resultado ML asociado a cada contenido.

```sql
CREATE TABLE predicciones (
    id             BIGSERIAL PRIMARY KEY,
    contenido_id   BIGINT NOT NULL REFERENCES contenidos(id) ON DELETE CASCADE,
    categoria      VARCHAR(100) NOT NULL,
    probabilidad   DOUBLE PRECISION NOT NULL,
    palabras_clave TEXT NOT NULL,   -- keywords separadas por coma
    created_at     TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_predicciones_contenido_id ON predicciones(contenido_id);
```

> **Nota:** Las palabras clave se almacenan como string separado por comas (`"AI,machine learning,Python"`) y se exponen como lista en la respuesta JSON.

---

## Restricciones y Comportamiento Actual

- **Sin autenticación ni autorización**: Cualquier cliente puede usar el endpoint.
- **Sin endpoints GET de clasificación**: No existe consulta histórica de predicciones por la API de Spring Boot (el historial se consulta directamente a FastAPI vía `/predicciones`).
- **Solo clasificación sincrónica**: El cliente espera hasta recibir la respuesta del modelo ML.
- **Timeouts fijos**: 5s de conexión y 10s de lectura hacia FastAPI. Si el modelo tarda más, la petición falla.

---

## Endpoint de Monitoreo

### `GET /actuator/health` — Health Check

Proveído por `spring-boot-starter-actuator`. Permite verificar que el servicio está operativo sin necesidad de ejecutar una clasificación real.

**URL:** `http://localhost:8080/actuator/health`  
**Método:** `GET`  
**Autenticación:** Ninguna

**Respuesta (HTTP 200 — servicio activo):**
```json
{ "status": "UP" }
```

> Este endpoint es consumido por el frontend al cargar la página para actualizar el indicador LED de estado de Spring Boot en la UI.
