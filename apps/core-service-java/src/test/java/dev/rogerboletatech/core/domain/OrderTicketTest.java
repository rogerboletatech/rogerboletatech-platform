package dev.rogerboletatech.core.domain;

import org.junit.jupiter.api.Test;

import java.time.Instant;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class OrderTicketTest {

	private static final Instant AGORA = Instant.parse("2026-10-27T10:00:00Z");

	@Test
	void abreEmStatusAbertoComIdUlid() {
		var ordem = OrderTicket.abrir("  Ana  ", AGORA);

		assertThat(ordem.status()).isEqualTo(StatusOrderTicket.ABERTO);
		assertThat(ordem.solicitante()).isEqualTo("Ana");
		assertThat(ordem.id().valor()).hasSize(26);
	}

	@Test
	void recusaSolicitanteVazio() {
		assertThatThrownBy(() -> OrderTicket.abrir("   ", AGORA))
				.isInstanceOf(OrderTicketException.class)
				.hasMessageContaining("solicitante");
	}

	@Test
	void confirmaSoQuandoAberto() {
		var ordem = OrderTicket.abrir("Ana", AGORA);
		ordem.confirmar();

		assertThat(ordem.status()).isEqualTo(StatusOrderTicket.CONFIRMADO);
		assertThatThrownBy(ordem::confirmar).isInstanceOf(OrderTicketException.class);
		assertThatThrownBy(ordem::cancelar).isInstanceOf(OrderTicketException.class);
	}

	@Test
	void cancelaSoQuandoAberto() {
		var ordem = OrderTicket.abrir("Ana", AGORA);
		ordem.cancelar();

		assertThat(ordem.status()).isEqualTo(StatusOrderTicket.CANCELADO);
		assertThatThrownBy(ordem::confirmar).isInstanceOf(OrderTicketException.class);
	}

	@Test
	void recusaIdQueNaoEhUlid() {
		assertThatThrownBy(() -> new OrderTicketId("nao-e-ulid"))
				.isInstanceOf(IllegalArgumentException.class);
	}
}
