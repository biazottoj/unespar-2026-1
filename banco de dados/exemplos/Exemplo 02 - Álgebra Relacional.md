# Walkthrough — Álgebra Relacional: Seleção, Projeção, União, Diferença e Interseção

Este walkthrough apresenta cinco operações fundamentais da álgebra relacional: **seleção**, **projeção**, **união**, **diferença** e **interseção**. Todas as operações serão explicadas a partir do mesmo conjunto de tabelas, para que seja possível comparar o efeito de cada operador sobre os dados.

A álgebra relacional trabalha com **tabelas** como objetos. Cada operação recebe uma ou mais tabelas como entrada e produz uma nova tabela como resultado. Por isso, é possível combinar operações, pois o resultado de uma operação pode ser usado como entrada de outra.

---

## 1. Conjunto de tabelas usado nos exemplos

Neste walkthrough, considere duas tabelas que representam alunos inscritos em duas oficinas diferentes.

### Relação `Inscritos_BD`

`Inscritos_BD(ra, nome, curso, periodo, cidade)`

| ra    | nome   | curso | periodo | cidade     |
|-------|--------|-------|---------|------------|
| RA101 | Ana    | SI    | 3       | Marialva   |
| RA102 | Bruno  | CC    | 5       | Maringá    |
| RA103 | Carla  | SI    | 3       | Marialva   |
| RA104 | Diego  | ES    | 7       | Apucarana  |
| RA105 | Elisa  | CC    | 5       | Maringá    |

### Relação `Inscritos_IA`

`Inscritos_IA(ra, nome, curso, periodo, cidade)`

| ra    | nome     | curso | periodo | cidade     |
|-------|----------|-------|---------|------------|
| RA103 | Carla    | SI    | 3       | Marialva   |
| RA105 | Elisa    | CC    | 5       | Maringá    |
| RA106 | Felipe   | ES    | 7       | Londrina   |
| RA107 | Gabriela | SI    | 3       | Marialva   |
| RA108 | Henrique | CC    | 1       | Apucarana  |

### Observação importante sobre as operações de conjunto

As operações **união**, **diferença** e **interseção** só podem ser aplicadas diretamente quando as tabelas são compatíveis. Neste exemplo, as duas tabelas possuem a mesma estrutura:

```text
(ra, nome, curso, periodo, cidade)
```

Isso permite comparar as linhas de uma tabela com as linhas da outra.

---

## 2. Seleção

A **seleção** filtra as linhas de uma tabela. Ela mantém todas as colunas, mas retorna apenas as linhas que satisfazem uma condição.

### Forma geral

```text
σ condição (tabela)
```

O símbolo `σ` é a letra grega sigma e representa a operação de seleção.

### Exemplo

**Consulta:** obter todos os alunos inscritos na oficina de Banco de Dados que são da cidade de Marialva e estão no 3º período.

### Resposta textual completa

```text
σ cidade = 'Marialva' AND periodo = 3 (Inscritos_BD)
```

### Quebrando a expressão

```text
σ
```

Indica que a operação é uma **seleção**. O objetivo é filtrar linhas.

```text
cidade = 'Marialva' AND periodo = 3
```

É a condição que será testada em cada linha da tabela. Para uma linha aparecer no resultado, ela precisa satisfazer as duas partes da condição: a cidade deve ser `Marialva` e o período deve ser `3`.

```text
(Inscritos_BD)
```

Indica a tabela sobre a qual a seleção será aplicada.

### Resultado

| ra    | nome  | curso | periodo | cidade   |
|-------|-------|-------|---------|----------|
| RA101 | Ana   | SI    | 3       | Marialva |
| RA103 | Carla | SI    | 3       | Marialva |

### Interpretação

A seleção analisou todas as linhas de `Inscritos_BD`, mas retornou apenas as linhas em que a cidade é `Marialva` e o período é `3`. As colunas da tabela original foram preservadas.

---

## 3. Projeção

A **projeção** escolhe quais colunas devem aparecer no resultado. Ela pode reduzir a quantidade de atributos exibidos.

### Forma geral

```text
π coluna1, coluna2, ... (tabela)
```

O símbolo `π` é a letra grega pi e representa a operação de projeção.

### Exemplo

**Consulta:** obter apenas os pares de curso e cidade dos alunos inscritos na oficina de Banco de Dados.

### Resposta textual completa

```text
π curso, cidade (Inscritos_BD)
```

### Quebrando a expressão

```text
π
```

Indica que a operação é uma **projeção**. O objetivo é escolher colunas.

```text
curso, cidade
```

São as colunas que devem aparecer no resultado.

```text
(Inscritos_BD)
```

Indica a tabela sobre a qual a projeção será aplicada.

### Resultado

| curso | cidade    |
|-------|-----------|
| SI    | Marialva  |
| CC    | Maringá   |
| ES    | Apucarana |

### Interpretação

A projeção manteve apenas as colunas `curso` e `cidade`. Como a álgebra relacional trabalha com conjuntos, linhas repetidas são eliminadas. Por isso, embora `Ana` e `Carla` sejam de `SI` e `Marialva`, esse par aparece apenas uma vez no resultado.

---

## 4. União

A **união** combina as linhas de duas tabelas compatíveis. O resultado contém as linhas que aparecem na primeira tabela, na segunda tabela ou em ambas.

### Forma geral

```text
tabela1 ∪ tabela2
```

O símbolo `∪` representa a operação de união.

### Exemplo

**Consulta:** obter todos os alunos que se inscreveram na oficina de Banco de Dados ou na oficina de Inteligência Artificial.

### Resposta textual completa

```text
Inscritos_BD ∪ Inscritos_IA
```

### Quebrando a expressão

```text
Inscritos_BD
```

É a primeira tabela da operação.

```text
∪
```

Indica a operação de **união**. Ela junta as linhas das duas tabelas.

```text
Inscritos_IA
```

É a segunda tabela da operação.

### Resultado

| ra    | nome     | curso | periodo | cidade    |
|-------|----------|-------|---------|-----------|
| RA101 | Ana      | SI    | 3       | Marialva  |
| RA102 | Bruno    | CC    | 5       | Maringá   |
| RA103 | Carla    | SI    | 3       | Marialva  |
| RA104 | Diego    | ES    | 7       | Apucarana |
| RA105 | Elisa    | CC    | 5       | Maringá   |
| RA106 | Felipe   | ES    | 7       | Londrina  |
| RA107 | Gabriela | SI    | 3       | Marialva  |
| RA108 | Henrique | CC    | 1       | Apucarana |

### Interpretação

A união retornou todos os alunos que aparecem em pelo menos uma das duas tabelas. `Carla` e `Elisa` aparecem nas duas tabelas, mas são exibidas apenas uma vez no resultado.

---

## 5. Diferença

A **diferença** retorna as linhas que aparecem na primeira tabela, mas não aparecem na segunda.

### Forma geral

```text
tabela1 − tabela2
```

O símbolo `−` representa a operação de diferença.

### Exemplo

**Consulta:** obter os alunos que se inscreveram na oficina de Banco de Dados, mas não se inscreveram na oficina de Inteligência Artificial.

### Resposta textual completa

```text
Inscritos_BD − Inscritos_IA
```

### Quebrando a expressão

```text
Inscritos_BD
```

É a primeira tabela. A diferença começa observando as linhas desta tabela.

```text
−
```

Indica a operação de **diferença**. Ela remove da primeira tabela as linhas que também aparecem na segunda.

```text
Inscritos_IA
```

É a segunda tabela. Suas linhas serão usadas para excluir linhas da primeira tabela.

### Resultado

| ra    | nome  | curso | periodo | cidade    |
|-------|-------|-------|---------|-----------|
| RA101 | Ana   | SI    | 3       | Marialva  |
| RA102 | Bruno | CC    | 5       | Maringá   |
| RA104 | Diego | ES    | 7       | Apucarana |

### Interpretação

A diferença retornou os alunos que estão em `Inscritos_BD` e não estão em `Inscritos_IA`. `Carla` e `Elisa` foram removidas porque aparecem nas duas tabelas.

---

## 6. Interseção

A **interseção** retorna as linhas que aparecem nas duas tabelas ao mesmo tempo.

### Forma geral

```text
tabela1 ∩ tabela2
```

O símbolo `∩` representa a operação de interseção.

### Exemplo

**Consulta:** obter os alunos que se inscreveram tanto na oficina de Banco de Dados quanto na oficina de Inteligência Artificial.

### Resposta textual completa

```text
Inscritos_BD ∩ Inscritos_IA
```

### Quebrando a expressão

```text
Inscritos_BD
```

É a primeira tabela da operação.

```text
∩
```

Indica a operação de **interseção**. Ela mantém apenas as linhas comuns às duas tabelas.

```text
Inscritos_IA
```

É a segunda tabela da operação.

### Resultado

| ra    | nome  | curso | periodo | cidade   |
|-------|-------|-------|---------|----------|
| RA103 | Carla | SI    | 3       | Marialva |
| RA105 | Elisa | CC    | 5       | Maringá  |

### Interpretação

A interseção retornou apenas os alunos que aparecem nas duas tabelas. Neste exemplo, `Carla` e `Elisa` estão inscritas nas duas oficinas.

---

## 7. Resumo das operações

| Operação | Símbolo | O que faz? | Exemplo |
|----------|---------|------------|---------|
| Seleção | `σ` | Filtra linhas | `σ cidade = 'Marialva' (Inscritos_BD)` |
| Projeção | `π` | Escolhe colunas | `π nome, cidade (Inscritos_BD)` |
| União | `∪` | Junta linhas de duas tabelas | `Inscritos_BD ∪ Inscritos_IA` |
| Diferença | `−` | Mantém linhas da primeira tabela que não estão na segunda | `Inscritos_BD − Inscritos_IA` |
| Interseção | `∩` | Mantém apenas linhas comuns às duas tabelas | `Inscritos_BD ∩ Inscritos_IA` |
