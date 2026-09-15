# Estudo Guiado de Revisão — SQL e CRUD
## Contexto: Sistema de Reservas de Hotel

## Objetivo

Este estudo guiado reúne os conteúdos trabalhados nas atividades anteriores de SQL e CRUD, agora utilizando um **sistema de reservas de hotel** como contexto único para toda a revisão.

Ao todo, a lista possui **50 exercícios**, distribuídos entre:

- consultas básicas;
- seleção e expressões lógicas;
- tratamento de `NULL`;
- `LIKE`, `UPPER` e `LOWER`;
- consultas com múltiplas tabelas;
- `INNER JOIN`, `LEFT JOIN` e `RIGHT JOIN`;
- aliases;
- expressões calculadas;
- `DISTINCT`;
- `GROUP BY`;
- `COUNT`, `SUM` e `AVG`;
- `HAVING`;
- `ORDER BY`;
- `UNION`, `UNION ALL` e `INTERSECT`;
- subconsultas;
- CRUD com PostgreSQL;
- integridade referencial.

Utilize o arquivo:

```text
banco_hotel_reservas_postgresql.sql
```

O banco principal utilizado na atividade possui as tabelas:

```text
tipo_quarto
quarto
hospede
reserva
funcionario
```

Os principais relacionamentos são:

```text
tipo_quarto 1 ----- N quarto
hospede     1 ----- N reserva
quarto      1 ----- N reserva

funcionario 1 ----- N funcionario
             supervisor
```

A tabela `funcionario` possui um autorrelacionamento: um funcionário pode possuir outro funcionário como supervisor.

> O objetivo desta revisão não é apenas memorizar sintaxe. Antes de escrever SQL, identifique **quais dados precisam aparecer**, **de quais tabelas eles vêm**, **como essas tabelas se relacionam** e **quais condições determinam o resultado**.

---

# Parte I — SELECT, projeção, seleção e expressões lógicas

## 1. Contextualização

O comando `SELECT` é utilizado para consultar dados.

Sua forma básica é:

```sql
SELECT coluna1, coluna2
FROM tabela;
```

Para recuperar todas as colunas:

```sql
SELECT *
FROM tabela;
```

A escolha das colunas que aparecerão no resultado é chamada de **projeção**.

Por exemplo:

```sql
SELECT numero, andar, status
FROM quarto;
```

A tabela `quarto` possui outras informações, mas apenas essas três colunas aparecem no resultado.

---

## 2. Seleção com WHERE

A cláusula `WHERE` determina quais linhas permanecem no resultado.

```sql
SELECT *
FROM quarto
WHERE status = 'Disponível';
```

Podemos utilizar operadores relacionais:

```text
=
<>
!=
>
<
>=
<=
```

e operadores lógicos:

```text
AND
OR
NOT
```

Exemplo:

```sql
SELECT *
FROM tipo_quarto
WHERE capacidade >= 3
  AND valor_diaria < 600;
```

Com `OR`:

```sql
WHERE status = 'Disponível'
   OR status = 'Manutenção'
```

Parênteses ajudam a explicitar a ordem das condições:

```sql
WHERE andar >= 2
  AND (status = 'Disponível' OR status = 'Ocupado')
```

---

## 3. Valores NULL

`NULL` representa ausência de valor.

No banco do hotel, alguns hóspedes não possuem telefone informado e alguns quartos não possuem informação de vista.

Não devemos escrever:

```sql
telefone = NULL
```

O correto é:

```sql
telefone IS NULL
```

ou:

```sql
telefone IS NOT NULL
```

---

## 4. UPPER e LOWER

Podemos normalizar temporariamente uma cadeia de caracteres:

```sql
SELECT *
FROM hospede
WHERE LOWER(cidade) = 'curitiba';
```

Assim, valores como `Curitiba` e `CURITIBA` podem ser encontrados pela mesma consulta.

---

## 5. LIKE

`LIKE` permite comparar textos com padrões.

```text
%  → qualquer sequência de caracteres
_  → exatamente um caractere
```

Exemplos:

```sql
WHERE nome LIKE 'A%'
```

Nomes iniciados por `A`.

```sql
WHERE nome LIKE '%a%'
```

Nomes contendo `a`.

```sql
WHERE numero LIKE '___'
```

Número de quarto com exatamente três caracteres.

---

# Exercícios — Parte I

## Exercício 1

Liste o identificador, o número, o andar e o status de todos os quartos.

---

## Exercício 2

Liste os hóspedes da cidade de `Curitiba`.

Apresente:

- id;
- nome;
- cidade.

---

## Exercício 3

Liste os tipos de quarto cuja diária seja superior a `300.00`.

Apresente:

- nome do tipo;
- valor da diária;
- capacidade.

---

## Exercício 4

Liste os tipos de quarto que:

- tenham capacidade para pelo menos `2` pessoas;
- possuam diária maior ou igual a `400.00`.

---

## Exercício 5

Liste quartos cujo status seja `Disponível` ou `Ocupado`, mas apenas aqueles localizados a partir do terceiro andar.

Utilize `AND`, `OR` e parênteses.

---

## Exercício 6

Liste os hóspedes que não possuem telefone informado.

Depois, escreva outra consulta que liste somente hóspedes com telefone informado.

---

## Exercício 7

Liste hóspedes de `Curitiba`, independentemente de a cidade estar armazenada com letras maiúsculas ou minúsculas.

Utilize `LOWER` ou `UPPER`.

---

## Exercício 8

Liste hóspedes cujo nome comece com a letra `A`.

Apresente id, nome e cidade.

---

## Exercício 9

Liste tipos de quarto cujo nome contenha a letra `a`.

Depois modifique a consulta para buscar hóspedes cujo nome termine com `a`.

---

## Exercício 10

Liste reservas que:

- estejam com status `Confirmada` ou `Concluída`;
- possuam pelo menos 2 hóspedes;
- tenham valor total superior a `500.00`.

---

# Parte II — Consultas com múltiplas tabelas e JOIN

## 6. Por que combinar tabelas?

Em um banco relacional, informações relacionadas ficam separadas.

A tabela `quarto`, por exemplo, possui:

```text
id_tipo
```

mas o nome da categoria está em:

```text
tipo_quarto
```

Para obter:

```text
301 | Luxo
```

precisamos combinar as tabelas.

---

## 7. INNER JOIN

`INNER JOIN` mantém somente linhas que possuem correspondência nas duas tabelas.

```sql
SELECT
    q.numero,
    t.nome_tipo
FROM quarto AS q
INNER JOIN tipo_quarto AS t
    ON q.id_tipo = t.id_tipo;
```

A cláusula `ON` define como as tabelas se relacionam.

---

## 8. LEFT JOIN

`LEFT JOIN` preserva todas as linhas da tabela à esquerda.

```sql
SELECT
    h.nome,
    r.id_reserva
FROM hospede AS h
LEFT JOIN reserva AS r
    ON h.id_hospede = r.id_hospede;
```

Hóspedes sem reserva continuam aparecendo, com dados da reserva como `NULL`.

Pergunta útil:

> Qual conjunto precisa obrigatoriamente aparecer completo?

Se a resposta for "todos os hóspedes", `hospede` deve estar do lado preservado da junção.

---

## 9. RIGHT JOIN

`RIGHT JOIN` preserva todas as linhas da tabela à direita.

```sql
FROM quarto AS q
RIGHT JOIN tipo_quarto AS t
    ON q.id_tipo = t.id_tipo
```

Uma consulta com `RIGHT JOIN` pode frequentemente ser reescrita invertendo as tabelas e usando `LEFT JOIN`.

---

## 10. Encontrando registros sem correspondência

Uma aplicação importante de `LEFT JOIN` é localizar registros sem relacionamento.

Exemplo:

```sql
SELECT
    h.id_hospede,
    h.nome
FROM hospede AS h
LEFT JOIN reserva AS r
    ON h.id_hospede = r.id_hospede
WHERE r.id_reserva IS NULL;
```

Essa consulta encontra hóspedes que nunca fizeram reserva.

---

## 11. Múltiplos JOIN

Podemos combinar diversas tabelas:

```sql
SELECT
    h.nome,
    q.numero,
    t.nome_tipo,
    r.data_checkin
FROM reserva AS r
INNER JOIN hospede AS h
    ON r.id_hospede = h.id_hospede
INNER JOIN quarto AS q
    ON r.id_quarto = q.id_quarto
INNER JOIN tipo_quarto AS t
    ON q.id_tipo = t.id_tipo;
```

Visualize o caminho:

```text
hospede
   |
reserva
   |
quarto
   |
tipo_quarto
```

---

## 12. ON e WHERE em junções externas

Em `LEFT JOIN`, posicionar um filtro no `ON` ou no `WHERE` pode alterar o resultado.

Por exemplo:

```sql
FROM hospede AS h
LEFT JOIN reserva AS r
    ON h.id_hospede = r.id_hospede
   AND r.status = 'Confirmada'
```

preserva todos os hóspedes.

Já:

```sql
WHERE r.status = 'Confirmada'
```

pode remover hóspedes sem reservas confirmadas.

---

# Exercícios — Parte II

## Exercício 11

Liste o número de cada quarto e o nome de seu tipo.

Mostre apenas quartos que possuam um tipo cadastrado.

---

## Exercício 12

Para cada reserva, mostre:

- hóspede;
- número do quarto;
- data de check-in;
- data de check-out.

Use `INNER JOIN`.

---

## Exercício 13

Liste as reservas realizadas em quartos do tipo `Luxo`.

Apresente:

- hóspede;
- quarto;
- tipo;
- valor total.

---

## Exercício 14

Liste todos os hóspedes e, quando houver, suas reservas.

Hóspedes sem reserva também devem aparecer.

---

## Exercício 15

Liste todos os quartos e suas reservas.

Quartos nunca reservados devem permanecer no resultado.

---

## Exercício 16

Liste apenas hóspedes que nunca realizaram uma reserva.

Use `LEFT JOIN` e `IS NULL`.

---

## Exercício 17

Liste todos os tipos de quarto e os quartos associados.

Tipos que não possuem nenhum quarto cadastrado também devem aparecer.

---

## Exercício 18

Liste apenas quartos que nunca foram utilizados em nenhuma reserva.

Apresente:

- id;
- número;
- andar;
- status.

---

## Exercício 19

Liste todos os tipos de quarto e os quartos associados.

Tipos sem quartos também devem aparecer.

Resolva primeiro com `LEFT JOIN`.

Depois reescreva utilizando `RIGHT JOIN`.

---

## Exercício 20

Crie um relatório contendo:

- hóspede;
- número do quarto;
- tipo do quarto;
- check-in;
- check-out;
- status da reserva.

Todos os hóspedes devem aparecer, inclusive aqueles que nunca reservaram um quarto.

---

# Parte III — Aliases, DISTINCT e expressões calculadas

## 13. Aliases

Aliases são nomes temporários.

Para tabelas:

```sql
FROM hospede AS h
```

Para colunas:

```sql
SELECT h.nome AS hospede
```

Eles ajudam quando:

- há várias tabelas;
- nomes são longos;
- expressões calculadas precisam de nomes;
- a mesma tabela aparece mais de uma vez.

---

## 14. DISTINCT

Para eliminar valores repetidos:

```sql
SELECT DISTINCT cidade
FROM hospede;
```

Use `DISTINCT` quando a duplicidade não fizer sentido para o resultado.

---

## 15. Colunas calculadas

No PostgreSQL, a diferença entre duas datas retorna a quantidade de dias.

Assim, podemos calcular a quantidade de diárias:

```sql
SELECT
    id_reserva,
    data_checkout - data_checkin AS quantidade_diarias
FROM reserva;
```

Também podemos calcular um valor estimado:

```sql
(data_checkout - data_checkin) * t.valor_diaria
```

---

## 16. Autorrelacionamento

Na tabela `funcionario`, um supervisor também é um funcionário.

Por isso, podemos utilizar a mesma tabela duas vezes:

```sql
SELECT
    f.nome AS funcionario,
    s.nome AS supervisor
FROM funcionario AS f
INNER JOIN funcionario AS s
    ON f.id_supervisor = s.id_funcionario;
```

Os aliases distinguem os papéis.

---

# Exercícios — Parte III

## Exercício 21

Liste todas as cidades dos hóspedes sem valores duplicados.

---

## Exercício 22

Para cada tipo de quarto, apresente:

- nome;
- valor da diária;
- valor estimado de uma estadia de 7 dias.

Dê à coluna calculada o alias:

```text
valor_semana
```

---

## Exercício 23

Para cada reserva, mostre:

- hóspede;
- número do quarto;
- quantidade de diárias;
- valor total;
- valor médio por diária.

Utilize expressões calculadas e aliases.

---

## Exercício 24

Utilize os aliases `h`, `r` e `q` para consultar:

- nome do hóspede;
- número do quarto;
- valor total.

Mostre apenas reservas com valor superior a `1000.00`.

---

## Exercício 25

Liste os estados dos hóspedes sem valores duplicados.

Depois explique por que `DISTINCT` altera a quantidade de linhas do resultado.

---

## Exercício 26

Utilizando a tabela `funcionario`, apresente:

- nome do funcionário;
- cargo;
- nome do supervisor.

Use a tabela `funcionario` duas vezes.

---

# Parte IV — Agrupamento e funções de agregação

## 17. Funções de agregação

As principais funções utilizadas são:

```text
COUNT → quantidade
SUM   → soma
AVG   → média
```

Exemplo:

```sql
SELECT COUNT(*)
FROM reserva;
```

---

## 18. GROUP BY

Para resumir reservas por hóspede:

```sql
SELECT
    id_hospede,
    COUNT(*) AS quantidade
FROM reserva
GROUP BY id_hospede;
```

Cada hóspede forma um grupo.

Uma regra prática:

> Colunas do `SELECT` que não participam de funções de agregação normalmente precisam aparecer no `GROUP BY`.

---

## 19. COUNT e LEFT JOIN

Em consultas com `LEFT JOIN`, existe diferença entre:

```sql
COUNT(*)
```

e:

```sql
COUNT(r.id_reserva)
```

Para um hóspede sem reservas, `COUNT(r.id_reserva)` retorna `0`, pois valores `NULL` não são contados.

---

## 20. HAVING

`WHERE` filtra linhas antes do agrupamento.

`HAVING` filtra grupos depois da agregação.

```sql
SELECT
    id_hospede,
    COUNT(*) AS quantidade
FROM reserva
GROUP BY id_hospede
HAVING COUNT(*) >= 2;
```

---

## 21. ORDER BY

`ORDER BY` organiza o resultado:

```sql
ORDER BY quantidade DESC
```

Podemos combinar critérios:

```sql
ORDER BY quantidade DESC, nome ASC
```

---

# Exercícios — Parte IV

## Exercício 27

Conte quantas reservas existem no banco.

---

## Exercício 28

Mostre a quantidade de reservas realizadas por cada hóspede que possui pelo menos uma reserva.

---

## Exercício 29

Mostre todos os hóspedes e a quantidade de reservas de cada um.

Hóspedes sem reservas devem aparecer com quantidade `0`.

---

## Exercício 30

Para cada tipo de quarto, mostre:

- nome do tipo;
- quantidade de reservas realizadas em quartos desse tipo.

---

## Exercício 31

Para cada hóspede que possui reservas, mostre:

- nome;
- quantidade de reservas;
- total gasto.

---

## Exercício 32

Para cada hóspede, mostre:

- nome;
- quantidade de reservas;
- total gasto;
- média de valor das reservas.

Inclua hóspedes sem reservas.

Ordene pelo total gasto, do maior para o menor.

---

## Exercício 33

Liste apenas hóspedes que possuem duas ou mais reservas.

Use:

- `JOIN`;
- `GROUP BY`;
- `COUNT`;
- `HAVING`.

---

## Exercício 34

Liste os tipos de quarto que aparecem em pelo menos duas reservas.

Apresente:

- tipo;
- quantidade de reservas;
- total faturado;
- média do valor das reservas.

Ordene da maior para a menor quantidade.

---

## Exercício 35

Para cada tipo de quarto, apresente:

- nome do tipo;
- quantidade de quartos cadastrados;
- quantidade total de reservas feitas nesses quartos.

Tipos sem quartos também devem aparecer.

Evite contar o mesmo quarto várias vezes devido às reservas.

---

# Parte V — Operações de conjunto e subconsultas

## 22. UNION e UNION ALL

`UNION` combina resultados e elimina duplicatas.

```sql
SELECT ...
UNION
SELECT ...
```

`UNION ALL` preserva duplicatas.

As consultas devem retornar:

- a mesma quantidade de colunas;
- tipos compatíveis.

---

## 23. INTERSECT

`INTERSECT` retorna valores presentes nas duas consultas.

Exemplo de pergunta:

> Quais hóspedes já reservaram tanto quartos Standard quanto quartos Luxo?

---

## 24. Subconsultas

Uma subconsulta pode funcionar como uma tabela temporária:

```sql
SELECT ...
FROM (
    SELECT ...
    FROM reserva
    WHERE ...
) AS reservas_filtradas;
```

Também pode aparecer em condições:

```sql
WHERE id_hospede IN (
    SELECT ...
)
```

ou:

```sql
WHERE id_hospede NOT IN (
    SELECT ...
)
```

---

# Exercícios — Parte V

## Exercício 36

Crie uma única lista contendo:

- cidades de hóspedes que reservaram quartos `Standard`;
- cidades de hóspedes que reservaram quartos `Luxo`.

Primeiro utilize `UNION ALL`.

Depois utilize `UNION` e compare os resultados.

---

## Exercício 37

Crie uma lista única com os nomes de hóspedes que possuem reservas `Concluída` e os hóspedes que possuem reservas `Confirmada`.

Elimine duplicatas com `UNION`.

---

## Exercício 38

Liste hóspedes que já realizaram reserva em quarto `Standard` e também em quarto `Luxo`.

Utilize `INTERSECT`.

---

## Exercício 39

Crie uma subconsulta no `FROM` que selecione reservas cujo valor total seja igual ou superior a `1000.00`.

Utilize o resultado para mostrar:

- hóspede;
- número do quarto;
- valor total.

---

## Exercício 40

Liste os hóspedes que realizaram pelo menos uma reserva em quarto do tipo `Luxo`.

Resolva utilizando uma subconsulta.

Cada hóspede deve aparecer apenas uma vez.

---

## Exercício 41

Liste hóspedes que **nunca** reservaram um quarto do tipo `Luxo`.

Utilize uma subconsulta com `NOT IN` ou uma estratégia equivalente.

---

## Exercício 42

Calcule o total gasto por hóspede.

Depois utilize essa consulta como subconsulta para listar somente hóspedes cujo total gasto seja superior à média dos totais gastos pelos hóspedes que possuem reservas.

---

# Parte VI — CRUD com PostgreSQL

## 25. O conceito de CRUD

CRUD representa:

```text
Create → INSERT
Read   → SELECT
Update → UPDATE
Delete → DELETE
```

Exemplo de cadastro:

```sql
INSERT INTO hospede
(id_hospede, nome, email, cidade, estado, telefone)
VALUES
(20, 'Marcos Silva', 'marcos@email.com', 'Curitiba', 'PR', '41999990020');
```

Consulta:

```sql
SELECT *
FROM hospede
WHERE id_hospede = 20;
```

Atualização:

```sql
UPDATE hospede
SET cidade = 'Londrina'
WHERE id_hospede = 20;
```

Exclusão:

```sql
DELETE FROM hospede
WHERE id_hospede = 20;
```

---

## 26. INSERT

Uma forma recomendada é informar as colunas explicitamente.

Também é possível inserir várias linhas:

```sql
INSERT INTO hospede
(id_hospede, nome, email, cidade, estado, telefone)
VALUES
(...),
(...),
(...);
```

---

## 27. UPDATE

Estrutura:

```sql
UPDATE tabela
SET coluna = valor
WHERE condição;
```

Mais de uma coluna:

```sql
UPDATE hospede
SET
    cidade = 'Curitiba',
    estado = 'PR'
WHERE id_hospede = 20;
```

Com expressão:

```sql
UPDATE tipo_quarto
SET valor_diaria = valor_diaria * 1.08
WHERE valor_diaria < 400;
```

### Cuidado

Sem `WHERE`, todas as linhas podem ser atualizadas.

Antes:

```sql
SELECT *
FROM tipo_quarto
WHERE valor_diaria < 400;
```

Depois, execute o `UPDATE`.

---

## 28. DELETE

Estrutura:

```sql
DELETE FROM tabela
WHERE condição;
```

Uma estratégia segura é usar primeiro:

```sql
SELECT *
FROM tabela
WHERE condição;
```

e só depois realizar a exclusão.

---

## 29. Integridade referencial

Uma reserva referencia:

```text
hospede
quarto
```

Portanto, o PostgreSQL não deve permitir uma reserva apontando para um hóspede ou quarto inexistente.

Da mesma forma, um hóspede com reservas associadas não pode ser excluído diretamente enquanto as reservas existirem, considerando as restrições definidas neste banco.

---

# Exercícios — Parte VI

## Exercício 43

Cadastre um novo hóspede no PostgreSQL.

Depois utilize `SELECT` para confirmar o cadastro.

---

## Exercício 44

Cadastre três novos quartos utilizando um único `INSERT`.

Utilize tipos de quarto já existentes.

Depois consulte somente os registros recém-inseridos.

---

## Exercício 45

Escolha um hóspede de teste e execute:

1. `SELECT` antes da alteração;
2. `UPDATE` da cidade;
3. `SELECT` depois da alteração.

---

## Exercício 46

Aumente em 10% o valor da diária de todos os tipos de quarto cujo valor atual seja inferior a `400.00`.

Antes do `UPDATE`, execute um `SELECT` com a mesma condição.

---

## Exercício 47

Cadastre um hóspede temporário.

Depois:

1. consulte;
2. exclua com `DELETE`;
3. consulte novamente para confirmar a remoção.

---

## Exercício 48

Tente cadastrar uma reserva utilizando um `id_hospede` inexistente.

Registre:

1. o comando executado;
2. o erro produzido pelo PostgreSQL;
3. por que a chave estrangeira impede a operação.