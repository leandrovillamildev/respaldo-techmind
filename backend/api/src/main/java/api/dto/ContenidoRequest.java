package api.dto;

import jakarta.validation.constraints.NotBlank;

public record ContenidoRequest(
        @NotBlank(message = "El título es obligatorio") String titulo,
        @NotBlank(message = "El texto es obligatorio") String texto
) {}
