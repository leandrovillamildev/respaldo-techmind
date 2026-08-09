"""
verify_schema.py  —  TechMind · Verificación de esquema PostgreSQL
==================================================================

Utilidad para que el equipo de QA valide el estado de la base de datos
antes de ejecutar la suite de pruebas.

Verifica:
  • Conexión a PostgreSQL
  • Existencia de tablas requeridas
  • Nombres exactos de columnas (detecta typos como espacios vs guiones bajos)
  • Tipos de datos de las columnas
  • Existencia de índices

Uso:
    python3 verify_schema.py
    python3 verify_schema.py --fix    # intenta corregir columnas con nombre incorrecto
"""

import os
import sys
import argparse
from dotenv import load_dotenv

import psycopg2

load_dotenv()

# ── Esquema esperado ──────────────────────────────────────────────────────────

EXPECTED_SCHEMA = {
    "contenidos": {
        "columns": {
            "id":         "integer",
            "titulo":     "text",
            "texto":      "text",
            "categoria":  "text",
            "created_at": "timestamp with time zone",
        },
        "indexes": [
            "idx_contenidos_categoria",
        ],
    },
    "predicciones": {
        "columns": {
            "id":                        "integer",
            "titulo":                    "text",
            "texto":                     "text",
            "categoria":                 "text",
            "probabilidad":              "double precision",
            "informaciones_adicionales": "ARRAY",
            "created_at":                "timestamp with time zone",
        },
        "indexes": [
            "idx_predicciones_categoria",
            "idx_predicciones_fecha",
        ],
    },
}

# Mapeo de columnas renombradas conocidas (nombre_viejo -> nombre_correcto)
KNOWN_RENAMES = {
    "predicciones": {
        "informaciones adicionales": "informaciones_adicionales",
    }
}

# ─────────────────────────────────────────────────────────────────────────────

def get_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=int(os.getenv("PG_PORT", 5432)),
        dbname=os.getenv("PG_DB", "techmind"),
        user=os.getenv("PG_USER", "techmind_user"),
        password=os.getenv("PG_PASSWORD", "techmind_pass"),
    )


def check_connection() -> bool:
    print("\n🔌  Verificando conexión a PostgreSQL...")
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print(f"    ✅  Conectado — {version.split(',')[0]}")
        cur.close()
        con.close()
        return True
    except Exception as e:
        print(f"    ❌  No se pudo conectar: {e}")
        print("    ℹ️   Verificá que Docker esté corriendo: docker-compose up -d")
        return False


def get_actual_columns(cur, table: str) -> dict:
    """Retorna {nombre_columna: tipo_dato} para la tabla dada."""
    cur.execute(
        """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position;
        """,
        (table,),
    )
    return {row[0]: row[1] for row in cur.fetchall()}


def get_actual_indexes(cur, table: str) -> list:
    """Retorna la lista de nombres de índices para la tabla dada."""
    cur.execute(
        """
        SELECT indexname
        FROM pg_indexes
        WHERE schemaname = 'public' AND tablename = %s;
        """,
        (table,),
    )
    return [row[0] for row in cur.fetchall()]


def check_table(cur, table: str, expected: dict, fix: bool) -> bool:
    """
    Verifica columnas e índices de una tabla.
    Si fix=True, intenta renombrar columnas conocidas incorrectas.
    Retorna True si la tabla está OK (o fue corregida).
    """
    print(f"\n  📋  Tabla: {table}")

    actual_columns = get_actual_columns(cur, table)
    if not actual_columns:
        print(f"      ❌  Tabla '{table}' NO EXISTE en la base de datos.")
        return False

    ok = True

    # ── Verificar columnas ────────────────────────────────────────────────────
    for col_name, col_type in expected["columns"].items():
        if col_name in actual_columns:
            print(f"      ✅  {col_name:<35} ({actual_columns[col_name]})")
        else:
            # ¿Hay un nombre incorrecto conocido?
            known = KNOWN_RENAMES.get(table, {})
            wrong_name = next(
                (k for k, v in known.items() if v == col_name and k in actual_columns),
                None,
            )
            if wrong_name:
                print(f"      ⚠️   '{wrong_name}' debería llamarse '{col_name}'")
                if fix:
                    try:
                        cur.execute(
                            f'ALTER TABLE {table} RENAME COLUMN "{wrong_name}" TO {col_name};'
                        )
                        cur.connection.commit()
                        print(f"      🔧  Columna renombrada: '{wrong_name}' → '{col_name}'")
                    except Exception as e:
                        print(f"      ❌  No se pudo renombrar: {e}")
                        ok = False
                else:
                    print(f"           Corregí con --fix o ejecutá manualmente:")
                    print(f"           ALTER TABLE {table} RENAME COLUMN \"{wrong_name}\" TO {col_name};")
                    ok = False
            else:
                print(f"      ❌  Columna FALTANTE: '{col_name}' (tipo esperado: {col_type})")
                ok = False

    # Columnas extra (no esperadas)
    extra = set(actual_columns.keys()) - set(expected["columns"].keys())
    for col in extra:
        print(f"      ℹ️   Columna extra (no esperada): '{col}'")

    # ── Verificar índices ─────────────────────────────────────────────────────
    actual_idx = get_actual_indexes(cur, table)
    for idx in expected.get("indexes", []):
        if idx in actual_idx:
            print(f"      ✅  índice: {idx}")
        else:
            print(f"      ⚠️   índice FALTANTE: {idx} (no crítico)")

    return ok


def main():
    parser = argparse.ArgumentParser(
        description="TechMind — Verificación de esquema PostgreSQL para QA",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Intentar corregir automáticamente columnas con nombre incorrecto",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  🧪  TechMind — Verificación de Esquema PostgreSQL")
    print("=" * 60)

    if not check_connection():
        sys.exit(1)

    try:
        con = get_connection()
        cur = con.cursor()
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        sys.exit(1)

    all_ok = True
    print("\n📊  Verificando tablas y columnas...")

    for table, expected in EXPECTED_SCHEMA.items():
        result = check_table(cur, table, expected, fix=args.fix)
        if not result:
            all_ok = False

    cur.close()
    con.close()

    print("\n" + "=" * 60)
    if all_ok:
        print("  ✅  Esquema verificado — todo en orden. La suite puede ejecutarse.")
    else:
        print("  ❌  Se encontraron problemas en el esquema.")
        print("  ℹ️   Ejecutá con --fix para corregir automáticamente:")
        print("       python3 verify_schema.py --fix")
    print("=" * 60 + "\n")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
