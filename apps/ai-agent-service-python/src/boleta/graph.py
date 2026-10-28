"""Grafo LangGraph do Boleta.

    guarda_entrada ─(recusa)──────────────────────────────► fim
          │
          ▼
    busca_diretrizes ─► responder ─► guarda_saida ─► fim

`responder` usa o LLM com timeout e circuit breaker. Se o cérebro cair,
cai no fallback determinístico com a diretriz encontrada (Módulo 5).
Cada nó emite um span e registra um passo em `passos`, que alimenta o Console Glass-Box.
"""

import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, StateGraph

from boleta import guardrails
from boleta.llm import LLMIndisponivel, LLMResiliente
from boleta.persona import SYSTEM_PROMPT
from boleta.telemetry import passo
from boleta.tools.diretrizes import Diretriz, buscar

FALLBACK_SEM_DIRETRIZ = (
    "Meu cérebro de LLM está fora do ar. Não achei diretriz sobre isso. Tenta de novo em instantes."
)
RESPOSTA_BLOQUEADA = "Minha resposta não passou no guardrail de saída. Esse erro vai pro console e vira aula."


class Passo(TypedDict):
    step: str
    decision: str
    detalhe: str


class Estado(TypedDict, total=False):
    pergunta: str
    diretrizes: list[Diretriz]
    resposta: str
    fallback: bool
    bloqueada: bool
    passos: Annotated[list[Passo], operator.add]


def _fallback(diretrizes: list[Diretriz]) -> str:
    if not diretrizes:
        return FALLBACK_SEM_DIRETRIZ
    d = diretrizes[0]
    return (
        "Meu cérebro de LLM está fora do ar. Enquanto isso, aqui está a Diretriz que fala disso: "
        f"#{d.numero:02d} {d.titulo}. {d.resumo}"
    )


def construir_grafo(llm: LLMResiliente):
    def guarda_entrada(estado: Estado) -> Estado:
        with passo("guarda_entrada") as span:
            veredito = guardrails.checar_entrada(estado["pergunta"])
            decisao = "permitido" if veredito.permitido else f"recusado:{veredito.motivo}"
            span.set_attribute("boleta.decision", decisao)
            saida: Estado = {"passos": [{"step": "guarda_entrada", "decision": decisao, "detalhe": ""}]}
            if not veredito.permitido:
                saida["resposta"] = veredito.mensagem
                saida["bloqueada"] = True
            return saida

    def busca_diretrizes(estado: Estado) -> Estado:
        with passo("busca_diretrizes", tool="diretrizes") as span:
            achadas = buscar(estado["pergunta"])
            ids = ",".join(f"#{d.numero:02d}" for d in achadas) or "nenhuma"
            span.set_attribute("boleta.decision", ids)
            return {
                "diretrizes": achadas,
                "passos": [{"step": "busca_diretrizes", "decision": ids, "detalhe": "busca por palavra-chave"}],
            }

    async def responder(estado: Estado) -> Estado:
        with passo("responder", tool="llm") as span:
            diretrizes = estado.get("diretrizes", [])
            contexto = "\n".join(f"Diretriz #{d.numero:02d} {d.titulo}: {d.resumo}" for d in diretrizes)
            prompt = f"{contexto}\n\nPergunta do aluno: {estado['pergunta']}" if contexto else estado["pergunta"]
            try:
                resposta = await llm.completar(SYSTEM_PROMPT, prompt)
                decisao, detalhe, fallback = "llm", "", False
            except LLMIndisponivel as erro:
                resposta = _fallback(diretrizes)
                decisao, detalhe, fallback = "fallback", str(erro), True
            span.set_attribute("boleta.decision", decisao)
            span.set_attribute("boleta.breaker", llm.breaker.estado)
            return {
                "resposta": resposta,
                "fallback": fallback,
                "passos": [{"step": "responder", "decision": decisao, "detalhe": detalhe}],
            }

    def guarda_saida(estado: Estado) -> Estado:
        with passo("guarda_saida") as span:
            veredito = guardrails.checar_saida(estado["resposta"])
            decisao = "aprovada" if veredito.permitido else f"bloqueada:{veredito.motivo}"
            span.set_attribute("boleta.decision", decisao)
            saida: Estado = {"passos": [{"step": "guarda_saida", "decision": decisao, "detalhe": ""}]}
            if not veredito.permitido:
                saida["resposta"] = RESPOSTA_BLOQUEADA
                saida["bloqueada"] = True
            return saida

    grafo = StateGraph(Estado)
    grafo.add_node("guarda_entrada", guarda_entrada)
    grafo.add_node("busca_diretrizes", busca_diretrizes)
    grafo.add_node("responder", responder)
    grafo.add_node("guarda_saida", guarda_saida)
    grafo.set_entry_point("guarda_entrada")
    grafo.add_conditional_edges(
        "guarda_entrada",
        lambda e: END if e.get("bloqueada") else "busca_diretrizes",
    )
    grafo.add_edge("busca_diretrizes", "responder")
    grafo.add_edge("responder", "guarda_saida")
    grafo.add_edge("guarda_saida", END)
    return grafo.compile()
