package api.dto;

import java.util.List;

public record PrediccionResponse(
        String categoria,
        Double probabilidad,
        List<String> informaciones_adicionales
) {}
