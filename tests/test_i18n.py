"""Testes para o módulo i18n."""

import pytest

from code_reviewer.i18n import (
    clear_cache,
    get_available_languages,
    get_language,
    load_translations,
    reset_language,
    set_language,
    t,
)


@pytest.fixture(autouse=True)
def reset_i18n_state():
    """Reseta o estado do i18n antes e depois de cada teste."""
    reset_language()
    clear_cache()
    yield
    reset_language()
    clear_cache()


class TestGetAvailableLanguages:
    """Testes para função get_available_languages."""

    def test_retorna_lista_idiomas(self):
        languages = get_available_languages()

        assert isinstance(languages, list)
        assert len(languages) >= 2

    def test_contem_pt_br(self):
        languages = get_available_languages()

        assert "pt-br" in languages

    def test_contem_en(self):
        languages = get_available_languages()

        assert "en" in languages


class TestLoadTranslations:
    """Testes para função load_translations."""

    def test_carrega_pt_br(self):
        translations = load_translations("pt-br")

        assert isinstance(translations, dict)
        assert "cli" in translations
        assert "terminal" in translations

    def test_carrega_en(self):
        translations = load_translations("en")

        assert isinstance(translations, dict)
        assert "cli" in translations
        assert "terminal" in translations

    def test_idioma_inexistente_faz_fallback(self):
        with pytest.warns(UserWarning, match="não encontrado"):
            translations = load_translations("fr")

        # Deve retornar as traduções de pt-br como fallback
        assert isinstance(translations, dict)
        assert "cli" in translations


class TestSetAndGetLanguage:
    """Testes para funções set_language e get_language."""

    def test_idioma_padrao_pt_br(self):
        assert get_language() == "pt-br"

    def test_define_idioma_en(self):
        set_language("en")

        assert get_language() == "en"

    def test_define_idioma_pt_br(self):
        set_language("en")  # Primeiro muda
        set_language("pt-br")  # Depois volta

        assert get_language() == "pt-br"

    def test_idioma_invalido_faz_fallback(self):
        with pytest.warns(UserWarning, match="não disponível"):
            set_language("invalid-lang")

        assert get_language() == "pt-br"


class TestTranslateFunction:
    """Testes para função t()."""

    def test_traducao_simples_pt_br(self):
        set_language("pt-br")

        result = t("cli.getting_diff")

        assert result == "Obtendo diff..."

    def test_traducao_simples_en(self):
        set_language("en")

        result = t("cli.getting_diff")

        assert result == "Getting diff..."

    def test_traducao_com_interpolacao(self):
        set_language("pt-br")

        result = t("cli.analyzing", branch="feature/x", base="main")

        assert "feature/x" in result
        assert "main" in result

    def test_chave_inexistente_retorna_chave(self):
        result = t("chave.inexistente")

        assert result == "chave.inexistente"

    def test_fallback_para_pt_br(self):
        # Se uma chave existir só em pt-br, deve fazer fallback
        set_language("en")

        # A função t() deve funcionar mesmo que a chave não exista em en
        result = t("cli.getting_diff")
        assert result  # Deve retornar algo, não vazio


class TestTranslationKeysSync:
    """Testes para verificar que todas as chaves existem nos dois idiomas."""

    def test_cli_keys_sync(self):
        pt_br = load_translations("pt-br")
        en = load_translations("en")

        pt_br_keys = set(pt_br.get("cli", {}).keys())
        en_keys = set(en.get("cli", {}).keys())

        assert pt_br_keys == en_keys, f"Chaves cli diferentes: {pt_br_keys ^ en_keys}"

    def test_terminal_keys_sync(self):
        pt_br = load_translations("pt-br")
        en = load_translations("en")

        pt_br_keys = set(pt_br.get("terminal", {}).keys())
        en_keys = set(en.get("terminal", {}).keys())

        assert pt_br_keys == en_keys, f"Chaves terminal diferentes: {pt_br_keys ^ en_keys}"

    def test_progress_keys_sync(self):
        pt_br = load_translations("pt-br")
        en = load_translations("en")

        pt_br_keys = set(pt_br.get("progress", {}).keys())
        en_keys = set(en.get("progress", {}).keys())

        assert pt_br_keys == en_keys, f"Chaves progress diferentes: {pt_br_keys ^ en_keys}"

    def test_parser_keys_sync(self):
        pt_br = load_translations("pt-br")
        en = load_translations("en")

        pt_br_keys = set(pt_br.get("parser", {}).keys())
        en_keys = set(en.get("parser", {}).keys())

        assert pt_br_keys == en_keys, f"Chaves parser diferentes: {pt_br_keys ^ en_keys}"


class TestCacheMemory:
    """Testes para cache em memória."""

    def test_cache_funciona(self):
        # Primeira chamada carrega do disco
        translations1 = load_translations("pt-br")

        # Segunda chamada deve vir do cache
        translations2 = load_translations("pt-br")

        assert translations1 is translations2  # Mesmo objeto na memória

    def test_clear_cache_funciona(self):
        translations1 = load_translations("pt-br")

        clear_cache()

        translations2 = load_translations("pt-br")

        # Após limpar cache, deve ser objeto diferente
        assert translations1 is not translations2
