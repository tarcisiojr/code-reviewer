## Why

O airev não tem visibilidade sobre como a ferramenta é usada. Sem telemetria, não é possível saber quais features são populares, quais runners são preferidos, ou qual a taxa de erro. Adicionar analytics anônimos com PostHog permite tomar decisões de produto baseadas em dados reais de uso.

## What Changes

- Novo módulo `analytics/` com client PostHog, gerenciamento de identidade anônima (UUID) e controle de opt-out
- Integração de eventos de telemetria no fluxo do comando `review` (`review_started`, `review_completed`, `review_failed`)
- Nova dependência: `posthog` (Python SDK)
- Novo arquivo de persistência: `~/.cache/airev/anonymous_id` (UUID gerado na primeira execução)
- Nova variável de ambiente `AIREV_NO_TELEMETRY=1` para opt-out
- Flush assíncrono com timeout de 2s via `atexit` para não bloquear a CLI

## Capabilities

### New Capabilities

- `usage-analytics`: Telemetria anônima de uso via PostHog — captura eventos do ciclo de review (início, conclusão, falha) com metadados não-sensíveis (runner, flags, contagens, duração). Opt-out via env var `AIREV_NO_TELEMETRY=1`. Identidade baseada em UUID persistido localmente.

### Modified Capabilities

_(nenhuma — a telemetria é transparente e não altera o comportamento existente)_

## Impact

- **Dependências**: Nova dependência `posthog` no `pyproject.toml`
- **Código**: Novo módulo `src/code_reviewer/analytics/`, modificações em `cli.py` para instrumentação de eventos
- **Rede**: Requests HTTP adicionais ao PostHog (fire-and-forget, não bloqueantes)
- **Armazenamento local**: Arquivo `~/.cache/airev/anonymous_id` (~36 bytes)
- **Privacidade**: Nenhum dado sensível enviado — sem código, branches, paths ou descrições. Apenas metadados anônimos (runner, flags booleanos, contagens numéricas, duração)
