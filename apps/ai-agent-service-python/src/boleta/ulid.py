"""ULID sem dependência externa: 48 bits de tempo em ms e 80 bits aleatórios, em Crockford base32.

Ordenável no tempo, como pede o contrato do Console Glass-Box (interacaoId).
"""

import os
import time

_ALFABETO = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def gerar_ulid() -> str:
    valor = (time.time_ns() // 1_000_000) << 80 | int.from_bytes(os.urandom(10), "big")
    return "".join(_ALFABETO[(valor >> (5 * i)) & 31] for i in range(25, -1, -1))
