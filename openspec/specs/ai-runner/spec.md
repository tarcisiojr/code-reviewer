## ADDED Requirements

### Requirement: Interface plugável para CLIs de IA
O sistema SHALL definir um Protocol `AIRunner` com método `run(prompt: str, workdir: Path) -> str` que cada implementação de CLI MUST seguir.

#### Scenario: Runner executa e retorna output
- **WHEN** o método `run` é chamado com um prompt e o diretório de trabalho
- **THEN** o runner executa o CLI de IA correspondente e retorna a saída como string

### Requirement: Runner para Gemini CLI
O sistema SHALL implementar `GeminiCLIRunner` que executa o prompt via `gemini` CLI, passando o prompt como argumento ou via arquivo temporário.

#### Scenario: Execução com sucesso
- **WHEN** o gemini CLI está instalado e configurado
- **THEN** o runner executa `gemini` com o prompt e retorna o output completo

#### Scenario: Gemini CLI não instalado
- **WHEN** o comando `gemini` não é encontrado no PATH
- **THEN** o runner lança erro com mensagem: "gemini-cli não encontrado. Instale em: https://github.com/google-gemini/gemini-cli"

### Requirement: Runner para Copilot CLI
O sistema SHALL implementar `CopilotCLIRunner` que executa o prompt via `gh copilot` CLI.

#### Scenario: Execução com sucesso
- **WHEN** o GitHub CLI com extensão Copilot está instalado e configurado
- **THEN** o runner executa o comando e retorna o output

#### Scenario: Copilot CLI não instalado
- **WHEN** o comando `gh copilot` não é encontrado
- **THEN** o runner lança erro com mensagem clara sobre como instalar

### Requirement: Seleção de runner via parâmetro CLI
O sistema SHALL permitir selecionar o runner via flag `--runner` (ex: `--runner gemini`, `--runner copilot`), com `gemini` como valor default.

#### Scenario: Runner selecionado via flag
- **WHEN** o usuário executa `code-reviewer review --base main --runner copilot`
- **THEN** o sistema usa o `CopilotCLIRunner` para executar a análise

#### Scenario: Runner inválido
- **WHEN** o usuário passa `--runner xyz` e não existe implementação para `xyz`
- **THEN** o sistema exibe erro listando os runners disponíveis

### Requirement: Verificar disponibilidade do CLI no startup
O sistema SHALL verificar se o CLI de IA selecionado está instalado e acessível antes de iniciar a análise.

#### Scenario: CLI disponível
- **WHEN** o runner selecionado verifica que o CLI está no PATH
- **THEN** a análise prossegue normalmente

#### Scenario: CLI indisponível
- **WHEN** o CLI não está instalado
- **THEN** o sistema encerra com mensagem de erro antes de fazer qualquer processamento
