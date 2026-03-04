"""Gerenciamento de identidade anônima para telemetria.

Gera e persiste um UUID v4 em ~/.cache/airev/anonymous_id
para identificação anônima nos eventos PostHog.
"""

import uuid
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "airev"
ID_FILE = CACHE_DIR / "anonymous_id"


def _is_valid_uuid(value: str) -> bool:
    """Verifica se o valor é um UUID v4 válido."""
    try:
        uuid.UUID(value, version=4)
        return True
    except (ValueError, AttributeError):
        return False


def get_anonymous_id() -> str | None:
    """Obtém ou gera o ID anônimo persistido.

    Na primeira execução, gera um UUID v4 e salva em disco.
    Nas execuções seguintes, reutiliza o UUID existente.
    Se o arquivo estiver corrompido, regenera o UUID.

    Returns:
        UUID string ou None se não for possível ler/gravar.
    """
    try:
        # Tenta ler ID existente
        if ID_FILE.exists():
            stored = ID_FILE.read_text().strip()
            if _is_valid_uuid(stored):
                return stored

        # Gera novo UUID (primeira execução ou arquivo corrompido)
        new_id = str(uuid.uuid4())
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        ID_FILE.write_text(new_id)
        return new_id
    except OSError:
        # Diretório não-gravável — opera sem telemetria
        return None
