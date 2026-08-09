# TechMind — API de Clasificación de Contenidos

> **Grupo 9 · Team 37** · Spring Boot 4.1 · Java 17 · PostgreSQL 16 · FastAPI (ML)

TechMind es una API REST que **clasifica automáticamente contenidos textuales** usando un modelo de Machine Learning externo. El usuario envía un título y un texto; el sistema los persiste, los envía a un microservicio de Data Science (FastAPI), y retorna la categoría predicha junto con palabras clave relevantes.

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [docs/FUNCIONALIDADES.md](docs/FUNCIONALIDADES.md) | Descripción completa de las funcionalidades, endpoints y esquema de base de datos |
| [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md) | Arquitectura del sistema, capas y decisiones técnicas |
| [docs/INTEGRACION_FASTAPI.md](docs/INTEGRACION_FASTAPI.md) | Guía de integración del microservicio FastAPI (Data Science) |
| [docs/SETUP.md](docs/SETUP.md) | Guía de instalación y configuración del entorno local |

---

## ⚡ Inicio Rápido

```bash
# 1. Levantar PostgreSQL con Docker
docker-compose up -d

# 2. Levantar la API Spring Boot
cd api/api
./mvnw spring-boot:run
```

La API queda disponible en **`http://localhost:8080`**.

### Ejemplo de uso

```bash
curl -X POST http://localhost:8080/contenido \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "El auge de la inteligencia artificial en 2025",
    "texto": "Los modelos de lenguaje grande han transformado la industria tecnológica..."
  }'
```

**Respuesta (HTTP 201):**
```json
{
  "categoria": "tecnología",
  "probabilidad": 0.94,
  "informaciones_adicionales": ["inteligencia artificial", "LLM", "tecnología"]
}
```

---

## 🧱 Stack Tecnológico

| Componente | Tecnología |
|------------|-----------|
| API Backend | Spring Boot 4.1 (Java 17) |
| Base de datos | PostgreSQL 16 |
| Migraciones DB | Flyway |
| ORM | Spring Data JPA (Hibernate) |
| Validaciones | Jakarta Bean Validation |
| Infraestructura | Docker / Docker Compose |
| Microservicio ML | FastAPI (Python) — externo |

---

## 📁 Estructura del Repositorio

```
g9-techmind-team37
├── .env                    # Variables de entorno locales
├── docker-compose.yml      # Infraestructura PostgreSQL
├── docs/                   # Documentación del proyecto
│   ├── FUNCIONALIDADES.md
│   ├── ARQUITECTURA.md
│   ├── INTEGRACION_FASTAPI.md
│   └── SETUP.md
└── api                     # Código fuente Spring Boot
    ├── pom.xml
    └── src/
        ├── main/
        │   ├── java/api/   # Código fuente Java
        │   └── resources/  # Config + migraciones SQL
        └── test/
```
