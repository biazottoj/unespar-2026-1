# Atividade — Análise de algoritmos com notação Big O

**Disciplina:** Teoria da Computação  
**Conteúdo:** Crescimento de funções e notação Big O  
**Nome:** ________________________________________________  
**Data:** ____/____/________

## Objetivo

Analisar **dez algoritmos apresentados em pseudocódigo**, relacionando a estrutura de execução à quantidade de operações e justificando um limite superior assintótico com a notação Big O.

## Instruções para todos os exercícios

Para **cada algoritmo**, apresente:

1. **Tamanho da entrada:** explique claramente o que representa `n`.
2. **Operação básica:** identifique uma operação relevante para a contagem (quando indicado, utilize a operação especificada).
3. **Simulação:** escolha um valor pequeno de `n` (preferencialmente 4 ou 5) e registre a quantidade de execuções da operação básica.
4. **Função de custo:** deduza uma expressão `C(n)` exata, quando viável, ou apresente um limite superior explícito e justificado.
5. **Notação Big O:** determine uma função `g(n)` tal que o custo total esteja em `O(g(n))`.
6. **Justificativa:** explique como a estrutura do algoritmo sustenta a classificação. Nos exercícios indicados com **[Demonstração formal]**, apresente valores válidos de `c` e `n0` para a desigualdade `C(n) <= c * g(n)`.

**Convenções:**

- Considere operações simples de atribuição, comparação, soma e acesso a posições de vetores como operações de custo constante, salvo indicação contrária.
- `//` representa divisão inteira; `piso(x)` e `teto(x)` indicam arredondamento para baixo e para cima, respectivamente.
- Analise o **pior caso**, quando o comportamento variar conforme os dados de entrada.
- Se houver uma estrutura previamente ordenada, não inclua o custo de ordená-la, a menos que o próprio algoritmo a ordene.
- Não basta responder apenas `O(...)`: mostre o raciocínio.
- Não utilize outras notações assintóticas nesta atividade.

---

# Exemplo resolvido — Como analisar um algoritmo passo a passo

**Leia este exemplo antes de iniciar os exercícios.** Ele apresenta o procedimento de análise que deverá ser repetido nas dez questões. O exemplo está resolvido; os exercícios seguintes devem ser respondidos pelo aluno.

## Situação-problema: verificar pedidos duplicados

Uma loja recebeu `n` pedidos. Para descobrir se há pedidos com o mesmo identificador, o sistema compara cada pedido com os que aparecem **depois dele** na lista. Essa escolha evita comparar um pedido com ele mesmo e evita repetir um par já verificado.

### Algoritmo

```text
procedimento verificarPedidosDuplicados(pedidos):
    n = tamanho(pedidos)
    existeDuplicado = falso

    para i de 0 até n - 2:
        para j de i + 1 até n - 1:
            se pedidos[i].id == pedidos[j].id:
                existeDuplicado = verdadeiro

    retornar existeDuplicado
```

**Hipóteses:** a lista pode conter qualquer quantidade de pedidos; a comparação entre dois identificadores é considerada uma operação de custo constante; e o algoritmo **não interrompe** a execução quando encontra um duplicado.

## Passo 1 — Identificar o tamanho da entrada

A primeira pergunta é: **o que representa `n`?**

```text
n = quantidade de pedidos na lista.
```

Por exemplo, `n = 4` significa que serão analisados quatro pedidos. Isso não significa que o algoritmo realizará apenas quatro comparações.

## Passo 2 — Escolher a operação que será contada

A operação básica será a comparação:

```text
pedidos[i].id == pedidos[j].id
```

Definimos:

```text
C(n) = número de comparações entre identificadores.
```

É importante indicar **qual operação** está sendo contada: a quantidade de comparações não é necessariamente igual à quantidade total de operações executadas pelo computador.

## Passo 3 — Simular uma entrada pequena

Considere quatro pedidos, identificados por `A`, `B`, `C` e `D`.

Vamos acompanhar os valores de `i` e `j`:

| `i` | Pedido escolhido | Pedidos seguintes comparados com ele | Comparações |
|---:|---|---|---:|
| 0 | A | B, C e D | 3 |
| 1 | B | C e D | 2 |
| 2 | C | D | 1 |
| **Total** | | | **6** |

Podemos também listar todos os pares examinados:

```text
(A, B), (A, C), (A, D), (B, C), (B, D), (C, D)
```

Portanto:

```text
C(4) = 3 + 2 + 1 = 6 comparações.
```

**Pergunta de verificação:** por que não contamos `(B, A)`? Porque o par `(A, B)` já foi verificado. Compará-lo novamente seria redundante.

## Passo 4 — Repetir a simulação com outro tamanho

Se houver cinco pedidos:

```text
Pedido 1: compara com 4 pedidos
Pedido 2: compara com 3 pedidos
Pedido 3: compara com 2 pedidos
Pedido 4: compara com 1 pedido
Pedido 5: compara com 0 pedidos

C(5) = 4 + 3 + 2 + 1 = 10
```

A tabela ajuda a identificar um padrão:

| Quantidade de pedidos `n` | Comparações `C(n)` |
|---:|---:|
| 2 | 1 |
| 3 | 3 |
| 4 | 6 |
| 5 | 10 |
| 6 | 15 |

O objetivo da simulação não é apenas obter números: é descobrir **por que** a quantidade de comparações cresce dessa maneira.

## Passo 5 — Construir uma função para qualquer `n`

Agora vamos generalizar o padrão encontrado:

- O primeiro pedido gera `n - 1` comparações.
- O segundo gera `n - 2` comparações.
- O terceiro gera `n - 3` comparações.
- Continuamos até o penúltimo pedido, que gera `1` comparação.
- O último não gera novas comparações.

Assim:

```text
C(n) = (n - 1) + (n - 2) + ... + 2 + 1
```

Para calcular essa soma, podemos escrevê-la em ordem crescente e decrescente:

```text
S  = 1       + 2       + ... + (n - 2) + (n - 1)
S  = (n - 1) + (n - 2) + ... + 2       + 1
--------------------------------------------------
2S = n       + n       + ... + n       + n
```

Existem `n - 1` parcelas iguais a `n` na última linha. Logo:

```text
2S = n * (n - 1)
 S = n * (n - 1) / 2
```

Concluímos que:

```text
C(n) = n * (n - 1) / 2
C(n) = (n^2 - n) / 2
```

**Confira a fórmula:** para `n = 5`, temos `C(5) = 5 * 4 / 2 = 10`, exatamente o resultado encontrado na simulação.

## Passo 6 — Identificar o crescimento e propor um Big O

Observe a expressão:

```text
C(n) = (n^2 - n) / 2
```

Quando `n` aumenta, o termo `n^2` cresce mais rapidamente que o termo `n`. Por isso, uma função de referência adequada para estabelecer um **limite superior** é:

```text
g(n) = n^2
```

Nossa hipótese será:

```text
C(n) pertence a O(n^2).
```

Entretanto, **identificar o termo dominante ainda não é uma demonstração formal**. Precisamos justificar a desigualdade da definição de Big O.

## Passo 7 — Demonstrar formalmente o Big O

Pela definição, precisamos encontrar constantes `c > 0` e `n0 >= 1` tais que:

```text
0 <= C(n) <= c * n^2, para todo n >= n0.
```

Começamos pela fórmula obtida:

```text
C(n) = n * (n - 1) / 2
```

Para todo `n >= 1`, vale `n - 1 <= n`. Portanto:

```text
n * (n - 1) <= n * n
```

Dividindo ambos os lados por `2`:

```text
n * (n - 1) / 2 <= n^2 / 2
```

Ou seja:

```text
C(n) <= (1/2) * n^2, para todo n >= 1.
```

**Encontramos as constantes necessárias:**

```text
c  = 1/2
n0 = 1
```

Logo, pela definição formal:

```text
C(n) pertence a O(n^2).
```

**Interpretação:** a partir de `n = 1`, a quantidade de comparações nunca ultrapassa metade de `n^2`. Essa desigualdade comprova um limite superior quadrático para a contagem de comparações.

## Passo 8 — Relacionar a contagem ao tempo total

Até aqui demonstramos formalmente um limite para **comparações entre identificadores**. O algoritmo também executa atribuições, incrementos de índices e testes dos laços.

No entanto, todas essas operações são de custo constante, e os dois laços não realizam mais do que uma quantidade quadrática de iterações. Assim, o custo total também pode ser limitado por uma constante multiplicada por `n^2` (para entradas suficientemente grandes).

Portanto, a classificação do **tempo total** do algoritmo também é:

```text
O(n^2)
```

**Atenção:** Big O é um limite superior. Por exemplo, um limite `O(n^3)` também seria verdadeiro, porém menos informativo para este algoritmo. Buscamos um limite que descreva adequadamente sua estrutura.

## Modelo de resposta que você deve reproduzir nos exercícios

Para **cada exercício**, organize sua solução seguindo este roteiro:

```text
1. Tamanho da entrada:
   n representa ____________________________________.

2. Operação básica:
   Vou contar ______________________________________.

3. Simulação com n = ____:
   Mostrar as iterações e a quantidade de operações.

4. Função de contagem:
   C(n) = __________________________________________.
   Explicar de onde veio a fórmula ou o limite.

5. Função de referência para Big O:
   g(n) = __________________________________________.

6. Justificativa:
   Explicar por que a estrutura do algoritmo não
   ultrapassa esse crescimento assintótico.

7. Conclusão sobre o tempo total:
   O(______________________________________________).

8. Quando solicitada demonstração formal:
   Mostrar C(n) <= c * g(n), indicar c e n0,
   e explicar por que a desigualdade vale para n >= n0.
```

**Importante:** alguns exercícios possuem laços consecutivos, outros possuem laços aninhados, divisões sucessivas ou recursão. Portanto, **não utilize automaticamente a fórmula do exemplo em todas as questões**. Reproduza o *método de análise*, adaptando a contagem à estrutura de cada algoritmo.

---

# Lista de exercícios — Analise os 10 algoritmos a seguir

## Exercício 1 — Consulta direta a uma posição do estoque

**Nível: fácil**

Em um depósito, as quantidades de produtos estão armazenadas em um vetor. O sistema recebe uma posição válida e consulta o estoque daquele produto.

```text
função consultarEstoque(estoques, posicao):
    quantidade = estoques[posicao]
    retornar quantidade
```

**Considere:** o vetor possui `n` posições e `posicao` é sempre válida. Identifique quantas posições são acessadas, mesmo quando `n` aumenta bastante.

---

## Exercício 2 — Contar faturas vencidas

**Nível: fácil**

Um setor financeiro precisa contar quantas faturas estão vencidas.

```text
função contarVencidas(faturas, dataAtual):
    total = 0
    n = tamanho(faturas)

    para i de 0 até n - 1:
        se faturas[i].vencimento < dataAtual:
            total = total + 1

    retornar total
```

**Considere:** uma comparação de data tem custo constante. Conte quantas verificações de vencimento são feitas no pior caso.

---

## Exercício 3 — Calcular receita total e maior venda

**Nível: fácil**

Uma loja realiza duas análises independentes sobre a mesma lista de vendas: calcular a receita total e identificar o maior valor registrado.

```text
função analisarVendas(vendas):
    n = tamanho(vendas)
    soma = 0

    para i de 0 até n - 1:
        soma = soma + vendas[i].valor

    maior = 0
    para i de 0 até n - 1:
        se vendas[i].valor > maior:
            maior = vendas[i].valor

    retornar (soma, maior)
```

**Considere:** os valores das vendas são não negativos. Conte as iterações dos dois laços separadamente e depois considere o custo total.

---

## Exercício 4 — Comparar clientes e centros de distribuição

**Nível: médio**

Uma empresa deseja identificar possíveis associações entre todos os clientes e todos os centros de distribuição.

```text
procedimento verificarAssociacoes(clientes, centros):
    n = tamanho(clientes)

    para i de 0 até n - 1:
        para j de 0 até n - 1:
            verificarPossibilidade(clientes[i], centros[j])
```

**Considere:** `centros` também possui exatamente `n` elementos, e `verificarPossibilidade` executa uma quantidade constante de operações. Determine quantas chamadas são realizadas.

---

## Exercício 5 — Comparar pares de sensores

**Nível: médio · [Demonstração formal]**

Em uma indústria, os sensores são comparados em pares para identificar possíveis conflitos de configuração. Comparar um sensor com ele mesmo ou repetir o mesmo par não é necessário.

```text
procedimento compararSensores(sensores):
    n = tamanho(sensores)

    para i de 0 até n - 2:
        para j de i + 1 até n - 1:
            compararConfiguracoes(sensores[i], sensores[j])
```

**Considere:** cada chamada a `compararConfiguracoes` custa tempo constante. Mostre a contagem para `n = 5`, deduza uma fórmula geral e demonstre formalmente o limite Big O escolhido.

---

## Exercício 6 — Reduzir sucessivamente um lote de inspeção

**Nível: médio · [Demonstração formal]**

Um supervisor investiga um lote de `n` encomendas. A cada etapa, reduz o grupo de inspeção aproximadamente à metade, até restar uma encomenda.

```text
função contarEtapasDeInspecao(n):
    restantes = n
    etapas = 0

    enquanto restantes > 1:
        restantes = (restantes + 1) // 2
        etapas = etapas + 1

    retornar etapas
```

**Considere:** `n >= 1`. Simule os valores `n = 8` e `n = 17`. Descubra como o número de etapas cresce quando `n` dobra. Na demonstração formal, é suficiente estabelecer um limite superior para o número de iterações.

---

## Exercício 7 — Conferir pedidos contra um catálogo ordenado

**Nível: médio**

Uma transportadora possui `n` pedidos e deseja verificar se os códigos aparecem em um catálogo **já ordenado**, também com `n` códigos. Cada pedido é procurado por busca binária.

```text
procedimento conferirPedidos(pedidos, catalogo):
    n = tamanho(pedidos)

    para i de 0 até n - 1:
        inicio = 0
        fim = n - 1

        enquanto inicio <= fim:
            meio = (inicio + fim) // 2

            se catalogo[meio] == pedidos[i].codigo:
                interromper o enquanto

            se catalogo[meio] < pedidos[i].codigo:
                inicio = meio + 1
            senão:
                fim = meio - 1
```

**Considere:** o catálogo já está ordenado e seu acesso por índice custa tempo constante. Analise o pior caso, quando os pedidos procurados não são encontrados. Explique separadamente o custo da busca de **um pedido** e o custo das buscas de **todos os pedidos**.

---

## Exercício 8 — Avaliar combinações operacionais

**Nível: médio**

Uma empresa pretende testar combinações de locais de coleta, transportadoras e horários disponíveis. Cada conjunto possui `n` opções.

```text
procedimento avaliarOperacoes(coletas, transportadoras, horarios):
    n = tamanho(coletas)

    para i de 0 até n - 1:
        para j de 0 até n - 1:
            para k de 0 até n - 1:
                avaliarCombinacao(coletas[i], transportadoras[j], horarios[k])
```

**Considere:** as três listas têm `n` elementos e `avaliarCombinacao` custa tempo constante. Determine quantas combinações serão avaliadas para `n = 3` e generalize.

---

## Exercício 9 — Explorar pacotes de serviços opcionais

**Nível: difícil**

Uma empresa oferece `n` serviços opcionais para uma entrega, como seguro, rastreamento especial ou embalagem reforçada. Cada serviço pode ser **incluído** ou **não incluído**. Um procedimento recursivo percorre todas as possibilidades e contabiliza cada configuração visitada.

```text
contador = 0

procedimento explorarServicos(indice, n, escolhido):
    se indice == n:
        contador = contador + 1
        retornar

    escolhido[indice] = falso
    explorarServicos(indice + 1, n, escolhido)

    escolhido[indice] = verdadeiro
    explorarServicos(indice + 1, n, escolhido)

procedimento iniciar(n):
    contador = 0
    escolhido = vetorDeBooleanos(n)
    explorarServicos(0, n, escolhido)
    retornar contador
```

**Considere:** cada chamada faz somente operações de custo constante, além das chamadas recursivas; o vetor `escolhido` é compartilhado e alterado na própria posição, sem cópias. A função contabiliza as configurações em vez de armazená-las. Explique a quantidade de chamadas finais para `n = 3` e `n = 4`. Analise o **trabalho total da árvore de chamadas**, não apenas a profundidade de uma única chamada.

---

## Exercício 10 — Experimentar todas as rotas de entrega

**Nível: difícil**

Uma transportadora deseja experimentar todas as possíveis ordens de visita a `n` destinos. Para cada ordem, calcula o custo da rota somando os custos de cada deslocamento consecutivo.

```text
melhorCusto = infinito

procedimento avaliarRota(rota, n):
    custo = distancia(deposito, rota[0])
    para i de 0 até n - 2:
        custo = custo + distancia(rota[i], rota[i + 1])
    custo = custo + distancia(rota[n - 1], deposito)
    melhorCusto = minimo(melhorCusto, custo)

procedimento gerarRotas(rota, inicio, n):
    se inicio == n:
        avaliarRota(rota, n)
        retornar

    para i de inicio até n - 1:
        trocar(rota[inicio], rota[i])
        gerarRotas(rota, inicio + 1, n)
        trocar(rota[inicio], rota[i])
```

**Considere:** `gerarRotas(rota, 0, n)` é a chamada inicial; `n >= 1`; as distâncias estão disponíveis para consulta em tempo constante; e cada troca custa tempo constante. Não se considera o custo de obter previamente as distâncias.

**Responda, justificando cada etapa:**

1. Quantas ordens diferentes de visita são geradas para `n = 3` e `n = 4`?
2. Quantas operações, aproximadamente, são necessárias para avaliar **uma** rota?
3. Como combinar o número de rotas e o custo de avaliação de cada rota?
4. Qual é o limite Big O para o tempo total dessa implementação?
5. Por que considerar apenas o número de rotas pode subestimar o custo total da implementação?

---

# Quadro de registro das análises

Preencha a tabela após resolver os exercícios. **Não há gabarito nesta folha.**

| Exercício | O que representa `n`? | Operação básica | Função ou limite de contagem | Big O do tempo total |
|---:|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |
| 8 | | | | |
| 9 | | | | |
| 10 | | | | |

## Checklist de revisão antes da entrega

- [ ] Defini o tamanho da entrada corretamente em cada exercício.
- [ ] Identifiquei uma operação básica ou expliquei como conto as iterações.
- [ ] Fiz pelo menos uma simulação com entrada pequena.
- [ ] Diferenciei **contagem exata de uma operação** de **custo total** quando necessário.
- [ ] Justifiquei minha classificação Big O.
- [ ] Nas demonstrações formais, explicitei uma desigualdade válida e as constantes `c` e `n0`.
- [ ] Nos exercícios recursivos, considerei **todas as chamadas** e não apenas um caminho da recursão.

**Fim da atividade.**
