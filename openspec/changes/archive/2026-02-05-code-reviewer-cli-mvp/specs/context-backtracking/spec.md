## ADDED Requirements

### Requirement: Rastrear callers das funções modificadas
O sistema SHALL buscar no projeto quais funções/métodos chamam as funções identificadas como modificadas, usando `grep -rn "function_name("` no diretório do repositório.

#### Scenario: Função com múltiplos callers
- **WHEN** a função `process_payment` foi modificada
- **THEN** o backtracking encontra todos os locais que chamam `process_payment(` e retorna arquivo, linha e trecho de código ao redor (até 10 linhas de contexto)

#### Scenario: Função sem callers
- **WHEN** a função modificada não é chamada por nenhum outro ponto do projeto
- **THEN** o backtracking retorna lista vazia de callers para essa função

#### Scenario: Limitar quantidade de referências
- **WHEN** uma função é chamada em mais de 5 locais diferentes
- **THEN** o backtracking retorna no máximo 5 referências, priorizando as do mesmo módulo/diretório

### Requirement: Rastrear callees das funções modificadas
O sistema SHALL analisar as linhas adicionadas no diff para identificar novos símbolos (funções, classes) utilizados, e buscar suas definições no projeto via `grep -rn "def symbol_name\|class symbol_name"`.

#### Scenario: Nova chamada de função adicionada
- **WHEN** uma linha adicionada contém `log_failure(result)` e essa função não aparecia no código anterior
- **THEN** o backtracking localiza a definição de `log_failure` e retorna arquivo, linha e assinatura

#### Scenario: Chamada a função inexistente
- **WHEN** o símbolo referenciado nas linhas adicionadas não é encontrado no projeto
- **THEN** o backtracking registra o símbolo como "definição não encontrada"

### Requirement: Ler conteúdo completo dos arquivos modificados
O sistema SHALL ler o conteúdo completo de cada arquivo modificado para fornecer contexto da função inteira onde a mudança aconteceu.

#### Scenario: Arquivo existente modificado
- **WHEN** o arquivo `services/payment.py` foi modificado
- **THEN** o context builder lê o conteúdo completo atual do arquivo

#### Scenario: Arquivo deletado
- **WHEN** um arquivo foi completamente removido no diff
- **THEN** o context builder não tenta ler o arquivo e registra como "arquivo removido"

### Requirement: Excluir diretórios irrelevantes do backtracking
O sistema SHALL excluir diretórios como `node_modules/`, `venv/`, `.git/`, `__pycache__/`, `dist/`, `build/` das buscas de backtracking.

#### Scenario: Referência em diretório excluído
- **WHEN** o grep encontra uma chamada a `process_payment` dentro de `node_modules/`
- **THEN** essa referência é excluída dos resultados

### Requirement: Montar estrutura de contexto
O sistema SHALL retornar uma estrutura contendo, para cada função modificada: nome da função, arquivo, callers (arquivo + linha + snippet), callees (arquivo + linha + assinatura) e conteúdo do arquivo completo.

#### Scenario: Contexto completo montado
- **WHEN** o backtracking é executado para a função `process_payment` em `services/payment.py`
- **THEN** o resultado contém: callers encontrados, callees identificados e conteúdo completo do arquivo
