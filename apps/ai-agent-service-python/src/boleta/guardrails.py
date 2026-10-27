"""Filtros de entrada e saída do Boleta (ficha técnica, seção 7).

Entrada: recusa pedidos fora de escopo antes de gastar LLM.
Saída: bloqueia jargão proibido pelo Protocolo de Compliance (blueprint 1.2) e travessão.
"""

import re
from dataclasses import dataclass

from boleta.texto import normalizar

# Protocolo de Compliance: domínio didático neutro, sem jargão de tesouraria.
TERMOS_PROIBIDOS = (
    "tesouraria",
    "renda fixa",
    "liquidacao cetip",
    "liquidacaocetip",
    "cetip",
    "boletarendafixa",
    "taxa di",
    "taxadi",
    "selic",
    "mesa de operacoes",
)

# Pedidos que o Boleta não atende (ficha técnica, seção 4, "Não faz").
FORA_DE_ESCOPO = {
    "conselho_financeiro": re.compile(r"\b(investir|investimento|acoes?|cripto|bitcoin)\b"),
    "conselho_juridico": re.compile(r"\b(processar|advogado|juridic[oa]|clt|rescisao)\b"),
    "merge_automatico": re.compile(r"\b(faz|faca|fazer|de) (o )?merge\b|\baprova (o|meu) pr\b"),
}

RECUSAS = {
    "conselho_financeiro": "Conselho financeiro tá fora do meu escopo. Sou agente de engenharia.",
    "conselho_juridico": "Assunto jurídico não é comigo. Procura um profissional da área.",
    "merge_automatico": "Merge e aprovação são decisão humana. Eu reviso, o engenheiro decide.",
}


@dataclass(frozen=True)
class Veredito:
    permitido: bool
    motivo: str | None = None
    mensagem: str | None = None


def checar_entrada(pergunta: str) -> Veredito:
    texto = normalizar(pergunta)
    if not texto.strip():
        return Veredito(False, "vazio", "Manda a pergunta que eu respondo.")
    for motivo, padrao in FORA_DE_ESCOPO.items():
        if padrao.search(texto):
            return Veredito(False, motivo, RECUSAS[motivo])
    return Veredito(True)


def checar_saida(resposta: str) -> Veredito:
    texto = normalizar(resposta)
    for termo in TERMOS_PROIBIDOS:
        if termo in texto:
            return Veredito(False, f"jargao_proibido:{termo}")
    if "—" in resposta:
        return Veredito(False, "travessao")
    return Veredito(True)
