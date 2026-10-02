# Lista de Exercícios — Introdução à Análise de Complexidade

# Parte I — Conceitos fundamentais

## Exercício 1 — Por que não medir apenas o tempo?

Explique por que medir o tempo de execução de um programa em um computador específico não é suficiente para caracterizar a eficiência de um algoritmo.

Na resposta, considere pelo menos três fatores externos que podem alterar a medição.

---

## Exercício 2 — Modelo RAM

Explique o que é o **modelo RAM (Random-Access Machine)**.

Indique quais das operações abaixo normalmente são tratadas como operações de custo constante nesse modelo:

a. soma de dois inteiros de tamanho convencional;  
b. acesso a `A[i]`;  
c. atribuição `x = 10`;  
d. comparação `x < y`;  
e. ordenar um vetor inteiro em uma única instrução;  
f. chamada de uma função cujo corpo percorre um vetor inteiro.

Justifique especialmente os itens **e** e **f**.

---

## Exercício 3 — Tamanho da entrada

Para cada problema, indique uma medida adequada para o tamanho da entrada.

a. Somar os valores de um vetor.  
b. Ordenar um vetor.  
c. Multiplicar dois inteiros muito grandes.  
d. Percorrer um grafo.  
e. Verificar se uma palavra possui determinado caractere.

Explique por que nem sempre o tamanho da entrada é representado apenas por `n`.

---

## Exercício 4 — Operação básica

Para cada algoritmo, indique uma operação que poderia ser adotada como **operação básica**.

a. Busca linear em um vetor.  
b. Encontrar o maior elemento de um vetor.  
c. Selection sort.  
d. Somar os elementos de um vetor.  
e. Verificar se existem dois valores iguais em um vetor usando dois laços.

Explique por que a escolha da operação básica facilita a análise.

---

## Exercício 5 — Tempo e espaço

Explique a diferença entre:

```text
complexidade de tempo
complexidade de espaço
```

Depois considere dois algoritmos hipotéticos para o mesmo problema:

```text
Algoritmo A:
tempo aproximado proporcional a n²
memória auxiliar proporcional a 1

Algoritmo B:
tempo aproximado proporcional a n
memória auxiliar proporcional a n
```

Explique a troca existente entre as duas soluções.

---

# Parte II — Contagem de operações

## Exercício 6 — Laço simples

Considere:

```text
soma = 0

for i = 1 até n:
    soma = soma + A[i]
```

Responda:

a. Qual é o tamanho da entrada?  
b. Considere `soma = soma + A[i]` como operação básica. Quantas vezes ela é executada?  
c. Escreva uma função `C(n)` para essa operação.  
d. Qual é a classificação em Big O?

---

## Exercício 7 — Laço com passo 2

Considere:

```text
for i = 0; i < n; i = i + 2:
    imprimir(A[i])
```

Responda:

a. Aproximadamente quantas vezes o corpo do laço é executado?  
b. O fato de o laço avançar de dois em dois altera a classificação em Big O?  
c. Justifique.

---

## Exercício 8 — Dois laços consecutivos

Considere:

```text
for i = 0 até n-1:
    operacao()

for j = 0 até n-1:
    operacao()
```

a. Quantas vezes `operacao()` é executada no total?  
b. Escreva `C(n)`.  
c. Classifique em Big O.  
d. Explique por que dois laços consecutivos não produzem, neste caso, `O(n²)`.

---

## Exercício 9 — Dois laços aninhados

Considere:

```text
for i = 0 até n-1:
    for j = 0 até n-1:
        operacao()
```

a. Quantas vezes `operacao()` é executada?  
b. Escreva `C(n)`.  
c. Classifique em Big O.

---

## Exercício 10 — Laço triangular

Considere:

```text
for i = 0 até n-1:
    for j = i+1 até n-1:
        operacao()
```

a. Quantas vezes o laço interno executa quando `i = 0`?  
b. E quando `i = 1`?  
c. E quando `i = n-2`?  
d. Escreva a soma que representa o total de execuções.  
e. Simplifique a soma.  
f. Classifique o algoritmo em Big O.

---

# Parte III — Melhor, pior e caso médio

## Exercício 11 — Busca linear

Considere uma busca linear por um valor `x` em um vetor de `n` elementos.

a. Qual é o melhor caso?  
b. Quantas comparações ocorrem no melhor caso?  
c. Qual é o pior caso?  
d. Quantas comparações ocorrem no pior caso?  
e. Supondo que `x` esteja no vetor e tenha a mesma probabilidade de aparecer em qualquer posição, qual é aproximadamente a quantidade média de comparações?  
f. Classifique melhor, pior e caso médio em Big O.

---

## Exercício 12 — Encontrar o maior valor

Considere:

```text
maior = A[0]

for i = 1 até n-1:
    if A[i] > maior:
        maior = A[i]
```

a. Qual operação deve ser contada?  
b. Quantas comparações são realizadas?  
c. A quantidade de comparações muda entre melhor e pior caso?  
d. A quantidade de atribuições para `maior` pode mudar? Dê exemplos.  
e. Qual é a complexidade em Big O?

---

## Exercício 13 — Insertion sort

Considere o insertion sort estudado em aula.

Explique:

a. por que um vetor já ordenado representa o melhor caso;  
b. por que um vetor em ordem inversa representa o pior caso;  
c. qual é a ordem de crescimento do melhor caso;  
d. qual é a ordem de crescimento do pior caso;  
e. por que duas entradas com o mesmo tamanho podem produzir tempos diferentes.

---

## Exercício 14 — Selection sort

No selection sort, em cada posição `i`, procuramos o menor elemento no restante do vetor.

a. Quantas comparações são feitas na primeira passagem?  
b. Quantas na segunda?  
c. Continue o padrão até a última passagem relevante.  
d. Escreva a soma total.  
e. O número de comparações muda se o vetor já estiver ordenado?  
f. Qual é a complexidade em Big O no melhor e no pior caso?
