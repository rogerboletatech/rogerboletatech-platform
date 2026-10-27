package dev.rogerboletatech.core.domain;

import java.time.Instant;
import java.util.Objects;

/**
 * Pedido de ordem corporativa. Agregado raiz do core-service.
 *
 * <p>Transições válidas: ABERTO → CONFIRMADO, ABERTO → CANCELADO.
 * Qualquer outra transição é recusada, sem exceção silenciosa.
 */
public final class OrderTicket {

	private final OrderTicketId id;
	private final String solicitante;
	private final Instant abertoEm;
	private StatusOrderTicket status;

	private OrderTicket(OrderTicketId id, String solicitante, Instant abertoEm, StatusOrderTicket status) {
		this.id = Objects.requireNonNull(id);
		this.solicitante = Objects.requireNonNull(solicitante);
		this.abertoEm = Objects.requireNonNull(abertoEm);
		this.status = Objects.requireNonNull(status);
	}

	public static OrderTicket abrir(String solicitante, Instant agora) {
		if (solicitante == null || solicitante.isBlank()) {
			throw new OrderTicketException("solicitante é obrigatório");
		}
		return new OrderTicket(OrderTicketId.novo(), solicitante.strip(), agora, StatusOrderTicket.ABERTO);
	}

	/** Reconstrói a partir do armazenamento. Não aplica transições. */
	public static OrderTicket restaurar(OrderTicketId id, String solicitante, Instant abertoEm, StatusOrderTicket status) {
		return new OrderTicket(id, solicitante, abertoEm, status);
	}

	public void confirmar() {
		exigir(StatusOrderTicket.ABERTO, "só é possível confirmar um OrderTicket aberto");
		this.status = StatusOrderTicket.CONFIRMADO;
	}

	public void cancelar() {
		exigir(StatusOrderTicket.ABERTO, "só é possível cancelar um OrderTicket aberto");
		this.status = StatusOrderTicket.CANCELADO;
	}

	private void exigir(StatusOrderTicket esperado, String mensagem) {
		if (status != esperado) {
			throw new OrderTicketException(mensagem + " (status atual: " + status + ")");
		}
	}

	public OrderTicketId id() {
		return id;
	}

	public String solicitante() {
		return solicitante;
	}

	public Instant abertoEm() {
		return abertoEm;
	}

	public StatusOrderTicket status() {
		return status;
	}
}
