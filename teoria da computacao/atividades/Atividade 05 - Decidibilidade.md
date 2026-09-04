# Lista de Exercícios — Capítulo 4: Decidibilidade

Esta lista contém **10 exercícios** sobre problemas decidíveis, reconhecíveis e indecidíveis, seguindo os conceitos discutidos no capítulo.

---

## Exercício 1 — Problemas como linguagens

Explique, com suas palavras, por que um problema de decisão pode ser representado como uma linguagem.

Depois, defina uma linguagem para o seguinte problema:

> Dado um número natural \(n\), determinar se \(n\) é múltiplo de 3.

Use a notação:

\[
L=\{\langle n\rangle \mid \cdots\}
\]

---

## Exercício 2 — \(A_{DFA}\)

Considere:

\[
A_{DFA}=\{\langle B,w\rangle \mid B \text{ é um AFD que aceita } w\}
\]

Explique por que \(A_{DFA}\) é decidível.

Sua resposta deve mencionar:

1. o que a Máquina de Turing recebe como entrada;
2. como ela simula o AFD;
3. por que a simulação sempre termina.

---

## Exercício 3 — \(A_{NFA}\)

Considere:

\[
A_{NFA}=\{\langle B,w\rangle \mid B \text{ é um AFN que aceita } w\}
\]

Mostre que \(A_{NFA}\) é decidível usando o fato de que todo AFN pode ser convertido para um AFD equivalente.

---

## Exercício 4 — Expressões regulares

Defina a linguagem:

\[
A_{REX}=\{\langle R,w\rangle \mid R \text{ é uma expressão regular que gera } w\}
\]

Explique como decidir \(A_{REX}\).

Sua solução deve seguir a cadeia:

\[
\text{expressão regular}
\rightarrow
\text{AFN}
\rightarrow
\text{AFD}
\rightarrow
\text{simulação}
\]

---

## Exercício 5 — Linguagem vazia de um AFD

Considere:

\[
E_{DFA}=\{\langle A\rangle \mid A \text{ é um AFD e }L(A)=\emptyset\}
\]

Descreva um algoritmo para decidir \(E_{DFA}\).

Depois, explique por que o problema pode ser resolvido usando alcançabilidade de estados.

---

## Exercício 6 — Equivalência de AFDs

Considere:

\[
EQ_{DFA}=\{\langle A,B\rangle \mid A \text{ e }B\text{ são AFDs e }L(A)=L(B)\}
\]

Mostre que \(EQ_{DFA}\) é decidível.

Dica: construa um AFD \(C\) que aceita as palavras em que \(A\) e \(B\) discordam:

\[
L(C)=
(L(A)\cap \overline{L(B)})
\cup
(\overline{L(A)}\cap L(B))
\]

---

## Exercício 7 — \(A_{CFG}\)

Considere:

\[
A_{CFG}=\{\langle G,w\rangle \mid G \text{ é uma GLC que gera } w\}
\]

Explique por que simplesmente testar todas as derivações de \(G\) pode não produzir um decisor.

Depois, explique como a Forma Normal de Chomsky permite construir um decisor para \(A_{CFG}\).

---

## Exercício 8 — Linguagem vazia de uma GLC

Considere:

\[
E_{CFG}=\{\langle G\rangle \mid G \text{ é uma GLC e }L(G)=\emptyset\}
\]

Descreva o algoritmo de marcação usado para decidir \(E_{CFG}\).

Aplique o algoritmo à gramática:

\[
S\to AB
\]

\[
A\to a
\]

\[
B\to C
\]

\[
C\to b
\]

A linguagem dessa gramática é vazia? Justifique.

---

## Exercício 9 — \(A_{TM}\)

Considere:

\[
A_{TM}=\{\langle M,w\rangle \mid M \text{ é uma MT e }M\text{ aceita }w\}
\]

Explique por que \(A_{TM}\) é Turing-reconhecível.

Depois, explique por que a simulação universal de \(M\) sobre \(w\) não é suficiente para mostrar que \(A_{TM}\) é decidível.

---

## Exercício 10 — Reconhecível, co-reconhecível e decidível

Explique o seguinte resultado:

\[
A\text{ é decidível}
\Leftrightarrow
A\text{ é Turing-reconhecível e }\overline{A}\text{ é Turing-reconhecível}
\]

Depois, use esse resultado para justificar por que:

\[
\overline{A_{TM}}
\]

não é Turing-reconhecível.

Dica: lembre-se de que \(A_{TM}\) é reconhecível, mas não é decidível.
