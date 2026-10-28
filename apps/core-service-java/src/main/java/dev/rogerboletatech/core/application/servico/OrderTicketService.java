package dev.rogerboletatech.core.application.servico;

import dev.rogerboletatech.core.application.porta.OrderTicketRepository;
import dev.rogerboletatech.core.application.porta.OrderTicketUseCases;
import dev.rogerboletatech.core.domain.OrderTicket;
import dev.rogerboletatech.core.domain.OrderTicketId;
import dev.rogerboletatech.core.domain.OrderTicketNaoEncontrado;

import java.time.Clock;

public class OrderTicketService implements OrderTicketUseCases {

	private final OrderTicketRepository repositorio;
	private final Clock relogio;

	public OrderTicketService(OrderTicketRepository repositorio, Clock relogio) {
		this.repositorio = repositorio;
		this.relogio = relogio;
	}

	@Override
	public OrderTicket abrir(String solicitante) {
		var ordem = OrderTicket.abrir(solicitante, relogio.instant());
		repositorio.salvar(ordem);
		return ordem;
	}

	@Override
	public OrderTicket buscar(OrderTicketId id) {
		return carregar(id);
	}

	@Override
	public OrderTicket confirmar(OrderTicketId id) {
		var ordem = carregar(id);
		ordem.confirmar();
		repositorio.salvar(ordem);
		return ordem;
	}

	@Override
	public OrderTicket cancelar(OrderTicketId id) {
		var ordem = carregar(id);
		ordem.cancelar();
		repositorio.salvar(ordem);
		return ordem;
	}

	private OrderTicket carregar(OrderTicketId id) {
		return repositorio.buscar(id).orElseThrow(() -> new OrderTicketNaoEncontrado(id));
	}
}
