## Context

O revisor de código usa diffs git para analisar mudanças. O formato padrão do diff mostra apenas linhas alteradas (com `+` e `-`), sem contexto adjacente. Isso causa confusão quando estruturas de código são parcialmente visíveis.

**Exemplo do problema:**
```diff
+        should_process = has_valid_input or has_cached_result
+            is_enabled
+            and meets_threshold_criteria
```

A LLM interpreta como erro de sintaxe porque não vê o `if (` que está numa linha não-modificada. O código completo é:
```python
        if (
            is_enabled
            and should_process
            and meets_threshold_criteria
        ):
```

**Estado atual:**
- O prompt já inclui instruções anti-falso-positivo
- O arquivo completo já está disponível na seção "ARQUIVOS MODIFICADOS"
- Mesmo assim, a LLM falha em correlacionar diff parcial com arquivo completo

## Goals / Non-Goals

**Goals:**
- Eliminar falsos positivos de sintaxe causados por diffs parciais
- Fornecer contexto visual suficiente para a LLM entender estruturas de código
- Manter compatibilidade com fluxo existente

**Non-Goals:**
- Mudar comportamento do git diff subjacente
- Resolver outros tipos de falsos positivos (imports, tipos, etc.)
- Adicionar validação de sintaxe real (AST parsing)

## Decisions

### 1. Usar `git diff -U<n>` para linhas de contexto
**Decisão:** Usar flag nativa do git (`-U3` ou `-U5`) em vez de processar manualmente.

**Alternativas consideradas:**
- Processar manualmente lendo arquivo e extraindo linhas → complexo, propenso a erros
- Usar biblioteca de parsing de diff → dependência adicional desnecessária

**Rationale:** Git já tem suporte nativo, menos código, mais confiável.

### 2. Default de 3 linhas de contexto
**Decisão:** Usar 3 linhas antes e depois de cada hunk como padrão.

**Alternativas consideradas:**
- 0 linhas (atual) → causa o problema
- 5 linhas → pode inflar o prompt desnecessariamente
- 10 linhas → muito contexto, ruído

**Rationale:** 3 linhas é suficiente para capturar a maioria das estruturas de controle (if/for/while/with) sem inflar demais o prompt.

### 3. Marcadores visuais de contexto
**Decisão:** Usar formato padrão do diff unificado onde linhas sem `+`/`-` são contexto.

**Formato:**
```diff
         if (
+            is_from_open_api
+            and payload_has_stocks_or_prices
         ):
```

**Rationale:** Formato já é reconhecido por LLMs treinadas em código. Não precisa de marcadores especiais.

### 4. Flag CLI opcional
**Decisão:** Adicionar `--context-lines N` (alias `-C N`) com default 3.

**Rationale:** Permite ajuste para casos especiais sem mudar comportamento padrão.

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| Prompts maiores aumentam custo de tokens | Default conservador de 3 linhas; documentar impacto |
| Mais contexto pode confundir a LLM sobre escopo | Instruções explícitas: "linhas sem +/- são apenas contexto" |
| Mudança no diff_parser pode quebrar testes | Manter interface compatível, adicionar testes para novo comportamento |

## Migration Plan

1. Atualizar `diff_parser.py` para aceitar parâmetro de contexto
2. Modificar comando git diff para usar `-U<n>`
3. Atualizar `prompt_builder.py` para formatar com contexto
4. Adicionar instrução no prompt explicando linhas de contexto
5. Adicionar flag `--context-lines` ao CLI
6. Atualizar testes

**Rollback:** Flag `--context-lines 0` restaura comportamento anterior.
