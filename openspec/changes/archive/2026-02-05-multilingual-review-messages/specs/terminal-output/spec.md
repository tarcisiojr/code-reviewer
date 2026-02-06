## ADDED Requirements

### Requirement: Usar sistema i18n para mensagens
O sistema SHALL usar o módulo i18n para todas as mensagens user-facing no terminal.

#### Scenario: Labels traduzidos no output
- **WHEN** o sistema renderiza um finding com sugestão
- **THEN** o label "Sugestão:" vem do sistema i18n via `t("terminal.suggestion")`

#### Scenario: Resumo traduzido
- **WHEN** o sistema exibe o resumo da análise
- **THEN** o label "RESUMO:" vem do sistema i18n via `t("terminal.summary")`

#### Scenario: Mensagem de sucesso traduzida
- **WHEN** a análise não encontra problemas
- **THEN** a mensagem de aprovação vem do sistema i18n via `t("terminal.no_problems")`

### Requirement: Mensagens de progresso traduzidas
O sistema SHALL usar i18n para mensagens de status e progresso.

#### Scenario: Status de análise
- **WHEN** o sistema exibe "Analisando diff..."
- **THEN** a mensagem vem do sistema i18n via `t("cli.analyzing_diff")`

#### Scenario: Mensagens de erro
- **WHEN** ocorre um erro ao obter diff
- **THEN** a mensagem de erro vem do sistema i18n com interpolação de variáveis
