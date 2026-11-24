# Lista de revisão para a prova — Teoria da Computação

## Objetivo e modo de utilização

Esta lista retoma o conteúdo estudado após a última avaliação: tamanho da entrada e contagem de operações, crescimento de funções, notação Big O e suas demonstrações, notações Ômega, Theta e little-o, e análise de algoritmos iterativos e recursivos.

**Como estudar:** leia a explicação de cada tópico, acompanhe o **exemplo resolvido** e, só então, resolva as **duas questões** seguintes. São **15 tópicos × 2 questões = 30 questões**. 

### Convenções desta lista

- `n` é o tamanho da entrada, um número inteiro. Adote `n \>= 1`, salvo quando outra condição estiver explícita.

- `C(n)` representa **quantas vezes uma operação básica escolhida é executada**. `T(n)` representa o custo total de execução. As duas funções não precisam ser numericamente iguais.

- Acesso a elemento de vetor por índice, comparação, atribuição, incremento e operação aritmética simples custam tempo constante. Nos problemas recursivos, suponha aritmética de custo constante para os valores trabalhados.

- `para i de a até b` inclui os dois extremos; se `a \> b`, executa zero iterações. `//` é divisão inteira. `log2 n` é logaritmo de base 2.

- Se o comportamento depende do conteúdo da entrada, analise o **pior caso**, salvo indicação contrária. Indique o caso analisado ao concluir.

- Ao provar uma notação, não basta escrever a resposta; **mostre a desigualdade ou o argumento matemático solicitado**.

- A classificação em Big O é um **limite superior**, não necessariamente o limite mais ajustado. A notação não é sinônimo de pior caso.

## Resumo das definições

| Notação | O que significa | Condição para `n \>= n0` |
| - | - | :-: |
| `O(g(n))` | Limite superior assintótico | `0 \<= T(n) \<= c\*g(n)` para **algum** `c \> 0` |
| `Omega(g(n))` | Limite inferior assintótico | `0 \<= c\*g(n) \<= T(n)` para **algum** `c \> 0` |
| `Theta(g(n))` | Limite superior e inferior da mesma ordem | `0 \<= c1\*g(n) \<= T(n) \<= c2\*g(n)` para **alguns** `c1,c2 \> 0` |
| `o(g(n))` | Limite superior assintótico estrito | Para **todo** `c \> 0`, existe `n0` tal que `0 \<= T(n) \< c\*g(n)` para `n \>= n0` |


**Para little-o:** se `g(n) \> 0` para valores suficientemente grandes e o limite de `T(n)/g(n)` existe, `T(n) ∈ o(g(n))` quando esse limite é `0`. Não confunda a exigência **“existe c”** de Big O com **“para todo c”** de little-o.


# Tópico 1 — Tamanho da entrada, operação básica e função de contagem

**Conteúdo.** Antes de classificar um algoritmo, identifique o que `n` representa. Uma mesma linha pode executar várias vezes. A contagem `C(n)` depende da **operação escolhida**, enquanto o tempo total `T(n)` considera também o restante das instruções. Se cada iteração executa apenas trabalho constante, a quantidade de iterações normalmente determina o crescimento.

**Exemplo resolvido — Conferir assinaturas:**

```
procedimento conferir(arquivos):  
    n = tamanho(arquivos)  
    para i de 0 até n - 1:  
        verificarAssinatura(arquivos\[i\])
```

Contando chamadas de `verificarAssinatura`, para `n=4` são feitas 4 chamadas. Para qualquer `n`, `C(n)=n`. Sob a hipótese de custo constante por verificação, o tempo total é `O(n)` (e também `Theta(n)`).

**Questão 1 — Registro de clientes (fácil).** Analise:

```
procedimento contarAtivos(clientes):  
    n = tamanho(clientes)  
    ativos = 0  
    para i de 0 até n - 1:  
        se clientes\[i\].ativo:  
            ativos = ativos + 1  
    retornar ativos
```

Defina o que é `n`; escolha como operação básica **a avaliação de `clientes\[i\].ativo`**; simule para quatro clientes, sendo dois ativos; deduza `C(n)`; e informe um Big O para o tempo total. Explique por que o número de clientes ativos não altera a contagem da operação escolhida.

**Questão 2 — Consulta de estoque (fácil).** Analise:

```
função consultar(estoque, posicao):  
    retornar estoque\[posicao\]
```

O vetor contém `n` produtos e a posição é válida. Conte acessos ao vetor para `n=5` e para `n=5000`; obtenha `C(n)` e classifique o tempo total. Explique por que a resposta **não** depende do número de elementos no vetor.


# Tópico 2 — Um laço simples e o crescimento linear

**Conteúdo.** Um laço que percorre cada elemento uma vez executa `n` iterações. Se cada iteração realiza um conjunto fixo de operações, a quantidade total cresce proporcionalmente a `n`.

**Exemplo resolvido — Somar preços:**

```
soma = 0  
para i de 0 até n - 1:  
    soma = soma + precos\[i\]
```

Se contamos a soma dentro do laço: para `n=3` ocorrem 3 somas; `C(n)=n`. A inicialização e o retorno não mudam a ordem de crescimento. O tempo é `O(n)`.

**Questão 3 — Média de temperaturas (fácil).** Analise:

```
função media(temperaturas):  
    n = tamanho(temperaturas)  
    soma = 0  
    para i de 0 até n - 1:  
        soma = soma + temperaturas\[i\]  
    retornar soma / n
```

Considere `n\>=1`. Conte as somas para `n=5`, construa `C(n)` e classifique `T(n)` em Big O. Justifique por que a divisão final não altera a classificação.

**Questão 4 — Procurar sem interromper (fácil).** Analise:

```
função existeCodigo(codigos, procurado):  
    n = tamanho(codigos)  
    encontrado = falso  
    para i de 0 até n - 1:  
        se codigos\[i\] == procurado:  
            encontrado = verdadeiro  
    retornar encontrado
```

Conte as comparações `codigos\[i\] == procurado` para `n=4`, primeiro quando o código está na posição 0 e depois quando não aparece. Encontre `C(n)` e `O(...)` do tempo total. Compare com uma busca linear que encerraria no primeiro acerto.


# Tópico 3 — Laços consecutivos e soma de custos

**Conteúdo.** Quando um laço termina antes do próximo começar, seus custos **se somam**: `C(n)=C1(n)+C2(n)`. Não multiplicamos simplesmente porque há dois `para` no código.

**Exemplo resolvido — Duas verificações:**

```
para i de 0 até n - 1: conferirEntrada(i)  
para j de 0 até n - 1: conferirSaida(j)
```

Há `n` chamadas ao primeiro procedimento e `n` ao segundo. A contagem conjunta é `C(n)=2n`, portanto o tempo total é `O(n)`, supondo chamadas de custo constante.

**Questão 5 — Auditoria em duas etapas (fácil).** Analise:

```
procedimento auditar(registros):  
    n = tamanho(registros)  
    para i de 0 até n - 1:  
        validar(registros\[i\])  
    para j de 0 até n - 1:  
        registrarLog(registros\[j\])
```

Considere ambas as chamadas de custo constante. Para `n=3`, indique quantas chamadas de cada procedimento ocorrem. Encontre a contagem conjunta e o Big O do tempo total. Explique por que o resultado não é quadrático.

**Questão 6 — Rotina com duas escalas (média).** Analise:

```
procedimento analisar(n):  
    para i de 0 até n - 1:  
        verificar(i)  
    para j de 0 até n\*n - 1:  
        registrar(j)
```

Suponha chamadas de custo constante. Para `n=3`, conte separadamente `verificar` e `registrar`, obtenha `C(n)` como soma das chamadas, identifique o termo dominante e classifique o tempo em Big O.


# Tópico 4 — Laços aninhados de limites independentes

**Conteúdo.** Um laço executado `n` vezes **dentro** de outro laço de `n` iterações provoca `n\*n = n^2` execuções da operação interna. Para três laços com `n` iterações cada, surgem `n^3` execuções.

**Exemplo resolvido — Cruzar duas listas:**

```
para i de 0 até n - 1:  
    para j de 0 até n - 1:  
        testarPar(i, j)
```

Para `n=3`, cada um dos 3 valores de `i` gera 3 chamadas: `3+3+3=9`. Portanto, `C(n)=n^2` e `T(n)` pertence a `O(n^2)`.

**Questão 7 — Produtos e filiais (média).** Uma rede compara `n` produtos com `n` filiais:

```
para i de 0 até n - 1:  
    para j de 0 até n - 1:  
        verificarOferta(produtos\[i\], filiais\[j\])
```

Conte as chamadas para `n=4`, generalize `C(n)` e apresente `O(...)` do tempo, supondo custo constante por chamada.

**Questão 8 — Três dimensões (média).** Um sistema verifica `n` equipes, `n` turnos e `n` salas:

```
para e de 0 até n - 1:  
    para t de 0 até n - 1:  
        para s de 0 até n - 1:  
            validar(e, t, s)
```

Conte as chamadas para `n=2`; escreva a expressão para `C(n)` e classifique o tempo. Explique a diferença em relação à questão anterior.


# Tópico 5 — Laços triangulares e somatórios

**Conteúdo.** Nem todo laço interno executa `n` vezes. Quando seu início depende de `i`, pode executar `n-1`, depois `n-2`, e assim por diante. A soma `1+2+...+(n-1)` equivale a `n(n-1)/2`.

**Exemplo resolvido — Pares distintos:**

```
para i de 0 até n - 2:  
    para j de i + 1 até n - 1:  
        comparar(i, j)
```

Com `n=4`, as chamadas são `3+2+1=6`. Para `n` elementos, `C(n)=n(n-1)/2`. Como o termo dominante é `n^2/2`, o tempo é `O(n^2)`.

**Questão 9 — Comparar sensores distintos (média).** Analise:

```
para i de 0 até n - 2:  
    para j de i + 1 até n - 1:  
        compararSensores(sensores\[i\], sensores\[j\])
```

Para `n=5`, faça uma tabela com o número de comparações para cada `i`. Deduza `C(n)` e classifique em Big O. Explique por que o algoritmo não compara cada sensor consigo mesmo.

**Questão 10 — Intervalos possíveis (média).** Analise:

```
para inicio de 0 até n - 1:  
    para fim de inicio até n - 1:  
        registrarIntervalo(inicio, fim)
```

Conte as chamadas com `n=4`; escreva o somatório e a fórmula fechada de `C(n)`; classifique em Big O. Qual a diferença entre este caso e a questão 9?


# Tópico 6 — Repetições multiplicativas e crescimento logarítmico

**Conteúdo.** Quando a variável de controle **divide ou dobra** a cada iteração, a quantidade de iterações tende a ser proporcional a `log2 n`. É necessário prestar atenção à condição de parada (`\>`, `\<`, `\<=`) para obter a contagem exata.

**Exemplo resolvido — Dividir lote ao meio:**

```
restantes = n  
enquanto restantes \> 1:  
    restantes = restantes // 2
```

Para `n=8`: `8 -\> 4 -\> 2 -\> 1`, isto é, 3 iterações. Em geral, para `n\>=1`, a contagem é `C(n)=piso(log2 n)`. Para `n\>=2`, seu crescimento é `O(log n)`.

**Questão 11 — Redução de lotes (média).** Analise:

```
restantes = n  
etapas = 0  
enquanto restantes \> 1:  
    restantes = restantes // 2  
    etapas = etapas + 1
```

Simule `n=16` e `n=17`, registre os valores de `restantes`, encontre a fórmula de `C(n)` contando as execuções de `etapas = etapas + 1` e classifique o tempo em Big O.

**Questão 12 — Crescimento de capacidade (média).** Analise:

```
capacidade = 1  
enquanto capacidade \< n:  
    capacidade = capacidade \* 2
```

Simule `n=20`; explique quantas vezes o comando de multiplicação executa e obtenha uma fórmula com `teto(log2 n)` para `n\>=1`. Classifique o tempo em Big O.


# Tópico 7 — Laços com custo n log n

**Conteúdo.** Quando um laço externo percorre `n` elementos e, em cada repetição, um laço interno executa aproximadamente `log2 n` vezes, a quantidade conjunta costuma ser proporcional a `n\*log2 n`.

**Exemplo resolvido — Conferência em escalas:**

```
para i de 0 até n - 1:  
    k = 1  
    enquanto k \< n:  
        testar(i, k)  
        k = k \* 2
```

Para `n=8`, `k` assume `1,2,4` — 3 testes por valor de `i` — e `C(8)=8\*3=24`. Em geral, `C(n)=n\*teto(log2 n)` para `n\>=1`; o tempo é `O(n log n)` para `n\>=2`.

**Questão 13 — Auditoria por escalas (média).** Analise:

```
para i de 0 até n - 1:  
    escala = 1  
    enquanto escala \<= n:  
        verificar(i, escala)  
        escala = escala \* 2
```

Para `n=8`, liste as escalas testadas por elemento e conte todas as chamadas. Deduza `C(n)` usando `piso(log2 n)` e classifique o tempo em Big O.

**Questão 14 — Redução por registro (média).** Analise:

```
para i de 0 até n - 1:  
    tamanho = n  
    enquanto tamanho \> 1:  
        comparar(i, tamanho)  
        tamanho = tamanho // 2
```

Para `n=16`, conte as chamadas de `comparar` por elemento e no total. Deduza `C(n)` e indique o Big O. Explique por que o custo não é quadrático.


# Tópico 8 — Crescimento de funções e termo dominante

**Conteúdo.** Para polinômios de custos não negativos, termos de maior grau dominam o crescimento para entradas grandes. Multiplicar por constantes não muda a classe assintótica. Em termos de ordem de crescimento, as funções `1`, `log n`, `n`, `n log n`, `n^2`, `n^3`, `2^n` e `n!` representam famílias diferentes.

**Exemplo resolvido — Estimar custo:** se `C(n)=4n^2+8n+100`, para todo `n\>=1` vale `8n\<=8n^2` e `100\<=100n^2`. Logo, `C(n)\<=112n^2` e `C(n) ∈ O(n^2)`.

**Questão 15 — Simplificação justificada (média).** A contagem obtida de um algoritmo é `C(n)=7n^3+5n^2+12`. Identifique o termo dominante, proponha `g(n)`, demonstre formalmente um limite Big O usando valores explícitos de `c` e `n0` e apresente a classificação.

**Questão 16 — Comparar soluções (média).** Três algoritmos possuem, sob o mesmo modelo de custo:

```
A(n) = 20n + 100  
B(n) = 2n^2 + 1  
D(n) = n \* log2 n
```

Coloque-os em ordem crescente de **taxa de crescimento assintótica** e explique o raciocínio. Indique a classe Big O mais informativa dentre `O(n)`, `O(n log n)` e `O(n^2)` para cada função. A ordenação obtida significa que o algoritmo de menor crescimento será sempre o mais rápido para qualquer `n`? Justifique.


# Tópico 9 — Prova formal de Big O: o papel de c e n0

**Conteúdo.** Demonstrar `T(n) ∈ O(g(n))` significa **encontrar** `c\>0` e `n0` de modo que `0\<=T(n)\<=c\*g(n)` para **todo** `n\>=n0`. A prova não é uma tabela com alguns valores: ela exige uma desigualdade geral.

**Exemplo resolvido — Função linear:** `T(n)=3n+5`. Para `n\>=1`, `5\<=5n`. Portanto, `3n+5\<=3n+5n=8n`. Podemos escolher `c=8`, `n0=1`. Logo, `T(n) ∈ O(n)`.

**Questão 17 — Limite linear (média).** Demonstre formalmente que `C(n)=4n+9` pertence a `O(n)`. Escreva a desigualdade inicial, encontre `c` e `n0`, justifique cada passagem e conclua.

**Questão 18 — Limite quadrático (média).** Demonstre formalmente que `C(n)=2n^2+7n+4` pertence a `O(n^2)`. Mostre como limitar os termos `7n` e `4` por múltiplos de `n^2` e escolha valores válidos de `c` e `n0`.


# Tópico 10 — Limite válido, limite ajustado e afirmações falsas

**Conteúdo.** Uma função linear pode estar tanto em `O(n)` quanto em `O(n^2)`, mas `O(n)` fornece um limite mais ajustado. Em contrapartida, `n^2` **não** está em `O(n)`: nenhuma constante fixa multiplicando `n` consegue superar `n^2` para todo `n` suficientemente grande.

**Exemplo resolvido — Refutar uma classificação:** para provar que `n^2` não pertence a `O(n)`, suponha que `n^2 \<= c\*n` para todo `n\>=n0`. Para `n\>0`, isso exige `n\<=c`. Basta escolher `n\>max(c,n0)` para obter uma contradição.

**Questão 19 — Detectar uma afirmação impossível (média).** Um colega afirma que `T(n)=n^2+2n` pertence a `O(n)`. Analise a afirmação e **demonstre que ela é falsa** a partir da definição formal de Big O.

**Questão 20 — Dois limites superiores (média).** Considere `T(n)=6n+1`. Demonstre que ela pertence a `O(n)` e também a `O(n^2)`. Escolha constantes para as duas provas e explique qual limite é mais informativo.


# Tópico 11 — Notação Ômega: limite inferior

**Conteúdo.** `T(n) ∈ Omega(g(n))` significa que `T(n)` fica **acima** de algum múltiplo positivo de `g(n)` a partir de `n0`. A desigualdade é `c\*g(n)\<=T(n)`. Ômega não significa, automaticamente, “melhor caso”: a notação pode caracterizar qualquer função de custo bem definida.

**Exemplo resolvido:** `T(n)=5n+3`. Para `n\>=1`, `5n\<=5n+3`. Escolhemos `c=5`, `n0=1` e concluímos `T(n) ∈ Omega(n)`.

**Questão 21 — Ômega quadrático (média).** Demonstre formalmente que `T(n)=2n^2+3n+1` pertence a `Omega(n^2)`, identificando `g(n)`, `c` e `n0`. Explique por que os termos adicionais não invalidam o limite inferior.

**Questão 22 — Ômega aplicado a um algoritmo (média).** Analise:

```
procedimento registrarEntradas(entradas):  
    n = tamanho(entradas)  
    para i de 0 até n - 1:  
        gravar(entradas\[i\])
```

Supondo `gravar` de custo constante positivo, obtenha `C(n)` como número de gravações, demonstre `C(n) ∈ Omega(n)` e explique por que o tempo total do algoritmo também tem um limite inferior linear.


# Tópico 12 — Notação Theta: limites dos dois lados

**Conteúdo.** `T(n) ∈ Theta(g(n))` quando conseguimos mostrar, simultaneamente, um limite inferior e um superior com a **mesma** função `g(n)`: `c1\*g(n)\<=T(n)\<=c2\*g(n)` para `n\>=n0`, com `c1,c2\>0`.

**Exemplo resolvido — Pares distintos:** `C(n)=n(n-1)/2`. Para `n\>=2`, como `n-1\>=n/2` e `n-1\<=n`, obtemos `n^2/4\<=C(n)\<=n^2/2`. Assim, `c1=1/4`, `c2=1/2`, `n0=2`, logo `C(n) ∈ Theta(n^2)`.

**Questão 23 — Theta linear (média).** Demonstre formalmente que `C(n)=4n+7` pertence a `Theta(n)`. Encontre `c1`, `c2` e `n0` e mostre as duas desigualdades.

**Questão 24 — Theta em laço triangular (difícil).** Analise:

```
para i de 0 até n - 1:  
    para j de 0 até i:  
        processar(i, j)
```

Com `processar` de custo constante positivo, simule `n=4`, deduza a fórmula exata de `C(n)` e prove formalmente `C(n) ∈ Theta(n^2)` com constantes. Explique como a contagem sustenta a classificação do tempo total.


# Tópico 13 — Notação little-o: crescimento estritamente menor

**Conteúdo.** `f(n) ∈ o(g(n))` diz que `f(n)` se torna desprezível em relação a `g(n)` conforme `n` cresce. Quando `g(n)\>0` e a razão possui limite, podemos verificar `lim \[f(n)/g(n)\] = 0`. Ao contrário de Big O, não basta um único multiplicador `c`: o limite estrito precisa funcionar para **qualquer** `c\>0`, a partir de algum `n0` que pode depender de `c`.

**Exemplo resolvido:** `f(n)=n`, `g(n)=n^2`. A razão é `n/n^2=1/n`, que tende a `0`; portanto, `n ∈ o(n^2)`. Já `n^2 ∉ o(n^2)`, porque sua razão é sempre `1`.

**Questão 25 — Comparação linear × quadrática (média).** Verifique se `f(n)=3n+4` pertence a `o(n^2)`. Calcule a razão, descreva o comportamento quando `n` cresce e apresente a conclusão. Opcionalmente, justifique pela definição “para todo `c\>0`”.

**Questão 26 — Mesmo crescimento ou crescimento estritamente menor? (média).** Julgue e justifique **ambas** as afirmações:

- (a) `n^2 ∈ o(n^2)`.

- (b) `n^2 ∈ o(n^3)`.

Use a razão entre as funções e explique o que diferencia little-o de Big O nesse caso.


# Tópico 14 — Recursão linear e recorrência

**Conteúdo.** Um algoritmo recursivo chama a si mesmo sobre uma entrada menor até atingir o **caso-base**. Para contar operações, podemos escrever uma **recorrência**, como `C(n)=C(n-1)+1` para `n\>0`, com `C(0)=0`. Nesse caso, a expansão produz `C(n)=n`.

**Exemplo resolvido — Exibir contagem regressiva:**

```
procedimento exibir(n):  
    se n == 0: retornar  
    mostrar(n)  
    exibir(n - 1)
```

Para `n=3`, as chamadas `mostrar(3)`, `mostrar(2)` e `mostrar(1)` são executadas. A recorrência é `C(n)=C(n-1)+1`; como `C(0)=0`, temos `C(n)=n`. O tempo total é `O(n)`.

**Questão 27 — Avisos recursivos (média).** Analise:

```
procedimento emitirAvisos(n):  
    se n == 0:  
        retornar  
    enviarAviso(n)  
    emitirAvisos(n - 1)
```

Considere `n\>=0` e custo constante por aviso. Simule `n=4`, escreva a recorrência da contagem de `enviarAviso`, resolva-a por expansão e classifique o tempo em Big O.

**Questão 28 — Fatorial recursivo (média).** Analise:

```
função fatorial(n):  
    se n \<= 1:  
        retornar 1  
    retornar n \* fatorial(n - 1)
```

Considere `n\>=1` e multiplicações de custo constante. Para `n=5`, conte as multiplicações realizadas; encontre uma recorrência para a contagem e obtenha `C(n)`; explique a complexidade temporal em Big O. O número de chamadas é igual ao número de multiplicações?


# Tópico 15 — Divisão e conquista: recursão e níveis de trabalho

**Conteúdo.** Alguns algoritmos reduzem o tamanho do problema pela metade. Se fazem **uma** chamada por nível, uma recorrência típica é `C(n)=C(n/2)+1`, com crescimento logarítmico. Se fazem **duas** chamadas por nível e precisam de trabalho linear para combinar resultados, surge `T(n)=2T(n/2)+n`, caso clássico do Merge Sort. Para simplificar, nas questões abaixo, considere `n` potência de 2.

**Exemplo resolvido — Uma chamada pela metade:**

```
procedimento reduzir(n):  
    se n \<= 1: retornar  
    registrarEtapa()  
    reduzir(n // 2)
```

Para `n=8`, ocorrem 3 registros: `8 -\> 4 -\> 2 -\> 1`. Se `n=2^k`, então `C(n)=k=log2 n`. O tempo total pertence a `O(log n)` para `n\>=2`.

**Questão 29 — Busca recursiva por redução (média).** Analise:

```
procedimento reduzirProblema(n):  
    se n \<= 1:  
        retornar  
    processarNivel()  
    reduzirProblema(n // 2)
```

Considere `n=2^k`, `n\>=2` e custo constante para `processarNivel`. Desenhe a sequência de chamadas para `n=16`, escreva e resolva a recorrência de `C(n)` (chamadas a `processarNivel`) e demonstre que essa contagem pertence a `Theta(log2 n)`.

**Questão 30 — Merge Sort e árvore de recursão (difícil).** Considere o pseudocódigo conceitual:

```
procedimento mergeSort(vetor):  
    n = tamanho(vetor)  
    se n \<= 1:  
        retornar  
    mergeSort(metadeEsquerda(vetor))  
    mergeSort(metadeDireita(vetor))  
    intercalarAsDuasMetades(vetor)
```

Adote `n=2^k`, `n\>=2`. As duas metades têm `n/2` elementos; cada intercalação em um subproblema de tamanho `m` processa exatamente `m` elementos; formar as metades não custa mais que `O(m)` e cada operação elementar tem custo constante. **Conte apenas elementos processados nas intercalações** para construir `C(n)`.

Desenhe a árvore para `n=8`, registre o trabalho de intercalação em **cada nível**, escreva a recorrência para `C(n)` e obtenha uma fórmula fechada. Classifique tanto a contagem quanto o tempo total usando Big O e Theta, justificando o número de níveis.


## Quadro de registro (para preenchimento ao final)

| Questões | Conteúdo | Minha resposta / principal classificação |
| - | - | - |
| 1–2 | Entrada e operação básica |  |
| 3–4 | Laço simples |  |
| 5–6 | Laços consecutivos |  |
| 7–8 | Laços aninhados |  |
| 9–10 | Laços triangulares |  |
| 11–12 | Laços logarítmicos |  |
| 13–14 | Laços `n log n` |  |
| 15–16 | Crescimento e termo dominante |  |
| 17–18 | Demonstração de Big O |  |
| 19–20 | Limites ajustados e refutação |  |
| 21–22 | Ômega |  |
| 23–24 | Theta |  |
| 25–26 | little-o |  |
| 27–28 | Recursão linear |  |
| 29–30 | Recursão por divisão |  |


**Fim da lista de revisão. As respostas dos exercícios estão no gabarito separado, destinado ao professor.**

