"""Client PostHog com inicialização lazy e flush assíncrono.

O SDK é importado e inicializado apenas na primeira chamada a capture(),
evitando overhead quando a telemetria está desabilitada.
"""

import atexit
import threading

# Chave e host do PostHog (projeto airev)
_API_KEY = "phc_Pa2Q1ssNkenBX1T0G3FbJ89aRJswyPwEJhtixiOo01N"
_HOST = "https://us.i.posthog.com"

# Estado do client (inicialização lazy)
_initialized = False
_posthog = None


def _ensure_initialized():
    """Inicializa o SDK PostHog na primeira chamada (lazy init)."""
    global _initialized, _posthog

    if _initialized:
        return

    try:
        import posthog

        posthog.project_api_key = _API_KEY
        posthog.host = _HOST
        posthog.debug = False
        # Desabilita logs do SDK para falha silenciosa
        posthog.disabled = False
        _posthog = posthog
        _initialized = True

        # Registra flush no encerramento do processo
        atexit.register(_flush_with_timeout)
    except Exception:
        # Falha silenciosa se o SDK não puder ser importado
        _initialized = True


def capture(distinct_id: str, event: str, properties: dict | None = None):
    """Envia evento ao PostHog.

    Args:
        distinct_id: ID anônimo do usuário.
        event: Nome do evento.
        properties: Propriedades do evento.
    """
    try:
        _ensure_initialized()
        if _posthog is not None:
            _posthog.capture(distinct_id, event, properties or {})
    except Exception:
        # Falha silenciosa — nenhum erro de telemetria deve aparecer
        pass


def _flush_with_timeout(timeout: float = 2.0):
    """Executa flush do PostHog em thread daemon com timeout.

    Garante que eventos pendentes são enviados sem bloquear
    o encerramento do processo por mais de `timeout` segundos.
    """
    if _posthog is None:
        return

    def _do_flush():
        try:
            _posthog.flush()
        except Exception:
            pass

    thread = threading.Thread(target=_do_flush, daemon=True)
    thread.start()
    thread.join(timeout=timeout)


def shutdown():
    """Encerra o client PostHog (flush final)."""
    _flush_with_timeout()
