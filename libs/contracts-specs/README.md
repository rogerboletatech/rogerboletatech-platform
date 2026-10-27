# contracts-specs

Contratos da plataforma, escritos antes do código (SDD, contract-first).

| Arquivo | Formato | O que descreve | Status |
|---|---|---|---|
| `openapi/ai-agent-service.yaml` | OpenAPI 3.1 | `POST /boleta/perguntar` e `GET /health` do serviço de IA | implementado |
| `asyncapi/console-glass-box.yaml` | AsyncAPI 3.0 | Eventos de passo do Boleta para o Console Glass-Box | planejado |

## Validar

```bash
npx @redocly/cli lint openapi/ai-agent-service.yaml
npx @asyncapi/cli validate asyncapi/console-glass-box.yaml
```

Regra: mudou o contrato, muda aqui antes do código. A implementação deve bater com o arquivo.
