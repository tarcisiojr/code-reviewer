"""Módulo de internacionalização (i18n) para o Code Reviewer CLI."""

import warnings
from pathlib import Path
from typing import Any

import yaml

# Diretório onde estão os arquivos de locale
LOCALES_DIR = Path(__file__).parent.parent / "locales"

# Idioma padrão (fallback)
DEFAULT_LANGUAGE = "pt-br"

# Estado global
_current_language: str = DEFAULT_LANGUAGE
_translations_cache: dict[str, dict[str, Any]] = {}


def get_available_languages() -> list[str]:
    """Retorna lista de idiomas disponíveis.

    Returns:
        Lista de códigos de idioma disponíveis (ex: ["pt-br", "en"])
    """
    if not LOCALES_DIR.exists():
        return [DEFAULT_LANGUAGE]

    languages = []
    for file in LOCALES_DIR.glob("*.yaml"):
        languages.append(file.stem)

    # Garante que o idioma padrão está na lista
    if DEFAULT_LANGUAGE not in languages:
        languages.insert(0, DEFAULT_LANGUAGE)

    return sorted(languages)


def load_translations(lang: str) -> dict[str, Any]:
    """Carrega traduções de um idioma específico.

    Args:
        lang: Código do idioma (ex: "pt-br", "en")

    Returns:
        Dicionário com as traduções carregadas
    """
    # Verifica cache primeiro
    if lang in _translations_cache:
        return _translations_cache[lang]

    locale_file = LOCALES_DIR / f"{lang}.yaml"

    if not locale_file.exists():
        if lang != DEFAULT_LANGUAGE:
            warnings.warn(
                f"Arquivo de locale '{lang}' não encontrado. Usando fallback '{DEFAULT_LANGUAGE}'.",
                UserWarning,
                stacklevel=2,
            )
            return load_translations(DEFAULT_LANGUAGE)
        # Se nem o padrão existe, retorna vazio
        return {}

    with open(locale_file, encoding="utf-8") as f:
        translations = yaml.safe_load(f) or {}

    # Armazena no cache
    _translations_cache[lang] = translations
    return translations


def _get_nested_value(data: dict[str, Any], key: str) -> str | None:
    """Obtém valor aninhado de um dicionário usando notação de ponto.

    Args:
        data: Dicionário com os dados
        key: Chave com notação de ponto (ex: "cli.analyzing")

    Returns:
        Valor encontrado ou None
    """
    parts = key.split(".")
    current = data

    for part in parts:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
        if current is None:
            return None

    return str(current) if current is not None else None


def t(key: str, **kwargs: Any) -> str:
    """Obtém uma tradução para a chave especificada.

    Args:
        key: Chave da tradução (ex: "cli.analyzing")
        **kwargs: Variáveis para interpolação (ex: branch="main")

    Returns:
        String traduzida com variáveis substituídas
    """
    translations = load_translations(_current_language)
    value = _get_nested_value(translations, key)

    # Fallback para idioma padrão se não encontrar
    if value is None and _current_language != DEFAULT_LANGUAGE:
        default_translations = load_translations(DEFAULT_LANGUAGE)
        value = _get_nested_value(default_translations, key)

    # Se ainda não encontrou, retorna a própria chave
    if value is None:
        return key

    # Interpolação de variáveis
    if kwargs:
        try:
            value = value.format(**kwargs)
        except KeyError:
            # Se faltar variável, retorna sem substituição
            pass

    return value


def set_language(lang: str) -> None:
    """Define o idioma atual para traduções.

    Args:
        lang: Código do idioma (ex: "pt-br", "en")
    """
    global _current_language

    available = get_available_languages()
    if lang not in available:
        warnings.warn(
            f"Idioma '{lang}' não disponível. Disponíveis: {available}. Usando '{DEFAULT_LANGUAGE}'.",
            UserWarning,
            stacklevel=2,
        )
        _current_language = DEFAULT_LANGUAGE
    else:
        _current_language = lang


def get_language() -> str:
    """Retorna o idioma atualmente configurado.

    Returns:
        Código do idioma atual
    """
    return _current_language


def reset_language() -> None:
    """Reseta o idioma para o padrão (útil para testes)."""
    global _current_language
    _current_language = DEFAULT_LANGUAGE


def clear_cache() -> None:
    """Limpa o cache de traduções (útil para testes)."""
    _translations_cache.clear()


# Exports públicos
__all__ = [
    "t",
    "set_language",
    "get_language",
    "get_available_languages",
    "load_translations",
    "reset_language",
    "clear_cache",
    "DEFAULT_LANGUAGE",
]
