## ADDED Requirements

### Requirement: Categoria text-quality no modelo
O sistema SHALL suportar a categoria `text-quality` no enum `Category` para classificar findings de ortografia e clareza semântica.

#### Scenario: Categoria reconhecida no parsing
- **WHEN** a IA retorna um finding com `"category": "text-quality"`
- **THEN** o parser reconhece a categoria e cria um objeto Finding válido

#### Scenario: Categoria presente no output JSON
- **WHEN** o usuário usa `--json-output` e há findings de text-quality
- **THEN** o JSON contém findings com `"category": "text-quality"`

### Requirement: Flag --text-quality opt-in
O sistema SHALL fornecer flag `--text-quality` no comando review para ativar verificação de qualidade de texto. A flag SHALL ser desativada por padrão.

#### Scenario: Flag desativada por padrão
- **WHEN** o usuário executa `airev review --base main` sem a flag
- **THEN** o prompt enviado à IA não contém instruções de verificação de texto

#### Scenario: Flag ativada explicitamente
- **WHEN** o usuário executa `airev review --base main --text-quality`
- **THEN** o prompt enviado à IA contém instruções de verificação de texto

### Requirement: Severidade INFO para findings de texto
O sistema SHALL usar severidade INFO para todos os findings da categoria text-quality.

#### Scenario: Finding de typo com severidade INFO
- **WHEN** a IA detecta erro de ortografia em mensagem de usuário
- **THEN** o finding é criado com `severity: INFO`

#### Scenario: Finding de clareza com severidade INFO
- **WHEN** a IA detecta mensagem semanticamente confusa
- **THEN** o finding é criado com `severity: INFO`

### Requirement: Escopo de verificação em padrões de código
O sistema SHALL instruir a IA a verificar ortografia apenas em strings que aparecem em contextos de mensagem ao usuário.

#### Scenario: Verificar strings em exceções
- **WHEN** o diff contém `raise ValueError("Usuário não encotrado")`
- **AND** `--text-quality` está ativo
- **THEN** a IA reporta o erro de ortografia "encotrado" → "encontrado"

#### Scenario: Verificar strings em prints
- **WHEN** o diff contém `print("Arquivo foi não salvo")`
- **AND** `--text-quality` está ativo
- **THEN** a IA reporta a ordem confusa da frase

#### Scenario: Ignorar identificadores técnicos
- **WHEN** o diff contém `config["redis_connection_timeout"]`
- **AND** `--text-quality` está ativo
- **THEN** a IA não reporta erro para snake_case em identificadores

#### Scenario: Ignorar termos técnicos
- **WHEN** o diff contém `raise ValueError("JSON malformed")`
- **AND** `--text-quality` está ativo
- **THEN** a IA não reporta "JSON" ou "malformed" como erros

### Requirement: Escopo de verificação em arquivos i18n
O sistema SHALL instruir a IA a verificar ortografia em arquivos de internacionalização.

#### Scenario: Verificar arquivos de locale
- **WHEN** o diff modifica arquivo em `locales/pt-br/messages.yaml`
- **AND** `--text-quality` está ativo
- **THEN** a IA verifica ortografia nas strings do arquivo

#### Scenario: Verificar arquivos de tradução JSON
- **WHEN** o diff modifica arquivo em `i18n/en.json`
- **AND** `--text-quality` está ativo
- **THEN** a IA verifica ortografia nas strings do arquivo

### Requirement: Idioma de verificação segue --lang
O sistema SHALL verificar ortografia no idioma configurado via flag `--lang`.

#### Scenario: Verificação em português
- **WHEN** o usuário executa com `--lang pt-br --text-quality`
- **THEN** a IA verifica ortografia considerando regras do português brasileiro

#### Scenario: Verificação em inglês
- **WHEN** o usuário executa com `--lang en --text-quality`
- **THEN** a IA verifica ortografia considerando regras do inglês

### Requirement: Formatação de text-quality no terminal
O sistema SHALL renderizar findings de text-quality com formatação visual distinta no terminal.

#### Scenario: Cor para categoria text-quality
- **WHEN** o terminal renderiza um finding de text-quality
- **THEN** a categoria é exibida com cor apropriada (ex: cyan ou magenta)

#### Scenario: Ícone para categoria text-quality
- **WHEN** o terminal renderiza um finding de text-quality em modo rico
- **THEN** um ícone apropriado é exibido (ex: ✏️ ou 📝)
