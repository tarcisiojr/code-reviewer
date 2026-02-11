## 1. Modelo e Categoria

- [x] 1.1 Adicionar `TEXT_QUALITY = "text-quality"` ao enum `Category` em `models.py`

## 2. CLI

- [x] 2.1 Adicionar flag `--text-quality` ao comando review em `cli.py`
- [x] 2.2 Passar parâmetro `text_quality` para o prompt builder

## 3. Prompt Builder

- [x] 3.1 Adicionar parâmetro `text_quality: bool = False` na função de build do prompt
- [x] 3.2 Adicionar placeholder `{text_quality_section}` no template `prompts/review_system.md`
- [x] 3.3 Criar conteúdo da seção text-quality com instruções de escopo (padrões de código e arquivos)
- [x] 3.4 Implementar substituição condicional do placeholder (seção completa ou string vazia)

## 4. Template de Prompt

- [x] 4.1 Adicionar seção "QUALIDADE DE TEXTO" ao template com instruções de verificação
- [x] 4.2 Incluir lista de padrões de código a verificar (raise, print, message=, etc)
- [x] 4.3 Incluir lista de arquivos a verificar (locales/**, i18n/**)
- [x] 4.4 Incluir lista de exclusões (snake_case, camelCase, termos técnicos)

## 5. Formatação Terminal

- [x] 5.1 Adicionar cor para categoria text-quality em `formatters/terminal.py`
- [x] 5.2 Adicionar ícone para categoria text-quality no modo rico

## 6. Internacionalização

- [x] 6.1 Adicionar chave de tradução para categoria text-quality nos locales pt-br
- [x] 6.2 Adicionar chave de tradução para categoria text-quality nos locales en

## 7. Testes

- [x] 7.1 Teste unitário: flag --text-quality reconhecida pelo CLI
- [x] 7.2 Teste unitário: prompt inclui seção text-quality quando flag ativa
- [x] 7.3 Teste unitário: prompt não inclui seção quando flag inativa
- [x] 7.4 Teste unitário: categoria TEXT_QUALITY reconhecida pelo response parser
