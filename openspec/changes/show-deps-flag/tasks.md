## 1. CLI

- [x] 1.1 Adicionar flag `--show-deps` / `-D` ao comando `review` em cli.py
- [x] 1.2 Passar `show_deps` e `context_graphs` para a função de formatação

## 2. Formatter

- [x] 2.1 Criar função `format_dependency_graph(graph: ContextGraph)` em terminal.py
- [x] 2.2 Criar função auxiliar `_group_deps_by_file(graphs: list[ContextGraph])`
- [x] 2.3 Modificar `format_result()` para aceitar parâmetros `context_graphs` e `show_deps`
- [x] 2.4 Integrar renderização de deps antes dos findings de cada arquivo
- [x] 2.5 Adicionar mensagem para arquivos sem findings quando deps ativo

## 3. Internacionalização

- [x] 3.1 Adicionar chaves `terminal.dependencies`, `terminal.callers`, `terminal.callees` em pt-br.yaml
- [x] 3.2 Adicionar mesmas chaves em en.yaml
- [x] 3.3 Adicionar chave `terminal.no_deps_found` para mensagem de deps vazias
- [x] 3.4 Adicionar chave `terminal.no_findings_file` para arquivos sem findings

## 4. Testes

- [x] 4.1 Testar flag `--show-deps` ativa corretamente o comportamento
- [x] 4.2 Testar formatação de deps com callers e callees
- [x] 4.3 Testar formatação de deps sem callers nem callees
- [x] 4.4 Testar integração de deps com findings no mesmo arquivo
- [x] 4.5 Testar arquivos só com deps (sem findings)
