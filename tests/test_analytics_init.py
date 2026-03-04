"""Testes para a fachada do módulo analytics."""

import os
from unittest.mock import MagicMock, patch

import pytest

from code_reviewer.analytics import is_enabled, shutdown_analytics, track_event


class TestIsEnabled:
    """Testes para verificação de opt-out."""

    def test_habilitado_por_padrao(self):
        """Telemetria habilitada quando env var não está definida."""
        with patch.dict(os.environ, {}, clear=True):
            assert is_enabled() is True

    def test_desabilitado_com_env_var(self):
        """Telemetria desabilitada quando AIREV_NO_TELEMETRY=1."""
        with patch.dict(os.environ, {"AIREV_NO_TELEMETRY": "1"}):
            assert is_enabled() is False

    def test_habilitado_com_valor_diferente(self):
        """Telemetria habilitada se env var tem valor diferente de 1."""
        with patch.dict(os.environ, {"AIREV_NO_TELEMETRY": "0"}):
            assert is_enabled() is True

    def test_desabilitado_com_espaco(self):
        """Telemetria desabilitada mesmo com espaço ao redor do valor."""
        with patch.dict(os.environ, {"AIREV_NO_TELEMETRY": " 1 "}):
            assert is_enabled() is False


class TestTrackEvent:
    """Testes para captura de eventos."""

    def test_opt_out_nao_envia_evento(self):
        """Com opt-out, nenhum evento é enviado."""
        with patch.dict(os.environ, {"AIREV_NO_TELEMETRY": "1"}):
            with patch("code_reviewer.analytics.client.capture") as mock_capture:
                track_event("review_started", {"runner": "gemini"})
                mock_capture.assert_not_called()

    def test_sdk_nao_importado_quando_desabilitado(self):
        """Com opt-out, o módulo client nem é importado."""
        with patch.dict(os.environ, {"AIREV_NO_TELEMETRY": "1"}):
            with patch("builtins.__import__", wraps=__import__) as mock_import:
                track_event("review_started")
                # Verifica que posthog não foi importado
                posthog_calls = [
                    c for c in mock_import.call_args_list
                    if "posthog" in str(c) and "analytics" not in str(c)
                ]
                assert len(posthog_calls) == 0

    @patch("code_reviewer.analytics.identity.get_anonymous_id", return_value="uuid-123")
    @patch("code_reviewer.analytics.client.capture")
    def test_evento_capturado_corretamente(self, mock_capture, mock_id):
        """Eventos são capturados com distinct_id e propriedades corretas."""
        with patch.dict(os.environ, {}, clear=True):
            track_event("review_started", {"runner": "gemini"})

        mock_capture.assert_called_once_with(
            "uuid-123", "review_started", {"runner": "gemini"}
        )

    @patch("code_reviewer.analytics.identity.get_anonymous_id", return_value=None)
    @patch("code_reviewer.analytics.client.capture")
    def test_sem_id_nao_envia_evento(self, mock_capture, mock_id):
        """Se não conseguir obter ID anônimo, não envia evento."""
        with patch.dict(os.environ, {}, clear=True):
            track_event("review_started")

        mock_capture.assert_not_called()

    def test_falha_silenciosa_em_erro(self):
        """Exceções no track_event não propagam."""
        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "code_reviewer.analytics.identity.get_anonymous_id",
                side_effect=Exception("Erro inesperado"),
            ):
                # Não deve lançar exceção
                track_event("review_started")


class TestShutdownAnalytics:
    """Testes para encerramento do analytics."""

    @patch("code_reviewer.analytics.client.shutdown")
    def test_shutdown_chama_client(self, mock_shutdown):
        """shutdown_analytics() delega para client.shutdown()."""
        with patch.dict(os.environ, {}, clear=True):
            shutdown_analytics()

        mock_shutdown.assert_called_once()

    @patch("code_reviewer.analytics.client.shutdown")
    def test_shutdown_ignorado_com_opt_out(self, mock_shutdown):
        """Com opt-out, shutdown é no-op."""
        with patch.dict(os.environ, {"AIREV_NO_TELEMETRY": "1"}):
            shutdown_analytics()

        mock_shutdown.assert_not_called()
