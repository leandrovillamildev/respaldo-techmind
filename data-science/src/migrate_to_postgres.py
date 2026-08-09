"""
migrate_to_postgres.py
Migra el dataset de entrenamiento de TechMind a PostgreSQL.

Lee el dataset desde contenidos_tecnicos.csv e inserta los registros
en la tabla `contenidos` de PostgreSQL.

⚠️  ORDEN CORRECTO DE ARRANQUE (BUG-7 — resuelto 2026-07-27):
Este script debe ejecutarse DESPUÉS de que Spring Boot haya levantado
al menos una vez, porque Flyway (Spring Boot) es quien crea las tablas
con el schema correcto (BIGSERIAL para id, sin columna categoria, etc.).

    1. docker-compose up -d                      # PostgreSQL
    2. cd backend/api && ./mvnw spring-boot:run  # Flyway crea tablas
    3. python3 data-science/src/migrate_to_postgres.py  # inserta datos
    4. uvicorn app.main:app --port 8000          # FastAPI

NOTA (BUG-6 — resuelto 2026-07-27):
Este script NO crea ni modifica la tabla `predicciones`.
Esa responsabilidad es exclusiva de Flyway (Spring Boot).

Uso:
    cp .env.example .env        # configurar credenciales
    python3 data-science/src/migrate_to_postgres.py
"""

import csv
import os
from datetime import datetime, timezone
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv()

BASE_DIR  = Path(__file__).parent
CSV_PATH  = BASE_DIR.parent / "data" / "raw" / "contenidos_tecnicos.csv"


# ── 1. Conexión a PostgreSQL ──────────────────────────────────────────────────

def get_pg_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=int(os.getenv("PG_PORT", 5432)),
        dbname=os.getenv("PG_DB", "techmind"),
        user=os.getenv("PG_USER", "techmind_user"),
        password=os.getenv("PG_PASSWORD", "techmind_pass"),
    )


pg_con = get_pg_connection()
pg_cur = pg_con.cursor()

# ── Verificar que Flyway ya creó la tabla contenidos ─────────────────────────
# (BUG-7: si ejecutamos antes que Spring Boot, el schema sería incorrecto)
pg_cur.execute("""
    SELECT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'contenidos'
    );
""")
tabla_existe = pg_cur.fetchone()[0]

if not tabla_existe:
    print("❌  La tabla 'contenidos' no existe en PostgreSQL.")
    print("")
    print("   Este script debe ejecutarse DESPUÉS de que Spring Boot haya")
    print("   levantado al menos una vez (Flyway crea las tablas).")
    print("")
    print("   Orden correcto:")
    print("   1. docker-compose up -d")
    print("   2. cd backend/api && ./mvnw spring-boot:run  (esperar inicio)")
    print("   3. python3 data-science/src/migrate_to_postgres.py")
    print("   4. uvicorn app.main:app --port 8000")
    pg_cur.close()
    pg_con.close()
    exit(1)

print("✅  Tabla 'contenidos' verificada (schema creado por Flyway)")


# ── 3. Leer registros de la fuente disponible ─────────────────────────────────

rows = []
timestamp = datetime.now(timezone.utc).isoformat()

print(f"📂  Leyendo dataset desde CSV: {CSV_PATH.name}")
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["titulo"].strip():
            rows.append((row["titulo"].strip(), row["texto"].strip(), row["categoria"].strip(), timestamp))

print(f"    {len(rows)} registros leídos")


# ── 4. Verificar si ya hay datos en PostgreSQL ────────────────────────────────

pg_cur.execute("SELECT COUNT(*) FROM contenidos")
existing = pg_cur.fetchone()[0]

if existing > 0:
    print(f"\n⚠️  La tabla 'contenidos' ya tiene {existing} registros.")
    resp = input("   ¿Querés reemplazarlos? (s/N): ").strip().lower()
    if resp != "s":
        print("   Migración cancelada — datos existentes conservados.")
        pg_cur.close()
        pg_con.close()
        exit(0)
    pg_cur.execute("TRUNCATE TABLE contenidos RESTART IDENTITY CASCADE")
    pg_con.commit()
    print("   Tabla vaciada.")


# ── 5. Insertar registros ─────────────────────────────────────────────────────────
# NOTA: la columna `categoria` del CSV no se inserta porque el schema de Flyway
# para `contenidos` no la incluye (es solo titulo, texto, created_at).
# La categoria la asigna el modelo ML en cada prediccion.

pg_cur.executemany(
    "INSERT INTO contenidos (titulo, texto) VALUES (%s, %s)",
    [(r[0], r[1]) for r in rows],
)
pg_con.commit()
print(f"✅  {len(rows)} registros insertados en PostgreSQL")


# ── 6. Verificación ───────────────────────────────────────────────────────────

print("\n📊  Registros insertados:")
pg_cur.execute("SELECT COUNT(*) FROM contenidos")
total = pg_cur.fetchone()[0]
print(f"    TOTAL: {total} registros en 'contenidos'")

print("\n🔍  Ejemplo — primeros 3 registros:")
pg_cur.execute("SELECT id, titulo FROM contenidos LIMIT 3")
for row in pg_cur.fetchall():
    print(f"    [{row[0]}] {row[1]}")

pg_cur.close()
pg_con.close()
print("\n✅  Migración a PostgreSQL completada.")
