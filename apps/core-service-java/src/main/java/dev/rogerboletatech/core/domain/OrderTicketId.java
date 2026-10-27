package dev.rogerboletatech.core.domain;

import com.github.f4b6a3.ulid.Ulid;
import com.github.f4b6a3.ulid.UlidCreator;

import java.util.Objects;

/**
 * Identificador do OrderTicket. ULID e não UUIDv4: ordenável no tempo e sem fragmentar o índice
 * (Diretriz de Trincheira #03).
 */
public record OrderTicketId(String valor) {

	public OrderTicketId {
		Objects.requireNonNull(valor, "id obrigatório");
		if (!Ulid.isValid(valor)) {
			throw new IllegalArgumentException("id não é um ULID válido: " + valor);
		}
	}

	public static OrderTicketId novo() {
		return new OrderTicketId(UlidCreator.getMonotonicUlid().toString());
	}
}
