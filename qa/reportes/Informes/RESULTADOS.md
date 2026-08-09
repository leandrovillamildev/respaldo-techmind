# Informe de resultados

**Proyecto:** TechMind - Organización Inteligente del Conocimiento Técnico  
**Responsable QA:** Federico G. Gutierrez  
**Fecha de Ejecución:** 04 de Agosto de 2026  

## Índice

- [Resumen Ejecutivo](#resumen-ejecutivo)
- [Resultados](#resultados)
- [Desglose por Tipo de Prueba](#desglose-por-tipo-de-prueba)
  - [FastAPI](#fastapi)
  - [PostgreSQL - techmind](#postgresql---techmind)
  - [Spring Boot](#spring-boot)
  - [Frontend](#frontend)
- [Detalle de Casos de Prueba](#detalle-de-casos-de-prueba)
  - [Sprint 1 (FastAPI & PostgreSQL)](#sprint-1-fastapi--postgresql)
  - [Sprint 2 (Data QA - PostgreSQL)](#sprint-2-data-qa---postgresql)
  - [Sprint 3 (Backend Spring Boot & ML)](#sprint-3-backend-spring-boot--ml)
  - [Sprint 4 (Frontend)](#sprint-4-frontend)

## Resumen Ejecutivo
Durante los Sprints 1, 2, 3 y 4, se ejecutaron de manera exhaustiva las suites de pruebas funcionales, de integridad, seguridad y resiliencia sobre el stack completo, abarcando las APIs backend (`FastAPI` y `Spring Boot`), la base de datos PostgreSQL (`techmind`), la integración con el microservicio de Machine Learning y la interfaz de usuario (Frontend en `Vanilla JS/Tailwind`).

- **Sprint 1 (FastAPI & PostgreSQL):** Se ejecutó la suite completa de pruebas sobre los endpoints de la API FastAPI y su integración con PostgreSQL, logrando una cobertura total en escenarios funcionales, de límites, seguridad, resiliencia y validación de datos.
- **Sprint 2 (Data QA - PostgreSQL):** Se auditó la integridad y persistencia de la base de datos techmind, evaluando las tablas contenidos y predicciones. Se logró cobertura total en integridad referencial, consistencia de esquemas, unicidad de claves primarias, límites superiores e inferiores y resiliencia ante inyecciones de datos.
- **Sprint 3 (Backend Spring Boot & ML):** Se validó la capa de API backend en Spring Boot conectada a PostgreSQL y al microservicio de ML, evaluando el flujo punta a punta desde las solicitudes HTTP POST (http://localhost:8080) y la invocación del modelo, hasta la respuesta JSON y la persistencia en contenidos.
- **Sprint 4 (Frontend de TechMind):** Superó exitosamente las pruebas de calidad, demostrando un alto nivel de estabilidad, seguridad y usabilidad. Se validó la protección contra ataques XSS en el manejo del DOM, la reactividad asíncrona para actualizar contenidos sin recargar la página, la prevención de peticiones duplicadas mediante la deshabilitación del botón de envío, y la correcta persistencia visual y accesible de los temas Dark y Light.

En todas las etapas se alcanzó un 100% de cobertura y éxito en los casos planificados, garantizando la estabilidad del sistema ante grandes volúmenes de texto, la sanitización de caracteres y el cumplimiento estricto de esquemas.

## Resultados

| Planificados | Ejecutados | Pasó | Falló | Éxito |
|:---:|:---:|:---:|:---:|:---:|
| 57 | 57 | 57 | 0 | 100% |

## Desglose por Tipo de Prueba

### FastAPI

| Categoría | Planificados | PASÓ | FALLÓ | % Éxito |
|---|:---:|:---:|:---:|:---:|
| Funcionales (Flujo Feliz) | 8 | 8 | -- | 100 |
| Casos Borde / Encoding (UTF-8) | 3 | 3 | -- | 100 |
| Validación de Esquema / Tipos | 3 | 3 | -- | 100 |
| Seguridad (Inyección SQL / Content-Type) | 2 | 2 | -- | 100 |
| Endpoints Complementarios | 3 | 3 | -- | 100 |
| Integridad de Datos | 6 | 6 | -- | 100 |
| **TOTAL** | **25** | **25** | **--** | **100** |

```
El MVP cumple con todos los criterios de aceptación funcionales, de rendimiento (< 2000 ms) y de seguridad especificados para el Sprint 1. La API demuestra alta estabilidad y resiliencia ante errores de infraestructura.
```

### PostgreSQL - techmind

| Categoría | Planificados | PASÓ | FALLÓ | % Éxito |
|---|:---:|:---:|:---:|:---:|
| Completitud | 5 | 5 | -- | 100 |
| Integridad y Estructura | 6 | 6 | -- | 100 |
| Formato y Calidad de Texto | 3 | 3 | -- | 100 |
| Edge Cases (Límites y Vacíos) | 2 | 2 | -- | 100 |
| Rendimiento e Inserción Masiva | 1 | 1 | -- | 100 |
| **TOTAL** | **17** | **17** | **--** | **100** |

```
La capa de datos en PostgreSQL demostró total solidez técnica en el Sprint 1 al garantizar la integridad de los datos (claves primarias, campos obligatorios y unicidad), alta resiliencia y seguridad (protección contra SQLi y soporte de estructuras complejas/TEXT) y excelente escalabilidad frente a inserciones masivas y grandes volúmenes de datos.
```

### Spring Boot

| Categoría | Planificados | PASÓ | FALLÓ | % Éxito |
|---|:---:|:---:|:---:|:---:|
| Clasificación y Persistencia Core | 1 | 1 | -- | 100 |
| Codificación y Caracteres (UTF-8) | 1 | 1 | -- | 100 |
| Validación de Campos y Esquema | 2 | 2 | -- | 100 |
| Seguridad y Sanitización | 1 | 1 | -- | 100 |
| Edge Cases (Textos de Gran Longitud) | 1 | 1 | -- | 100 |
| **TOTAL** | **6** | **6** | **--** | **100** |

```
El módulo Spring Boot API demostró una alta madurez técnica e integración funcional al responder de manera óptima en seguridad, rendimiento e integridad. La aplicación intercepta entradas inválidas en la capa del servidor mediante Bean Validation retornando errores 400 Bad Request, previene ataques de inyección SQL mediante consultas parametrizadas con JPA/Hibernate, preserva símbolos y emojis gracias a su configuración UTF-8, y procesa de forma transparente payloads superiores a los 50.000 caracteres dentro de los tiempos de respuesta esperados.
```

### Frontend
| Categoria | Planificado | PASÓ | FALLÓ | % Éxito |
|-----------|-----------|-----------|-----------|-----------|
| Funcional / Pipeline & Modales | 2 | 2 | 0 | 100 |
| Validación de Controles e Interfaz | 1 | 1 | 0 | 100 |
| Persistencia y Reactividad de Estado (UI) | 1 | 1 | 0 | 100 |
| Seguridad y Sanitización Frontend (XSS) | 1 | 1 | 0 | 100 |
| UX / Control de Performance (Debounce) | 1 | 1 | 0 | 100 |
| Navegación & UI/UX (Light/Dark Mode) | 3 | 3 | 0 | 100 |
| **TOTAL** | **9** | **9** | **0** | **100** |

```
La interfaz de usuario de TechMind demostró una sólida madurez técnica y usabilidad durante el Sprint 4. La aplicación mitiga con éxito vulnerabilidades de XSS al sanitizar las entradas en el DOM, gestiona de forma reactiva y sin recargas la actualización del feed de contenidos, y previene condiciones de carrera deshabilitando el botón de envío tras la primera interacción. Asimismo, el sistema conserva una excelente coherencia visual y accesibilidad en sus modos claro y oscuro, garantizando la estabilidad e integridad de todos sus componentes de diseño.
```

## Detalle de Casos de Prueba

### Sprint 1 (FastAPI)

**Testeo Funcionales (Flujo Feliz) — [8 casos]**
- **CP-FASTAPI-01:** Valida que la API clasifique correctamente un contenido técnico válido devuelto con HTTP 200.
- **CP-FASTAPI-02:** Comprueba la extracción y retorno correcto de la lista de palabras clave relevantes en la respuesta.
- **CP-FASTAPI-03:** Verifica la generación de un score de probabilidad de clasificación válido entre 0 y 1.
- **CP-FASTAPI-09:** Confirma que la estructura del objeto JSON devuelto contenga todas las claves y tipos de datos especificados.
- **CP-FASTAPI-10:** Valida la correcta inicialización y carga de los modelos serializados (.joblib) al arrancar el servicio.
- **CP-FASTAPI-11:** Mide el tiempo de respuesta del endpoint asegurando que la inferencia se ejecute en menos de 2000 ms.
- **CP-FASTAPI-20:** Verifica que el modelo normalice y procese adecuadamente textos ingresados con tildes y mayúsculas sostenidas.
- **CP-FASTAPI-22:** Evalúa la latencia, estabilidad y cero tasa de errores del endpoint ante 100 peticiones concurrentes en ráfaga.

**Casos Borde / Encoding (UTF-8) — [3 casos]**
- **CP-FASTAPI-12:** Evalúa el comportamiento y la gestión de memoria de la API ante payloads de gran tamaño (+500k caracteres).
- **CP-FASTAPI-13:** Garantiza la sanitización y el soporte de codificación UTF-8 procesando caracteres especiales, etiquetas y emojis sin errores.
- **CP-FASTAPI-21:** Evalúa cómo reacciona la API ante entradas no técnicas o sin sentido.

**Validación de Esquema / Tipos — [3 casos]**
- **CP-FASTAPI-14:** Confirma el rechazo inmediato (HTTP 422) por parte de Pydantic al enviar tipos de datos no válidos (números o booleanos).
- **CP-FASTAPI-23:** Valida que la API rechace payloads nulos devolviendo 422 Unprocessable Entity cuando el cuerpo enviado está vacío.
- **CP-FASTAPI-24:** Valida que la API detecte errores de sintaxis JSON y rechace la petición con un 422 Unprocessable Entity.

**Seguridad (Inyección SQL / Content-Type) — [2 casos]**
- **CP-FASTAPI-15:** Comprueba la inmunidad ante intentos de inyección SQL guardando los comandos maliciosos como texto plano.
- **CP-FASTAPI-16:** Valida el rechazo de solicitudes con formatos no soportados como XML mediante una respuesta HTTP 422.

**Endpoints Complementarios — [3 casos]**
- **CP-FASTAPI-17:** Verifica la disponibilidad y estado operativo del microservicio mediante el endpoint de diagnóstico GET /health.
- **CP-FASTAPI-18:** Valida que el endpoint GET /categorias retorne el catálogo completo con las 8 categorías del modelo.
- **CP-FASTAPI-25:** Valida que el endpoint GET /predicciones retorne el catálogo completo con las predicciones realizadas.

**Integridad de Datos — [6 casos]**
- **CP-FASTAPI-04:** Controla el rechazo de la solicitud (HTTP 422) cuando el campo "titulo" se envía vacío.
- **CP-FASTAPI-05:** Controla el rechazo de la solicitud (HTTP 422) cuando el campo "texto" no contiene información.
- **CP-FASTAPI-06:** Valida la respuesta de error adecuada al enviar tanto el título como el texto vacíos en el payload.
- **CP-FASTAPI-07:** Comprueba la intercepción y manejo de excepciones ante la recepción de una estructura JSON mal formada.
- **CP-FASTAPI-08:** Verifica el rechazo con código HTTP 405 Method Not Allowed al enviar una petición GET al endpoint POST /predecir.
- **CP-FASTAPI-19:** Verifica que la API rechace la petición cuando se omiten claves obligatorias dentro del cuerpo JSON.

### Sprint 2 (PostgreSQL)

**Completitud — [5 casos]**
- **CP-DB-01:** Verifica la ausencia de filas incompletas en contenidos.
- **CP-DB-02:** Confirma de que no existen registros de texto idénticos sobrecargando la base de datos.
- **CP-DB-03:** Distribución uniforme y validación sobre las 8 categorías temáticas del modelo.
- **CP-DB-04:** Coincidencia del 100% entre la respuesta JSON de la API y el registro persistido en predicciones.
- **CP-DB-05:** Aprobación de rango numérico estrictamente acotado en [0,0; 1,0].

**Integridad y Estructura — [6 casos]**
- **CP-DB-08:** 100% de unicidad en la columna id de predicciones con secuencia autoincremental coherente.
- **CP-DB-09:** Fechas de la columna created_at válidas, no nulas y alineadas a la zona horaria actual.
- **CP-DB-10:** Confirmación de cadenas válidas y limpias sin presencia de nulos ni espacios aislados.
- **CP-DB-11:** Categorías predichas pertenecientes de forma estricta al dominio semántico (Backend, Bases de Datos, etc.).
- **CP-DB-13:** Coincidencia perfecta del 100% en campos clave de la tabla de origen contenidos.
- **CP-DB-14:** Verifica las restricciones PRIMARY KEY sobre la tabla contenidos.

**Formato y Calidad de Texto — [3 casos]**
- **CP-DB-06:** Valida el tipo de dato text[] para palabras clave e inferencias con arreglos vacíos {}.
- **CP-DB-07:** Sanitización e inserción exitosa del texto literal conteniendo comandos destructivos (ej. '; DROP TABLE...) sin alteración de la estructura.
- **CP-DB-15:** Evaluación cualitativa de textos cortos garantizando significancia técnica para el modelo NLP.

**Edge Cases (Límites y Vacíos) — [2 casos]**
- **CP-DB-16:** Validación de rechazo/ausencia de textos con longitud 0 o TRIM nulo.
- **CP-DB-17:** Confirmación de persistencia íntegra de payloads extensos en el tipo de dato TEXT sin truncamiento.

**Rendimiento e inserción masiva — [1 caso]**
- **CP-DB-12:** Resistencia y persistencia exitosa ante ráfagas de carga masiva de hasta 300 peticiones/minuto.

### Sprint 3 (Backend Spring Boot & ML)

**Clasificación y Persistencia Core — [1 caso]**
- **CP-SPRINGBOOT-01:** Valida que la API clasifique e invoque el modelo de ML, responda con HTTP 201 y persista el contenido en PostgreSQL.

**Codificación y Caracteres (UTF-8) — [1 caso]**
- **CP-SPRINGBOOT-02:** Comprueba la preservación correcta de codificación UTF-8, tildes y emojis en la respuesta JSON y en la base de datos.

**Validación de Campos y Esquema — [2 casos]**
- **CP-SPRINGBOOT-03:** Verifica el rechazo de peticiones sin el campo obligatorio título, devolviendo un error HTTP 400 Bad Request.
- **CP-SPRINGBOOT-04:** Confirma que el backend invalide y rechace mediante @NotBlank las entradas con cadenas vacías o solo espacios.

**Seguridad y Sanitización — [1 caso]**
- **CP-SPRINGBOOT-05:** Evalúa la sanitización del ORM ante comillas simples e inyecciones SQL, garantizando la integridad de la base de datos.

**Edge Cases (Textos de Gran Longitud) — [1 caso]**
- **CP-SPRINGBOOT-06:** Mide el rendimiento y la persistencia sin truncamiento al procesar payloads extensos de más de 50,000 caracteres.

### Sprint 4 (Frontend)

**Funcional / Pipeline & Modales — [2 casos]**
- **CP-FRONTEND-01:** Valida que el usuario pueda ingresar título y texto técnico, ejecutar la clasificación asíncrona y visualizar la categoría predicha, porcentaje de confianza y palabras clave en el panel derecho.
- **CP-FRONTEND-03:** Comprueba que el botón ver JSON desplegue un modal formateado con la sintaxis de respuesta cruda devuelta por el backend (categoría, probabilidad, informaciones_adicionales).

**Validación de Controles e Interfaz — [1 caso]**
- **CP-FRONTEND-02:** Verifica que la aplicación no permita enviar el formulario sin completar los campos de texto requeridos, mostrando advertencias en rojo y evitando llamadas innecesarias a la API.

**Persistencia y Reactividad de Estado (UI) — [1 caso]**
- **CP-FRONTEND-04:** Valida que al clasificar un nuevo elemento, este aparezca inmediatamente en el listado inferior de contenidos clasificados recientemente sin necesidad de refrescar la página.

**Seguridad y Sanitización Frontend (XSS) — [1 caso]**
- **CP-FRONTEND-05:** Asegura que scripts o etiquetas HTML e inyecciones JS ingresadas en el formulario no se ejecuten en el navegador y se muestren escapadas como texto plano.

**UX / Control de Performance (Debounce) — [1 caso]**
- **CP-FRONTEND-06:** Inhabilita el botón de envío tras el primer clic pasando a estado cargando/deshabilitado, evitando múltiples peticiones simultáneas o duplicadas al backend ante doble clic.
- **CP-FRONTEND-06:** Inhabilita el botón de envío tras el primer clic pasando a estado cargando/deshabilitado, evitando múltiples peticiones simultáneas o duplicadas al backend ante doble clic.

**Navegación & UI/UX (Light/Dark Mode) — [3 casos]**
- **CP-FRONTEND-07:** Valida la alternancia fluida entre Modo Claro y Modo Oscuro, manteniendo la legibilidad, contraste de componentes y la persistencia del tema tras recargar la página.
- **CP-FRONTEND-08:** Confirma la correcta navegación y redirección de los ítems de la barra lateral (Historial BD, Swagger FastAPI, Clasificador IA) en interfaz con Modo Oscuro.
- **CP-FRONTEND-09:** Confirma la correcta navegación y redirección de los ítems de la barra lateral (Historial BD, Swagger FastAPI, Clasificador IA) en interfaz con Modo Claro.

---
_QA Testing Guide — TechMind Project v4.0 — Sprint 4_