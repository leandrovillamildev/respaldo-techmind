-- V1__create_tables.sql
-- Tablas base de TechMind: contenidos ingresados y predicciones del modelo ML

CREATE TABLE contenidos (
    id          BIGSERIAL PRIMARY KEY,
    titulo      VARCHAR(255) NOT NULL,
    texto       TEXT NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE predicciones (
    id                      BIGSERIAL PRIMARY KEY,
    contenido_id            BIGINT NOT NULL REFERENCES contenidos(id) ON DELETE CASCADE,
    categoria               VARCHAR(100) NOT NULL,
    probabilidad            DOUBLE PRECISION NOT NULL,
    palabras_clave          TEXT NOT NULL, -- keywords separadas por coma
    created_at              TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_predicciones_contenido_id ON predicciones(contenido_id);
