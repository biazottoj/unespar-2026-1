# Atividade – SQL: Operações de Conjunto, Aliases, Expressões e Subconsultas

## Objetivo

Praticar os conceitos apresentados na parte final do Capítulo 7, com foco em:

- operações de conjunto (`UNION`, `UNION ALL`, `INTERSECT`);
- aliases de tabelas e colunas;
- colunas calculadas por expressões;
- uso da mesma tabela mais de uma vez em uma consulta;
- subconsultas utilizadas na cláusula `FROM`.

Utilize o banco de dados disponibilizado para o **Programiz/SQLite**.

---

## 1. Cidades em comum

Escreva uma consulta que mostre as cidades nas quais existe **pelo menos um fornecedor e pelo menos uma peça**.

Utilize uma operação de conjunto.

---

## 2. Todas as cidades, preservando repetições

Mostre todas as cidades presentes nas tabelas `fornecedor` e `peca`.

O resultado deve:

- incluir as cidades provenientes das duas tabelas;
- preservar valores repetidos;
- permitir a presença de `NULL`.

Utilize uma operação de conjunto adequada.

Depois, altere a consulta para que os valores duplicados sejam eliminados.

---

## 3. Aliases de tabelas

Utilizando os aliases `p` para `peca` e `e` para `embarque`, obtenha:

- código da peça;
- nome da peça;
- data do embarque;
- quantidade embarcada.

Considere apenas os embarques cuja quantidade seja superior a **70 unidades**.

---

## 4. Aliases de tabelas e colunas

Para cada embarque, mostre:

- nome do fornecedor;
- nome da peça;
- quantidade embarcada.

Utilize aliases para as três tabelas envolvidas:

- `f` para `fornecedor`;
- `p` para `peca`;
- `e` para `embarque`.

No resultado, renomeie as colunas para:

- `fornecedor`;
- `peca`;
- `quantidade`.

---

## 5. Coluna calculada por expressão

A coluna `peso_peca` armazena o peso das peças em quilogramas.

Crie uma consulta que mostre:

- código da peça;
- nome da peça;
- peso em quilogramas;
- peso em gramas.

A coluna calculada deve receber o alias:

`peso_gramas`

Considere que:

**1 kg = 1000 g**

---

## 6. Autorrelacionamento – empregado e chefe

A tabela `empregado` armazena tanto empregados quanto seus respectivos chefes.

Escreva uma consulta que apresente:

- nome do empregado;
- nome de seu chefe.

Utilize a tabela `empregado` **duas vezes** na cláusula `FROM`, atribuindo o alias `chefe` a uma delas.

Renomeie as colunas do resultado para:

- `empregado`;
- `chefe`.

---

## 7. Autorrelacionamento com dois níveis hierárquicos

Utilizando a tabela `empregado`, obtenha os empregados que possuem **chefe e chefe do chefe**.

O resultado deve apresentar:

- nome do empregado;
- nome do chefe;
- nome do chefe do chefe.

Para isso, será necessário utilizar a tabela `empregado` três vezes na mesma consulta.

Sugestão de aliases:

- `e` → empregado;
- `c` → chefe;
- `s` → superior do chefe.

---

## 8. Subconsulta na cláusula FROM

Crie inicialmente uma subconsulta que selecione apenas as peças cuja cor seja **Vermelho**.

A subconsulta deve retornar:

- `cod_peca`;
- `nome_peca`.

Em seguida, utilize o resultado dessa subconsulta como uma tabela temporária na cláusula `FROM` de uma consulta maior.

A consulta final deve mostrar, para cada embarque dessas peças:

- código da peça;
- nome da peça;
- código do fornecedor;
- data do embarque.

Atribua o alias `pecas_vermelhas` ao resultado da subconsulta.

---

## 9. Subconsulta na cláusula FROM – desafio

Crie uma subconsulta que identifique todos os fornecedores que realizaram embarques com quantidade **maior ou igual a 100 unidades**.

A subconsulta deve retornar apenas o código do fornecedor.

Depois, utilize o resultado dessa subconsulta na cláusula `FROM` para obter:

- código do fornecedor;
- nome do fornecedor;
- cidade do fornecedor.

O resultado final **não deve apresentar fornecedores duplicados**.

> Pense em qual ponto da consulta o uso de `DISTINCT` é mais adequado.
