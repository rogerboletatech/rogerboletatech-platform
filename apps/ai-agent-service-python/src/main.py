"""API do ai-agent-service. Chamada pelo BFF, que propaga o `traceparent` W3C."""

import json
import os
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from opentelemetry.propagate import extract
from pydantic import BaseModel, Field

from boleta.graph import Passo, construir_grafo
from boleta.llm import LLM, LLMFake, LLMResiliente
from boleta.llm_anthropic import LLMAnthropic
from boleta.telemetry import tracer
from boleta.ulid import gerar_ulid


class PerguntaIn(BaseModel):
    pergunta: str = Field(max_length=4000)


class RespostaOut(BaseModel):
    resposta: str
    autor: str = "Boleta (agente de IA)"
    fallback: bool
    bloqueada: bool
    passos: list[Passo]


def criar_app(provedor: LLM | None = None) -> FastAPI:
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

    @app.post("/boleta/perguntar/stream")
    async def perguntar_stream(corpo: PerguntaIn, request: Request) -> StreamingResponse:
        contexto = extract(dict(request.headers))

        async def eventos():
            interacao = gerar_ulid()
            ordem = 0
            estado: dict = {}
            with tracer.start_as_current_span("boleta.interacao", context=contexto) as span:
                trace_id = format(span.get_span_context().trace_id, "032x")
                async for atualizacao in grafo.astream({"pergunta": corpo.pergunta, "passos": []}, stream_mode="updates"):
                    for dados in atualizacao.values():
                        for passo_feito in dados.get("passos", []):
                            ordem += 1
                            yield _evento(
                                "passo",
                                {
                                    "interacaoId": interacao,
                                    "ordem": ordem,
                                    "step": passo_feito["step"],
                                    "decision": passo_feito["decision"],
                                    "detalhe": passo_feito["detalhe"],
                                    "traceId": trace_id,
                                    "emitidoEm": _agora(),
                                },
                            )
                        estado.update({k: v for k, v in dados.items() if k != "passos"})
                yield _evento(
                    "resposta",
                    {
                        "interacaoId": interacao,
                        "resposta": estado.get("resposta", ""),
                        "autor": "Boleta (agente de IA)",
                        "fallback": estado.get("fallback", False),
                        "bloqueada": estado.get("bloqueada", False),
                    },
                )

        return StreamingResponse(eventos(), media_type="text/event-stream")

    return app


def _evento(nome: str, dados: dict) -> str:
    return f"event: {nome}\ndata: {json.dumps(dados, ensure_ascii=False)}\n\n"


def _agora() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def provedor_padrao() -> LLM:
    # Claude de verdade só com chave no ambiente. Sem ela, modo simulação (LLMFake).
    if os.getenv("ANTHROPIC_API_KEY"):
        return LLMAnthropic()
    return LLMFake()


app = criar_app(provedor_padrao())
