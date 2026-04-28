# Diretrizes para a Inteligência Artificial e Agentes (AI_GUIDELINES)

Se você é uma IA encarregada de manter ou estender a base deste projeto, deve tomar as presentes heurísticas como fonte de verdade para a gestão de código e arquitetura.

## Estrutura do Núcleo do Projeto
O `narrative-world-generator-ai-agent` abriga um ecossistema bifurcado de geração, dividido sob o módulo genérico `app/`. Em suma:
1. **Simulador de RPG em Turnos:** (`app/services/simulation_service.py`) Lógica para manipular um estado do mundo em resposta ao input criativo do jogador do turno atual.
2. **Gerador de Histórias Longevas em Capítulos:** (`app/services/story_service.py`) Rede assíncrona focada unicamente na escrita passiva (ou controlada). Planeja a sinopse inteira através de `story_generator/graph_builder.py`.

### A Nova Arquitetura Frontend/Backend (Facade e UI)
Visando a evolução do projeto para uma aplicação Web (Angular Frontend + FastAPI Backend), a arquitetura foi dividida:
- **`app/api_facade.py`**: Funciona como o controlador principal (simulando rotas de uma API REST). A interface **NUNCA** deve chamar a lógica interna diretamente, sempre passando pela Facade.
- **`gui/`**: Contém a interface do usuário prototipada em **Streamlit**. O Streamlit consome a Facade. A interface deve manter o mínimo de estado possível, espelhando um front-end Web.

## Boas Práticas (Must-Have)

### 1. Respeite as Restrições de Modelos Locais (Sliding Window Context)
Esse projeto **PRECISA** suportar modelos com janelas de contexto extremamente limitadas (ex.: Llama 3 8B, Mistral, executados via LM Studio).
- **Nunca injete listas cruas de todo o progresso passado diretamente no prompt.**
- Confie no conceito de Memórias de Resumo Dinâmicas (`story_summary` ou extrações de `scene_log`), resumindo pedaços antigos e mantendo apenas o mais recente exposto na íntegra.
- Não estoure os tokens com payloads repetitivos de contexto.

### 2. Aproveitamento de Estado
As representações de dados e estruturas de interface já foram desenvolvidas no pacote `app/model/`.
- Adote herança, agregação ou chaves opcionais ali (usando o nativo TypedDict) ao invés de recriar blocos duplicados de tipagem. Ex: `StoryState` é preferível se estender lógicas do `GameState`.

### 3. Checkpoints e Salto Seguros
- Todas as execuções de fluxo contínuo ou interativas **devem ser persistidas**.
- As rotinas de retomada de jogo (`load_save()` de `save_repository.py` ou do `story_generation_repository.py`) são obrigações de tolerância a falhas para não frustrar o usuário após crashs (algo corriqueiro com inferência local de IA).

### 4. Estilos de Terminal e LLMs
- Todos os `print()` para o cliente tendem a usar métodos customizáveis de CLI. Reutilize `app/ui/print_terminal.py` para não sujar os displays textuais.
- Centralize qualquer contato com IA pela wrapper oficial abstrata `app/llm.py` via método padrão `call_llm` que engatilha o Provider escolhido sem lock-in para um provedor. Se necessitar Extração Estruturada forte (JSON), você pode forçar no prompt de sistema ou verificar o suporte ao parse da LLM em questão.
