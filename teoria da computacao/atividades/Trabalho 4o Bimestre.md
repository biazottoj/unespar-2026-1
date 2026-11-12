# Trabalho Avaliativo — Pesquisa sobre Notações Assintóticas e Aplicações Clássicas

**Disciplina:** Teoria da Computação  
**Unidade:** Análise de Algoritmos  
**Valor:** **4,0 pontos**  
**Aluno(a):** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
**Turma:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  **Data de entrega:** **/**/\_\_\_\_\_\_\_\_


## 1. Orientações para a pesquisa e para a entrega

1. **Pesquise antes de responder.** As quatro primeiras questões são uma pesquisa orientada sobre conteúdos ainda não trabalhados em aula.

2. Utilize **pelo menos duas fontes confiáveis**, como livros de algoritmos, materiais didáticos de universidades ou capítulos de livros digitais. Ao final, informe o autor ou instituição, título e link (quando disponível).

3. Redija as explicações **com suas próprias palavras**. 

4. Nas questões com algoritmos, considere que comparações, atribuições, operações aritméticas simples e acesso a posições de vetores possuem custo constante (de acordo com o modelo RAM).

5. Utilize `n` para representar o tamanho da entrada, `C(n)` para a **contagem da operação escolhida** e `T(n)` para o **custo total** do algoritmo. Explique a relação entre as duas quando necessário.

6. Use `log2 n` para logaritmo de base 2; `//` representa divisão inteira; `n^2` significa `n` ao quadrado. 

7. Nos algoritmos cujo comportamento muda conforme a entrada, indique se a análise corresponde ao **melhor caso**, ao **pior caso** ou a uma contagem que independe dos dados.

8. Ao pesquisar provas, procure justificar **por que as desigualdades valem para todo `n \>= n0`**.


# Parte A — Pesquisa orientada sobre notações (2,0 pontos)

## Questão 1 — Pesquisando a notação Ômega (Ω) — 0,5 ponto

A notação Ômega é utilizada para estabelecer um tipo de limite assintótico diferente daquele estudado em Big O.

**Pesquise e responda:**

**a)** O que significa afirmar que uma função `T(n)` pertence a `Ω(g(n))`? Explique usando suas próprias palavras.  
**b)** Escreva a **definição formal** de Ômega, indicando a desigualdade necessária e o significado de `c` e `n0`.  
**c)** Compare a definição de Ômega à de Big O: o que muda na direção da desigualdade?  
**d)** Considere `T(n) = 4n + 3`, com `n \>= 1`. Mostre, escolhendo valores de `c` e `n0`, que `T(n) ∈ Ω(n)`.

**Para orientar a pesquisa:** procure expressões como “limite inferior assintótico” e “Big Omega definition”.


## Questão 2 — Pesquisando a notação Theta (Θ) — 0,5 ponto

Em diversas análises, não queremos apenas um limite superior ou inferior: queremos descrever a **ordem de crescimento** de maneira mais ajustada.

**Pesquise e responda:**

**a)** O que significa `T(n) ∈ Θ(g(n))`?  
**b)** Por que uma demonstração de Theta precisa apresentar **dois limites**?  
**c)** Escreva sua definição formal, usando `c1`, `c2` e `n0`, e explique o papel de cada constante.  
**d)** Considere `T(n) = 2n^2 + 3n + 1`, com `n \>= 1`. Encontre constantes que permitam provar `T(n) ∈ Θ(n^2)`. Apresente a desigualdade completa.

**Para orientar a pesquisa:** observe que, quando uma função está em `O(g(n))` **e** em `Ω(g(n))`, com a **mesma** `g(n)`, há uma consequência importante. Investigue qual é ela.


## Questão 3 — Pesquisando a notação little-o (o) — 0,5 ponto

A notação **little-o** é escrita com a letra `o` minúscula. Embora sua grafia se pareça com Big O, as duas notações **não significam a mesma coisa**.

**Pesquise e responda:**

**a)** Explique o significado de `T(n) ∈ o(g(n))`.  
**b)** Qual é a diferença entre um **limite superior** representado por Big O e um **limite superior estrito** representado por little-o?  
**c)** Pesquise como o limite da razão `T(n)/g(n)`, quando `n` cresce indefinidamente, pode ajudar a verificar a relação little-o. Indique as condições em que esse critério é aplicável.  
**d)** Investigue se `n ∈ o(n^2)` e se `n^2 ∈ o(n^2)`. Justifique as duas respostas por meio de razões ou limites.

**Para orientar a pesquisa:** em uma definição formal de little-o, observe atentamente a diferença entre **“existe uma constante c”** e **“para toda constante c positiva”**.


## Questão 4 — Comparando as quatro notações — 0,5 ponto

Organize o resultado de sua pesquisa em **um quadro comparativo** com as quatro notações:

```
O(g(n))     Ω(g(n))     Θ(g(n))     o(g(n))
```

O quadro deverá apresentar, para cada notação: (i) nome; (ii) tipo de limite ou relação; (iii) condição matemática necessária; e (iv) um exemplo simples de função que satisfaça a relação.

Em seguida, classifique as afirmações como **verdadeiras ou falsas**, sempre justificando:

**a)** Se `T(n) ∈ Θ(n)`, então `T(n) ∈ O(n)`.  
**b)** Se `T(n) ∈ O(n^2)`, então necessariamente `T(n) ∈ Θ(n^2)`.  
**c)** Se `T(n) ∈ o(n^2)`, então `T(n) ∈ O(n^2)`.  
**d)** Ômega é necessariamente a análise do melhor caso de um algoritmo.


# Parte B — Aplicação a algoritmos clássicos (1,5 ponto)

**Orientação para esta parte:** os algoritmos a seguir são exemplos tradicionais de livros introdutórios de Algoritmos. Pesquise seu funcionamento quando necessário. Para cada questão, não basta informar uma notação: mostre **como a estrutura do algoritmo gera seu custo**. Não é necessário demonstrar todos os casos com o mesmo rigor algébrico da Parte A, mas as conclusões devem ser justificadas.

## Questão 5 — Comparando afirmações de crescimento — 0,3 ponto

Considere as funções de custo abaixo:

```
A(n) = 5n + 2  
B(n) = 2n^2 + n  
C(n) = n \* log2 n
```

**a)** Escolha, para cada função, uma classificação em Theta e justifique pela presença dos termos dominantes.  
**b)** Determine se `A(n) ∈ o(n^2)`. Explique.  
**c)** Determine se `B(n) ∈ Ω(n^2)`. Explique.  
**d)** Explique, com base nesses exemplos, por que Big O e Theta não são sinônimos.


## Questão 6 — Busca do maior elemento (algoritmo iterativo) — 0,3 ponto

Um dos problemas mais tradicionais é encontrar o maior elemento de um vetor.

```
função encontrarMaior(vetor):  
    n = tamanho(vetor)  
    maior = vetor\[0\]  
  
    para i de 1 até n - 1:  
        se vetor\[i\] \> maior:  
            maior = vetor\[i\]  
  
    retornar maior
```

Considere `n \>= 1` e comparações de custo constante.

**a)** Simule a execução com `\[4, 9, 2, 7, 5\]`.  
**b)** Quantas vezes a comparação `vetor\[i\] \> maior` é executada? Escreva `C(n)`.  
**c)** Indique um limite superior e um limite inferior para o crescimento das comparações.  
**d)** Classifique o **tempo total** em Theta e justifique.


## Questão 7 — Busca linear: melhor caso e pior caso — 0,3 ponto

A **busca linear** procura um valor percorrendo um vetor a partir do primeiro elemento.

```
função buscaLinear(vetor, alvo):  
    n = tamanho(vetor)  
  
    para i de 0 até n - 1:  
        se vetor\[i\] == alvo:  
            retornar i  
  
    retornar -1
```

Considere `n \>= 1`.

**a)** Simule a busca em `\[3, 8, 2, 10, 6\]` para `alvo = 3` e para `alvo = 6`. Conte as comparações em cada situação.  
**b)** Qual é a quantidade de comparações no **melhor caso**? E no **pior caso**?  
**c)** Indique a classificação em Theta do melhor caso e do pior caso.  
**d)** Explique por que Ômega não deve ser confundido com “melhor caso” nem Big O com “pior caso”.


## Questão 8 — Busca binária: redução sucessiva da entrada — 0,3 ponto

A **busca binária** procura um elemento em um vetor **já ordenado**, eliminando aproximadamente metade do intervalo de busca a cada iteração.

```
função buscaBinaria(vetor, alvo):  
    inicio = 0  
    fim = tamanho(vetor) - 1  
  
    enquanto inicio \<= fim:  
        meio = (inicio + fim) // 2  
  
        se vetor\[meio\] == alvo:  
            retornar meio  
  
        se vetor\[meio\] \< alvo:  
            inicio = meio + 1  
        senao:  
            fim = meio - 1  
  
    retornar -1
```

Considere `n \>= 1`, acesso por índice em tempo constante e vetor previamente ordenado.

**a)** Simule a busca de `15` em `\[2, 4, 6, 8, 10, 12, 14, 16\]` e registre os intervalos examinados.  
**b)** Explique por que o número de iterações no pior caso cresce de forma logarítmica.  
**c)** Pesquise a complexidade em Theta do **pior caso** da busca binária e justifique sua resposta.  
**d)** Por que não devemos incluir o custo de **ordenar o vetor** nessa análise?


## Questão 9 — Selection Sort: comparação de elementos — 0,3 ponto

O **Selection Sort** ordena um vetor selecionando, a cada posição, o menor elemento da parte ainda não ordenada.

```
procedimento selectionSort(vetor):  
    n = tamanho(vetor)  
  
    para i de 0 até n - 2:  
        posMenor = i  
  
        para j de i + 1 até n - 1:  
            se vetor\[j\] \< vetor\[posMenor\]:  
                posMenor = j  
  
        trocar(vetor\[i\], vetor\[posMenor\])
```

Considere que `trocar` e as comparações possuem custo constante e `n \>= 2`.

**a)** Para `n = 5`, registre quantas comparações do teste `vetor\[j\] \< vetor\[posMenor\]` ocorrem em cada valor de `i`.  
**b)** Escreva a soma que representa essas comparações e deduza `C(n)`.  
**c)** Mostre como a fórmula encontrada ajuda a justificar que o tempo total pertence a `Θ(n^2)`.  
**d)** Determine se a contagem de comparações muda quando o vetor já está ordenado. Justifique usando o pseudocódigo.


# Parte C — Aplicação a um algoritmo recursivo clássico (0,5 ponto)

## Questão 10 — Merge Sort: divisão e conquista — 0,5 ponto

O **Merge Sort** é um algoritmo clássico de ordenação baseado na estratégia de **dividir e conquistar**. Sua ideia é dividir um vetor em duas metades, ordenar cada metade recursivamente e, por fim, intercalar as duas partes ordenadas.

Considere o seguinte pseudocódigo simplificado:

```
procedimento mergeSort(vetor):  
    n = tamanho(vetor)  
  
    se n \<= 1:  
        retornar vetor  
  
    meio = n // 2  
    esquerda = mergeSort(primeiraMetade(vetor))  
    direita = mergeSort(segundaMetade(vetor))  
  
    retornar intercalar(esquerda, direita)
```

**Hipóteses:** considere `n` potência de 2, duas chamadas recursivas sobre grupos de tamanho `n/2` e que `intercalar` percorre e escreve os `n` elementos do grupo atual, consumindo tempo proporcional a `n`. A construção das metades não deve acrescentar custo maior que o de intercalação.

**Pesquise o funcionamento do algoritmo e responda:**

**a)** Desenhe a árvore de divisões para `n = 8`, até alcançar vetores de tamanho 1.  
**b)** Quantos níveis de divisão são necessários para chegar aos casos-base? Relacione esse número a `log2 n`.  
**c)** Pesquise o significado da recorrência `T(n) = 2T(n/2) + c\*n`. Explique o papel de cada termo, sem precisar aplicar o Teorema Mestre.  
**d)** Explique por que o trabalho realizado nas intercalações de cada nível é proporcional a `n` e utilize isso para justificar a classificação `Θ(n \* log2 n)` do **tempo total**.  
**e)** Compare o crescimento do Merge Sort ao do Selection Sort, investigando se `n \* log2 n ∈ o(n^2)`. Explique o significado prático da conclusão para entradas grandes.


## Entrega

O trabalho pode ser feito em grupos de até 4 pessoas.

Entrega via link: [https://forms.gle/LxgXvhhmMpVtgfMTA](https://forms.gle/LxgXvhhmMpVtgfMTA)

Entrega até dia 27/11/2026
