# Lista de Exercícios — Procedures e Triggers no PostgreSQL
---

# Parte I — Reconhecimento do banco

## Exercício 1

Liste todas as tabelas existentes no banco e inspecione a estrutura de `reserva`, `hospede`, `quarto` e `tipo_quarto`.

## Exercício 2

Conte quantos registros existem nas tabelas `tipo_quarto`, `quarto`, `hospede` e `reserva`.

## Exercício 3

Liste as procedures e funções existentes no banco. Depois, visualize o código de `sp_criar_reserva` e `fn_validar_reserva`.

---

# Parte II — Procedures existentes

## Exercício 4

Execute `sp_reajustar_diarias` para aumentar todas as diárias em 4%. Consulte `tipo_quarto` antes e depois.

## Exercício 5

Execute `sp_reajustar_diarias` para alterar apenas um tipo de quarto, escolhido pelo `id_tipo`.

## Exercício 6

Utilize `sp_criar_reserva` para criar uma reserva válida. Depois consulte id, hóspede, quarto, check-in, checkout, quantidade de hóspedes e valor total.

## Exercício 7

Tente criar uma reserva com checkout anterior ao check-in. Anote a mensagem de erro e explique por que a operação foi bloqueada.

## Exercício 8

Tente criar uma reserva com quantidade de hóspedes maior que a capacidade do quarto. Antes, consulte número, tipo e capacidade do quarto escolhido.

---

# Parte III — Criando Procedures

## Exercício 9

Crie uma procedure `sp_marcar_notificacao_processada` que receba `id_notificacao`, altere `processada` para `TRUE` e lance exceção caso a notificação não exista.

## Exercício 10

Crie uma procedure `sp_colocar_quarto_manutencao` que receba `id_quarto`, altere o status para `Manutenção`, use `RAISE NOTICE` e lance exceção se o quarto não existir.

## Exercício 11

Crie uma procedure `sp_liberar_quarto` que receba `id_quarto`, altere o status para `Disponível` e lance exceção se o quarto não existir.

## Exercício 12

Crie uma procedure `sp_alterar_status_reserva` que receba o id da reserva e um novo status. Permita apenas `Confirmada`, `Hospedada`, `Concluída` e `Cancelada`. Para qualquer outro valor, use `RAISE EXCEPTION`.

## Exercício 13

Crie uma procedure `sp_aplicar_desconto_reserva` que receba id da reserva e percentual de desconto. Valide o percentual entre 0 e 100, reduza `valor_total` e mostre o novo valor com `RAISE NOTICE`.

---

# Parte IV — Criando Triggers de Validação

## Exercício 14

Crie a função `fn_validar_capacidade_quarto`. Ela deve impedir `INSERT` ou `UPDATE` em `reserva` quando `quantidade_hospedes` exceder a capacidade do tipo de quarto.

A função deve consultar a capacidade, comparar com `NEW.quantidade_hospedes`, usar `RAISE EXCEPTION` em caso inválido e retornar `NEW` quando válido.

Crie a trigger `trg_validar_capacidade_quarto` como `BEFORE INSERT OR UPDATE` em `reserva`.

## Exercício 15

Crie `fn_validar_quarto_disponivel` para impedir uma nova reserva quando o quarto estiver `Manutenção` ou `Inativo`.

Crie `trg_validar_quarto_disponivel` como `BEFORE INSERT` em `reserva`.

Teste colocando um quarto em manutenção com a procedure do Exercício 10.

## Exercício 16

Crie `fn_validar_datas_reserva` para impedir uma reserva quando `data_checkout <= data_checkin`.

Crie `trg_validar_datas_reserva` como `BEFORE INSERT OR UPDATE` em `reserva`.

---

# Parte V — Criando Triggers de Auditoria

## Exercício 17

Crie a tabela `auditoria_status_reserva` com:

- `id_auditoria`
- `id_reserva`
- `status_anterior`
- `status_novo`
- `data_alteracao`

Crie `fn_auditar_status_reserva` usando `OLD.status` e `NEW.status`, registrando apenas mudanças reais de status.

Crie `trg_auditar_status_reserva` como `AFTER UPDATE OF status` em `reserva`.

## Exercício 18

Teste a trigger anterior alterando o status de uma reserva. Depois consulte `auditoria_status_reserva`.

## Exercício 19

Crie uma tabela `auditoria_valor_diaria` com id da auditoria, id do tipo, valor anterior, valor novo e data da alteração.

Crie uma função e uma trigger para registrar alterações em `tipo_quarto.valor_diaria`.

A trigger deve executar apenas após atualização de `valor_diaria`.

---

# Parte VI — Triggers para INSERT e DELETE sem TG_OP

## Exercício 20

Crie `fn_auditar_nova_reserva` para registrar, após um `INSERT` em `reserva`:

- id da reserva
- id do hóspede
- id do quarto
- valor total
- data da criação

Crie `trg_auditar_nova_reserva` como `AFTER INSERT`.

Use somente `NEW`.

## Exercício 21

Crie uma função separada `fn_auditar_exclusao_reserva` para registrar, após `DELETE`:

- id da reserva excluída
- status anterior
- valor anterior
- data da exclusão

Crie `trg_auditar_exclusao_reserva` como `AFTER DELETE`.

Use somente `OLD`.

> Não use a mesma função dos exercícios de INSERT e DELETE.

---

# Parte VII — Trigger Condicional com WHEN

## Exercício 22

Crie `fn_notificar_reserva_alto_valor` para inserir uma notificação.

Crie `trg_notificar_reserva_alto_valor` como `AFTER INSERT` somente quando `NEW.valor_total > 2000`, usando `WHEN`.

## Exercício 23

Crie `fn_notificar_cancelamento_aluno` para inserir uma notificação quando uma reserva mudar para `Cancelada`.

Crie `trg_notificar_cancelamento_aluno` como `AFTER UPDATE OF status` usando `WHEN` com `OLD.status` e `NEW.status`.

---
