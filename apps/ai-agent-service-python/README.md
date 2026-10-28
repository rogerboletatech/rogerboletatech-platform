# ai-agent-service-python

Serviço de IA da Esteira Full Lab. Casa do **Boleta** (`src/boleta/`) e da extração usada pelo Camel (`src/extraction/`). Por que é módulo e não serviço: [ADR-0001](../../docs/adr/0001-boleta-como-modulo-do-ai-agent-service.md).

## Rodando

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev]"
.venv/Scripts/python -m pytest
.venv/Scripts/python -m uvicorn main:app --app-dir src --reload
```

```bash
curl -X POST localhost:8000/boleta/perguntar -H "content-type: application/json" -d '{"pergunta":"meu @Scheduled roda em 4 pods"}'
```

O LLM é escolhido pelo ambiente:
- Sem `ANTHROPIC_API_KEY`: `LLMFake` (modo simulação, sem custo).
- Com `ANTHROPIC_API_KEY`: Claude via SDK oficial, modelo `claude-haiku-5-5` (o mais barato). Troque com `BOLETA_MODELO`.

```bash
ANTHROPIC_API_KEY=... .venv/Scripts/python -m uvicorn main:app --app-dir src
```

Nunca commite a chave. Ela só vai para o ambiente da sua máquina.

## Fluxo do grafo

`guarda_entrada → busca_diretrizes → responder → guarda_saida`

- **guarda_entrada:** recusa fora de escopo (conselho financeiro, jurídico, pedido de merge) sem gastar LLM.
- **busca_diretrizes:** palavra-chave nas Diretrizes de Trincheira. Vira RAG no Módulo 4.
- **responder:** LLM com timeout estrito e circuit breaker. Se cair, usa o fallback determinístico com a diretriz encontrada.
- **guarda_saida:** barra jargão do Protocolo de Compliance e travessão.

Cada passo gera um span `boleta.<passo>` com `boleta.step`, `boleta.tool` e `boleta.decision`, filho do `traceparent` que vem do BFF. A resposta também traz `passos[]` para o Console Glass-Box.

## Fronteira

`lint-imports` (rodar a partir de `src/`) garante que `boleta` e `extraction` não importam um ao outro.
