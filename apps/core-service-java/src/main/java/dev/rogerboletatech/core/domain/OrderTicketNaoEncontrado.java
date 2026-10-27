package dev.rogerboletatech.core.domain;

public class OrderTicketNaoEncontrado extends RuntimeException {

	public OrderTicketNaoEncontrado(OrderTicketId id) {
		super("OrderTicket não encontrado: " + id.valor());
	}
}
