# Atividade 06 — Reduções, P, NP, NP-Difícil e NP-Completo

---

## Exercício 1 — Tempo polinomial ou não polinomial

Considere os seguintes tempos de execução:

a. `T(n) = 5n + 20`  
b. `T(n) = n² + 3n + 1`  
c. `T(n) = n⁵`  
d. `T(n) = 2ⁿ`  
e. `T(n) = n!`  
f. `T(n) = n² log n`

Para cada função:

1. indique se ela representa tempo polinomial ou não polinomial;
2. explique por que algoritmos exponenciais tornam-se problemáticos quando `n` cresce.

---

## Exercício 2 — P e NP

Considere os problemas:

### Problema A

> Dado um grafo `G` e dois vértices `s` e `t`, determine se existe um caminho entre `s` e `t`.

### Problema B

> Dado um grafo `G`, determine se existe um ciclo Hamiltoniano.

Responda:

a. Qual dos problemas sabemos que pertence a P?

b. Por que o Problema A pode ser resolvido em tempo polinomial?

c. Suponha que alguém forneça uma sequência de vértices como solução candidata para o Problema B. O que seria necessário verificar para confirmar que ela representa um ciclo Hamiltoniano?

d. Essa verificação pode ser realizada em tempo polinomial?

e. O fato de podermos verificar uma solução de B em tempo polinomial significa que conseguimos encontrar essa solução em tempo polinomial? Justifique.

---

## Exercício 3 — Entendendo uma redução

Suponha que:

```text
A <=p B
```

Responda:

a. O que essa expressão significa?

b. Qual problema é transformado em qual?

c. Se tivermos um algoritmo polinomial para B, o que podemos concluir sobre A?

d. Podemos concluir, apenas a partir de `A <=p B`, que B pertence a P?

e. Qual dos dois problemas podemos considerar como sendo, no mínimo, tão difícil quanto o outro?

---

## Exercício 4 — Direção da redução

Um aluno deseja provar que um novo problema X é NP-difícil.

Ele sabe que o problema HAM é NP-completo.

Qual das seguintes reduções ele deveria tentar construir?

### A)

```text
X <=p HAM
```

### B)

```text
HAM <=p X
```

Explique detalhadamente sua resposta.

Depois, explique por que realizar a redução na direção errada não demonstra que X é NP-difícil.

---

## Exercício 5 — Redução entre dois problemas de P

Considere:

### Problema CAMINHO-K

Entrada: grafo não ponderado `G`, vértices `s`, `t` e número `k`.

Pergunta:

> Existe um caminho de `s` até `t` contendo no máximo `k` arestas?

### Problema DISTÂNCIA-K

Entrada: grafo não ponderado `G`, vértices `s`, `t` e número `k`.

Pergunta:

> A distância mínima entre `s` e `t` é menor ou igual a `k`?

Responda:

a. Explique como transformar uma instância de CAMINHO-K em uma instância de DISTÂNCIA-K.

b. Mostre que:

```text
CAMINHO-K <=p DISTÂNCIA-K
```

c. Essa redução é possível mesmo os dois problemas pertencendo a P?

d. Por que reduções entre problemas de P normalmente são menos interessantes para a análise de NP-completude?

---

# Exercícios 6–8 — Redução de Ciclo Hamiltoniano para TSP

Considere o grafo `G` com:

```text
V = {A, B, C, D, E}
```

e as seguintes arestas:

```text
AB
AC
AD
BC
CD
DE
CE
```

Uma representação aproximada do grafo é:

```text
A ----- B
| \     |
|  \    |
D ----- C
 \     /
  \   /
    E
```

---

## Exercício 6 — Ciclo Hamiltoniano

a. Defina, com suas palavras, o que é um ciclo Hamiltoniano.

b. Determine se o grafo fornecido possui um ciclo Hamiltoniano.

c. Caso exista, forneça um exemplo.

d. Explique por que verificar um ciclo Hamiltoniano fornecido como candidato pode ser feito em tempo polinomial.

---

## Exercício 7 — Construindo a instância do TSP

Vamos reduzir Ciclo Hamiltoniano para a versão de decisão do TSP.

Construa um grafo completo `G'` contendo os mesmos vértices de `G`.

Para cada par de vértices `u,v`, atribua:

```text
peso 1 -> se a aresta existia em G
peso 2 -> se a aresta não existia em G
```

Responda:

a. Complete a tabela:

| Aresta | Peso |
|---|---:|
| AB | |
| AC | |
| AD | |
| AE | |
| BC | |
| BD | |
| BE | |
| CD | |
| CE | |
| DE | |

b. Como `n = 5`, qual valor devemos utilizar para `k`?

c. Encontre, se existir, uma rota do TSP com custo `<= k`.

d. Qual é o custo dessa rota?

e. O que essa resposta nos permite concluir sobre o grafo original?

---

## Exercício 8 — Provando a redução

Queremos mostrar:

```text
HAM <=p TSP
```

A transformação utilizada é:

```text
peso(u,v) = 1, se (u,v) existe em G
peso(u,v) = 2, caso contrário
```

e:

```text
k = n
```

Responda:

a. Se `G` possui ciclo Hamiltoniano, por que a instância correspondente do TSP necessariamente possui uma rota de custo `n`?

b. Se a instância do TSP possui uma rota com custo `<= n`, por que todas as arestas dessa rota precisam ter peso 1?

c. O que isso significa no grafo original `G`?

d. Explique por que:

```text
G pertence a HAM se, e somente se, f(G) pertence a TSP
```

e. Quantos pares de vértices precisam ser examinados para construir `G'`?

f. Justifique por que a transformação pode ser realizada em tempo `O(n²)`.

g. Conclua formalmente a redução.

---

## Exercício 9 — NP-difícil ou NP-completo?

Considere as afirmações:

### Problema X

Sabemos que:

```text
HAM <=p X
```

e que HAM é NP-completo.

### Problema Y

Sabemos que:

```text
HAM <=p Y
```

e também conseguimos verificar, em tempo polinomial, uma solução candidata para Y.

Responda:

a. O que podemos concluir sobre X?

b. Podemos concluir imediatamente que X é NP-completo? Por quê?

c. O que podemos concluir sobre Y?

d. Quais são as duas condições necessárias para que um problema seja NP-completo?

---

## Exercício 10 — TSP: decisão versus otimização

Considere duas versões do Problema do Caixeiro Viajante.

### TSP de decisão

> Existe uma rota que visita todas as cidades exatamente uma vez, retorna ao início e possui custo menor ou igual a `k`?

### TSP de otimização

> Qual é a rota de menor custo que visita todas as cidades exatamente uma vez e retorna ao início?

Responda:

a. Qual das versões é um problema de decisão?

b. Por que a versão de decisão pertence a NP?

c. A versão de decisão do TSP é NP-completa. O que isso significa?

d. Por que o TSP de otimização pode ser classificado como NP-difícil?

e. Explique por que normalmente não classificamos diretamente o problema de otimização como NP-completo.
