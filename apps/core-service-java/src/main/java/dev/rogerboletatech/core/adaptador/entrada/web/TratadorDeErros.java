package dev.rogerboletatech.core.adaptador.entrada.web;

import dev.rogerboletatech.core.domain.OrderTicketException;
import dev.rogerboletatech.core.domain.OrderTicketNaoEncontrado;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
class TratadorDeErros {

	@ExceptionHandler(OrderTicketNaoEncontrado.class)
	ProblemDetail naoEncontrado(OrderTicketNaoEncontrado erro) {
		return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, erro.getMessage());
	}

	@ExceptionHandler(OrderTicketException.class)
	ProblemDetail regraDeNegocio(OrderTicketException erro) {
		return ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, erro.getMessage());
	}

	@ExceptionHandler(IllegalArgumentException.class)
	ProblemDetail idInvalido(IllegalArgumentException erro) {
		return ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, erro.getMessage());
	}
}
