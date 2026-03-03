"""Testes para o módulo description_input."""

from unittest.mock import MagicMock, patch

import pytest
from prompt_toolkit.keys import Keys

from code_reviewer.description_input import (
    MAX_DESCRIPTION_LENGTH,
    _create_key_bindings,
    ask_description_interactive,
    get_description,
    is_interactive_mode,
    read_from_stdin,
    truncate_description,
)


class TestReadFromStdin:
    """Testes para função read_from_stdin."""

    def test_stdin_vazio_retorna_none(self):
        """Verifica que stdin vazio retorna None."""
        with patch("code_reviewer.description_input.sys.stdin") as mock_stdin:
            mock_stdin.isatty.return_value = True
            result = read_from_stdin()
            assert result is None

    def test_stdin_com_conteudo(self):
        """Verifica que stdin com conteúdo é lido corretamente."""
        with (
            patch("code_reviewer.description_input.sys.stdin") as mock_stdin,
            patch("code_reviewer.description_input.select.select") as mock_select,
        ):
            mock_stdin.isatty.return_value = False
            mock_stdin.read.return_value = "Descrição do PR\n"
            mock_select.return_value = ([mock_stdin], [], [])

            result = read_from_stdin()

            assert result == "Descrição do PR"

    def test_stdin_apenas_whitespace_retorna_none(self):
        """Verifica que stdin com apenas espaços retorna None."""
        with (
            patch("code_reviewer.description_input.sys.stdin") as mock_stdin,
            patch("code_reviewer.description_input.select.select") as mock_select,
        ):
            mock_stdin.isatty.return_value = False
            mock_stdin.read.return_value = "   \n\n   "
            mock_select.return_value = ([mock_stdin], [], [])

            result = read_from_stdin()

            assert result is None


class TestIsInteractiveMode:
    """Testes para função is_interactive_mode."""

    def test_no_interactive_desabilita(self):
        """Verifica que --no-interactive desabilita modo interativo."""
        result = is_interactive_mode(no_interactive=True, json_output=False)
        assert result is False

    def test_json_output_desabilita(self):
        """Verifica que --json-output desabilita modo interativo."""
        result = is_interactive_mode(no_interactive=False, json_output=True)
        assert result is False

    def test_sem_tty_stdout_desabilita(self):
        """Verifica que sem TTY no stdout desabilita modo interativo."""
        with patch("code_reviewer.description_input.sys.stdout") as mock_stdout:
            mock_stdout.isatty.return_value = False
            result = is_interactive_mode(no_interactive=False, json_output=False)
            assert result is False

    def test_sem_tty_stdin_desabilita(self):
        """Verifica que sem TTY no stdin desabilita modo interativo."""
        with (
            patch("code_reviewer.description_input.sys.stdout") as mock_stdout,
            patch("code_reviewer.description_input.sys.stdin") as mock_stdin,
        ):
            mock_stdout.isatty.return_value = True
            mock_stdin.isatty.return_value = False
            result = is_interactive_mode(no_interactive=False, json_output=False)
            assert result is False

    def test_modo_interativo_ativo(self):
        """Verifica que modo interativo é ativado quando condições são atendidas."""
        with (
            patch("code_reviewer.description_input.sys.stdout") as mock_stdout,
            patch("code_reviewer.description_input.sys.stdin") as mock_stdin,
        ):
            mock_stdout.isatty.return_value = True
            mock_stdin.isatty.return_value = True
            result = is_interactive_mode(no_interactive=False, json_output=False)
            assert result is True


class TestTruncateDescription:
    """Testes para função truncate_description."""

    def test_descricao_dentro_do_limite(self):
        """Verifica que descrição dentro do limite não é truncada."""
        description = "Descrição curta"
        result = truncate_description(description)
        assert result == description

    def test_descricao_excede_limite(self):
        """Verifica que descrição longa é truncada."""
        description = "x" * (MAX_DESCRIPTION_LENGTH + 500)
        result = truncate_description(description)
        assert len(result) == MAX_DESCRIPTION_LENGTH

    def test_truncamento_exibe_aviso(self):
        """Verifica que truncamento exibe aviso via reporter."""
        description = "x" * (MAX_DESCRIPTION_LENGTH + 100)
        reporter = MagicMock()

        truncate_description(description, reporter)

        reporter.warning.assert_called_once()
        assert "truncada" in reporter.warning.call_args[0][0].lower()


class TestCreateKeyBindings:
    """Testes para os key bindings customizados do prompt interativo."""

    def _make_event(self, text_before_cursor="", full_text=""):
        """Cria um mock de KeyPressEvent para testes de key bindings."""
        event = MagicMock()
        buf = MagicMock()
        doc = MagicMock()
        doc.text_before_cursor = text_before_cursor
        buf.document = doc
        buf.text = full_text
        event.current_buffer = buf
        event.app = MagicMock()
        return event

    def _find_handler(self, bindings, *keys):
        """Encontra handler pelo nome das keys no prompt_toolkit."""
        target = tuple(keys)
        for b in bindings.bindings:
            if b.keys == target:
                return b.handler
        return None

    def test_enter_envia_texto(self):
        """Verifica que Enter envia o texto (validate_and_handle)."""
        bindings = _create_key_bindings()
        event = self._make_event(text_before_cursor="Descrição do MR")

        handler = self._find_handler(bindings, Keys.ControlM)
        assert handler is not None
        handler(event)

        event.current_buffer.validate_and_handle.assert_called_once()

    def test_enter_com_texto_vazio_envia(self):
        """Verifica que Enter com texto vazio envia (retorna string vazia)."""
        bindings = _create_key_bindings()
        event = self._make_event(text_before_cursor="")

        handler = self._find_handler(bindings, Keys.ControlM)
        handler(event)

        event.current_buffer.validate_and_handle.assert_called_once()

    def test_backslash_enter_insere_nova_linha(self):
        """Verifica que \\+Enter remove o \\ e insere nova linha."""
        bindings = _create_key_bindings()
        event = self._make_event(text_before_cursor="Linha 1\\")

        handler = self._find_handler(bindings, Keys.ControlM)
        handler(event)

        # Deve remover o backslash e inserir nova linha
        event.current_buffer.delete_before_cursor.assert_called_once_with(count=1)
        event.current_buffer.insert_text.assert_called_once_with("\n")
        # Não deve enviar
        event.current_buffer.validate_and_handle.assert_not_called()

    def test_shift_enter_insere_nova_linha(self):
        """Verifica que Shift+Enter (escape+enter) insere nova linha."""
        bindings = _create_key_bindings()
        event = self._make_event(text_before_cursor="Texto existente")

        handler = self._find_handler(bindings, Keys.Escape, Keys.ControlM)
        assert handler is not None
        handler(event)

        event.current_buffer.insert_text.assert_called_once_with("\n")

    def test_esc_cancela_retornando_none(self):
        """Verifica que Esc cancela o prompt retornando None."""
        bindings = _create_key_bindings()
        event = self._make_event()

        handler = self._find_handler(bindings, Keys.Escape)
        assert handler is not None
        handler(event)

        event.app.exit.assert_called_once_with(result=None)


class TestAskDescriptionInteractive:
    """Testes para função ask_description_interactive."""

    def test_texto_colado_preserva_quebras_de_linha(self):
        """Verifica que texto colado via Ctrl+V preserva quebras de linha."""
        texto_colado = "Linha 1\nLinha 2\nLinha 3"
        with patch(
            "code_reviewer.description_input.pt_prompt", return_value=texto_colado
        ):
            result = ask_description_interactive()

        assert result == texto_colado

    def test_esc_retorna_none(self):
        """Verifica que Esc (prompt retorna None) resulta em None."""
        with patch(
            "code_reviewer.description_input.pt_prompt", return_value=None
        ):
            result = ask_description_interactive()

        assert result is None

    def test_texto_vazio_retorna_none(self):
        """Verifica que texto vazio ou só whitespace retorna None."""
        with patch(
            "code_reviewer.description_input.pt_prompt", return_value="   \n  "
        ):
            result = ask_description_interactive()

        assert result is None

    def test_texto_com_strip(self):
        """Verifica que texto é stripped antes de retornar."""
        with patch(
            "code_reviewer.description_input.pt_prompt",
            return_value="  Descrição  \n",
        ):
            result = ask_description_interactive()

        assert result == "Descrição"


class TestGetDescription:
    """Testes para função get_description."""

    def test_flag_direta_tem_prioridade(self):
        """Verifica que flag --description tem prioridade."""
        result = get_description(
            description_flag="Descrição via flag",
            no_interactive=False,
            json_output=False,
        )
        assert result == "Descrição via flag"

    def test_flag_stdin_le_de_stdin(self):
        """Verifica que -d - lê de stdin."""
        with (
            patch("code_reviewer.description_input.sys.stdin") as mock_stdin,
            patch("code_reviewer.description_input.select.select") as mock_select,
        ):
            mock_stdin.isatty.return_value = False
            mock_stdin.read.return_value = "Descrição de stdin\n"
            mock_select.return_value = ([mock_stdin], [], [])

            result = get_description(
                description_flag="-",
                no_interactive=False,
                json_output=False,
            )

            assert result == "Descrição de stdin"

    def test_sem_flag_e_nao_interativo_retorna_none(self):
        """Verifica que sem flag e modo não-interativo retorna None."""
        result = get_description(
            description_flag=None,
            no_interactive=True,
            json_output=False,
        )
        assert result is None

    def test_descricao_truncada_automaticamente(self):
        """Verifica que descrição longa é truncada automaticamente."""
        long_description = "x" * (MAX_DESCRIPTION_LENGTH + 100)
        result = get_description(
            description_flag=long_description,
            no_interactive=False,
            json_output=False,
        )
        assert len(result) == MAX_DESCRIPTION_LENGTH
