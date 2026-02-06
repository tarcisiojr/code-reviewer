## Context

O airev atualmente analisa código buscando problemas de segurança, performance, bugs e resource leaks. O prompt enviado à IA (`prompts/review_system.md`) instrui sobre essas categorias específicas. O sistema já suporta internacionalização via `--lang` e usa um enum `Category` para classificar findings.

Desenvolvedores têm subido código com erros de ortografia e mensagens confusas em textos voltados ao usuário. Esta funcionalidade adiciona uma nova categoria opt-in para detectar esses problemas.

## Goals / Non-Goals

**Goals:**
- Adicionar categoria `text-quality` para detectar erros de ortografia e clareza semântica
- Tornar a verificação opt-in via flag `--text-quality` (desligada por padrão)
- Verificar apenas strings em contextos específicos (mensagens ao usuário, arquivos i18n)
- Usar o idioma configurado via `--lang` para validar ortografia

**Non-Goals:**
- Não verificar nomes de variáveis, identificadores ou termos técnicos
- Não fazer correção automática (apenas reportar)
- Não adicionar dependência de spell-checker externo (usar capacidade nativa da IA)

## Decisions

### Decisão 1: Categoria separada vs subcategoria de bug
**Escolha**: Nova categoria `TEXT_QUALITY = "text-quality"`

**Alternativas consideradas**:
- Usar categoria `bug` existente: Rejeitada porque typos não são bugs no sentido técnico
- Criar subcategorias: Rejeitada porque aumentaria complexidade do modelo

**Rationale**: Categoria separada permite filtrar/ignorar facilmente e alinha com o padrão existente de categorias independentes.

### Decisão 2: Severidade padrão
**Escolha**: Sempre INFO

**Alternativas consideradas**:
- WARNING para mensagens muito confusas: Rejeitada para manter simplicidade
- Configurável por finding: Rejeitada para evitar complexidade

**Rationale**: Erros de texto nunca são críticos para funcionamento do sistema. INFO é apropriado.

### Decisão 3: Opt-in vs Opt-out
**Escolha**: Opt-in via `--text-quality` (desligado por padrão)

**Alternativas consideradas**:
- Ligado por padrão com `--no-text-quality`: Rejeitada porque adiciona ruído para quem não quer

**Rationale**: Funcionalidade nova não deve mudar comportamento padrão existente.

### Decisão 4: Escopo de verificação via prompt
**Escolha**: Instruir a IA sobre quais padrões verificar diretamente no prompt

**Padrões a verificar**:
- Código: `raise *Error(...)`, `raise *Exception(...)`, `print(...)`, `console.log(...)`, `message=`, `label=`, `title=`, `description=`, `text=`
- Arquivos: `locales/**/*`, `i18n/**/*`, `messages.*`, `strings.*`

**Rationale**: A IA já entende contexto e pode distinguir mensagens ao usuário de identificadores técnicos.

### Decisão 5: Implementação via seção condicional no prompt
**Escolha**: Adicionar seção opcional no template `review_system.md` ativada por placeholder

**Implementação**:
- Novo placeholder `{text_quality_section}` no template
- Quando `--text-quality` ativo: preenche com instruções de verificação
- Quando inativo: placeholder substituído por string vazia

**Rationale**: Mantém template legível e evita lógica complexa de montagem.

## Risks / Trade-offs

**Ruído em termos técnicos** → Mitigação: Instruções explícitas no prompt para ignorar snake_case, camelCase, termos técnicos comuns.

**Falsos positivos em nomes próprios** → Mitigação: Instruir IA a não reportar nomes próprios ou termos de domínio específico.

**Performance do prompt maior** → Mitigação: Seção adicional é pequena (~200 tokens), impacto negligenciável.
