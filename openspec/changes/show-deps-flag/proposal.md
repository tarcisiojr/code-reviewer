## Why

O airev coleta informações de callers e callees das funções modificadas, mas essa informação só é visível para a IA no prompt — o usuário final não tem acesso ao grafo de dependências. Expor essa visualização permite que o usuário entenda o impacto das mudanças antes mesmo de ver os findings.

## What Changes

- Adicionar flag `--show-deps` (ou `-D`) ao comando `airev review`
- Renderizar grafo de dependências no terminal, integrado por arquivo
- Mostrar dependências para todas as funções modificadas, independente de terem findings
- Formato expandido: árvore com callers/callees, arquivo:linha e snippet

## Capabilities

### New Capabilities

- `deps-visualization`: Renderização do grafo de dependências (callers/callees) no terminal para o usuário final

### Modified Capabilities

Nenhuma. Os requisitos de `context-backtracking` e `terminal-output` não mudam — apenas adicionamos uma nova forma de visualizar dados já coletados.

## Impact

- **cli.py**: Nova flag `--show-deps` / `-D`
- **formatters/terminal.py**: Nova função `format_dependencies()` e integração em `format_result()`
- **i18n/locales/**: Novas chaves de tradução para labels de dependências
