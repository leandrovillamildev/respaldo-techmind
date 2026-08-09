# 🔧 Fix — BUG-03: Indicadores de estado congelados en rojo al iniciar la aplicación

**Fecha:** 30 de Julio de 2026   
**Reportado por:** QA — Federico G. Gutierrez  
**Resuelto por:** Equipo Data Science, Backend y Full Stack  
**Estado:** ✅ Resuelto

---

## ❓ ¿Qué pasaba?
Al iniciar la aplicación web en el navegador, los indicadores de estado (LEDs) de los servicios backend (`Spring Boot :8080` y `FastAPI ML :8000`) dentro del panel de la barra lateral permanecían en color rojo (no disponibles), a pesar de que los contenedores en el backend ya estaban arriba y operativos.

El usuario se veía obligado a presionar F5 (recarga manual) para que el cliente web refrescara los health checks y mostrara los LEDs en verde.

---

## 🔍 Causa raíz
El problema tuvo dos factores de origen (Cliente + Infraestructura):
1. Falta de Polling en Frontend: La función de chequeo de estado (`checkServerStatus`) solo se ejecutaba una única vez al momento de cargar el script, sin reintentos automáticos si la API demoraba unos segundos adicionales en responder.
2. Saturación de Recursos en Servidor: El entorno de despliegue inicial contaba con recursos de hardware acotados, provocando retrasos en la respuesta de los endpoints `/health` de Spring Boot y FastAPI durante la inicialización de la app.

---

## ✅ ¿Necesito recrear la base de datos?
**Si.** Se desplegó una nueva instancia dedicada con mayores capacidades para garantizar disponibilidad continua y tiempos de respuesta ultra-bajos.

---

## 🛠️ Pasos para aplicar el fix

### Paso 1 — Migración de Entorno de Despliegue (DevOps)
Se aprovisionó una nueva instancia de servidor con las siguientes especificaciones:
- Recursos: 4 vCPU / 32 GB RAM.
- Nueva Dirección de Acceso: [http://163.176.183.89:5173/](http://163.176.183.89:5173/)

### Paso 2 — Implementación de Health Check Polling en Frontend (`app.js`)
Se incorporó un temporizador de verificación periódica y reintentos automáticos durante los primeros segundos del ciclo de vida del sitio web:

```
// Verificar estado inmediatamente y establecer polling cada 10 segundos
function initHealthCheckPolling() {
    checkServicesHealth(); // Ejecución inicial
    setInterval(checkServicesHealth, 10000); // Polling automático
}

document.addEventListener('DOMContentLoaded', initHealthCheckPolling);
```

## 📋 Checklist de verificación para QA

Antes de ejecutar la suite de pruebas, seguir este orden:

- [ ] Acceder a la nueva URL de la aplicación: [http://163.176.183.89:5173/](http://163.176.183.89:5173/).
- [ ] Abrir el menú o popover de "Estado de servicios" en la barra lateral nada más cargar la página.
- [ ] Verificar que los LEDs de `Spring Boot :8080`, `FastAPI ML :8000` y `PostgreSQL :5432` se sincronicen automáticamente a verde (operativo) sin necesidad de forzar un F5.
- [ ] Dejar la pestaña abierta durante 30 segundos y verificar en las DevTools (`Network`) que el polling `/health` se mantiene ejecutando en segundo plano de forma no bloqueante.

---

_Documentación generada por el Equipo Data Science, Backend y Full Stack — TechMind · Sprint 4_
