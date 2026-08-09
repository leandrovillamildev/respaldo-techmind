"""
app/database.py
Módulo de conexión a PostgreSQL para el microservicio FastAPI de TechMind.

Lee las credenciales desde variables de entorno (.env).
"""

import os
import psycopg2


def get_connection():
    """Abre y devuelve una conexión a PostgreSQL usando las variables de entorno."""
    return psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=int(os.getenv("PG_PORT", 5432)),
        dbname=os.getenv("PG_DB", "techmind"),
        user=os.getenv("PG_USER", "techmind_user"),
        password=os.getenv("PG_PASSWORD", "techmind_pass"),
    )


def init_db():
    """
    Verifica la conexión a PostgreSQL al arrancar FastAPI.

    NOTA (BUG-5 — resuelto 2026-07-27):
    FastAPI ya NO crea ni gestiona la tabla `predicciones`.
    Esa tabla es responsabilidad exclusiva de Flyway (Spring Boot), que la
    crea con el schema correcto (contenido_id FK, palabras_clave TEXT, etc.).
    Crear la tabla desde aquí generaba un conflicto de schemas incompatibles.

    FastAPI solo persiste predicciones a través de log_prediccion(),
    que escribe en la tabla `predicciones` ya creada por Flyway.
    """
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT 1;
    """)
    cur.close()
    con.close()
    print("✅  Conexión a PostgreSQL verificada correctamente")


def get_predicciones(limit: int = 50):
    """
    Obtiene el historial de predicciones guardadas en PostgreSQL
    uniendo la tabla predicciones con contenidos por contenido_id.
    """
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute(
            """
            SELECT p.id, c.titulo, p.categoria, p.probabilidad, p.palabras_clave, p.created_at, c.texto
            FROM predicciones p
            JOIN contenidos c ON c.id = p.contenido_id
            ORDER BY p.created_at DESC
            LIMIT %s
            """,
            (limit,),
        )
        rows = cur.fetchall()
        cur.close()
        con.close()
        return [
            {
                "id": r[0],
                "titulo": r[1],
                "categoria": r[2],
                "probabilidad": round(float(r[3]), 2),
                "keywords": r[4].split(",") if r[4] else [],
                "created_at": r[5].isoformat() + "Z" if r[5] else "",
                "texto": r[6] if r[6] else ""
            }
            for r in rows
        ]
    except Exception as exc:
        print(f"⚠️ Error al obtener predicciones de PostgreSQL: {exc}")
        return []


def delete_prediccion(prediccion_id: int) -> bool:
    """
    Elimina en cascada una predicción y su contenido asociado de PostgreSQL por ID.
    Retorna True si fue eliminada correctamente, False si no se encontró.
    """
    try:
        con = get_connection()
        cur = con.cursor()

        cur.execute("SELECT contenido_id FROM predicciones WHERE id = %s;", (prediccion_id,))
        row = cur.fetchone()
        if not row:
            cur.close()
            con.close()
            return False

        contenido_id = row[0]

        cur.execute("DELETE FROM predicciones WHERE id = %s;", (prediccion_id,))
        if contenido_id:
            cur.execute("DELETE FROM contenidos WHERE id = %s;", (contenido_id,))

        con.commit()
        cur.close()
        con.close()
        return True
    except Exception as exc:
        print(f"⚠️ Error al eliminar predicción ID {prediccion_id} de PostgreSQL: {exc}")
        if 'con' in locals() and con:
            try:
                con.rollback()
                con.close()
            except Exception:
                pass
        return False



def get_analytics_data(tz_offset_minutes: int = 0):
    """
    Agrupa estadísticas visuales de la base de datos PostgreSQL:
    - KPIs (total predicciones, categoría líder, avg probabilidad)
    - Conteo por categoría (Doughnut chart)
    - Conteo por hora del día 00-23 adaptado a la zona horaria del usuario (Area chart)
    - Top 15 palabras clave más frecuentes (Tag cloud)
    """
    try:
        con = get_connection()
        cur = con.cursor()

        # 1. Total & Avg Prob
        cur.execute("SELECT COUNT(*), AVG(probabilidad) FROM predicciones;")
        tot_row = cur.fetchone()
        total_count = tot_row[0] if tot_row and tot_row[0] else 0
        avg_prob = round(float(tot_row[1]) * 100, 1) if tot_row and tot_row[1] else 0.0

        # 2. Categorías
        cur.execute("""
            SELECT categoria, COUNT(*) AS total
            FROM predicciones
            GROUP BY categoria
            ORDER BY total DESC;
        """)
        cat_rows = cur.fetchall()
        categorias = {r[0]: r[1] for r in cat_rows}
        top_categoria = cat_rows[0][0] if cat_rows else "N/A"

        # 3. Horas del día (00 a 23) ajustadas a la zona horaria del usuario
        cur.execute(
            """
            SELECT EXTRACT(HOUR FROM (created_at + (%s || ' minutes')::interval))::int AS hora, COUNT(*)
            FROM predicciones
            WHERE created_at IS NOT NULL
            GROUP BY hora
            ORDER BY hora;
            """,
            (tz_offset_minutes,),
        )
        hour_rows = cur.fetchall()
        hour_dict = {r[0]: r[1] for r in hour_rows}
        horas = [hour_dict.get(h, 0) for h in range(24)]

        # 4. Top Keywords (normalizado a minúsculas y desduplicado por documento)
        cur.execute("SELECT palabras_clave FROM predicciones WHERE palabras_clave IS NOT NULL AND palabras_clave != '';")
        kw_rows = cur.fetchall()
        STOPWORDS_IGNORE = {
            "mediante", "globalmente", "además", "ademas", "través", "traves", "debido", "según", "segun",
            "cada", "forma", "manera", "principalmente", "especialmente", "actualmente", "diferentes",
            "varios", "varias", "asimismo", "generalmente", "realmente", "nivel", "tipo", "tipos",
            "parte", "partes", "medio", "medios", "modo", "modos", "hacer", "hace", "hacen", "haciendo",
            "realizar", "realiza", "realizan", "realizando", "permite", "permiten", "permitiendo",
            "tutorial", "guia", "guía", "introduccion", "introducción", "explicacion", "explicación",
            "concepto", "conceptos", "basico", "básicos", "basicos", "básica", "basica", "avanzado",
            "avanzada", "desarrollo", "creacion", "creación", "uso", "usando", "ejemplo", "ejemplos"
        }
        kw_counts = {}
        for row in kw_rows:
            raw_text = row[0].replace("[", "").replace("]", "").replace('"', '').replace("'", "")
            words = set([
                w.strip().lower() for w in raw_text.split(",")
                if w.strip() and len(w.strip()) > 2 and w.strip().lower() not in STOPWORDS_IGNORE
            ])
            for w in words:
                kw_counts[w] = kw_counts.get(w, 0) + 1

        top_kw = sorted(kw_counts.items(), key=lambda x: x[1], reverse=True)[:15]

        cur.close()
        con.close()

        return {
            "total_count": total_count,
            "avg_prob": avg_prob,
            "top_categoria": top_categoria,
            "categorias": categorias,
            "horas": horas,
            "top_keywords": [{"word": k[0], "count": k[1]} for k in top_kw]
        }
    except Exception as exc:
        print(f"⚠️ Error al generar analytics desde PostgreSQL: {exc}")
        return {
            "total_count": 0,
            "avg_prob": 0.0,
            "top_categoria": "Sin datos",
            "categorias": {},
            "horas": [0] * 24,
            "top_keywords": []
        }



