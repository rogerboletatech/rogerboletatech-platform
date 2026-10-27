package dev.rogerboletatech.core.application.porta;

import dev.rogerboletatech.core.domain.OrderTicket;
import dev.rogerboletatech.core.domain.OrderTicketId;

import java.util.Optional;

/** Porta de saída: o domínio não sabe se o dado mora em memória, Postgres ou outro lugar. */
public interface OrderTicketRepository {

	void salvar(OrderTicket ordem);

	Optional<OrderTicket> buscar(OrderTicketId id);
}
