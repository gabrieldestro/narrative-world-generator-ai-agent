# Evolução da Arquitetura: Projeto Client/Server (Angular + FastAPI + Docker)

Este documento descreve o plano arquitetural futuro para transformar o Gerador Narrativo (atualmente com uma UI em Streamlit e API simulada) em um sistema Web Client/Server completo.

## Estado Atual
*   **Lógica Core (LangGraph)**: Separada na pasta `app/services/`.
*   **API Simulada**: `app/api_facade.py` atua como um controlador único.
*   **Frontend Prototipado**: `gui/app.py` em Streamlit consome a API Simulada.

## Plano de Migração

A migração ocorrerá em 3 fases principais:

### Fase 1: Transformando o Backend em API REST (FastAPI)
1.  **Adicionar FastAPI**: Instalar `fastapi` e `uvicorn`.
2.  **Conversão do Facade**: O arquivo `api_facade.py` será renomeado para `api_routes.py`. Cada função será decorada com rotas do FastAPI.
    *   *Exemplo*: `def api_process_turn()` se tornará `@app.post("/simulation/turn") def process_turn(payload: TurnPayload)`.
3.  **Gerenciamento de Estado**: Como a API REST é *stateless* (sem estado), o `sim_state` que hoje vive na sessão do Streamlit, será armazenado temporariamente (ex: Redis ou arquivos JSON na pasta `sessions/`) e recuperado pelo `simulation_id` enviado em cada requisição.

### Fase 2: Conteinerização (Docker)
1.  **Dockerfile do Backend**: Criar uma imagem baseada em Python 3.10+, copiando os `requirements.txt` e executando o `uvicorn`.
2.  **Volumes**: Garantir que as pastas `worlds/` e `saves/` sejam montadas como volumes do Docker para persistência de dados.
3.  **Docker Compose**: Orquestrar o serviço de Backend junto com serviços auxiliares (como um futuro Redis ou Banco de Dados).

### Fase 3: Novo Frontend (Angular)
O Streamlit será totalmente descartado e substituído por uma Single Page Application (SPA) Angular.
1.  **Setup**: Criar um projeto paralelo (ex: `narrative-world-client`) usando Angular CLI.
2.  **Integração REST**: Criar `Services` no Angular (`simulation.service.ts`) que apontarão para os endpoints do FastAPI.
3.  **Benefícios Visuais**: 
    *   O Streamlit limita fortemente o layout. Com Angular e bibliotecas como TailwindCSS, implementaremos animações fluidas, efeitos de "digitação de máquina" para a IA, e interfaces Drag-and-Drop para o editor de JSON.
    *   **WebSockets**: Implementar conexões WebSocket no FastAPI e no Angular para gerar o texto da história (stream) em tempo real, eliminando a longa barra de carregamento.

## Resumo das Decisões Tomadas
- O Streamlit servirá **apenas como prova de conceito** para validar se a quebra de Serviços/Facade foi bem feita.
- O código dentro de `app/engine` e `app/story_generator` **não sofrerá alterações**, pois já está perfeitamente desacoplado graças aos `services/`.
