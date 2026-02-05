## Context

Projeto greenfield — não existe código no repositório ainda. A ferramenta será uma CLI Python que analisa diffs de branches git e envia contexto estruturado para CLIs de IA (Gemini CLI, Copilot CLI, etc.) obter uma análise de código focada em segurança, performance e bugs. O diferencial é o módulo de backtracking que traça callers/callees das funções modificadas, fornecendo contexto que nenhuma ferramenta open source oferece hoje.

O ambiente alvo é GitLab CI, mas o MVP roda localmente no terminal. O CLI de IA já possui tools nativos (leitura de arquivos, MCPs, extensões) — nosso wrapper é o "curador de contexto" e o CLI é o "cérebro".

## Goals / Non-Goals

**Goals:**
- Ferramenta CLI funcional que analisa diff de uma branch e retorna findings no terminal
- Backtracking de contexto: rastrear callers e callees das funções modificadas via grep
- Saída estruturada em JSON parseável para operações futuras
- Interface plugável de runners para trocar entre CLIs de IA sem mudar o código
- Renderização formatada no terminal com severidades (CRITICAL, WARNING, INFO)

**Non-Goals:**
- Integração direta com API do GitLab (futuro)
- Exit codes para falhar pipelines (futuro)
- Suporte a análise de repositórios remotos (só local)
- Análise estática sem IA (não é um linter)
- Sugestões de melhoria em código não alterado pelo desenvolvedor

## Decisions

### 1. Estrutura do projeto: src layout com pyproject.toml

**Decisão**: Usar src layout (`src/code_reviewer/`) com pyproject.toml e entry point via console_scripts.

**Alternativas consideradas**:
- Flat layout (`code_reviewer/` na raiz) — mais simples, mas src layout evita imports acidentais e é o padrão recomendado pela PyPA.

**Rationale**: src layout é o padrão moderno para projetos Python distribuíveis. O entry point `code-reviewer` via console_scripts permite instalação com `pip install .` e uso direto no terminal.

### 2. CLI framework: click

**Decisão**: Usar `click` para a interface CLI.

**Alternativas consideradas**:
- `argparse` (stdlib) — zero dependências, mas verboso e sem features como grupos de comandos, auto-help, e tipos customizados.
- `typer` — moderno, baseado em type hints, mas adiciona dependência extra e é menos estabelecido.

**Rationale**: click é maduro, bem documentado, e permite crescer para subcomandos futuros (ex: `code-reviewer review`, `code-reviewer config`).

### 3. Parsing de diff: regex sobre output do git diff

**Decisão**: Parsear o output de `git diff <base>...HEAD` com regex para extrair hunk headers (nomes de funções), arquivos modificados e linhas alteradas.

**Alternativas consideradas**:
- `unidiff` (biblioteca Python) — faz parsing de unified diff, mas não extrai nomes de funções dos hunk headers.
- Tree-sitter para AST — preciso mas pesado e language-specific.

**Rationale**: Os hunk headers do git (`@@ -10,5 +10,7 @@ def function_name`) já contêm os nomes das funções. Regex é suficiente para o MVP e não adiciona dependência.

### 4. Backtracking: grep-based via subprocess

**Decisão**: Para cada função identificada no diff, usar `grep -rn "function_name("` no projeto para encontrar callers, e parsear as linhas adicionadas no diff para identificar callees.

**Alternativas consideradas**:
- AST parsing (ast module do Python) — preciso mas só funciona para Python.
- Language Server Protocol (LSP) — muito preciso mas complexo demais para MVP.
- ctags/cscope — requer setup adicional.

**Rationale**: grep é universal, funciona para qualquer linguagem, é rápido e não adiciona dependências. Limitamos a 5 referências por símbolo e 10 linhas de contexto ao redor para controlar o tamanho.

### 5. Interface de runners: Protocol (structural typing)

**Decisão**: Usar `typing.Protocol` para definir a interface `AIRunner` com método `run(prompt: str, workdir: Path) -> str`. Cada CLI de IA tem sua implementação.

```
runners/
├── base.py      ← Protocol AIRunner
├── gemini.py    ← GeminiCLIRunner
├── copilot.py   ← CopilotCLIRunner
└── claude.py    ← ClaudeCLIRunner
```

**Alternativas consideradas**:
- ABC (Abstract Base Class) — requer herança explícita.
- Funções simples — menos estruturado, dificulta mock em testes.

**Rationale**: Protocol permite duck typing, não exige herança, e facilita testes com mocks. Cada runner encapsula as particularidades de como o CLI recebe prompt e retorna output.

### 6. Schema de saída: JSON validado com Pydantic

**Decisão**: O prompt instrui a IA a retornar JSON com schema definido. O wrapper valida com modelos Pydantic (`ReviewResult`, `Finding`). Fallbacks para quando o JSON vem malformado.

**Campos do Finding**:
- `file`: caminho do arquivo
- `line`: número da linha
- `severity`: CRITICAL | WARNING | INFO
- `category`: security | performance | bug | resource-leak
- `title`: título curto
- `description`: explicação do problema
- `suggestion`: sugestão de correção
- `code_snippet`: trecho de código relevante

**Alternativas consideradas**:
- dataclasses — mais simples, mas sem validação automática.
- JSON Schema manual — mais verboso e sem type checking.

**Rationale**: Pydantic oferece validação, serialização e type checking. Os modelos servem como documentação viva do contrato de saída.

### 7. Prompt: arquivo markdown com placeholders

**Decisão**: O system prompt fica em `prompts/review_system.md` com placeholders (`{diff}`, `{context}`, `{references}`) substituídos em runtime.

**Rationale**: Separar prompt do código permite iterar no prompt sem mudar Python. O arquivo é versionado e pode ser customizado por projeto.

### 8. Arquitetura de módulos

```
src/code_reviewer/
├── cli.py                ← Entry point click
├── diff_parser.py        ← Parseia git diff
├── context_builder.py    ← Backtracking (grep-based)
├── prompt_builder.py     ← Monta prompt final
├── response_parser.py    ← Parseia/valida JSON
├── models.py             ← Pydantic models
├── runners/
│   ├── __init__.py
│   ├── base.py           ← Protocol AIRunner
│   ├── gemini.py         ← GeminiCLIRunner
│   └── copilot.py        ← CopilotCLIRunner
├── formatters/
│   ├── __init__.py
│   └── terminal.py       ← Renderiza no terminal
└── prompts/
    └── review_system.md  ← System prompt template
```

## Risks / Trade-offs

- **[Parsing de hunk headers pode falhar]** → Os hunk headers do git usam heurísticas para nomes de funções. Para linguagens com syntax incomum pode não funcionar. Mitigation: tratar como fallback sem nome de função e ainda analisar o diff.

- **[grep-based backtracking tem falsos positivos]** → grep pode encontrar matches em comentários ou strings. Mitigation: filtrar resultados óbvios (linhas começando com `#`, `//`, `/*`) e limitar quantidade de referências.

- **[LLM pode não retornar JSON válido]** → Mitigation: cadeia de fallbacks — json.loads direto → extrair de bloco ```json → regex para `{...}` → retornar como texto raw.

- **[Context window da IA pode estourar]** → Em MRs grandes com muitos arquivos e referências. Mitigation: limitar 5 refs por símbolo, 10 linhas de contexto, e no futuro implementar chunking (analisar arquivo por arquivo).

- **[Dependência de CLI externo instalado]** → O runner precisa que gemini-cli/copilot esteja instalado e configurado. Mitigation: verificação no startup com mensagem clara de erro.
