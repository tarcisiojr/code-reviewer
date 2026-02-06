## Why

Desenvolvedores estão subindo código com erros de ortografia e mensagens confusas em textos voltados ao usuário (exceções, mensagens de erro, arquivos i18n). Isso prejudica a credibilidade do software e a experiência do usuário. A ferramenta de review pode detectar esses problemas automaticamente.

## What Changes

- Nova categoria de finding `text-quality` para verificação de ortografia e clareza semântica
- Nova flag `--text-quality` (opt-in, desligada por padrão) para ativar a verificação
- Prompt da IA modificado para incluir instruções de verificação de texto quando flag ativada
- Verificação aplicada apenas em padrões específicos (mensagens ao usuário) e arquivos i18n

## Capabilities

### New Capabilities

- `text-quality-review`: Define a nova categoria de verificação que analisa ortografia e clareza semântica em mensagens voltadas ao usuário. Inclui regras de escopo (quais strings verificar), severidade padrão (INFO), e integração com o idioma configurado via `--lang`.

### Modified Capabilities

- `prompt-building`: Adicionar seção condicional no prompt para instruir a IA a verificar ortografia e clareza quando `--text-quality` está ativo. Define quais padrões de código e arquivos devem ser analisados.

## Impact

- **models.py**: Novo valor `TEXT_QUALITY = "text-quality"` no enum `Category`
- **cli.py**: Nova opção `--text-quality` no comando review
- **prompt_builder.py**: Lógica condicional para incluir instruções de text-quality
- **prompts/review_system.md**: Nova seção de verificação de texto (condicional)
- **formatters/terminal.py**: Cor/ícone para categoria text-quality
- **locales/**: Novas chaves de tradução para a categoria
