## MODIFIED Requirements

### Requirement: Perguntar descrição interativamente
O sistema SHALL perguntar ao usuário se deseja adicionar descrição quando: não foi fornecida via flag, modo interativo está ativo, e ambiente é TTY.

#### Scenario: Prompt interativo após exibir diff
- **WHEN** o diff foi exibido e descrição não foi fornecida
- **AND** `--no-interactive` não foi usado
- **AND** stdout é TTY
- **THEN** o sistema exibe prompt com instruções claras sobre atalhos de teclado

#### Scenario: Usuário envia descrição com Enter
- **WHEN** o prompt interativo é exibido
- **AND** o usuário digitou ou colou texto
- **AND** o usuário pressiona Enter
- **THEN** o texto é enviado e capturado como descrição

#### Scenario: Usuário pula descrição com Esc
- **WHEN** o prompt interativo é exibido
- **AND** o usuário pressiona Esc
- **THEN** o sistema continua sem descrição

#### Scenario: Usuário pula descrição com input vazio
- **WHEN** o prompt interativo é exibido
- **AND** o usuário pressiona Enter sem digitar nada
- **THEN** o sistema continua sem descrição

### Requirement: Suportar input multi-linha com bracketed paste
O sistema SHALL suportar input multi-linha usando `prompt_toolkit` com bracketed paste mode habilitado.

#### Scenario: Colar Markdown com quebras de linha
- **WHEN** o usuário cola texto contendo quebras de linha (ex: descrição de MR)
- **THEN** todas as linhas são capturadas, incluindo linhas vazias intermediárias

#### Scenario: Nova linha com Shift+Enter
- **WHEN** o usuário está digitando no prompt interativo
- **AND** pressiona Shift+Enter
- **THEN** uma nova linha é inserida no texto sem enviar

#### Scenario: Nova linha com backslash+Enter
- **WHEN** o usuário está digitando no prompt interativo
- **AND** digita `\` seguido de Enter
- **THEN** o caractere `\` é removido do texto
- **AND** uma nova linha é inserida no texto sem enviar

#### Scenario: Cancelar input com Esc
- **WHEN** o usuário está no prompt de descrição
- **AND** pressiona Esc
- **THEN** o sistema continua sem descrição (não aborta o comando)

## REMOVED Requirements

### Requirement: Cancelar input com Ctrl+C
**Reason**: Substituído por Esc como tecla de cancelamento, mais intuitivo para "cancelar e seguir"
**Migration**: Usuários devem usar Esc em vez de Ctrl+C para cancelar o prompt de descrição
