"""Testes para o client PostHog."""

from unittest.mock import MagicMock, patch

import pytest

from code_reviewer.analytics import client


@pytest.fixture(autouse=True)
def reset_client_state():
    """Reseta o estado do client entre testes."""
    client._initialized = False
    client._posthog = None
    yield
    client._initialized = False
    client._posthog = None


class TestLazyInit:
    """Testes para inicialização lazy do SDK."""

    def test_sdk_nao_inicializado_antes_da_primeira_chamada(self):
        """O SDK não é importado até a primeira chamada a capture()."""
        assert client._initialized is False
        assert client._posthog is None

    def test_sdk_inicializado_na_primeira_capture(self):
        """O SDK é inicializado na primeira chamada a capture()."""
        mock_posthog = MagicMock()
        with patch.dict("sys.modules", {"posthog": mock_posthog}):
            client.capture("test-id", "test_event")

        assert client._initialized is True

    def test_sdk_inicializado_apenas_uma_vez(self):
        """Chamadas subsequentes reutilizam o SDK já inicializado."""
        mock_posthog = MagicMock()
        with patch.dict("sys.modules", {"posthog": mock_posthog}):
            client.capture("test-id", "event_1")
            client.capture("test-id", "event_2")

        # project_api_key é setado apenas uma vez (na init)
        assert mock_posthog.project_api_key == client._API_KEY


class TestCapture:
    """Testes para envio de eventos."""

    def test_evento_capturado_com_propriedades(self):
        """Eventos são enviados com distinct_id, nome e propriedades."""
        mock_posthog = MagicMock()
        with patch.dict("sys.modules", {"posthog": mock_posthog}):
            client.capture("uid-123", "review_started", {"runner": "gemini"})

        mock_posthog.capture.assert_called_once_with(
            "uid-123", "review_started", {"runner": "gemini"}
        )

    def test_falha_silenciosa_em_erro_de_rede(self):
        """Erro no capture não propaga exceção."""
        mock_posthog = MagicMock()
        mock_posthog.capture.side_effect = Exception("Erro de rede")

        with patch.dict("sys.modules", {"posthog": mock_posthog}):
            # Não deve lançar exceção
            client.capture("uid-123", "review_started")

    def test_falha_silenciosa_se_sdk_nao_importavel(self):
        """Se o SDK não pode ser importado, falha silenciosa."""
        with patch.dict("sys.modules", {"posthog": None}):
            with patch("builtins.__import__", side_effect=ImportError):
                client.capture("uid-123", "test_event")

        # Não deve lançar exceção


class TestFlush:
    """Testes para flush com timeout."""

    def test_flush_executa_em_thread_com_timeout(self):
        """O flush é executado em thread separada com timeout."""
        mock_posthog = MagicMock()
        client._posthog = mock_posthog
        client._initialized = True

        client._flush_with_timeout(timeout=1.0)

        mock_posthog.flush.assert_called_once()

    def test_flush_ignora_quando_nao_inicializado(self):
        """Se o SDK não foi inicializado, flush é no-op."""
        client._posthog = None
        client._flush_with_timeout()  # Não deve lançar exceção

    def test_flush_falha_silenciosa(self):
        """Erro no flush não propaga exceção."""
        mock_posthog = MagicMock()
        mock_posthog.flush.side_effect = Exception("Timeout")
        client._posthog = mock_posthog
        client._initialized = True

        # Não deve lançar exceção
        client._flush_with_timeout(timeout=1.0)

    def test_shutdown_chama_flush(self):
        """shutdown() executa o flush com timeout."""
        mock_posthog = MagicMock()
        client._posthog = mock_posthog
        client._initialized = True

        client.shutdown()

        mock_posthog.flush.assert_called_once()
