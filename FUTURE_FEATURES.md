# Funcionalidades Futuras (Pré-Migração)

Este documento atua como um backlog de melhorias que devem ser aplicadas à versão atual da aplicação (Interface Gráfica em Python/Streamlit + API Facade) *antes* da grande migração arquitetural para Angular e Docker.

### Backlog de Interface (UI) e Funcionalidades

- [ ] **Editor Dinâmico de Mundos:** Melhorar a página "Editor de Templates". Em vez de utilizar um único `textarea` gigante para editar JSON cru, a interface deve renderizar os dados como um formulário limpo, dividindo Mundo, NPCs, Estado do Jogador, etc., em campos editáveis separados.
- [ ] **Leitor de Narrativas Salvas:** Criar uma tela dedicada (ou adicionar à Dashboard/Gerador) para listar todas as histórias e simulações já geradas, permitindo a leitura rápida sem precisar abrir os arquivos `.txt` e `.json` manualmente.
- [ ] **Retomada de Histórias Incompletas:** Adicionar na UI a funcionalidade de "Carregar História", permitindo continuar a geração (seja no modo Simulador Interativo ou no Gerador Contínuo) exatamente de onde o processo parou (já existente no CLI, falta trazer para o Streamlit).

### Backlog de Banco de Dados e Infraestrutura

- [ ] **Migração para NoSQL / Cloud Storage:** Substituir o sistema atual de repositórios baseado em arquivos textuais e variáveis em `.env` locais por um banco de dados de documentos (como MongoDB) ou um provedor na nuvem. Isso facilitará buscas, integridade de sessões de usuário e o futuro deploy.
