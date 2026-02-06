## Why

O Code Reviewer CLI atualmente tem todas as mensagens hardcoded em português brasileiro diretamente no código-fonte. Isso impede que desenvolvedores de outras equipes ou países utilizem a ferramenta de forma efetiva, e limita a adoção internacional. Adicionar suporte multilingual com pt-br como padrão permite manter a experiência atual enquanto abre portas para usuários de outros idiomas.

## What Changes

- Nova opção `--lang` / `-l` no CLI para selecionar idioma (default: `pt-br`)
- Sistema de tradução baseado em arquivos YAML/JSON por idioma
- Todas as mensagens do CLI extraídas para arquivos de tradução
- Todas as mensagens do formatador terminal extraídas para traduções
- Prompt enviado à IA adaptado conforme idioma selecionado
- Suporte inicial para: `pt-br` (padrão), `en` (inglês)

## Capabilities

### New Capabilities
- `i18n`: Sistema de internacionalização para suporte multilingual de mensagens. Cobre extração de strings, carregamento de traduções, e resolução de mensagens por idioma.

### Modified Capabilities
- `terminal-output`: Adicionar requisito para usar sistema i18n ao invés de strings hardcoded nas mensagens de output

## Impact

- **Código afetado**:
  - `src/code_reviewer/cli.py` - nova opção `--lang`, integração com i18n
  - `src/code_reviewer/formatters/terminal.py` - uso de traduções para labels
  - `src/code_reviewer/formatters/progress.py` - uso de traduções para status
  - `src/code_reviewer/response_parser.py` - mensagens de fallback traduzidas
  - `src/code_reviewer/prompt_builder.py` - prompt template por idioma
  - `src/code_reviewer/prompts/` - múltiplos templates por idioma

- **Novos arquivos**:
  - `src/code_reviewer/i18n/` - módulo de internacionalização
  - `src/code_reviewer/locales/pt-br.yaml` - traduções pt-br
  - `src/code_reviewer/locales/en.yaml` - traduções inglês

- **Dependências**: Nenhuma nova dependência externa necessária (usar stdlib ou PyYAML já existente)

- **Breaking changes**: Nenhum - pt-br permanece como padrão
