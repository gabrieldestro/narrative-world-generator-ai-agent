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

#### Explicação das variáveis:

LLM_MODEL
Nome do modelo de linguagem que será utilizado (ex: gpt-4, mistral, etc).

PROVIDER_NAME
Define o tipo de provedor:

* "openai" → usa API externa
* "local" → usa modelo local via LM Studio

BASE_URL
URL do provedor da API.
Pode ser deixado em branco se estiver usando LM Studio (local).
Exemplo para OpenAI: https://api.openai.com/v1

TOKEN
Token de autenticação da API (necessário para provedores externos como OpenAI).

SIMULATION_TYPE
Define o tipo de simulação:

* 0 → LITE (simulação simplificada)
* 1 → Completa (suporta mudanças de estado via ferramentas)

DEBUG
Ativa logs detalhados:

* 0 → desativado
* 1 → ativado (output mais verboso para debugging)

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

O projeto possui dois módulos independentes operando na linha de comando:

#### 4.1. Simulador Narrativo (Turn-based RPG)
Para interagir turno a turno manipulando as ações da história:
`python -m app.main`

#### 4.2. Gerador Automático de História Completa
Para usar o pipeline focado em compilar um framework/mundo em uma história literária completa (capitulada de forma ininterrupta ou persistida):
`python -m app.main_story`

## Como funciona

O usuário interage com o sistema via console.
Cada entrada representa uma ação do jogador.
A IA processa essa ação e retorna uma continuação da narrativa.
O estado da história é mantido internamente e pode evoluir com base nas decisões.

No modo completo, o sistema também permite:

* Alterações estruturais no mundo (via ferramentas)
* Evolução mais complexa da narrativa

## Próximos passos

* Criar uma interface gráfica (GUI) que se comunique com a aplicação via API
* Melhorar o sistema de logs da narrativa, especialmente para suportar:

  * Branches da história
  * Manipulação de save states
  * Histórico de decisões
