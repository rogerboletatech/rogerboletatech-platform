# ADR-0001: Boleta como módulo do ai-agent-service-python

- **Status:** Proposta
- **Data:** 2026-10-27
- **Decisor:** Roger

## Contexto

O Boleta é o agente-personagem da plataforma. Existia a opção de criar um serviço próprio (`apps/boleta-agent`) ou colocá-lo como módulo dentro do serviço Python que já existe no blueprint (`apps/ai-agent-service-python`).

## Decisão

O Boleta nasce como um módulo (`src/boleta/`) dentro de `apps/ai-agent-service-python`.

## Justificativa

A Diretriz #05 lista os 4 únicos motivos para extrair um serviço: escala assimétrica, poliglotismo obrigatório, isolamento de blast radius e autonomia de times. Hoje o Boleta não atende nenhum:

- Mesma linguagem e runtime do serviço de IA (Python).
- Sem volumetria conhecida que justifique escala isolada.
- Um único time (Roger).

Criar um serviço separado agora contradiria o que a plataforma ensina.

## Consequências

- Fronteira entre `boleta/` e `extraction/` precisa ser protegida (teste de import, ex.: `import-linter`).
- Se o Boleta passar a ter carga muito diferente do serviço de extração (ex.: picos em lives), reavaliar a extração. Essa reavaliação vira conteúdo do Módulo 2.
