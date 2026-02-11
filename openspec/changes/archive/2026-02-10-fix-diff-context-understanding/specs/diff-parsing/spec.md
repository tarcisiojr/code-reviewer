## MODIFIED Requirements

### Requirement: Extrair diff entre branches
O sistema SHALL executar `git diff -U<N> <base>...HEAD` para obter o diff unificado entre a branch atual e a branch base especificada, incluindo N linhas de contexto configuráveis.

#### Scenario: Diff com mudanças em múltiplos arquivos
- **WHEN** o usuário executa o CLI passando `--base main`
- **THEN** o sistema executa `git diff -U3 main...HEAD` e retorna o diff completo com 3 linhas de contexto padrão

#### Scenario: Diff com contexto customizado
- **WHEN** o usuário executa o CLI passando `--base main --context-lines 5`
- **THEN** o sistema executa `git diff -U5 main...HEAD` e retorna o diff com 5 linhas de contexto

#### Scenario: Branch base não existe
- **WHEN** a branch base especificada não existe no repositório
- **THEN** o sistema exibe mensagem de erro clara e encerra com exit code 1

#### Scenario: Sem mudanças no diff
- **WHEN** não há diferenças entre a branch atual e a base
- **THEN** o sistema exibe mensagem informando que não há mudanças para analisar e encerra com exit code 0

## ADDED Requirements

### Requirement: Extrair linhas de contexto dos hunks
O sistema SHALL extrair e armazenar linhas de contexto (sem prefixo `+` ou `-`) de cada hunk, além das linhas adicionadas e removidas.

#### Scenario: Hunk com linhas de contexto
- **WHEN** um hunk contém linhas de contexto antes e depois das mudanças
- **THEN** o parser registra essas linhas como `context_lines` com seus números de linha correspondentes

#### Scenario: Estrutura de dados inclui contexto
- **WHEN** o diff é parseado com sucesso
- **THEN** cada hunk contém `context_lines` além de `added_lines` e `removed_lines`

### Requirement: Preservar formatação original de linhas de contexto
O sistema SHALL preservar a indentação e formatação original das linhas de contexto para manter visibilidade da estrutura do código.

#### Scenario: Indentação preservada
- **WHEN** uma linha de contexto tem 8 espaços de indentação no arquivo original
- **THEN** a linha de contexto no output mantém os 8 espaços de indentação
