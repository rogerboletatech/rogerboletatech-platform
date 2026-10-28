package dev.rogerboletatech.core;

import dev.rogerboletatech.core.adaptador.saida.memoria.OrderTicketRepositorioMemoria;
import dev.rogerboletatech.core.application.porta.OrderTicketRepository;
import dev.rogerboletatech.core.application.porta.OrderTicketUseCases;
import dev.rogerboletatech.core.application.servico.OrderTicketService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Clock;

/** Liga as portas aos adaptadores. É o único lugar que conhece as duas pontas. */
@Configuration
class ConfiguracaoOrderTicket {

	@Bean
	OrderTicketRepository orderTicketRepository() {
		return new OrderTicketRepositorioMemoria();
	}

	@Bean
	OrderTicketUseCases orderTicketUseCases(OrderTicketRepository repositorio) {
		return new OrderTicketService(repositorio, Clock.systemUTC());
	}
}
