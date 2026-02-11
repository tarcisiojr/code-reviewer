## MODIFIED Requirements

### Requirement: Incluir aviso anti-falso-positivo para análise de diff parcial
O sistema SHALL incluir no prompt uma instrução explícita alertando a LLM que o diff mostra apenas código parcial e que ela MUST consultar a seção "ARQUIVOS MODIFICADOS" antes de reportar erros de sintaxe ou código incompleto. O aviso SHALL incluir um exemplo visual de diff multiline para demonstrar o problema.

#### Scenario: Aviso presente no prompt
- **WHEN** o prompt é montado
- **THEN** o prompt contém instrução similar a: "IMPORTANTE: O diff mostra apenas as linhas alteradas. Código aparentemente incompleto (blocos abertos, imports parciais) pode estar completo no arquivo original. SEMPRE consulte a seção 'ARQUIVOS MODIFICADOS' antes de reportar erros de sintaxe ou código incompleto."

#### Scenario: Posicionamento do aviso
- **WHEN** o prompt é montado
- **THEN** o aviso é posicionado após a seção "REGRAS IMPORTANTES" e antes da seção "FOCO DA ANÁLISE"

#### Scenario: LLM não reporta falso positivo de sintaxe
- **WHEN** o diff mostra código parcial (ex: abertura de bloco sem fechamento visível)
- **AND** o arquivo completo na seção "ARQUIVOS MODIFICADOS" mostra código sintaticamente correto
- **THEN** a LLM não reporta erro de sintaxe para esse trecho

#### Scenario: Exemplo visual no aviso
- **WHEN** o prompt é montado
- **THEN** o aviso inclui exemplo mostrando diff parcial vs código completo, demonstrando que linhas sem `+`/`-` são contexto e não indicam erro

## ADDED Requirements

### Requirement: Instruir sobre linhas de contexto
O sistema SHALL incluir no prompt uma explicação de que linhas sem prefixo `+` ou `-` no diff são linhas de contexto adjacentes às mudanças, não código a ser analisado.

#### Scenario: Explicação de linhas de contexto presente
- **WHEN** o prompt é montado
- **THEN** o prompt contém instrução: "No DIFF, linhas sem prefixo (sem + ou -) são CONTEXTO adjacente às mudanças. Use-as para entender a estrutura, mas analise apenas linhas com +."

#### Scenario: Posicionamento da explicação
- **WHEN** o prompt é montado
- **THEN** a explicação aparece na seção "REGRAS ANTI-FALSOS POSITIVOS" junto com as outras regras
