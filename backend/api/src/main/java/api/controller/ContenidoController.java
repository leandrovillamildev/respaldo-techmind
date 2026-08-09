package api.controller;

import api.dto.ContenidoRequest;
import api.dto.PrediccionResponse;
import api.service.PrediccionService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/contenido")
@CrossOrigin(origins = "*")
public class ContenidoController {

    private final PrediccionService prediccionService;

    public ContenidoController(PrediccionService prediccionService) {
        this.prediccionService = prediccionService;
    }

    @PostMapping
    public ResponseEntity<PrediccionResponse> clasificarContenido(@Valid @RequestBody ContenidoRequest request) {
        PrediccionResponse response = prediccionService.clasificar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminarContenido(@PathVariable Long id) {
        boolean eliminado = prediccionService.eliminarPrediccion(id);
        if (eliminado) {
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}
