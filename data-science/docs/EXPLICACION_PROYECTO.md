# 🧠 TechMind — Explicación del Proyecto

> **¿Para quién es este documento?**  
> Para cualquier persona (estudiante, jurado, reclutador o compañero) que quiera entender **qué es TechMind**, **cómo funciona** y **qué problema resuelve**, expresado en lenguaje claro, simple y accesible sin necesidad de saber programar.

---

## 🎯 ¿Qué problema resuelve TechMind?

Imaginate que sos estudiante o profesional de tecnología.  
Cada día leés artículos, tutoriales, documentación de herramientas, guías de código y resúmenes de cursos...  
Con el tiempo, acumulás cientos de notas guardadas en distintos lugares y, cuando querés volver a encontrar algo, **no sabés por dónde empezar a buscar**.

**TechMind resuelve exactamente ese problema.**

Le entregás cualquier texto técnico —puede ser el título de un artículo y su explicación, un snippet de código o una nota rápida— y el sistema en **menos de un segundo** responde automáticamente con:

1. 📂 **La categoría temática** (`Backend`, `Frontend`, `Data Science`, `DevOps`, `Mobile`, `Bases de Datos`, `Seguridad`, `Cloud`).
2. 📊 **El nivel de probabilidad / confianza** de la predicción (por ejemplo: `88.7% de certeza`).
3. 🔑 **Las palabras clave (keywords) más relevantes** extraídas del texto.
4. 📜 **Un historial organizado y persistente** disponible desde la interfaz web.

Todo sin que ninguna persona tenga que leerlo ni etiquetarlo a mano.

---

## 🏗️ ¿Cómo funciona el sistema en la práctica? (El flujo paso a paso)

TechMind está formado por **cuatro componentes que trabajan en equipo**, conectadas como los engranajes de un reloj:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. 🎨 FRONTEND (Interfaz Web Cyber AI — Puerto 5173)                   │
│    VOS escribís el título y texto en la pantalla y tocás "Clasificar"   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ ✉️ Envía el contenido
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. ☕ BACKEND PRINCIPAL (Java / Spring Boot — Puerto 8080)              │
│    Recibe el texto, genera su ID y le pide ayuda a la Inteligencia Art.│
└──────────────┬──────────────────────────────────────────┬───────────────┘
               │ 🤖 Solicita predicción                   │ 💾 Guarda datos
               ▼                                          ▼
┌──────────────────────────────┐          ┌──────────────────────────────┐
│ 3. 🟣 CIENCIA DE DATOS       │          │ 4. 🗄️ BASE DE DATOS         │
│    FastAPI (Python) :8000    │          │    PostgreSQL (Puerto 5432)   │
│    Analiza el texto con ML,  │          │    Almacena los contenidos e  │
│    calcula la categoría y    │          │    historial de predicciones  │
│    extrae palabras clave     │          │    de forma permanente       │
└──────────────────────────────┘          └──────────────────────────────┘
```

---

## ⚙️ Explicación simple de cada parte

| Componente | ¿Qué tecnología usa? | ¿Cuál es su trabajo en simple? |
|---|---|---|
| 🎨 **1. Interfaz Web (Frontend)** | HTML5, JavaScript Vanilla, TailwindCSS Dark Mode | Es la pantalla donde interactúas. Mostrás el formulario, los botones neón con efecto de vidrio (Glassmorphism), los badges de palabras clave, el historial y los indicadores LED en tiempo real del estado de cada servicio. |
| ☕ **2. Backend (Spring Boot)** | Java 17, Spring Boot 4.x, JPA, Flyway, Actuator | Es el "cerebro orquestador". Recibe tu petición desde la web, gestiona las transacciones, le pide la inferencia al modelo de IA y coordina el guardado en la base de datos. Expone `/actuator/health` para que el frontend sepa si está activo. |
| 🤖 **3. Ciencia de Datos (FastAPI)** | Python 3.12, FastAPI, Scikit-Learn | Es la "inteligencia artificial". Recibe el texto, lo convierte en números, calcula a qué categoría pertenece y extrae las palabras más importantes. |
| 🗄️ **4. Base de Datos** | PostgreSQL 16 | Es la "memoria central". Guarda todos los artículos ingresados y sus resultados de forma segura para que puedas ver tu historial en cualquier momento. |

---

## 🧪 ¿Cómo "aprende" la Inteligencia Artificial de TechMind?

El módulo de Ciencia de Datos realiza un proceso de aprendizaje automático (Machine Learning) en 5 sencillos pasos:

### 🗃️ Paso 1 — Alimentarla con ejemplos reales (221 Registros)
Le entregamos al sistema un libro de estudio (**dataset de entrenamiento**) con **221 ejemplos reales** etiquetados previamente en las 8 categorías principales de la tecnología.

### 🧹 Paso 2 — Limpiar el texto (Procesamiento NLP)
Antes de leer un texto, la computadora elimina palabras sin valor informativo (como *"el"*, *"la"*, *"para"*, *"de"*), pasa todo a minúsculas y remueve signos de puntuación.

### 🔢 Paso 3 — Convertir palabras en números (Vectorización TF-IDF)
Las computadoras no leen letras, leen números. Usamos una técnica llamada **TF-IDF**:
> Cada palabra recibe una puntuación numérica. Cuanto más única y representativa es una palabra para un texto (ejemplo: *"kubernetes"* o *"docker"*), mayor es su número.

### 🤖 Paso 4 — Clasificar con Regresión Logística
Con los textos convertidos en números, el algoritmo aprende patrones de asociación:
> *"Si en el texto aparecen términos como 'spring', 'java' y 'autowired' → 89% probable que sea **Backend**."*  
> *"Si aparecen 'pandas', 'scikit' y 'dataset' → es **Data Science**."*

### 🔑 Paso 5 — Extraer las palabras clave
Identifica los 5 términos con mayor peso dentro del texto ingresado y los devuelve en forma de etiquetas (*badges*) para que el usuario entienda rápidamente de qué trata el documento.

---

## 📬 ¿Qué le enviás y qué te responde?

### 📥 Lo que el usuario ingresa:
* **Título:** `"Introducción a Spring Boot"`
* **Texto:** `"Tutorial sobre el uso de @Autowired, @Component y la configuración de beans en Java."`

### 📤 Lo que TechMind responde en pantalla (< 0.05 segundos):
* 📂 **Categoría:** `Backend`
* 📊 **Confianza:** `88.7%`
* 🔑 **Palabras Clave:** `spring boot`, `java`, `autowired`, `component`, `beans`

---

## 🗂️ Las 8 Categorías que clasifica

| Categoría | ¿De qué trata? | Ejemplos de tecnologías |
|---|---|---|
| ☕ **Backend** | Lógica de servidor, APIs y arquitectura | Spring Boot, Java, Node.js, Express, APIs REST |
| 🎨 **Frontend** | Interfaz visual y experiencia de usuario | React, Vue.js, HTML5, CSS3, TailwindCSS |
| 📊 **Data Science** | Análisis de datos y modelos de IA | Pandas, Scikit-Learn, Python, Machine Learning |
| 🛠️ **DevOps** | Automatización, contenedores y despliegues | Docker, Kubernetes, CI/CD, Linux |
| 📱 **Mobile** | Aplicaciones para celulares | React Native, Flutter, Android, iOS |
| 🗄️ **Bases de Datos** | Almacenamiento y consultas relacionales o NoSQL | PostgreSQL, MySQL, MongoDB, Redis |
| 🛡️ **Seguridad** | Protección de datos y autenticación | JWT, OAuth2, Cifrado, OWASP |
| ☁️ **Cloud** | Infraestructura en la nube | OCI (Oracle Cloud), AWS, Servidores |

---

## 🚀 ¿Cómo se ejecuta todo junto? (Auto-Healing & Docker)

Para evitar instalar Java, Python y PostgreSQL por separado, el proyecto cuenta con **Docker Compose** y un script automático denominado **`setup.py`**:

Con un solo comando:
```powershell
python setup.py --docker
```
El sistema automáticamente:
1. Verifica si existen los modelos de Inteligencia Artificial (si no están, los entrena e instala en 2 segundos).
2. Construye los 4 contenedores de forma aislada.
3. Levanta la pantalla web en **[http://localhost:5173](http://localhost:5173)** lista para usar.

---

## 👥 Resumen del Trabajo en Equipo

* 🟣 **Data Science & ML (Ernesto, Leandro & Rómulo):** Entrenamiento del modelo NLP, vectorización TF-IDF, dataset de 221 registros, microservicio FastAPI y scripts de auto-healing.
* 🔵 **Backend Java (Sergio, Andrés, Noelia, Camila):** Desarrollo de la API REST Spring Boot, controladores transaccionales, migraciones Flyway y persistencia.
* 🎨 **Frontend UI & Fullstack (Ernesto):** Diseño Cyber AI Dark Mode en TailwindCSS, consumo de APIs, indicadores de estado en tiempo real y modal de historial.
* 🧪 **QA & Testing (Federico):** Suite automatizada de pruebas E2E, matrices de validación y reportes de resiliencia.

---

## 💡 En resumen

> **TechMind es un asistente inteligente que organiza tus notas y lecturas técnicas en segundos. Lee el contenido, descubre su tema principal, extrae las palabras clave y lo guarda en tu historial automáticamente.**