# AI Narrative Simulator

## Introdução

Este projeto é um simulador narrativo baseado em IA, desenvolvido em Python, que permite a criação de histórias dinâmicas a partir de interações do usuário.

A aplicação funciona via console (CLI), onde o usuário insere ações e a IA responde, evoluindo a narrativa em tempo real.

Atualmente, o sistema suporta dois tipos de provedores de linguagem:

* OpenAI (modelos remotos)
* Modelos locais via LM Studio

## Setup

### 1. Criar arquivo .env

Crie um arquivo chamado `.env` na pasta app com as seguintes variáveis:

LLM_MODEL=""
PROVIDER_NAME=""
BASE_URL=""
TOKEN=""
SIMULATION_TYPE=1
DEBUG=0
AUTO_PLAY=0
STORY_CHAPTER_PARTS=3
TEMPERATURE=1

#### Explicação das variáveis:

LLM_MODEL
Nome do modelo de linguagem que será utilizado (ex: gpt-4, mistral, etc).

PROVIDER_NAME
Define o tipo de provedor:

* "openai" → usa API externa
* "local" → usa modelo local via LM Studio ou inferência local

BASE_URL
URL do provedor da API.
Pode ser deixado em branco se estiver usando LM Studio local nativo.
Exemplo para OpenAI ou inferência em nuvem: https://api.openai.com/v1

TOKEN
Token de autenticação da API (necessário para provedores externos).

SIMULATION_TYPE
Define o tipo de simulação:

* 0 → LITE (simulação simplificada)
* 1 → Completa (suporta mudanças de estado via ferramentas)

DEBUG
Ativa logs detalhados:

* 0 → desativado
* 1 → ativado (output mais verboso para debugging)

AUTO_PLAY
Habilita o modo de simulação passivo/automático para demonstração ou auto-resolução.
* 0 → desligado
* 1 → ligado

STORY_CHAPTER_PARTS
Para o modo de Gerador de Histórias Longevas, define a quantidade de sub-eventos/turnos necessários até que um capítulo se encerre.

TEMPERATURE
Controla a criatividade da Inteligência Artificial. Valores mais altos (ex: 1) deixam o texto mais criativo; valores baixos (ex: 0.1) o tornam mais mecânico e previsível.

### 2. Criar ambiente virtual

python -m venv venv

Ativar o ambiente:

Windows:
venv\Scripts\activate

Linux/Mac:
source venv/bin/activate

### 3. Instalar dependências

pip install -r requirements.txt

### 4. Executar a aplicação

Você pode interagir com o gerador usando a Interface Gráfica (Streamlit) ou via Terminal (CLI clássico).

#### 4.1. Interface Gráfica (Streamlit)
Esta é a nova interface visual da aplicação, estruturada com um padrão `api_facade` preparando-a para futura evolução Web:
`streamlit run gui/main_gui.py`

*(O navegador abrirá automaticamente em `localhost:8501`)*

#### 4.2. Terminal CLI Clássico (Simulador RPG)
Para interagir em modo texto via prompt de comando:
`python -m app.main`

#### 4.3. Terminal CLI (Gerador Automático de História)
Para gerar contos passivos ininterruptos via CLI:
`python -m app.main_story`

## Como funciona

Na Interface Gráfica ou CLI, o usuário seleciona um Template de Mundo.
A IA processa as decisões e invoca ferramentas no LangGraph.

A nova arquitetura introduziu a pasta `app/services/` e `app/api_facade.py`, isolando completamente a lógica Core do modo de exibição, visando a migração futura para um Backend robusto.

## Evolução Arquitetural (Próximos Passos)

* Migrar o `api_facade.py` atual para um servidor REST usando **FastAPI**.
* Empacotar a aplicação Backend em **Docker** para deploy facilitado.
* Desenvolver um novo projeto de Frontend moderno usando **Angular** para substituir a prototipagem feita em Streamlit.
* Ver o arquivo `FUTURE_ARCHITECTURE.md` para detalhes da próxima evolução do sistema.
