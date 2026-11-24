# Gabarito — Avaliação do 2º Bimestre

**Disciplina:** Teoria da Computação  
**Universidade Estadual do Paraná (UNESPAR) — Campus de Apucarana**  
**Curso:** Ciência da Computação  
**Valor da avaliação:** 4,0 pontos  
**Conteúdos:** Análise de algoritmos, Big O, Ômega, Theta, little-o e recursão.

As resoluções abaixo seguem a numeração da avaliação. Neste material, `C(n)` representa a quantidade de execuções da operação básica indicada, enquanto `T(n)` representa o tempo total de execução. Pressupõe-se custo constante para operações elementares, conforme o enunciado da prova.

---

## Questão 1 — Registro de clientes (0,2 ponto)

**Tamanho da entrada:** `n` é o número de clientes no vetor.

**Operação básica:** avaliação da condição `clientes[i].ativo`.

**Simulação para quatro clientes, com dois ativos:**

| Índice `i` | Situação do cliente | Avaliações da condição |
|---:|---|---:|
| 0 | Ativo | 1 |
| 1 | Inativo | 1 |
| 2 | Ativo | 1 |
| 3 | Inativo | 1 |
| **Total** | **2 clientes ativos** | **4 avaliações** |

O laço visita todos os clientes, independentemente de estarem ativos. Portanto:

```text
C(n) = n
```

Como cada iteração realiza uma verificação e, eventualmente, um incremento — ambos de custo constante —, o tempo total cresce linearmente:

```text
T(n) ∈ O(n)
```

A quantidade de clientes ativos altera **quantas vezes `ativos` é incrementado**, mas não altera a quantidade de **avaliações da condição**, pois o laço não é interrompido.

---

## Questão 2 — Auditoria em duas etapas (0,3 ponto)

O algoritmo possui dois laços consecutivos, cada um com `n` iterações.

Para `n = 3`:

| Procedimento | Número de chamadas |
|---|---:|
| `validar` | 3 |
| `registrarLog` | 3 |
| **Total** | **6** |

A contagem conjunta é:

```text
C(n) = n + n = 2n
```

Como as chamadas têm custo constante, segue que:

```text
T(n) ∈ O(n)
```

O resultado **não é quadrático** porque o segundo laço começa somente quando o primeiro termina. Seus custos são **somados**, não multiplicados. Para obter `n²` execuções de uma operação interna, seria necessário, por exemplo, um laço de `n` iterações dentro de outro laço de `n` iterações.

---

## Questão 3 — Comparar sensores distintos (0,4 ponto)

O laço externo percorre `i` de `0` até `n − 2`. Para cada `i`, o laço interno começa em `i + 1` e termina em `n − 1`.

Para `n = 5`:

| `i` | Valores de `j` | Comparações |
|---:|---|---:|
| 0 | 1, 2, 3, 4 | 4 |
| 1 | 2, 3, 4 | 3 |
| 2 | 3, 4 | 2 |
| 3 | 4 | 1 |
| **Total** | | **10** |

A quantidade geral de comparações é:

```text
C(n) = (n − 1) + (n − 2) + ... + 2 + 1
     = n(n − 1)/2
     = (n² − n)/2
```

Para demonstrar o limite superior, observe que, para `n ≥ 1`:

```text
C(n) = n(n − 1)/2 ≤ n²/2
```

Assim, tomando `c = 1/2` e `n0 = 1`, temos `C(n) ∈ O(n²)`. Considerando os demais controles dos laços, que não aumentam a ordem de crescimento, o tempo total também satisfaz:

```text
T(n) ∈ O(n²)
```

O algoritmo não compara um sensor consigo mesmo porque **`j` começa em `i + 1`**, logo sempre vale `j > i`. Isso também evita contar duas vezes o mesmo par, como `(0, 1)` e `(1, 0)`.

---

## Questão 4 — Crescimento de capacidade (0,4 ponto)

O algoritmo começa com `capacidade = 1` e dobra esse valor enquanto ele for menor que `n`.

Para `n = 20`:

| Iteração | Capacidade antes | Capacidade depois |
|---:|---:|---:|
| 1 | 1 | 2 |
| 2 | 2 | 4 |
| 3 | 4 | 8 |
| 4 | 8 | 16 |
| 5 | 16 | 32 |

Ao alcançar `32`, a condição `32 < 20` é falsa. Portanto, o comando `capacidade = capacidade * 2` é executado **5 vezes**.

Após `k` multiplicações, a capacidade é `2^k`. A execução termina assim que:

```text
2^k ≥ n
```

A menor quantidade inteira de multiplicações que satisfaz essa condição é:

```text
C(n) = teto(log2 n), para n ≥ 1
```

Em particular, `C(1) = 0`. Para entradas suficientemente grandes, a contagem cresce proporcionalmente ao logaritmo do tamanho da entrada. Logo:

```text
T(n) ∈ O(log n)
```

O valor de `n` não precisa ser potência de dois: o algoritmo para na **primeira potência de dois maior ou igual a `n`**.

---

## Questão 5 — Limite quadrático (0,4 ponto)

Queremos demonstrar:

```text
C(n) = 2n² + 7n + 4 ∈ O(n²)
```

Pela definição de Big O, precisamos encontrar `c > 0` e `n0` tais que:

```text
0 ≤ 2n² + 7n + 4 ≤ c · n², para todo n ≥ n0.
```

Escolhemos `n0 = 1`. Como `n ≥ 1`, temos `n ≤ n²` e `1 ≤ n²`. Portanto:

```text
7n ≤ 7n²
 4 ≤ 4n²
```

Somando esses limites ao termo `2n²`:

```text
2n² + 7n + 4 ≤ 2n² + 7n² + 4n²
              ≤ 13n²
```

Logo, uma escolha válida é:

```text
c = 13
n0 = 1
```

Como `0 ≤ C(n) ≤ 13n²` para todo `n ≥ 1`, concluímos formalmente:

```text
C(n) ∈ O(n²)
```

As constantes escolhidas não precisam ser as menores possíveis; basta que satisfaçam a desigualdade para todos os valores previstos de `n`.

---

## Questão 6 — Notação Ômega: limite inferior (0,4 ponto)

A notação **Ômega**, escrita `Ω(g(n))`, expressa um **limite inferior assintótico**. Afirmar que `T(n) ∈ Ω(g(n))` significa que, a partir de determinado tamanho da entrada, `T(n)` é pelo menos tão grande quanto um múltiplo positivo fixo de `g(n)`.

**Definição formal:** existem constantes `c > 0` e `n0` tais que:

```text
0 ≤ c · g(n) ≤ T(n), para todo n ≥ n0.
```

- `c` é uma constante positiva fixa que multiplica a função de referência.
- `n0` estabelece a partir de qual tamanho de entrada a desigualdade precisa ser verdadeira.

**Ômega não é sinônimo de melhor caso.** A notação caracteriza o crescimento de uma função de custo definida previamente. É possível usar Ômega para estudar a função de pior caso, a de melhor caso ou outra medida de custo. A distinção entre melhor e pior caso está na **função analisada**, não na escolha da notação.

---

## Questão 7 — Notação Theta: limites dos dois lados (0,4 ponto)

A notação **Theta**, escrita `Θ(g(n))`, expressa um **limite assintótico ajustado**: `T(n)` cresce na mesma ordem de `g(n)`, considerando fatores multiplicativos constantes.

Isso exige simultaneamente:

- Um **limite inferior**, para assegurar que `T(n)` não cresça assintoticamente abaixo da ordem de `g(n)`.
- Um **limite superior**, para assegurar que `T(n)` não cresça assintoticamente acima da ordem de `g(n)`.

**Definição formal:** existem constantes positivas `c1`, `c2` e um valor `n0` tais que:

```text
0 ≤ c1 · g(n) ≤ T(n) ≤ c2 · g(n), para todo n ≥ n0.
```

- `c1` multiplica `g(n)` para estabelecer o **limite inferior**.
- `c2` multiplica `g(n)` para estabelecer o **limite superior**.
- `n0` é o ponto a partir do qual **as duas desigualdades** devem valer simultaneamente.

Portanto, dizer que `T(n) ∈ Θ(g(n))` equivale a afirmar que `T(n) ∈ O(g(n))` **e** `T(n) ∈ Ω(g(n))`, usando a mesma função de referência `g(n)`.

---

## Questão 8 — Notação little-o: crescimento estritamente menor (0,4 ponto)

A notação **little-o**, escrita `o(g(n))`, representa um **limite superior assintótico estrito**. Ela indica que `T(n)` se torna insignificante em relação a `g(n)` quando `n` cresce indefinidamente.

A diferença principal está nas constantes usadas na definição:

**Big O:** basta que **exista uma** constante `c > 0` para a qual a desigualdade funcione a partir de algum `n0`:

```text
0 ≤ T(n) ≤ c · g(n), para todo n ≥ n0.
```

**Little-o:** a desigualdade deve funcionar **para toda** constante positiva `c`; o valor de `n0` pode depender da constante escolhida:

```text
Para todo c > 0, existe n0 tal que
0 ≤ T(n) < c · g(n), para todo n ≥ n0.
```

Quando `g(n) > 0` para valores suficientemente grandes e o limite da razão existe, a condição:

```text
lim (n → ∞) [T(n)/g(n)] = 0
```

mostra que `T(n)` cresce estritamente mais devagar do que `g(n)`. Por exemplo, `n ∈ o(n²)` porque `n/n² = 1/n` tende a zero. Em contrapartida, `n² ∉ o(n²)`, pois `n²/n² = 1`, e não zero.

Assim, **toda relação little-o também fornece uma relação Big O, mas a recíproca não é necessariamente verdadeira**.

---

## Questão 9 — Avisos recursivos (0,4 ponto)

O procedimento envia um aviso para `n` e depois repete o processo com `n − 1`, até alcançar o caso-base `n = 0`.

**Simulação para `n = 4`:**

```text
emitirAvisos(4) → enviarAviso(4)
  emitirAvisos(3) → enviarAviso(3)
    emitirAvisos(2) → enviarAviso(2)
      emitirAvisos(1) → enviarAviso(1)
        emitirAvisos(0) → retorna
```

Há **4 chamadas a `enviarAviso`**.

Contando apenas esses envios, a recorrência é:

```text
C(0) = 0
C(n) = C(n − 1) + 1, para n ≥ 1.
```

**Resolução por expansão:**

```text
C(n) = C(n − 1) + 1
     = C(n − 2) + 1 + 1
     = C(n − 3) + 1 + 1 + 1
     = ...
     = C(0) + n
     = n.
```

Como existe uma quantidade constante de instruções em cada chamada recursiva, o tempo total, para `n ≥ 1`, cresce linearmente:

```text
T(n) ∈ O(n)
```

A execução realiza `n + 1` chamadas ao procedimento, incluindo a chamada final com `n = 0`, mas somente `n` dessas chamadas executam `enviarAviso`.

---

## Questão 10 — Merge Sort e árvore de recursão (0,7 ponto)

O Merge Sort divide o vetor em duas metades, ordena recursivamente cada metade e intercala os resultados. Neste exercício, `C(n)` conta **elementos processados durante as intercalações**.

**Árvore de recursão para `n = 8`:**

```text
                           8           → intercala 8 elementos
                        /     \
                       4       4        → 2 × 4 = 8 elementos
                     /  \     /  \
                    2    2   2    2      → 4 × 2 = 8 elementos
                   /\   /\  /\   /\
                  1  1 1  1 1  1 1  1     → casos-base: 0 intercalações
```

**Trabalho de intercalação por nível:**

| Nível | Subproblemas | Elementos por intercalação | Total no nível |
|---:|---:|---:|---:|
| 0 | 1 | 8 | 8 |
| 1 | 2 | 4 | 8 |
| 2 | 4 | 2 | 8 |
| 3 | 8 | 1 | 0 (casos-base) |
| **Total** | | | **24** |

Portanto, `C(8) = 8 + 8 + 8 = 24 = 8 · log2 8`.

**Recorrência da contagem:**

```text
C(1) = 0
C(n) = 2C(n/2) + n, para n ≥ 2 e n potência de 2.
```

O termo `2C(n/2)` representa o trabalho das duas metades; o termo `n` representa os elementos processados na intercalação do subproblema atual.

**Resolução por expansão:**

```text
C(n) = 2C(n/2) + n
     = 2[2C(n/4) + n/2] + n
     = 4C(n/4) + 2n
     = 8C(n/8) + 3n
     = ...
     = 2^k C(n/2^k) + k · n.
```

Como `n = 2^k`, temos `k = log2 n` e `n/2^k = 1`. Substituindo o caso-base `C(1) = 0`:

```text
C(n) = n · C(1) + n · log2 n
     = n · log2 n.
```

A árvore tem `log2 n` níveis com intercalações: em cada nível, os tamanhos dos subproblemas somam `n`. O nível adicional de folhas contém somente casos-base, sem intercalação.

**Classificação da contagem:**

```text
C(n) ∈ O(n log n)
```

**Classificação do tempo total:** o processamento de cada subproblema, incluindo as atividades de divisão e intercalação, tem custo no máximo proporcional ao tamanho do subproblema, conforme as hipóteses. Por isso, cada nível custa `O(n)`; existem `log2 n` níveis não triviais e `n` casos-base de custo constante. Assim:

```text
T(n) ∈ O(n log n)
```

Esse resultado descreve o crescimento do algoritmo sob as condições estabelecidas na questão, para `n` potência de dois e `n ≥ 2`.

---

## Resumo das respostas

| Questão | Resultado principal |
|---:|---|
| **1** | `C(n) = n`; tempo `O(n)` |
| **2** | `C(n) = 2n`; tempo `O(n)` |
| **3** | `C(n) = n(n − 1)/2`; tempo `O(n²)` |
| **4** | `C(n) = teto(log2 n)`; tempo `O(log n)` |
| **5** | `c = 13`, `n0 = 1`; `C(n) ∈ O(n²)` |
| **6** | Ômega: limite inferior assintótico |
| **7** | Theta: limites superior e inferior da mesma ordem |
| **8** | little-o: limite superior estrito; razão tende a zero |
| **9** | `C(n) = n`; tempo `O(n)` |
| **10** | `C(n) = n log2 n`; tempo `O(n log n)` |

**Fim do gabarito.**
