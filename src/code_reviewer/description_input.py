"""Description Input - Captura de descrição das alterações."""

import select
import sys

from prompt_toolkit import prompt as pt_prompt
from prompt_toolkit.key_binding import KeyBindings

# Limite máximo de caracteres para a descrição
MAX_DESCRIPTION_LENGTH = 2000


def read_from_stdin() -> str | None:
    """Lê descrição de stdin (para uso com pipe ou redirecionamento).

    Returns:
        Conteúdo de stdin ou None se stdin estiver vazio
    """
    # Verifica se há dados disponíveis em stdin sem bloquear
    if not sys.stdin.isatty():
        # Stdin não é TTY, pode ter dados via pipe
        if select.select([sys.stdin], [], [], 0.0)[0]:
            content = sys.stdin.read()
            return content.strip() if content.strip() else None
    return None


def is_interactive_mode(no_interactive: bool, json_output: bool) -> bool:
    """Verifica se deve usar modo interativo.

    Args:
        no_interactive: Flag --no-interactive foi passada
        json_output: Flag --json-output foi passada

    Returns:
        True se deve perguntar interativamente
    """
    if no_interactive:
        return False
    if json_output:
        return False
    if not sys.stdout.isatty():
        return False
    if not sys.stdin.isatty():
        return False
    return True


def _create_key_bindings() -> KeyBindings:
    """Cria key bindings customizados para o prompt interativo.

    Comportamento:
    - Enter: envia o texto (ou insere nova linha se último char é backslash)
    - Shift+Enter / Alt+Enter: insere nova linha
    - Esc: cancela e retorna None

    Returns:
        KeyBindings configurados
    """
    bindings = KeyBindings()

    @bindings.add("enter")
    def _handle_enter(event):
        """Enter envia o texto. Se termina com \\, remove e insere nova linha."""
        buf = event.current_buffer
        text_before = buf.document.text_before_cursor

        if text_before.endswith("\\"):
            # Remove o backslash e insere nova linha
            buf.delete_before_cursor(count=1)
            buf.insert_text("\n")
        else:
            # Envia o texto
            buf.validate_and_handle()

    @bindings.add("escape", "enter")
    def _handle_shift_enter(event):
        """Shift+Enter / Alt+Enter insere nova linha."""
        event.current_buffer.insert_text("\n")

    @bindings.add("escape", eager=False)
    def _handle_escape(event):
        """Esc cancela o prompt e retorna None."""
        event.app.exit(result=None)

    return bindings


def ask_description_interactive() -> str | None:
    """Pergunta descrição ao usuário de forma interativa.

    Usa prompt_toolkit com key bindings customizados:
    - Enter envia o texto
    - Shift+Enter ou backslash+Enter insere nova linha
    - Esc cancela e segue sem descrição
    - Texto colado via Ctrl+V preserva quebras de linha

    Returns:
        Descrição digitada/colada ou None se usuário pulou
    """
    bindings = _create_key_bindings()

    print("📝 Descrição das alterações (cole o texto do MR):")
    print("   Enter envia · Shift+Enter ou \\ para nova linha · Esc para pular\n")

    text = pt_prompt(
        "> ",
        multiline=True,
        key_bindings=bindings,
    )

    if text is None:
        return None

    return text.strip() if text.strip() else None


def truncate_description(description: str, reporter=None) -> str:
    """Trunca descrição se exceder o limite.

    Args:
        description: Descrição original
        reporter: ProgressReporter opcional para exibir aviso

    Returns:
        Descrição truncada se necessário
    """
    if len(description) <= MAX_DESCRIPTION_LENGTH:
        return description

    truncated = description[:MAX_DESCRIPTION_LENGTH]

    if reporter:
        reporter.warning(
            f"Descrição truncada de {len(description)} para {MAX_DESCRIPTION_LENGTH} caracteres"
        )

    return truncated


def get_description(
    description_flag: str | None,
    no_interactive: bool,
    json_output: bool,
    reporter=None,
) -> str | None:
    """Obtém a descrição das alterações.

    Ordem de prioridade:
    1. Flag --description com valor direto
    2. Flag --description com "-" (ler de stdin)
    3. Prompt interativo (se modo interativo ativo)

    Args:
        description_flag: Valor da flag --description ou None
        no_interactive: Flag --no-interactive foi passada
        json_output: Flag --json-output foi passada
        reporter: ProgressReporter opcional para exibir mensagens

    Returns:
        Descrição das alterações ou None se não fornecida
    """
    description = None

    # Caso 1: Flag com valor direto
    if description_flag and description_flag != "-":
        description = description_flag

    # Caso 2: Flag com "-" (ler de stdin)
    elif description_flag == "-":
        description = read_from_stdin()

    # Caso 3: Modo interativo
    elif is_interactive_mode(no_interactive, json_output):
        description = ask_description_interactive()

    # Aplica truncamento se necessário
    if description:
        description = truncate_description(description, reporter)

    return description
