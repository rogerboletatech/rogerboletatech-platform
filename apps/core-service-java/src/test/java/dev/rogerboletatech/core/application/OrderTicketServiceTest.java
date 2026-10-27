package dev.rogerboletatech.core.application;

import dev.rogerboletatech.core.adaptador.saida.memoria.OrderTicketRepositorioMemoria;
import dev.rogerboletatech.core.application.servico.OrderTicketService;
import dev.rogerboletatech.core.domain.OrderTicketId;
import dev.rogerboletatech.core.domain.OrderTicketNaoEncontrado;
import org.junit.jupiter.api.Test;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class OrderTicketServiceTest {

	private final Clock relogio = Clock.fixed(Instant.parse("2026-10-27T10:00:00Z"), ZoneOffset.UTC);
	private final OrderTicketService servico = new OrderTicketService(new OrderTicketRepositorioMemoria(), relogio);

	@Test
	void abrirUsaORelogioInjetado() {
		var ordem = servico.abrir("Ana");

		assertThat(ordem.abertoEm()).isEqualTo(relogio.instant());
		assertThat(servico.buscar(ordem.id()).solicitante()).isEqualTo("Ana");
	}

	@Test
	void confirmarPersisteATransicao() {
		var ordem = servico.abrir("Ana");
		servico.confirmar(ordem.id());

		assertThat(servico.buscar(ordem.id()).status().name()).isEqualTo("CONFIRMADO");
	}

	@Test
	void ordemInexistenteLancaNaoEncontrado() {
		var id = OrderTicketId.novo();

		assertThatThrownBy(() -> servico.cancelar(id)).isInstanceOf(OrderTicketNaoEncontrado.class);
	}
}
