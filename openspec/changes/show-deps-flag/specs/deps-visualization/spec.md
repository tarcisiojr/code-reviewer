## ADDED Requirements

### Requirement: Flag --show-deps para ativar visualização
O sistema SHALL aceitar a flag `--show-deps` (ou `-D`) no comando `airev review` para ativar a exibição do grafo de dependências no terminal.

#### Scenario: Flag ativa visualização
- **WHEN** o usuário executa `airev review -b main --show-deps`
- **THEN** o sistema exibe o grafo de dependências para cada função modificada no output

#### Scenario: Flag curta funciona
- **WHEN** o usuário executa `airev review -b main -D`
- **THEN** o comportamento é idêntico a `--show-deps`

#### Scenario: Sem flag não mostra deps
- **WHEN** o usuário executa `airev review -b main` sem a flag
- **THEN** o sistema não exibe o grafo de dependências (comportamento atual)

### Requirement: Renderizar deps integrado por arquivo
O sistema SHALL exibir as dependências de cada função modificada antes dos findings do mesmo arquivo.

#### Scenario: Deps aparecem antes dos findings
- **WHEN** o arquivo `auth.py` tem função modificada `authenticate` e findings
- **THEN** o output mostra primeiro as deps de `authenticate`, depois os findings de `auth.py`

#### Scenario: Múltiplas funções no mesmo arquivo
- **WHEN** o arquivo `auth.py` tem funções `authenticate` e `logout` modificadas
- **THEN** o output mostra deps de ambas funções antes dos findings do arquivo

### Requirement: Mostrar deps de todas funções modificadas
O sistema SHALL exibir dependências para todas as funções modificadas, independente de terem findings associados.

#### Scenario: Arquivo sem findings mas com deps
- **WHEN** o arquivo `utils.py` tem função modificada mas nenhum finding
- **THEN** o output mostra as deps da função e mensagem indicando ausência de findings

#### Scenario: Função sem callers nem callees
- **WHEN** a função modificada não tem callers nem callees
- **THEN** o output indica que não há dependências encontradas

### Requirement: Formato de árvore ASCII para deps
O sistema SHALL renderizar dependências no formato de árvore ASCII com indicadores visuais para callers e callees.

#### Scenario: Estrutura da árvore
- **WHEN** a função `authenticate` tem 2 callers e 1 callee
- **THEN** o output exibe:
  ```
  📊 DEPENDENCIES: authenticate (linha 45)
  │
  ├── 📥 CALLERS (2)
  │   ├── api/routes.py:87     → handle_login(request)
  │   └── cli/commands.py:123  → login_command(args)
  │
  └── 📤 CALLEES (1)
      └── validate_credentials → auth/validators.py:23
  ```

#### Scenario: Callers mostram arquivo:linha e snippet
- **WHEN** a função tem callers
- **THEN** cada caller exibe `arquivo:linha → snippet_do_codigo`

#### Scenario: Callees mostram nome e definição
- **WHEN** a função tem callees
- **THEN** cada callee exibe `nome_funcao → arquivo:linha`

### Requirement: Labels traduzidos via i18n
O sistema SHALL usar o módulo i18n para todos os labels da visualização de deps.

#### Scenario: Header DEPENDENCIES traduzido
- **WHEN** o idioma é pt-br
- **THEN** o header usa `t("terminal.dependencies")` para "DEPENDÊNCIAS"

#### Scenario: Labels CALLERS e CALLEES traduzidos
- **WHEN** o idioma é pt-br
- **THEN** os labels usam `t("terminal.callers")` e `t("terminal.callees")`

#### Scenario: Mensagem de sem deps traduzida
- **WHEN** a função não tem callers nem callees
- **THEN** a mensagem usa `t("terminal.no_deps_found")`
