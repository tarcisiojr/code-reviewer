## Context

O Code Reviewer CLI é uma ferramenta de linha de comando que analisa diffs de código usando IA. Atualmente, todas as mensagens de interface (status, erros, labels de output) estão hardcoded em português brasileiro nos módulos Python. Os prompts enviados à IA também estão em português.

**Estado atual**:
- Mensagens de CLI em `cli.py` (ex: "Analisando diff...", "Erro ao obter branch")
- Labels de output em `formatters/terminal.py` (ex: "Sugestão:", "RESUMO:")
- Mensagens de status em `formatters/progress.py`
- Prompt template em `prompts/review_system.md` (português)

**Restrições**:
- Manter compatibilidade total com uso atual (pt-br como padrão)
- Não adicionar dependências externas pesadas (evitar gettext, babel)
- Solução simples e manutenível

## Goals / Non-Goals

**Goals:**
- Permitir seleção de idioma via `--lang` no CLI
- Extrair todas as strings user-facing para arquivos de tradução
- Suportar pt-br (padrão) e en (inglês) inicialmente
- Facilitar adição de novos idiomas no futuro
- Adaptar prompt da IA conforme idioma selecionado

**Non-Goals:**
- Internacionalização completa (formatação de datas, números, pluralização complexa)
- Detecção automática de idioma do sistema
- Tradução em tempo real ou dinâmica
- Suporte a mais de 2 idiomas nesta iteração

## Decisions

### 1. Formato de armazenamento: YAML

**Decisão**: Usar arquivos YAML para traduções em `src/code_reviewer/locales/`

**Alternativas consideradas**:
- JSON: Menos legível, sem suporte a comentários
- gettext (.po): Overhead de ferramentas, complexidade desnecessária
- Python dicts: Mistura código com dados

**Rationale**: YAML é legível, suporta comentários, e PyYAML já é dependência comum. Estrutura hierárquica facilita organização por módulo.

### 2. Estrutura das traduções: Flat com prefixos

**Decisão**: Chaves flat com prefixo de módulo (ex: `cli.analyzing`, `terminal.summary`)

```yaml
# locales/pt-br.yaml
cli:
  analyzing: "Analisando: {branch} → {base}"
  getting_diff: "Obtendo diff..."
  error_branch: "Erro ao obter branch atual: {error}"

terminal:
  summary: "RESUMO:"
  suggestion: "Sugestão:"
  no_problems: "✓ Nenhum problema encontrado. Código aprovado!"
```

**Rationale**: Prefixos evitam colisões e facilitam localizar onde cada string é usada.

### 3. API de acesso: Função `t()` com contexto

**Decisão**: Criar módulo `i18n` com função `t(key, **kwargs)` que usa idioma do contexto global.

```python
from code_reviewer.i18n import t, set_language

set_language("en")
message = t("cli.analyzing", branch="feature/x", base="main")
```

**Alternativas consideradas**:
- Classe Translator injetada: Mais complexo, requer passar instância
- Decorators: Over-engineering para o caso de uso

**Rationale**: Função global é simples, familiar (padrão gettext), e suficiente para CLI sem concorrência.

### 4. Prompts da IA: Arquivos separados por idioma

**Decisão**: Manter templates de prompt separados em `prompts/review_system_{lang}.md`

**Rationale**: Prompts são textos longos com formatação específica. Traduzir inline seria confuso. Arquivos separados permitem ajuste fino por idioma.

### 5. Fallback: Sempre para pt-br

**Decisão**: Se uma chave não existir no idioma selecionado, usar pt-br como fallback.

**Rationale**: Garante que a ferramenta nunca quebre por tradução faltante. pt-br é o idioma mais completo.

### 6. Passagem do idioma: Via opção CLI global

**Decisão**: Adicionar `--lang` como opção do grupo `@main.command()` que propaga para submódulos.

```python
@click.option("--lang", "-l", default="pt-br", help="Idioma das mensagens")
def review(lang: str, ...):
    set_language(lang)
    ...
```

**Rationale**: Simples, explícito, sem magia. Usuário controla o idioma por execução.

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| Traduções incompletas em novos idiomas | Fallback automático para pt-br |
| Performance de carregar YAML | Lazy loading + cache em memória (load uma vez) |
| Chaves de tradução incorretas em runtime | Testes unitários verificam existência de chaves |
| Prompt em idioma diferente pode afetar qualidade da IA | Testar com ambos idiomas; ajustar prompts conforme necessário |
| Manutenção de múltiplos arquivos de tradução | Documentar processo; manter en e pt-br sincronizados |

## Open Questions

1. ~~Qual formato usar para interpolação de variáveis?~~ → Decidido: `{variable}` (format string Python)
2. Devemos permitir override via variável de ambiente `CODE_REVIEWER_LANG`? → Pode ser adicionado posteriormente
