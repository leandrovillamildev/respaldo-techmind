package api.service;

import api.dto.ContenidoRequest;
import api.dto.PrediccionResponse;
import api.model.Contenido;
import api.model.Prediccion;
import api.repository.ContenidoRepository;
import api.repository.PrediccionRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class PrediccionService {

    private final ContenidoRepository contenidoRepository;
    private final PrediccionRepository prediccionRepository;
    private final String dsApiUrl;
    private final HttpClient httpClient;

    public PrediccionService(ContenidoRepository contenidoRepository,
                             PrediccionRepository prediccionRepository,
                             @Value("${techmind.ds.api.url}") String dsApiUrl) {
        this.contenidoRepository = contenidoRepository;
        this.prediccionRepository = prediccionRepository;
        this.dsApiUrl = dsApiUrl;
        this.httpClient = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_1_1)
                .connectTimeout(Duration.ofSeconds(5))
                .build();
    }

    /**
     * Orquesta el flujo completo de clasificación.
     *
     * BUG-4 (resuelto 2026-07-27): La llamada HTTP a FastAPI se realiza FUERA
     * de cualquier transacción para no mantener la conexión a PostgreSQL abierta
     * durante la espera de respuesta del modelo ML (hasta 10 s), lo que agotaba
     * el pool de conexiones bajo carga concurrente.
     */
    public PrediccionResponse clasificar(ContenidoRequest request) {
        // 1. Persistir el contenido — transacción corta y acotada
        Contenido contenido = guardarContenido(request);

        // 2. Llamar a FastAPI FUERA de transacción — puede tardar hasta 10 s
        PrediccionResponse resultado = llamarFastApi(request);

        // 3. Persistir la predicción — segunda transacción corta y acotada
        guardarPrediccion(contenido, resultado);

        return resultado;
    }

    // ── Paso 1: guardar contenido (transacción propia) ────────────────────────

    @Transactional
    protected Contenido guardarContenido(ContenidoRequest request) {
        Contenido contenido = new Contenido(request.titulo(), request.texto());
        return contenidoRepository.save(contenido);
    }

    // ── Paso 2: llamar a FastAPI (sin transacción) ────────────────────────────

    private PrediccionResponse llamarFastApi(ContenidoRequest request) {
        String jsonBody = "{\"titulo\":\"" + escapeJson(request.titulo())
                + "\",\"texto\":\"" + escapeJson(request.texto()) + "\"}";

        HttpRequest httpRequest = HttpRequest.newBuilder()
                .uri(URI.create(dsApiUrl + "/predecir"))
                .header("Content-Type", "application/json")
                .timeout(Duration.ofSeconds(10))
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

        String responseBody;
        int statusCode;
        try {
            HttpResponse<String> httpResponse = httpClient.send(httpRequest, HttpResponse.BodyHandlers.ofString());
            statusCode = httpResponse.statusCode();
            responseBody = httpResponse.body();
        } catch (IOException | InterruptedException ex) {
            throw new DsServiceUnavailableException(
                    "No se pudo contactar al servicio de clasificación (FastAPI): " + ex.getMessage(), ex);
        }

        if (statusCode < 200 || statusCode >= 300) {
            throw new DsServiceUnavailableException(
                    "El servicio de clasificación respondió con error " + statusCode + ": " + responseBody, null);
        }

        return parseResponse(responseBody);
    }

    // ── Paso 3: guardar predicción (transacción propia) ───────────────────────

    @Transactional
    protected void guardarPrediccion(Contenido contenido, PrediccionResponse resultado) {
        Prediccion prediccion = new Prediccion(
                contenido,
                resultado.categoria(),
                resultado.probabilidad(),
                resultado.informaciones_adicionales()
        );
        prediccionRepository.save(prediccion);
    }

    @Transactional
    public boolean eliminarPrediccion(Long prediccionId) {
        return prediccionRepository.findById(prediccionId).map(prediccion -> {
            Contenido contenido = prediccion.getContenido();
            prediccionRepository.delete(prediccion);
            if (contenido != null) {
                contenidoRepository.delete(contenido);
            }
            return true;
        }).orElse(false);
    }


    // ── Parser de la respuesta JSON de FastAPI ────────────────────────────────

    /**
     * BUG-3 (resuelto 2026-07-27): Se agregaron null-checks en todos los campos
     * parseados. Si FastAPI devuelve un JSON malformado o con campos faltantes,
     * se lanza DsServiceUnavailableException con un mensaje descriptivo en lugar
     * de un NullPointerException opaco que producía HTTP 500.
     * También se corrigió la regex de extractDouble para manejar 0.0, 1.0 y
     * valores en notación científica (p. ej. 1.0e-2).
     */
    private PrediccionResponse parseResponse(String json) {
        String categoria = extractString(json, "categoria");
        Double probabilidad = extractDouble(json, "probabilidad");
        List<String> keywords = extractStringArray(json, "informaciones_adicionales");

        if (categoria == null || categoria.isBlank()) {
            throw new DsServiceUnavailableException(
                    "Respuesta inválida del servicio ML: falta el campo 'categoria'. Respuesta recibida: " + json, null);
        }
        if (probabilidad == null) {
            throw new DsServiceUnavailableException(
                    "Respuesta inválida del servicio ML: falta el campo 'probabilidad'. Respuesta recibida: " + json, null);
        }

        return new PrediccionResponse(categoria, probabilidad, keywords);
    }

    private String extractString(String json, String field) {
        Matcher m = Pattern.compile("\"" + field + "\"\\s*:\\s*\"([^\"]*)\"").matcher(json);
        return m.find() ? m.group(1) : null;
    }

    /**
     * Regex corregida: acepta enteros, decimales y notación científica
     * (ej: 0, 1, 0.97, 1.0e-2). La versión anterior con [0-9.]+ fallaba
     * con valores 0 exacto y con exponentes.
     */
    private Double extractDouble(String json, String field) {
        Matcher m = Pattern.compile("\"" + field + "\"\\s*:\\s*([0-9]*\\.?[0-9]+(?:[eE][+-]?[0-9]+)?)").matcher(json);
        return m.find() ? Double.valueOf(m.group(1)) : null;
    }

    private List<String> extractStringArray(String json, String field) {
        Matcher m = Pattern.compile("\"" + field + "\"\\s*:\\s*\\[([^\\]]*)\\]").matcher(json);
        java.util.List<String> result = new java.util.ArrayList<>();
        if (m.find()) {
            Matcher items = Pattern.compile("\"([^\"]*)\"").matcher(m.group(1));
            while (items.find()) {
                result.add(items.group(1));
            }
        }
        return result;
    }

    private static String escapeJson(String value) {
        if (value == null) return "";
        return value.replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t");
    }

    public static class DsServiceUnavailableException extends RuntimeException {
        public DsServiceUnavailableException(String message, Throwable cause) {
            super(message, cause);
        }
    }
}