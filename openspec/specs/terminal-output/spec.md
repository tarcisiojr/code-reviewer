## ADDED Requirements

### Requirement: Usar biblioteca rich para renderização
O sistema SHALL usar a biblioteca `rich` para renderização de todas as saídas no terminal.

#### Scenario: Cores via rich Console
- **WHEN** o sistema renderiza um finding CRITICAL
- **THEN** o terminal usa `rich.console.Console` para exibir cores e formatação

#### Scenario: Fallback para terminal simples
- **WHEN** o terminal não suporta cores (no_color=True ou TERM=dumb)
- **THEN** o rich automaticamente faz fallback para texto sem cores

### Requirement: Suportar modo silencioso para CI
O sistema SHALL suportar um modo de saída simplificado sem formatação rica para ambientes CI.

#### Scenario: Output em CI sem formatação rica
- **WHEN** o sistema está em modo CI (--no-progress ou auto-detectado)
- **THEN** a saída usa apenas texto simples sem cores ou formatação especial

#### Scenario: JSON output não afetado
- **WHEN** o usuário usa --json-output
- **THEN** a saída é JSON puro independente do modo CI ou normal
