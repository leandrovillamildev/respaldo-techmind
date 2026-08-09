# 🔧 Fix — Columna `informaciones_adicionales` en tabla `predicciones`

**Fecha:** 24 de Julio de 2026  
**Reportado por:** QA — Federico G. Gutierrez  
**Resuelto por:** Equipo Data Science  
**Estado:** ✅ Resuelto

---

## ❓ ¿Qué pasaba?

Al intentar guardar una predicción en la base de datos, aparecía este error en consola:

```
Error al guardar predicción en PostgreSQL:
column "informaciones adicionales" of relation "predicciones" does not exist
```

La API seguía respondiendo correctamente al cliente (la predicción se devolvía igual), pero **el registro no se guardaba en la base de datos**.

---

## 🔍 Causa raíz

La tabla `predicciones` fue creada con el nombre de columna **incorrecto** (con espacio):

| | Nombre de columna |
|---|---|
| ❌ Como estaba en la DB | `informaciones adicionales` (con espacio) |
| ✅ Como debe estar | `informaciones_adicionales` (con guión bajo) |

El código Python siempre estuvo correcto. El problema era únicamente el estado de la base de datos.

> **¿Por qué el script de creación no lo corrigió solo?**  
> Porque usa `CREATE TABLE IF NOT EXISTS` — si la tabla ya existe, no la vuelve a crear ni modifica sus columnas. El schema incorrecto quedó "congelado".

---

## ✅ ¿Necesito recrear la base de datos?

**No.** No se pierden datos. El fix es un simple renombrado de columna.

---

## 🛠️ Pasos para aplicar el fix

> ⚠️ Ejecutar **una sola vez** en el entorno donde corre Docker.

### Paso 1 — Aplicar el fix

```bash
docker exec techmind-postgres psql -U techmind_user -d techmind -c \
  "ALTER TABLE predicciones RENAME COLUMN \"informaciones adicionales\" TO informaciones_adicionales;"
```

Resultado esperado:
```
ALTER TABLE
```

### Paso 2 — Verificar que quedó bien

```bash
docker exec techmind-postgres psql -U techmind_user -d techmind -c \
  "SELECT column_name FROM information_schema.columns WHERE table_name = 'predicciones';"
```

Resultado esperado (todas las columnas con nombre correcto):

```
       column_name        
--------------------------
 id
 titulo
 texto
 categoria
 probabilidad
 informaciones_adicionales   ← debe aparecer con guión bajo
 created_at
```

### Paso 3 — Verificación con el script de QA (recomendado)

```bash
python3 data-science/src/verify_schema.py
```

Resultado esperado:
```
============================================================
  🧪  TechMind — Verificación de Esquema PostgreSQL
============================================================

🔌  Verificando conexión a PostgreSQL...
    ✅  Conectado — PostgreSQL 16...

📊  Verificando tablas y columnas...

  📋  Tabla: contenidos
      ✅  id                      (integer)
      ✅  titulo                  (text)
      ✅  texto                   (text)
      ✅  categoria               (text)
      ✅  created_at              (timestamp with time zone)

  📋  Tabla: predicciones
      ✅  id                      (integer)
      ✅  titulo                  (text)
      ✅  texto                   (text)
      ✅  categoria               (text)
      ✅  probabilidad            (double precision)
      ✅  informaciones_adicionales (ARRAY)
      ✅  created_at              (timestamp with time zone)

============================================================
  ✅  Esquema verificado — todo en orden. La suite puede ejecutarse.
============================================================
```

---

## 📋 Checklist de arranque recomendado para QA (Sprint 2 en adelante)

Antes de ejecutar la suite de pruebas, seguir este orden:

- [ ] `docker-compose up -d` — levantar PostgreSQL
- [ ] `python3 data-science/src/verify_schema.py` — verificar schema ✅
- [ ] `uvicorn app.main:app --reload --port 8000` — iniciar FastAPI
- [ ] Ejecutar colección Postman

> Si `verify_schema.py` muestra errores, ejecutar:  
> `python3 data-science/src/verify_schema.py --fix`

---

## ❓ ¿Puede `informaciones_adicionales` ser una lista vacía `[]`?

**Sí, y es comportamiento válido.** No indica un fallo del pipeline.

Ocurre cuando el texto ingresado, luego de ser limpiado (minúsculas, stopwords removidas, caracteres especiales eliminados), no contiene ningún token con peso TF-IDF mayor a cero en el vocabulario entrenado.

| Campo | Comportamiento con texto muy corto/genérico |
|---|---|
| `categoria` | ✅ Se calcula igual, siempre presente |
| `probabilidad` | ✅ Se calcula igual, siempre entre 0 y 1 |
| `informaciones_adicionales` | ⚠️ Puede ser `[]` — válido por diseño |

**Ejemplo de payload que produce `[]` en keywords:**
```json
{
  "titulo": "ok",
  "texto": "el la los un de del al a en"
}
```
La API responde HTTP 200 correctamente, con `informaciones_adicionales: []`.

---

_Documentación generada por el Equipo Data Science — TechMind · Sprint 1_
