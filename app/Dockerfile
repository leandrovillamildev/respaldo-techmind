# Dockerfile — Microservicio FastAPI de Ciencia de Datos (TechMind)
FROM python:3.12-slim

WORKDIR /workspace

# Evita la generación de archivos .pyc y fuerza unbuffered stdout
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MODEL_PATH=./data-science/models

# Instalar dependencias
COPY data-science/requirements.txt ./data-science/requirements.txt
RUN pip install --no-cache-dir -r data-science/requirements.txt

# Copiar la aplicación y los modelos serializados (.joblib)
COPY app/ ./app/
COPY data-science/models/ ./data-science/models/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
