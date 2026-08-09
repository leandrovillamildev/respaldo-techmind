package api.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "predicciones")
@Getter
@Setter
@NoArgsConstructor
public class Prediccion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "contenido_id", nullable = false)
    private Contenido contenido;

    @Column(nullable = false)
    private String categoria;

    @Column(nullable = false)
    private Double probabilidad;

    // Guardadas como texto separado por coma en la DB, expuestas como lista en la app
    @Column(name = "palabras_clave", nullable = false, columnDefinition = "TEXT")
    private String palabrasClave;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    public Prediccion(Contenido contenido, String categoria, Double probabilidad, List<String> palabrasClave) {
        this.contenido = contenido;
        this.categoria = categoria;
        this.probabilidad = probabilidad;
        this.palabrasClave = String.join(",", palabrasClave);
    }

    public List<String> getPalabrasClaveList() {
        return List.of(palabrasClave.split(","));
    }
}
