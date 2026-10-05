# Trabalho – Banco de Dados Aplicado às Práticas Extensionistas

**Valor:** 2,0 pontos  
**Data de entrega:** **19/10/2026**

## Objetivo

O objetivo deste trabalho é aplicar os conceitos de Banco de Dados estudados em aula em um contexto relacionado à disciplina de **Práticas Extensionistas**.

A partir desse contexto, deverá ser projetado e implementado um banco de dados capaz de armazenar informações relevantes e produzir consultas e relatórios que possam auxiliar a organização.

---

## Parte 1 – Modelagem e criação do banco de dados

Os alunos deverão desenvolver um banco de dados adequado ao contexto escolhido.

O banco deverá possuir tabelas suficientes para representar corretamente o problema.

O arquivo SQL deverá conter todos os comandos necessários para a criação do banco
e as **restrições necessárias para garantir a integridade dos dados**.

Devem ser utilizados, quando aplicáveis:

- `PRIMARY KEY`;
- `FOREIGN KEY`;
- `NOT NULL`;
- `UNIQUE`;
- `CHECK`;
- valores padrão com `DEFAULT`;
- tipos de dados adequados para cada atributo.

Os relacionamentos entre as tabelas deverão ser representados por meio de chaves estrangeiras.

---

## Parte 2 – População do banco

Deverá ser criado um segundo arquivo SQL contendo os comandos utilizados para popular o banco.

O banco deverá possuir **pelo menos 50 registros no total**, considerando a soma dos registros de todas as tabelas.

Por exemplo:

```text
Participante: 20 registros
Evento:       10 registros
Inscrição:    25 registros
---------------------------
Total:        55 registros
```

Os dados **podem ser fictícios**, desde que:

- sejam coerentes com o contexto escolhido;
- respeitem as restrições definidas nas tabelas;
- permitam executar adequadamente as consultas solicitadas.

A inserção deverá ser realizada utilizando comandos SQL, como:

```sql
INSERT INTO participante
(id_participante, nome, email)
VALUES
(1, 'Ana Silva', 'ana@email.com');
```

---

## Parte 3 – Consultas e relatórios

Os alunos deverão criar **pelo menos 10 consultas ou relatórios SQL diferentes** utilizando os dados armazenados.

As consultas devem devem explorar os diferentes recursos estudados durante a disciplina.

Ao longo das 10 consultas, devem aparecer recursos como:

- seleção com `WHERE`;
- múltiplas condições com `AND` e `OR`;
- `INNER JOIN`;
- `LEFT JOIN` ou `RIGHT JOIN`;
- consulta envolvendo três ou mais tabelas;
- funções de agregação:
  - `COUNT`;
  - `SUM`;
  - `AVG`;
  - `MIN`;
  - `MAX`;
- `GROUP BY`;
- `HAVING`;
- `ORDER BY`;
- `DISTINCT`;
- subconsultas;
- expressões calculadas;
- outros recursos SQL estudados em aula.

Cada consulta deverá representar uma **pergunta ou informação relevante para o contexto extensionista**.

Por exemplo:

> Qual o período médio de estadia dos hospedes no ultimo ano?

---

## Descrição das consultas

Para cada uma das 10 consultas, o aluno deverá apresentar:

**1. Pergunta ou objetivo da consulta**
**2. Código SQL**
**3. Resultado da consulta (print da tabela)**
**4. Breve explicação do resultado**

---

## Entrega

**Data: 19/10/2026.**

Os scripts entregues deverão ser executáveis no **PostgreSQL**. O banco deverá poder ser criado e populado a partir dos arquivos entregues, sem necessidade de criação manual das tabelas ou inserção manual dos dados.

**Entrgue um ZIP com todas os arquivos.**
**Link para entrega:** [https://forms.gle/UaXTJQkwVy74fAkUA](https://forms.gle/UaXTJQkwVy74fAkUA)
