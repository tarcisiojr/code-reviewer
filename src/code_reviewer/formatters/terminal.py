"""Terminal Formatter - Renderização colorida dos resultados."""

from collections import defaultdict
from typing import TextIO
import sys

from ..i18n import t
from ..models import Category, ContextGraph, Finding, ReviewResult, Severity


# Códigos ANSI para cores
class Colors:
    """Códigos de cores ANSI."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BG_RED = "\033[41m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


def _supports_color() -> bool:
    """Verifica se o terminal suporta cores."""
    # Desabilita cores se não for TTY
    if not hasattr(sys.stdout, "isatty"):
        return False
    if not sys.stdout.isatty():
        return False
    return True


def _colorize(text: str, *codes: str) -> str:
    """Aplica códigos de cor ao texto.

    Args:
        text: Texto a colorir
        codes: Códigos ANSI a aplicar

    Returns:
        Texto com códigos ANSI (ou texto puro se cores desabilitadas)
    """
    if not _supports_color():
        return text
    return "".join(codes) + text + Colors.RESET


def format_severity(severity: Severity) -> str:
    """Formata a severidade com cor.

    Args:
        severity: Severidade do finding

    Returns:
        String formatada com cor
    """
    if severity == Severity.CRITICAL:
        return _colorize(f"[{severity.value}]", Colors.BOLD, Colors.RED)
    elif severity == Severity.WARNING:
        return _colorize(f"[{severity.value}]", Colors.BOLD, Colors.YELLOW)
    else:
        return _colorize(f"[{severity.value}]", Colors.BOLD, Colors.BLUE)


def format_category_badge(category: Category) -> str:
    """Formata o badge da categoria.

    Args:
        category: Categoria do finding

    Returns:
        String formatada com ícone e cor para a categoria
    """
    # Ícones e cores por categoria
    category_styles = {
        Category.SECURITY: ("🔒", Colors.RED),
        Category.PERFORMANCE: ("⚡", Colors.YELLOW),
        Category.BUG: ("🐛", Colors.MAGENTA),
        Category.RESOURCE_LEAK: ("💧", Colors.CYAN),
        Category.TEXT_QUALITY: ("✏️", Colors.CYAN),
    }

    icon, color = category_styles.get(category, ("•", Colors.WHITE))
    return f"{icon} {_colorize(category.value, color)}"


def format_finding(finding: Finding) -> str:
    """Formata um finding para exibição.

    Args:
        finding: Finding a formatar

    Returns:
        String formatada multi-linha
    """
    lines = []

    # Header: [SEVERITY] arquivo:linha - Título
    severity_str = format_severity(finding.severity)
    category_badge = format_category_badge(finding.category)
    location = _colorize(f"{finding.file}:{finding.line}", Colors.CYAN)
    title = _colorize(finding.title, Colors.BOLD)

    lines.append(f"  {severity_str} {category_badge} {location} - {title}")

    # Descrição
    if finding.description:
        lines.append(f"  │ {finding.description}")

    # Code snippet
    if finding.code_snippet:
        snippet_lines = finding.code_snippet.strip().split("\n")
        for snippet_line in snippet_lines[:5]:  # Limita a 5 linhas
            lines.append(f"  │ {_colorize(snippet_line, Colors.DIM)}")

    # Sugestão
    if finding.suggestion:
        lines.append("  │")
        lines.append(f"  │ {_colorize(t('terminal.suggestion'), Colors.GREEN)} {finding.suggestion}")

    lines.append("")

    return "\n".join(lines)


def _group_deps_by_file(graphs: list[ContextGraph]) -> dict[str, list[ContextGraph]]:
    """Agrupa ContextGraphs por arquivo.

    Args:
        graphs: Lista de grafos de contexto

    Returns:
        Dicionário mapeando arquivo -> lista de grafos
    """
    deps_by_file: dict[str, list[ContextGraph]] = defaultdict(list)
    for graph in graphs:
        deps_by_file[graph.file].append(graph)
    return dict(deps_by_file)


def format_dependency_graph(graph: ContextGraph) -> str:
    """Formata um grafo de dependências em árvore ASCII.

    Args:
        graph: Grafo de contexto de uma função

    Returns:
        String formatada multi-linha com árvore de deps
    """
    lines = []

    # Header: 📊 DEPENDENCIES: function_name (linha N)
    header = _colorize(
        f"📊 {t('terminal.dependencies')}: {graph.function_name}",
        Colors.BOLD,
        Colors.CYAN,
    )
    lines.append(f"  {header}")
    lines.append("  │")

    has_callers = len(graph.callers) > 0
    has_callees = len(graph.callees) > 0

    # Se não tem callers nem callees
    if not has_callers and not has_callees:
        lines.append(f"  └── {_colorize(t('terminal.no_deps_found'), Colors.DIM)}")
        lines.append("")
        return "\n".join(lines)

    # Callers
    if has_callers:
        # Usa ├── se tem callees, └── se não tem
        branch = "├──" if has_callees else "└──"
        lines.append(f"  {branch} 📥 {_colorize(t('terminal.callers'), Colors.YELLOW)} ({len(graph.callers)})")

        for i, caller in enumerate(graph.callers):
            is_last = i == len(graph.callers) - 1
            # Conectores verticais dependem se tem callees depois
            prefix = "│   " if has_callees else "    "
            connector = "└──" if is_last else "├──"
            location = _colorize(f"{caller.file}:{caller.line}", Colors.DIM)
            snippet = caller.snippet.strip()[:50] if caller.snippet else ""
            lines.append(f"  {prefix}{connector} {location}     → {snippet}")

        if has_callees:
            lines.append("  │")

    # Callees
    if has_callees:
        lines.append(f"  └── 📤 {_colorize(t('terminal.callees'), Colors.GREEN)} ({len(graph.callees)})")

        for i, callee in enumerate(graph.callees):
            is_last = i == len(graph.callees) - 1
            connector = "└──" if is_last else "├──"
            func_name = callee.function_name or "?"
            location = _colorize(f"{callee.file}:{callee.line}", Colors.DIM)
            lines.append(f"      {connector} {func_name}     → {location}")

    lines.append("")
    return "\n".join(lines)


def format_file_header(file_path: str) -> str:
    """Formata o header de um arquivo.

    Args:
        file_path: Caminho do arquivo

    Returns:
        Header formatado
    """
    return _colorize(f"\n{file_path}", Colors.BOLD, Colors.MAGENTA)


def format_header(result: ReviewResult) -> str:
    """Formata o header da análise.

    Args:
        result: Resultado da análise

    Returns:
        Header formatado
    """
    line = "═" * 50
    files_text = t("terminal.files_count", count=result.files_analyzed)
    return f"""
{_colorize(line, Colors.DIM)}
{_colorize(f"  {t('terminal.code_review')}", Colors.BOLD)} — {_colorize(result.branch, Colors.CYAN)}
  {t('terminal.compared_with')} {_colorize(result.base, Colors.CYAN)}  │  {files_text}
{_colorize(line, Colors.DIM)}
"""


def format_summary(result: ReviewResult) -> str:
    """Formata o resumo da análise.

    Args:
        result: Resultado da análise

    Returns:
        Resumo formatado
    """
    line = "═" * 50

    if result.summary.total == 0:
        return f"""
{_colorize(line, Colors.DIM)}
  {_colorize(t('terminal.no_problems'), Colors.GREEN)}
{_colorize(line, Colors.DIM)}
"""

    critical = _colorize(str(result.summary.critical), Colors.RED) if result.summary.critical else "0"
    warning = _colorize(str(result.summary.warning), Colors.YELLOW) if result.summary.warning else "0"
    info = _colorize(str(result.summary.info), Colors.BLUE) if result.summary.info else "0"
    findings_text = t("terminal.findings_count", count=result.summary.total)

    return f"""
{_colorize(line, Colors.DIM)}
  {_colorize(t('terminal.summary'), Colors.BOLD)} {findings_text}
  {critical} critical, {warning} warning, {info} info
{_colorize(line, Colors.DIM)}
"""


def format_result(
    result: ReviewResult,
    output: TextIO = sys.stdout,
    context_graphs: list[ContextGraph] | None = None,
    show_deps: bool = False,
) -> None:
    """Formata e imprime o resultado completo.

    Args:
        result: Resultado da análise
        output: Stream de saída (default: stdout)
        context_graphs: Lista de grafos de contexto para deps (opcional)
        show_deps: Se True, exibe dependências antes dos findings
    """
    # Header
    output.write(format_header(result))

    # Agrupa findings por arquivo
    by_file: dict[str, list[Finding]] = defaultdict(list)
    for finding in result.findings:
        by_file[finding.file].append(finding)

    # Agrupa deps por arquivo se show_deps ativo
    deps_by_file: dict[str, list[ContextGraph]] = {}
    if show_deps and context_graphs:
        deps_by_file = _group_deps_by_file(context_graphs)

    # Coleta todos os arquivos (união de findings e deps)
    all_files = set(by_file.keys())
    if show_deps:
        all_files.update(deps_by_file.keys())

    # Imprime findings e deps agrupados por arquivo
    for file_path in sorted(all_files):
        output.write(format_file_header(file_path))
        output.write("\n")

        # Renderiza deps antes dos findings (se show_deps ativo)
        if show_deps and file_path in deps_by_file:
            for graph in deps_by_file[file_path]:
                output.write(format_dependency_graph(graph))

        # Renderiza findings
        findings = by_file.get(file_path, [])
        if findings:
            for finding in sorted(findings, key=lambda f: f.line):
                output.write(format_finding(finding))
        elif show_deps and file_path in deps_by_file:
            # Arquivo com deps mas sem findings
            output.write(f"  {t('terminal.no_findings_file')}\n\n")

    # Se tinha arquivos analisados mas sem findings e sem deps
    if result.files_analyzed > 0 and not result.findings and not deps_by_file:
        output.write("\n")

    # Resumo
    output.write(format_summary(result))

    # Raw response se houver
    if result.raw_response:
        output.write("\n")
        output.write(_colorize(t("terminal.raw_response"), Colors.DIM))
        output.write("\n")
        output.write(result.raw_response[:500])
        if len(result.raw_response) > 500:
            output.write("\n...")
        output.write("\n")
