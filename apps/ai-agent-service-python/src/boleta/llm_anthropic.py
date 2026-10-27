"""Adaptador do LLM real: Claude via SDK oficial `anthropic`.

Implementa o Protocol `boleta.llm.LLM`. O grafo não sabe que existe; quem liga é `main.py`.
Modelo padrão: `claude-haiku-5-5`, o mais barato da família, pedido explicitamente pelo Roger
(a ficha técnica manda economizar tokens). Para trocar, passe `modelo=` ou use BOLETA_MODELO.
"""

import os

from anthropic import AsyncAnthropic

from boleta.llm import LLMIndisponivel

MODELO_PADRAO = "claude-haiku-5-5"
MAX_TOKENS_PADRAO = 1024


class LLMAnthropic:
    def __init__(
        self,
        cliente: AsyncAnthropic | None = None,
        modelo: str | None = None,
        max_tokens: int = MAX_TOKENS_PADRAO,
    ):
        # Sem api_key explícita, o SDK lê ANTHROPIC_API_KEY do ambiente. Nunca hardcode chave.
        self.cliente = cliente or AsyncAnthropic(max_retries=0)
        self.modelo = modelo or os.getenv("BOLETA_MODELO", MODELO_PADRAO)
        self.max_tokens = max_tokens

    async def completar(self, system: str, prompt: str) -> str:
        resposta = await self.cliente.messages.create(
            model=self.modelo,
            max_tokens=self.max_tokens,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        # Recusa de segurança não é resposta: vira falha, e o grafo cai no fallback.
        if resposta.stop_reason == "refusal":
            raise LLMIndisponivel("recusa do provedor")
        texto = "".join(bloco.text for bloco in resposta.content if bloco.type == "text")
        if not texto.strip():
            raise LLMIndisponivel("resposta vazia")
        return texto
