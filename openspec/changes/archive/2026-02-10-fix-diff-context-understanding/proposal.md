## Why

A LLM está gerando falsos positivos de erro de sintaxe ao analisar diffs parciais. Quando o diff mostra apenas as linhas alteradas (ex: continuação de um `if` multiline), a LLM interpreta incorretamente como código incompleto, mesmo com instruções explícitas para consultar o arquivo completo. Isso gera ruído e prejudica a confiança do usuário nas revisões.

## What Changes

- Adicionar linhas de contexto adjacentes ao diff para dar visibilidade da estrutura completa
- Melhorar a formatação do diff para indicar visualmente que é parcial (usar `...` ou marcadores)
- Adicionar validação pré-envio para detectar falsos positivos óbvios de sintaxe
- Reforçar instruções no prompt com exemplo específico de diff multiline
- Incluir número de linhas antes/depois no hunk header para contexto

## Capabilities

### New Capabilities
- `diff-context-lines`: Capacidade de incluir N linhas de contexto antes/depois de cada hunk no diff para evitar confusão sobre estruturas de código parciais

### Modified Capabilities
- `prompt-building`: Alterar instruções anti-falso-positivo para serem mais específicas e incluir exemplo visual de diff multiline vs código completo
- `diff-parsing`: Modificar extração de hunks para incluir linhas de contexto configuráveis

## Impact

- **Arquivos afetados**:
  - `src/code_reviewer/diff_parser.py` - extrair linhas de contexto
  - `src/code_reviewer/prompt_builder.py` - formatação do diff com contexto
  - `src/code_reviewer/prompts/review_system.md` - instruções melhoradas
- **CLI**: Nova flag opcional `--context-lines` (default: 3)
- **Compatibilidade**: Mudança retrocompatível, comportamento atual preservado como fallback
