"""Runner para Gemini CLI."""

import subprocess
from pathlib import Path

from .base import RunnerNotFoundError, check_command_exists


class GeminiCLIRunner:
    """Runner que executa prompts via Gemini CLI.

    O Gemini CLI é a ferramenta oficial do Google para interagir
    com o Gemini a partir do terminal.

    Instalação: https://github.com/google-gemini/gemini-cli
    """

    @property
    def name(self) -> str:
        """Nome identificador do runner."""
        return "gemini"

    def check_availability(self) -> bool:
        """Verifica se o gemini CLI está disponível."""
        return check_command_exists("gemini")

    def run(self, prompt: str, workdir: Path) -> str:
        """Executa o prompt via Gemini CLI.

        Args:
            prompt: O prompt completo para enviar
            workdir: Diretório de trabalho

        Returns:
            Resposta do Gemini

        Raises:
            RunnerNotFoundError: Se gemini-cli não estiver instalado
            subprocess.CalledProcessError: Se a execução falhar
        """
        if not self.check_availability():
            raise RunnerNotFoundError(
                "gemini-cli não encontrado no PATH.\n"
                "Instale em: https://github.com/google-gemini/gemini-cli\n"
                "Ou configure outro runner com --runner <nome>"
            )

        # Executa o Gemini CLI passando o prompt via stdin
        # O flag -y aceita automaticamente (YOLO mode para CI)
        result = subprocess.run(
            [
                "gemini",
                "-y",  # Auto-accept / YOLO mode
            ],
            input=prompt,
            capture_output=True,
            text=True,
            cwd=workdir,
            timeout=300,  # 5 minutos de timeout
        )

        # Combina stdout e stderr (Gemini pode usar ambos)
        output = result.stdout
        if result.stderr:
            output += "\n" + result.stderr

        return output.strip()
