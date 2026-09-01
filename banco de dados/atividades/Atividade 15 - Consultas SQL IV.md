# Atividade – Revisão Geral de Consultas SQL

## Contexto

Considere o banco de dados de uma plataforma de streaming com as tabelas `usuario`, `plano`, `conteudo` e `visualizacao`.

Utilize o arquivo `banco_streaming_revisao_sql_programiz.sql` no Programiz antes de iniciar.

## Objetivo

Cada exercício exige combinar vários recursos SQL em uma mesma consulta. Ao longo da lista, você deverá utilizar `SELECT`, `WHERE`, operadores lógicos, aliases, expressões, `DISTINCT`, `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `GROUP BY`, `COUNT`, `SUM`, `AVG`, `HAVING`, `ORDER BY`, `UNION`, `INTERSECT` e subconsultas.

## 1. Filmes longos assistidos por usuários com plano

Liste os usuários que assistiram a conteúdos do tipo `Filme` com duração superior a 100 minutos. Apresente nome do usuário, plano, título, duração e minutos assistidos. Use `INNER JOIN`, `WHERE`, `AND` e aliases.

## 2. Usuários sem visualizações

Liste todos os usuários que nunca realizaram uma visualização. Apresente nome, cidade e plano, quando houver. Usuários sem plano também devem aparecer. Use `LEFT JOIN`, `IS NULL` e junção com `plano`.

## 3. Quantidade de visualizações por plano

Para cada plano, mostre nome do plano, quantidade de usuários associados e quantidade total de visualizações feitas por esses usuários. Inclua planos sem usuários. Use múltiplos `LEFT JOIN`, `GROUP BY`, `COUNT(DISTINCT ...)` e `COUNT(...)`.

## 4. Usuários com alto consumo

Liste usuários cujo total de minutos assistidos seja superior a 150. Apresente usuário, plano, quantidade de visualizações e total de minutos. Use `INNER JOIN`, `GROUP BY`, `COUNT`, `SUM` e `HAVING`.

## 5. Gêneros populares

Liste gêneros com pelo menos duas visualizações. Apresente gênero, quantidade de visualizações, total de minutos e média de minutos. Use `JOIN`, `GROUP BY`, `COUNT`, `SUM`, `AVG`, `HAVING` e `ORDER BY`.

## 6. Conteúdos nunca assistidos

Liste conteúdos nunca visualizados, apresentando título, tipo, gênero e duração. Use `LEFT JOIN`, `IS NULL` e `ORDER BY` por duração decrescente.

## 7. Usuários que assistiram Drama

Liste usuários que assistiram pelo menos um conteúdo de `Drama`. Apresente nome, cidade e plano. Cada usuário deve aparecer uma vez. Use subconsulta, `JOIN` e `DISTINCT`.

## 8. Usuários que não assistiram Drama

Liste usuários que não possuem nenhuma visualização de conteúdos de `Drama`. Apresente nome, cidade e plano. Use subconsulta, `LEFT JOIN` e `NOT IN` ou estratégia equivalente.

## 9. Conteúdos assistidos por usuários Premium

Liste visualizações feitas por usuários do plano `Premium`, considerando apenas visualizações com pelo menos 50 minutos. Apresente usuário, conteúdo, plano, data e minutos. Use quatro tabelas, `INNER JOIN`, `WHERE` e `AND`.

## 10. Todos os usuários e seu consumo

Para cada usuário, apresente nome, plano, quantidade de visualizações e total de minutos assistidos. Todos os usuários devem aparecer. Use `LEFT JOIN`, `GROUP BY`, `COUNT` e `SUM`.

## 11. Planos sem usuários

Liste planos sem usuários associados, apresentando código, nome e preço mensal. Resolva com `RIGHT JOIN` ou `LEFT JOIN` equivalente e `IS NULL`.

## 12. Comparação entre duração e consumo

Liste visualizações em que o usuário assistiu menos de 70% da duração do conteúdo. Apresente usuário, conteúdo, duração, minutos assistidos e percentual assistido. Use `JOIN`, expressão calculada, alias e `WHERE`.

## 13. Usuários com diversidade de gêneros

Liste usuários que assistiram conteúdos de pelo menos dois gêneros diferentes. Apresente nome, quantidade de gêneros diferentes e quantidade total de visualizações. Use `JOIN`, `GROUP BY`, `COUNT(DISTINCT ...)`, `COUNT` e `HAVING`.

## 14. Conteúdos mais assistidos

Liste conteúdos com duas ou mais visualizações. Apresente título, tipo, gênero, quantidade de visualizações e total de minutos. Use `JOIN`, `GROUP BY`, `COUNT`, `SUM`, `HAVING` e `ORDER BY`.

## 15. Subconsulta no FROM

Crie uma subconsulta que selecione apenas visualizações com 60 minutos ou mais, retornando id do usuário, id do conteúdo e minutos assistidos. Use-a no `FROM` para mostrar nome do usuário, título, gênero e minutos. Use alias para a subconsulta e `JOIN`.

## 16. Usuários acima da média de consumo

Liste usuários cujo total de minutos seja superior à média do total de minutos por usuário. Apresente usuário e total. Use `GROUP BY`, `SUM`, `HAVING`, subconsulta e uma segunda agregação dentro da subconsulta.

## 17. Relatório por plano e cidade

Para cada combinação de plano e cidade, apresente plano, cidade, quantidade de usuários e quantidade total de visualizações. Inclua planos sem usuários. Use múltiplos `LEFT JOIN`, `GROUP BY`, `COUNT(DISTINCT ...)` e `COUNT(...)`.

## 18. Conteúdos de usuários de Curitiba e Londrina

Crie uma única lista com os títulos assistidos por usuários de Curitiba e os títulos assistidos por usuários de Londrina, sem duplicatas. Use `JOIN`, `WHERE` e `UNION`.

## 19. Conteúdos em comum entre Padrão e Premium

Identifique conteúdos assistidos por usuários do plano `Padrão` e também por usuários do plano `Premium`. Apresente apenas o título. Use duas consultas completas com `JOIN`, `WHERE` e `INTERSECT`.

## 20. Desafio integrador

Crie um relatório geral, com uma linha por usuário, contendo nome, cidade, plano, quantidade total de visualizações, quantidade de conteúdos diferentes, quantidade de gêneros diferentes, total de minutos e média de minutos por visualização. Inclua usuários sem plano e sem visualizações. Ordene da maior para a menor quantidade de visualizações e, em caso de empate, por nome. Use múltiplos `LEFT JOIN`, aliases, `GROUP BY`, `COUNT`, `COUNT(DISTINCT ...)`, `SUM`, `AVG` e `ORDER BY`.
