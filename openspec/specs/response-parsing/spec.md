## ADDED Requirements

### Requirement: Parsear JSON da resposta da IA
O sistema SHALL tentar parsear a resposta da IA como JSON usando `json.loads()`.

#### Scenario: JSON válido retornado diretamente
- **WHEN** a IA retorna `{"review": {"findings": [...], "summary": {...}}}`
- **THEN** o parser converte para o modelo Pydantic `ReviewResult` com sucesso

#### Scenario: JSON dentro de bloco markdown
- **WHEN** a IA retorna o JSON envolvido em ` ```json ... ``` `
- **THEN** o parser extrai o conteúdo do bloco markdown e parseia o JSON

### Requirement: Fallback para respostas malformadas
O sistema SHALL implementar uma cadeia de fallbacks quando o JSON não é válido: (1) tentar extrair de bloco markdown, (2) tentar regex para encontrar `{...}`, (3) retornar como texto raw não estruturado.

#### Scenario: JSON parcialmente correto
- **WHEN** a resposta contém texto antes/depois do JSON mas o JSON em si é válido
- **THEN** o parser extrai o JSON via regex e parseia com sucesso

#### Scenario: Resposta completamente não-JSON
- **WHEN** a IA retorna texto livre sem nenhum JSON válido
- **THEN** o parser retorna um `ReviewResult` com um único finding do tipo INFO contendo o texto raw da resposta

### Requirement: Validar com modelos Pydantic
O sistema SHALL validar o JSON parseado contra modelos Pydantic: `ReviewResult` contendo `findings: list[Finding]` e `summary: ReviewSummary`.

#### Scenario: Todos os campos presentes
- **WHEN** o JSON contém todos os campos obrigatórios de cada Finding (file, line, severity, category, title, description, suggestion, code_snippet)
- **THEN** a validação passa e retorna o modelo tipado

#### Scenario: Campos opcionais ausentes
- **WHEN** um Finding não contém `code_snippet` ou `suggestion`
- **THEN** os campos ausentes recebem valor default (string vazia) e a validação passa

#### Scenario: Severidade inválida
- **WHEN** um Finding contém `severity: "HIGH"` em vez dos valores permitidos
- **THEN** o parser mapeia para o valor mais próximo (`WARNING`) ou usa `INFO` como fallback

### Requirement: Retornar resultado tipado
O sistema SHALL retornar um objeto `ReviewResult` tipado que pode ser serializado de volta para JSON e usado por formatters/integrações futuras.

#### Scenario: Serialização para JSON
- **WHEN** o `ReviewResult` é serializado com `.model_dump_json()`
- **THEN** o JSON resultante segue o schema definido e pode ser consumido por outros sistemas
