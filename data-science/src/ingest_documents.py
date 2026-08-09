"""
ingest_documents.py  —  TechMind · Ingesta de documentos PDF / DOCX
=====================================================================

Carga documentos técnicos en la tabla `contenidos` de PostgreSQL
para ampliar el dataset de entrenamiento del modelo.

Uso básico:
    python3 ingest_documents.py                         # procesa carpeta ./documentos/
    python3 ingest_documents.py --carpeta ./mis_docs/   # carpeta personalizada
    python3 ingest_documents.py --archivo guia.pdf --categoria DevOps  # archivo único

Modo "multi-categoría" (PDF que cubre varios temas):
    El script detecta automáticamente si querés dividir el documento
    en secciones y asignarle una categoría diferente a cada una.

Flujo:
    1. Escanear carpeta buscando *.pdf y *.docx
    2. Extraer texto completo
    3. Limpiar (saltos de página, headers repetidos, líneas vacías)
    4. Mostrar preview → pedir categoría al usuario (Opción A — manual)
    5. Preguntar si dividir en secciones (para docs multi-categoría)
    6. Verificar duplicados (hash MD5 del texto)
    7. Insertar en PostgreSQL
    8. Al final: mostrar resumen y recordatorio de re-entrenamiento

Cuándo re-entrenar:
    Después de agregar ~20 documentos nuevos o cuando alguna categoría
    gane 5+ registros. Comando: jupyter nbconvert --execute TechMind_DataScience.ipynb
"""

import argparse
import hashlib
import os
import re
import sys
import textwrap
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# ── Dependencias opcionales (PDF / DOCX) ─────────────────────────────────────
try:
    import pdfplumber
    PDF_OK = True
except ImportError:
    PDF_OK = False

try:
    from docx import Document as DocxDocument
    DOCX_OK = True
except ImportError:
    DOCX_OK = False

# ── Constantes ────────────────────────────────────────────────────────────────
CATEGORIAS = [
    "Backend",
    "Frontend",
    "Data Science",
    "DevOps",
    "Mobile",
    "Bases de Datos",
    "Seguridad",
    "Cloud",
]

CARPETA_DEFAULT = Path(__file__).parent.parent.parent / "documentos"
UMBRAL_REENTRENAMIENTO = 3  # re-entrenar el modelo cada N documentos nuevos
NOTEBOOK_PATH = Path(__file__).parent.parent / "notebooks" / "TechMind_DataScience.ipynb"

# ─────────────────────────────────────────────────────────────────────────────
# 1. Conexión a PostgreSQL
# ─────────────────────────────────────────────────────────────────────────────

def get_connection():
    load_dotenv()
    return psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=int(os.getenv("PG_PORT", 5432)),
        dbname=os.getenv("PG_DB", "techmind"),
        user=os.getenv("PG_USER", "techmind_user"),
        password=os.getenv("PG_PASSWORD", "techmind_pass"),
    )

# ─────────────────────────────────────────────────────────────────────────────
# 2. Extracción de texto
# ─────────────────────────────────────────────────────────────────────────────

def extraer_pdf(ruta: Path) -> str:
    if not PDF_OK:
        print("  ⚠️  pdfplumber no instalado. Ejecutá: pip install pdfplumber")
        return ""
    try:
        texto = []
        with pdfplumber.open(ruta) as pdf:
            for pagina in pdf.pages:
                t = pagina.extract_text()
                if t:
                    texto.append(t)
        return "\n".join(texto)
    except Exception as e:
        print(f"  ❌ Error leyendo PDF: {e}")
        return ""


def extraer_docx(ruta: Path) -> str:
    if not DOCX_OK:
        print("  ⚠️  python-docx no instalado. Ejecutá: pip install python-docx")
        return ""
    try:
        doc = DocxDocument(ruta)
        parrafos = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(parrafos)
    except Exception as e:
        print(f"  ❌ Error leyendo DOCX: {e}")
        return ""


def extraer_texto(ruta: Path) -> str:
    ext = ruta.suffix.lower()
    if ext == ".pdf":
        return extraer_pdf(ruta)
    elif ext == ".docx":
        return extraer_docx(ruta)
    else:
        print(f"  ⚠️  Formato no soportado: {ext}")
        return ""

# ─────────────────────────────────────────────────────────────────────────────
# 3. Limpieza de texto
# ─────────────────────────────────────────────────────────────────────────────

def limpiar_texto(texto: str) -> str:
    # Normalizar saltos de línea
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    # Eliminar líneas que son solo números de página (ej: "- 12 -", "12", "Página 12")
    texto = re.sub(r"(?m)^[-–—\s]*[Pp][áa]gina\s*\d+[-–—\s]*$", "", texto)
    texto = re.sub(r"(?m)^\s*\d+\s*$", "", texto)
    # Colapsar líneas vacías múltiples en una sola
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    # Eliminar espacios al inicio/fin de cada línea
    lineas = [l.strip() for l in texto.split("\n")]
    texto = "\n".join(lineas)
    return texto.strip()

# ─────────────────────────────────────────────────────────────────────────────
# 4. Detección de secciones (para docs multi-categoría)
# ─────────────────────────────────────────────────────────────────────────────

def dividir_en_secciones(texto: str) -> list[dict]:
    """
    Divide el texto en secciones basándose en headings detectados heurísticamente.
    Un heading se detecta como una línea corta (<= 8 palabras) seguida de una línea en blanco.
    Devuelve lista de {"titulo": str, "texto": str}.
    """
    lineas = texto.split("\n")
    secciones = []
    titulo_actual = "Sección 1"
    buffer = []

    for i, linea in enumerate(lineas):
        palabras = linea.strip().split()
        es_heading = (
            1 <= len(palabras) <= 8
            and linea.strip() == linea.strip().capitalize()  # empieza con mayúscula
            and (i + 1 >= len(lineas) or lineas[i + 1].strip() == "")  # sigue línea vacía
            and len(linea.strip()) > 3
        )
        if es_heading and buffer:
            secciones.append({"titulo": titulo_actual, "texto": "\n".join(buffer).strip()})
            buffer = []
            titulo_actual = linea.strip()
        else:
            if linea.strip():
                buffer.append(linea)

    if buffer:
        secciones.append({"titulo": titulo_actual, "texto": "\n".join(buffer).strip()})

    # Si no detectó secciones, devolver el documento completo como una sola
    if not secciones:
        secciones = [{"titulo": "Documento completo", "texto": texto}]

    return [s for s in secciones if len(s["texto"].split()) > 20]  # filtrar secciones muy cortas

# ─────────────────────────────────────────────────────────────────────────────
# 5. Interacción con el usuario
# ─────────────────────────────────────────────────────────────────────────────

def mostrar_preview(texto: str, titulo_archivo: str, palabras: int = 60) -> None:
    preview = " ".join(texto.split()[:palabras])
    print(f"\n{'─' * 60}")
    print(f"  📄 {titulo_archivo}")
    print(f"{'─' * 60}")
    print(textwrap.fill(f"Preview: \"{preview}...\"", width=60, initial_indent="  "))
    print(f"  📊 {len(texto.split())} palabras totales")


def pedir_categoria(mensaje: str = "") -> str:
    print(f"\n  Categorías disponibles:")
    for i, cat in enumerate(CATEGORIAS, 1):
        print(f"    {i:2}. {cat}")
    if mensaje:
        print(f"\n  {mensaje}")
    while True:
        try:
            opcion = input("\n  ¿Categoría? [1-8] (o 's' para saltear): ").strip().lower()
            if opcion == "s":
                return ""
            idx = int(opcion) - 1
            if 0 <= idx < len(CATEGORIAS):
                return CATEGORIAS[idx]
            print("  ⚠️  Número fuera de rango.")
        except (ValueError, KeyboardInterrupt):
            print("\n  ⚠️  Ingresá un número del 1 al 8.")


def preguntar_si_no(pregunta: str) -> bool:
    resp = input(f"\n  {pregunta} [s/N]: ").strip().lower()
    return resp in ("s", "si", "sí", "y", "yes")

# ─────────────────────────────────────────────────────────────────────────────
# 6. Verificación de duplicados
# ─────────────────────────────────────────────────────────────────────────────

def hash_texto(texto: str) -> str:
    return hashlib.md5(texto.encode("utf-8")).hexdigest()


def es_duplicado(cur, texto: str) -> bool:
    """Verifica si un texto con el mismo hash ya existe en contenidos."""
    h = hash_texto(texto)
    cur.execute("SELECT 1 FROM contenidos WHERE MD5(texto) = %s LIMIT 1", (h,))
    return cur.fetchone() is not None

# ─────────────────────────────────────────────────────────────────────────────
# 7. Inserción en PostgreSQL
# ─────────────────────────────────────────────────────────────────────────────

def insertar_registro(cur, titulo: str, texto: str, categoria: str) -> bool:
    if not titulo.strip() or not texto.strip():
        return False
    cur.execute(
        "INSERT INTO contenidos (titulo, texto, categoria) VALUES (%s, %s, %s)",
        (titulo.strip()[:200], texto.strip(), categoria),
    )
    return True

# ─────────────────────────────────────────────────────────────────────────────
# 8. Procesamiento de un archivo
# ─────────────────────────────────────────────────────────────────────────────

def procesar_archivo(ruta: Path, con, cur, categoria_forzada: str = "") -> int:
    """
    Procesa un archivo PDF o DOCX.
    Devuelve el número de registros insertados.
    """
    print(f"\n{'═' * 60}")
    print(f"  📂 {ruta.name}")

    texto_raw = extraer_texto(ruta)
    if not texto_raw.strip():
        print("  ⚠️  No se pudo extraer texto — saltando.")
        return 0

    texto = limpiar_texto(texto_raw)
    titulo_base = ruta.stem.replace("_", " ").replace("-", " ").title()

    insertados = 0

    # ── Modo forzado (--categoria desde CLI) ──────────────────────────────────
    if categoria_forzada:
        mostrar_preview(texto, ruta.name)
        print(f"\n  Categoría asignada por parámetro: [{categoria_forzada}]")

        if es_duplicado(cur, texto):
            print("  ⚠️  Documento ya existe en la base de datos — saltando.")
            return 0

        if insertar_registro(cur, titulo_base, texto, categoria_forzada):
            con.commit()
            print(f"  ✅ Insertado: \"{titulo_base}\" → {categoria_forzada}")
            insertados += 1
        return insertados

    # ── Modo interactivo (Opción A) ───────────────────────────────────────────
    mostrar_preview(texto, ruta.name)

    # ¿Dividir en secciones?
    dividir = preguntar_si_no(
        "¿Este documento cubre MÚLTIPLES categorías y querés dividirlo en secciones?"
    )

    if dividir:
        secciones = dividir_en_secciones(texto)
        print(f"\n  📑 Se detectaron {len(secciones)} secciones:")
        for i, sec in enumerate(secciones, 1):
            preview_sec = " ".join(sec["texto"].split()[:12])
            print(f"    {i}. {sec['titulo'][:50]} — \"{preview_sec}...\"")

        for i, sec in enumerate(secciones, 1):
            print(f"\n  ── Sección {i}/{len(secciones)}: {sec['titulo'][:50]}")
            preview_corto = " ".join(sec["texto"].split()[:40])
            print(textwrap.fill(f"  \"{preview_corto}...\"", width=60, initial_indent="  "))

            cat = pedir_categoria()
            if not cat:
                print(f"  ⏭️  Sección {i} salteada.")
                continue

            titulo_sec = f"{titulo_base} — {sec['titulo']}"

            if es_duplicado(cur, sec["texto"]):
                print("  ⚠️  Esta sección ya existe en la base de datos — saltando.")
                continue

            if insertar_registro(cur, titulo_sec, sec["texto"], cat):
                con.commit()
                print(f"  ✅ Insertado: \"{titulo_sec[:60]}\" → {cat}")
                insertados += 1

    else:
        # Documento completo como un registro
        cat = pedir_categoria()
        if not cat:
            print("  ⏭️  Documento salteado.")
            return 0

        if es_duplicado(cur, texto):
            print("  ⚠️  Documento ya existe en la base de datos — saltando.")
            return 0

        if insertar_registro(cur, titulo_base, texto, cat):
            con.commit()
            print(f"  ✅ Insertado: \"{titulo_base}\" → {cat}")
            insertados += 1

    return insertados

# ─────────────────────────────────────────────────────────────────────────────
# 9. Resumen final y recordatorio de re-entrenamiento
# ─────────────────────────────────────────────────────────────────────────────

def mostrar_resumen(cur, insertados_sesion: int) -> None:
    print(f"\n{'═' * 60}")
    print(f"  📊 RESUMEN DE LA SESIÓN")
    print(f"{'─' * 60}")
    print(f"  Documentos/secciones insertados: {insertados_sesion}")

    cur.execute("SELECT COUNT(*) FROM contenidos")
    total = cur.fetchone()[0]
    print(f"  Total de registros en 'contenidos': {total}")

    print(f"\n  Distribución actual por categoría:")
    cur.execute(
        "SELECT categoria, COUNT(*) as n FROM contenidos GROUP BY categoria ORDER BY n DESC"
    )
    for cat, n in cur.fetchall():
        barra = "█" * min(n, 30)
        print(f"    {cat:<20} {n:3}  {barra}")

    print(f"\n{'─' * 60}")
    if insertados_sesion >= UMBRAL_REENTRENAMIENTO:
        print(f"  🔁 Se insertaron {insertados_sesion} documento(s) — umbral de re-entrenamiento alcanzado ({UMBRAL_REENTRENAMIENTO}).")
    else:
        restantes = UMBRAL_REENTRENAMIENTO - insertados_sesion
        print(f"  💡 Faltan {restantes} documento(s) más para activar el re-entrenamiento automático.")
    print(f"{'═' * 60}\n")


def reentrenar_modelo() -> bool:
    """
    Ejecuta el notebook completo para regenerar los .joblib.
    Devuelve True si el re-entrenamiento fue exitoso.
    """
    import subprocess
    if not NOTEBOOK_PATH.exists():
        print(f"  ❌ Notebook no encontrado: {NOTEBOOK_PATH}")
        return False

    # Buscar jupyter en conda o sistema
    jupyter_paths = [
        "/opt/anaconda3/bin/jupyter",
        "/usr/local/bin/jupyter",
        "jupyter",
    ]
    jupyter_bin = next((p for p in jupyter_paths if Path(p).exists() or p == "jupyter"), "jupyter")

    print(f"\n  ⏳ Re-entrenando el modelo (esto puede tardar 1-2 minutos)...")
    try:
        result = subprocess.run(
            [
                jupyter_bin, "nbconvert",
                "--to", "notebook",
                "--execute",
                f"--ExecutePreprocessor.timeout=180",
                "--inplace",
                str(NOTEBOOK_PATH),
            ],
            capture_output=True,
            text=True,
            timeout=200,
        )
        if result.returncode == 0:
            print("  ✅ Modelo re-entrenado correctamente.")
            print("  💾 Nuevos .joblib generados: tfidf_vectorizer.joblib · modelo_clasificador.joblib")
            print("  ⚠️  Reiniciá FastAPI para que cargue los nuevos modelos:")
            print("        uvicorn app.main:app --port 8000")
            return True
        else:
            print(f"  ❌ Error durante el re-entrenamiento:")
            print(f"  {result.stderr[-300:] if result.stderr else 'Sin detalles'}")
            return False
    except subprocess.TimeoutExpired:
        print("  ❌ El re-entrenamiento superó el tiempo máximo (3 min). Corré el notebook manualmente.")
        return False
    except FileNotFoundError:
        print(f"  ❌ jupyter no encontrado. Re-entrená manualmente:")
        print(f"        jupyter nbconvert --execute TechMind_DataScience.ipynb")
        return False

# ─────────────────────────────────────────────────────────────────────────────
# 10. Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="TechMind — Ingestar documentos PDF/DOCX a PostgreSQL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python3 ingest_documents.py
  python3 ingest_documents.py --carpeta ./mis_docs/
  python3 ingest_documents.py --archivo guia_kubernetes.pdf --categoria DevOps
        """,
    )
    parser.add_argument("--carpeta", type=Path, default=CARPETA_DEFAULT,
                        help="Carpeta con documentos PDF/DOCX (default: ./documentos/)")
    parser.add_argument("--archivo", type=Path, default=None,
                        help="Procesar un solo archivo")
    parser.add_argument("--categoria", type=str, default="",
                        help="Asignar categoría directamente (sin preguntar)")
    args = parser.parse_args()

    # Verificar dependencias
    if not PDF_OK:
        print("⚠️  pdfplumber no instalado — los PDFs no se procesarán.")
        print("   Instalar: pip install pdfplumber")
    if not DOCX_OK:
        print("⚠️  python-docx no instalado — los DOCX no se procesarán.")
        print("   Instalar: pip install python-docx")

    # Validar categoría si se pasó por CLI
    if args.categoria and args.categoria not in CATEGORIAS:
        print(f"❌ Categoría inválida: '{args.categoria}'")
        print(f"   Válidas: {', '.join(CATEGORIAS)}")
        sys.exit(1)

    # Conectar a PostgreSQL
    try:
        con = get_connection()
        cur = con.cursor()
        print("✅ Conectado a PostgreSQL")
    except Exception as e:
        print(f"❌ No se pudo conectar a PostgreSQL: {e}")
        print("   Verificá que Docker esté corriendo: docker-compose up -d")
        sys.exit(1)

    insertados_total = 0

    # ── Modo archivo único ────────────────────────────────────────────────────
    if args.archivo:
        if not args.archivo.exists():
            print(f"❌ Archivo no encontrado: {args.archivo}")
            sys.exit(1)
        insertados_total += procesar_archivo(args.archivo, con, cur, args.categoria)

    # ── Modo carpeta ──────────────────────────────────────────────────────────
    else:
        if not args.carpeta.exists():
            args.carpeta.mkdir(parents=True)
            print(f"📁 Carpeta creada: {args.carpeta}")
            print(f"   Colocá tus archivos PDF o DOCX ahí y volvé a ejecutar el script.")
            sys.exit(0)

        archivos = sorted(
            list(args.carpeta.glob("*.pdf")) + list(args.carpeta.glob("*.docx"))
        )

        if not archivos:
            print(f"📂 No se encontraron archivos PDF o DOCX en: {args.carpeta}")
            print(f"   Colocá tus documentos en esa carpeta y volvé a ejecutar.")
            sys.exit(0)

        print(f"\n📂 {len(archivos)} archivo(s) encontrado(s) en '{args.carpeta}':")
        for a in archivos:
            size_kb = a.stat().st_size // 1024
            print(f"   • {a.name} ({size_kb} KB)")

        for archivo in archivos:
            insertados_total += procesar_archivo(archivo, con, cur, args.categoria)

    # ── Resumen ───────────────────────────────────────────────────────────────
    mostrar_resumen(cur, insertados_total)

    # ── Re-entrenamiento automático ───────────────────────────────────────────
    if insertados_total >= UMBRAL_REENTRENAMIENTO:
        print(f"  🔁 Se alcanzó el umbral de {UMBRAL_REENTRENAMIENTO} documento(s) nuevo(s).")
        if preguntar_si_no("¿Re-entrenar el modelo ahora?"):
            cur.close()
            con.close()
            reentrenar_modelo()
            return

    cur.close()
    con.close()


if __name__ == "__main__":
    main()
