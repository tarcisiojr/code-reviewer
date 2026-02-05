## ADDED Requirements

### Requirement: Renderizar findings no terminal com formatação
O sistema SHALL renderizar cada finding com: severidade colorida, arquivo e linha, título, descrição e sugestão.

#### Scenario: Finding CRITICAL exibido
- **WHEN** o resultado contém um finding CRITICAL em `services/payment.py:47`
- **THEN** o terminal exibe `[CRITICAL]` em vermelho, seguido de arquivo:linha, título, descrição e sugestão

#### Scenario: Finding WARNING exibido
- **WHEN** o resultado contém um finding WARNING
- **THEN** o terminal exibe `[WARNING]` em amarelo com as mesmas informações

#### Scenario: Finding INFO exibido
- **WHEN** o resultado contém um finding INFO
- **THEN** o terminal exibe `[INFO]` em azul com as mesmas informações

### Requirement: Agrupar findings por arquivo
O sistema SHALL agrupar os findings por arquivo, exibindo o nome do arquivo como header seguido dos findings daquele arquivo.

#### Scenario: Múltiplos findings no mesmo arquivo
- **WHEN** existem 2 findings em `services/payment.py` e 1 em `routes/checkout.py`
- **THEN** o terminal exibe o header `services/payment.py` com 2 findings abaixo, depois `routes/checkout.py` com 1 finding

#### Scenario: Arquivo sem findings
- **WHEN** um arquivo foi analisado mas não teve findings
- **THEN** o terminal exibe o nome do arquivo seguido de "Nenhum problema encontrado"

### Requirement: Exibir resumo ao final
O sistema SHALL exibir um resumo ao final com contadores: total de findings, quantidade por severidade (CRITICAL, WARNING, INFO).

#### Scenario: Resumo com findings
- **WHEN** a análise encontrou 1 CRITICAL, 2 WARNING e 0 INFO
- **THEN** o terminal exibe: "RESUMO: 3 findings (1 critical, 2 warning, 0 info)"

#### Scenario: Resumo sem findings
- **WHEN** a análise não encontrou nenhum finding
- **THEN** o terminal exibe: "Nenhum problema encontrado. Código aprovado!"

### Requirement: Exibir header com informações da análise
O sistema SHALL exibir no topo da saída: nome da branch analisada, branch base, quantidade de arquivos analisados.

#### Scenario: Header exibido
- **WHEN** a análise é executada na branch `feature/add-payment` contra `main` com 3 arquivos
- **THEN** o terminal exibe header com essas informações antes dos findings
