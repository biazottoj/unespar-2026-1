# Lista de Exercícios — Transações e ACID no PostgreSQL

## Parte I — Conceitos básicos

### Exercício 1

Explique com suas palavras o que é uma **transação** em um banco de dados.

---

### Exercício 2

Explique a diferença entre:

```sql
COMMIT
```

e:

```sql
ROLLBACK
```

---

### Exercício 3

Explique o que significa **Atomicidade** no conjunto de propriedades ACID.

Use um exemplo relacionado ao sistema de reservas de hotel.

---

### Exercício 4

Explique o que significa **Consistência** em uma transação.

Relacione sua resposta com restrições como:

```text
PRIMARY KEY
FOREIGN KEY
CHECK
NOT NULL
```

---

### Exercício 5

Explique o que significa **Isolamento**.

Considere duas pessoas tentando reservar o mesmo quarto ao mesmo tempo.

---

### Exercício 6

Explique o que significa **Durabilidade**.

O que deve acontecer depois da execução de:

```sql
COMMIT;
```

---

## Parte II — BEGIN, COMMIT e ROLLBACK

### Exercício 7

Consulte o status de um quarto.

Depois:

1. inicie uma transação;
2. altere o status para `Manutenção`;
3. consulte o quarto;
4. execute `ROLLBACK`;
5. consulte novamente.

Explique o resultado.

---

### Exercício 8

Repita o exercício anterior, mas desta vez utilize:

```sql
COMMIT;
```

Explique a diferença observada.

---

### Exercício 9

Escolha uma reserva existente.

Dentro de uma transação:

1. altere o status da reserva para `Concluída`;
2. consulte a reserva;
3. execute `ROLLBACK`;
4. consulte novamente.

---

### Exercício 10

Crie uma transação que:

1. altere uma reserva para `Concluída`;
2. altere o quarto correspondente para `Disponível`;
3. confirme ambas as alterações com `COMMIT`.

---

### Exercício 11

Crie uma transação que execute dois `UPDATE`s.

Antes do `COMMIT`, execute consultas para verificar os valores alterados.

Depois execute:

```sql
ROLLBACK;
```

Explique quais valores permaneceram.

---

## Parte III — Erros dentro da transação

### Exercício 12

Inicie uma transação e execute:

1. um `UPDATE` válido;
2. um `UPDATE` que viole uma restrição `CHECK`.

Depois tente executar um `SELECT`.

Registre a mensagem exibida pelo PostgreSQL.

---

### Exercício 13

Após provocar um erro dentro de uma transação, execute:

```sql
ROLLBACK;
```

Depois execute novamente uma consulta válida.

Explique por que o `ROLLBACK` foi necessário.

---

### Exercício 14

Crie uma situação em que:

1. uma reserva seja alterada corretamente;
2. um segundo comando gere erro;
3. a transação seja desfeita.

Explique como esse comportamento demonstra **Atomicidade**.

---

### Exercício 15

Explique o significado da mensagem:

```text
current transaction is aborted
```

Quando ela aparece no PostgreSQL?

---

## Parte IV — SAVEPOINT

### Exercício 16

Crie uma transação com duas alterações.

Depois da primeira alteração:

```sql
SAVEPOINT etapa1;
```

Faça a segunda alteração e execute:

```sql
ROLLBACK TO SAVEPOINT etapa1;
```

Depois execute:

```sql
COMMIT;
```

Explique qual alteração permaneceu.

---

### Exercício 17

Crie uma transação com três `UPDATE`s e dois `SAVEPOINT`s.

Depois retorne ao primeiro `SAVEPOINT`.

Observe quais alterações foram desfeitas.

---

### Exercício 18

Utilize:

```sql
RELEASE SAVEPOINT
```

em uma transação.

Explique qual é a função desse comando.

---

### Exercício 19

Explique a diferença entre:

```sql
ROLLBACK;
```

e:

```sql
ROLLBACK TO SAVEPOINT nome;
```

---

## Parte V — Autocommit

### Exercício 20

Execute um `UPDATE` simples sem utilizar:

```sql
BEGIN;
```

Depois consulte o registro alterado.

Explique por que a alteração já está confirmada.

---

### Exercício 21

Explique o conceito de **autocommit**.

Qual é a diferença entre executar um comando normalmente e executar esse mesmo comando dentro de:

```sql
BEGIN;
...
COMMIT;
```

---

## Parte VI — Transações e triggers

### Exercício 22

Inicie uma transação e altere o status de uma reserva de forma que uma trigger de auditoria seja executada.

Consulte a tabela de auditoria.

Depois execute:

```sql
ROLLBACK;
```

Consulte novamente a auditoria.

Explique o resultado.

---

### Exercício 23

Explique por que uma operação executada por uma trigger normalmente faz parte da mesma transação que disparou a trigger.

---

### Exercício 24

Crie um teste em que:

1. uma trigger insira uma notificação;
2. a transação seja desfeita;
3. a notificação também desapareça.

Explique por que isso ocorre.

---

## Parte VII — Transações e procedures

### Exercício 25

Inicie uma transação.

Dentro dela, execute uma procedure que altere o status de um quarto.

Depois execute:

```sql
ROLLBACK;
```

Verifique o estado do quarto.

---

### Exercício 26

Explique por que executar:

```sql
CALL nome_procedure(...);
```

dentro de uma transação não significa necessariamente que as alterações serão confirmadas imediatamente.

---

## Parte VIII — Operações integradas

### Exercício 27

Crie uma tabela simples de pagamento:

```text
pagamento
```

com pelo menos:

- id do pagamento;
- id da reserva;
- valor;
- data do pagamento.

Depois crie uma transação que:

1. registre um pagamento;
2. conclua a reserva;
3. libere o quarto;
4. execute `COMMIT`.

---

### Exercício 28

Repita o exercício anterior, mas provoque um erro na terceira operação.

Depois execute:

```sql
ROLLBACK;
```

Verifique:

- pagamento;
- reserva;
- quarto.

Explique o resultado.

---

### Exercício 29

Considere o seguinte fluxo:

```text
Registrar pagamento
Atualizar reserva
Atualizar quarto
Registrar auditoria
```

Explique quais propriedades ACID são importantes nesse processo e por quê.

---

### Exercício 30 — Desafio integrador

Implemente uma operação completa de checkout utilizando uma transação.

A operação deve:

1. receber uma reserva existente;
2. registrar um pagamento;
3. alterar a reserva para `Concluída`;
4. alterar o quarto para `Disponível`;
5. consultar os dados antes do `COMMIT`;
6. confirmar a operação;
7. repetir o processo com outro registro, provocando um erro proposital;
8. executar `ROLLBACK`;
9. demonstrar que nenhuma alteração da segunda tentativa permaneceu.

Ao final, escreva uma breve explicação identificando onde aparecem:

```text
Atomicidade
Consistência
Isolamento
Durabilidade
BEGIN
COMMIT
ROLLBACK
SAVEPOINT
```

Entrega:

Entrega via link: [https://forms.gle/LUTv8RsoeVjrSdDeA](https://forms.gle/LUTv8RsoeVjrSdDeA)
Entrega até 27/10/2026
