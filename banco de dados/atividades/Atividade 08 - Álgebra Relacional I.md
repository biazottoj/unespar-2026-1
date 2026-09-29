# Lista de Exercícios — Álgebra Relacional

Esta lista contém 40 exercícios discursivos sobre **seleção**, **projeção**, **união**, **diferença** e **interseção**.

Todos os exercícios usam o mesmo conjunto de tabelas. As tabelas possuem a mesma estrutura, o que permite aplicar operações de conjunto entre elas.

---

## Conjunto de tabelas para todas as questões

### Relação `Matriculados_BD`

`Matriculados_BD(ra, nome, curso, periodo, cidade)`

| ra  | nome   | curso | periodo | cidade    |
|-----|--------|-------|---------|-----------|
| A01 | Ana    | SI    | 3       | Marialva  |
| A02 | Bruno  | CC    | 5       | Maringá   |
| A03 | Carla  | SI    | 3       | Marialva  |
| A04 | Diego  | ES    | 7       | Apucarana |
| A05 | Elisa  | CC    | 5       | Maringá   |
| A06 | Felipe | ES    | 3       | Londrina  |

### Relação `Matriculados_IA`

`Matriculados_IA(ra, nome, curso, periodo, cidade)`

| ra  | nome     | curso | periodo | cidade    |
|-----|----------|-------|---------|-----------|
| A03 | Carla    | SI    | 3       | Marialva  |
| A05 | Elisa    | CC    | 5       | Maringá   |
| A07 | Gabriela | SI    | 3       | Marialva  |
| A08 | Henrique | CC    | 1       | Apucarana |
| A09 | Isabela  | ES    | 7       | Londrina  |
| A10 | João     | SI    | 5       | Maringá   |

### Relação `Matriculados_Web`

`Matriculados_Web(ra, nome, curso, periodo, cidade)`

| ra  | nome     | curso | periodo | cidade    |
|-----|----------|-------|---------|-----------|
| A01 | Ana      | SI    | 3       | Marialva  |
| A06 | Felipe   | ES    | 3       | Londrina  |
| A07 | Gabriela | SI    | 3       | Marialva  |
| A10 | João     | SI    | 5       | Maringá   |
| A11 | Karen    | CC    | 1       | Apucarana |
| A12 | Lucas    | ES    | 7       | Marialva  |

---

# Parte 1 — Operações isoladas

Para as questões 1 a 10, escreva a expressão em álgebra relacional e apresente a tabela resultante.

## 1. Seleção

Obtenha todos os alunos de `Matriculados_BD` que são da cidade de Marialva.

## 2. Seleção

Obtenha todos os alunos de `Matriculados_IA` que estão no 7º período.

## 3. Projeção

Obtenha apenas as colunas `curso` e `cidade` da tabela `Matriculados_Web`.

## 4. Projeção

Obtenha apenas as colunas `nome` e `cidade` da tabela `Matriculados_IA`.

## 5. União

Obtenha todos os alunos que aparecem em `Matriculados_BD` ou em `Matriculados_IA`.

## 6. União

Obtenha todos os alunos que aparecem em `Matriculados_IA` ou em `Matriculados_Web`.

## 7. Diferença

Obtenha os alunos que estão em `Matriculados_BD`, mas não estão em `Matriculados_IA`.

## 8. Diferença

Obtenha os alunos que estão em `Matriculados_Web`, mas não estão em `Matriculados_BD`.

## 9. Interseção

Obtenha os alunos que aparecem tanto em `Matriculados_BD` quanto em `Matriculados_IA`.

## 10. Interseção

Obtenha os alunos que aparecem tanto em `Matriculados_IA` quanto em `Matriculados_Web`.

---

# Parte 2 — Construção de consultas com operações combinadas

Para as questões 11 a 25, construa a expressão em álgebra relacional correspondente ao enunciado. O foco desta seção é **formular a consulta**, não identificar uma tabela resultante já fornecida.

## 11. Seleção com União

Construa uma consulta para obter todos os alunos da cidade de Marialva que aparecem em `Matriculados_BD` ou em `Matriculados_IA`.

## 12. Seleção com União

Construa uma consulta para obter todos os alunos do curso de Sistemas de Informação (`SI`) que aparecem em `Matriculados_IA` ou em `Matriculados_Web`.

## 13. Seleção com Interseção

Construa uma consulta para obter os alunos do 3º período que aparecem tanto em `Matriculados_BD` quanto em `Matriculados_Web`.

## 14. Seleção com Interseção

Construa uma consulta para obter os alunos do curso de Ciência da Computação (`CC`) que aparecem tanto em `Matriculados_BD` quanto em `Matriculados_IA`.

## 15. Seleção com União

Construa uma consulta para obter todos os alunos da cidade de Maringá que aparecem em `Matriculados_BD` ou em `Matriculados_Web`.

## 16. Projeção com Interseção

Construa uma consulta para obter apenas `nome` e `cidade` dos alunos que aparecem tanto em `Matriculados_BD` quanto em `Matriculados_IA`.

## 17. Projeção com União

Construa uma consulta para obter apenas os pares `curso` e `periodo` dos alunos que aparecem em `Matriculados_BD` ou em `Matriculados_Web`.

## 18. Projeção com Interseção

Construa uma consulta para obter apenas `nome` e `curso` dos alunos que aparecem tanto em `Matriculados_IA` quanto em `Matriculados_Web`.

## 19. Projeção com União

Construa uma consulta para obter apenas as cidades dos alunos que aparecem em `Matriculados_BD` ou em `Matriculados_IA`.

## 20. Seleção, Projeção e União

Construa uma consulta para obter os pares `curso` e `cidade` dos alunos do 3º período que aparecem em `Matriculados_BD` ou em `Matriculados_IA`.

## 21. Projeção, Seleção, União e Diferença

Construa uma consulta para obter apenas `ra` e `nome` dos alunos que aparecem em pelo menos uma das três relações, estão no 3º período e não são da cidade de Marialva.

## 22. Projeção, Seleção, União e Interseção

Construa uma consulta para obter apenas `nome` e `curso` dos alunos da cidade de Maringá que pertencem ao conjunto comum entre os alunos que aparecem em `Matriculados_BD` ou `Matriculados_IA` e os alunos que aparecem em `Matriculados_IA` ou `Matriculados_Web`.

## 23. Projeção, Seleção e União

Construa uma consulta para obter apenas `curso` e `cidade` dos alunos que satisfazem pelo menos uma das seguintes condições: estão no 7º período e aparecem em `Matriculados_BD` ou `Matriculados_IA`; ou aparecem em `Matriculados_Web` e são da cidade de Marialva.

## 24. Projeção, Seleção, União e Diferença

Construa uma consulta para obter apenas `nome` e `cidade` dos alunos do curso de Ciência da Computação (`CC`) que aparecem em pelo menos uma das três relações, removendo desse conjunto os alunos da cidade de Apucarana que aparecem em `Matriculados_IA` ou em `Matriculados_Web`.

## 25. Projeção, Seleção, União e Interseção

Construa uma consulta para obter apenas `nome` e `curso` dos alunos que estão no 3º período, aparecem em `Matriculados_BD` ou em `Matriculados_Web` e também pertencem a pelo menos um dos seguintes grupos: alunos da cidade de Marialva que aparecem em `Matriculados_BD` ou `Matriculados_IA`; alunos da cidade de Londrina que aparecem em `Matriculados_IA` ou `Matriculados_Web`.

---

# Parte 3 — Identificação de resultados de expressões

Para as questões 26 a 40, identifique a tabela resultante de cada expressão. Não é necessário criar uma nova expressão; o objetivo é interpretar a expressão dada e apresentar o resultado final.

## 26. Expressão com Seleção e União

```text
σ curso = 'SI' (σ periodo = 3 (Matriculados_BD ∪ Matriculados_IA))
```

## 27. Expressão com Seleção e União

```text
σ cidade = 'Maringá' (σ curso = 'CC' (Matriculados_BD ∪ Matriculados_IA))
```

## 28. Expressão com Projeção, Seleção e União

```text
π curso, cidade (σ periodo = 3 (Matriculados_BD ∪ Matriculados_Web))
```

## 29. Expressão com Projeção, Seleção e União

```text
π nome, curso (σ cidade = 'Marialva' (Matriculados_IA ∪ Matriculados_Web))
```

## 30. Expressão com Seleção, Interseção e União

```text
σ periodo = 3 ((Matriculados_BD ∩ Matriculados_Web) ∪ (Matriculados_IA ∩ Matriculados_Web))
```

## 31. Expressão com Seleção, Interseção e União

```text
σ curso = 'SI' (Matriculados_IA ∩ Matriculados_Web) ∪ σ curso = 'SI' (Matriculados_BD ∩ Matriculados_IA)
```

## 32. Expressão com Projeção, Seleção e Interseção

```text
π nome, cidade (σ curso = 'CC' (Matriculados_BD ∩ Matriculados_IA))
```

## 33. Expressão com Projeção, Seleção e Interseção

```text
π curso, periodo (σ cidade = 'Marialva' (Matriculados_BD) ∩ σ cidade = 'Marialva' (Matriculados_IA))
```

## 34. Expressão com União, Diferença, Seleção e Projeção

```text
π nome, cidade (σ cidade = 'Marialva' ((Matriculados_BD ∪ Matriculados_Web) − Matriculados_IA))
```

## 35. Expressão com União, Interseção, Seleção e Projeção

```text
π nome, curso ((σ periodo = 7 (Matriculados_BD ∪ Matriculados_Web)) ∩ (σ curso = 'ES' (Matriculados_IA ∪ Matriculados_Web)))
```

## 36. Expressão com Seleção, União e Diferença

```text
σ periodo = 3 ((Matriculados_BD ∪ Matriculados_IA) − Matriculados_Web)
```

## 37. Expressão com Projeção, Seleção, União e Diferença

```text
π nome, curso (σ cidade = 'Marialva' ((Matriculados_BD ∪ Matriculados_Web) − Matriculados_IA))
```

## 38. Expressão com Projeção, Seleção, União e Interseção

```text
π curso, periodo ((σ cidade = 'Marialva' (Matriculados_BD ∪ Matriculados_IA)) ∩ (σ periodo = 3 (Matriculados_BD ∪ Matriculados_Web)))
```

## 39. Expressão com Projeção, Seleção, União e Diferença

```text
π nome, cidade ((σ curso = 'SI' (Matriculados_BD ∪ Matriculados_Web)) − (σ periodo = 5 (Matriculados_IA ∪ Matriculados_Web)))
```

## 40. Expressão com Seleção, Interseção e União

```text
σ cidade = 'Marialva' ((Matriculados_BD ∩ Matriculados_Web) ∪ (Matriculados_BD ∩ Matriculados_IA) ∪ (Matriculados_IA ∩ Matriculados_Web))
```

## Entrega
- A entrega pode ser feita até as 23:59 do dia 09/06/2026
- A entrega deve ser feita no link: [https://forms.gle/BrzVQixSNmv6zVTo9](https://forms.gle/BrzVQixSNmv6zVTo9)

