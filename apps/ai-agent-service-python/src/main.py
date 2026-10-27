"""API do ai-agent-service. Chamada pelo BFF, que propaga o `traceparent` W3C."""

from fastapi import FastAPI, Request
from opentelemetry.propagate import extract
from pydantic import BaseModel, Field

from boleta.graph import Passo, construir_grafo
from boleta.llm import LLM, LLMFake, LLMResiliente
from boleta.telemetry import tracer


class PerguntaIn(BaseModel):
    pergunta: str = Field(max_length=4000)


class RespostaOut(BaseModel):
    resposta: str
    autor: str = "Boleta (agente de IA)"
    fallback: bool
    bloqueada: bool
    passos: list[Passo]


def criar_app(provedor: LLM | None = None) -> FastAPI:
    # Provedor real ainda em aberto (ficha técnica, seção 9): por padrão, modo simulação.
    llm = LLMResiliente(provedor or LLMFake())
    grafo = construir_grafo(llm)
    app = FastAPI(title="ai-agent-service", version="0.1.0")

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok", "llm_breaker": llm.breaker.estado}

    @app.post("/boleta/perguntar", response_model=RespostaOut)
    async def perguntar(corpo: PerguntaIn, request: Request) -> RespostaOut:
        contexto = extract(dict(request.headers))
        with tracer.start_as_current_span("boleta.interacao", context=contexto):
            estado = await grafo.ainvoke({"pergunta": corpo.pergunta, "passos": []})
        return RespostaOut(
            resposta=estado["resposta"],
            fallback=estado.get("fallback", False),
            bloqueada=estado.get("bloqueada", False),
            passos=estado["passos"],
        )

    return app


app = criar_app()
