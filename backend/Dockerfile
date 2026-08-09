# Dockerfile — Backend Spring Boot Java 17 (TechMind)
FROM eclipse-temurin:17-jdk AS build
WORKDIR /app

# Copiar configuración Maven y código fuente
COPY backend/api/mvnw .
COPY backend/api/.mvn .mvn
COPY backend/api/pom.xml .
COPY backend/api/src src

# Sanitizar saltos de línea de Windows (CRLF -> LF), dar permisos de ejecución y compilar jar
RUN sed -i 's/\r$//' mvnw && chmod +x mvnw && ./mvnw package -DskipTests

# Etapa 2 — Imagen liviana de ejecución
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080
# Límites de memoria para OCI Free Tier / servidores con RAM limitada (1–2 GB).
# -Xms64m     : Heap inicial de 64 MB (no reserva RAM de más al arrancar)
# -Xmx256m    : Heap máximo de 256 MB (evita que el OOM Killer del kernel mate el proceso)
# -XX:+UseSerialGC : GC serie, consume menos overhead en CPUs de 1–2 núcleos
ENTRYPOINT ["java", \
  "-Xms64m", "-Xmx256m", \
  "-XX:+UseSerialGC", \
  "-jar", "app.jar"]
