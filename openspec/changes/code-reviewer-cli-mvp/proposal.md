## Why

Equipes de desenvolvimento precisam de uma primeira camada automatizada de revisão de código que analise mudanças (diffs) em busca de falhas de segurança, problemas de performance e bugs potenciais — antes que um revisor humano gaste tempo. Hoje, nenhuma ferramenta open source oferece backtracking de contexto (rastrear callers/callees das funções modificadas), resultando em análises superficiais com falsos positivos.

## What Changes

- Criação de uma ferramenta CLI em Python que analisa o diff de uma branch contra uma branch base
- Implementação de um parser de diff que extrai funções modificadas a partir dos hunk headers do git
- Construção de um módulo de backtracking que traça o grafo de contexto (callers e callees) via grep
- Montagem de prompts estruturados com instruções para retornar JSON com schema definido
- Execução da análise via CLIs de IA (Gemini CLI, Copilot CLI, etc.) através de uma interface plugável (Strategy pattern)
- Parsing e validação do JSON retornado pela IA com modelos Pydantic
- Renderização formatada dos resultados no terminal (MVP)
- Saída no terminal com severidades: CRITICAL, WARNING, INFO

## Capabilities

### New Capabilities

- `diff-parsing`: Extrair e parsear diffs do git, identificando arquivos modificados, funções afetadas (via hunk headers) e linhas alteradas
- `context-backtracking`: Construir grafo de contexto ao redor das mudanças — rastrear callers (quem chama) e callees (o que é chamado) das funções modificadas via grep
- `prompt-building`: Montar prompts estruturados com seções claras (regras, diff, contexto, referências) e instruções para retorno em JSON
- `ai-runner`: Interface plugável para execução de CLIs de IA (Gemini CLI, Copilot CLI, Claude CLI) via subprocess, usando Strategy pattern
- `response-parsing`: Parsear e validar o JSON retornado pela IA contra um schema definido (Pydantic), com fallbacks para outputs malformados
- `terminal-output`: Renderizar resultados da análise no terminal com formatação, cores e resumo por severidade

### Modified Capabilities

## Impact

- **Novo projeto Python**: Estrutura completa com pyproject.toml, src layout, testes
- **Dependências**: click (CLI), pydantic (validação), subprocess (chamada ao CLI de IA)
- **Pré-requisitos do ambiente**: Git instalado, pelo menos um CLI de IA (gemini-cli, copilot-cli, etc.) configurado
- **Futuro**: Integração com API do GitLab para postar comments inline em MRs, exit codes para falhar pipelines CI/CD
