## ADDED Requirements

### Requirement: Carregar traduções de arquivos YAML
O sistema SHALL carregar traduções de arquivos YAML localizados em `src/code_reviewer/locales/`.

#### Scenario: Carregamento de idioma existente
- **WHEN** o sistema inicializa com idioma "pt-br"
- **THEN** o sistema carrega traduções de `locales/pt-br.yaml`

#### Scenario: Carregamento de idioma inexistente
- **WHEN** o sistema inicializa com idioma "fr" que não existe
- **THEN** o sistema faz fallback para "pt-br" e emite warning

### Requirement: Função de tradução t()
O sistema SHALL fornecer uma função `t(key, **kwargs)` para obter traduções.

#### Scenario: Tradução simples
- **WHEN** o código chama `t("cli.getting_diff")`
- **THEN** retorna a string traduzida para o idioma atual

#### Scenario: Tradução com interpolação
- **WHEN** o código chama `t("cli.analyzing", branch="feat/x", base="main")`
- **THEN** retorna a string com variáveis substituídas (ex: "Analisando: feat/x → main")

#### Scenario: Chave inexistente
- **WHEN** o código chama `t("chave.inexistente")`
- **THEN** retorna a própria chave como fallback e emite warning em modo debug

### Requirement: Configurar idioma global
O sistema SHALL permitir configurar o idioma atual via função `set_language(lang)`.

#### Scenario: Definir idioma
- **WHEN** o código chama `set_language("en")`
- **THEN** todas as chamadas subsequentes a `t()` usam traduções em inglês

#### Scenario: Obter idioma atual
- **WHEN** o código chama `get_language()`
- **THEN** retorna o código do idioma atual (ex: "pt-br")

### Requirement: Idiomas suportados inicialmente
O sistema SHALL suportar os idiomas `pt-br` (padrão) e `en` (inglês).

#### Scenario: Listar idiomas disponíveis
- **WHEN** o código chama `get_available_languages()`
- **THEN** retorna lista com pelo menos ["pt-br", "en"]

### Requirement: Cache de traduções
O sistema SHALL fazer cache das traduções em memória após primeiro carregamento.

#### Scenario: Carregamento único
- **WHEN** o sistema carrega traduções de um idioma
- **THEN** chamadas subsequentes usam cache em memória sem reler arquivo

### Requirement: Fallback para idioma padrão
O sistema SHALL usar pt-br como fallback quando uma tradução não existir no idioma selecionado.

#### Scenario: Tradução parcial
- **WHEN** o idioma "en" não tem tradução para "cli.nova_chave"
- **THEN** o sistema busca em "pt-br" antes de retornar a chave como fallback

### Requirement: Prompts da IA por idioma
O sistema SHALL carregar templates de prompt específicos por idioma.

#### Scenario: Prompt em português
- **WHEN** o idioma é "pt-br"
- **THEN** o sistema usa `prompts/review_system_pt-br.md`

#### Scenario: Prompt em inglês
- **WHEN** o idioma é "en"
- **THEN** o sistema usa `prompts/review_system_en.md`
