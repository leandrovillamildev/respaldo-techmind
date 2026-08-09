#!/usr/bin/env python3
"""
setup.py — TechMind · Script de instalación y arranque automático universal
=============================================================================
Instala todas las dependencias y deja el proyecto andando en cualquier sistema:
Windows, macOS o Linux.

Ejecución:
    python setup.py          ← Modo A (Desarrollo local: Docker DB + APIs/Frontend nativos)
    python setup.py --start  ← Inicio rápido de servicios previamente instalados
    python setup.py --docker ← Modo B (100% Dockerizado: PostgreSQL + FastAPI + Spring Boot + Frontend)

Hackathon G9 LATAM · Equipo 37
"""

import os
import sys
import subprocess
import platform
import time
import shutil
import argparse
import socket

# ─── Configuración ────────────────────────────────────────────────────────────

IS_WINDOWS  = platform.system() == "Windows"
VENV_DIR    = "venv"
SCRIPTS_DIR = "Scripts" if IS_WINDOWS else "bin"

VENV_PYTHON   = os.path.join(VENV_DIR, SCRIPTS_DIR, "python.exe" if IS_WINDOWS else "python")
VENV_PIP      = os.path.join(VENV_DIR, SCRIPTS_DIR, "pip.exe"    if IS_WINDOWS else "pip")
VENV_UVICORN  = os.path.join(VENV_DIR, SCRIPTS_DIR, "uvicorn.exe" if IS_WINDOWS else "uvicorn")

REQUIREMENTS   = os.path.join("data-science", "requirements.txt")
MIGRATE_SCRIPT = os.path.join("data-science", "src", "migrate_to_postgres.py")

TOTAL_STEPS   = 7


# ─── Helpers ──────────────────────────────────────────────────────────────────

def header(n, msg):
    print(f"\n{'─' * 65}")
    print(f"  [{n}/{TOTAL_STEPS}] {msg}")
    print(f"{'─' * 65}")

def ok(msg):    print(f"  ✅  {msg}")
def warn(msg):  print(f"  ⚠️   {msg}")
def info(msg):  print(f"  ℹ️   {msg}")

def fail(msg):
    print(f"\n  ❌  {msg}")
    print("  Revisá el error anterior y volvé a intentar.")
    sys.exit(1)

def run(cmd, **kwargs):
    """Ejecuta un comando en shell de forma multiplataforma."""
    return subprocess.run(cmd, shell=True, **kwargs)

def run_or_fail(cmd, error_msg, **kwargs):
    """Ejecuta un comando y termina con mensaje en caso de error."""
    result = run(cmd, **kwargs)
    if result.returncode != 0:
        fail(error_msg)
    return result

def is_port_open(port):
    """Comprueba si un puerto local está escuchando."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(('127.0.0.1', port)) == 0


# ─── Paso 1 — Verificar Python ───────────────────────────────────────────────

def check_python():
    header(1, "Verificando instalación de Python")
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 10):
        fail(
            f"Se requiere Python 3.10 o superior. Tenés Python {v.major}.{v.minor}.\n"
            "  Descargalo desde https://www.python.org/downloads/\n"
            "  (En Windows: asegurate de marcar 'Add Python to PATH' durante la instalación)"
        )
    ok(f"Python {v.major}.{v.minor}.{v.micro} en {platform.system()} — OK")


# ─── Paso 2 — Entorno virtual ────────────────────────────────────────────────

def create_venv():
    header(2, "Preparando entorno virtual de Python (venv)")
    if os.path.exists(VENV_PYTHON):
        ok("El entorno virtual ya existe en ./venv — omitiendo creación")
        return
    info("Creando entorno virtual en ./venv ...")
    run_or_fail(
        f'"{sys.executable}" -m venv {VENV_DIR}',
        "No se pudo crear el entorno virtual."
    )
    ok("Entorno virtual creado exitosamente")


# ─── Paso 3 — Instalar dependencias ──────────────────────────────────────────

def install_deps():
    header(3, "Instalando dependencias necesarias (FastAPI, Scikit-Learn, Psycopg2)")
    if not os.path.exists(REQUIREMENTS):
        fail(f"No se encontró el archivo {REQUIREMENTS}")
    info("Instalando dependencias desde requirements.txt ...")
    run_or_fail(
        f'"{VENV_PIP}" install -r "{REQUIREMENTS}" --quiet',
        f"Error al instalar dependencias desde {REQUIREMENTS}"
    )
    ok("Todas las dependencias están instaladas y listas")


# ─── Paso 4 — Variables de entorno ───────────────────────────────────────────

def setup_env():
    header(4, "Configurando variables de entorno (.env)")
    if not os.path.exists(".env"):
        if not os.path.exists(".env.example"):
            fail("No se encontró .env.example en la raíz del proyecto.")
        shutil.copy(".env.example", ".env")

    with open(".env", "r", encoding="utf-8") as f:
        env_content = f.read()

    admin_user = "admin"
    admin_pass = "admin123"

    # Si estamos en terminal interactiva, solicitar credenciales al usuario
    if sys.stdin.isatty():
        print("\n  🔐 Configuración de cuenta Administrador:")
        try:
            u_input = input("     Ingrese usuario administrador [admin]: ").strip()
            if u_input:
                admin_user = u_input

            p_input = input("     Ingrese contraseña administrador [admin123]: ").strip()
            if p_input:
                admin_pass = p_input
        except (KeyboardInterrupt, EOFError):
            print()
            pass
        except Exception:
            pass

    # Actualizar o insertar ADMIN_USER, ADMIN_PASSWORD y JWT_SECRET en .env
    lines = env_content.splitlines()
    updated_user = False
    updated_pass = False
    updated_jwt = False
    new_lines = []

    for line in lines:
        if line.startswith("ADMIN_USER="):
            new_lines.append(f"ADMIN_USER={admin_user}")
            updated_user = True
        elif line.startswith("ADMIN_PASSWORD="):
            new_lines.append(f"ADMIN_PASSWORD={admin_pass}")
            updated_pass = True
        elif line.startswith("JWT_SECRET="):
            new_lines.append(line)
            updated_jwt = True
        else:
            new_lines.append(line)

    if not updated_user:
        new_lines.append(f"ADMIN_USER={admin_user}")
    if not updated_pass:
        new_lines.append(f"ADMIN_PASSWORD={admin_pass}")
    if not updated_jwt:
        new_lines.append("JWT_SECRET=supersecret_techmind_token_2026")

    with open(".env", "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")

    ok(f"Credenciales de administrador listas en .env (Usuario: '{admin_user}')")




# ─── Paso 5 — Docker / PostgreSQL ────────────────────────────────────────────

def start_docker():
    header(5, "Verificando e iniciando PostgreSQL en Docker")

    # Verificar que Docker esté disponible
    result = run("docker --version", capture_output=True)
    if result.returncode != 0:
        fail(
            "Docker no está instalado o no está en el PATH de tu sistema.\n"
            "  Instalá Docker Desktop desde https://www.docker.com/products/docker-desktop/"
        )

    # Verificar que el servicio/motor de Docker esté corriendo
    result = run("docker ps", capture_output=True)
    if result.returncode != 0:
        fail(
            "Docker está instalado pero no se encuentra ejecutándose.\n"
            "  Abrí Docker Desktop, esperá a que el ícono esté en verde y volvé a ejecutar setup.py."
        )

    # Levantar el contenedor de PostgreSQL
    info("Levantando contenedor techmind-postgres (Puerto 5432) ...")
    result = run("docker compose up -d postgres")
    if result.returncode != 0:
        info("Intentando iniciar contenedor existente 'techmind-postgres'...")
        result = run("docker start techmind-postgres", capture_output=True)
        if result.returncode != 0:
            fail("No se pudo levantar PostgreSQL con Docker.")

    # Esperar a que PostgreSQL acepte conexiones
    print("  ⏳ Esperando respuesta de PostgreSQL", end="", flush=True)
    for _ in range(30):
        time.sleep(1)
        ready = run(
            "docker exec techmind-postgres pg_isready -U techmind_user -d techmind",
            capture_output=True
        )
        if ready.returncode == 0:
            print(" ✅")
            ok("PostgreSQL activo y listo en localhost:5432")
            return
        print(".", end="", flush=True)

    print()
    warn("PostgreSQL tardó en responder pero continuaremos con el arranque...")


# ─── Paso 6 — Migración del Dataset ──────────────────────────────────────────

def migrate_db():
    header(6, "Verificando e ingiriendo dataset de entrenamiento (221 registros)")
    if not os.path.exists(MIGRATE_SCRIPT):
        fail(f"No se encontró el script de migración: {MIGRATE_SCRIPT}")

    info("Ejecutando script de migración CSV a PostgreSQL ...")
    result = subprocess.run(
        [VENV_PYTHON, MIGRATE_SCRIPT],
        input="N\n",
        text=True
    )

    if result.returncode != 0:
        warn("La migración reportó un aviso. Si las tablas Flyway de Spring Boot aún no fueron creadas, los datos se cargarán cuando Spring Boot inicie.")
    else:
        ok("Base de datos lista con 221 registros de contenido técnico")


# ─── Paso 7 — Iniciar Servicios (Frontend + FastAPI ML) ──────────────────────

def start_services():
    header(7, "Poniendo en marcha el proyecto (Frontend + FastAPI)")

    # Servidor Web liviano para el Frontend en puerto 5173
    if not is_port_open(5173):
        info("Iniciando servidor web para el Frontend en http://localhost:5173 ...")
        cmd_frontend = [sys.executable, "-m", "http.server", "5173", "--directory", "frontend"]
        subprocess.Popen(cmd_frontend, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
        ok("Frontend Web iniciado en http://localhost:5173")
    else:
        ok("Frontend Web ya disponible en http://localhost:5173")

    print()
    print(" ╔═════════════════════════════════════════════════════════════════════╗")
    print(" ║                  🚀 PROYECTO TECHMIND LISTO Y EN EJECUCIÓN          ║")
    print(" ╠═════════════════════════════════════════════════════════════════════╣")
    print(" ║  🎨 Frontend Web UI (Stitch UI):   http://localhost:5173            ║")
    print(" ║  🤖 Microservicio FastAPI ML:   http://localhost:8000               ║")
    print(" ║  ☕ API Spring Boot (Backend):  http://localhost:8080               ║")
    print(" ║  📖 Documentación Swagger:      http://localhost:8000/docs          ║")
    print(" ╚═════════════════════════════════════════════════════════════════════╝")
    print()
    info("Para conectar el backend Java de Spring Boot:")
    print("  En otra terminal ejecutá: cd backend/api && ./mvnw spring-boot:run\n")
    print("  Para detener la API de Python: Presioná CTRL + C\n")

    cmd_uvicorn = [VENV_UVICORN, "app.main:app", "--reload", "--port", "8000"]

    env = os.environ.copy()
    env["MODEL_PATH"] = os.path.join("data-science", "models")

    try:
        subprocess.run(cmd_uvicorn, env=env)
    except KeyboardInterrupt:
        print("\n\n  🛑 Microservicio FastAPI detenido por el usuario.")
        sys.exit(0)
    except FileNotFoundError:
        fail(f"No se encontró uvicorn en {VENV_UVICORN}. Ejecutá primero: python setup.py")


# ─── Modo 100% Dockerizado ──────────────────────────────────────────────────

def check_model_files():
    """Verifica que los archivos .joblib existen antes de buildear Docker."""
    models_dir = os.path.join("data-science", "models")
    required = ["tfidf_vectorizer.joblib", "modelo_clasificador.joblib"]
    missing = []
    for f in required:
        path = os.path.join(models_dir, f)
        if not os.path.isfile(path):
            missing.append(path)
    return missing


def reset_docker_volumes():
    """
    Elimina el volumen de PostgreSQL si existe, para que Flyway
    pueda crear las tablas limpias con el esquema correcto (BIGSERIAL).
    Solo se ejecuta si el usuario confirma o si el volumen ya está presente.
    """
    import subprocess as _sp
    # Detectar si el volumen viejo existe
    result = _sp.run(
        "docker volume ls --format {{.Name}}",
        shell=True,
        stdout=_sp.PIPE,
        stderr=_sp.DEVNULL
    )
    volume_names = result.stdout.decode(errors="replace") if result.returncode == 0 else ""

    # Buscar volumen que corresponda al proyecto
    candidate_volumes = [
        v.strip() for v in volume_names.splitlines()
        if "techmind" in v.lower() and "data" in v.lower()
    ]

    if candidate_volumes:
        warn(f"Volumen de datos viejo detectado: {', '.join(candidate_volumes)}")
        warn("Esto puede causar errores de schema en Spring Boot (serial vs bigint).")
        print()
        print("  ¿Querés eliminar el volumen para un deploy limpio? (s/N): ", end="", flush=True)
        try:
            answer = input().strip().lower()
        except EOFError:
            answer = "s"

        if answer in ("s", "si", "sí", "y", "yes"):
            info("Deteniendo contenedores y eliminando volumen...")
            run("docker compose --profile full down -v")
            ok("Volumen eliminado. Flyway creará el schema correcto desde cero.")
        else:
            warn("Continuando sin limpiar el volumen. Si Spring Boot falla, ejecutá:")
            warn("  docker compose --profile full down -v")
            warn("  python setup.py --docker")
    else:
        # Primera vez: bajar contenedores por las dudas
        run("docker compose --profile full down")



def run_full_docker():
    """Ejecuta los 4 contenedores en Docker Compose."""
    print()
    print("  🐳 TechMind — Modo 100% Dockerizado (Producción / Demo)")
    print()

    # 1. Verificar modelos ML (auto-generar si no existen)
    missing = check_model_files()
    if missing:
        warn("No se encontraron los modelos .joblib. Generándolos automáticamente...")
        if not os.path.exists(VENV_PYTHON):
            info("Creando entorno virtual e instalando librerías de Data Science para la generación...")
            create_venv()
            install_deps()
        
        gen_script = os.path.join("data-science", "src", "generate_models.py")
        py_bin = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable
        
        res = run(f'"{py_bin}" "{gen_script}"')
        if res.returncode != 0:
            fail("No se pudieron generar los modelos de ML (.joblib).")
        missing = check_model_files()
        if missing:
            fail("Los modelos no pudieron ser guardados en data-science/models/")

    ok("Modelos ML verificados: tfidf_vectorizer.joblib y modelo_clasificador.joblib")

    # 2. Limpiar volúmenes viejos para evitar errores de schema de Flyway
    reset_docker_volumes()

    # 3. Build y arranque del stack completo
    print()
    info("Compilando y levantando PostgreSQL + FastAPI + Spring Boot + Frontend en Docker...")
    result = run("docker compose --profile full up -d --build")
    if result.returncode == 0:
        print()
        ok("¡Todo el stack fue dockerizado y levantado exitosamente en contenedores!")
        print()
        print("  • Frontend Web UI: http://localhost:5173")
        print("  • Spring Boot API: http://localhost:8080")
        print("  • FastAPI ML:      http://localhost:8000")
        print()
        info("Esperando que los servicios estén listos (~15 segundos)...")
        time.sleep(15)
        ok("¡Proyecto listo! Abrí http://localhost:5173 en tu navegador.")
    else:
        fail("Ocurrió un error al compilar la pila Docker.")
        print()
        warn("Tip: si el error es de schema, ejecutá:")
        warn("  docker-compose --profile full down -v")
        warn("  python setup.py --docker")



# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="TechMind — Script de instalación y arranque universal"
    )
    parser.add_argument(
        "--start",
        action="store_true",
        help="Inicio rápido de los servicios (omite el proceso de instalación inicial)."
    )
    parser.add_argument(
        "--docker",
        action="store_true",
        help="Compila y ejecuta los 4 componentes en contenedores Docker (Modo Dockerizado Completo)."
    )
    args = parser.parse_args()

    print()
    print("╔═════════════════════════════════════════════════════════════════╗")
    print("║   🧠 TechMind — Asistente de Instalación y Arranque             ║")
    print("║   Hackathon G9 LATAM · Equipo 37                                ║")
    print("╚═════════════════════════════════════════════════════════════════╝")

    # Configurar siempre .env primero para asegurar que existan las credenciales
    setup_env()

    if args.docker:
        run_full_docker()
        return

    if args.start:
        if not os.path.exists(VENV_PYTHON):
            fail("El entorno virtual no existe. Ejecutá primero: python setup.py")
        start_docker()
        start_services()
        return

    # Setup completo por defecto (Modo A)
    check_python()
    create_venv()
    install_deps()
    start_docker()
    migrate_db()
    start_services()


if __name__ == "__main__":
    main()
