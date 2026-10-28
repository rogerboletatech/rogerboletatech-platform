# ADR-0002: Provedor de LLM real é Claude, atrás de um Protocol

- **Status:** Aceita
- **Data:** 2026-10-28
- **Decisor:** Roger

## Contexto

A ficha técnica do Boleta deixou em aberto o provedor de LLM e a estratégia de custo. O grafo precisa de um modelo para responder, mas a plataforma também precisa rodar sem chave e sem gasto, para aula e para testes.

## Decisão

- O grafo depende só do Protocol `boleta.llm.LLM`. Nenhum nó importa SDK de provedor.
- O provedor real é Claude, via SDK oficial `anthropic`, em `boleta/llm_anthropic.py`.
- O modelo padrão é `claude-haiku-5-5`, o mais barato da família. Troca por `BOLETA_MODELO`.
- Sem `ANTHROPIC_API_KEY`, `main.py` usa `LLMFake`. Assim o serviço sobe e os testes rodam sem rede e sem custo.
- Recusa de segurança (`stop_reason == "refusal"`) e resposta vazia viram `LLMIndisponivel`. O grafo então cai no fallback determinístico.

## Justificativa

- O Protocol mantém a troca de provedor como detalhe de adaptador. Trocar de modelo ou de fornecedor não mexe no grafo.
- Haiku é o modelo mais barato, e a ficha manda economizar tokens na fase de simulação.
- Recusa tratada como falha evita que uma recusa apareça como resposta válida ao aluno.
- Testes com cliente falso não gastam tokens e não dependem de rede.

## Consequências

- Chave de API só no ambiente da máquina. Nunca no repositório.
- Mudar o modelo padrão exige revisar custo e qualidade e, se for relevante, nova ADR.
- Span e métricas de custo por chamada ainda não existem. Entram junto com o Módulo 7 (observabilidade).
