## ADDED Requirements

### Requirement: Incluir linhas de contexto no diff
O sistema SHALL incluir N linhas de contexto antes e depois de cada hunk no diff, usando a flag nativa `git diff -U<N>`.

#### Scenario: Diff com contexto padrão
- **WHEN** o usuário executa o CLI sem especificar linhas de contexto
- **THEN** o sistema executa `git diff -U3 <base>...HEAD` incluindo 3 linhas de contexto por padrão

#### Scenario: Diff com contexto customizado
- **WHEN** o usuário executa o CLI com `--context-lines 5`
- **THEN** o sistema executa `git diff -U5 <base>...HEAD` incluindo 5 linhas de contexto

#### Scenario: Diff sem contexto adicional
- **WHEN** o usuário executa o CLI com `--context-lines 0`
- **THEN** o sistema executa `git diff -U0 <base>...HEAD` mostrando apenas linhas alteradas

### Requirement: Diferenciar linhas de contexto no output
O sistema SHALL formatar linhas de contexto (sem `+` ou `-`) de forma distinta das linhas alteradas para que a LLM entenda que são apenas referência.

#### Scenario: Estrutura de controle visível no contexto
- **WHEN** um hunk contém linhas alteradas dentro de um bloco `if` multiline
- **THEN** a linha do `if (` aparece como contexto (sem prefixo `+` ou `-`) antes das linhas alteradas

#### Scenario: Formatação de linhas de contexto
- **WHEN** o diff é formatado para o prompt
- **THEN** linhas de contexto aparecem com espaço inicial (padrão git) e linhas alteradas com `+` ou `-`

### Requirement: Flag CLI para linhas de contexto
O sistema SHALL aceitar uma flag `--context-lines` (alias `-C`) para configurar o número de linhas de contexto.

#### Scenario: Flag longa
- **WHEN** o usuário passa `--context-lines 5`
- **THEN** o valor 5 é usado como parâmetro para `-U` no git diff

#### Scenario: Flag curta
- **WHEN** o usuário passa `-C 5`
- **THEN** o valor 5 é usado como parâmetro para `-U` no git diff

#### Scenario: Valor inválido
- **WHEN** o usuário passa `--context-lines -1` ou valor não numérico
- **THEN** o sistema exibe erro e usa o valor padrão (3)
