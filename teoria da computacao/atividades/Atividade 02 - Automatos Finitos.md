# Lista de Exercícios — Autômatos Finitos Determinísticos

A lista abaixo contém **10 exercícios em ordem progressiva de dificuldade**, começando com leitura e simulação de AFDs e avançando para construção de autômatos que combinam múltiplas propriedades.

---

## Exercício 1 — Simulando um AFD

Considere um AFD sobre:

\[
\Sigma=\{a,b\}
\]

com a seguinte tabela de transições:

| Estado | `a` | `b` |
|---|---|---|
| \(q_0\) | \(q_1\) | \(q_0\) |
| \(q_1\) | \(q_1\) | \(q_0\) |

Considere:

- \(q_0\) como estado inicial;
- \(q_1\) como estado final.

Para cada palavra abaixo:

1. apresente a sequência de estados visitados;
2. indique se a palavra é aceita ou rejeitada.

Palavras:

a) `a`  
b) `b`  
c) `aba`  
d) `abb`  
e) `bba`  
f) \(\varepsilon\)

Ao final, descreva em português qual linguagem esse AFD reconhece.

---


## Exercício 2 — Palavras que terminam em `b`

Construa um AFD sobre:

\[
\Sigma=\{a,b\}
\]

que reconheça palavras que **terminam com `b`**.

Apresente:

- significado de cada estado;
- estado inicial;
- estado(s) final(is);
- tabela de transições.

Teste o AFD com:

`b`, `aba`, `abb`, `baa`, \(\varepsilon\).

---

## Exercício 3 — Comprimento ímpar

Construa um AFD sobre:

\[
\Sigma=\{0,1\}
\]

que aceite palavras de **comprimento ímpar**.

Explique o que cada estado representa.

---

## Exercício 4 — Quantidade par de `a`

Construa um AFD sobre:

\[
\Sigma=\{a,b\}
\]

que reconheça palavras que possuem uma **quantidade par de símbolos `a`**.

Teste:

`b`, `aa`, `aba`, `abba`, `aaa`.

Antes de construir o AFD, responda:

> O autômato precisa saber exatamente quantos `a`s já apareceram ou apenas alguma propriedade dessa quantidade?

---


