"""
expand_and_train.py
===================
Amplía el dataset de TechMind (con foco especial en Mobile y Cloud),
aplica Data Augmentation y preprocesamiento avanzado (NLTK + TF-IDF Sublineal 1-3 n-gramas),
entrena un Ensamble Calibrado (LogisticRegression + Calibrated LinearSVC + ComplementNB)
y genera los archivos .joblib optimizados para la API FastAPI.
"""

import os
import csv
import re
import joblib
import pandas as pd
import numpy as np
import psycopg2
from pathlib import Path

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Intentar cargar stopwords de NLTK con fallback robusto
try:
    import nltk
    nltk.download('stopwords', quiet=True)
    from nltk.corpus import stopwords
    STOPWORDS_ES = set(stopwords.words('spanish'))
    print("✅ NLTK Stopwords cargadas exitosamente (154 palabras).")
except Exception:
    STOPWORDS_ES = {
        "el","la","los","las","un","una","unos","unas","de","del","al","a","en","y","o",
        "que","con","para","por","se","su","sus","es","son","este","esta","estos","estas",
        "como","más","mas","muy","entre","sobre","desde","hasta","tambien","también","ser",
        "utilizando","utiliza","permite","contenido","introduccion","introducción","tutorial",
        "cómo","como","así","asi","para","con","por","del","los","las","una","un","ante",
        "bajo","cabe","con","contra","desde","hacia","hasta","para","por","segun","según",
        "sin","so","sobre","tras","durante","mediante","uso","usando","ejemplo","guia","guía"
    }
    print("⚠️ NLTK no disponible. Usando lista expandida de stopwords manuales.")

# Palabras adicionales de ruido técnico común que no aportan a la categoría
RUIDO_TECNICO = {
    "tutorial", "guia", "guía", "introduccion", "introducción", "explicacion", "explicación",
    "concepto", "conceptos", "basico", "básicos", "basicos", "básica", "basica", "avanzado",
    "avanzada", "desarrollo", "creacion", "creación", "uso", "usando", "ejemplo", "ejemplos",
    "practica", "práctica", "practicas", "prácticas", "paso", "pasos", "aplicacion", "aplicación",
    "aplicaciones", "sistema", "sistemas", "servicio", "servicios", "completo", "completa"
}
STOPWORDS_TOTAL = STOPWORDS_ES.union(RUIDO_TECNICO)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import ComplementNB
from sklearn.ensemble import VotingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

BASE_DIR = Path(__file__).parent.parent
RAW_CSV_PATH = BASE_DIR / "data" / "raw" / "contenidos_tecnicos.csv"
MODELS_DIR = BASE_DIR / "models"

# ── 1. Cargar CSV existente ──────────────────────────────────────────────────
print("📂 Cargando dataset existente...")
if os.path.exists(RAW_CSV_PATH):
    df_existente = pd.read_csv(RAW_CSV_PATH)
    print(f"   {len(df_existente)} registros actuales en CSV.")
else:
    df_existente = pd.DataFrame(columns=["titulo", "texto", "categoria"])

# ── 2. Definir nuevos registros focalizados (Data Augmentation & Border Cases) ───────
NUEVOS_DATOS_ESPECIALIZADOS = [
    # ── MOBILE (Refuerzo especializado) ──────────────────────────────────────
    ("Navegación nativa en iOS con SwiftUI NavigationStack", "Cómo estructurar flujos de pantalla declarativos, paso de binding y rutas en SwiftUI para iOS 16+.", "Mobile"),
    ("Jetpack Compose State Management y Remember", "Manejo de estado reactivo en Android con remember, rememberSaveable y StateFlow en Kotlin Compose.", "Mobile"),
    ("Compilación nativa de Flutter con Dart AOT", "Compilación Ahead-Of-Time (AOT) en Flutter para generar código de máquina nativo súper rápido en iOS y Android.", "Mobile"),
    ("Módulos nativos en React Native con la nueva arquitectura (Fabric)", "Integración de C++ y TurboModules en React Native para comunicación directa con el hilo nativo.", "Mobile"),
    ("Persistencia local rápida con Realm / Isar en móviles", "Uso de bases de datos orientadas a objetos ultrarrápidas para sincronización offline en Flutter y React Native.", "Mobile"),
    ("Inyección de dependencias en Android con Hilt y Dagger", "Configuración de anotaciones @AndroidEntryPoint y @HiltViewModel para desacoplar componentes nativos.", "Mobile"),
    ("Arquitectura MVVM y Clean Architecture en iOS con Swift", "Organización de capas de presentación, caso de uso y repositorio usando Combine y Async/Await en Swift.", "Mobile"),
    ("Push Notifications nativas con APNs y Firebase en iOS", "Configuración de certificados Apple Push Notification service (APNs) y payload de notificaciones en Swift.", "Mobile"),
    ("Deep Links e Intent Filters en aplicaciones Android", "Manejo de esquemas URL personalizados y Universal Links para abrir pantallas específicas de la app móvil.", "Mobile"),
    ("Pruebas automatizadas de UI en iOS con XCTest y XCUITest", "Escritura de tests de interfaz para simular toques, scroll y aserciones de elementos visuales en iOS.", "Mobile"),
    ("Optimizaciones de rendimiento de batería y memoria en apps móviles", "Estrategias para minimizar consumo de batería, rastreo GPS en background y fugas de memoria en smartphones.", "Mobile"),
    ("Kotlin Multiplatform (KMP) para compartir lógica de negocio", "Compartir código de lógica de dominio, modelos y red entre iOS y Android usando Kotlin Multiplatform.", "Mobile"),

    # ── CLOUD (Refuerzo especializado) ──────────────────────────────────────
    ("Arquitectura de Redes VPC en AWS: Subnets y NAT Gateway", "Diseño de redes privadas virtuales, tablas de ruteo, subredes públicas/privadas e instancias Bastion en AWS.", "Cloud"),
    ("Servicios Serverless con AWS Lambda y API Gateway", "Creación de microservicios sin servidor mediante funciones Lambda activadas por endpoints de API Gateway.", "Cloud"),
    ("Oracle Cloud Infrastructure (OCI) Autonomous Database", "Despliegue y administración de bases de datos autónomas con autorreparación y escalado dinámico en OCI.", "Cloud"),
    ("Políticas IAM y Roles de Asunción en AWS / Azure", "Configuración de políticas de seguridad basadas en JSON, mínimo privilegio y asunción de roles IAM para servicios.", "Cloud"),
    ("Almacenamiento global con AWS S3 y CloudFront CDN", "Distribución acelerada de archivos multimedia y assets estáticos mediante puntos de presencia de CloudFront.", "Cloud"),
    ("Despliegue de infraestructura multinube con Terraform HCL", "Procesamiento de plantillas declarativas en HCL para aprovisionar recursos en AWS, Azure y Google Cloud.", "Cloud"),
    ("Monitoreo cloud nativo con AWS CloudWatch y CloudTrail", "Auditoría de llamadas a la API de AWS y métricas de consumo de cómputo en tiempo real con alarmas SNS.", "Cloud"),
    ("Google Cloud Run y ejecución de contenedores sin servidor", "Despliegue de contenedores Docker HTTP en GCP con autoescalado a cero instancias cuando no hay tráfico.", "Cloud"),
    ("Estrategias FinOps para optimizar costos de cómputo Cloud", "Uso de instancias Spot/Reservadas, análisis de facturación en la nube y etiquetado de recursos cloud.", "Cloud"),
    ("Azure App Services y Azure Functions serverless", "Alojamiento de aplicaciones web y funciones asíncronas serverless en la plataforma en la nube de Microsoft Azure.", "Cloud"),
    ("Disaster Recovery y Multi-Region Active-Active en Cloud", "Estrategias de replicación transcontinental de datos y conmutación por error DNS para alta disponibilidad cloud.", "Cloud"),
    ("Conexión privada corporativa con AWS Direct Connect / OCI FastConnect", "Enlace dedicado de fibra óptica entre el data center on-premise y la nube privada virtual.", "Cloud"),

    # ── DEVOPS ──────────────────────────────────────────────────────────────
    ("Orquestación de clústeres de Kubernetes con Helm y Kustomize", "Plantillado de recursos de Kubernetes y gestión de entornos dev, staging y prod con Helm charts.", "DevOps"),
    ("Pipelines de CI/CD avanzados en GitHub Actions con Caching", "Reutilización de caché de dependencias npm/maven y paralelizacion de jobs de pruebas automatizadas.", "DevOps"),
    ("GitOps con ArgoCD y Sincronización Automática", "Despliegue continuo declarativo desde Git hacia Kubernetes mediante el agente controlador de ArgoCD.", "DevOps"),

    # ── BACKEND ─────────────────────────────────────────────────────────────
    ("Microservicios reactivos con Spring Boot 3 y WebFlux", "Programación reactiva no bloqueante en Java utilizando Netty, Flux, Mono y Spring WebFlux.", "Backend"),
    ("API REST con FastAPI, Pydantic v2 y SQLModel", "Desarrollo de microservicios ultra rápidos en Python con tipado estático, validación Pydantic y ORM async.", "Backend"),
    ("Comunicación entre microservicios con gRPC y Protobuf", "Serialización binaria de alta velocidad mediante Protocol Buffers y contratos gRPC en servicios backend.", "Backend"),

    # ── FRONTEND ────────────────────────────────────────────────────────────
    ("Next.js 14 App Router, Server Actions y React Server Components", "Renderizado híbrido en el servidor, mutaciones de datos directas con Server Actions y optimización web.", "Frontend"),
    ("Gestión de estado asíncrono con TanStack React Query v5", "Caché de consultas HTTP, invalidación de queries y mutaciones optimistas en aplicaciones frontend.", "Frontend"),

    # ── DATA SCIENCE ────────────────────────────────────────────────────────
    ("Fine-tuning de modelos LLM con LoRA y Hugging Face", "Ajuste fino eficiente de modelos de lenguaje grandes mediante adaptadores de baja densidad LoRA.", "Data Science"),
    ("Vector Embeddings e Indexación HNSW con ChromaDB / pgvector", "Búsqueda por similitud semántica de texto utilizando embeddings vectoriales y métricas de coseno.", "Data Science"),

    # ── BASES DE DATOS ──────────────────────────────────────────────────────
    ("Consultas analíticas avanzadas en PostgreSQL con Window Functions", "Uso de OVER(), PARTITION BY, DENSE_RANK() y LAG() para reportes complejos en PostgreSQL.", "Bases de Datos"),
    ("Indexación GIN y búsqueda Full-Text Search en PostgreSQL", "Búsqueda rápida de texto en campos JSONB y documentos usando índices GIN y tsvector en PostgreSQL.", "Bases de Datos"),

    # ── SEGURIDAD ───────────────────────────────────────────────────────────
    ("Autenticación robusta con OAuth2, PKCE y JSON Web Tokens (JWT)", "Implementación de flujos seguros de autorización sin estado con tokens de acceso y refresh tokens.", "Seguridad"),
    ("Protección contra inyecciones SQL y mitigación de OWASP Top 10", "Buenas prácticas de sanitización de entradas, cabeceras de seguridad HSTS/CSP y consultas preparadas.", "Seguridad")
]

df_nuevos = pd.DataFrame(NUEVOS_DATOS_ESPECIALIZADOS, columns=["titulo", "texto", "categoria"])

# Combinar manteniendo unicidad de titulo
df_total = pd.concat([df_existente, df_nuevos], ignore_index=True)
df_total.drop_duplicates(subset=["titulo"], inplace=True)
print(f"✅ Total registros combinados en dataset: {len(df_total)}")

# Guardar en CSV
df_total.to_csv(RAW_CSV_PATH, index=False, encoding="utf-8")
print(f"💾 Guardado CSV actualizado en {RAW_CSV_PATH}")

print("\n📊 Distribución final por categoría:")
print(df_total["categoria"].value_counts())

# ── 3. Migración opcional a PostgreSQL ───────────────────────────────────────
print("\n🐘 Intentando sincronizar dataset con PostgreSQL...")
def get_pg_con():
    return psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=int(os.getenv("PG_PORT", 5432)),
        dbname=os.getenv("PG_DB", "techmind"),
        user=os.getenv("PG_USER", "techmind_user"),
        password=os.getenv("PG_PASSWORD", "techmind_pass"),
        connect_timeout=3
    )

try:
    con = get_pg_con()
    cur = con.cursor()
    cur.execute("TRUNCATE TABLE contenidos RESTART IDENTITY CASCADE;")
    rows = [(row["titulo"], row["texto"]) for _, row in df_total.iterrows()]
    cur.executemany("INSERT INTO contenidos (titulo, texto) VALUES (%s, %s);", rows)
    con.commit()
    cur.close()
    con.close()
    print("✅ Registros migrados exitosamente a PostgreSQL.")
except Exception as e:
    print(f"⚠️ Aviso migración PostgreSQL: {e} (Continuando entrenamiento independientemente)")

# ── 4. Preprocesamiento & Feature Engineering ───────────────────────────────
print("\n🤖 Preprocesando datos y configurando Vectorizador TF-IDF Avanzado...")

def limpiar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúñü0-9\s]", " ", texto)
    palabras = texto.split()
    palabras = [p for p in palabras if p not in STOPWORDS_TOTAL and len(p) > 2]
    return " ".join(palabras)

df_total["texto_completo"] = df_total["titulo"] + ". " + df_total["texto"]
df_total["texto_limpio"] = df_total["texto_completo"].apply(limpiar_texto)

vectorizer = TfidfVectorizer(
    sublinear_tf=True,       # Escalamiento logarítmico (1 + log(tf))
    ngram_range=(1, 3),      # Unigramas, Bigramas y Trigramas técnicos
    min_df=1,
    max_df=0.90,
    max_features=6000
)

X = vectorizer.fit_transform(df_total["texto_limpio"])
y = df_total["categoria"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# ── 5. Construcción del Ensamble Calibrado (Soft Voting) ─────────────────────
print("⚡ Entrenando Ensamble Calibrado (Logistic Regression + Calibrated LinearSVC + ComplementNB)...")

clf_lr = LogisticRegression(max_iter=1000, class_weight="balanced", C=1.5, random_state=42)
clf_svc = CalibratedClassifierCV(
    estimator=LinearSVC(class_weight="balanced", max_iter=3000, random_state=42),
    cv=5,
    method="sigmoid"
)
clf_cnb = ComplementNB(alpha=0.5)

ensamble_eval = VotingClassifier(
    estimators=[
        ("lr", clf_lr),
        ("svc", clf_svc),
        ("cnb", clf_cnb)
    ],
    voting="soft"
)

ensamble_eval.fit(X_train, y_train)

y_pred = ensamble_eval.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"\n✨ ¡Evaluación de Ensamble Completada!")
print(f"🎯 Accuracy en Holdout Test (20%): {acc:.4f} ({acc*100:.2f}%)")
print("\n📋 Reporte de clasificación detallado:")
print(classification_report(y_test, y_pred))

# ── 6. Re-fit final sobre el 100% de los datos para Producción ──────────────
print("\n🏋️ Entrenando modelo final sobre el 100% del dataset...")
modelo_final = VotingClassifier(
    estimators=[
        ("lr", LogisticRegression(max_iter=1000, class_weight="balanced", C=1.5, random_state=42)),
        ("svc", CalibratedClassifierCV(
            estimator=LinearSVC(class_weight="balanced", max_iter=3000, random_state=42),
            cv=5,
            method="sigmoid"
        )),
        ("cnb", ComplementNB(alpha=0.5))
    ],
    voting="soft"
)
modelo_final.fit(X, y)

# ── 7. Serializar artefactos .joblib ──────────────────────────────────────────
os.makedirs(MODELS_DIR, exist_ok=True)
joblib.dump(vectorizer, MODELS_DIR / "tfidf_vectorizer.joblib")
joblib.dump(modelo_final, MODELS_DIR / "modelo_clasificador.joblib")

print(f"💾 Nuevos artefactos .joblib serializados exitosamente en {MODELS_DIR}")
print("🚀 Proceso de optimización de modelo completado con éxito.")
