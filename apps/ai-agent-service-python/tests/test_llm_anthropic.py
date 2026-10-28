from types import SimpleNamespace

import pytest

from boleta.llm import LLMIndisponivel, LLMResiliente
from boleta.llm_anthropic import LLMAnthropic, MODELO_PADRAO


class MensagensFalsas:
    def __init__(self, resposta=None, erro=None):
        self.resposta = resposta
        self.erro = erro
        self.chamada = None

    async def create(self, **kwargs):
        self.chamada = kwargs
        if self.erro:
            raise self.erro
        return self.resposta


def cliente_falso(mensagens):
    return SimpleNamespace(messages=mensagens)


def resposta(*blocos, stop_reason="end_turn"):
    return SimpleNamespace(
        stop_reason=stop_reason,
        content=[SimpleNamespace(type=t, text=txt) for t, txt in blocos],
    )


async def test_envia_system_modelo_padrao_e_junta_blocos_de_texto():
    mensagens = MensagensFalsas(resposta(("thinking", ""), ("text", "Use ShedLock."), ("text", " Pronto.")))
    llm = LLMAnthropic(cliente=cliente_falso(mensagens))

    texto = await llm.completar("persona", "pergunta")

    assert texto == "Use ShedLock. Pronto."
    assert mensagens.chamada["model"] == MODELO_PADRAO == "claude-haiku-5-5"
    assert mensagens.chamada["system"] == "persona"
    assert mensagens.chamada["messages"] == [{"role": "user", "content": "pergunta"}]


async def test_recusa_vira_indisponivel():
    llm = LLMAnthropic(cliente=cliente_falso(MensagensFalsas(resposta(stop_reason="refusal"))))
    with pytest.raises(LLMIndisponivel, match="recusa"):
        await llm.completar("s", "p")


async def test_resposta_so_com_thinking_vira_indisponivel():
    llm = LLMAnthropic(cliente=cliente_falso(MensagensFalsas(resposta(("thinking", "")))))
    with pytest.raises(LLMIndisponivel, match="vazia"):
        await llm.completar("s", "p")


async def test_erro_do_sdk_passa_pelo_breaker_e_vira_fallback():
    erro = ConnectionError("rede caiu")
    llm = LLMResiliente(LLMAnthropic(cliente=cliente_falso(MensagensFalsas(erro=erro))))
    with pytest.raises(LLMIndisponivel):
        await llm.completar("s", "p")
    assert llm.breaker.estado == "fechado"  # uma falha só não abre o circuito


def test_modelo_pode_vir_do_ambiente(monkeypatch):
    monkeypatch.setenv("BOLETA_MODELO", "claude-sonnet-5-5")
    assert LLMAnthropic(cliente=cliente_falso(None)).modelo == "claude-sonnet-5-5"
