package dev.rogerboletatech.core.application.porta;

import dev.rogerboletatech.core.domain.OrderTicket;
import dev.rogerboletatech.core.domain.OrderTicketId;

/** Porta de entrada: o que o mundo de fora pode pedir ao core. */
public interface OrderTicketUseCases {

	OrderTicket abrir(String solicitante);

	OrderTicket buscar(OrderTicketId id);

	OrderTicket confirmar(OrderTicketId id);

	OrderTicket cancelar(OrderTicketId id);
}
