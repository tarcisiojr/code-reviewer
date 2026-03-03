## 1. Refatorar key bindings do prompt interativo

- [x] 1.1 Criar key binding para Enter que envia o texto (`validate_and_handle()`) ou insere nova linha se última char é `\` (removendo o `\`)
- [x] 1.2 Criar key binding para Shift+Enter / Alt+Enter (`escape`, `enter`) que insere nova linha
- [x] 1.3 Criar key binding para Esc que cancela o prompt retornando None (`event.app.exit(result=None)`)
- [x] 1.4 Remover tratamento de `KeyboardInterrupt` (Ctrl+C) como cancelamento do prompt

## 2. Atualizar mensagem de instrução

- [x] 2.1 Reformular mensagem para: `📝 Descrição das alterações (cole o texto do MR):` seguido de `Enter envia · Shift+Enter ou \ para nova linha · Esc para pular`

## 3. Atualizar testes

- [x] 3.1 Adicionar teste para Enter enviar texto (submit)
- [x] 3.2 Adicionar teste para `\`+Enter inserir nova linha e remover o `\`
- [x] 3.3 Adicionar teste para Esc cancelar e retornar None
- [x] 3.4 Adicionar teste para Shift+Enter inserir nova linha
- [x] 3.5 Adicionar teste para texto colado preservar quebras de linha
- [x] 3.6 Remover/atualizar testes que referenciam Ctrl+C/Ctrl+D como cancelamento
