## Context

O prompt interativo de descrição de alterações (`ask_description_interactive()` em `description_input.py`) usa `prompt_toolkit` com `multiline=True`. Nesse modo padrão, Enter cria nova linha e Alt+Enter envia — o oposto do que o usuário espera. Os usuários colam texto do MR e ficam presos sem saber como enviar.

A referência de UX são o Claude Code e Copilot CLI, onde Enter sempre envia e Shift+Enter cria nova linha.

## Goals / Non-Goals

**Goals:**
- Enter SHALL enviar o texto (submit)
- Shift+Enter e `\`+Enter SHALL criar nova linha
- Esc SHALL cancelar e seguir sem descrição
- Texto colado via Ctrl+V SHALL preservar quebras de linha
- Mensagem de instrução SHALL ser clara e concisa sobre os atalhos

**Non-Goals:**
- Alterar o fluxo de prioridade de entrada (flag > stdin > interativo)
- Alterar o limite de caracteres
- Configuração de terminal do usuário (Shift+Enter depende do terminal)
- Suportar editor externo (ex: $EDITOR) para entrada de texto

## Decisions

### 1. Manter `multiline=True` com key bindings invertidos

**Decisão:** Usar `multiline=True` e sobrescrever os bindings de Enter e Alt+Enter.

**Alternativa descartada:** Usar `multiline=False` — não renderiza múltiplas linhas corretamente na tela.

**Racional:** O mantenedor do prompt_toolkit recomenda essa abordagem (Issue #728). O `multiline=True` configura o layout de renderização para exibir múltiplas linhas, enquanto os key bindings controlam o comportamento das teclas independentemente.

**Implementação:**
- `@kb.add('enter')` → verifica se termina com `\`, se sim remove e insere `\n`; se não, `validate_and_handle()` (envia)
- `@kb.add('escape', 'enter')` → `insert_text('\n')` (captura Shift+Enter / Alt+Enter)

### 2. Esc para cancelar via `event.app.exit(result=None)`

**Decisão:** Usar binding `@kb.add('escape')` sem `eager` para cancelar.

**Trade-off:** Existe um delay de ~50ms porque o terminal precisa distinguir Esc isolado de sequências que começam com Esc (como Shift+Enter = `\x1b\r`). O prompt_toolkit resolve isso via timeout.

**Racional:** O delay é quase imperceptível e Esc é mais intuitivo que Ctrl+C para "cancelar e seguir". O resultado será `None`, tratado da mesma forma que o cancelamento atual.

### 3. Bracketed paste sem configuração adicional

**Decisão:** Não customizar o handler de bracketed paste.

**Racional:** Com `multiline=True`, o prompt_toolkit já preserva newlines do texto colado automaticamente via `Keys.BracketedPaste`. Funciona em todos os terminais modernos sem configuração.

### 4. Mensagem de instrução reformulada

**Decisão:** Mensagem curta com separadores visuais:
```
📝 Descrição das alterações (cole o texto do MR):
   Enter envia · Shift+Enter ou \ para nova linha · Esc para pular
```

**Racional:** Informação essencial primeiro (Enter envia), atalhos secundários depois, tudo numa linha. O formato com `·` é limpo e escaneável.

## Risks / Trade-offs

- **[Shift+Enter não funciona em todos os terminais]** → Mitigação: `\`+Enter funciona universalmente como alternativa. A mensagem lista as duas opções.
- **[Esc tem delay de ~50ms]** → Mitigação: delay é imperceptível para humanos. Se for problema, pode ser substituído por Ctrl+C no futuro.
- **[Esc pode conflitar com bindings de terminal]** → Mitigação: o prompt_toolkit resolve conflitos via timeout; testado com iTerm2, Terminal.app, VS Code.
