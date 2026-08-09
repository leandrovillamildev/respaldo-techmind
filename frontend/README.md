# 🎨 TechMind — Módulo Frontend

> Interfaz web interactiva **Cyber AI Dark Mode** (Glassmorphism) construida en HTML + JavaScript Vanilla + Tailwind CSS CDN. Se comunica dinámicamente con la API REST de Spring Boot (`:8080`) y el microservicio FastAPI ML (`:8000`).

---

## 🏗️ Estructura del Módulo

```
frontend/
├── index.html   # Estructura DOM, estilos Tailwind inline y tokens de diseño CSS custom
├── app.js       # Toda la lógica cliente: i18n, auth, health checks, SPA routing, charts
├── Dockerfile   # Nginx Alpine para servir el frontend en producción
└── README.md    # Este archivo
```

---

## ✨ Funcionalidades Principales

### 1. Navegación SPA (Single Page Application)
La UI opera como una SPA con tres vistas que se ocultan/muestran sin recargar la página:

| Vista | Ruta interna | Descripción |
|---|---|---|
| **Clasificador** | `#classifier-view-section` | Formulario de ingesta y resultado del modelo |
| **Historial** | `#history-view-section` | Lista detallada con búsqueda y filtro por categoría |
| **Análisis** | `#analytics-view-section` | Dashboard con KPIs y gráficos Chart.js |

### 2. Indicadores de Estado en Tiempo Real
LEDs pulsantes en el sidebar verificando la salud de cada servicio:
- **Spring Boot :8080** → `GET /actuator/health` → `{"status":"UP"}`
- **FastAPI ML :8000** → `GET /health` → `{"status":"ok"}`
- **PostgreSQL :5432** → estado inferido vía FastAPI

El popover de "Estado de servicios" también muestra métricas del servidor OCI en tiempo real: CPU, RAM usada/libre, Swap y Uptime (polling cada 10 s vía `GET /system-stats`).

### 3. Clasificador de Contenido Técnico
- Campos para **Título** y **Contenido técnico** (texto crudo, markdown o resumen).
- Botón **"Clasificar con TechMind"** con estado de carga animado.
- Botón **"Limpiar formulario"** para vaciar los campos.
- Resultado: badge de categoría con color e ícono único, barra de confianza animada y tags de palabras clave TF-IDF.
- Botón **"Ver JSON"** que abre un modal con el payload completo (entrada + inferencia) y función de **Copiar al Portapapeles**.

### 4. Historial de Consultas
- Vista compacta en grid (3 columnas en desktop) en la sección inferior del Clasificador.
- Vista detallada con buscador de texto libre y filtro desplegable por categoría (con conteo real por categoría).
- Botones **"Ver más / Ver menos"** para expandir descripciones largas.
- Botones **"Ver JSON"** por entrada para inspeccionar el payload completo.
- Botones **"Borrar"** visibles únicamente cuando hay sesión de administrador activa.

### 5. Dashboard de Análisis (Chart.js)
- **3 KPI cards:** Total Clasificaciones, Categoría Líder, Confianza Promedio.
- **Doughnut Chart:** Distribución porcentual por categoría técnica.
- **Area Line Chart:** Actividad de consultas por hora del día (24 h, ajustado a UTC del navegador).
- **Nube de palabras clave:** Badges/pills interactivos con frecuencia de aparición.
- Los gráficos se re-renderizan automáticamente al cambiar entre modo claro y oscuro.

### 6. Autenticación de Administrador
- Botón **"Iniciar sesión"** en el header → abre modal con usuario y contraseña.
- Credenciales validadas contra `POST /auth/login` de FastAPI (token Bearer en `sessionStorage`).
- Al estar logueado aparece el popover con nombre del usuario, badge "Sesión Activa" y botón **"Cerrar Sesión"**.
- Los botones de borrado de predicciones solo son visibles con sesión activa.

### 7. Internacionalización (i18n) — Español / English
- Botón `🌐 EN / ES` junto al botón de Admin para alternar idiomas instantáneamente.
- **67 claves de traducción** cubriendo toda la UI estática y dinámica.
- Preferencia persistida en `localStorage`.
- El contenido dinámico visible (historial, analytics) se refresca automáticamente al cambiar de idioma.

### 8. Tema Claro / Oscuro
- Toggle en el sidebar con persistencia en `localStorage`.
- El modo inicial se lee desde `localStorage` antes del primer render para evitar flash.

### 9. Sidebar Responsivo
- **Desktop:** colapsable a icon rail (64 px), expandible a 256 px. Estado persistido en `localStorage`.
- **Mobile:** panel overlay activado con botón hamburger `☰`.
- Al hacer clic en cualquier ícono de navegación o en el LED de estado mientras el sidebar está colapsado, se expande automáticamente.

---

## 🔌 Configuración de API

El frontend detecta el entorno automáticamente según `window.location.hostname`:

| Entorno | Spring Boot | FastAPI |
|---|---|---|
| `localhost` | `http://localhost:8080` | `http://localhost:8000` |
| Producción (OCI) | `http://<IP_OCI>:8080` | `http://<IP_OCI>:8000` |

La lógica de selección de endpoint está en las primeras líneas de [`app.js`](./app.js).

---

## 🚀 Ejecución Local

```bash
# Servidor Python simple en el puerto 5173
python3 -m http.server 5173 --directory frontend
```

👉 **[http://localhost:5173](http://localhost:5173)**

### Con Docker (producción)
```bash
docker compose --profile full up -d --build
```
El servicio `frontend` se sirve vía **Nginx Alpine** en el puerto `80`.

---

## 🗂️ Indicadores de Estado HTTP

| Servicio | Endpoint de Health Check | Respuesta esperada |
|---|---|---|
| Spring Boot | `GET :8080/actuator/health` | `{"status":"UP"}` |
| FastAPI | `GET :8000/health` | `{"status":"ok"}` |
| Métricas OCI | `GET :8000/system-stats` | JSON con CPU, RAM, Swap, Uptime |

---

*Módulo mantenido por el equipo TechMind G9 LATAM Team 37. Última actualización: 2026-08-08.*
