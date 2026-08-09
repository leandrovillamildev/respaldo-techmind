# 🔧 Fix — Soporte Multi-Arquitectura (ARM64 / AMD64) en Dockerfile de Spring Boot

**Fecha:** 29 de Julio de 2026  
**Reportado por:** Equipo de Desarrollo / QA (macOS Apple Silicon)  
**Resuelto por:** Equipo TechMind  
**Estado:** ✅ Resuelto  

---

## ❓ ¿Qué pasaba?

Al ejecutar el instalador automatizado en un sistema macOS con procesador Apple Silicon (M1/M2/M3/M4):

```bash
python3 setup.py --docker
```

La compilación de la pila Docker abortaba en el paso de Spring Boot con el siguiente error:

```text
ERROR [springboot internal] load metadata for docker.io/library/eclipse-temurin:17-jdk-alpine:
target springboot: failed to solve: eclipse-temurin:17-jdk-alpine: failed to resolve source metadata for docker.io/library/eclipse-temurin:17-jdk-alpine: no match for platform in manifest: not found
```

---

## 🔍 Causa raíz

La imagen base [backend/Dockerfile](file:///Users/ernesto/Documents/GitHub/g9-latam-techmind-team37/backend/Dockerfile) utilizaba la variante Alpine de JDK 17:

```dockerfile
FROM eclipse-temurin:17-jdk-alpine AS build
...
FROM eclipse-temurin:17-jre-alpine
```

En Docker Hub, la distribución `eclipse-temurin:17-jdk-alpine` únicamente contiene manifiestos para la arquitectura **`linux/amd64`** (Intel/AMD x86_64). Cuando Docker Desktop en macOS intenta construir la imagen utilizando la arquitectura nativa **`linux/arm64`**, Docker Hub devuelve un error indicando que no existe esa plataforma en el manifiesto de la imagen.

En sistemas Windows / Linux x86_64 el proceso funcionaba correctamente porque la arquitectura coincidente es `amd64`.

---

## ✅ Solución aplicada

Se cambiaron las imágenes base en `backend/Dockerfile` a las versiones estándar multi-arquitectura de **Eclipse Temurin (Adoptium)**:

```diff
# Dockerfile — Backend Spring Boot Java 17 (TechMind)
-FROM eclipse-temurin:17-jdk-alpine AS build
+FROM eclipse-temurin:17-jdk AS build
 WORKDIR /app

 ...

-FROM eclipse-temurin:17-jre-alpine
+FROM eclipse-temurin:17-jre
 WORKDIR /app
```

---

## 🚀 Beneficios

1. **Soporte Nativo Multi-Plataforma:** Las etiquetas `eclipse-temurin:17-jdk` y `17-jre` disponen de manifiestos multi-arch nativos (`linux/amd64` y `linux/arm64`).
2. **Compatibilidad total con macOS:** Funciona sin errores de manifest en procesadores Apple Silicon (M1/M2/M3/M4).
3. **Compatibilidad con Windows y Linux:** Mantiene el funcionamiento 100% idéntico en entornos Windows/AMD64.
4. **Preparado para OCI (Oracle Cloud Infrastructure):** Permite hacer deploy sin cambios en instancias Intel/AMD o instancias ARM64 (Ampere A1).
