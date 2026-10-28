package dev.rogerboletatech.core.adaptador.entrada.web;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class OrderTicketControllerTest {

	@Autowired
	MockMvc mvc;

	@Test
	void abreBuscaConfirmaERecusaSegundaConfirmacao() throws Exception {
		var resposta = mvc.perform(post("/order-tickets")
						.contentType(MediaType.APPLICATION_JSON)
						.content("{\"solicitante\":\"Ana\"}"))
				.andExpect(status().isCreated())
				.andExpect(jsonPath("$.status").value("ABERTO"))
				.andReturn().getResponse().getContentAsString();

		var id = resposta.replaceAll(".*\"id\":\"([^\"]+)\".*", "$1");

		mvc.perform(get("/order-tickets/" + id))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.solicitante").value("Ana"));

		mvc.perform(post("/order-tickets/" + id + "/confirmacao"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.status").value("CONFIRMADO"));

		mvc.perform(post("/order-tickets/" + id + "/confirmacao"))
				.andExpect(status().isConflict());
	}

	@Test
	void ordemInexistenteRetorna404() throws Exception {
		mvc.perform(get("/order-tickets/nao-e-ulid"))
				.andExpect(status().isBadRequest());
		mvc.perform(get("/order-tickets/01ARZ3NDEKTSV4RRFFQ69G5FAV"))
				.andExpect(status().isNotFound());
	}

	@Test
	void solicitanteVazioRetorna400() throws Exception {
		mvc.perform(post("/order-tickets")
						.contentType(MediaType.APPLICATION_JSON)
						.content("{\"solicitante\":\" \"}"))
				.andExpect(status().isBadRequest());
	}
}
