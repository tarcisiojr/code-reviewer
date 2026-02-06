## Context

O CLI atual usa `click.echo()` para mensagens simples de progresso. A formatação de resultados usa ANSI codes manuais em `formatters/terminal.py`. Não há feedback visual durante operações demoradas como a chamada à IA.

## Goals / Non-Goals

**Goals:**
- Mostrar progresso animado durante cada etapa do pipeline
- Usar biblioteca `rich` para UI consistente e rica
- Suportar modo CI/pipe sem animações
- Manter compatibilidade com `--json-output`

**Non-Goals:**
- Alterar o formato da saída final dos findings (já está bom)
- Adicionar níveis de verbosidade múltiplos (verbose, debug) - apenas on/off para animações
- Suportar temas ou customização de cores

## Decisions

### 1. Usar `rich` em vez de continuar com ANSI manual

**Escolha:** Migrar para biblioteca `rich`

**Alternativas consideradas:**
- Continuar com ANSI codes manuais: mais trabalho, menos features
- Usar `click.progressbar`: limitado, sem spinners
- Usar `tqdm`: focado em progress bars, não em spinners/status

**Rationale:** `rich` oferece Console, Status (spinners), Progress, e Panel em uma API consistente. Já é padrão de mercado para CLIs Python modernos.

### 2. Criar classe `ProgressReporter` para encapsular output

**Escolha:** Novo módulo `src/code_reviewer/formatters/progress.py`

```python
class ProgressReporter:
    def __init__(self, console: Console, enabled: bool = True):
        self.console = console
        self.enabled = enabled

    def status(self, message: str) -> ContextManager:
        if self.enabled:
            return self.console.status(message, spinner="dots")
        return nullcontext()

    def step(self, message: str):
        self.console.print(f"[dim]→[/dim] {message}")
```

**Rationale:** Encapsula a lógica de animação vs texto simples em um só lugar.

### 3. Detectar modo CI automaticamente

**Escolha:** Verificar `sys.stdout.isatty()` e variáveis de ambiente comuns

```python
def is_ci_environment() -> bool:
    if not sys.stdout.isatty():
        return True
    ci_vars = ["CI", "GITLAB_CI", "GITHUB_ACTIONS", "JENKINS_URL"]
    return any(os.environ.get(var) for var in ci_vars)
```

**Rationale:** GitLab CI, GitHub Actions e Jenkins definem essas variáveis. Combinado com TTY check, cobre a maioria dos casos.

### 4. Flag `--no-progress` em vez de `--ci`

**Escolha:** `--no-progress`

**Alternativas consideradas:**
- `--ci`: Pode ter outras implicações futuras
- `--quiet`: Confuso - não silencia tudo, só animações

**Rationale:** Nome descritivo que indica exatamente o que faz.

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| `rich` aumenta dependências | Biblioteca leve (~3MB), amplamente usada |
| Migrar terminal.py pode quebrar testes | Manter funções existentes, adicionar novas em paralelo |
| Spinners podem não funcionar em alguns terminais | Fallback automático do rich para texto simples |
| Tempo de execução das etapas impreciso | Usar `time.perf_counter()` para medição precisa |
