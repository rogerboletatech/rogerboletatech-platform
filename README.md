# rogerboletatech-platform

Plataforma de Engenharia de Software Especialista: da intenção à produção, com arquitetura distribuída, poliglotismo, SDD e caos visível.

Aqui você constrói a **Esteira Full Lab**, um motor transacional de ponta a ponta, e acompanha cada requisição pelo **Console Glass-Box**. Quem te acompanha é o **Boleta**, um agente de IA construído com a mesma stack que você vai aprender. ([ficha técnica](docs/boleta-agent/ficha-tecnica.md))

> Status: estrutura inicial. Nada roda ainda.

## Estrutura

```text
apps/
  web-portal-angular/       Angular 22+ (Signals, Console Glass-Box)
  bff-gateway-java/         Java 25 + Spring Cloud Gateway
  orchestrator-camel-java/  Java 25 + Apache Camel
  core-service-java/        Java 25 + Spring Boot (DDD, Hexagonal, ULID)
  ai-agent-service-python/  Python + FastAPI + LangGraph (casa do Boleta)
libs/
  contracts-specs/          OpenAPI, AsyncAPI, especificações SDD
docs/
  boleta-agent/             Ficha técnica do agente
  adr/                      Decisões de arquitetura
  modulos-curso/            Conteúdo dos módulos
  diretrizes-trincheira/    Artigos de sobrevivência em produção
```

## Regras do repositório

- Domínio didático neutro: ordens corporativas e matrículas (`OrderTicket`, `EnrollmentPipeline`). Sem jargão de tesouraria.
- Commits só de equipamento pessoal, fora de VPN corporativa.
- Toda decisão relevante vira ADR em `docs/adr/`.
