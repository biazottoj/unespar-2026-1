# Exemplos apresentados na aula

## Exemplo 7.1 — Obter a tabela de peças

```sql
SELECT *
FROM peca;
```

### Resultado esperado

| cod_peca | nome_peca  | cor_peca | peso_peca | cidade_peca |
|---|---|---|---:|---|
| P1 | Eixo | Vermelho | 12.00 | Rio |
| P2 | Pino | Verde | 17.00 | Curitiba |
| P3 | Parafuso | Azul | 17.00 | Rio |
| P4 | Parafuso | Vermelho | 14.00 | Porto Alegre |
| P5 | Engrenagem | Azul | 22.00 | rIo |
| P6 | Roda | Vermelho | 19.00 | Curitiba |
| P7 | Porca | Preto | 8.00 | Rio |

A consulta não possui `WHERE` e utiliza `SELECT *`. Portanto, retorna todas as linhas e todas as colunas de `peca`.

---

## Exemplo 7.2 — Obter as peças da cidade de Rio

```sql
SELECT *
FROM peca
WHERE cidade_peca = 'Rio';
```

### Resultado esperado

| cod_peca | nome_peca | cor_peca | peso_peca | cidade_peca |
|---|---|---|---:|---|
| P1 | Eixo | Vermelho | 12.00 | Rio |
| P3 | Parafuso | Azul | 17.00 | Rio |
| P7 | Porca | Preto | 8.00 | Rio |

A peça `P5` não aparece porque sua cidade está cadastrada como `rIo`. A comparação por igualdade diferencia letras maiúsculas de minúsculas no PostgreSQL.

---

## Exemplo 7.3 — Obter código, nome e peso das peças de Rio

```sql
SELECT
    cod_peca,
    nome_peca,
    peso_peca
FROM peca
WHERE cidade_peca = 'Rio';
```

### Resultado esperado

| cod_peca | nome_peca | peso_peca |
|---|---|---:|
| P1 | Eixo | 12.00 |
| P3 | Parafuso | 17.00 |
| P7 | Porca | 8.00 |

### Equivalência em álgebra relacional

```text
π cod_peca, nome_peca, peso_peca
(
    σ cidade_peca = 'Rio'
    (
        peca
    )
)
```

---

## Exemplo 7.4 — Peças de Rio cujo peso excede 15

```sql
SELECT *
FROM peca
WHERE cidade_peca = 'Rio'
  AND peso_peca > 15;
```

### Resultado esperado

| cod_peca | nome_peca | cor_peca | peso_peca | cidade_peca |
|---|---|---|---:|---|
| P3 | Parafuso | Azul | 17.00 | Rio |

As duas condições precisam ser verdadeiras porque foram conectadas por `AND`.

---

## Exemplo 7.5 — Embarques de peças denominadas Parafuso

Para cada embarque de uma peça denominada `Parafuso`, obter o código da peça, o código do fornecedor e a data do embarque.

```sql
SELECT
    peca.cod_peca,
    embarque.cod_fornec,
    embarque.data_embarq
FROM peca,
     embarque
WHERE peca.cod_peca = embarque.cod_peca
  AND peca.nome_peca = 'Parafuso';
```

### Resultado esperado

| cod_peca | cod_fornec | data_embarq |
|---|---|---|
| P3 | F1 | 2026-03-01 |
| P3 | F2 | 2026-03-02 |
| P4 | F1 | 2026-03-03 |
| P3 | F3 | 2026-03-04 |
| P3 | F1 | 2026-04-01 |

A condição `peca.cod_peca = embarque.cod_peca` mantém apenas as combinações em que a peça da tabela `peca` corresponde à peça registrada no embarque.

### Versão equivalente com `JOIN`

```sql
SELECT
    p.cod_peca,
    e.cod_fornec,
    e.data_embarq
FROM peca AS p
JOIN embarque AS e
  ON p.cod_peca = e.cod_peca
WHERE p.nome_peca = 'Parafuso';
```

---

## Exemplo 7.6 — Embarques de Parafuso com o nome do fornecedor

```sql
SELECT
    peca.cod_peca,
    embarque.cod_fornec,
    fornecedor.nome_fornec,
    embarque.data_embarq
FROM peca,
     embarque,
     fornecedor
WHERE peca.cod_peca = embarque.cod_peca
  AND fornecedor.cod_fornec = embarque.cod_fornec
  AND peca.nome_peca = 'Parafuso';
```

### Resultado esperado

| cod_peca | cod_fornec | nome_fornec | data_embarq |
|---|---|---|---|
| P3 | F1 | Silva | 2026-03-01 |
| P3 | F2 | Souza | 2026-03-02 |
| P4 | F1 | Silva | 2026-03-03 |
| P3 | F3 | Santos | 2026-03-04 |
| P3 | F1 | Silva | 2026-04-01 |

---

## Exemplo 7.7 — Fornecedores que não são de Porto Alegre

Obter também os fornecedores cuja cidade não foi informada.

```sql
SELECT *
FROM fornecedor
WHERE cidade_fornec <> 'Porto Alegre'
   OR cidade_fornec IS NULL;
```

### Resultado esperado

| cod_fornec | nome_fornec | status_fornec | cidade_fornec |
|---|---|---:|---|
| F2 | Souza | 10 | Curitiba |
| F3 | Santos | 30 | Curitiba |
| F5 | Moraes | 30 | NULL |
| F6 | Pereira | 15 | Rio |
| F7 | Almeida | 10 | Rio |

Somente `cidade_fornec <> 'Porto Alegre'` não incluiria o fornecedor `F5`, pois comparações com `NULL` produzem valor lógico desconhecido. Por isso, é necessário testar `IS NULL` separadamente.

---

## Exemplo 7.8 — Peças de Rio sem diferenciar maiúsculas e minúsculas

### Alternativa com `UPPER`

```sql
SELECT *
FROM peca
WHERE UPPER(cidade_peca) = 'RIO';
```

### Alternativa com `LOWER`

```sql
SELECT *
FROM peca
WHERE LOWER(cidade_peca) = 'rio';
```

### Resultado esperado para ambas

| cod_peca | nome_peca | cor_peca | peso_peca | cidade_peca |
|---|---|---|---:|---|
| P1 | Eixo | Vermelho | 12.00 | Rio |
| P3 | Parafuso | Azul | 17.00 | Rio |
| P5 | Engrenagem | Azul | 22.00 | rIo |
| P7 | Porca | Preto | 8.00 | Rio |

A peça `P5` passa a aparecer porque `UPPER('rIo')` resulta em `RIO`.

---

## Exemplo 7.9 — Fornecedores cujo nome começa com S maiúsculo

```sql
SELECT
    cod_fornec,
    nome_fornec
FROM fornecedor
WHERE nome_fornec LIKE 'S%';
```

### Resultado esperado

| cod_fornec | nome_fornec |
|---|---|
| F1 | Silva |
| F2 | Souza |
| F3 | Santos |

No padrão `S%`, a letra `S` deve aparecer no início e `%` representa qualquer sequência de caracteres, inclusive uma sequência vazia.

---

## Exemplo 7.10 — Diferentes cidades em que há fornecedores

```sql
SELECT DISTINCT
    cidade_fornec
FROM fornecedor;
```

### Resultado esperado

| cidade_fornec |
|---|
| Porto Alegre |
| Curitiba |
| Rio |
| NULL |

Embora existam vários fornecedores em algumas cidades, `DISTINCT` elimina as linhas repetidas. Os valores `NULL` também são agrupados em uma única linha no resultado de `SELECT DISTINCT`.