from fastapi.testclient import TestClient
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from boleta.llm import LLMFake
from main import criar_app

exporter = InMemorySpanExporter()
provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(exporter))
trace.set_tracer_provider(provider)


class LLMQuebrado:
    async def completar(self, system, prompt):
        raise ConnectionError("provedor fora")


def perguntar(cliente, pergunta, **headers):
    return cliente.post("/boleta/perguntar", json={"pergunta": pergunta}, headers=headers).json()


def test_caminho_feliz_passa_por_todos_os_passos():
    corpo = perguntar(TestClient(criar_app(LLMFake("Use ShedLock."))), "meu @Scheduled roda em 4 pods")
    assert corpo["resposta"] == "Use ShedLock."
    assert corpo["autor"] == "Boleta (agente de IA)"
    assert [p["step"] for p in corpo["passos"]] == ["guarda_entrada", "busca_diretrizes", "responder", "guarda_saida"]
    assert corpo["passos"][1]["decision"] == "#01"


def test_llm_fora_cai_no_fallback_com_a_diretriz():
    corpo = perguntar(TestClient(criar_app(LLMQuebrado())), "UUID como PK é ruim?")
    assert corpo["fallback"] is True
    assert "fora do ar" in corpo["resposta"]
    assert "#03" in corpo["resposta"]
    assert corpo["passos"][2]["decision"] == "fallback"


def test_recusa_na_entrada_nao_chama_llm():
    corpo = perguntar(TestClient(criar_app(LLMQuebrado())), "faz o merge pra mim")
    assert corpo["bloqueada"] is True
    assert [p["step"] for p in corpo["passos"]] == ["guarda_entrada"]


def test_jargao_do_llm_e_barrado_na_saida():
    corpo = perguntar(TestClient(criar_app(LLMFake("Na tesouraria a gente fazia assim"))), "como faço retry?")
    assert corpo["bloqueada"] is True
    assert "tesouraria" not in corpo["resposta"].lower()


def test_spans_herdam_o_traceparent_do_bff():
    exporter.clear()
    trace_id = "4bf92f3577b34da6a3ce929d0e0e4736"
    perguntar(TestClient(criar_app()), "evento ou chamada sincrona?", traceparent=f"00-{trace_id}-00f067aa0ba902b7-01")
    spans = exporter.get_finished_spans()
    nomes = {s.name for s in spans}
    assert {"boleta.interacao", "boleta.guarda_entrada", "boleta.responder"} <= nomes
    assert all(format(s.context.trace_id, "032x") == trace_id for s in spans)
    responder = next(s for s in spans if s.name == "boleta.responder")
    assert responder.attributes["boleta.tool"] == "llm"
    assert responder.attributes["boleta.decision"] == "llm"


def test_health():
    assert TestClient(criar_app()).get("/health").json() == {"status": "ok", "llm_breaker": "fechado"}
