# CHANGELOG — TechMind · Proyecto Completo

> Todas las versiones están ordenadas de la más reciente a la más antigua.
> Se sigue el formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).
> Para el detalle técnico (causa, síntoma y código) de cada bug, ver [`BUGFIX_REGISTRO.md`](data-science/docs/BUGFIX_REGISTRO.md).

## [2.0.0] — 2026-08-08 · Corrección de Bugs Frontend y Sistema de Internacionalización (ES / EN)

### Corregido

- **Listeners duplicados en modal "Ver JSON" (`frontend/app.js`):** El botón `#btn-view-json` y el botón de cierre `#modal-close` tenían sus event listeners registrados dos veces dentro de `bindEvents()` (líneas 182–193 y 492–501), haciendo que `toggleJsonModal()` se ejecutara dos veces por clic y el modal se abriera y cerrara instantáneamente. Eliminado el bloque duplicado.

- **Ícono `science` desaparecía tras la primera clasificación (`frontend/app.js`):** `setLoadingState(false)` reconstruía el botón "Clasificar con TechMind" sin incluir el `<span class="material-symbols-outlined">science</span>` del HTML original. El botón quedaba sin ícono después de cada uso. Corregido incluyendo el icono en el `innerHTML` de restauración.

- **LED del indicador de estado pulsaba en verde aunque hubiera servicios caídos (`frontend/app.js`):** La clase `led-pulse` (animación de glow verde) se asignaba al LED general en todos los estados, incluyendo el de error. Ahora `led-pulse` solo se aplica cuando *todos* los servicios están operativos.

- **Vista Analytics no removía la clase `flex` al cambiar de sección (`frontend/app.js`):** `showClassifier()` y `showHistory()` agregaban `hidden` a la vista de Analytics pero no removían `flex`, generando un conflicto de layout al navegar de vuelta. Agregado `analyticsView.classList.remove('flex')` en ambas funciones.

- **Botón de admin en español decía "Admin Login" (`frontend/app.js`):** Cambiado el texto del botón en estado deslogueado a `"Iniciar sesión"` en la clave `es` de `TRANSLATIONS` y en `updateAdminUIState()`, que ahora usa `t('admin_login')` en lugar del string hardcodeado.

### Añadido

- **Apertura del sidebar al hacer clic en el LED de "Estado de servicios" (`frontend/app.js`):** El indicador de microservicios en el sidebar colapsado ahora tiene el mismo comportamiento que los íconos de navegación: al hacer clic sobre él estando el sidebar colapsado, se expande automáticamente (con la animación CSS de 320 ms) y luego despliega el popover de estado. Si el sidebar ya está expandido, el popover se abre/cierra de forma normal.

- **Sistema de Internacionalización completo ES / EN (`frontend/index.html` + `frontend/app.js`):**
  - **Botón de idioma `🌐`:** Añadido botón compacto con icono `translate` (Material Symbols) junto al botón de Admin en el encabezado principal. Muestra el idioma al que se puede cambiar (`EN` / `ES`) y en pantallas pequeñas solo muestra el icono. La preferencia se persiste en `localStorage`.
  - **Diccionario `TRANSLATIONS` con 67 claves** en español e inglés, cubriendo la totalidad del texto visible de la UI:
    - Sidebar: navegación, estado de servicios, OCI Server, RAM Usada, toggle de tema.
    - Formulario: título, etiquetas, placeholders, botones.
    - Tarjeta de resultados: título, "Categoría predicha", "Esperando análisis...", "Confianza del Modelo", "Palabras clave extraídas".
    - Historial reciente y vista detallada: encabezados, buscador, filtro, botones "Ver más / Ver menos", "Borrar", "Ver JSON".
    - Analytics: KPI labels, títulos de gráficos, dataset label del line chart.
    - Modal JSON y modal de login admin: todos los textos estáticos.
    - Toasts, mensajes de error, confirmaciones de borrado y estados vacíos.
  - **Función `t(key)`:** Helper global que resuelve la clave en el idioma activo con fallback al español.
  - **Función `applyTranslations()`:** Actualiza en una sola pasada todos los elementos con `data-i18n` / `data-i18n-placeholder`, el header dinámico según la vista activa (`currentView`), el botón del toggle de tema y el estado inicial de la tarjeta de resultados cuando no hay clasificación en curso.
  - **Variable `currentView`:** Registra la vista activa (`'classifier'` / `'history'` / `'analytics'`) para que el header del encabezado se traduzca correctamente al cambiar de idioma desde cualquier sección.
  - **Atributos `data-i18n` y `data-i18n-placeholder`** agregados a ∼35 elementos estáticos en el HTML (sidebar, formulario, resultados, historial, analytics, modales).
  - **`updateThemeToggleUI()`** extraída como función global (antes era un `const` local dentro de `bindEvents()`), permitiendo que `applyTranslations()` la invoque directamente y que el toggle de tema muestre `"Dark mode"` / `"Light mode"` al cambiar al inglés.
  - Al cambiar de idioma, el contenido dinámico visible (tarjetas del historial, gráficos de Analytics) se refresca automáticamente con los textos del nuevo idioma.

---

## [1.9.0] — 2026-08-07 · Rediseño de Sidebar Estilo Claude, UX del Formulario, Responsividad Móvil y Parsing de Horarios UTC

### Añadido
- **Rediseño de Sidebar Colapsable Estilo Claude (`frontend/index.html` + `frontend/app.js`):**
  - **Colapso a Icon Rail (64px):** El sidebar ahora se reduce en escritorio a una barra de iconos centrados (44x44px) alineados simétricamente, manteniendo acceso instantáneo al logo, *Clasificador*, *Historial*, *Análisis*, *Cambiar tema* y *Estado de servicios*.
  - **Controlador Integrado en el Sidebar:** Eliminado el botón flotante del encabezado principal e integrado el chevron de colapso (`<` / `>`) directamente en la cabecera superior derecha del sidebar.
  - **Reapertura al Hacer Clic en Iconos:** Hacer clic sobre el logo de TechMind o sobre cualquier icono de navegación estando colapsado despliega suavemente el sidebar completo (256px).
  - **Reorganización del Isotipo de Marca:** El logo principal reorganiza el título **TechMind** y subtítulo **Organización inteligente** en la parte superior, ubicando el icono de cerebro (`psychology`) centrado directamente **debajo de ambos textos**.
  - **Relocalización del Botón de Cambio de Tema:** Trasladado el botón de tema (claro/oscuro) desde la barra superior hacia la parte inferior del sidebar (justo encima de *Estado de servicios*), integrándose al flujo con etiquetas dinámicas (*Modo claro* / *Modo oscuro*).
  - **Persistencia de Estado:** El estado colapsado o expandido del sidebar se conserva en `localStorage`.

- **Mejoras en el Formulario y Navegación Dinámica (`frontend/index.html` + `frontend/app.js`):**
  - **Botón "Limpiar formulario":** Incorporado botón secundario con icono `delete_sweep` junto al botón principal de clasificación para vaciar título y texto con un solo clic.
  - **Encabezados Dinámicos por Vista:** La barra superior actualiza su título y subtítulo dinámicamente según la subpágina activa (*"Clasificación de contenido técnico"*, *"Historial de consultas"*, *"Panel de análisis"*), eliminando títulos duplicados dentro del contenido.
  - **Conteo Real en Filtro por Categorías:** Las opciones del desplegable de filtro en Historial ahora muestran el número exacto de consultas por categoría (ej. `Backend (3)`, `Todas las categorías (12)`).

- **Optimización Responsiva para Dispositivos Móviles (`frontend/index.html` + `frontend/app.js`):**
  - **Botón Hamburger Móvil (`menu`):** Agregado botón de menú desplegable en el header principal para abrir el sidebar como panel overlay en pantallas `< 768px`.
  - **Botón de Admin Compacto:** El texto "Admin Login" se oculta en móviles pequeños dejando solo el icono `admin_panel_settings`, evitando el salto de línea del título principal.
  - **Pestaña de Análisis Adaptativa:** Tarjetas KPI, rejilla de gráficos de Chart.js y nube de palabras clave escalan sus paddings y tamaños de fuente para visualización perfecta en teléfonos.

- **Panel de Autenticación y Cierre por Clic Externo (`frontend/index.html` + `frontend/app.js`):**
  - **Alineación Simétrica del Popover:** Corregida la posición del menú flotante de Admin (`right-0`) alineándolo perfectamente bajo el botón superior.
  - **Cierre por Clic Fuera (Backdrop & Outside Click):** El menú desplegable de usuario y el modal de inicio de sesión se cierran automáticamente al hacer clic en cualquier área externa.
  - **Duración de Notificaciones (Toasts):** Reducido el tiempo de despliegue de las alertas flotantes de login/logout a 1.8 segundos.
  - **Identidad Visual del Escudo:** Los contenedores del icono de escudo en el popover y en el modal adoptan un tono morado/violeta (`bg-purple-500/20 text-purple-700 dark:text-purple-300`).

- **Precisión de Confianza, Gráficos y Parsing de Horarios UTC (`frontend/app.js`):**
  - **Porcentaje de Confianza con 1 Decimal:** Formateada la cifra de confianza a 1 decimal (ej. `39.5%`) en los resultados del clasificador, tarjetas del historial y KPIs de análisis.
  - **Bordes Limpios y Leyenda Circular en Chart.js:** Actualizada la leyenda del gráfico de dona con estilo de punto circular (`usePointStyle: true, pointStyle: 'circle'`), eliminando bordes negros rígidos. El gráfico se re-renderiza automáticamente al alternar entre modo claro y oscuro.
  - **Conversión de Marcas de Tiempo UTC a Hora Local (`parseDate`):** Implementada la función `parseDate(isoStr)` que parsea marcas de tiempo de PostgreSQL (`created_at`) en UTC y las convierte de forma nativa a la hora local del navegador (ej. UTC-5 en Colombia).

### Corregido / Mejorado
- **Contraste de Colores Verdes en Modo Claro (`frontend/index.html` + `frontend/app.js`):** Reemplazados los tonos verdes claros por `text-emerald-950 font-bold` sobre el botón de Admin activo y en notificaciones Toast para garantizar legibilidad perfecta sobre fondo claro.
- **Hover Morado en Botones Secundarios (`frontend/index.html`):** Los botones "Admin Login" y "Limpiar formulario" incorporan un fondo morado suave traslúcido (`hover:bg-purple-900/10`) al pasar el cursor en modo claro.

---

## [1.8.0] — 2026-08-06 · Panel de Autenticación Admin, Tokens de Sesión y Eliminación de Consultas

### Añadido
- **Autenticación y Sesiones Admin en Microservicio FastAPI (`app/main.py`):**
  - Creado el endpoint `POST /auth/login` que recibe usuario y contraseña, valida credenciales con comparación de hash SHA-256 e inyecta un Token Bearer seguro (`secrets.token_hex(32)`) en `ACTIVE_TOKENS`.
  - Creado el endpoint `POST /auth/logout` para invalidación inmediata de tokens en el servidor.
  - Creado el endpoint protegido `DELETE /predicciones/{prediccion_id}` que requiere la cabecera `Authorization: Bearer <token>` para autorizar la eliminación de consultas.

- **Eliminación en Cascada en PostgreSQL (`app/database.py`):**
  - Implementada la función `delete_prediccion(prediccion_id: int)` que elimina de forma atómica y en cascada la predicción en la tabla `predicciones` y su correspondiente contenido en `contenidos`, incluyendo manejo explícito de `con.rollback()` ante cualquier excepción de base de datos.

- **Paridad en API REST Spring Boot (`backend/api/src/main/java/api/`):**
  - **Servicio:** Añadido el método `@Transactional public boolean eliminarPrediccion(Long prediccionId)` en `PrediccionService.java`.
  - **Controlador:** Expuesto el endpoint `@DeleteMapping("/{id}")` en `ContenidoController.java` para dar soporte a solicitudes de eliminación directa en el puerto 8080.

- **Panel de Login Admin, Menú Popover y Gestión Visual en Web UI (`frontend/`):**
  - **Header:** Botón **Admin Login** en la barra superior con indicador dinámico de estado (`🛡️ Admin (usuario)`).
  - **Modal de Login Centrado (`index.html` + `app.js`):** Interfaz modal Cyber AI Glassmorphism perfectamente centrada en pantalla para la autenticación de administradores con validación y alertas.
  - **Menú Desplegable Popover:** Al estar logueado como administrador, un clic sobre el botón abre un menú popover con información del usuario activo y el botón de acción **"🚪 Cerrar Sesión"**.
  - **Acceso Invitados:** Los usuarios sin autenticar mantienen el uso libre del clasificador e historial pero sin acceso a botones de borrado.
  - **Botones "🗑️ Borrar":** En las tarjetas e ítems del historial se renderizan condicionalmente los botones de eliminación cuando la sesión de administrador está activa, con alerta de confirmación y refresco en tiempo real del historial y los gráficos del Dashboard de Análisis.

- **Configuración Interactiva e Integración Docker (`setup.py`, `.env.example`, `docker-compose.yml`):**
  - **Setup Universal:** `setup.py` solicita interactivamente el usuario y contraseña del administrador en la primera ejecución y actualiza automáticamente `.env`.
  - **Docker Compose:** Propagadas las variables `ADMIN_USER`, `ADMIN_PASSWORD` y `JWT_SECRET` a los servicios de `fastapi` y `springboot`.

---

## [1.7.0] — 2026-08-04 · Dashboard de Análisis Gráfico y Estadísticas en Tiempo Real (Chart.js + PostgreSQL)

### Añadido
- **Función y Endpoint de Analytics (`app/database.py` + `app/main.py`):** Creado el módulo `get_analytics_data()` y el endpoint `GET /analytics` en FastAPI, que ejecuta consultas SQL optimizadas sobre la base de datos PostgreSQL para obtener:
  - **KPIs:** Total de predicciones registradas, categoría con mayor volumen de consultas y nivel promedio de confianza del modelo.
  - **Distribución por Categoría:** Conteo relativo entre las 8 categorías del sistema.
  - **Distribución Horaria (24h):** Actividad agrupada por hora del día (`EXTRACT(HOUR FROM created_at)`).
  - **Frecuencia de Keywords:** Ranking de las 15 palabras clave más comunes normalizadas a minúsculas y desduplicadas por documento.

- **Sección e Interfaz "Análisis" en la Web UI (`frontend/index.html` + `frontend/app.js`):**
  - **Navegación:** Agregado el nuevo botón **"Análisis"** (`analytics`) en la barra de navegación lateral (Sidebar) ubicado justo debajo de *Historial*.
  - **Librería de Gráficos:** Integración de **Chart.js 4.4+** vía CDN.
  - **KPI Cards:** 3 tarjetas superiores (*Total Clasificaciones*, *Categoría Líder*, *Confianza Promedio*) con iconografía neón.
  - **Visualizaciones Interactivas:**
    1. 🍩 **Doughnut Chart:** Distribución porcentual por categoría técnica.
    2. 📈 **Area Line Chart:** Curva de actividad de consultas a lo largo de las 24 horas del día.
    3. 🏷️ **Nube de Etiquetas (Tag Cloud de Badges/Pills):** Reemplazado el gráfico de barras por una rejilla compacta de pastillas neón interactivas con contador de frecuencia (`#keyword  count`), ahorrando más del 60% de espacio vertical.
  - **Compatibilidad de Tema:** Los gráficos adaptan dinámicamente sus colores, rejillas y etiquetas al cambiar entre *Modo Claro* y *Modo Oscuro*.

### Corregido / Mejorado
- **Refresco condicional/lazy de Analytics para conservar recursos (`frontend/app.js`):** La llamada a `loadAnalyticsDashboard()` tras una clasificación ahora verifica si la pestaña *"Análisis"* está activa. Si el usuario está en la vista del Clasificador, no realiza ninguna petición al servidor hasta que abra la pestaña.
- **Intervalo equilibrado de polling de métricas (`frontend/app.js`):** Ajustado el intervalo de consulta de `fetchSystemStats` a 10 segundos, logrando un equilibrio perfecto entre fluidez en tiempo real y conservación de recursos en la VM de OCI.
- **Evitado de caché en consultas de telemetría (`frontend/app.js`):** Agregado el parámetro de marcas de tiempo `?t=${Date.now()}` a las peticiones HTTP del dashboard para evitar que el navegador responda con datos cacheados.
- **Adaptación automática a la zona horaria del usuario (`app/database.py` + `frontend/app.js`):** El frontend detecta automáticamente el desfasaje horario del navegador (`new Date().getTimezoneOffset()`) y lo envía en el parámetro `tz_offset`. PostgreSQL desplaza el cálculo de `EXTRACT(HOUR FROM (created_at + interval))` para que la curva de actividad 24h muestre exactamente las horas locales de la región del usuario (ej: 16:00 hs en lugar de 19:00 hs UTC).
- **Filtro de conectores y adverbios genéricos (`app/main.py` + `app/database.py`):** Agregado el conjunto `RUIDO_CONECTORES` (*mediante, globalmente, además, través, según, principal, cada, etc.*) a las stopwords del pipeline NLP y a la agregación de analytics, asegurando que el ranking de palabras clave solo muestre conceptos y tecnologías puramente técnicas (*FastAPI, Docker, Spring Boot, PostgreSQL, JWT, etc.*).
- **Normalización estricta de palabras clave (`app/database.py`):** Removidos corchetes `[` `]` y comillas simples/dobles residuales en la columna `palabras_clave` de PostgreSQL antes de contabilizar frecuencias.

---

## [1.6.1] — 2026-08-04 · Métricas en Tiempo Real del Servidor OCI (CPU, RAM y Swap)

### Añadido
- **Endpoint de telemetría de hardware en FastAPI (`app/main.py`):** Creado el endpoint `GET /system-stats` respaldado por `psutil` (con fallback nativo a `/proc/meminfo` y `os.getloadavg()` en Linux), que expone métricas en tiempo real de consumo de CPU (%), RAM total/usada/disponible (MB), Swap (MB) y **tiempo de actividad del servidor (Uptime)**.
- **Widgets visuales de telemetría en el Frontend (`frontend/index.html` + `frontend/app.js`):** Expandido el popover *"Estado de servicios"* en la barra lateral (Sidebar) reemplazando la etiqueta fija con un badge dinámico de **Uptime** (`schedule`) y 3 barras de progreso animadas en estética *Cyber AI Dark Mode*:
  - ⏱️ **Badge de Uptime del servidor** (ej. `2d 4h 15m`).
  - 💻 **Carga de CPU** con porcentaje actualizado dinámicamente.
  - 🧠 **Consumo de RAM** con lectura de megabytes usados/totales y badge indicador de **RAM Libre**.
  - 🔄 **Consumo de Swap** con barra de capacidad.
  - **Polling en tiempo real:** Actualización automática cada 5 segundos.
  - **Código de colores reactivo:** Verde (RAM < 80%), Amarillo (RAM 80%-90%), Rojo (RAM > 90%).

---

## [1.6.0] — 2026-08-03 · Mejoras de Isotipo, Hover Unificado y Funciones de Historial

### Añadido
- **Botón "Ver más" / "Ver menos" en descripciones del Historial (`frontend/app.js`):** Agregada la capacidad de expandir y contraer descripciones extensas en las tarjetas de consulta tanto en el grid inicial como en la lista detallada.
- **Botón "Copiar JSON" por consulta en el Historial (`frontend/app.js`):** Cada entrada del historial incorpora su propio botón interactivo para copiar el objeto JSON completo de la consulta al portapapeles con feedback instantáneo (`¡Copiado!`) y notificación flotante.

### Corregido
- **Contraste y color del Isotipo de TechMind en Modo Claro (`frontend/index.html`):** Ajustados los tonos del isotipo (`psychology`) a morado violeta intenso (`text-purple-700 dark:text-primary`) y el nombre TechMind a `text-purple-950 dark:text-primary-fixed`, resolviendo la falta de contraste en el modo claro.
- **Hover unificado para Clasificador, Historial y Estado de servicios (`frontend/index.html` + `frontend/app.js`):** Creada la clase CSS `.sidebar-nav-item` que unifica el estilo hover para los 3 botones principales del sidebar con fondo violeta traslúcido, borde suave y elevación idéntica.

---

## [1.5.2] — 2026-08-03 · Optimización de `docker-compose.yml` para OCI Free Tier (1 vCPU · 1 GB RAM · 2 GB Swap)

### Mejorado
- **Límites de memoria por contenedor (`docker-compose.yml`):** Se agregaron `mem_limit` y `memswap_limit` a los cuatro servicios para prevenir que el OOM Killer del kernel mate procesos silenciosamente cuando la RAM se agota. El presupuesto total queda dentro del límite de 1 GB de RAM real, usando el swap de 2 GB como colchón ante picos de carga:

  | Servicio | `mem_limit` (RAM) | `memswap_limit` (RAM + Swap) |
  |---|---|---|
  | `postgres` | 150 MB | 300 MB |
  | `fastapi` | 220 MB | 440 MB |
  | `springboot` | 384 MB | 768 MB |
  | `frontend` | 48 MB | 96 MB |
  | **Total estimado** | **~982 MB** | **dentro del 1 GB** |

- **Límites de CPU por contenedor (`docker-compose.yml`):** Se agregó la directiva `cpus` a cada servicio para evitar que un solo contenedor monopolice el único vCPU disponible:
  - `postgres`: `0.25` (mayormente I/O)
  - `fastapi`: `0.50` (inferencia por request)
  - `springboot`: `0.50` (API transaccional)
  - `frontend`: `0.10` (Nginx estático)

- **Tuning de PostgreSQL para bajo consumo de RAM (`docker-compose.yml`):** Se agregó la directiva `command` con parámetros optimizados para entornos de 1 GB:
  - `shared_buffers=32MB` (reducido desde el default de 128MB)
  - `work_mem=4MB` (20 conexiones × 4MB = 80MB pico)
  - `maintenance_work_mem=32MB`
  - `effective_cache_size=128MB`
  - `max_connections=20` (suficiente para el pool de Spring Boot)
  - `wal_buffers=8MB`, `checkpoint_completion_target=0.9`

- **Uvicorn single-worker (`docker-compose.yml`):** Se sobreescribió el `command` del servicio `fastapi` para forzar `--workers 1`, evitando que Uvicorn spawne múltiples workers en una instancia de 1 vCPU. Se agregó `--limit-max-requests 500` para que el worker se reinicie periódicamente y libere posibles memory leaks de las librerías de ML.

- **Healthcheck más tolerante para PostgreSQL:** Se aumentó `start_period` de 0s a 20s para dar más tiempo de arranque a la base de datos en una instancia con I/O lenta (OCI Free Tier usa almacenamiento de bloque compartido).

---

## [1.5.1] — 2026-08-03 · Actualización del Notebook de Data Science (Alineación con Pipeline de Producción + Cross-Validation)

### Añadido / Mejorado
- **Ampliación del Dataset de Entrenamiento (`data-science/data/raw/contenidos_tecnicos.csv`):** Dataset expandido de ~221 a **259 registros técnicos balanceados** (+38 registros especializados), resolviendo ambigüedades y reforzando la precisión en las categorías **Mobile** (*SwiftUI, Jetpack Compose, Flutter Dart AOT, React Native Fabric, Kotlin KMP*) y **Cloud** (*AWS VPC, Lambda, S3, CloudFront, Terraform HCL, OCI Autonomous DB, FinOps*).
- **Ensamble de Modelos con Calibración de Confianza (`data-science/src/expand_and_train.py`):** Reemplazada la `LogisticRegression` individual por un ensamble `VotingClassifier` (Soft Voting) que combina 3 algoritmos complementarios:
  1. `LogisticRegression` con pesos de clase balanceados ($C=1.5$).
  2. `CalibratedClassifierCV(LinearSVC)` con calibración de probabilidades de Platt (`method='sigmoid'`), proporcionando estimaciones de confianza nítidas y precisas.
  3. `ComplementNB` optimizado para clasificación de textos.
- **Preprocesamiento y NLTK Stopwords (`data-science/src/expand_and_train.py` + `app/main.py`):** Integrado el corpus oficial de 154 stopwords en español de NLTK en el pipeline de entrenamiento e inferencia FastAPI, omitiendo además términos de ruido técnico neutro (*"tutorial"*, *"guia"*, *"ejemplo"*, *"introduccion"*).
- **Feature Engineering con TF-IDF Sublineal y N-Gramas 1-3 (`data-science/src/expand_and_train.py`):** Configurado `TfidfVectorizer` con `sublinear_tf=True` (escalado logarítmico de término $1 + \log(tf)$) y rango de n-gramas de 1 a 3 para capturar expresiones técnicas compuestas (*"aws lambda serverless"*, *"react native navigation"*).
- **Nuevos Artefactos `.joblib` (`data-science/models/`):** Generados los archivos binarios `tfidf_vectorizer.joblib` y `modelo_clasificador.joblib` manteniendo 100% la compatibilidad con los contratos de API de FastAPI y Spring Boot.
- **Incremento en Métricas de Rendimiento:** Alcanzado un **90.38% de Accuracy** en la evaluación holdout (20% test data), logrando un **100% de Precisión/Recall en Mobile** y un **94% de F1-Score en Cloud**.
- **Notebook reescrito para reflejar el pipeline de producción actual (`data-science/notebooks/TechMind_DataScience.ipynb`):** El notebook estaba desactualizado respecto a `expand_and_train.py` — mostraba 61 registros, usaba un `TfidfVectorizer` básico (1-2 n-gramas, 1500 features) y un `LogisticRegression` individual. Se reescribió completo (de 64 celdas dispersas a 40 celdas consolidadas y documentadas) para reflejar fielmente el pipeline de producción:
  - Carga dinámica del CSV mostrando **259 registros** reales.
  - Concatenación de `titulo + texto` en el preprocesamiento (alineado con la mejora del ensamble).
  - `TfidfVectorizer` sublineal con n-gramas 1-3 y 6 000 features (idéntico a `expand_and_train.py`).
  - **Ensamble Calibrado** (`LogisticRegression` + `CalibratedClassifierCV(LinearSVC)` + `ComplementNB`) con soft voting.
  - Todos los gráficos (distribución de categorías, longitud de textos, confusion matrix) regenerados con los 259 registros actuales.
  - Compatibilidad total con nbformat 4.5 (campo `id` en cada celda).
- **Validación Cruzada Estratificada K-Fold (K=5) (`data-science/notebooks/TechMind_DataScience.ipynb`):** Nueva sección 9 que usa el **100% de las muestras** para evaluar el modelo, eliminando la dependencia de un único corte de datos. Implementada con un `Pipeline(TF-IDF → Ensamble)` correcto que re-fitea el vectorizador en cada fold para evitar *data leakage*. Resultados obtenidos:
  - Accuracy promedio CV: **87.28% ± 4.11%**
  - Rango: [80.77% – 92.16%]
  - Gráfico de barras por fold incluido.

### Corregido
- **Porcentajes de Confianza con decimales y punto sobrante (`frontend/index.html` + `frontend/app.js`):** Eliminadas las cifras decimales en la "Confianza del Modelo" tanto en el marcador principal (`0%`) como en los registros del historial reciente y la vista detallada (`Math.round(prob * 100)`).
- **Legibilidad del mensaje de error de BD en Modo Claro (`frontend/app.js`):** Actualizados los estilos en el bloque `catch` del historial para que las alertas de error de conexión a la base de datos se muestren en un color rojo oscuro bien definido (`text-rose-700 dark:text-rose-200`) y con alto contraste sobre fondo claro.
- **Resplandor y deslumbre del Modo Claro (`frontend/index.html`):** Redefinidas las variables CSS `:root` hacia un diseño cálido cremita/arena mate (`#e8e2d5` y `#eee7d9`) con tipografía en tono café/carbón profundo (`#231f18`), eliminando la iluminación blanca cegadora de fondo e inputs.
- **Parpadeo de cambio de fuente / FOUT (`frontend/index.html`):** Al cargar la aplicación, se percibía un breve intercambio o parpadeo (*font swap*) debido a la directiva `display=swap` en Google Fonts. Resuelto precargando la hoja de estilos (`rel="preload"`) y cambiando el parámetro a `display=block` para que el texto se renderice directamente en la tipografía definitiva (`Inter` / `Outfit`) desde el primer instante sin ningún parpadeo.
- **Ícono de estrellas en etiqueta de Confianza (`frontend/app.js`):** Eliminado el ícono de estrellas (`auto_awesome` ✨) posicionado al lado de la etiqueta "Confianza: %" en las tarjetas del historial.
- **Efecto borroso en el Sidebar Móvil (`frontend/index.html`):** Eliminadas las clases `backdrop-blur-sm` y `backdrop-blur-2xl` en el overlay y panel de navegación lateral para evitar distorsiones al abrir el menú en dispositivos móviles.
- **Ortografía y formato en textos del sistema (`frontend/index.html` + `frontend/app.js`):** Corregidos acentos, minúsculas tras comas o inicios de descripciones y estandarización ortográfica.

### Añadido
- **Notificación de alerta cuando faltan campos al clasificar (`frontend/app.js`):** Al presionar el botón de clasificación con campos vacíos, se despliega la alerta con el mensaje exacto `Por favor, llena todos los campos`. Ante errores de conexión o servidor, se mantiene el mensaje `Hubo un error, por favor intenta de nuevo más tarde`.
- **Navegación al inicio mediante el logo TechMind (`frontend/index.html` + `frontend/app.js`):** El elemento de marca "TechMind" en el sidebar redirige al usuario de vuelta a la vista principal (Home/Clasificador) al hacer clic.

### Decisión de Arquitectura
- `expand_and_train.py` permanece como **fuente de verdad de producción** (genera los artefactos `.joblib` para la API FastAPI).
- El notebook actúa como **documentación viva y reproducible** del mismo pipeline, enriquecida con Cross-Validation como capa adicional de análisis para presentación.

---

## [1.3.2] — 2026-07-31 · Estabilidad en OCI (memoria, devtools y auto-restart)

### Corregido

- **`backend/Dockerfile` — JVM sin límite de heap → OOM Killer del kernel:** Spring Boot corría sin flags `-Xmx`, por lo que la JVM podía crecer hasta consumir toda la RAM del servidor. En el OCI Free Tier (1 GB RAM), después de unas horas el kernel de Linux terminaba el proceso silenciosamente mediante el OOM Killer, dejando el servicio en rojo sin ningún error explícito en los logs de Docker. Corregido añadiendo `-Xms64m -Xmx256m -XX:+UseSerialGC` al `ENTRYPOINT`, limitando el heap máximo a 256 MB y usando el GC serie (más eficiente en CPUs de 1–2 núcleos).

- **`backend/api/pom.xml` — `spring-boot-devtools` activo en producción:** La dependencia `spring-boot-devtools` tenía `<scope>runtime</scope>`, lo que hacía que se incluyera en el JAR final y se activara dentro del contenedor Docker, monitoreando el filesystem en busca de cambios y reiniciando la aplicación innecesariamente, consumiendo CPU y RAM de forma continua. Cambiado a `<scope>test</scope>` para excluirlo del artefacto de producción. El comportamiento en desarrollo local (IntelliJ / VS Code) no se ve afectado.

- **`docker-compose.yml` — contenedores sin política de reinicio:** Ningún servicio tenía definida la directiva `restart`, por lo que si un contenedor crasheaba (por OOM u otro error) quedaba detenido permanentemente hasta intervención manual. Añadido `restart: unless-stopped` a los cuatro servicios (`postgres`, `fastapi`, `springboot`, `frontend`) para garantizar auto-recovery automático ante fallos y arranque automático tras un reinicio de la VM.

---

## [1.3.1] — 2026-07-30 · Compatibilidad Docker Compose v2

### Corregido
- **`setup.py` — migración de `docker-compose` (v1) a `docker compose` (v2):** El script de setup usaba el binario standalone `docker-compose` (Docker Compose v1, deprecado desde 2023), que no está disponible en instalaciones modernas de Docker Engine. En servidores con Docker Compose v2 instalado como plugin, los comandos fallaban con error de comando no encontrado. Se reemplazaron las 6 llamadas afectadas:
  - `docker compose up -d postgres`
  - `docker compose --profile full up -d --build`
  - `docker compose --profile full down`
  - `docker compose --profile full down -v` (ejecución + mensajes de ayuda)

  El comando `docker compose` (sin guión) es compatible con Windows (Docker Desktop), macOS (Docker Desktop) y Linux (Docker Engine 20.10+), por lo que el cambio es transparente en todos los entornos.

---

## [1.3.0] — 2026-07-30 · Mejoras de UX en Clasificador

### Corregido
- **Ícono duplicado en sidebar (`frontend/index.html`):** El enlace de navegación "Clasificador" usaba el mismo ícono `psychology` que el logo principal "TechMind" en la parte superior del sidebar, generando confusión visual. Reemplazado por el ícono `category` de Material Symbols para diferenciar claramente ambos elementos.
- **Decimales excesivos en probabilidad (`app/database.py` + `frontend/app.js`):** Los valores de probabilidad devueltos por el modelo ML se mostraban con hasta 4 decimales. Se aplica `round(float, 2)` en la API Python (`get_predicciones`) y `Math.round` en el frontend antes de renderizar. El porcentaje de confianza en la UI se muestra con 2 decimales.
- **Efecto de brillo blanco/púrpura sobre el panel de resultados (`frontend/index.html`):** Eliminado el `<div>` con clase `bg-primary-fixed blur-md` posicionado en la esquina superior derecha del recuadro "Resultado del Análisis", que generaba un resplandor no deseado sobre el borde superior del panel.

### Mejorado
- **Limpieza automática de campos tras clasificar (`frontend/app.js`):** Al hacer clic en "Clasificar con TechMind" y recibir una respuesta exitosa, los campos de título y contenido se vacían automáticamente, preparando la interfaz para una nueva consulta sin necesidad de borrar manualmente el texto anterior.
- **Descripción del contenido visible en historial (`app/database.py` + `frontend/app.js`):** La consulta SQL del endpoint `GET /predicciones` ahora incluye el campo `c.texto` de la tabla `contenidos`. El frontend muestra el texto/descripción truncado (con `line-clamp-2`) debajo del título tanto en las tarjetas recientes del clasificador como en la subpágina de historial detallado.

---

## [1.2.0] — 2026-07-30 · Health Check de Spring Boot + Actuator

### Corregido
- **Bug visual en la UI — indicador LED de Spring Boot siempre en rojo (`frontend/app.js`):** El health check usaba `fetch('/contenido', { method: 'OPTIONS' })` para detectar si Spring Boot estaba activo. El browser bloqueaba esta llamada por política CORS al tratarla de forma distinta a un preflight automático, lanzando siempre el bloque `catch` y mostrando el LED en rojo aunque el servidor estuviera operativo y la clasificación funcionara correctamente. Corregido reemplazando el método `OPTIONS` por `GET /actuator/health`, consistente con el patrón ya aplicado para FastAPI.
- **Redundancia y UX en Modal JSON de Inferencia (`frontend/index.html` y `frontend/app.js`):** Se eliminó el botón redundante "Cerrar" en la barra inferior del modal. Se habilitó el cierre nativo mediante el botón "X" en la barra superior, click en el fondo oscuro (backdrop) y presionado de la tecla `Escape`.

### Añadido
- **Botón "Copiar JSON" en Modal de Inferencia (`frontend/index.html` y `frontend/app.js`):** Reemplazado el pie del modal con una acción de exportación interactiva que copia todo el payload JSON (entrada + resultado) al portapapeles con feedback animado de 2 segundos ("¡Copiado!") y notificación Toast.

### Añadido
- **`spring-boot-starter-actuator` en `backend/api/api/pom.xml`:** Nueva dependencia que expone el endpoint estándar `GET /actuator/health` con respuesta `{ "status": "UP" }` cuando el servicio está operativo.
- **Configuración de Actuator en `backend/api/api/src/main/resources/application.properties`:**
  - `management.endpoints.web.exposure.include=health` — solo expone el endpoint de salud (no métricas ni información sensible).
  - `management.endpoint.health.show-details=never` — respuesta mínima sin detalles internos.
  - `management.endpoints.web.cors.allowed-origins=*` y `allowed-methods=GET` — permite que el frontend consulte el endpoint sin errores de CORS.

### Documentación
- **`backend/docs/ARQUITECTURA.md`:** Actualizados el bloque de `application.properties` con las nuevas propiedades de Actuator, el flujo de arranque (ahora lista los dos endpoints expuestos en `:8080`) y agregada la nueva sección *"Endpoint de Health Check"* con contrato JSON.
- **`backend/docs/FUNCIONALIDADES.md`:** Título actualizado a *"Endpoints Disponibles"* (plural). Agregada sección `GET /actuator/health` con contrato completo, descripción de uso y contexto de integración con el frontend.
- **`backend/docs/SETUP.md`:** Health check básico corregido (de `curl /contenido` a `curl /actuator/health`). Agregada entrada en Troubleshooting: *"El indicador de Spring Boot aparece en rojo en la UI"* con causa, verificación y solución.
- **`frontend/README.md`:** Indicadores de estado detallados con el endpoint exacto que cada servicio usa para su health check.

---

## [1.1.0] — 2026-07-28 · Sprint 2 & QA Automation (anterior)

### Añadido
- **Diagrama Infográfico de Arquitectura de Sistema:** Generado e integrado en `README.md` (`assets/techmind_project_flow.png`) mostrando el flujo visual multicontenedor (Frontend UI → Spring Boot :8080 → FastAPI ML :8000 → PostgreSQL 16 :5432).
- **Suite de Pruebas Automatizadas de QA (Sprint 2):** Creada e implementada suite de 14 casos de prueba E2E cubriendo flujos felices, límites de carga, resistencia a inyección SQL/XSS, resiliencia y validación de tipos HTTP (reporte en `qa/reportes/resultados-sprint-2.md`).
- **Documentación del Esquema Relacional de PostgreSQL:** Creado informe técnico completo (`informe_base_de_datos.md`) con diagrama Entidad-Relación (ER) Mermaid, contratos DDL, índices y mapeo JPA.

### Corregido
- **Eliminación de la llamada redundante `log_prediccion()` en FastAPI (`app/main.py` y `app/database.py`):** Solucionado el error de log en PostgreSQL (`null value in column "contenido_id" violates not-null constraint`). FastAPI opera ahora como un microservicio 100% stateless mientras Spring Boot administra la transacción y asignación de `contenido_id`.

---

## [0.6.0] — 2026-07-22 · Bug Fixes + Corrección de rutas del modelo

### Corregido
- **Bug crítico en `app/main.py` — endpoint `POST /predecir`:** la variable `probabilidad` nunca se calculaba antes de ser usada en `log_prediccion()`, lo que causaba un `NameError` en runtime. Se agregó el cálculo correcto usando `modelo.predict_proba(vector)[0].max()` antes de la llamada a la función de logging.
- **Rutas de serialización en `TechMind_DataScience.ipynb`:** las celdas de `joblib.dump()` y `joblib.load()` usaban rutas relativas simples (`"tfidf_vectorizer.joblib"`, `"modelo_clasificador.joblib"`) que guardaban los artefactos en el directorio de trabajo del kernel (`data-science/notebooks/`), no en `data-science/models/` donde FastAPI los busca. Se corrigieron las rutas a `"../models/tfidf_vectorizer.joblib"` y `"../models/modelo_clasificador.joblib"`.
- **Esquema PostgreSQL — tabla `predicciones`:** la columna fue creada por el script de migración (`migrate_to_postgres.py`) con el nombre `keywords` en lugar de `informaciones_adicionales`, lo que causaba un error silencioso al intentar persistir cada predicción. Corregido en dos pasos: (1) `ALTER TABLE` sobre la DB existente y (2) corrección del nombre en el `SCHEMA_SQL` del script de migración para que instalaciones nuevas también queden correctas.

### Verificado
- Pipeline completo probado end-to-end: `POST /predecir` → clasificación → persistencia en PostgreSQL sin errores.
- Los modelos `.joblib` ahora se generan directamente en `data-science/models/` al ejecutar el notebook.

---

## [0.5.0] — 2026-07-21 · Ingesta de Documentos + Re-entrenamiento Automático

### Añadido
- **Script de ingesta interactiva** (`ingest_documents.py`) que permite importar archivos PDF (`pdfplumber`) y DOCX (`python-docx`) a PostgreSQL.
  - Soporta la extracción y limpieza automatizada de texto.
  - Permite etiquetar manualmente la categoría (Opción A) en una interfaz CLI interactiva con preview de texto.
  - Detección de secciones para documentos multi-categoría, permitiendo split y etiquetado independiente por sección.
  - Control de duplicados mediante verificación del hash MD5 del contenido en la base de datos.
- **Re-entrenamiento automático local**: el script de ingesta cuenta con un trigger automático que detecta si se han importado 3 o más documentos en una sola sesión y ofrece ejecutar el notebook mediante Jupyter (`jupyter nbconvert --execute`) en segundo plano para regenerar los modelos `.joblib`.
- **Nueva guía de ingesta** (`INGESTA_DOCUMENTOS.md`) detallando la preparación de documentos, flujo de ejecución, Edge Cases y solución de problemas.
- **Guía de entrega de Backend** (`ENTREGA_BACKEND.md`) para facilitar al equipo Java qué archivos deben clonarse (código, docker, docs) y cuáles compartirse manualmente (modelos `.joblib` en `.gitignore`).
- **Plan y suite de pruebas para QA** (`QA_TESTING.md` y `postman_collection.json`) con 23 casos de prueba para validar Happy Paths, Edge Cases, Error Handling y performance contra el endpoint local.

### Cambiado
- **`requirements.txt`** — agregadas dependencias para procesamiento de documentos: `pdfplumber>=0.11.0` y `python-docx>=1.1.0`.
- **`.gitignore`** — modificado para excluir archivos locales PDF y DOCX en la carpeta `documentos/` (`documentos/*.pdf` y `documentos/*.docx`) y mantener solo la carpeta usando `.gitkeep`.
- **`README.md`** — tabla de documentación actualizada con los nuevos entregables (`ENTREGA_BACKEND.md`, `QA_TESTING.md`, `INGESTA_DOCUMENTOS.md` y `postman_collection.json`).

---

## [0.4.0] — 2026-07-21 · FastAPI + PostgreSQL

### Añadido
- **Microservicio FastAPI** (`app/main.py`) con tres endpoints:
  - `POST /predecir` — inferencia interna consumida por Spring Boot. Carga los `.joblib` al arrancar, clasifica el texto y persiste la predicción en PostgreSQL.
  - `GET /health` — health check para que Spring Boot verifique disponibilidad antes de llamar.
  - `GET /categorias` — devuelve la lista de las 8 categorías del modelo.
  - `GET /docs` — documentación Swagger automática generada por FastAPI.
- **Módulo de base de datos** (`app/database.py`) con `get_connection()`, `init_db()` y `log_prediccion()` para PostgreSQL.
- **Script de migración a PostgreSQL** (`migrate_to_postgres.py`) — crea las tablas `contenidos` y `predicciones`, lee desde SQLite o CSV, e incluye confirmación interactiva para evitar reemplazos accidentales.
- **Tabla `predicciones`** en PostgreSQL — log automático de cada inferencia con `titulo`, `texto`, `categoria`, `probabilidad`, `informaciones_adicionales` y `created_at`.
- **`docker-compose.yml`** — levanta PostgreSQL 16 localmente con un solo comando (`docker-compose up -d`). Incluye health check y volumen persistente.
- **`.env.example`** — plantilla de variables de entorno para Python (FastAPI) y referencia para Spring Boot.
- **`.gitignore`** — excluye `.env`, `*.joblib`, `techmind.db` y archivos de Python/Jupyter del repositorio.
- **`BACKEND_INTEGRATION.md`** — guía completa para el equipo de Java/Spring Boot: setup, contrato del endpoint `/predecir`, ejemplos de código Java (`RestTemplate` y `WebClient`), configuración de `application.properties`, schema SQL y checklist de verificación.

### Cambiado
- **`requirements.txt`** — agregados `fastapi>=0.111.0`, `uvicorn[standard]>=0.29.0`, `psycopg2-binary>=2.9.9`, `python-dotenv>=1.0.0`.
- **`TechMind_DataScience.ipynb` — Celda 3** — modo dual: si `PG_HOST` está configurado carga desde PostgreSQL; si no, hace fallback a SQLite local (retrocompatible).

### Arquitectura
```
Postman → Spring Boot (8080) → FastAPI (8000) → PostgreSQL (5432)
                     └─────────────────────────────────────────────┘
```

---

## [0.3.0] — 2026-07-17 · Migración de base de datos a SQLite

### Añadido
- **Base de datos SQLite** `techmind.db` — migración del dataset original `contenidos_tecnicos.csv` a una base de datos relacional embebida. La tabla `contenidos` incorpora dos campos nuevos respecto al CSV:
  - `id` — clave primaria autoincremental, necesaria para que el Back-End pueda referenciar registros individuales.
  - `created_at` — timestamp UTC de inserción, útil para auditoría y reentrenamiento incremental.
- **Script de migración** `migrate_to_sqlite.py` — script Python reutilizable (sin dependencias externas, solo stdlib) que: lee el CSV → crea el esquema → importa los 61 registros → verifica la distribución por categoría → imprime ejemplos de carga. Puede volver a ejecutarse en cualquier momento para regenerar la DB desde cero.
- **Índice sobre `categoria`** (`idx_categoria`) — mejora el rendimiento de consultas por categoría, especialmente relevante cuando el dataset crezca.

### Cambiado
- **Notebook `TechMind_DataScience.ipynb` — Celda 3**: la carga del dataset se migró de `pd.read_csv("contenidos_tecnicos.csv")` a `pd.read_sql_query(...)` sobre `techmind.db`. El resto del pipeline (preprocesamiento, vectorización, modelo, serialización) no requirió cambios.

### Por qué SQLite
- Permite al Back-End consultar, insertar y filtrar contenidos sin parsear un CSV manualmente.
- Soporta queries SQL estándar (`SELECT`, `INSERT`, `WHERE categoria = ?`) directamente desde Java (JDBC) o Python.
- Es un archivo único (`techmind.db`) — no requiere servidor, fácil de subir a OCI Object Storage.
- La tabla queda preparada para recibir nuevos registros vía `POST /contenido` sin necesidad de reescribir el archivo CSV.

---

## [0.2.0] — 2026-07-15 · MVP del Hackathon

### Añadido
- **Pipeline de inferencia end-to-end** — función `procesar_contenido(titulo, texto)` que encadena limpieza → vectorización → clasificación → extracción de keywords y devuelve un dict JSON-serializable listo para el contrato REST.
- **Extracción de palabras clave** (campo `informaciones_adicionales`) mediante los términos con mayor peso TF-IDF dentro del documento individual, desacoplada de la predicción de categoría.
- **Tres ejemplos de uso documentados** en el notebook (Backend / Data Science / DevOps) como requisito obligatorio del MVP.
- **Serialización de artefactos** — `tfidf_vectorizer.joblib` y `modelo_clasificador.joblib` guardados con `joblib`, más celda de validación de carga que simula el arranque de la API.
- **Notas de integración** en la última sección del notebook (Celda 28): pasos para subir a OCI Object Storage y opciones de arquitectura (microservicio Python vs. exportación al formato Java).
- **Contrato de respuesta acordado** — campo renombrado a `informaciones_adicionales` (plural) para alinear con el equipo de Back-End:
  ```json
  {
    "categoria": "Backend",
    "probabilidad": 0.2779,
    "informaciones_adicionales": ["boot", "spring boot", "spring", "creación apis", "java spring"]
  }
  ```

### Cambiado
- El campo de salida originalmente denominado `informacion_adicional` (singular, según el PDF de la consigna) fue renombrado a `informaciones_adicionales` (plural) para coincidir con el contrato que usa el equipo de Back-End.

---

## [0.1.0] — 2026-07-14 · Construcción del pipeline base

### Añadido
- **Dataset sintético** `contenidos_tecnicos.csv` — ~60 registros en español, con campos `titulo`, `texto` y `categoria`, repartidos en 8 categorías: Backend, Frontend, Data Science, DevOps, Mobile, Bases de Datos, Seguridad y Cloud.
- **EDA inicial** — gráfico de distribución de categorías (countplot), histograma de longitud de textos (en palabras), chequeo de nulos y filas duplicadas.
- **Preprocesamiento de texto** — función `limpiar_texto(texto)`: minúsculas → remoción de puntuación (regex) → filtrado de stopwords en español (lista propia de ~30 términos, incluidos frases funcionales como "se explica", "se presenta").
- **Vectorización TF-IDF** — `TfidfVectorizer` con `max_features=1500`, `ngram_range=(1, 2)` y `min_df=1` para capturar unigramas y bigramas (p. ej. "api rest", "machine learning").
- **Modelo de clasificación** — Regresión Logística con `class_weight="balanced"` y `max_iter=1000`, entrenada sobre split train/test estratificado (75/25, `random_state=42`).
- **Evaluación del modelo** — accuracy, `classification_report` por categoría (precision / recall / F1) y matriz de confusión (heatmap con Seaborn).
  - Accuracy reportado sobre el test set actual: **~0.69** (orientativo; refleja las limitaciones del dataset pequeño).
  - Categorías con peor generalización: **DevOps** y **Seguridad** (menos ejemplos de entrenamiento).

---

## [0.0.1] — 2026-07-13 · Scaffolding inicial

### Añadido
- Estructura base del notebook `TechMind_DataScience.ipynb` con secciones enumeradas (EDA → Preprocesamiento → Vectorización → Modelo → Evaluación → Keywords → Inferencia → Serialización).
- Definición del alcance y rol del componente de Ciencia de Datos dentro del equipo (ver `detalle_trabajo.md`).
- Primeras dependencias identificadas: `pandas`, `scikit-learn`, `matplotlib`, `seaborn`, `joblib`, `re`, `json`, `numpy`.

---

*Mantenido por el equipo completo — TechMind G9 LATAM Team 37. Última actualización: 2026-08-08.*
