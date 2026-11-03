# Atividade Prática — Índices no PostgreSQL

**Disciplina:** Banco de Dados  
**Contexto:** Sistema de Reservas de Hotel  
**Ambiente:** PostgreSQL via terminal (`psql`)

## 1. Objetivo

Nesta atividade, você investigará como os **índices** influenciam a execução de consultas no PostgreSQL. Em vez de apenas criar índices, você deverá **comparar os planos de execução antes e depois**, observar o impacto da seletividade e discutir os custos envolvidos.

Ao final, você deverá saber utilizar:

- `CREATE INDEX` e `DROP INDEX`;
- `EXPLAIN` e `EXPLAIN ANALYZE`;
- `ANALYZE`;
- índices simples, compostos, por expressão e parciais;
- comandos para listar e medir índices;
- conceitos de `Seq Scan`, `Index Scan`, seletividade e custo de manutenção.

> **Atenção:** criar um índice não garante que o PostgreSQL vá utilizá-lo. O plano depende da consulta, da distribuição dos dados e das estimativas do otimizador. Não existe um tempo ou plano exato que todos os computadores devam apresentar.

---

## 2. Preparação do ambiente

### 2.1. Acessar o banco

Entre no `psql` e conecte-se ao banco do hotel utilizado nas aulas anteriores. Por exemplo:

```bash
psql -U postgres -d hotel_triggers
```

Ou, se já estiver no `psql`:

```text
\c hotel_triggers
```

Para conferir as tabelas existentes:

```text
\dt
```

**Não altere nem apague os dados originais do hotel.** Todos os experimentos de desempenho serão realizados em tabelas com o prefixo `lab_`.

### 2.2. Criar uma tabela de laboratório

Execute o script a seguir **uma única vez**, no início da atividade. Ele recria somente a tabela didática `lab_reserva_indice` e insere **200.000 registros fictícios**.

```sql
DROP TABLE IF EXISTS lab_reserva_indice;

CREATE TABLE lab_reserva_indice (
    id_reserva BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_hospede INTEGER NOT NULL,
    id_quarto INTEGER NOT NULL,
    email_contato VARCHAR(150) NOT NULL,
    cidade VARCHAR(60) NOT NULL,
    status VARCHAR(20) NOT NULL,
    data_checkin DATE NOT NULL,
    valor_total NUMERIC(10,2) NOT NULL
);

INSERT INTO lab_reserva_indice (
    id_hospede,
    id_quarto,
    email_contato,
    cidade,
    status,
    data_checkin,
    valor_total
)
SELECT
    ((n - 1) % 400) + 1,
    ((n - 1) % 30) + 1,
    'cliente' || n || '@hotel.com',
    CASE (n % 4)
        WHEN 0 THEN 'Curitiba'
        WHEN 1 THEN 'Londrina'
        WHEN 2 THEN 'Maringá'
        ELSE 'Apucarana'
    END,
    CASE
        WHEN n % 100 = 0 THEN 'Cancelada'
        WHEN n % 100 < 56 THEN 'Confirmada'
        WHEN n % 100 < 90 THEN 'Concluída'
        ELSE 'Hospedada'
    END,
    DATE '2025-01-01' + ((n - 1) % 730),
    (100 + ((n * 7) % 1200))::NUMERIC(10,2)
FROM generate_series(1, 200000) AS g(n);

ANALYZE lab_reserva_indice;
```

> O campo `id_hospede` da tabela de laboratório é apenas um identificador fictício usado nos testes. Esta tabela **não precisa** ter chaves estrangeiras para as tabelas reais do hotel.

### 2.3. Como registrar as observações

Ative a medição de tempo no `psql`:

```text
\timing on
```

Para visualizar o plano de execução com informações reais:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM lab_reserva_indice
WHERE id_reserva = 150000;
```

Registre os seguintes elementos sempre que a questão solicitar comparação:

| Consulta | Índice existente? | Tipo de scan observado | Tempo de execução | Observações |
|---|---|---|---|---|
| Exemplo | Sim/Não | `Seq Scan`, `Index Scan` etc. | Valor mostrado pelo PostgreSQL | Quantidade de linhas, filtros, custo etc. |

**Importante:** `EXPLAIN ANALYZE` executa a consulta. Nesta atividade, utilize-o principalmente com `SELECT`. Em testes de desempenho, repita cada consulta algumas vezes e compare os resultados com cautela, pois cache e condições da máquina influenciam os tempos.

---

# Parte I — Reconhecimento e primeiros índices

## Exercício 1 — Inspeção do banco

No banco do hotel:

1. Liste as tabelas existentes.
2. Consulte a estrutura de `hospede` e `reserva`.
3. Identifique quais índices já existem por causa de `PRIMARY KEY` e `UNIQUE`.
4. Explique por que não faria sentido criar outro índice idêntico sobre uma chave primária.

## Exercício 2 — Conferência dos dados de teste

Na tabela `lab_reserva_indice`:

1. Conte os registros inseridos.
2. Descubra quantas cidades diferentes existem.
3. Conte quantas reservas existem em cada status.
4. Identifique a data de check-in mais antiga e a mais recente.

**Entrega:** apresente as consultas SQL e seus resultados.

## Exercício 3 — Índice criado pela chave primária

Execute:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM lab_reserva_indice
WHERE id_reserva = 150000;
```

1. Qual plano de execução foi escolhido?
2. Existe algum índice que pode ser utilizado nessa busca?
3. Quem criou esse índice?
4. Liste os índices da tabela e identifique o relacionado à chave primária.

## Exercício 4 — Busca sem índice adequado

Execute:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM lab_reserva_indice
WHERE email_contato = 'cliente85000@hotel.com';
```

Registre o tipo de scan e o tempo de execução. Explique por que o PostgreSQL pode precisar examinar muitas linhas.

## Exercício 5 — Criando o primeiro índice

Crie um índice B-tree sobre a coluna `email_contato`:

```sql
CREATE INDEX idx_lab_reserva_email
ON lab_reserva_indice(email_contato);

ANALYZE lab_reserva_indice;
```

Repita a consulta do Exercício 4.

1. O plano de execução mudou?
2. Qual índice apareceu no plano, se algum?
3. O tempo foi menor, maior ou semelhante?
4. Qual a principal justificativa para esse resultado?

## Exercício 6 — Comparação documentada

Execute três vezes a consulta do Exercício 5 e registre os tempos. Compare com o resultado obtido antes da criação do índice.

Explique por que **uma única medição** não é suficiente para concluir que uma consulta ficou mais rápida.

---

# Parte II — Seletividade e diferentes consultas

## Exercício 7 — Coluna com poucos valores distintos

Antes de criar um novo índice, execute:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM lab_reserva_indice
WHERE cidade = 'Curitiba';
```

Crie um índice sobre `cidade` e execute novamente a consulta.

1. Aproximadamente qual parcela da tabela corresponde a Curitiba?
2. O PostgreSQL utilizou o índice?
3. Por que um índice pode não ser vantajoso quando a consulta retorna muitas linhas?

## Exercício 8 — Valores frequentes e raros

Consulte a quantidade de registros para cada `status`. Depois crie um índice simples nessa coluna.

Compare com `EXPLAIN (ANALYZE, BUFFERS)` as duas consultas:

```sql
SELECT *
FROM lab_reserva_indice
WHERE status = 'Cancelada';
```

```sql
SELECT *
FROM lab_reserva_indice
WHERE status = 'Confirmada';
```

Use `EXPLAIN (ANALYZE, BUFFERS)` antes de cada `SELECT` ao executar os testes.

**Pergunta:** a mesma estrutura de índice é necessariamente escolhida para os dois valores? Justifique com a quantidade de linhas retornadas.

## Exercício 9 — Índice e contagem de registros

Após criar o índice de `cidade`, compare os planos de:

```sql
SELECT *
FROM lab_reserva_indice
WHERE cidade = 'Curitiba';
```

```sql
SELECT COUNT(*)
FROM lab_reserva_indice
WHERE cidade = 'Curitiba';
```

1. As operações escolhidas são iguais?
2. Você encontrou `Index Only Scan` ou `Bitmap` em algum plano?
3. Por que buscar todas as colunas pode ter um custo diferente de apenas contar registros?

Não é necessário que todos os computadores apresentem os mesmos tipos de scan.

## Exercício 10 — Consultas por intervalo de datas

Antes de criar um índice sobre `data_checkin`, analise:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM lab_reserva_indice
WHERE data_checkin BETWEEN DATE '2025-06-01'
                       AND DATE '2025-06-07';
```

Registre o plano e a quantidade de linhas retornadas.

## Exercício 11 — Índices e ordenação

Crie um índice sobre `data_checkin`. Depois compare os planos das consultas:

```sql
SELECT *
FROM lab_reserva_indice
WHERE data_checkin BETWEEN DATE '2025-06-01'
                       AND DATE '2025-06-07';
```

```sql
SELECT *
FROM lab_reserva_indice
ORDER BY data_checkin
LIMIT 20;
```

1. O índice foi útil para uma das consultas? Para ambas?
2. Há operação de ordenação (`Sort`) explícita no plano?
3. Por que a presença de `LIMIT` pode influenciar a escolha do plano?

---

# Parte III — Índices compostos e especializados

## Exercício 12 — Índices e chaves estrangeiras

Retorne às tabelas reais `hospede` e `reserva` do hotel.

1. Identifique a chave primária de cada uma.
2. Identifique a chave estrangeira que relaciona uma reserva ao hóspede.
3. Verifique se há um índice explícito na coluna da chave estrangeira da tabela `reserva`.
4. Explique: o PostgreSQL cria automaticamente um índice na **coluna filha** de toda `FOREIGN KEY`?

**Não crie nem remova índices nas tabelas originais nesta questão.**

## Exercício 13 — Índice composto

Na tabela de laboratório, analise:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM lab_reserva_indice
WHERE id_hospede = 125
  AND status = 'Confirmada';
```

Crie o índice composto:

```sql
CREATE INDEX idx_lab_reserva_hospede_status
ON lab_reserva_indice(id_hospede, status);
```

Execute `ANALYZE` e repita a consulta. Compare os planos.

## Exercício 14 — Ordem das colunas

Com o índice `(id_hospede, status)` criado, analise separadamente:

```sql
SELECT * FROM lab_reserva_indice WHERE id_hospede = 125;
```

```sql
SELECT * FROM lab_reserva_indice WHERE status = 'Confirmada';
```

```sql
SELECT * FROM lab_reserva_indice
WHERE id_hospede = 125 AND status = 'Confirmada';
```

1. Em quais casos o índice composto foi escolhido?
2. Por que a ordem das colunas pode influenciar o uso do índice?
3. Por que o índice simples sobre `status`, criado antes, também pode interferir nos resultados?

## Exercício 15 — Comparando duas ordens possíveis

Crie outro índice composto, desta vez com as colunas invertidas:

```sql
CREATE INDEX idx_lab_reserva_status_hospede
ON lab_reserva_indice(status, id_hospede);
```

Analise novamente as três consultas do Exercício 14.

Identifique **qual índice o PostgreSQL escolhe em cada caso**. Não presuma que o índice criado por último será utilizado. Ao final, remova o índice de ordem invertida.

## Exercício 16 — Índice em expressão

Considere uma consulta que ignora diferenças entre letras maiúsculas e minúsculas:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM lab_reserva_indice
WHERE LOWER(email_contato) = 'cliente85000@hotel.com';
```

1. O índice simples sobre `email_contato` foi aproveitado?
2. Crie um **índice em expressão** usando `LOWER(email_contato)`.
3. Repita a consulta.
4. Explique por que um índice na expressão pode ser mais adequado nesse caso.

## Exercício 17 — Índice parcial

Crie um índice parcial sobre `data_checkin` contendo **somente as reservas canceladas**:

```sql
CREATE INDEX idx_lab_reserva_data_cancelada
ON lab_reserva_indice(data_checkin)
WHERE status = 'Cancelada';
```

Compare os planos para buscas no mesmo intervalo de datas, uma com `status = 'Cancelada'` e outra com `status = 'Confirmada'`.

Explique por que o índice parcial não representa todos os registros da tabela e por que a condição da consulta é importante.

## Exercício 18 — Escolhendo um índice para uma necessidade real

Uma tela do sistema precisa exibir as reservas de um hóspede, ordenadas da mais recente para a mais antiga:

```sql
SELECT
    id_reserva,
    id_hospede,
    data_checkin,
    status
FROM lab_reserva_indice
WHERE id_hospede = 125
ORDER BY data_checkin DESC
LIMIT 10;
```

1. Analise o plano atual.
2. Proponha e crie um índice adequado a esse padrão de consulta.
3. Execute novamente o plano.
4. Explique por que escolheu as colunas e a ordem do índice.

---

# Parte IV — Custo de armazenamento e manutenção

## Exercício 19 — Espaço ocupado

Consulte os índices da tabela de laboratório usando `pg_indexes` ou comandos do `psql`.

Depois descubra:

- tamanho dos dados da tabela;
- tamanho total dos índices;
- tamanho total da relação incluindo índices.

Dica: pesquise e utilize `pg_relation_size`, `pg_indexes_size`, `pg_total_relation_size` e `pg_size_pretty`.

**Pergunta:** os índices ocupam espaço de armazenamento? Justifique com os valores obtidos.

## Exercício 20 — Comparação de INSERT

Crie duas tabelas de laboratório com **a mesma estrutura e nenhum dado**: `lab_sem_indice` e `lab_com_indice`. Utilize apenas as colunas `email_contato`, `cidade`, `status` e `valor_total`.

Crie um índice em `email_contato` **somente** na tabela `lab_com_indice`.

Insira os mesmos 50.000 registros, copiados de `lab_reserva_indice`, nas duas tabelas. Meça os tempos de execução com `\timing on`.

1. Qual inserção levou mais tempo?
2. Qual operação extra foi necessária na tabela com índice?
3. É correto afirmar que a diferença encontrada será sempre igual em outras máquinas e execuções? Explique.

## Exercício 21 — Comparação de UPDATE

Nas duas tabelas criadas no Exercício 20, altere o campo `email_contato` dos primeiros 10.000 registros copiados, usando um critério que identifique as mesmas linhas em ambas.

Meça os tempos e responda:

1. A tabela com índice precisou realizar trabalho adicional?
2. Por que alterações em uma coluna indexada podem ter custo maior?
3. Quais outros fatores podem interferir no tempo medido?

## Exercício 22 — Removendo um índice

Remova o índice criado sobre `email_contato` da tabela principal de laboratório:

```sql
DROP INDEX IF EXISTS idx_lab_reserva_email;
```

Depois:

1. confira que ele não aparece mais na lista de índices;
2. execute novamente `EXPLAIN (ANALYZE, BUFFERS)` para a consulta do Exercício 4;
3. compare o novo plano com o registrado no Exercício 5;
4. explique por que o resultado pode voltar a apresentar uma varredura sequencial.

---

# Parte V — Análise e desafio integrador

## Exercício 23 — Escolha de índices

Para cada situação, decida **se criaria um índice** e, em caso positivo, qual seria:

1. A tabela tem apenas 20 registros e quase nunca é consultada.
2. Uma tabela tem 2 milhões de linhas e é frequentemente pesquisada por um email específico.
3. Uma consulta retorna quase todos os registros de uma tabela.
4. Um relatório busca repetidamente reservas por `id_hospede` e intervalo de datas.
5. Uma tabela recebe milhares de inserções por segundo, mas uma determinada coluna quase nunca aparece em consultas.

Justifique cada decisão em termos de seletividade, frequência de uso e custo de manutenção.

## Exercício 24 — Interpretando planos

Escolha **três consultas diferentes** desta atividade. Para cada uma, apresente:

- SQL da consulta;
- plano obtido com `EXPLAIN (ANALYZE, BUFFERS)`;
- índice ou índices disponíveis;
- tipo de scan utilizado;
- quantidade de linhas retornadas;
- tempo de execução;
- explicação do motivo pelo qual o índice foi utilizado ou não.

## Exercício 25 — Desafio final

Imagine que o sistema de hotel cresceu e agora possui milhões de reservas. A equipe relata lentidão nas consultas de busca por hóspede e nas consultas por período.

Realize uma pequena análise de otimização utilizando `lab_reserva_indice`:

1. selecione uma consulta de busca por hóspede e outra por período;
2. registre os respectivos planos de execução;
3. avalie os índices que já existem e identifique possíveis redundâncias;
4. crie ou ajuste **até dois índices**, justificando suas escolhas;
5. atualize as estatísticas, se necessário;
6. execute novamente as consultas;
7. compare as evidências antes e depois;
8. produza uma conclusão curta indicando **benefícios, limitações e custos** da solução.

Não basta afirmar que um índice deixa a busca mais rápida: sua justificativa deve estar baseada no plano de execução e nas medições realizadas.

---

## 3. Entrega

Utilize o link para entrega: []()

Entrega ate 10/11/2026
