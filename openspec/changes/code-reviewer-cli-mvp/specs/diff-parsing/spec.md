## ADDED Requirements

### Requirement: Extrair diff entre branches
O sistema SHALL executar `git diff <base>...HEAD` para obter o diff unificado entre a branch atual e a branch base especificada.

#### Scenario: Diff com mudanças em múltiplos arquivos
- **WHEN** o usuário executa o CLI passando `--base main`
- **THEN** o sistema executa `git diff main...HEAD` e retorna o diff completo

#### Scenario: Branch base não existe
- **WHEN** a branch base especificada não existe no repositório
- **THEN** o sistema exibe mensagem de erro clara e encerra com exit code 1

#### Scenario: Sem mudanças no diff
- **WHEN** não há diferenças entre a branch atual e a base
- **THEN** o sistema exibe mensagem informando que não há mudanças para analisar e encerra com exit code 0

### Requirement: Identificar arquivos modificados
O sistema SHALL extrair a lista de arquivos modificados a partir do diff, incluindo caminho completo relativo à raiz do repositório.

#### Scenario: Múltiplos arquivos modificados
- **WHEN** o diff contém mudanças em 3 arquivos (`services/payment.py`, `routes/checkout.py`, `utils/helpers.py`)
- **THEN** o parser retorna uma lista com os 3 caminhos de arquivo

#### Scenario: Ignorar arquivos irrelevantes
- **WHEN** o diff contém mudanças em arquivos de lock (`package-lock.json`, `poetry.lock`), arquivos gerados ou migrations
- **THEN** esses arquivos são excluídos da análise

### Requirement: Extrair funções modificadas dos hunk headers
O sistema SHALL parsear os hunk headers do diff (`@@ -L,S +L,S @@ nome_da_funcao`) para extrair os nomes das funções/classes onde as mudanças ocorreram.

#### Scenario: Hunk header com nome de função
- **WHEN** um hunk header é `@@ -45,7 +45,9 @@ def process_payment(amount, token)`
- **THEN** o parser extrai `process_payment` como função modificada no arquivo correspondente

#### Scenario: Hunk header sem nome de função
- **WHEN** um hunk header não contém identificador de função (ex: mudança no topo do arquivo)
- **THEN** o parser registra a mudança sem nome de função associado, usando o nome do arquivo como contexto

### Requirement: Extrair linhas adicionadas e removidas
O sistema SHALL extrair as linhas adicionadas (prefixo `+`) e removidas (prefixo `-`) de cada hunk, com seus respectivos números de linha.

#### Scenario: Linhas adicionadas e removidas
- **WHEN** um hunk contém `-    result = charge(amount)` e `+    result = charge(amount, currency="BRL")`
- **THEN** o parser registra a linha removida e a adicionada com seus números de linha correspondentes

### Requirement: Retornar estrutura parseada
O sistema SHALL retornar o diff parseado como uma estrutura de dados contendo: lista de arquivos modificados, cada um com suas funções afetadas, linhas adicionadas e linhas removidas.

#### Scenario: Estrutura completa
- **WHEN** o diff é parseado com sucesso
- **THEN** o resultado é uma lista de `DiffFile`, cada um contendo `path`, `hunks` (com `function_name`, `added_lines`, `removed_lines`)
