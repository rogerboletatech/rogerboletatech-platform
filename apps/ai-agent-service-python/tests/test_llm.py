import asyncio

import pytest

from boleta.llm import CircuitBreaker, LLMFake, LLMIndisponivel, LLMResiliente


class LLMQuebrado:
    def __init__(self):
        self.chamadas = 0

    async def completar(self, system, prompt):
        self.chamadas += 1
        raise ConnectionError("provedor fora")


class LLMLento:
    async def completar(self, system, prompt):
        await asyncio.sleep(1)
        return "tarde demais"


class Relogio:
    def __init__(self):
        self.agora = 0.0

    def __call__(self):
        return self.agora


async def test_timeout_estrito_vira_indisponivel():
    llm = LLMResiliente(LLMLento(), timeout_s=0.01)
    with pytest.raises(LLMIndisponivel, match="timeout"):
        await llm.completar("s", "p")


async def test_breaker_abre_e_para_de_chamar_o_provedor():
    provedor = LLMQuebrado()
    llm = LLMResiliente(provedor, breaker=CircuitBreaker(limite_falhas=2))
    for _ in range(2):
        with pytest.raises(LLMIndisponivel):
            await llm.completar("s", "p")
    with pytest.raises(LLMIndisponivel, match="circuito aberto"):
        await llm.completar("s", "p")
    assert provedor.chamadas == 2


def test_breaker_meio_aberto_fecha_no_sucesso_e_reabre_na_falha():
    relogio = Relogio()
    breaker = CircuitBreaker(limite_falhas=1, reset_s=10, relogio=relogio)
    breaker.falha()
    assert breaker.estado == "aberto"
    relogio.agora = 10
    assert breaker.estado == "meio_aberto"
    breaker.falha()
    assert breaker.estado == "aberto"
    relogio.agora = 20
    breaker.sucesso()
    assert breaker.estado == "fechado"


async def test_sucesso_passa_a_resposta():
    assert await LLMResiliente(LLMFake("ok")).completar("s", "p") == "ok"
