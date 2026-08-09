# Dockerfile — Frontend Web UI (TechMind)
FROM nginx:alpine

# Copiar archivos estáticos del frontend al directorio de Nginx
COPY frontend/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
