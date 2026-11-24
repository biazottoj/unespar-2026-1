# Gabarito comentado — Revisão de Teoria da Computação (30 questões)

**Uso:** apoio ao professor para correção coletiva, exposição no quadro e atribuição de crédito parcial.  
**Documento correspondente:** `revisao_analise_algoritmos_30_questoes.md`  
**Abrangência:** crescimento de funções, contagem de operações, Big O, Ômega, Theta, little-o, algoritmos iterativos e recursivos.

> **Como conduzir a correção:** peça primeiro que os alunos identifiquem `n` e a operação básica; faça uma simulação pequena com a turma; generalize para `C(n)`; e só então apresente `O(...)`, `Omega(...)`, `Theta(...)` ou `o(...)`. Quando a questão pedir demonstração, explicite as constantes e a validade da desigualdade para todos os `n` a partir de `n0`.

## Recapitulação para o quadro: as quatro notações

```text
Big O:     T(n) <= c*g(n)                       (limite superior)
Omega:     T(n) >= c*g(n)                       (limite inferior)
Theta:     c1*g(n) <= T(n) <= c2*g(n)           (ambos os limites)
little-o:  T(n) < c*g(n) para QUALQUER c>0,    (limite estrito)
           após um n0 que pode depender de c.
```

Nas três primeiras definições, basta **encontrar** constantes positivas apropriadas. Em little-o, um único `c` não é suficiente. Para funções não negativas, um teste útil de little-o é verificar se `T(n)/g(n)` tende a `0` quando `n` cresce indefinidamente (com `g(n)>0` eventualmente).

**Atenção aos custos:** `C(n)` contabiliza uma operação especificada; `T(n)` contabiliza todas as etapas. Quando todos os laços executam trabalho constante por iteração, costuma ser possível justificar que os dois crescem na mesma ordem. Não trate isso como uma igualdade numérica automática.

**Atenção aos casos:** a função de custo pode ser de melhor caso, pior caso ou um caso fixo. Big O, Omega e Theta não são nomes para esses casos; são relações entre funções.

---

# Tópico 1 — Tamanho da entrada e operação básica

## Questão 1 — Registro de clientes

**Resposta esperada:** `n` é o número de clientes; `C(n)=n` avaliações de `clientes[i].ativo`; tempo total `O(n)`.

**Passo a passo:**

1. Para `n=4`, o índice percorre `0,1,2,3`.
2. A expressão `clientes[i].ativo` é avaliada **uma vez em cada iteração**, independentemente do valor booleano encontrado.
3. Uma simulação possível é `[ativo, inativo, ativo, inativo]`: ocorrem 4 testes e apenas 2 incrementos de `ativos`.
4. Generalizando, `C(n)=1+1+...+1` (n parcelas), isto é, `n`.
5. As inicializações e os testes dos laços têm custo constante por iteração. Portanto, `T(n) ∈ O(n)`; sob o modelo adotado, também `Theta(n)`.

**Explique no quadro:** a quantidade de clientes ativos modifica **quantas vezes `ativos = ativos + 1` executa**, mas não modifica o número de testes selecionados como operação básica.

**Crédito parcial:** reconhecer `n`, fazer 4 testes na simulação, escrever `C(n)=n` e justificar `O(n)`.

## Questão 2 — Consulta de estoque

**Resposta esperada:** `C(n)=1` acesso; `T(n) ∈ O(1)`.

**Passo a passo:**

1. `n` é a quantidade de produtos armazenados no vetor.
2. A operação básica é ler `estoque[posicao]`.
3. Com `n=5`, ocorre 1 acesso. Com `n=5000`, também 1 acesso.
4. A posição é conhecida e válida: não há procura por todos os elementos.
5. Assim, `C(n)=1`. Uma constante `c=1` com `n0=1` prova `C(n) ∈ O(1)`.

**Explique no quadro:** a expressão `estoque[posicao]` acessa diretamente uma posição; o custo independe da quantidade de posições do vetor, conforme o modelo RAM utilizado. Uma busca por valor, sem índice conhecido, seria outro algoritmo.

**Crédito parcial:** distinguir acesso direto de busca e identificar custo constante.

---

# Tópico 2 — Um laço simples

## Questão 3 — Média de temperaturas

**Resposta esperada:** `C(n)=n` somas, `T(n) ∈ O(n)`.

**Simulação:** com 5 temperaturas, `soma = soma + temperaturas[i]` executa para `i=0,1,2,3,4`: cinco vezes.

**Generalização:** para uma lista de `n` temperaturas, o laço percorre `n` elementos, então `C(n)=n`. O algoritmo ainda calcula uma divisão após o laço; essa operação acrescenta uma constante. Uma expressão representativa da contagem simplificada é `n+1` operações relevantes, logo `O(n)`.

**Fala sugerida:** “Não precisamos multiplicar `n` pela divisão. Ela ocorre uma única vez, depois de todas as somas.”

**Crédito parcial:** 5 somas na entrada pequena, `n` no geral, `O(n)` com justificativa.

## Questão 4 — Procurar sem interromper

**Resposta esperada:** `C(n)=n` comparações em qualquer entrada; `T(n) ∈ O(n)`.

**Simulação para `n=4`:** mesmo que o procurado esteja na posição 0, o algoritmo testa as posições `0,1,2,3`: 4 comparações. Se não estiver presente, testa igualmente `0,1,2,3`: 4 comparações.

**Generalização:** `C(n)=n`, pois não há comando de interrupção ou retorno dentro do laço. As operações condicionais extras são de custo constante por iteração, portanto `T(n)` é linear.

**Comparação solicitada:** uma busca linear com `retornar i` após o primeiro acerto pode executar 1 comparação no melhor caso e até `n` no pior caso. Neste algoritmo, mesmo após encontrar o valor, a execução continua.

**Crédito parcial:** destacar a ausência de retorno antecipado; indicar 4 e 4; identificar `n` e `O(n)`.

---

# Tópico 3 — Laços consecutivos

## Questão 5 — Auditoria em duas etapas

**Resposta esperada:** `n` chamadas de `validar`, `n` de `registrarLog`; `C(n)=2n`; `O(n)`.

**Simulação para `n=3`:**

| Etapa | Chamadas |
|---|---:|
| Validar três registros | 3 |
| Registrar três logs | 3 |
| **Total** | **6** |

**Generalização:** o primeiro laço faz `n` chamadas, depois termina. O segundo também faz `n` chamadas. Como são consecutivos, somamos `n+n=2n`. O fator multiplicativo 2 é constante, logo o crescimento é linear.

**Fala sugerida:** “Dois laços não significam, por si só, `n^2`. Só multiplicamos quantidades quando um laço repete integralmente o outro.”

**Crédito parcial:** 3+3, `2n`, `O(n)`.

## Questão 6 — Rotina com duas escalas

**Resposta esperada:** `C(n)=n+n^2`, `T(n) ∈ O(n^2)`.

**Simulação para `n=3`:**

- Primeiro laço: índices `0,1,2`, portanto 3 chamadas a `verificar`.
- Segundo laço: de `0` até `n*n-1 = 8`, portanto 9 chamadas a `registrar`.
- Total: `C(3)=3+9=12` chamadas.

**Generalização:** o primeiro laço tem `n` iterações, o segundo `n^2`, então `C(n)=n+n^2`.

**Prova opcional de Big O:** para `n>=1`, `n<=n^2`; logo `n+n^2<=2n^2`. Escolhendo `c=2`, `n0=1`, demonstramos `C(n) ∈ O(n^2)`.

**Crédito parcial:** contagens 3 e 9; soma correta; termo dominante `n^2`.

---

# Tópico 4 — Laços aninhados

## Questão 7 — Produtos e filiais

**Resposta esperada:** `C(4)=16`, `C(n)=n^2`, `T(n) ∈ O(n^2)`.

**Simulação:** há quatro produtos. Para cada produto são examinadas as quatro filiais. As chamadas se distribuem como `4+4+4+4=16`.

**Generalização:** o laço externo repete `n` vezes, e para cada repetição o interno realiza `n` chamadas. Assim, `C(n)=n*n=n^2`.

**Prova simples:** `C(n)=1*n^2`; tome `c=1`, `n0=1` para a contagem. O custo total também é `O(n^2)` porque o trabalho interno e o controle dos laços são constantes por iteração.

**Crédito parcial:** contagem 16, fórmula `n^2`, explicação do aninhamento.

## Questão 8 — Três dimensões

**Resposta esperada:** `C(2)=8`, `C(n)=n^3`, `T(n) ∈ O(n^3)`.

**Simulação:** para cada uma das 2 equipes, há 2 turnos; para cada combinação equipe–turno, há 2 salas. Portanto, `2*2*2=8` chamadas.

**Generalização:** `n` escolhas de equipe, `n` de turno e `n` de sala; logo `C(n)=n*n*n=n^3`.

**Comparação com a questão 7:** naquela tínhamos pares `(produto, filial)`, aqui triplas `(equipe, turno, sala)`. A terceira dimensão acrescenta um fator `n`.

**Crédito parcial:** 8 chamadas, `n^3`, `O(n^3)` e comparação correta.

---

# Tópico 5 — Laços triangulares

## Questão 9 — Comparar sensores distintos

**Resposta esperada:** `C(5)=10`, `C(n)=n(n-1)/2`, `T(n) ∈ O(n^2)`.

**Tabela da simulação:**

| `i` | Valores de `j` | Comparações |
|---:|---|---:|
| 0 | 1,2,3,4 | 4 |
| 1 | 2,3,4 | 3 |
| 2 | 3,4 | 2 |
| 3 | 4 | 1 |
| **Total** | | **10** |

**Generalização:** `C(n)=(n-1)+(n-2)+...+1 = n(n-1)/2`.

**Demonstração de Big O:** para `n>=1`, `n-1<=n`, portanto `C(n)<=n^2/2`. Escolha `c=1/2` e `n0=1` para a contagem; o tempo total é quadrático por causa das iterações do laço interno e dos controles associados.

**Por que não compara consigo mesmo?** Porque o laço interno começa em `j=i+1`, nunca em `j=i`; também não visita pares já examinados em ordem inversa.

**Crédito parcial:** tabela 4,3,2,1; soma 10; fórmula; `O(n^2)`.

## Questão 10 — Intervalos possíveis

**Resposta esperada:** `C(4)=10`, `C(n)=n(n+1)/2`, `T(n) ∈ O(n^2)`.

**Simulação:**

| `inicio` | Valores de `fim` | Chamadas |
|---:|---|---:|
| 0 | 0,1,2,3 | 4 |
| 1 | 1,2,3 | 3 |
| 2 | 2,3 | 2 |
| 3 | 3 | 1 |
| **Total** | | **10** |

**Generalização:** `C(n)=n+(n-1)+...+1=n(n+1)/2`.

**Prova:** para `n>=1`, `n+1<=2n`, logo `C(n)<=n^2`. Um limite superior válido usa `c=1`, `n0=1`.

**Diferença da questão 9:** nesta questão, `j` ou `fim` **pode ser igual a** `i` ou `inicio`; por isso, os `n` intervalos de tamanho 1 são incluídos. A questão 9 registra somente pares com índices diferentes.

**Crédito parcial:** 4+3+2+1; fórmula; diferença da inclusão da diagonal; `O(n^2)`.

---

# Tópico 6 — Laços logarítmicos

## Questão 11 — Redução de lotes

**Resposta esperada:** `C(n)=piso(log2 n)` para `n>=1`; `O(log n)` para `n>=2`.

**Simulação `n=16`:** `16 -> 8 -> 4 -> 2 -> 1`. O comando `etapas = etapas + 1` executa 4 vezes.

**Simulação `n=17`:** `17 -> 8 -> 4 -> 2 -> 1`. O mesmo comando executa 4 vezes.

**Por que a função é logarítmica?** Após `k` divisões inteiras por 2, o valor é `piso(n/2^k)`. A condição `restantes>1` deixa de ser verdadeira quando se chega a 1 ou menos. O número exato de iterações é `piso(log2 n)`, para `n>=1`.

**Prova de limite superior:** `piso(log2 n)<=log2 n` para `n>=2`; tome `c=1`, `n0=2` para a contagem. O tempo total possui o mesmo crescimento, somado ao custo constante das inicializações.

**Atenção:** `n=1` executa zero iterações; a classificação assintótica se refere ao comportamento para tamanhos grandes.

**Crédito parcial:** duas sequências corretas; 4 e 4; função com piso; `O(log n)`.

## Questão 12 — Crescimento de capacidade

**Resposta esperada:** `C(n)=teto(log2 n)` para `n>=1`; `O(log n)` para `n>=2`.

**Simulação `n=20`:**

```text
capacidade: 1 -> 2 -> 4 -> 8 -> 16 -> 32
```

O comando `capacidade = capacidade * 2` é executado 5 vezes; após a quinta, `32<20` é falso.

**Generalização:** após `k` multiplicações, `capacidade=2^k`. Procuramos o menor inteiro `k` com `2^k>=n`, isto é, `C(n)=teto(log2 n)`.

**Prova:** para `n>=2`, `teto(log2 n)<=log2 n+1<=2log2 n`. Assim, `c=2`, `n0=2` provam `C(n) ∈ O(log n)`; como as demais operações custam no máximo uma constante por iteração, o tempo total também é logarítmico.

**Crédito parcial:** 5 dobramentos, `teto(log2 n)` e justificativa.

---

# Tópico 7 — Crescimento n log n

## Questão 13 — Auditoria por escalas

**Resposta esperada:** `C(n)=n*(piso(log2 n)+1)`, `O(n log n)` para `n>=2`.

**Simulação `n=8`:** para cada elemento, `escala` assume `1,2,4,8` (quatro testes). Como há 8 elementos, são `8*4=32` chamadas a `verificar`.

**Generalização:** as potências de 2 que satisfazem `2^k<=n` são as de expoentes `k=0,1,...,piso(log2 n)`. Portanto, são `piso(log2 n)+1` chamadas por elemento, multiplicadas por `n`.

**Justificativa de Big O:** para `n>=2`, `piso(log2 n)+1<=log2 n+1<=2log2 n`. Logo, `C(n)<=2n log2 n`, com `c=2` e `n0=2`.

**Atenção:** a condição é `escala<=n`, então a escala 8 entra quando `n=8`. Se fosse `<n`, entrariam apenas `1,2,4`.

**Crédito parcial:** 4 escalas, 32 chamadas; fórmula; `O(n log n)`.

## Questão 14 — Redução por registro

**Resposta esperada:** `C(n)=n*piso(log2 n)`, `O(n log n)`.

**Simulação `n=16`:** para cada `i`, o valor de `tamanho` é testado em `16,8,4,2` e o laço termina ao chegar a 1. São 4 chamadas a `comparar` por elemento. Como existem 16 elementos, `C(16)=16*4=64`.

**Generalização:** cada um dos `n` elementos produz `piso(log2 n)` chamadas, logo `C(n)=n*piso(log2 n)`.

**Prova de Big O:** como `piso(log2 n)<=log2 n` para `n>=2`, `C(n)<=n log2 n`; escolha `c=1`, `n0=2`.

**Por que não é quadrático?** O laço interno **não percorre n posições**; ele reduz `tamanho` pela metade a cada repetição, realizando apenas ordem de `log n` chamadas.

**Crédito parcial:** 4/64, fórmula e explicação do crescimento logarítmico interno.

---

# Tópico 8 — Crescimento e termo dominante

## Questão 15 — Simplificação justificada

**Resposta esperada:** `C(n) ∈ O(n^3)`.

**Passo 1 — Identificar a referência:** o termo dominante de `7n^3+5n^2+12` é `7n^3`. Escolhemos `g(n)=n^3`.

**Passo 2 — Montar a desigualdade:** queremos `7n^3+5n^2+12 <= c*n^3`.

**Passo 3 — Usar `n>=1`:**

```text
n^2 <= n^3
1   <= n^3
```

Assim:

```text
7n^3 + 5n^2 + 12
<= 7n^3 + 5n^3 + 12n^3
= 24n^3.
```

**Passo 4 — Escolher constantes e concluir:** `c=24`, `n0=1`. Como a função é não negativa para `n>=1`, ela pertence a `O(n^3)`.

**Crédito parcial:** termo dominante, desigualdades por parcela e constantes válidas.

## Questão 16 — Comparar soluções

**Ordem de crescimento:** `A(n)`, depois `D(n)`, depois `B(n)`.

| Função | Crescimento principal | Big O mais informativo dentre as opções |
|---|---|---|
| `20n+100` | Linear | `O(n)` |
| `n*log2 n` | Linearítmico | `O(n log n)` |
| `2n^2+1` | Quadrático | `O(n^2)` |

**Justificativa:** `log n` cresce sem limite, então `n log n` eventualmente cresce mais do que qualquer múltiplo fixo de `n`; por outro lado, `log n/n` tende a 0, então `n log n` cresce menos do que `n^2` em termos assintóticos. O termo dominante de cada polinômio determina sua ordem.

**A classificação não prevê o vencedor para todo `n`:** as constantes e os valores pequenos da entrada podem inverter o desempenho prático. Por exemplo, para `n=2`, `A(2)=140` e `B(2)=9`, apesar de `A` ter crescimento assintótico mais favorável.

**Crédito parcial:** ordem correta, Big O de cada função e ressalva sobre constantes/entradas pequenas.

---

# Tópico 9 — Demonstração formal de Big O

## Questão 17 — Limite linear

**Queremos provar:** `C(n)=4n+9 ∈ O(n)`.

1. Escolhemos `g(n)=n`.
2. A desigualdade procurada é `4n+9<=c*n`.
3. Se `n>=1`, então `9<=9n`.
4. Portanto, `4n+9<=4n+9n=13n`.
5. Podemos adotar `c=13` e `n0=1`.
6. Como `0<=4n+9<=13n` para todo `n>=1`, a definição foi satisfeita.

**Fala sugerida:** “Escolhi constantes que funcionam; não preciso encontrar a menor constante possível.”

**Crédito parcial:** desigualdade, substituição `9<=9n`, escolha de `c/n0` e conclusão.

## Questão 18 — Limite quadrático

**Queremos provar:** `C(n)=2n^2+7n+4 ∈ O(n^2)`.

1. Escolhemos `g(n)=n^2`.
2. Para `n>=1`, `n<=n^2` e `1<=n^2`.
3. Logo, `7n<=7n^2` e `4<=4n^2`.
4. Somando as parcelas:

```text
2n^2 + 7n + 4
<= 2n^2 + 7n^2 + 4n^2
= 13n^2.
```

5. Constantes válidas: `c=13`, `n0=1`.
6. Portanto `C(n) ∈ O(n^2)`.

**Crédito parcial:** limitar ambos os termos, escolher 13 e 1 e escrever a conclusão.

---

# Tópico 10 — Limite ajustado e afirmações falsas

## Questão 19 — Afirmação impossível

**Resposta:** a afirmação `n^2+2n ∈ O(n)` é **falsa**.

**Prova por contradição:** suponha existirem constantes `c>0`, `n0` tais que `n^2+2n<=c*n` para todo `n>=n0`. Para `n>0`, dividindo por `n`, teríamos:

```text
n + 2 <= c.
```

Entretanto, podemos escolher `n>max(n0,c)`. Nesse caso, `n+2>c`, contradizendo a desigualdade. Logo, não existe constante positiva fixa `c` que sustente esse Big O.

**Fala sugerida:** “Não basta tentar dois valores de c e concluir que é falso. Precisamos mostrar por que **nenhuma** constante fixa serve.”

**Crédito parcial:** hipótese, divisão válida para `n>0`, contradição com n arbitrariamente grande.

## Questão 20 — Dois limites superiores

**Primeira prova, `O(n)`:** para `n>=1`, `1<=n`, portanto `6n+1<=6n+n=7n`. Tome `c=7`, `n0=1`.

**Segunda prova, `O(n^2)`:** para `n>=1`, `n<=n^2`. Logo, `6n+1<=7n<=7n^2`. Tome `c=7`, `n0=1`.

**Interpretação:** ambas são verdadeiras, porque Big O só exige um limite superior. `O(n)` é mais informativo neste caso, pois descreve uma função de referência com menor crescimento do que `n^2`.

**Crédito parcial:** as duas provas, constantes adequadas e distinção entre limites válidos e ajustados.

---

# Tópico 11 — Notação Ômega

## Questão 21 — Ômega quadrático

**Queremos provar:** `T(n)=2n^2+3n+1 ∈ Omega(n^2)`.

1. Escolha `g(n)=n^2`.
2. A condição requerida é `c*n^2 <= 2n^2+3n+1`.
3. Como `3n+1>=0` para `n>=1`, temos `2n^2 <= 2n^2+3n+1`.
4. Tome `c=2`, `n0=1`.
5. Portanto, `T(n) ∈ Omega(n^2)`.

**Explique no quadro:** os termos adicionais são não negativos; aumentam o valor da função, logo não prejudicam um limite **inferior**.

**Crédito parcial:** direção correta da desigualdade, `c=2` e `n0=1`, justificativa.

## Questão 22 — Ômega aplicado a um algoritmo

**Resposta esperada:** `C(n)=n` gravações; `C(n) ∈ Omega(n)` e `T(n) ∈ Omega(n)`.

1. O laço executa de `0` até `n-1`, realizando `n` chamadas a `gravar`.
2. A função de contagem é `C(n)=n`.
3. Para todo `n>=1`, `1*n<=n`; basta escolher `c=1`, `n0=1`.
4. Como cada gravação tem custo constante **positivo**, existem unidades positivas de custo para cada uma das `n` chamadas. Logo, o tempo total também está limitado inferiormente por um múltiplo positivo de `n`.

**Ponto importante:** uma prova para a contagem de gravações não significa que `T(n)=n` exatamente. Significa que esse trabalho obrigatoriamente ocorre e fornece um limite inferior do tempo.

**Crédito parcial:** `C(n)=n`, desigualdade de Omega, argumento para custo total.

---

# Tópico 12 — Notação Theta

## Questão 23 — Theta linear

**Queremos provar:** `C(n)=4n+7 ∈ Theta(n)`.

**Limite inferior:** como `7>=0`, `4n<=4n+7`; podemos escolher `c1=4`.

**Limite superior:** para `n>=1`, `7<=7n`; então `4n+7<=4n+7n=11n`; podemos escolher `c2=11`.

**Desigualdade conjunta:**

```text
4n <= 4n + 7 <= 11n, para todo n>=1.
```

Portanto `c1=4`, `c2=11`, `n0=1` demonstram `Theta(n)`.

**Crédito parcial:** ambas as desigualdades, mesmas referências `n`, constantes corretas.

## Questão 24 — Theta em laço triangular

**Resposta esperada:** `C(n)=n(n+1)/2 ∈ Theta(n^2)`.

**Simulação `n=4`:**

| `i` | `j` | Execuções de `processar` |
|---:|---|---:|
| 0 | 0 | 1 |
| 1 | 0,1 | 2 |
| 2 | 0,1,2 | 3 |
| 3 | 0,1,2,3 | 4 |
| **Total** | | **10** |

**Generalização:** `C(n)=1+2+...+n=n(n+1)/2`.

**Limite inferior:** para `n>=1`, `n+1>=n`. Portanto:

```text
C(n)=n(n+1)/2 >= n^2/2.
```

**Limite superior:** para `n>=1`, `n+1<=2n`. Então:

```text
C(n)=n(n+1)/2 <= n^2.
```

**Conclusão formal:**

```text
(1/2)*n^2 <= C(n) <= 1*n^2, para n>=1.
```

Podemos escolher `c1=1/2`, `c2=1`, `n0=1`. Logo, `C(n) ∈ Theta(n^2)`.

**Tempo total:** a quantidade de iterações internas é quadrática e cada uma tem custo constante positivo; o controle dos laços acrescenta trabalho de ordem no máximo quadrática. Assim, `T(n) ∈ Theta(n^2)` sob as hipóteses do enunciado.

**Crédito parcial:** tabela, fórmula, prova inferior, prova superior, conexão com `T(n)`.

---

# Tópico 13 — Notação little-o

## Questão 25 — Comparação linear × quadrática

**Resposta:** `3n+4 ∈ o(n^2)` é **verdadeira**.

**Pela razão entre funções:**

```text
(3n+4)/n^2 = 3/n + 4/n^2.
```

Quando `n` cresce, tanto `3/n` quanto `4/n^2` tendem a 0. Logo, a razão tende a 0, o que prova a relação little-o.

**Demonstração diretamente pela definição (opcional):** para `n>=1`, `3n+4<=7n`. Dado **qualquer** `c>0`, escolha um inteiro `n0>max(1,7/c)`. Então, para todo `n>=n0`, `7n<c*n^2`. Assim:

```text
0 <= 3n+4 <= 7n < c*n^2.
```

**Explique:** o `n0` é escolhido depois que alguém informa `c`. Isso é permitido em little-o; não existe apenas um `c` fixado uma vez para sempre.

**Crédito parcial:** razão correta, limite zero e interpretação estrita.

## Questão 26 — Mesmo crescimento ou estritamente menor?

**(a) `n^2 ∈ o(n^2)` — falsa.** A razão `n^2/n^2=1`, que não tende a 0. Outra maneira: para `c=1/2`, a exigência `n^2<c*n^2` falha para todo `n>0`.

**(b) `n^2 ∈ o(n^3)` — verdadeira.** Para `n>0`, a razão `n^2/n^3=1/n`, que tende a 0. Logo, `n^2` cresce estritamente mais devagar do que `n^3`.

**Comparação com Big O:** `n^2 ∈ O(n^2)` é verdadeiro (com `c=1`), embora `n^2 ∉ o(n^2)`. Isso mostra por que as notações não são equivalentes.

**Crédito parcial:** análise das duas razões e distinção conceitual.

---

# Tópico 14 — Recursão linear

## Questão 27 — Avisos recursivos

**Resposta esperada:** `C(n)=n` chamadas a `enviarAviso`; `T(n) ∈ O(n)`.

**Simulação para `n=4`:**

```text
emitirAvisos(4) -> enviarAviso(4)
emitirAvisos(3) -> enviarAviso(3)
emitirAvisos(2) -> enviarAviso(2)
emitirAvisos(1) -> enviarAviso(1)
emitirAvisos(0) -> caso-base: não envia
```

**Recorrência da contagem:**

```text
C(0) = 0
C(n) = 1 + C(n-1), para n>0.
```

**Expansão:** `C(n)=1+[1+C(n-2)]=2+C(n-2)=...=n+C(0)=n`.

**Classificação:** cada chamada tem custo constante, incluindo o teste do caso-base. Existem `n+1` ativações, portanto `T(n) ∈ O(n)` (também `Theta(n)` para `n>=1`).

**Crédito parcial:** quatro avisos, caso-base correto, recorrência e solução.

## Questão 28 — Fatorial recursivo

**Resposta esperada:** `C(n)=n-1` multiplicações para `n>=1`; `O(n)` sob aritmética de custo constante.

**Simulação `n=5`:**

```text
fatorial(5) -> 5 * fatorial(4)
fatorial(4) -> 4 * fatorial(3)
fatorial(3) -> 3 * fatorial(2)
fatorial(2) -> 2 * fatorial(1)
fatorial(1) -> retorna 1
```

Há 4 multiplicações (`5*`, `4*`, `3*`, `2*`).

**Recorrência para multiplicações:**

```text
C(1)=0
C(n)=C(n-1)+1, para n>1.
```

**Resolução:** `C(n)=n-1`. O número de chamadas/ativações é `n`, porque a ativação `fatorial(1)` existe, embora não multiplique. Cada ativação tem custo constante, então o tempo total é `O(n)`; para `n>=2`, `C(n)` também é `Theta(n)`.

**Observação:** se analisássemos custos reais de multiplicar inteiros arbitrariamente grandes, precisaríamos de outro modelo; o enunciado especifica custo constante.

**Crédito parcial:** 4 multiplicações, fórmula `n-1`, distinção entre chamadas e multiplicações e `O(n)`.

---

# Tópico 15 — Recursão por divisão

## Questão 29 — Busca recursiva por redução

**Resposta esperada:** `C(n)=log2 n` para `n=2^k`; `Theta(log2 n)` para `n>=2`.

**Sequência para `n=16`:**

```text
16 -> processarNivel() -> 8
 8 -> processarNivel() -> 4
 4 -> processarNivel() -> 2
 2 -> processarNivel() -> 1
 1 -> caso-base
```

São 4 chamadas à operação `processarNivel`.

**Recorrência:**

```text
C(1)=0
C(n)=C(n/2)+1, para n>1.
```

**Expansão:** `C(n)=1+C(n/2)=2+C(n/4)=...=k+C(1)` quando `n/2^k=1`. Como `2^k=n`, `k=log2 n`, e `C(n)=log2 n`.

**Prova Theta:** com `g(n)=log2 n`, para as entradas consideradas e `n>=2` vale:

```text
1*g(n) <= C(n) <= 1*g(n).
```

Escolha `c1=1`, `c2=1`, `n0=2` no domínio `n=2^k`. O tempo total também é `Theta(log n)` porque cada nível adiciona apenas custo constante.

**Crédito parcial:** 4 níveis úteis, recorrência, expansão e justificativa Theta.

## Questão 30 — Merge Sort e árvore de recursão

**Resposta esperada para o número de elementos processados nas intercalações:** `C(n)=n*log2 n` para `n=2^k`, `n>=1`. O tempo total pertence a `O(n log n)` e a `Theta(n log n)` sob as hipóteses do enunciado.

**Passo 1 — Desenhar a árvore com `n=8`:**

```text
                   [8]
                 /     \
               [4]     [4]
              /  \     /  \
            [2]  [2] [2]  [2]
            /\    /\   /\   /\
          [1][1][1][1][1][1][1][1]
```

Os `[1]` representam casos-base, sem intercalação. O trabalho de intercalação é executado em cada nó **de tamanho maior que 1**.

**Passo 2 — Contar as intercalações por nível:**

| Nível de intercalação | Quantidade de subproblemas | Elementos por subproblema | Total |
|---|---:|---:|---:|
| Vetor de tamanho 8 | 1 | 8 | 8 |
| Vetores de tamanho 4 | 2 | 4 | 8 |
| Vetores de tamanho 2 | 4 | 2 | 8 |
| **Total** | | | **24** |

**Passo 3 — Generalizar:** cada nível de intercalação processa os `n` elementos da entrada, repartidos em subproblemas. Existem `log2 n` níveis que realizam intercalação, pois os tamanhos são divididos por 2 até chegar a 1.

Portanto, `C(n)=n*log2 n`. Para `n=8`: `C(8)=8*3=24`, como na tabela.

**Passo 4 — Escrever a recorrência:**

```text
C(1)=0
C(n)=2*C(n/2)+n, para n>1 e n potência de 2.
```

O termo `2*C(n/2)` corresponde às duas metades. O termo `+n` corresponde a processar os `n` elementos durante a intercalação do subproblema atual.

**Passo 5 — Demonstrar a classificação da contagem:** para `n>=2` e `n=2^k`, temos `C(n)=n*log2 n` exatamente. Logo:

```text
1*(n*log2 n) <= C(n) <= 1*(n*log2 n).
```

Assim, com `c1=c2=1`, `n0=2`, a contagem pertence a `Theta(n log n)` e, consequentemente, a `O(n log n)`.

**Passo 6 — Relacionar com o tempo total:** cada intercalação de tamanho `m` exige trabalho proporcional a `m`, e formar as metades não ultrapassa esse custo. As chamadas e os testes dos casos-base também são no máximo da mesma ordem. Há ainda trabalho positivo proporcional ao número de elementos processados nas intercalações. Isso fornece limites superior e inferior de ordem `n log n` para o tempo total, sob as hipóteses dadas.

**Erro comum:** afirmar que `2*T(n/2)` implica `O(2^n)`. O número 2 indica duas chamadas sobre **metades** do problema, e a árvore tem `log2 n` níveis; não se trata de ramificação sobre `n-1` elementos até a profundidade `n`.

**Crédito parcial:** árvore correta, 8+8+8=24, recorrência, `C(n)=n log2 n`, justificativa Theta/Big O.

---

## Síntese para a correção coletiva

| Questão | Contagem / resultado-chave | Classificação relevante |
|---:|---|---|
| 1 | `C(n)=n` testes | `O(n)` |
| 2 | `C(n)=1` acesso | `O(1)` |
| 3 | `C(n)=n` somas | `O(n)` |
| 4 | `C(n)=n` comparações | `O(n)` |
| 5 | `C(n)=2n` chamadas | `O(n)` |
| 6 | `C(n)=n+n^2` chamadas | `O(n^2)` |
| 7 | `C(n)=n^2` chamadas | `O(n^2)` |
| 8 | `C(n)=n^3` chamadas | `O(n^3)` |
| 9 | `C(n)=n(n-1)/2` comparações | `O(n^2)` |
| 10 | `C(n)=n(n+1)/2` chamadas | `O(n^2)` |
| 11 | `C(n)=piso(log2 n)` | `O(log n)` |
| 12 | `C(n)=teto(log2 n)` | `O(log n)` |
| 13 | `C(n)=n*(piso(log2 n)+1)` | `O(n log n)` |
| 14 | `C(n)=n*piso(log2 n)` | `O(n log n)` |
| 15 | `7n^3+5n^2+12` | `O(n^3)`; `c=24`, `n0=1` |
| 16 | `A<D<B` em crescimento | `O(n)`, `O(n log n)`, `O(n^2)` |
| 17 | `4n+9` | `O(n)`; `c=13`, `n0=1` |
| 18 | `2n^2+7n+4` | `O(n^2)`; `c=13`, `n0=1` |
| 19 | `n^2+2n` | **Não pertence** a `O(n)` |
| 20 | `6n+1` | `O(n)` e `O(n^2)`; linear é mais ajustado |
| 21 | `2n^2+3n+1` | `Omega(n^2)`; `c=2`, `n0=1` |
| 22 | `C(n)=n` gravações | `Omega(n)` |
| 23 | `4n+7` | `Theta(n)`; `c1=4`, `c2=11`, `n0=1` |
| 24 | `C(n)=n(n+1)/2` | `Theta(n^2)`; `c1=1/2`, `c2=1`, `n0=1` |
| 25 | `(3n+4)/n^2 -> 0` | `o(n^2)` |
| 26 | Razões `1` e `1/n` | Não `o(n^2)`; sim `o(n^3)` |
| 27 | `C(n)=n` avisos | `O(n)` |
| 28 | `C(n)=n-1` multiplicações | `O(n)` |
| 29 | `C(n)=log2 n` | `Theta(log n)` |
| 30 | `C(n)=n*log2 n` | `Theta(n log n)` |

## Rubrica geral (sugestão de correção, caso a lista seja pontuada)

A revisão **não pressupõe nota atribuída**. Caso o professor queira aproveitar parte dela como atividade avaliativa, sugere-se distribuir o valor de cada questão em quatro dimensões: interpretação da entrada e do algoritmo (20%), simulação/contagem correta (30%), classificação assintótica (20%) e justificativa matemática ou explicação do crescimento (30%). Em questões puramente conceituais, redistribua proporcionalmente esses critérios.

**Fim do gabarito.**
