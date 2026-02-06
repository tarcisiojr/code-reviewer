## 1. Setup do módulo i18n

- [x] 1.1 Criar estrutura de diretórios `src/code_reviewer/i18n/` e `src/code_reviewer/locales/`
- [x] 1.2 Criar `src/code_reviewer/i18n/__init__.py` com exports públicos

## 2. Implementação core do i18n

- [x] 2.1 Implementar função `load_translations(lang)` para carregar YAML
- [x] 2.2 Implementar função `t(key, **kwargs)` para obter traduções com interpolação
- [x] 2.3 Implementar `set_language(lang)` e `get_language()` para configurar idioma global
- [x] 2.4 Implementar `get_available_languages()` para listar idiomas disponíveis
- [x] 2.5 Implementar cache em memória para traduções carregadas
- [x] 2.6 Implementar fallback para pt-br quando tradução não existir

## 3. Arquivos de tradução

- [x] 3.1 Criar `locales/pt-br.yaml` com todas as strings extraídas do código
- [x] 3.2 Criar `locales/en.yaml` com traduções em inglês

## 4. Prompt com suporte a idioma

- [x] 4.1 Adicionar placeholder `{language}` no prompt para instrução de idioma de resposta
- [x] 4.2 Atualizar `prompt_builder.py` para passar idioma ao prompt

## 5. Integração com CLI

- [x] 5.1 Adicionar opção `--lang` / `-l` ao comando `review` em `cli.py`
- [x] 5.2 Chamar `set_language(lang)` no início do comando
- [x] 5.3 Substituir strings hardcoded em `cli.py` por chamadas a `t()`

## 6. Atualização dos formatters

- [x] 6.1 Atualizar `formatters/terminal.py` para usar `t()` em todas as mensagens
- [x] 6.2 Atualizar `formatters/progress.py` para usar `t()` em mensagens de status
- [x] 6.3 Atualizar `response_parser.py` para usar `t()` em mensagens de fallback

## 7. Testes

- [x] 7.1 Criar testes para módulo i18n (carregamento, tradução, fallback)
- [x] 7.2 Criar testes para verificar que todas as chaves existem nos arquivos de locale
- [x] 7.3 Testar CLI com `--lang pt-br` e `--lang en`
