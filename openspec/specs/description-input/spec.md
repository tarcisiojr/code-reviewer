## ADDED Requirements

### Requirement: Aceitar descrição via flag CLI
O sistema SHALL aceitar uma flag `--description` (alias `-d`) que recebe texto livre descrevendo as alterações.

#### Scenario: Descrição fornecida via flag
- **WHEN** o usuário executa `airev review --base main --description "Corrige bug de login"`
- **THEN** a descrição é capturada e disponibilizada para inclusão no prompt

#### Scenario: Descrição com quebras de linha via flag
- **WHEN** o usuário fornece descrição multi-linha via flag (ex: usando `$'...'` no shell)
- **THEN** as quebras de linha são preservadas na descrição

### Requirement: Aceitar descrição via stdin
O sistema SHALL aceitar `-` como valor da flag `--description` para ler a descrição de stdin.

#### Scenario: Descrição lida de stdin via pipe
- **WHEN** o usuário executa `cat descricao.md | airev review --base main -d -`
- **THEN** o conteúdo de stdin é lido e usado como descrição

#### Scenario: Descrição lida de arquivo via redirecionamento
- **WHEN** o usuário executa `airev review --base main -d - < descricao.md`
- **THEN** o conteúdo do arquivo é lido e usado como descrição

#### Scenario: Stdin vazio com flag -d -
- **WHEN** o usuário executa `airev review --base main -d -`
- **AND** stdin está vazio (sem pipe ou redirecionamento)
- **THEN** o sistema continua sem descrição (não bloqueia aguardando input)

### Requirement: Desabilitar modo interativo via flag
O sistema SHALL aceitar uma flag `--no-interactive` que desabilita prompts interativos.

#### Scenario: Flag no-interactive fornecida
- **WHEN** o usuário executa `airev review --base main --no-interactive`
- **THEN** o sistema não faz prompts interativos, mesmo em ambiente TTY

#### Scenario: Uso típico em CI
- **WHEN** o comando é executado em pipeline CI com `--no-interactive`
- **THEN** o comando executa sem aguardar input do usuário

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

### Requirement: Limitar tamanho da descrição
O sistema SHALL limitar a descrição a 2000 caracteres, exibindo aviso se truncada.

#### Scenario: Descrição dentro do limite
- **WHEN** a descrição tem até 2000 caracteres
- **THEN** a descrição é usada integralmente

#### Scenario: Descrição excede limite
- **WHEN** a descrição tem mais de 2000 caracteres
- **THEN** a descrição é truncada em 2000 caracteres
- **AND** um aviso é exibido ao usuário
