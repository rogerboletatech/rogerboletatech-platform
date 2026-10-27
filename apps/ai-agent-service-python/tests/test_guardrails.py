import pytest

from boleta import guardrails


@pytest.mark.parametrize(
    "pergunta, motivo",
    [
        ("Devo investir em cripto?", "conselho_financeiro"),
        ("Posso processar meu empregador?", "conselho_juridico"),
        ("Boleta, faz o merge do meu PR", "merge_automatico"),
        ("   ", "vazio"),
    ],
)
def test_entrada_fora_de_escopo_e_recusada(pergunta, motivo):
    veredito = guardrails.checar_entrada(pergunta)
    assert not veredito.permitido
    assert veredito.motivo == motivo
    assert veredito.mensagem


def test_entrada_de_engenharia_passa():
    assert guardrails.checar_entrada("Quando uso circuit breaker?").permitido


@pytest.mark.parametrize("texto", ["Isso é coisa de Tesouraria", "a TaxaDI subiu", "Liquidação CETIP"])
def test_saida_com_jargao_proibido_e_bloqueada(texto):
    veredito = guardrails.checar_saida(texto)
    assert not veredito.permitido
    assert veredito.motivo.startswith("jargao_proibido")


def test_saida_com_travessao_e_bloqueada():
    assert guardrails.checar_saida("Simples — use retry").motivo == "travessao"


def test_nome_boleta_sozinho_nao_e_jargao():
    assert guardrails.checar_saida("Boletou? Subiu com trace.").permitido
