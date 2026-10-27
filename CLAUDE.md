# CLAUDE.md

Monorepo da plataforma @rogerboletatech: Esteira Full Lab + Console Glass-Box + Boleta (agente de IA). Visão completa em `docs/master-blueprint.md`; agente em `docs/boleta-agent/ficha-tecnica.md`. Só leia esses arquivos se a tarefa exigir.

## Regras inegociáveis
- Domínio didático neutro: `OrderTicket`, `EnrollmentPipeline`, `TransactionSaga`. Proibido jargão de tesouraria/banco (tesouraria, renda fixa, CETIP, Taxa DI, Selic, `BoletaRendaFixa`...). Vale para código, testes, docs e commits.
- Nada sobre empresas ou empregadores reais.
- Git: identidade `Roger Boleta <rogerboletatech@users.noreply.github.com>`, já configurada no repo. Trabalhe em branch, nunca direto na `main`.
- Toda decisão relevante vira ADR em `docs/adr/NNNN-titulo.md` (Status, Data, Contexto, Decisão, Justificativa, Consequências).
- Só extraia serviço com direcionador real (Diretriz #05).

## Estilo
- Código, comentários e docs em português BR; termos técnicos de mercado em inglês.
- Frases curtas, sem travessão.
- Testes junto com o código, sempre.

## Stack e comandos
| App | Stack | Status |
|---|---|---|
| `apps/ai-agent-service-python` | Python 3.12, FastAPI, LangGraph, OpenTelemetry | esqueleto pronto |
| `apps/core-service-java` | Java 25, Spring Boot 4, DDD/Hexagonal, ULID | OrderTicket com testes (`./mvnw test`) |
| `apps/bff-gateway-java` | Java 25, Spring Cloud Gateway | vazio |
| `apps/orchestrator-camel-java` | Java 25, Apache Camel | vazio |
| `apps/web-portal-angular` | Angular 22+, Signals | vazio |
| `libs/contracts-specs` | OpenAPI, AsyncAPI (SDD, contract-first) | vazio |

Python (a partir de `apps/ai-agent-service-python`):
- testes: `.venv/Scripts/python -m pytest -q`
- fronteira de módulos: `cd src && ../.venv/Scripts/lint-imports --config ../pyproject.toml`

## Boleta
- Sempre se declara IA; humano decide (sem merge/aprovação automática).
- LLM atrás do Protocol `boleta.llm.LLM`; provedor real ainda em aberto, padrão é `LLMFake`.
- Spans OTel com `boleta.step`, `boleta.tool`, `boleta.decision`.
