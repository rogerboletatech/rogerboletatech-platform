"""Busca nas Diretrizes de Trincheira.

Versão inicial por palavra-chave, em memória. Vira RAG de verdade no Módulo 4,
quando os artigos de docs/diretrizes-trincheira/ existirem.
"""

from dataclasses import dataclass

from boleta.texto import normalizar


@dataclass(frozen=True)
class Diretriz:
    numero: int
    titulo: str
    resumo: str
    palavras_chave: tuple[str, ...]


CATALOGO = (
    Diretriz(
        1,
        "@Scheduled sem lock distribuído",
        "Com 4 pods, o job roda 4 vezes. Use lock distribuído (ex.: ShedLock) ou mova para um único agendador.",
        ("scheduled", "cron", "job", "agendador", "shedlock", "lock"),
    ),
    Diretriz(
        2,
        "Log sem payload completo",
        "log.info em loop e payload inteiro no log custam caro e vazam dado. Logue identificadores, com retenção curta.",
        ("log", "logging", "payload", "loop", "lgpd"),
    ),
    Diretriz(
        3,
        "UUIDv4 como chave primária",
        "UUIDv4 aleatório fragmenta o índice B-tree. Prefira ULID ou UUIDv7, ordenáveis no tempo.",
        ("uuid", "ulid", "pk", "chave", "indice", "primary"),
    ),
    Diretriz(
        4,
        "Chamada síncrona que deveria ser evento",
        "Se o chamador não precisa da resposta agora, publique um evento. Acoplamento temporal derruba a cadeia inteira.",
        ("sincrona", "sincrono", "evento", "kafka", "rest", "acoplamento", "fila"),
    ),
    Diretriz(
        5,
        "Só extraia serviço com direcionador real",
        "Quatro motivos: escala assimétrica, poliglotismo obrigatório, isolamento de blast radius e autonomia de times.",
        ("microsservico", "microservico", "servico", "extrair", "monolito", "modular"),
    ),
)


def buscar(pergunta: str, limite: int = 2) -> list[Diretriz]:
    texto = normalizar(pergunta)
    pontuadas = [(sum(p in texto for p in d.palavras_chave), d) for d in CATALOGO]
    relevantes = sorted((pd for pd in pontuadas if pd[0] > 0), key=lambda pd: -pd[0])
    return [d for _, d in relevantes[:limite]]
