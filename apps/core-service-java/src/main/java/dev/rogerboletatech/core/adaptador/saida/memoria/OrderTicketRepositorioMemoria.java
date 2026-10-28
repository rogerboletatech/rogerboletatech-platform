package dev.rogerboletatech.core.adaptador.saida.memoria;

import dev.rogerboletatech.core.application.porta.OrderTicketRepository;
import dev.rogerboletatech.core.domain.OrderTicket;
import dev.rogerboletatech.core.domain.OrderTicketId;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

/** Adaptador de saída em memória. Troca por JPA quando o modelo de persistência for decidido. */
public class OrderTicketRepositorioMemoria implements OrderTicketRepository {

	private final Map<OrderTicketId, OrderTicket> ordens = new ConcurrentHashMap<>();

	@Override
	public void salvar(OrderTicket ordem) {
		ordens.put(ordem.id(), ordem);
	}

	@Override
	public Optional<OrderTicket> buscar(OrderTicketId id) {
		return Optional.ofNullable(ordens.get(id));
	}
}
