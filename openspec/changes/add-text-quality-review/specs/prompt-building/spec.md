## ADDED Requirements

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
