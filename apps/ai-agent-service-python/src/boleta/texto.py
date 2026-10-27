import unicodedata


def normalizar(texto: str) -> str:
    """Minúsculas e sem acento, para comparar palavras-chave."""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sem_acento.lower()
