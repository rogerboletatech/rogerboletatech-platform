package dev.rogerboletatech.core.adaptador.entrada.web;

import dev.rogerboletatech.core.application.porta.OrderTicketUseCases;
import dev.rogerboletatech.core.domain.OrderTicket;
import dev.rogerboletatech.core.domain.OrderTicketId;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;

@RestController
@RequestMapping("/order-tickets")
class OrderTicketController {

	private final OrderTicketUseCases casos;

	OrderTicketController(OrderTicketUseCases casos) {
		this.casos = casos;
	}

	record AbrirOrderTicketRequest(@NotBlank @Size(max = 120) String solicitante) {}

	record OrderTicketResponse(String id, String solicitante, Instant abertoEm, String status) {
		static OrderTicketResponse de(OrderTicket ordem) {
			return new OrderTicketResponse(
					ordem.id().valor(),
					ordem.solicitante(),
					ordem.abertoEm(),
					ordem.status().name());
		}
	}

	@PostMapping
	@ResponseStatus(HttpStatus.CREATED)
	OrderTicketResponse abrir(@Valid @RequestBody AbrirOrderTicketRequest corpo) {
		return OrderTicketResponse.de(casos.abrir(corpo.solicitante()));
	}

	@GetMapping("/{id}")
	OrderTicketResponse buscar(@PathVariable String id) {
		return OrderTicketResponse.de(casos.buscar(new OrderTicketId(id)));
	}

	@PostMapping("/{id}/confirmacao")
	OrderTicketResponse confirmar(@PathVariable String id) {
		return OrderTicketResponse.de(casos.confirmar(new OrderTicketId(id)));
	}

	@PostMapping("/{id}/cancelamento")
	OrderTicketResponse cancelar(@PathVariable String id) {
		return OrderTicketResponse.de(casos.cancelar(new OrderTicketId(id)));
	}
}
