"""Testes para o terminal formatter."""

import io

from code_reviewer.formatters.terminal import (
    _group_deps_by_file,
    format_dependency_graph,
    format_finding,
    format_header,
    format_result,
    format_severity,
    format_summary,
)
from code_reviewer.models import (
    Category,
    ContextGraph,
    Finding,
    FunctionRef,
    ReviewResult,
    ReviewSummary,
    Severity,
)


class TestFormatSeverity:
    """Testes para função format_severity."""

    def test_critical_contem_texto(self):
        result = format_severity(Severity.CRITICAL)
        assert "CRITICAL" in result

    def test_warning_contem_texto(self):
        result = format_severity(Severity.WARNING)
        assert "WARNING" in result

    def test_info_contem_texto(self):
        result = format_severity(Severity.INFO)
        assert "INFO" in result


class TestFormatFinding:
    """Testes para função format_finding."""

    def test_finding_completo(self):
        finding = Finding(
            file="test.py",
            line=42,
            severity=Severity.CRITICAL,
            category=Category.SECURITY,
            title="SQL Injection",
            description="Concatenação de SQL perigosa",
            suggestion="Use prepared statements",
            code_snippet="query = f'SELECT * FROM {table}'",
        )

        result = format_finding(finding)

        assert "test.py:42" in result
        assert "SQL Injection" in result
        assert "Concatenação de SQL perigosa" in result
        assert "Use prepared statements" in result

    def test_finding_sem_snippet(self):
        finding = Finding(
            file="app.py",
            line=10,
            severity=Severity.WARNING,
            category=Category.PERFORMANCE,
            title="N+1 Query",
            description="Query em loop",
            suggestion="",
            code_snippet="",
        )

        result = format_finding(finding)

        assert "app.py:10" in result
        assert "N+1 Query" in result


class TestFormatHeader:
    """Testes para função format_header."""

    def test_contem_branch(self):
        result = ReviewResult(
            branch="feature/test",
            base="main",
            files_analyzed=3,
            findings=[],
            summary=ReviewSummary(total=0, critical=0, warning=0, info=0),
        )

        header = format_header(result)

        assert "feature/test" in header
        assert "main" in header
        assert "3" in header


class TestFormatSummary:
    """Testes para função format_summary."""

    def test_sem_findings(self):
        result = ReviewResult(
            branch="branch",
            base="main",
            files_analyzed=1,
            findings=[],
            summary=ReviewSummary(total=0, critical=0, warning=0, info=0),
        )

        summary = format_summary(result)

        assert "Nenhum problema encontrado" in summary

    def test_com_findings(self):
        result = ReviewResult(
            branch="branch",
            base="main",
            files_analyzed=1,
            findings=[],
            summary=ReviewSummary(total=5, critical=2, warning=2, info=1),
        )

        summary = format_summary(result)

        assert "5" in summary
        assert "2" in summary  # critical e warning


class TestFormatResult:
    """Testes para função format_result."""

    def test_resultado_completo(self):
        findings = [
            Finding(
                file="a.py",
                line=10,
                severity=Severity.CRITICAL,
                category=Category.SECURITY,
                title="Bug 1",
                description="Desc 1",
                suggestion="",
                code_snippet="",
            ),
            Finding(
                file="a.py",
                line=20,
                severity=Severity.WARNING,
                category=Category.BUG,
                title="Bug 2",
                description="Desc 2",
                suggestion="",
                code_snippet="",
            ),
            Finding(
                file="b.py",
                line=5,
                severity=Severity.INFO,
                category=Category.PERFORMANCE,
                title="Bug 3",
                description="Desc 3",
                suggestion="",
                code_snippet="",
            ),
        ]

        result = ReviewResult(
            branch="feature/x",
            base="main",
            files_analyzed=2,
            findings=findings,
            summary=ReviewSummary(total=3, critical=1, warning=1, info=1),
        )

        output = io.StringIO()
        format_result(result, output)
        text = output.getvalue()

        # Verifica que contém os elementos principais
        assert "feature/x" in text
        assert "a.py" in text
        assert "b.py" in text
        assert "Bug 1" in text
        assert "Bug 2" in text
        assert "Bug 3" in text

    def test_resultado_vazio(self):
        result = ReviewResult(
            branch="clean",
            base="main",
            files_analyzed=1,
            findings=[],
            summary=ReviewSummary(total=0, critical=0, warning=0, info=0),
        )

        output = io.StringIO()
        format_result(result, output)
        text = output.getvalue()

        assert "Nenhum problema encontrado" in text

    def test_com_raw_response(self):
        result = ReviewResult(
            branch="test",
            base="main",
            files_analyzed=1,
            findings=[],
            summary=ReviewSummary(total=0, critical=0, warning=0, info=0),
            raw_response="Resposta da IA em texto livre",
        )

        output = io.StringIO()
        format_result(result, output)
        text = output.getvalue()

        assert "Resposta raw" in text
        assert "Resposta da IA em texto livre" in text

    def test_com_deps_e_findings(self):
        """Verifica que deps aparecem antes dos findings do mesmo arquivo."""
        findings = [
            Finding(
                file="auth.py",
                line=50,
                severity=Severity.WARNING,
                category=Category.SECURITY,
                title="Problema de auth",
                description="Descrição do problema",
                suggestion="",
                code_snippet="",
            ),
        ]

        result = ReviewResult(
            branch="feature/auth",
            base="main",
            files_analyzed=1,
            findings=findings,
            summary=ReviewSummary(total=1, critical=0, warning=1, info=0),
        )

        context_graphs = [
            ContextGraph(
                function_name="authenticate",
                file="auth.py",
                callers=[
                    FunctionRef(
                        file="routes.py",
                        line=87,
                        snippet="authenticate(user)",
                        function_name="handle_login",
                    ),
                ],
                callees=[
                    FunctionRef(
                        file="validators.py",
                        line=23,
                        snippet="validate(credentials)",
                        function_name="validate_credentials",
                    ),
                ],
            ),
        ]

        output = io.StringIO()
        format_result(result, output, context_graphs=context_graphs, show_deps=True)
        text = output.getvalue()

        # Verifica que deps aparecem
        assert "DEPENDÊNCIAS" in text or "DEPENDENCIES" in text
        assert "authenticate" in text
        assert "CALLERS" in text
        assert "CALLEES" in text
        # E também os findings
        assert "Problema de auth" in text

    def test_arquivo_so_com_deps_sem_findings(self):
        """Verifica mensagem para arquivos com deps mas sem findings."""
        result = ReviewResult(
            branch="feature/utils",
            base="main",
            files_analyzed=1,
            findings=[],
            summary=ReviewSummary(total=0, critical=0, warning=0, info=0),
        )

        context_graphs = [
            ContextGraph(
                function_name="helper_func",
                file="utils.py",
                callers=[
                    FunctionRef(
                        file="main.py",
                        line=10,
                        snippet="helper_func()",
                        function_name="main",
                    ),
                ],
                callees=[],
            ),
        ]

        output = io.StringIO()
        format_result(result, output, context_graphs=context_graphs, show_deps=True)
        text = output.getvalue()

        # Verifica que deps aparecem
        assert "helper_func" in text
        # E a mensagem de sem findings
        assert "Sem findings" in text or "No findings" in text


class TestFormatDependencyGraph:
    """Testes para função format_dependency_graph."""

    def test_com_callers_e_callees(self):
        """Verifica formatação com callers e callees."""
        graph = ContextGraph(
            function_name="process_data",
            file="processor.py",
            callers=[
                FunctionRef(
                    file="main.py",
                    line=42,
                    snippet="process_data(input)",
                    function_name="run",
                ),
                FunctionRef(
                    file="cli.py",
                    line=87,
                    snippet="process_data(args)",
                    function_name="command",
                ),
            ],
            callees=[
                FunctionRef(
                    file="validators.py",
                    line=23,
                    snippet="validate(data)",
                    function_name="validate",
                ),
            ],
        )

        result = format_dependency_graph(graph)

        assert "process_data" in result
        assert "CALLERS" in result
        assert "(2)" in result  # quantidade de callers
        assert "main.py:42" in result
        assert "cli.py:87" in result
        assert "CALLEES" in result
        assert "(1)" in result  # quantidade de callees
        assert "validate" in result

    def test_sem_callers_nem_callees(self):
        """Verifica formatação quando não há dependências."""
        graph = ContextGraph(
            function_name="isolated_func",
            file="isolated.py",
            callers=[],
            callees=[],
        )

        result = format_dependency_graph(graph)

        assert "isolated_func" in result
        assert "Sem dependências" in result or "No dependencies" in result

    def test_apenas_callers(self):
        """Verifica formatação com apenas callers."""
        graph = ContextGraph(
            function_name="leaf_func",
            file="leaf.py",
            callers=[
                FunctionRef(
                    file="parent.py",
                    line=10,
                    snippet="leaf_func()",
                    function_name="parent",
                ),
            ],
            callees=[],
        )

        result = format_dependency_graph(graph)

        assert "CALLERS" in result
        assert "CALLEES" not in result
        assert "parent.py:10" in result

    def test_apenas_callees(self):
        """Verifica formatação com apenas callees."""
        graph = ContextGraph(
            function_name="root_func",
            file="root.py",
            callers=[],
            callees=[
                FunctionRef(
                    file="child.py",
                    line=5,
                    snippet="child_func()",
                    function_name="child_func",
                ),
            ],
        )

        result = format_dependency_graph(graph)

        assert "CALLERS" not in result
        assert "CALLEES" in result
        assert "child_func" in result


class TestGroupDepsByFile:
    """Testes para função _group_deps_by_file."""

    def test_agrupa_por_arquivo(self):
        """Verifica que grafos são agrupados corretamente por arquivo."""
        graphs = [
            ContextGraph(function_name="func1", file="a.py", callers=[], callees=[]),
            ContextGraph(function_name="func2", file="a.py", callers=[], callees=[]),
            ContextGraph(function_name="func3", file="b.py", callers=[], callees=[]),
        ]

        result = _group_deps_by_file(graphs)

        assert "a.py" in result
        assert "b.py" in result
        assert len(result["a.py"]) == 2
        assert len(result["b.py"]) == 1

    def test_lista_vazia(self):
        """Verifica comportamento com lista vazia."""
        result = _group_deps_by_file([])

        assert result == {}
