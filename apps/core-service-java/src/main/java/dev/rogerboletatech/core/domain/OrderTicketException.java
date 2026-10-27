package dev.rogerboletatech.core.domain;

/** Violação de regra de negócio do OrderTicket. */
public class OrderTicketException extends RuntimeException {

	public OrderTicketException(String mensagem) {
		super(mensagem);
	}
}
