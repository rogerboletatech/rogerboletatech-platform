"""Porta para o provedor de LLM, com timeout estrito e circuit breaker (Módulo 5).

O provedor ainda é questão em aberto (ficha técnica, seção 9). Por isso o grafo
depende só do Protocol `LLM`; o adaptador real entra depois sem tocar no grafo.
"""

import asyncio
import time
from typing import Protocol


class LLM(Protocol):
    async def completar(self, system: str, prompt: str) -> str: ...


class LLMIndisponivel(Exception):
    """O cérebro caiu: timeout, erro do provedor ou circuito aberto."""


class CircuitBreaker:
    """Abre após `limite_falhas` falhas seguidas; tenta de novo (half-open) após `reset_s`."""

    def __init__(self, limite_falhas: int = 3, reset_s: float = 30.0, relogio=time.monotonic):
        self.limite_falhas = limite_falhas
        self.reset_s = reset_s
        self._relogio = relogio
        self._falhas = 0
        self._aberto_em: float | None = None

    @property
    def estado(self) -> str:
        if self._aberto_em is None:
            return "fechado"
        if self._relogio() - self._aberto_em >= self.reset_s:
            return "meio_aberto"
        return "aberto"

    def permite(self) -> bool:
        return self.estado != "aberto"

    def sucesso(self) -> None:
        self._falhas = 0
        self._aberto_em = None

    def falha(self) -> None:
        self._falhas += 1
        if self.estado == "meio_aberto" or self._falhas >= self.limite_falhas:
            self._aberto_em = self._relogio()


class LLMResiliente:
    def __init__(self, provedor: LLM, timeout_s: float = 8.0, breaker: CircuitBreaker | None = None):
        self.provedor = provedor
        self.timeout_s = timeout_s
        self.breaker = breaker or CircuitBreaker()

    async def completar(self, system: str, prompt: str) -> str:
        if not self.breaker.permite():
            raise LLMIndisponivel("circuito aberto")
        try:
            resposta = await asyncio.wait_for(self.provedor.completar(system, prompt), self.timeout_s)
        except Exception as erro:
            self.breaker.falha()
            motivo = "timeout" if isinstance(erro, TimeoutError) else type(erro).__name__
            raise LLMIndisponivel(motivo) from erro
        self.breaker.sucesso()
        return resposta


class LLMFake:
    """Provedor determinístico para testes e para o modo simulação."""

    def __init__(self, resposta: str = "Resposta curta: depende do direcionador. Qual é o seu?"):
        self.resposta = resposta

    async def completar(self, system: str, prompt: str) -> str:
        return self.resposta
