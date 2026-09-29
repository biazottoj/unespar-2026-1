# Atividade – 20 exercícios sobre INNER, LEFT e RIGHT JOIN

## Contexto

A atividade utiliza um banco de dados simplificado de uma **plataforma de streaming**.

O banco possui as tabelas:

- `plano`;
- `usuario`;
- `conteudo`;
- `visualizacao`.

Utilize o arquivo `banco_streaming_joins_20_exercicios_programiz.sql` no **Programiz** antes de iniciar os exercícios.

## Objetivos

Ao final da atividade, espera-se que você consiga:

- utilizar `INNER JOIN` para recuperar somente registros com correspondência;
- utilizar `LEFT JOIN` para preservar todos os registros da tabela à esquerda;
- utilizar `RIGHT JOIN` para preservar todos os registros da tabela à direita;
- combinar três ou mais tabelas;
- identificar registros sem correspondência usando `IS NULL`;
- compreender a diferença entre filtros aplicados no `ON` e no `WHERE`;
- utilizar aliases para melhorar a legibilidade das consultas.

> As tabelas apresentadas em **Resposta esperada** mostram apenas o resultado que sua consulta deve produzir. A consulta SQL não é fornecida, para que você possa construí-la.

> **Observação sobre RIGHT JOIN:** versões modernas do SQLite suportam `RIGHT JOIN`. Caso a instância do Programiz utilizada em aula não aceite essa sintaxe, a mesma lógica pode ser obtida invertendo as tabelas e usando `LEFT JOIN`.

---

## Questão 1 — Básico

**Tipo de JOIN a praticar:** `INNER JOIN`

Liste o nome de cada usuário e o nome do seu plano. Mostre apenas usuários que possuem um plano associado.

### Resposta esperada

| usuario | plano |
| --- | --- |
| Ana | Padrão |
| Bruno | Premium |
| Carla | Básico |
| Elisa | Padrão |
| Fábio | Premium |
| Gabriela | Família |

## Questão 2 — Básico

**Tipo de JOIN a praticar:** `INNER JOIN`

Liste o nome dos usuários e o preço mensal de seus respectivos planos.

### Resposta esperada

| usuario | preco_mensal |
| --- | --- |
| Ana | 39.90 |
| Bruno | 54.90 |
| Carla | 24.90 |
| Elisa | 39.90 |
| Fábio | 54.90 |
| Gabriela | 69.90 |

## Questão 3 — Básico

**Tipo de JOIN a praticar:** `INNER JOIN`

Para cada visualização, mostre o nome do usuário e o título do conteúdo assistido.

### Resposta esperada

| usuario | conteudo |
| --- | --- |
| Ana | Horizonte Perdido |
| Ana | Código Fantasma |
| Bruno | Horizonte Perdido |
| Carla | Receita de Família |
| Elisa | Última Estação |
| Elisa | Horizonte Perdido |
| Bruno | Oceano Azul |
| Gabriela | Cidade Invisível |
| Ana | Oceano Azul |

## Questão 4 — Básico

**Tipo de JOIN a praticar:** `INNER JOIN`

Mostre o nome do usuário, o título do conteúdo e a data da visualização para todas as visualizações realizadas.

### Resposta esperada

| usuario | conteudo | data_visualizacao |
| --- | --- | --- |
| Ana | Horizonte Perdido | 2026-08-20 |
| Ana | Código Fantasma | 2026-08-21 |
| Bruno | Horizonte Perdido | 2026-08-22 |
| Carla | Receita de Família | 2026-08-22 |
| Elisa | Última Estação | 2026-08-23 |
| Elisa | Horizonte Perdido | 2026-08-24 |
| Bruno | Oceano Azul | 2026-08-24 |
| Gabriela | Cidade Invisível | 2026-08-25 |
| Ana | Oceano Azul | 2026-08-25 |

## Questão 5 — Básico

**Tipo de JOIN a praticar:** `INNER JOIN`

Liste apenas as visualizações de conteúdos do tipo Filme. Mostre usuário, título e minutos assistidos.

### Resposta esperada

| usuario | conteudo | minutos_assistidos |
| --- | --- | --- |
| Ana | Horizonte Perdido | 118 |
| Bruno | Horizonte Perdido | 80 |
| Carla | Receita de Família | 102 |
| Elisa | Horizonte Perdido | 118 |

## Questão 6 — Intermediário

**Tipo de JOIN a praticar:** `LEFT JOIN`

Liste todos os usuários e o nome de seu plano. Usuários sem plano também devem aparecer.

### Resposta esperada

| usuario | plano |
| --- | --- |
| Ana | Padrão |
| Bruno | Premium |
| Carla | Básico |
| Diego | NULL |
| Elisa | Padrão |
| Fábio | Premium |
| Gabriela | Família |

## Questão 7 — Intermediário

**Tipo de JOIN a praticar:** `LEFT JOIN`

Liste todos os usuários e suas visualizações. Mostre nome do usuário, id da visualização e data. Usuários sem visualizações devem permanecer no resultado.

### Resposta esperada

| usuario | id_visualizacao | data_visualizacao |
| --- | --- | --- |
| Ana | 1 | 2026-08-20 |
| Ana | 2 | 2026-08-21 |
| Ana | 9 | 2026-08-25 |
| Bruno | 3 | 2026-08-22 |
| Bruno | 7 | 2026-08-24 |
| Carla | 4 | 2026-08-22 |
| Diego | NULL | NULL |
| Elisa | 5 | 2026-08-23 |
| Elisa | 6 | 2026-08-24 |
| Fábio | NULL | NULL |
| Gabriela | 8 | 2026-08-25 |

## Questão 8 — Intermediário

**Tipo de JOIN a praticar:** `LEFT JOIN`

Liste os usuários que nunca realizaram uma visualização.

### Resposta esperada

| id_usuario | nome |
| --- | --- |
| 4 | Diego |
| 6 | Fábio |

## Questão 9 — Intermediário

**Tipo de JOIN a praticar:** `LEFT JOIN`

Liste todos os conteúdos e, quando houver, o id da visualização associada. Conteúdos nunca assistidos também devem aparecer.

### Resposta esperada

| id_conteudo | titulo | id_visualizacao |
| --- | --- | --- |
| 101 | Horizonte Perdido | 1 |
| 101 | Horizonte Perdido | 3 |
| 101 | Horizonte Perdido | 6 |
| 102 | Código Fantasma | 2 |
| 103 | Receita de Família | 4 |
| 104 | Última Estação | 5 |
| 105 | Oceano Azul | 7 |
| 105 | Oceano Azul | 9 |
| 106 | Jogo de Poder | NULL |
| 107 | Cidade Invisível | 8 |
| 108 | Som do Tempo | NULL |

## Questão 10 — Intermediário

**Tipo de JOIN a praticar:** `LEFT JOIN`

Liste os conteúdos que nunca foram visualizados.

### Resposta esperada

| id_conteudo | titulo |
| --- | --- |
| 106 | Jogo de Poder |
| 108 | Som do Tempo |

## Questão 11 — Intermediário

**Tipo de JOIN a praticar:** `RIGHT JOIN`

Utilizando RIGHT JOIN, liste todos os planos e os usuários associados. Planos sem usuários também devem aparecer.

### Resposta esperada

| plano | usuario |
| --- | --- |
| Básico | Carla |
| Padrão | Ana |
| Padrão | Elisa |
| Premium | Bruno |
| Premium | Fábio |
| Família | Gabriela |
| Estudante | NULL |

## Questão 12 — Intermediário

**Tipo de JOIN a praticar:** `RIGHT JOIN`

Utilizando RIGHT JOIN, liste todos os conteúdos e as visualizações associadas. Mostre título e id da visualização.

### Resposta esperada

| conteudo | id_visualizacao |
| --- | --- |
| Horizonte Perdido | 1 |
| Horizonte Perdido | 3 |
| Horizonte Perdido | 6 |
| Código Fantasma | 2 |
| Receita de Família | 4 |
| Última Estação | 5 |
| Oceano Azul | 7 |
| Oceano Azul | 9 |
| Jogo de Poder | NULL |
| Cidade Invisível | 8 |
| Som do Tempo | NULL |

## Questão 13 — Intermediário

**Tipo de JOIN a praticar:** `RIGHT JOIN`

Utilizando RIGHT JOIN, liste apenas os planos que não possuem nenhum usuário associado.

### Resposta esperada

| id_plano | nome_plano |
| --- | --- |
| 5 | Estudante |

## Questão 14 — Avançado

**Tipo de JOIN a praticar:** `INNER JOIN`

Mostre usuário, plano, conteúdo e data para cada visualização. Use INNER JOIN entre as quatro tabelas.

### Resposta esperada

| usuario | plano | conteudo | data_visualizacao |
| --- | --- | --- | --- |
| Ana | Padrão | Horizonte Perdido | 2026-08-20 |
| Ana | Padrão | Código Fantasma | 2026-08-21 |
| Bruno | Premium | Horizonte Perdido | 2026-08-22 |
| Carla | Básico | Receita de Família | 2026-08-22 |
| Elisa | Padrão | Última Estação | 2026-08-23 |
| Elisa | Padrão | Horizonte Perdido | 2026-08-24 |
| Bruno | Premium | Oceano Azul | 2026-08-24 |
| Gabriela | Família | Cidade Invisível | 2026-08-25 |
| Ana | Padrão | Oceano Azul | 2026-08-25 |

## Questão 15 — Avançado

**Tipo de JOIN a praticar:** `LEFT JOIN`

Crie um relatório com todos os usuários, seu plano e o título dos conteúdos assistidos. Usuários sem plano ou sem visualização devem continuar aparecendo.

### Resposta esperada

| usuario | plano | conteudo |
| --- | --- | --- |
| Ana | Padrão | Horizonte Perdido |
| Ana | Padrão | Código Fantasma |
| Ana | Padrão | Oceano Azul |
| Bruno | Premium | Horizonte Perdido |
| Bruno | Premium | Oceano Azul |
| Carla | Básico | Receita de Família |
| Diego | NULL | NULL |
| Elisa | Padrão | Última Estação |
| Elisa | Padrão | Horizonte Perdido |
| Fábio | Premium | NULL |
| Gabriela | Família | Cidade Invisível |

## Questão 16 — Avançado

**Tipo de JOIN a praticar:** `LEFT JOIN + ON`

Liste todos os usuários e apenas suas visualizações realizadas a partir de 24/08/2026. Usuários sem visualizações nesse período também devem aparecer. Coloque o filtro de data na cláusula ON.

### Resposta esperada

| usuario | data_visualizacao |
| --- | --- |
| Ana | 2026-08-25 |
| Bruno | 2026-08-24 |
| Carla | NULL |
| Diego | NULL |
| Elisa | 2026-08-24 |
| Fábio | NULL |
| Gabriela | 2026-08-25 |

## Questão 17 — Avançado

**Tipo de JOIN a praticar:** `LEFT JOIN`

Liste todos os planos e a cidade dos usuários associados. Planos sem usuários devem aparecer com cidade NULL.

### Resposta esperada

| plano | cidade |
| --- | --- |
| Básico | Curitiba |
| Padrão | Curitiba |
| Padrão | Londrina |
| Premium | Londrina |
| Premium | Cascavel |
| Família | Ponta Grossa |
| Estudante | NULL |

## Questão 18 — Avançado

**Tipo de JOIN a praticar:** `RIGHT JOIN`

Utilizando RIGHT JOIN, mostre todos os conteúdos do gênero Drama e, quando houver, o nome dos usuários que os visualizaram.

### Resposta esperada

| conteudo | usuario |
| --- | --- |
| Horizonte Perdido | Ana |
| Horizonte Perdido | Bruno |
| Horizonte Perdido | Elisa |
| Jogo de Poder | NULL |

## Questão 19 — Desafio

**Tipo de JOIN a praticar:** `LEFT JOIN`

Liste todos os conteúdos e, quando houver visualização, mostre também o usuário e o plano desse usuário. Conteúdos nunca visualizados devem permanecer no resultado.

### Resposta esperada

| conteudo | usuario | plano |
| --- | --- | --- |
| Horizonte Perdido | Ana | Padrão |
| Horizonte Perdido | Bruno | Premium |
| Horizonte Perdido | Elisa | Padrão |
| Código Fantasma | Ana | Padrão |
| Receita de Família | Carla | Básico |
| Última Estação | Elisa | Padrão |
| Oceano Azul | Bruno | Premium |
| Oceano Azul | Ana | Padrão |
| Jogo de Poder | NULL | NULL |
| Cidade Invisível | Gabriela | Família |
| Som do Tempo | NULL | NULL |

## Questão 20 — Desafio

**Tipo de JOIN a praticar:** `LEFT JOIN + GROUP BY`

Gere um relatório com todos os usuários e a quantidade de visualizações realizadas por cada um. Usuários sem visualizações devem aparecer com quantidade 0.

### Resposta esperada

| usuario | quantidade_visualizacoes |
| --- | --- |
| Ana | 3 |
| Bruno | 2 |
| Carla | 1 |
| Diego | 0 |
| Elisa | 2 |
| Fábio | 0 |
| Gabriela | 1 |
