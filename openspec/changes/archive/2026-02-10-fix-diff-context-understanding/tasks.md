## 1. Atualizar Diff Parser

- [x] 1.1 Adicionar parâmetro `context_lines: int = 3` na função `get_diff()` em `diff_parser.py`
- [x] 1.2 Modificar comando git diff para usar `-U<context_lines>` em vez do padrão
- [x] 1.3 Adicionar campo `context_lines` na estrutura `DiffHunk` para armazenar linhas de contexto
- [x] 1.4 Atualizar parser para extrair linhas sem prefixo `+`/`-` como `context_lines`
- [x] 1.5 Preservar indentação original das linhas de contexto

## 2. Atualizar CLI

- [x] 2.1 Adicionar flag `--context-lines` (alias `-C`) com tipo `int` e default `3`
- [x] 2.2 Adicionar validação para rejeitar valores negativos
- [x] 2.3 Passar parâmetro `context_lines` para `get_diff()`

## 3. Atualizar Prompt Builder

- [x] 3.1 Modificar `format_diff_for_prompt()` para incluir linhas de contexto no output
- [x] 3.2 Formatar linhas de contexto com espaço inicial (padrão git diff)

## 4. Atualizar Template do Prompt

- [x] 4.1 Adicionar regra em "REGRAS ANTI-FALSOS POSITIVOS": linhas sem `+`/`-` são contexto
- [x] 4.2 Adicionar exemplo visual de diff com contexto vs diff parcial
- [x] 4.3 Reforçar aviso anti-falso-positivo com instrução sobre linhas de contexto

## 5. Testes

- [x] 5.1 Adicionar teste para `get_diff()` com diferentes valores de `context_lines`
- [x] 5.2 Adicionar teste para parsing de linhas de contexto em `DiffHunk`
- [x] 5.3 Adicionar teste para flag CLI `--context-lines`
- [x] 5.4 Adicionar teste para formatação de diff com contexto no prompt

## 6. Validação Final

- [x] 6.1 Executar `pytest` e verificar todos os testes passando
- [x] 6.2 Testar manualmente com diff que causava falso positivo
- [x] 6.3 Verificar que `--context-lines 0` restaura comportamento anterior
