# 📊 Informe de Resultados QA — Sprint 3

**Proyecto:** TechMind — Organización Inteligente del Conocimiento Técnico  
**Componente:** Spring Boot API & Integración con Microservicio de ML / PostgreSQL  
**Responsable QA:** Federico G. Gutierrez  
**Fecha de Ejecución:** 29 de Julio de 2026  

---

## 📈 Resumen Ejecutivo
Durante la fase de validación de la capa de API backend en Spring Boot (conectada a PostgreSQL `techmind` y al microservicio de Machine Learning), se ejecutó la suite de pruebas funcionales, de validación, seguridad y resiliencia. Se evaluó el flujo completo desde la recepción de solicitudes HTTP POST en el servidor (`http://localhost:8080`), la invocación del modelo de ML, la respuesta JSON y la correcta persistencia en la tabla `contenidos`.

Se logró un 100% de cobertura y éxito en los casos planificados, garantizando el cumplimiento de requisitos de esquemas, sanitización de caracteres y estabilidad ante volúmenes extensos de texto.

### 📊 Métricas Generales
* **Casos Planificados:** 6
* **Casos Ejecutados:** 6
* **Casos Exitosos (PASÓ):** 6
* **Casos Fallidos (FALLÓ):** 0
* **Porcentaje de Éxito:** 100%

---

## 🧪 Desglose por Tipo de Prueba
| Categoria | Planificado | PASÓ | FALLÓ | % Éxito |
|-----------|-----------|-----------|-----------|-----------|
| Clasificación y Persistencia Core | 1 | 1 | 0 | 100 |
| Codificación y Caracteres (UTF-8) | 1 | 1 | 0 | 100 |
| Validación de Campos y Esquema | 2 | 2 | 0 | 100 |
| Seguridad y Sanitización | 1 | 1 | 0 | 100 |
| Edge Cases (Textos de Gran Longitud) | 1 | 1 | 0 | 100 |
| **TOTAL** | **6** | **6** | **0** | **100** |

---
## 🐛 Registro de Incidentes y Bug Fixes
| ID Bug | Componente | Descripción de la Falla | Solución Aplicada | Resultado Re-Test QA | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BUG-ENV-01** | `backend/Dockerfile` | Fallo de build en macOS Apple Silicon (ARM64) por imagen `eclipse-temurin:17-jdk-alpine` solo compatible con AMD64 (`no match for platform in manifest`). | Se cambió la imagen base en `Dockerfile` a `eclipse-temurin:17-jdk` y `17-jre` (versiones multi-arquitectura nativas). | **Exitoso.** Build ejecutado mediante `python3 setup.py --docker` en ARM64 (Apple Silicon) y AMD64. Contenedor desplegado correctamente. | **CERRADO** |
---

## 🎯 Conclusión y Recomendaciones
El módulo Spring Boot API ha demostrado una excelente madurez técnica e integración funcional:
- Validaciones de Capa del Servidor: Las anotaciones del Bean Validation (@NotBlank, @NotNull) funcionan según la especificación, interceptando entradas inválidas antes de interactuar con la capa de persistencia y retornando códigos de error adecuados (400 Bad Request).
- Consistencia de Encoding: La configuración UTF-8 en Tomcat/Spring Boot y PostgreSQL preserva la integridad gráfica y semántica de símbolos especiales, comillas y emojis.
- Resiliencia y Inmunidad SQLi: Las consultas parametrizadas implementadas mediante JPA/Hibernate garantizan la sanitización automática de comillas simples y caracteres de escape, previniendo ataques de inyección SQL.
- Manejo de Payloads Masivos: El pipeline procesó de manera transparente textos de más de 50,000 caracteres con respuestas óptimas dentro del umbral de rendimiento esperado.