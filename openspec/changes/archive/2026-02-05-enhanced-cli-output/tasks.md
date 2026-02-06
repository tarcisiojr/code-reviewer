## 1. Setup e Dependências

- [x] 1.1 Adicionar `rich` como dependência no `pyproject.toml`
- [x] 1.2 Reinstalar o pacote para incluir a nova dependência

## 2. Módulo ProgressReporter

- [x] 2.1 Criar `src/code_reviewer/formatters/progress.py` com classe `ProgressReporter`
- [x] 2.2 Implementar método `status()` que retorna context manager para spinner
- [x] 2.3 Implementar método `step()` para mensagens simples de progresso
- [x] 2.4 Implementar função `is_ci_environment()` para detectar CI via TTY e env vars
- [x] 2.5 Criar testes em `tests/test_progress.py`

## 3. Exibição de Informações do Diff

- [x] 3.1 Adicionar método para formatar lista de arquivos com contagem de linhas (+/-)
- [x] 3.2 Adicionar método para exibir resumo do diff (total arquivos, total linhas)
- [x] 3.3 Integrar exibição de arquivos no cli.py após parsing do diff

## 4. Exibição de Dependências do Backtracking

- [x] 4.1 Modificar `context_builder.py` para retornar informações de callers/callees
- [x] 4.2 Adicionar método para formatar e exibir dependências encontradas
- [x] 4.3 Integrar exibição de dependências no cli.py após construção de contexto

## 5. Flags do CLI

- [x] 5.1 Adicionar flag `--no-progress` no comando review
- [x] 5.2 Adicionar flag `--progress` para forçar animações em CI
- [x] 5.3 Implementar lógica de auto-detecção de CI combinada com flags

## 6. Integração no Pipeline

- [x] 6.1 Refatorar cli.py para usar ProgressReporter em cada etapa
- [x] 6.2 Adicionar spinners: "Analisando diff...", "Construindo contexto...", "Executando análise...", "Processando resposta..."
- [x] 6.3 Implementar medição de tempo com `time.perf_counter()`
- [x] 6.4 Exibir tempo total ao final da análise

## 7. Testes e Validação

- [x] 7.1 Atualizar testes existentes para funcionar com rich
- [x] 7.2 Testar modo CI (--no-progress)
- [x] 7.3 Testar auto-detecção de TTY
- [x] 7.4 Rodar pipeline completo e verificar saída animada
