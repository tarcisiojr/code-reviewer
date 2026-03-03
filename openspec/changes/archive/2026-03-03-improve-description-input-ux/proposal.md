## Why

Os usuários estão tendo dificuldades com o prompt interativo de descrição do MR. O modo `multiline=True` do prompt_toolkit faz com que Enter adicione nova linha em vez de enviar, causando confusão. A experiência deveria ser similar ao Claude Code e Copilot CLI: Ctrl+V cola o texto, Enter envia, e Shift+Enter ou `\` cria nova linha.

## What Changes

- Inverter o comportamento do Enter no prompt interativo: Enter envia (submit), Shift+Enter ou `\`+Enter criam nova linha
- Substituir Ctrl+C por Esc como tecla de cancelamento (seguir sem descrição)
- Atualizar mensagem de instrução para refletir os novos atalhos de forma clara e concisa
- Manter bracketed paste preservando quebras de linha do texto colado

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `description-input`: Alterar comportamento das teclas no prompt interativo (Enter envia, Shift+Enter/backslash para nova linha, Esc cancela)

## Impact

- **src/code_reviewer/description_input.py**: Refatorar key bindings do prompt_toolkit na função `ask_description_interactive()`
- **tests/test_description_input.py**: Atualizar testes para refletir novo comportamento de teclas
