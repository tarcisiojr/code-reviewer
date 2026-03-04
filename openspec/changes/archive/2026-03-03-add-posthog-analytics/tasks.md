## 1. Dependências e estrutura

- [x] 1.1 Adicionar `posthog` como dependência no `pyproject.toml`
- [x] 1.2 Criar estrutura do módulo `src/code_reviewer/analytics/` (`__init__.py`, `client.py`, `identity.py`)

## 2. Identidade anônima

- [x] 2.1 Implementar `identity.py` — geração de UUID v4, leitura/gravação em `~/.cache/airev/anonymous_id`, tratamento de arquivo corrompido
- [x] 2.2 Escrever testes para `identity.py` — primeira execução, reutilização, arquivo corrompido, diretório não-gravável

## 3. Client PostHog

- [x] 3.1 Implementar `client.py` — inicialização lazy do SDK PostHog com api_key e host, wrapper para `capture()`, flush com thread+timeout via `atexit`
- [x] 3.2 Escrever testes para `client.py` — lazy init, flush com timeout, falha silenciosa em erro de rede

## 4. Fachada do módulo analytics

- [x] 4.1 Implementar `__init__.py` — `track_event()`, `shutdown_analytics()`, `is_enabled()`, checagem de opt-out (`AIREV_NO_TELEMETRY`), integração identity+client
- [x] 4.2 Escrever testes para `__init__.py` — opt-out desabilita tudo, SDK não importado quando desabilitado, eventos capturados corretamente

## 5. Instrumentação na CLI

- [x] 5.1 Adicionar `track_event("review_started", {...})` no início do comando `review` com flags de configuração
- [x] 5.2 Adicionar `track_event("review_completed", {...})` no final bem-sucedido com duração e contagens
- [x] 5.3 Adicionar `track_event("review_failed", {...})` em cada ponto de falha com `error_type` apropriado
- [x] 5.4 Registrar `shutdown_analytics()` via `atexit` no início do comando `review`

## 6. Validação e documentação

- [x] 6.1 Executar todos os testes e validar que a suíte existente continua passando
- [x] 6.2 Adicionar seção no README sobre telemetria e opt-out
