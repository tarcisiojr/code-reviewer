## Why

A saída atual do CLI é muito simples - apenas exibe o resultado final sem mostrar o progresso das etapas intermediárias. Isso dificulta entender o que a ferramenta está fazendo durante a execução, especialmente em análises demoradas. Queremos uma saída rica e animada (spinners, progress bars) por padrão, mas com opção de desabilitar para ambientes de CI.

## What Changes

- Adicionar saída animada com spinners durante cada etapa do pipeline (parsing diff, construindo contexto, executando IA, parseando resposta)
- Usar biblioteca `rich` para renderização rica (spinners, cores, tabelas)
- Adicionar flag `--no-progress` para desabilitar animações (modo CI)
- Auto-detectar quando não é TTY (pipe, CI) e desabilitar animações automaticamente
- Exibir lista de arquivos modificados com contagem de linhas (+/-) após parsing do diff
- Exibir dependências encontradas durante backtracking (callers e callees)
- Mostrar estatísticas no final: tempo de execução total, tempo por etapa

## Capabilities

### New Capabilities

- `cli-verbosity`: Controle de verbosidade e modo CI para saída do terminal

### Modified Capabilities

- `terminal-output`: Adicionar suporte a mensagens de progresso e modo silencioso para CI

## Impact

- **Código afetado**: `src/code_reviewer/cli.py`, `src/code_reviewer/formatters/terminal.py`
- **Nova dependência**: `rich` para spinners, progress bars e formatação rica
- **Interface**: Nova flag `--no-progress` no CLI
- **Compatibilidade**: Comportamento padrão muda para saída animada (melhoria UX), mas detecta CI automaticamente
