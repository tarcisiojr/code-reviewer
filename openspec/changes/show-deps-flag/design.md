## Context

O airev já coleta callers/callees via `context_builder.py` e monta `ContextGraph` para cada função modificada. Esses dados são formatados em `prompt_builder.py` para envio à IA, mas nunca são exibidos ao usuário.

A estrutura `ContextGraph` contém:
- `function_name`: nome da função modificada
- `file`: arquivo onde está a função
- `callers`: lista de `FunctionRef` (file, line, snippet)
- `callees`: lista de `FunctionRef` (file, line, function_name)
- `file_content`: conteúdo completo do arquivo

O formatter atual (`terminal.py`) agrupa findings por arquivo, mas não tem acesso ao `ContextGraph`.

## Goals / Non-Goals

**Goals:**
- Permitir que o usuário visualize o grafo de dependências no terminal
- Integrar a visualização por arquivo, junto com os findings
- Mostrar deps de todas as funções modificadas (com ou sem findings)
- Usar formato de árvore ASCII legível

**Non-Goals:**
- Alterar a coleta de dependências (já existe e funciona)
- Adicionar novos formatos de output (DOT, JSON específico para deps)
- Aumentar profundidade do backtracking (mantém 1 nível)
- Filtrar ou agrupar deps por tipo/módulo

## Decisions

### 1. Flag `--show-deps` / `-D` (opt-in)

**Decisão**: A visualização de deps é opt-in via flag.

**Alternativas consideradas**:
- Sempre mostrar deps → aumenta ruído para quem só quer findings
- Flag `--hide-deps` (opt-out) → muda comportamento default, breaking change implícito

**Rationale**: Opt-in mantém o comportamento atual como default e permite adoção gradual.

### 2. Passar `context_graphs` para o formatter

**Decisão**: Modificar `format_result()` para receber `context_graphs` como parâmetro opcional.

**Alternativas consideradas**:
- Adicionar `context_graphs` ao modelo `ReviewResult` → mistura dados de análise com dados de apresentação
- Criar novo modelo `RichReviewResult` → over-engineering para uma flag

**Rationale**: Parâmetro opcional mantém a interface simples e não polui o modelo de dados.

### 3. Mapear ContextGraph → arquivo para integração

**Decisão**: Criar dicionário `deps_by_file: dict[str, list[ContextGraph]]` agrupando por `graph.file`.

**Rationale**: O formatter já itera por arquivo ao renderizar findings. O agrupamento permite inserir deps antes dos findings de cada arquivo.

### 4. Formato de renderização

**Decisão**: Árvore ASCII com emojis para callers/callees.

```
📊 DEPENDENCIES: function_name (linha N)
│
├── 📥 CALLERS (N)
│   ├── path/file.py:42     → snippet_do_caller
│   └── path/other.py:87    → outro_snippet
│
└── 📤 CALLEES (N)
    ├── callee_name         → path/def.py:23
    └── outro_callee        → path/impl.py:56
```

**Alternativas consideradas**:
- Formato tabular → menos legível para relações hierárquicas
- Formato compacto em linha → perde clareza

**Rationale**: Árvore ASCII é familiar (tree, cargo tree) e expressa bem a relação caller→função→callee.

### 5. Arquivos sem findings mas com deps

**Decisão**: Mostrar seção de deps + mensagem "✅ Sem findings neste arquivo".

**Rationale**: O usuário pediu para ver deps de todas as funções modificadas, não só das problemáticas.

## Risks / Trade-offs

**[Output muito longo]** → Se muitas funções modificadas, o output pode ficar extenso.
- *Mitigação*: Aceitar por agora. Futuramente pode-se adicionar `--deps-limit N`.

**[Deps sem contexto de findings]** → Usuário pode não entender por que deps são mostrados.
- *Mitigação*: Header claro "📊 DEPENDENCIES" e documentação na ajuda do CLI.

**[Performance]** → Nenhum impacto, pois os dados já são coletados.
- *Mitigação*: N/A.
