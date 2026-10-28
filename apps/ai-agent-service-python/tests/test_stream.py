import json
import re

from fastapi.testclient import TestClient

from boleta.llm import LLMFake
from main import criar_app


class LLMQuebrado:
    async def completar(self, system, prompt):
        raise ConnectionError("provedor fora")


def eventos_do_stream(cliente, pergunta):
    corpo = cliente.post("/boleta/perguntar/stream", json={"pergunta": pergunta}).text
    eventos = []
    for bloco in corpo.strip().split("\n\n"):
        linhas = dict(linha.split(": ", 1) for linha in bloco.splitlines())
        eventos.append((linhas["event"], json.loads(linhas["data"])))
    return eventos


def test_stream_emite_um_passo_por_nó_e_resposta_no_fim():
    eventos = eventos_do_stream(TestClient(criar_app(LLMFake("Use ShedLock."))), "meu @Scheduled roda em 4 pods")
    passos = [dados for nome, dados in eventos if nome == "passo"]
    assert [p["step"] for p in passos] == ["guarda_entrada", "busca_diretrizes", "responder", "guarda_saida"]
    assert [p["ordem"] for p in passos] == [1, 2, 3, 4]
    assert eventos[-1][0] == "resposta"
    assert eventos[-1][1]["resposta"] == "Use ShedLock."


def test_passos_compartilham_interacao_e_trace():
    eventos = eventos_do_stream(TestClient(criar_app(LLMFake("ok"))), "meu @Scheduled roda em 4 pods")
    dados = [d for nome, d in eventos if nome == "passo"]
    assert len({d["interacaoId"] for d in dados}) == 1
    assert len(dados[0]["interacaoId"]) == 26
    assert all(re.fullmatch(r"[0-9a-f]{32}", d["traceId"]) for d in dados)


def test_stream_marca_fallback_quando_llm_cai():
    eventos = eventos_do_stream(TestClient(criar_app(LLMQuebrado())), "meu @Scheduled roda em 4 pods")
    resposta = eventos[-1][1]
    assert resposta["fallback"] is True
    assert "#01" in resposta["resposta"]


def test_stream_bloqueia_entrada_fora_de_escopo_sem_chamar_llm():
    eventos = eventos_do_stream(TestClient(criar_app(LLMQuebrado())), "devo investir em ações?")
    passos = [d for nome, d in eventos if nome == "passo"]
    assert [p["step"] for p in passos] == ["guarda_entrada"]
    assert eventos[-1][1]["bloqueada"] is True
