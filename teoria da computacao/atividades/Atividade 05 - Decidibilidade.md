# Lista de Exercícios — Capítulo 4: Decidibilidade

Esta lista contém **10 exercícios** sobre problemas decidíveis, reconhecíveis e indecidíveis, seguindo os conceitos discutidos no capítulo.

---

## Exercício 1 — Problemas como linguagens

Explique, com suas palavras, por que um problema de decisão pode ser representado como uma linguagem.

Depois, defina uma linguagem para o seguinte problema:

> Dado um número natural `n`, determinar se `n` é múltiplo de 3.

Use a notação:

```text
L = { <n> : n é múltiplo de 3 }
```

---

## Exercício 2 — ADFA

Considere:

```text
ADFA = { <B,w> : B é um AFD que aceita w }
```

Explique por que `ADFA` é decidível.

Sua resposta deve mencionar:

1. o que a Máquina de Turing recebe como entrada;
2. como ela simula o AFD;
3. por que a simulação sempre termina.

---

## Exercício 3 — ANFA

Considere:

```text
ANFA = { <B,w> : B é um AFN que aceita w }
```

Mostre que `ANFA` é decidível usando o fato de que todo AFN pode ser convertido para um AFD equivalente.

---

## Exercício 4 — Expressões regulares

Defina a linguagem:

```text
AREX = { <R,w> : R é uma expressão regular que gera w }
```

Explique como decidir `AREX`.

Sua solução deve seguir a cadeia:

```text
expressão regular -> AFN -> AFD -> simulação
```

---

## Exercício 5 — Linguagem vazia de um AFD

Considere:

```text
EDFA = { <A> : A é um AFD e L(A) é vazia }
```

Descreva um algoritmo para decidir `EDFA`.

Depois, explique por que o problema pode ser resolvido usando alcançabilidade de estados.

---

## Exercício 6 — Equivalência de AFDs

Considere:

```text
EQDFA = { <A,B> : A e B são AFDs e L(A) = L(B) }
```

Mostre que `EQDFA` é decidível.

Dica: construa um AFD `C` que aceita as palavras em que `A` e `B` discordam:

```text
L(C) =
(palavras aceitas por A e não aceitas por B)
OU
(palavras não aceitas por A e aceitas por B)
```

---

## Exercício 7 — ACFG

Considere:

```text
ACFG = { <G,w> : G é uma GLC que gera w }
```

Explique por que simplesmente testar todas as derivações de `G` pode não produzir um decisor.

Depois, explique como a Forma Normal de Chomsky permite construir um decisor para `ACFG`.

---

## Exercício 8 — Linguagem vazia de uma GLC

Considere:

```text
ECFG = { <G> : G é uma GLC e L(G) é vazia }
```

Descreva o algoritmo de marcação usado para decidir `ECFG`.

Aplique o algoritmo à gramática:

```text
S -> AB
A -> a
B -> C
C -> b
```

A linguagem dessa gramática é vazia? Justifique.

---

## Exercício 9 — ATM

Considere:

```text
ATM = { <M,w> : M é uma MT e M aceita w }
```

Explique por que `ATM` é Turing-reconhecível.

Depois, explique por que a simulação universal de `M` sobre `w` não é suficiente para mostrar que `ATM` é decidível.

---

## Exercício 10 — Reconhecível, co-reconhecível e decidível

Explique o seguinte resultado:

```text
A é decidível
SE, E SOMENTE SE,
A é Turing-reconhecível e o complemento de A é Turing-reconhecível.
```

Depois, use esse resultado para justificar por que:

```text
o complemento de ATM
```

não é Turing-reconhecível.

Dica: lembre-se de que `ATM` é reconhecível, mas não é decidível.
