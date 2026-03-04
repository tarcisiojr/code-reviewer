## Context

O airev é uma CLI Python/Click que executa code reviews com IA. Atualmente não possui nenhuma telemetria de uso — apenas checagem de versão contra o PyPI. O projeto já utiliza `~/.cache/airev/` para persistência local e segue o padrão de opt-out via variável de ambiente (ex: `AIREV_NO_UPDATE_CHECK=1`).

O fluxo principal é o comando `review`, que passa por: extração de diff → parsing → backtracking de contexto → chamada ao runner IA → parsing de resposta → exibição. Cada etapa pode falhar, e queremos visibilidade sobre sucesso/falha desse pipeline.

## Goals / Non-Goals

**Goals:**

- Capturar eventos anônimos do ciclo de review para entender padrões de uso
- Zero impacto no tempo de execução percebido pelo usuário
- Falha totalmente silenciosa — nenhum erro de telemetria deve aparecer no console
- Opt-out simples via `AIREV_NO_TELEMETRY=1`
- Identificação anônima persistente via UUID local

**Non-Goals:**

- Rastrear dados sensíveis (código, branches, paths, descrições)
- Telemetria em tempo real ou dashboards operacionais
- A/B testing ou feature flags via PostHog
- Telemetria nos comandos `runners` e `upgrade` (escopo futuro)

## Decisions

### 1. PostHog Python SDK como client

**Escolha:** Usar o SDK oficial `posthog` em vez de HTTP raw com urllib.

**Alternativas consideradas:**
- **urllib raw** — Segue o padrão do `http_client.py` existente, zero dependências. Porém, requer implementar manualmente o POST para `/capture/`, sem retries ou batching.
- **PostHog SDK** — Dependência adicional, mas gerencia consumer thread, serialização, e edge cases de flush.

**Razão:** Para 1-2 eventos por execução, o SDK é suficientemente leve e evita reimplementar lógica que já existe. O SDK é bem mantido e lida com cenários de rede instável.

### 2. Flush com atexit + thread com timeout

**Escolha:** Registrar `atexit` handler que faz `posthog.flush()` em uma thread daemon com timeout de 2 segundos.

**Alternativas consideradas:**
- **`posthog.flush()` síncrono no final** — Simples, mas bloqueia a CLI se a rede estiver lenta.
- **`posthog.shutdown()` direto** — Pode demorar indefinidamente.
- **Daemon thread sem join** — Eventos podem se perder se o process exit for rápido demais.

**Razão:** Thread com timeout garante: (1) flush acontece na maioria dos casos, (2) nunca trava mais que 2s, (3) funciona com `sys.exit()` graças ao `atexit`.

```
atexit registrado
       │
       ▼
┌──────────────┐     ┌───────────┐
│ Thread daemon │────▶│  flush()  │──▶ HTTP POST ao PostHog
│  timeout=2s  │     └───────────┘
└──────────────┘
       │
  join(timeout=2)
       │
   process exit
```

### 3. UUID persistido em ~/.cache/airev/anonymous_id

**Escolha:** Gerar UUID v4 na primeira execução e salvar em `~/.cache/airev/anonymous_id`.

**Alternativas consideradas:**
- **Hash do hostname+username** — Determinístico, mas pode ser reversível e viola a proposta de anonimato.
- **UUID em ~/.config/airev/** — Semanticamente mais correto (config vs cache), mas o projeto já usa `~/.cache/airev/`.
- **Sem persistência (UUID por sessão)** — Impossibilita análise de retenção e frequência de uso.

**Razão:** UUID v4 é verdadeiramente anônimo, não-reversível, e `~/.cache/airev/` já existe no projeto.

### 4. Lazy initialization do client PostHog

**Escolha:** Inicializar o SDK PostHog apenas quando a telemetria está habilitada e um evento é capturado pela primeira vez.

**Razão:** Evita import e setup do SDK em cenários de opt-out ou quando a CLI é invocada para help/version. Minimiza impacto no startup time.

```python
# Padrão: módulo expõe funções simples, inicialização interna é lazy
from .analytics import track_event, shutdown_analytics

track_event("review_started", {...})  # inicializa SDK na primeira chamada
```

### 5. Estrutura do módulo analytics/

```
src/code_reviewer/analytics/
├── __init__.py      # API pública: track_event(), shutdown_analytics(), is_enabled()
├── client.py        # Setup e wrapper do PostHog SDK (lazy init, flush, shutdown)
└── identity.py      # Geração e leitura do UUID persistido
```

**Separação de responsabilidades:**
- `identity.py` — Apenas lida com UUID (gerar, ler, salvar). Sem dependência do PostHog.
- `client.py` — Encapsula o SDK PostHog. Conhece api_key e host. Gerencia lifecycle.
- `__init__.py` — Fachada que combina identity + client. Checa opt-out. Expõe API simples.

### 6. Eventos e propriedades

| Evento | Propriedades |
|---|---|
| `review_started` | `runner`, `lang`, `json_output`, `text_quality`, `show_deps`, `no_interactive`, `min_confidence`, `context_lines`, `version` |
| `review_completed` | `duration_s`, `files_count`, `findings_total`, `findings_critical`, `findings_warning`, `findings_info`, `version` |
| `review_failed` | `error_type` (`diff_error`, `runner_unavailable`, `runner_not_found`, `runner_error`, `parse_error`, `branch_error`), `version` |

**Invariantes:**
- Nenhum evento contém: nomes de branch, paths de arquivo, código, descrições, mensagens de erro
- `version` presente em todos os eventos para correlação com releases
- `error_type` é uma string enum fixa, nunca contém a mensagem de erro real

## Risks / Trade-offs

- **Dependência extra (`posthog`)** → Risco baixo. SDK é leve, bem mantido, e usado amplamente. Impacto no install size é mínimo.

- **Eventos perdidos em redes lentas** → Aceito. O timeout de 2s é um trade-off explícito entre garantia de entrega e experiência do usuário. Para analytics agregados, perda parcial é tolerável.

- **UUID deletado pelo usuário** → Um novo UUID é gerado. O usuário aparece como "novo" no PostHog. Comportamento aceitável — não é um sistema de autenticação.

- **Percepção negativa sobre telemetria** → Mitigado por: opt-out fácil, zero dados sensíveis, documentação clara no README sobre o que é coletado.

- **Import do SDK impacta startup** → Mitigado por lazy init. O SDK só é importado quando o primeiro evento é capturado.
