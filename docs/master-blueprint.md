# 🏗️ Master Blueprint: Roger Boleta Tech (`@rogerboletatech`)
**A Plataforma de Engenharia de Software Especialista: Da Intenção à Produção com Arquitetura Distribuída, Poliglotismo, SDD e Caos Visível.**

Este documento consolida toda a visão estratégica, pedagógica, arquitetural e operacional da plataforma **Roger Boleta Tech**. O objetivo é formar Engenheiros de Software Especialistas e Arquitetos de Soluções, ensinando o que cursos de sintaxe ignoram: tomada de decisão sob pressão, alinhamento com negócio, orquestração de Agentes de IA e sobrevivência nas trincheiras de produção.

---

## Parte 1: Identidade, Posicionamento, Compliance e Hospedagem

### 1.1. A Persona Técnica e o "Porquê" do Nome
*   **Identidade Unificada:** `@rogerboletatech` (GitHub, YouTube, Instagram, TikTok, X, Vercel).
*   **Storytelling de Autoridade:** O apelido **"Boleta"** nasceu nas trincheiras de engenharia após desenhar e integrar uma esteira *full* de altíssima criticidade do zero ao deploy. Na plataforma, "Boletar" é ressignificado como: *colocar sistemas distribuídos complexos de pé em produção com resiliência, rastreabilidade e risco zero*.
*   **O Projeto Prático Oficial:** Batizado de **`Esteira Full Lab`** (ou `Boleta Engine`), onde o aluno constrói e estressa um motor transacional de ponta a ponta.

### 1.2. Protocolo de Blindagem e Compliance (Segurança para quem atua em Bancos)
Para manter 100% de conformidade ética, contratual e jurídica com instituições financeiras:
1.  **Abstração Total de Domínio:** Proibição absoluta de usar jargões exclusivos de tesouraria/bancos no código-fonte público (ex: nada de `LiquidacaoCetip`, `BoletaRendaFixa`, `TaxaDI`). O domínio didático da plataforma será **Processamento de Ordens Corporativas e Matrículas de Alta Volumetria** (`OrderTicket`, `EnrollmentPipeline`, `TransactionSaga`). Os padrões (Camel, Circuit Breaker, ULID, SDD) pertencem à ciência da computação aberta.
2.  **Segregação Física e de Rede:** Jamais realizar commits, editar arquivos ou acessar contas do `@rogerboletatech` utilizando equipamentos corporativos ou conectado à VPN do empregador (Lei de Software 9.609/98).
3.  **Higiene de Git e Conta GitHub (`github.com/rogerboletatech`):**
    *   Repositórios pessoais antigos que contenham dados civis sensíveis ou testes técnicos antigos devem ser mantidos como `Private`.
    *   Configuração obrigatória no repositório local antes de qualquer commit:
        ```bash
        git config user.name "Roger Boleta"
        git config user.email "rogerboletatech@users.noreply.github.com"
        ```
    *   Remoção de vínculos diretos entre a URL antiga do GitHub e perfis corporativos públicos.
    *   Desativação da sincronização de agenda telefônica ao criar redes sociais do `@rogerboletatech`.

### 1.3. Arquitetura de Publicação e Custos (Estratégia Serverless / Freemium)
*   **Front-end e Portal de Artigos (Vercel - Custo R$ 0):** Hospedado em `rogerboletatech.vercel.app` (apontando para `apps/web-portal-angular`). Contém todos os artigos em Markdown e o **Console de Arquitetura Visual**.
*   **Modo Simulação Client-Side (Economia de Nuvem):** Na versão pública da Vercel, o Console de Arquitetura possui um motor em RxJS/Signals que simula a física da rede, a abertura do Circuit Breaker e o roteamento do Apache Camel direto no navegador do visitante, permitindo 100.000 acessos simultâneos a custo zero de servidor.
*   **Modo Real de Execução (`docker-compose` Local e Google Cloud Run):** O aluno clona o Monorepo no GitHub e roda `docker-compose up` na própria máquina para subir as JVMs, Python, PostgreSQL, Redis e Kafka reais, conectando o Angular via **Server-Sent Events (SSE)**. Para demonstrações em nuvem, utiliza-se o **Google Cloud Run** (com *Scale-to-Zero*) + **Neon.tech** (Postgres Serverless) + **Upstash** (Redis Serverless).

---

## Parte 2: O Conceito Inovador — A Plataforma "Glass-Box" (Caixa de Vidro)

A tela da aplicação web em **Angular 22+** é dividida em duas áreas interativas:

1.  **Painel de Experiência (60% - Esquerda):** A aplicação funcional de negócio + leitor dos Módulos e Diretrizes de Trincheira.
2.  **Console de Arquitetura e Caos (40% - Direita):** Um diagrama vivo dos sistemas distribuídos alimentado de forma não intrusiva por eventos do **OpenTelemetry / Micrometer**.
    *   **Visão Raio-X:** Ao clicar em "Processar Ordem", o aluno assiste à requisição saindo do Angular, passando pelo BFF, sendo enriquecida e roteada pelo Apache Camel, acionando o Agente de IA em Python e salvando no PostgreSQL com chave ULID.
    *   **Painel de Engenharia de Caos:** Botões interativos onde o aluno provoca falhas reais (*"Simular Latência de 5s no Banco"*, *"Derrubar Microsserviço Python"*, *"Injetar Pico de 500 req/s"*). Ele visualiza em tempo real o **Rate Limiter** bloqueando excessos (HTTP 429), o **Circuit Breaker** mudando de Verde (*Closed*) para Vermelho (*Open*), o **Retry com Exponential Backoff + Jitter** atuando e o **Fallback** salvando a experiência do usuário.

---

## Parte 3: Topologia Técnica do Monorepo (`rogerboletatech-platform`)

```text
rogerboletatech-platform/
├── apps/
│   ├── web-portal-angular/       # Angular 22+ (Signals, Standalone, Console Glass-Box) -> Deploy Vercel
│   ├── bff-gateway-java/         # Java 25 LTS + Spring Cloud Gateway (OAuth2, Rate Limit, Agregação)
│   ├── orchestrator-camel-java/  # Java 25 LTS + Apache Camel (EIP, Saga, DLQ, Circuit Breaker)
│   ├── core-service-java/        # Java 25 LTS + Spring Boot 3.x (DDD, Hexagonal, Virtual Threads, ULID)
│   └── ai-agent-service-python/  # Python + FastAPI + Pydantic (CrewAI/LangGraph, Extração e RAG)
├── libs/
│   └── contracts-specs/          # Contratos OpenAPI, AsyncAPI e Especificações SDD
├── docs/
│   ├── modulos-curso/            # Conteúdo didático do básico ao avançado
│   └── diretrizes-trincheira/    # Artigos práticos de sobrevivência em produção
├── docker-compose.yml            # Infraestrutura local completa (Postgres, Redis, Kafka, Prometheus)
└── README.md                     # Vitrine principal do @rogerboletatech
```

---

## Parte 4: Currículo Completo do Curso (Do Básico Direto ao Avançado)

### Módulo 0: O Engenheiro Decisor, Discovery e a Escala de "Super Times"
Na era em que a IA gera código em segundos, digitar sintaxe virou *commodity*. O valor está na decisão arquitetural antes da primeira linha de código.
*   **Product Discovery Técnico:** Como traduzir a visão do PM/Stakeholder em direcionadores arquiteturais.
*   **Event Storming Completo (Comandos, Eventos e Read Models):** Mapeamento colaborativo do domínio para identificar regras de negócio, integrações e **Bounded Contexts** (Contextos Delimitados).
*   **Análise de Trade-offs:**
    *   *Público Interno (Backoffice) vs. Externo (B2C):* Impacto em latência, segurança de borda, SEO e custo de nuvem.
    *   *Volumetria e Concorrência:* Quando usar processamento síncrono vs. filas assíncronas.
*   **Team Topologies e o Conceito de "Super Time":**
    *   A Lei de Conway e o limite da Carga Cognitiva.
    *   **A Célula de Alta Performance:** `1 PM + 2 Engenheiros Especialistas`. Por que dois engenheiros? Para eliminar o **viés arquitetural** através de *sparring* técnico, enquanto Agentes de IA atuam como a força operacional de codificação.
    *   **A Regra de Escala pelo DDD:** Não se adiciona desenvolvedores a um time para tentar entregar mais rápido. Só se escala a equipe quando o domínio cresce e exige a separação de um novo contexto: **`1 Novo Bounded Context = 1 Novo Super Time`**.

### Módulo 1: SDD (Spec-Driven Development) e Orquestração de Agentes IA
*   **O Paradigma SDD:** Especificações formais como a única fonte da verdade. Transformando resultados do Event Storming em artefatos estruturados.
*   **Contract-First (OpenAPI 3.1 / AsyncAPI / JSON Schema):** Travando as interfaces entre Front, BFF, Camel e Microsserviços antes de codar.
*   **Fábrica Multiagente (CrewAI / LangGraph / AutoGen):**
    *   Orquestrando agentes especializados (*Agente PM/Spec*, *Agente Arquiteto*, *Agente Java/Spring*, *Agente Angular*, *Agente QA/Sec*).
    *   **Human-in-the-Loop:** O engenheiro especialista auditando Pull Requests gerados por IA quanto a brechas de segurança, N+1 queries e violações de arquitetura.

### Módulo 2: Arquitetura Evolutiva — Do Monólito Modular aos Microsserviços
*   **O Começo Pragmático (Modulith):** Estruturando domínios isolados dentro da mesma JVM com **Spring Modulith** e protegendo fronteiras com testes automatizados no **ArchUnit**.
*   **Extração Cirúrgica:** Como a Arquitetura Hexagonal (*Ports and Adapters*) permite arrancar um módulo que atingiu gargalo de volumetria e transformá-lo em um microsserviço independente em horas, sem reescrever regras de negócio.

### Módulo 3: A Esteira Corporativa — BFF, Apache Camel e Java 25 LTS
*   **Camada BFF (Backend for Frontend):** O escudo do Front-end. Agregação de chamadas, adaptação de payloads para a tela e validação de JWT.
*   **Orquestração com Apache Camel:**
    *   Implementando *Enterprise Integration Patterns (EIP)*: *Content-Based Router*, *Splitter*, *Aggregator*, *Enricher*.
    *   Isolando a complexidade de integração para manter os microsserviços de domínio puros.
*   **Microsserviço de Persistência (Spring Boot 3.x):**
    *   Concorrência massiva com **Virtual Threads (Project Loom)**.
    *   Modelagem tática de DDD (Aggregates, Entities, Value Objects) e migrations seguras com Flyway.

### Módulo 4: Arquitetura Poliglota — Integrando Python e Inteligência Artificial
*   **A Ferramenta Certa para o Trabalho Certo:** Java domina o transacional pesado; Python domina IA, Ciência de Dados e LLMs.
*   **Microsserviço Cognitivo (FastAPI + Pydantic):** Criando endpoints assíncronos em Python com validação estrita de dados para conversar perfeitamente com o Apache Camel.
*   **Agentes em Produção:** O Camel recebe um payload bruto, aciona o serviço Python (que executa um grafo LangGraph/CrewAI com RAG em banco vetorial) e devolve um JSON enriquecido para gravação transacional no Java.

### Módulo 5: Resiliência Extrema, Proteção de Borda e Engenharia de Caos
*   **Proteção de Borda (API Gateway):**
    *   *Rate Limiting* (Algoritmos Token Bucket / Leaky Bucket no Redis) e retorno semântico `HTTP 429 Too Many Requests`.
    *   *Throttling* vs. *Load Shedding* (descartando tráfego secundário em momentos de crise para salvar o core financeiro).
*   **Tolerância a Falhas (Resilience4j + Camel):**
    *   *Circuit Breaker:* Calibrando limiares de falha, janelas deslizantes e transição entre *Closed*, *Open* e *Half-Open*.
    *   *Retry com Exponential Backoff e Jitter:* Como adicionar aleatoriedade temporal nas retentativas para evitar que milhares de clientes derrubem um serviço que acabou de se recuperar (*Thundering Herd*).
    *   *Bulkhead Pattern:* Compartimentação de pools de threads/conexões para evitar efeito dominó (*Cascading Failures*).
    *   *Timeouts Estritos (Fail Fast)* e *Fallbacks* inteligentes.
*   **Consistência Eventual e Integridade Distribuída:**
    *   *Idempotência Estrita:* Garantindo que retentativas de rede nunca dupliquem transações financeiras.
    *   *Transactional Outbox Pattern:* Salvando no banco e publicando no broker com garantia atômica.
    *   *Saga Pattern (Orquestração vs. Coreografia):* Desfazendo operações com transações compensatórias no Camel.
    *   *Dead Letter Queues (DLQ):* Gestão e reprocessamento de *Poison Messages*.

### Módulo 6: Front-end Corporativo Reativo e Telemetria Visual (Angular 22+)
*   **Angular Moderno:** *Standalone Components*, *Signals*, *Computed Signals*, novo *Control Flow* (`@if`, `@for`, `@defer`) e *NgRx Signal Store*.
*   **Performance de UI:** *Change Detection OnPush*, hidratação SSR e arquitetura de componentes *Smart vs. Dumb*.
*   **Construindo o Console Glass-Box:** Uso de *HTTP Interceptors*, propagação de headers W3C (`traceparent`) e consumo de streams **SSE (Server-Sent Events)** para animar a topologia da esteira em tempo real.

### Módulo 7: Observabilidade Full-Stack e Testes de Contrato
*   **Observabilidade:** Rastreamento distribuído de ponta a ponta com **OpenTelemetry**, métricas na JVM/Camel com **Micrometer/Prometheus** e dashboards no **Grafana**.
*   **Testes que Importam:** Testes de integração reais subindo containers efêmeros com **Testcontainers** e **Contract Testing (Pact)** garantindo que Front, BFF, Java e Python nunca quebrem a integração.

---

## Parte 5: Base de Conhecimento — As 6 Diretrizes de Trincheira (Artigos Práticos)

Esta seção do portal `@rogerboletatech` reúne verdades de produção que evitam prejuízos financeiros, retrabalho arquitetural e quedas de sistema.

---

### 🔥 Diretriz #01: A "Síndrome do Endpoint Faltante" — Por que seu Desenho de Solução Vive Voltando para Aprovação?

**A Dor na Trincheira:**
Você desenha a solução, aprova no comitê de arquitetura e o desenvolvimento começa. Duas semanas depois, o time trava: *"Precisamos aprovar um ajuste no desenho porque faltou o endpoint X, Y e Z para a tela funcionar"*. Se isso acontece com frequência, **não é azar; é um sintoma claro de falha metodológica no Discovery/Event Storming ou de acoplamento errado na governança da arquitetura.**

**O Diagnóstico Especialista (As 3 Causas Raízes):**

1.  **Event Storming Cego para Leitura (Esquecer os *Read Models*):**
    *   *O Erro:* Na dinâmica de Event Storming, os engenheiros focam 90% da energia nos Post-its Azuis (Comandos: `CriarOrdem`, `CancelarMatricula`) e Laranjas (Eventos: `OrdemCriada`). Eles esquecem os **Post-its Verdes (Read Models / Modelos de Leitura)**.
    *   *A Consequência:* O backend constrói perfeitamente os endpoints de escrita (`POST`, `PUT`), mas quando o Front-end (Angular) vai montar a tela, descobre que precisa listar dados cruzados, filtros específicos ou contadores que ninguém mapeou. Resultado: correria para criar endpoints `GET` de última hora e reabertura do desenho.
    *   *A Cura:* No Event Storming, para cada tela ou passo do usuário, é obrigatório colar o Post-it Verde respondendo: **"Quais dados exatos o usuário precisa ver na tela para conseguir tomar a decisão de disparar este Comando?"** Cada Post-it Verde vira uma especificação de query no BFF.
2.  **Ausência de BFF e Design Orientado a Tabelas (CRUD Thinking):**
    *   *O Erro:* Desenhar APIs de microsserviços espelhando tabelas do banco de dados em vez de espelhar a jornada do usuário.
    *   *A Cura:* Os microsserviços Core devem expor capacidades de domínio estáveis. Quem deve absorver a necessidade de "endpoints específicos para a tela X" é o **BFF (Backend for Frontend)** — ou uma camada GraphQL/Agregadora — que pertence ao próprio escopo do time de produto, sem precisar alterar a arquitetura dos microsserviços subjacentes.
3.  **Governança no Nível de Abstração Errado (C4 Model):**
    *   *O Erro:* Colocar rotas REST específicas (`/api/v1/clientes/saldo-consolidado`) dentro de um Documento de Arquitetura Macro que exige aprovação formal de comitê.
    *   *A Cura:* Aprovação de arquitetura deve validar **Contexto e Containers (Níveis 1 e 2 do C4 Model)**: quais sistemas conversam, qual protocolo (REST vs. Kafka), qual o SLA, volumetria e segurança. Novos endpoints dentro de um canal de comunicação já aprovado não são "mudanças de arquitetura"; são evoluções de **Contrato (SDD / OpenAPI)** validadas via *Mock Server* entre Front e Back no Dia 1 da Sprint.

---

### 🔥 Diretriz #02: O Custo Oculto do `log.info` — Observabilidade vs. Fatura da Nuvem

**A Dor na Trincheira:**
Desenvolvedores espalham `log.info("Entrou no método X")`, `log.info("Payload recebido: " + json)` por todo o código. Em produção, sob 5.000 req/s, isso gera terabytes de texto inútil. Ferramentas de APM e ingestão (Datadog, Splunk, CloudWatch) cobram por gigabyte indexado — transformando logs mal feitos em uma conta de dezenas de milhares de reais por mês, além de degradar o I/O da aplicação.

**O Padrão Especialista:**
*   **Proibição de Logs em Loops e Concatenação de Strings:** Usar sempre parametrização (`log.debug("Processando item {}", id)`) para evitar alocação de memória se o nível estiver desativado.
*   **Log Estruturado (JSON) com Trace ID:** Logs são dados para máquinas lerem. Devem sair em formato JSON contendo obrigatoriamente `trace_id`, `span_id`, `service_name` e `ulid` da transação.
*   **Semântica Estrita de Níveis em Produção:**
    *   `ERROR`: Falha crítica que exige ação humana ou abertura de incidente imediato.
    *   `WARN`: Anomalia recuperada automaticamente (ex: *Circuit Breaker* abriu, *Fallback* acionado, *Retry* executado).
    *   `INFO`: Exclusivo para marcos de negócio de alto nível (1 log de resumo ao final da transação/esteira).
    *   `DEBUG` / `TRACE`: Desligados por padrão em produção; ativados em tempo real via *Actuator / Feature Flag* apenas para investigar um incidente específico por poucos minutos.

---

### 🔥 Diretriz #03: A Armadilha Mortal do `@Scheduled` em Múltiplos Pods no Kubernetes

**A Dor na Trincheira:**
O desenvolvedor cria uma rotina de fechamento ou reprocessamento com `@Scheduled(cron = "0 0 2 * * *")` no Spring Boot. Funciona perfeitamente na máquina local. Quando sobe para produção no Kubernetes com 4 *Pods* (réplicas) para alta disponibilidade, **as 4 instâncias disparam o job exatamente no mesmo milissegundo**. O resultado: clientes cobrados 4 vezes, envio de e-mails quadruplicados e *Deadlocks* severos no banco de dados.

**O Padrão Especialista:**
*   **Regra Inegociável:** Aplicações distribuídas são *Stateless*; nunca confie em agendadores isolados na memória da JVM.
*   **Solução 1 (Lock Distribuído no Código):** Utilizar **ShedLock** integrado ao Redis ou PostgreSQL. Quando dão 02h00, os 4 Pods tentam adquirir o lock; apenas 1 consegue executar a rotina e os outros 3 abortam silenciosamente.
*   **Solução 2 (Orquestração Externa Cloud-Native):** Remover o `@Scheduled` da aplicação. Transformar a rotina em um comando acionado por um **Kubernetes CronJob**, AWS EventBridge ou rota do Apache Camel que publica uma única mensagem em uma fila consumida por apenas um worker por vez, sempre protegida por chave de **Idempotência**.

---

### 🔥 Diretriz #04: Fragmentação de Índices no Banco — Por que trocar `UUIDv4` por `ULID`?

**A Dor na Trincheira:**
Para fugir do `AUTO_INCREMENT` sequencial (que gera contenção e expõe a volumetria do negócio em URLs), os times adotam o `UUIDv4` (ex: `f47ac10b-58cc-4372-a567-0e02b2c3d479`) como Primary Key. Porém, o UUIDv4 é 100% aleatório. Quando o PostgreSQL precisa inserir milhões de linhas com chaves aleatórias, ele precisa gravar dados no meio de páginas de disco já cheias da árvore **B-Tree**, causando *Page Splits* constantes, fragmentação severa do índice, inchaço de armazenamento (*Bloat*) e queda drástica na velocidade de `INSERT`.

**O Padrão Especialista:**
*   Adotar **ULID** (*Universally Unique Lexicographically Sortable Identifier*) ou `UUIDv7`.
*   **Como funciona:** Os primeiros 48 bits do ULID representam o *timestamp* em milissegundos, e os 80 bits restantes são aleatórios (ex: `01HV8G7K9P...`).
*   **O Ganho Duplo:** Ele continua sendo gerado na aplicação (sem bater no banco antes e permitindo criar chaves de idempotência no cliente/BFF), mas como começa com o tempo atual, **todas as novas inserções acontecem de forma estritamente sequencial no final da árvore B-Tree do banco de dados**, entregando performance de `AUTO_INCREMENT` com a segurança e distribuição de um UUID.

---

### 🔥 Diretriz #05: Monólito Modular vs. Microsserviços (e Monorepo vs. Multirepo)

**A Dor na Trincheira:**
Criar 12 microsserviços em 12 repositórios Git diferentes no início de um projeto para uma equipe de 4 pessoas. O time passa 80% do tempo atualizando versões de bibliotecas, consertando contratos quebrados, lidando com falhas de rede e fazendo deploys coordenados (o temido **Monólito Distribuído**).

**O Padrão Especialista:**
*   **Separar no Código antes de Separar na Rede:** Todo sistema novo deve nascer como um **Monólito Modular** (com fronteiras de Bounded Context blindadas por *ArchUnit* / *Spring Modulith*) a menos que exista um direcionador comprovado.
*   **Os 4 Únicos Motivos Reais para Extrair um Microsserviço:**
    1.  *Escala Assimétrica Extrema:* Um módulo específico consome 90% da CPU/Memória e precisa escalar isoladamente.
    2.  *Poliglotismo Obrigatório:* O módulo exige uma linguagem incompatível com o runtime principal (ex: nosso serviço de Agentes de IA em **Python**).
    3.  *Isolamento de Blast Radius (Raio de Explosão):* Rotinas que manipulam buffers gigantes ou integrações legadas instáveis que não podem derrubar a JVM do core transacional.
    4.  *Autonomia de Super Times:* Quando a empresa cresce e múltiplos esquadrões independentes precisam de ciclos de deploy completamente isolados.
*   **Vantagem do Monorepo na Era da IA:** Manter Front (Angular), BFF, Camel e Microsserviços em um **Monorepo** permite que Agentes de IA (Cursor, CrewAI) enxerguem o contrato de ponta a ponta na mesma árvore de diretórios, realizando refatorações atômicas perfeitas.

---

### 🔥 Diretriz #06: Acoplamento Temporal — O que deve ser Síncrono vs. Assíncrono?

**A Dor na Trincheira:**
O usuário clica em "Finalizar Compra". Na mesma requisição HTTP síncrona, o backend valida o saldo, chama a API de antifraude, chama a API da prefeitura para emitir Nota Fiscal, gera um PDF e chama o servidor SMTP para enviar e-mail. Se a API da prefeitura demorar 15 segundos ou cair, a thread do servidor trava e o cliente recebe erro na compra.

**O Padrão Especialista:**
*   **Lei do Desacoplamento Temporal:** Na thread síncrona da requisição do usuário, execute **apenas o mínimo indispensável para confirmar a intenção ou validar uma regra impeditiva imediata**.
*   Tudo o que for consequência (emitir NF, gerar PDF, notificar sistemas legados, enviar e-mail, atualizar dashboard analítico) deve ser disparado de forma **Assíncrona** via eventos no **Apache Camel / Kafka** (utilizando o padrão *Transactional Outbox*). Se o servidor de e-mail cair por 2 horas, a esteira guarda a mensagem, aplica *Retry* com *Backoff* e entrega quando o serviço voltar, sem que o cliente na ponta perceba qualquer falha.