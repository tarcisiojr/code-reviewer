"""Fachada do módulo de analytics — API pública para telemetria.

Combina identity + client e gerencia opt-out via env var.
Todas as funções são seguras para chamar em qualquer contexto —
falham silenciosamente sem afetar o fluxo principal.

Uso:
    from code_reviewer.analytics import track_event, shutdown_analytics

    track_event("review_started", {"runner": "gemini"})
"""

import os


def is_enabled() -> bool:
    """Verifica se a telemetria está habilitada.

    Desabilitada quando AIREV_NO_TELEMETRY=1.
    """
    return os.environ.get("AIREV_NO_TELEMETRY", "").strip() != "1"


def track_event(event: str, properties: dict | None = None):
    """Captura um evento de telemetria anônimo.

    Se a telemetria estiver desabilitada via AIREV_NO_TELEMETRY=1,
    esta função é no-op. Falha silenciosamente em qualquer erro.

    Args:
        event: Nome do evento (ex: "review_started").
        properties: Propriedades do evento.
    """
    if not is_enabled():
        return

    try:
        from .client import capture
        from .identity import get_anonymous_id

        distinct_id = get_anonymous_id()
        if distinct_id is None:
            return

        capture(distinct_id, event, properties)
    except Exception:
        # Falha silenciosa total
        pass


def shutdown_analytics():
    """Encerra o módulo de analytics (flush final).

    Seguro para chamar mesmo se a telemetria estiver desabilitada.
    """
    if not is_enabled():
        return

    try:
        from .client import shutdown

        shutdown()
    except Exception:
        pass
