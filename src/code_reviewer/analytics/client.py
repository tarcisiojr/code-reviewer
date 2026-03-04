"""Client PostHog com inicialização lazy e flush assíncrono.

O SDK é importado e inicializado apenas na primeira chamada a capture(),
evitando overhead quando a telemetria está desabilitada.
"""

import atexit
import logging
import threading

# Chave e host do PostHog (projeto airev)
_API_KEY = "phc_Pa2Q1ssNkenBX1T0G3FbJ89aRJswyPwEJhtixiOo01N"
_HOST = "https://us.i.posthog.com"
_REQUEST_TIMEOUT = 5

# Estado do client (inicialização lazy)
_initialized = False
_posthog = None


def _ensure_initialized():
    """Inicializa o SDK PostHog na primeira chamada (lazy init)."""
    global _initialized, _posthog

    if _initialized:
        return

    try:
        from posthog import Posthog

        # Suprime todos os logs do SDK (erros de rede, SSL, etc.)
        posthog_logger = logging.getLogger("posthog")
        posthog_logger.setLevel(logging.CRITICAL + 1)
        posthog_logger.addHandler(logging.NullHandler())
        posthog_logger.propagate = False

        _posthog = Posthog(
            _API_KEY,
            host=_HOST,
            timeout=_REQUEST_TIMEOUT,
            max_retries=1,
            on_error=lambda error, items: None,
        )
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
            _posthog.capture(
                event,
                distinct_id=distinct_id,
                properties=properties or {},
            )
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
