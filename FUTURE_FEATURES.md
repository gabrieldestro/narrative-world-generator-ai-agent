# Próximas Features e Roadmap (Gerador de Narrativas Longas)

Este documento centraliza as melhorias esperadas para o módulo **Gerador de História Completa em Capítulos** (`app/main_story.py`).
Instrução para a IA: Na próxima iteração, você pode pedir que eu implemente esses pontos diretamente consultando este arquivo.

## 1. Interação e Revisão Parametrizada pelo Usuário
Atualmente a geração de narrativa (quando em modo Gerador) trabalha em fluxo direto/autônomo. Precisamos parametrizar as seguintes opções:

- **Flag de Auto-Play X Revisão:** Permitir que o comportamento seja parametrizável. O usuário pode querer dar o prompt inicial e voltar uma hora depois para a história pronta, ou pode querer supervisionar cautelosamente o ritmo artístico (Aguardando _input_).

**Se ativado:**
1. **Revisão da Sinopse (Planning Node):** Pausar a thread de geração após a IA formular o "O quê" acontecerá e permitir edição, aprovação manual ou ajuste direcionado antes de criar os capítulos.
2. **Revisão dos Capítulos Base:** Após a partição dos capítulos em JSON, parar e deixar o usuário editar livremente o array de sinopses.
3. **Revisão Capítulo-a-Capítulo:** Após gerar o texto extenso de um capítulo, aguardar a aprovação do usuário. Se o usuário reprovar, pode gerar novamente este braço até seguir para o próximo capítulo.

## 2. Particionamento de Geração de Alto Volume (Context Window Limits)
Não podemos assumir que a janela de contexto conseguirá gerar um capítulo inteiro de 3.000 palavras em um único disparo (`call_llm`).
- **Geração Incremental de Capítulos:** Modificar a lógica do `writing_node` para ser capaz de particionar a geração e montar o capítulo ao longo de múltiplas requisições. O nó deve escrever o início, avançar para o meio conectando o contexto imediatamente interior, e finalizar.
