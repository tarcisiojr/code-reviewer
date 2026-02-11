## ADDED Requirements

### Requirement: Montar prompt com seções estruturadas
O sistema SHALL montar um prompt contendo seções claramente delimitadas: REGRAS, DIFF, ARQUIVOS MODIFICADOS e REFERÊNCIAS (backtracking).

#### Scenario: Prompt completo com todas as seções
- **WHEN** o diff e o contexto foram extraídos com sucesso
- **THEN** o prompt contém as 4 seções separadas por delimitadores claros, com o diff completo, conteúdo dos arquivos e referências de backtracking

### Requirement: Incluir regras de escopo no prompt
O sistema SHALL incluir instruções explícitas para que a IA analise APENAS as linhas adicionadas/modificadas no diff, usando o contexto e referências apenas para entender a mudança, sem sugerir melhorias em código não alterado.

#### Scenario: Regras de escopo presentes
- **WHEN** o prompt é montado
- **THEN** o prompt contém instrução explícita: "Analise APENAS as mudanças marcadas com + no DIFF. Use CONTEXTO e REFERÊNCIAS para entender a mudança, NÃO para sugerir melhorias em código existente."

### Requirement: Incluir schema JSON esperado no prompt
O sistema SHALL incluir no prompt o schema JSON exato que a IA MUST retornar, com exemplo de um finding completo.

#### Scenario: Schema presente no prompt
- **WHEN** o prompt é montado
- **THEN** o prompt contém o schema JSON com campos: file, line, severity, category, title, description, suggestion, code_snippet

### Requirement: Incluir categorias de análise no prompt
O sistema SHALL instruir a IA a focar nas categorias: segurança (injection, XSS, secrets), performance (N+1, loops), bugs potenciais (null, race condition) e recursos não fechados (connections, files).

#### Scenario: Categorias listadas
- **WHEN** o prompt é montado
- **THEN** o prompt contém lista explícita das categorias de análise com exemplos

### Requirement: Carregar template de prompt de arquivo externo
O sistema SHALL carregar o system prompt de um arquivo markdown (`prompts/review_system.md`) e substituir placeholders (`{diff}`, `{context}`, `{references}`, `{json_schema}`) pelos valores reais.

#### Scenario: Template carregado e preenchido
- **WHEN** o prompt builder é chamado com diff, contexto e referências
- **THEN** o arquivo template é lido, placeholders são substituídos e o prompt final é retornado como string

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

### Requirement: Incluir descrição das alterações no prompt
O sistema SHALL incluir uma seção de descrição das alterações no prompt quando fornecida pelo usuário.

#### Scenario: Descrição presente no prompt
- **WHEN** o usuário forneceu descrição (via flag ou interativamente)
- **THEN** o prompt contém uma seção "DESCRIÇÃO DAS ALTERAÇÕES" com o texto fornecido

#### Scenario: Descrição ausente não aparece no prompt
- **WHEN** o usuário não forneceu descrição
- **THEN** o prompt não contém a seção "DESCRIÇÃO DAS ALTERAÇÕES"

#### Scenario: Posicionamento da seção de descrição
- **WHEN** a descrição é incluída no prompt
- **THEN** a seção aparece após "REGRAS IMPORTANTES" e antes de "FOCO DA ANÁLISE"

### Requirement: Suportar placeholder de descrição no template
O sistema SHALL suportar um placeholder `{description}` no template do prompt que é substituído pela seção de descrição ou string vazia.

#### Scenario: Placeholder substituído com descrição
- **WHEN** descrição foi fornecida
- **THEN** o placeholder `{description}` é substituído pela seção formatada

#### Scenario: Placeholder substituído sem descrição
- **WHEN** descrição não foi fornecida
- **THEN** o placeholder `{description}` é substituído por string vazia

### Requirement: Incluir seção de text-quality condicionalmente no prompt
O sistema SHALL incluir uma seção de instruções para verificação de qualidade de texto no prompt quando a flag `--text-quality` estiver ativa.

#### Scenario: Seção incluída quando flag ativa
- **WHEN** o prompt é montado com `text_quality=True`
- **THEN** o prompt contém seção "QUALIDADE DE TEXTO" com instruções de verificação

#### Scenario: Seção omitida quando flag inativa
- **WHEN** o prompt é montado com `text_quality=False`
- **THEN** o prompt não contém seção de verificação de texto

### Requirement: Instruções de escopo para text-quality
O sistema SHALL incluir no prompt instruções claras sobre quais strings verificar e quais ignorar.

#### Scenario: Padrões de código a verificar
- **WHEN** o prompt inclui seção de text-quality
- **THEN** o prompt lista padrões: `raise *Error(...)`, `raise *Exception(...)`, `print(...)`, `console.log(...)`, parâmetros `message=`, `label=`, `title=`, `description=`, `text=`

#### Scenario: Arquivos a verificar
- **WHEN** o prompt inclui seção de text-quality
- **THEN** o prompt lista padrões de arquivos: `locales/**/*`, `i18n/**/*`, `messages.*`, `strings.*`

#### Scenario: Exclusões explícitas
- **WHEN** o prompt inclui seção de text-quality
- **THEN** o prompt instrui a ignorar: identificadores (snake_case, camelCase), termos técnicos (HTTP, JSON, API), nomes próprios

### Requirement: Placeholder para seção text-quality
O sistema SHALL usar placeholder `{text_quality_section}` no template de prompt para inserção condicional da seção.

#### Scenario: Placeholder substituído quando ativo
- **WHEN** `text_quality=True` e o template contém `{text_quality_section}`
- **THEN** o placeholder é substituído pelas instruções completas de verificação

#### Scenario: Placeholder removido quando inativo
- **WHEN** `text_quality=False` e o template contém `{text_quality_section}`
- **THEN** o placeholder é substituído por string vazia

### Requirement: Incluir persona clara no prompt
O sistema SHALL definir a persona "revisor de código sênior" no início do prompt, estabelecendo expertise e propósito.

#### Scenario: Persona presente no prompt
- **WHEN** o prompt é montado
- **THEN** o prompt inicia com texto similar a: "Você é um revisor de código sênior especializado em segurança, performance e qualidade de software. Sua função é fornecer feedback construtivo, acionável e de alta confiança."

### Requirement: Incluir princípios fundamentais no prompt
O sistema SHALL incluir uma seção de princípios fundamentais com 5 itens: foco nas mudanças, contexto como referência, alta confiança, acionável, sem ruído.

#### Scenario: Princípios presentes no prompt
- **WHEN** o prompt é montado
- **THEN** o prompt contém seção "PRINCÍPIOS FUNDAMENTAIS" com os 5 itens listados

### Requirement: Incluir regras anti-falsos positivos no prompt
O sistema SHALL incluir uma seção de regras anti-falsos positivos com pelo menos 6 regras específicas para evitar findings irrelevantes.

#### Scenario: Regras anti-ruído presentes
- **WHEN** o prompt é montado
- **THEN** o prompt contém seção "REGRAS ANTI-FALSOS POSITIVOS" incluindo: não questionar imports, não tratar escopo aberto como incompleto, não sugerir em código não alterado, não reportar sintaxe baseado em diff parcial, não duplicar funcionalidade, não sugerir refatorações sem benefício claro

### Requirement: Incluir categoria error-handling no prompt
O sistema SHALL incluir a categoria "Tratamento de Erros" nas instruções de análise.

#### Scenario: Categoria error-handling presente
- **WHEN** o prompt é montado
- **THEN** o prompt contém seção de "Tratamento de Erros (WARNING)" listando: exceções silenciadas, catch genérico, falta de logging, promises sem catch

### Requirement: Incluir categoria breaking-change no prompt
O sistema SHALL incluir a categoria "Breaking Changes em APIs" nas instruções de análise.

#### Scenario: Categoria breaking-change presente
- **WHEN** o prompt é montado
- **THEN** o prompt contém seção "Breaking Changes em APIs (WARNING)" listando os patterns a detectar: remoção de campos, campos opcionais tornados obrigatórios, mudança de tipo, remoção de endpoints, valores de enum removidos

### Requirement: Incluir definições de severidade no prompt
O sistema SHALL incluir definições claras do que cada nível de severidade significa.

#### Scenario: Definições de severidade presentes
- **WHEN** o prompt é montado
- **THEN** o prompt contém seção "SEVERIDADE" definindo: CRITICAL (vulnerabilidade, crash, perda de dados), WARNING (bug potencial, performance, breaking change), INFO (robustez, boa prática)

### Requirement: Incluir campo confidence no schema JSON do prompt
O sistema SHALL incluir o campo `confidence` (1-10) no schema JSON de exemplo do prompt.

#### Scenario: Schema com confidence
- **WHEN** o prompt é montado
- **THEN** o JSON_SCHEMA_EXAMPLE contém campo "confidence" com valor de exemplo (ex: 8)

### Requirement: Instruir LLM sobre priorização por confidence
O sistema SHALL instruir a LLM a priorizar findings de alta confiança e sempre incluir o score.

#### Scenario: Instrução de confidence presente
- **WHEN** o prompt é montado
- **THEN** o prompt contém instrução similar a: "Priorize findings com confiança ≥7. Sempre inclua o score de confiança (1-10) em cada finding."

### Requirement: Instruir sobre linhas de contexto
O sistema SHALL incluir no prompt uma explicação de que linhas sem prefixo `+` ou `-` no diff são linhas de contexto adjacentes às mudanças, não código a ser analisado.

#### Scenario: Explicação de linhas de contexto presente
- **WHEN** o prompt é montado
- **THEN** o prompt contém instrução: "No DIFF, linhas sem prefixo (sem + ou -) são CONTEXTO adjacente às mudanças. Use-as para entender a estrutura, mas analise apenas linhas com +."

#### Scenario: Posicionamento da explicação
- **WHEN** o prompt é montado
- **THEN** a explicação aparece na seção "REGRAS ANTI-FALSOS POSITIVOS" junto com as outras regras
