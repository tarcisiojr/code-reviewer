## ADDED Requirements

### Requirement: Opt-out via variável de ambiente
O sistema SHALL desabilitar toda telemetria quando a variável de ambiente `AIREV_NO_TELEMETRY` estiver definida com valor `1`. Nenhum evento SHALL ser enviado, nenhuma conexão de rede SHALL ser feita, e o SDK PostHog NÃO SHALL ser inicializado.

#### Scenario: Telemetria desabilitada via env var
- **WHEN** `AIREV_NO_TELEMETRY=1` está definida no ambiente
- **THEN** nenhum evento é enviado ao PostHog e nenhuma chamada de rede é feita pelo módulo analytics

#### Scenario: Telemetria habilitada por padrão
- **WHEN** `AIREV_NO_TELEMETRY` não está definida ou tem valor diferente de `1`
- **THEN** o sistema captura e envia eventos normalmente

### Requirement: Identidade anônima persistente
O sistema SHALL gerar um UUID v4 na primeira execução e persisti-lo em `~/.cache/airev/anonymous_id`. Este UUID SHALL ser usado como `distinct_id` em todos os eventos PostHog. O UUID MUST ser verdadeiramente aleatório e não-reversível a dados do usuário.

#### Scenario: Primeira execução gera UUID
- **WHEN** o arquivo `~/.cache/airev/anonymous_id` não existe
- **THEN** o sistema gera um UUID v4, salva no arquivo, e usa como distinct_id

#### Scenario: Execuções subsequentes reutilizam UUID
- **WHEN** o arquivo `~/.cache/airev/anonymous_id` já existe com UUID válido
- **THEN** o sistema lê e reutiliza o UUID existente

#### Scenario: Arquivo corrompido regenera UUID
- **WHEN** o arquivo `~/.cache/airev/anonymous_id` existe mas contém conteúdo inválido
- **THEN** o sistema gera um novo UUID v4 e sobrescreve o arquivo

### Requirement: Evento review_started
O sistema SHALL capturar o evento `review_started` no início do comando `review`, contendo apenas metadados de configuração: `runner`, `lang`, `json_output`, `text_quality`, `show_deps`, `no_interactive`, `min_confidence`, `context_lines`, `version`.

#### Scenario: Captura de configuração do review
- **WHEN** o usuário executa `airev review --base main --runner gemini --text-quality`
- **THEN** o sistema envia evento `review_started` com `runner=gemini`, `text_quality=true`, e demais flags com seus valores padrão

### Requirement: Evento review_completed
O sistema SHALL capturar o evento `review_completed` ao final bem-sucedido de um review, contendo: `duration_s`, `files_count`, `findings_total`, `findings_critical`, `findings_warning`, `findings_info`, `version`.

#### Scenario: Review finalizado com sucesso
- **WHEN** o review completa sem erros e produz findings
- **THEN** o sistema envia evento `review_completed` com duração em segundos, contagem de arquivos analisados e breakdown de findings por severidade

### Requirement: Evento review_failed
O sistema SHALL capturar o evento `review_failed` quando o review falha em qualquer etapa, contendo: `error_type` (valor enum fixo) e `version`. O `error_type` MUST ser um dos valores: `branch_error`, `diff_error`, `runner_unavailable`, `runner_not_found`, `runner_error`, `parse_error`.

#### Scenario: Falha na obtenção de diff
- **WHEN** o comando `git diff` falha durante o review
- **THEN** o sistema envia evento `review_failed` com `error_type=diff_error`

#### Scenario: Runner não disponível
- **WHEN** o runner selecionado não está instalado ou acessível
- **THEN** o sistema envia evento `review_failed` com `error_type=runner_unavailable`

### Requirement: Nenhum dado sensível nos eventos
O sistema MUST NOT incluir em nenhum evento: nomes de branch, caminhos de arquivo, conteúdo de código, descrições de PR, mensagens de erro, ou qualquer informação que possa identificar o projeto sendo analisado.

#### Scenario: Propriedades do evento não contêm dados sensíveis
- **WHEN** qualquer evento é capturado
- **THEN** as propriedades contêm apenas: nomes de flags, valores booleanos, contagens numéricas, duração, versão, e error_type (enum fixo)

### Requirement: Falha silenciosa total
Qualquer erro no módulo de analytics — falha de rede, erro do SDK, impossibilidade de ler/gravar UUID — MUST NOT produzir output no console, MUST NOT lançar exceção para o caller, e MUST NOT afetar o fluxo normal da CLI.

#### Scenario: Erro de rede ao enviar evento
- **WHEN** o PostHog está inacessível ou a rede está bloqueada
- **THEN** o erro é ignorado silenciosamente e a CLI continua normalmente

#### Scenario: Erro ao ler/gravar arquivo de UUID
- **WHEN** o diretório `~/.cache/airev/` não é gravável
- **THEN** o sistema ignora o erro e opera sem telemetria nesta execução

### Requirement: Flush assíncrono com timeout
O sistema SHALL registrar um handler `atexit` que executa `posthog.flush()` em uma thread daemon com timeout de 2 segundos. Se o flush não completar dentro do timeout, o processo SHALL encerrar normalmente sem aguardar.

#### Scenario: Flush completa dentro do timeout
- **WHEN** a rede está disponível e o flush leva menos de 2 segundos
- **THEN** os eventos são enviados com sucesso antes do processo encerrar

#### Scenario: Flush excede o timeout
- **WHEN** a rede está lenta e o flush leva mais de 2 segundos
- **THEN** o processo encerra normalmente após 2 segundos sem aguardar o flush

### Requirement: Inicialização lazy do SDK
O SDK PostHog MUST NOT ser importado ou inicializado até que o primeiro evento seja capturado. Se a telemetria estiver desabilitada, o SDK MUST NOT ser importado em nenhum momento.

#### Scenario: Import lazy na primeira chamada
- **WHEN** `track_event()` é chamado pela primeira vez
- **THEN** o SDK PostHog é importado e inicializado neste momento

#### Scenario: SDK não importado quando desabilitado
- **WHEN** `AIREV_NO_TELEMETRY=1` está definida
- **THEN** o módulo `posthog` nunca é importado durante a execução
