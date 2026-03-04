"""Testes para o módulo de identidade anônima."""

import uuid
from unittest.mock import MagicMock, patch

import pytest

from code_reviewer.analytics.identity import get_anonymous_id


class TestGetAnonymousId:
    """Testes para geração e persistência do UUID anônimo."""

    def test_primeira_execucao_gera_uuid(self, tmp_path):
        """Na primeira execução, gera UUID v4 e salva no arquivo."""
        id_file = tmp_path / "anonymous_id"

        with patch("code_reviewer.analytics.identity.ID_FILE", id_file), \
             patch("code_reviewer.analytics.identity.CACHE_DIR", tmp_path):
            result = get_anonymous_id()

        assert result is not None
        uuid.UUID(result, version=4)  # Valida formato
        assert id_file.read_text().strip() == result

    def test_reutiliza_uuid_existente(self, tmp_path):
        """Execuções subsequentes reutilizam o UUID salvo."""
        id_file = tmp_path / "anonymous_id"
        existing_id = str(uuid.uuid4())
        id_file.write_text(existing_id)

        with patch("code_reviewer.analytics.identity.ID_FILE", id_file), \
             patch("code_reviewer.analytics.identity.CACHE_DIR", tmp_path):
            result = get_anonymous_id()

        assert result == existing_id

    def test_arquivo_corrompido_regenera_uuid(self, tmp_path):
        """Arquivo com conteúdo inválido gera novo UUID."""
        id_file = tmp_path / "anonymous_id"
        id_file.write_text("conteudo-invalido-nao-uuid")

        with patch("code_reviewer.analytics.identity.ID_FILE", id_file), \
             patch("code_reviewer.analytics.identity.CACHE_DIR", tmp_path):
            result = get_anonymous_id()

        assert result is not None
        uuid.UUID(result, version=4)
        assert result != "conteudo-invalido-nao-uuid"

    def test_diretorio_nao_gravavel_retorna_none(self, tmp_path):
        """Se o diretório não é gravável, retorna None."""
        mock_id_file = MagicMock()
        mock_id_file.exists.return_value = False

        mock_cache_dir = MagicMock()
        mock_cache_dir.mkdir.side_effect = OSError("Permissão negada")

        with patch("code_reviewer.analytics.identity.ID_FILE", mock_id_file), \
             patch("code_reviewer.analytics.identity.CACHE_DIR", mock_cache_dir):
            result = get_anonymous_id()

        assert result is None

    def test_diretorio_nao_gravavel_simples(self):
        """Se ocorre OSError ao acessar o arquivo, retorna None."""
        with patch("code_reviewer.analytics.identity.ID_FILE") as mock_file:
            mock_file.exists.side_effect = OSError("Erro de I/O")
            result = get_anonymous_id()

        assert result is None

    def test_uuid_gerado_e_valido_v4(self, tmp_path):
        """O UUID gerado é especificamente versão 4."""
        id_file = tmp_path / "anonymous_id"

        with patch("code_reviewer.analytics.identity.ID_FILE", id_file), \
             patch("code_reviewer.analytics.identity.CACHE_DIR", tmp_path):
            result = get_anonymous_id()

        parsed = uuid.UUID(result)
        assert parsed.version == 4
