# Estudo Guiado de Revisão — Teoria da Computação

## Conteúdos do bimestre

Este estudo guiado reúne os principais conteúdos trabalhados durante o bimestre:

- autômatos finitos;
- autômatos com pilha;
- máquinas de Turing;
- tipos de problemas computacionais;
- decidibilidade e reconhecibilidade;
- Problema da Parada;
- redução de problemas;
- tempo polinomial e exponencial;
- classes P e NP;
- problemas NP-difíceis e NP-completos.

---

# Parte I — Autômatos Finitos

## 1. Linguagens, alfabetos e palavras

Um **alfabeto** é um conjunto finito de símbolos.

Exemplo:

```text
Σ = {0, 1}
```

Uma **palavra** é uma sequência finita formada por símbolos do alfabeto.

Exemplos:

```text
0
1
01
1011
```

A palavra vazia é representada por:

```text
ε
```

Uma **linguagem** é um conjunto de palavras.

Exemplo:

```text
L = { palavras sobre {0,1} que terminam em 1 }
```

Palavras como:

```text
1
01
101
1101
```

pertencem a essa linguagem.

---

## 2. Autômato Finito Determinístico — AFD

Um **Autômato Finito Determinístico (AFD)** é uma máquina com:

- conjunto finito de estados;
- alfabeto;
- função de transição;
- estado inicial;
- conjunto de estados finais.

Representação:

```text
AFD = (Q, Σ, δ, q0, F)
```

onde:

```text
Q  = conjunto de estados
Σ  = alfabeto
δ  = função de transição
q0 = estado inicial
F  = conjunto de estados finais
```

No AFD, para cada combinação:

```text
estado atual + símbolo lido
```

existe exatamente **um próximo estado**.

### Exemplo

Considere um AFD que reconhece palavras sobre `{0,1}` que terminam em `1`.

| Estado | 0 | 1 |
|---|---|---|
| q0 | q0 | q1 |
| q1 | q0 | q1 |

Estado inicial:

```text
q0
```

Estado final:

```text
q1
```

Assim:

```text
101 -> aceita
110 -> rejeita
1   -> aceita
ε   -> rejeita
```

---

## 3. Autômato Finito Não Determinístico — AFN

No **Autômato Finito Não Determinístico (AFN)**, uma combinação de estado e símbolo pode possuir:

- nenhuma transição;
- uma transição;
- várias transições.

Um AFN aceita uma palavra quando **pelo menos um caminho possível** termina em estado final.

Dependendo da definição utilizada, também podem existir transições `ε`, nas quais a máquina muda de estado sem consumir símbolo da entrada.

Apesar da diferença:

```text
AFD e AFN possuem o mesmo poder expressivo.
```

Todo AFN pode ser convertido para um AFD equivalente.

---

# Exercícios — Parte I

## Exercício 1

Explique a diferença entre:

```text
alfabeto
palavra
linguagem
```

Dê um exemplo de cada um utilizando o alfabeto `{a,b}`.

---

## Exercício 2

Considere o AFD:

| Estado | a | b |
|---|---|---|
| q0 | q1 | q0 |
| q1 | q1 | q0 |

Estado inicial:

```text
q0
```

Estado final:

```text
q1
```

Simule as palavras:

```text
a
b
aba
abb
bba
ε
```

Depois descreva, em português, a linguagem reconhecida.

---

## Exercício 3

Construa um AFD sobre `{0,1}` que reconheça palavras de comprimento ímpar.

Para cada estado, explique **o que ele representa**.

---

## Exercício 4

Explique a principal diferença entre AFD e AFN.

Depois responda:

> Um AFN é mais poderoso que um AFD em termos das linguagens que consegue reconhecer?

Justifique.

---

# Parte II — Autômatos com Pilha

## 4. Por que um AFD não é suficiente?

Um AFD possui memória limitada aos seus estados.

Considere:

```text
L = { a^n b^n : n >= 0 }
```

Exemplos:

```text
ε
ab
aabb
aaabbb
```

Para reconhecer essa linguagem, é necessário lembrar quantos `a` foram encontrados para depois comparar com a quantidade de `b`.

Como `n` pode crescer indefinidamente, uma quantidade fixa de estados não é suficiente.

---

## 5. Autômato com Pilha — AP

Um **Autômato com Pilha (AP)** adiciona uma pilha ao modelo de autômato finito.

A pilha segue a estrutura:

```text
LIFO
Last In, First Out
```

As principais operações são:

```text
push -> empilhar
pop  -> desempilhar
```

A pilha fornece memória adicional ao autômato.

Autômatos com Pilha estão associados às **linguagens livres de contexto**.

---

## 6. Exemplo: a^n b^n

Para reconhecer:

```text
L = { a^n b^n : n >= 0 }
```

podemos utilizar a estratégia:

```text
para cada a:
    empilhar X

para cada b:
    desempilhar X

ao final:
    aceitar somente se a pilha voltou ao marcador inicial
```

Para a entrada:

```text
aaabbb
```

a ideia é:

```text
a -> empilha X
a -> empilha X
a -> empilha X

b -> remove X
b -> remove X
b -> remove X
```

Ao final, a quantidade de `a` corresponde à quantidade de `b`.

---

## 7. Limitações do AP

O AP é mais poderoso que o AFD, mas ainda possui limitações.

Por exemplo:

```text
L = { a^n b^n c^n : n >= 1 }
```

não pode ser reconhecida por um Autômato com Pilha convencional.

Nesse caso, precisamos de um modelo mais poderoso, como uma Máquina de Turing.

---

# Exercícios — Parte II

## Exercício 5

Explique por que um AFD não consegue reconhecer:

```text
L = { a^n b^n : n >= 0 }
```

---

## Exercício 6

Considere a entrada:

```text
aabb
```

para um AP que reconhece:

```text
L = { a^n b^n : n >= 0 }
```

Mostre a evolução da pilha após cada símbolo.

---

## Exercício 7

Repita a análise para:

```text
aaabb
```

A palavra deve ser aceita ou rejeitada?

Justifique utilizando o conteúdo da pilha.

---

## Exercício 8

Proponha uma estratégia de alto nível para um AP que reconheça:

```text
L = { a^n b^m a^n : n >= 0 e m > 0 }
```

Explique:

1. o que deve ser empilhado;
2. quando começa o desempilhamento;
3. para que servem os símbolos `b`.

---

# Parte III — Máquina de Turing

## 8. O modelo de Máquina de Turing

A **Máquina de Turing (MT)** é um modelo abstrato de computação mais poderoso que AFDs e APs.

Seus principais componentes são:

```text
fita
cabeça de leitura/escrita
conjunto de estados
função de transição
```

A cabeça pode:

```text
ler um símbolo
escrever um símbolo
mover-se para a esquerda
mover-se para a direita
mudar de estado
```

A fita funciona como uma memória potencialmente ilimitada.

---

## 9. Função de transição

Uma transição pode ser interpretada como:

```text
estado atual + símbolo lido
        ->
novo estado + símbolo escrito + movimento
```

Exemplo:

```text
(q0, 0) -> (q0, 1, R)
```

Significa:

1. a máquina está em `q0`;
2. lê `0`;
3. escreve `1`;
4. permanece em `q0`;
5. move a cabeça para a direita.

---

## 10. Exemplo: complemento binário

Uma MT pode transformar:

```text
10110
```

em:

```text
01001
```

Estratégia:

```text
0 -> escrever 1 e mover para direita
1 -> escrever 0 e mover para direita
branco -> parar
```

---

## 11. Exemplo: a^n b^n c^n

Uma estratégia para reconhecer:

```text
L = { a^n b^n c^n : n >= 1 }
```

é:

```text
1. marcar um a ainda não utilizado como X;
2. procurar um b ainda não utilizado e marcar como Y;
3. procurar um c ainda não utilizado e marcar como Z;
4. voltar ao início;
5. repetir;
6. aceitar quando não restarem símbolos não marcados.
```

---

# Exercícios — Parte III

## Exercício 9

Liste e explique os principais componentes de uma Máquina de Turing.

---

## Exercício 10

Interprete a transição:

```text
(q2, 1) -> (q3, X, L)
```

Explique cada elemento.

---

## Exercício 11

Considere uma MT que realiza complemento binário.

Mostre passo a passo o resultado para:

```text
10101
```

---

## Exercício 12

Explique, em alto nível, como uma MT pode reconhecer:

```text
L = { a^n b^n c^n : n >= 1 }
```

Indique quais símbolos auxiliares podem ser utilizados e por que a MT consegue realizar essa tarefa enquanto um AP convencional não consegue.

---

# Parte IV — Problemas Computacionais e Decidibilidade

## 12. Problema, instância, entrada e saída

Um **problema computacional** descreve uma tarefa geral.

Uma **instância** é um caso específico do problema.

Exemplo:

```text
Problema:
encontrar o menor elemento de uma lista

Instância:
[8, 3, 11, 2, 7]

Saída:
2
```

Um algoritmo deve resolver todas as instâncias válidas do problema.

---

## 13. Problemas de decisão, busca e otimização

### Problema de decisão

Produz:

```text
SIM ou NÃO
```

Exemplo:

> Existe caminho entre `s` e `t`?

### Problema de busca

Pede uma solução concreta.

Exemplo:

> Encontre um caminho entre `s` e `t`.

### Problema de otimização

Pede a melhor solução de acordo com algum critério.

Exemplo:

> Encontre o caminho de menor custo entre `s` e `t`.

---

## 14. Linguagem como problema de decisão

Um problema de decisão pode ser representado como uma linguagem.

Exemplo:

```text
ADFA = { <B,w> : B é um AFD que aceita w }
```

Assim:

```text
<B,w> pertence a ADFA
```

significa que:

```text
B aceita w
```

---

## 15. Decidibilidade

Um problema é **decidível** quando existe um algoritmo que:

```text
1. recebe qualquer instância válida;
2. produz a resposta correta;
3. sempre termina.
```

Uma Máquina de Turing que possui essa propriedade é chamada de **decisor**.

---

## 16. Reconhecibilidade

Um **reconhecedor** possui uma garantia mais fraca.

Se:

```text
w pertence a L
```

ele aceita e termina.

Se:

```text
w não pertence a L
```

ele pode:

```text
rejeitar e terminar
OU
continuar executando indefinidamente
```

Comparação:

| Caso | Decisor | Reconhecedor |
|---|---|---|
| entrada pertence à linguagem | aceita e para | aceita e para |
| entrada não pertence | rejeita e para | rejeita ou pode não parar |
| sempre termina? | sim | não necessariamente |

---

## 17. Problema da Parada

O **Problema da Parada** pergunta:

> Dado um programa `P` e uma entrada `x`, o programa termina quando executado sobre `x`?

Em termos de Máquina de Turing:

```text
HALT = { <M,w> : M termina quando executada sobre w }
```

O Problema da Parada é **indecidível**.

Isso significa que não existe um algoritmo geral que receba qualquer programa e qualquer entrada e sempre determine corretamente se a execução terminará.

Isso não significa que nunca conseguimos analisar se um programa específico termina.

---

## 18. Ideia da prova do Problema da Parada

Suponha que exista um algoritmo perfeito:

```text
HALT(P,x)
```

que responda corretamente se `P(x)` termina.

Criamos então:

```text
D(P):

    se HALT(P,P) = SIM:
        entre em loop

    caso contrário:
        pare
```

Agora perguntamos:

```text
D(D) termina?
```

Se `HALT` disser que termina, `D` entra em loop.

Se `HALT` disser que não termina, `D` termina.

Surge uma contradição.

Logo, um decisor geral para o Problema da Parada não pode existir.

---

# Exercícios — Parte IV

## Exercício 13

Explique a diferença entre:

```text
problema
instância
entrada
saída
```

Utilize um exemplo diferente dos apresentados no material.

---

## Exercício 14

Classifique cada problema como decisão, busca ou otimização:

a. Existe um caminho entre os vértices `A` e `B`?  
b. Encontre um caminho entre os vértices `A` e `B`.  
c. Encontre o caminho de menor custo entre `A` e `B`.  
d. Existe uma rota do caixeiro viajante com custo menor ou igual a 100?

---

## Exercício 15

Explique o que é um **decisor** e o que é um **reconhecedor**.

Depois complete:

| Entrada | Decisor | Reconhecedor |
|---|---|---|
| pertence à linguagem | | |
| não pertence à linguagem | | |
| sempre termina? | | |

---

## Exercício 16

Considere:

```text
ATM = { <M,w> : M é uma MT que aceita w }
```

Explique por que podemos reconhecer `ATM` simulando `M` sobre `w`.

Depois explique por que essa mesma estratégia não produz um decisor.

---

## Exercício 17

Explique o Problema da Parada com suas próprias palavras.

Depois explique o que significa afirmar que ele é **indecidível**.

---

## Exercício 18

Explique a ideia central da prova por contradição do Problema da Parada.

Sua resposta deve mencionar:

```text
algoritmo hipotético HALT
autorreferência
D(D)
contradição
```

---

# Parte V — Redução de Problemas

## 19. O que é uma redução?

Reduzir um problema `A` a um problema `B` significa transformar uma instância de `A` em uma instância de `B` de forma que a resposta seja preservada.

Representamos:

```text
A <=p B
```

quando a transformação pode ser realizada em tempo polinomial.

Intuitivamente:

```text
instância de A
      |
      | transformação
      v
instância de B
      |
      | solução de B
      v
resposta para A
```

---

## 20. O significado da direção

Se:

```text
A <=p B
```

então:

> Se eu souber resolver `B`, posso usar essa solução para resolver `A`.

Assim, `B` é pelo menos tão difícil quanto `A`.

Uma forma prática de lembrar:

```text
A -> B
```

A seta aponta para o problema que gostaríamos de saber resolver.

---

## 21. Como provar uma redução

Para provar:

```text
A <=p B
```

devemos mostrar três elementos:

### 1. Construção

Como transformar uma instância de `A` em uma instância de `B`.

### 2. Correção

A transformação deve preservar a resposta:

```text
x pertence a A
se, e somente se,
f(x) pertence a B
```

### 3. Tempo

A transformação `f` deve ser computável em tempo polinomial.

---

## 22. Exemplo: Ciclo Hamiltoniano para TSP

Um **ciclo Hamiltoniano**:

```text
visita todos os vértices
visita cada vértice exatamente uma vez
retorna ao início
```

O problema `HAM` pergunta:

> Dado um grafo `G`, existe um ciclo Hamiltoniano?

O **TSP de decisão** pergunta:

> Existe uma rota que visita todas as cidades exatamente uma vez, retorna ao início e possui custo menor ou igual a `k`?

Para reduzir HAM para TSP:

```text
1. mantenha os mesmos vértices;
2. complete o grafo;
3. dê peso 1 às arestas que existiam no grafo original;
4. dê peso 2 às arestas que não existiam;
5. defina k = número de vértices.
```

A transformação é polinomial porque precisamos examinar no máximo uma quantidade da ordem de:

```text
O(n²)
```

pares de vértices.

---

# Exercícios — Parte V

## Exercício 19

Explique, com suas palavras, o significado de:

```text
A <=p B
```

Depois explique qual dos dois problemas pode ser considerado, no mínimo, tão difícil quanto o outro.

---

## Exercício 20

Liste e explique as três etapas necessárias para provar corretamente uma redução polinomial.

---

## Exercício 21

Um aluno deseja provar que um problema `X` é NP-difícil.

Ele sabe que `HAM` é NP-completo.

Qual redução deve tentar construir?

```text
X <=p HAM
```

ou:

```text
HAM <=p X
```

Explique por que a direção importa.

---

## Exercício 22

Considere:

```text
V = {A, B, C, D}
E = {AB, BC, CD, DA}
```

Realize a transformação de HAM para TSP:

1. complete o grafo;
2. atribua pesos 1 e 2;
3. determine `k`;
4. encontre uma rota de custo menor ou igual a `k`, se existir;
5. explique por que a transformação pode ser feita em tempo `O(n²)`.

---

# Parte VI — Classes de Problemas: P, NP, NP-Difícil e NP-Completo

## 23. Complexidade de tempo

O tempo de execução de um algoritmo pode ser expresso em função do tamanho da entrada.

Exemplos:

```text
n
n²
n³
2ⁿ
n!
```

Funções como:

```text
n
n²
n³
5n² + 3n + 1
```

são polinomiais.

Funções como:

```text
2ⁿ
3ⁿ
n!
```

crescem muito mais rapidamente.

---

## 24. Classe P

A classe **P** contém problemas de decisão que podem ser resolvidos em tempo polinomial por um algoritmo determinístico.

Exemplo:

> Existe caminho entre `s` e `t` em um grafo?

Podemos resolver usando BFS ou DFS em:

```text
O(|V| + |E|)
```

Portanto, esse problema pertence a `P`.

---

## 25. Classe NP

A classe **NP** contém problemas de decisão cujas soluções candidatas podem ser verificadas em tempo polinomial.

Importante:

```text
NP não significa "não polinomial".
```

Exemplo:

> Existe um ciclo Hamiltoniano em `G`?

Encontrar o ciclo pode ser difícil.

Mas, se alguém fornecer:

```text
A -> B -> C -> D -> A
```

podemos verificar rapidamente:

```text
todos os vértices aparecem?
há repetição?
todas as arestas existem?
o ciclo retorna ao início?
```

Logo:

```text
HAM pertence a NP
```

---

## 26. Relação entre P e NP

Todo problema de `P` também pertence a `NP`.

```text
P está contido em NP
```

A grande pergunta é:

```text
P = NP?
```

Ou seja:

> Todo problema cuja solução pode ser verificada em tempo polinomial também pode ser resolvido em tempo polinomial?

---

## 27. NP-difícil

Um problema `B` é **NP-difícil** quando todo problema em `NP` pode ser reduzido a `B` em tempo polinomial.

Isso significa:

> `B` é pelo menos tão difícil quanto qualquer problema de NP.

Um problema NP-difícil não precisa pertencer a NP.

---

## 28. NP-completo

Um problema é **NP-completo** quando:

```text
1. pertence a NP;
2. é NP-difícil.
```

Portanto:

```text
NP-completo = pertence a NP + NP-difícil
```

Exemplos clássicos:

```text
Ciclo Hamiltoniano — decisão
TSP — decisão
SAT
```

---

## 29. TSP: decisão e otimização

### TSP de decisão

Pergunta:

> Existe uma rota com custo menor ou igual a `k`?

Essa versão é NP-completa.

### TSP de otimização

Pergunta:

> Qual é a rota de menor custo?

Essa versão é NP-difícil.

A versão de otimização não é normalmente chamada de NP-completa porque `NP` é definida para problemas de decisão.

---

# Exercícios — Parte VI

## Exercício 23

Classifique as funções abaixo como polinomiais ou não polinomiais:

```text
n
n²
n⁵ + 3n
2ⁿ
3ⁿ
n!
```

---

## Exercício 24

Explique o que significa dizer que um problema pertence à classe `P`.

Dê um exemplo.

---

## Exercício 25

Explique o que significa dizer que um problema pertence à classe `NP`.

Sua resposta deve destacar a diferença entre:

```text
resolver
verificar
```

---

## Exercício 26

Explique a relação:

```text
P está contido em NP
```

Depois explique a pergunta:

```text
P = NP?
```

---

## Exercício 27

Defina, com suas palavras:

```text
NP-difícil
NP-completo
```

Depois explique a diferença entre os dois conceitos.

---

## Exercício 28

Considere um problema `Y`.

Sabemos que:

```text
HAM <=p Y
```

e também sabemos que:

```text
Y pertence a NP
```

Sabendo que HAM é NP-completo, o que podemos concluir sobre `Y`?

Justifique.

---

## Exercício 29

Explique por que:

```text
TSP de decisão
```

é classificado como NP-completo, enquanto:

```text
TSP de otimização
```

é normalmente classificado como NP-difícil.


# Checklist final de revisão

| Conceito | Pergunta de revisão |
|---|---|
| Alfabeto | Quais símbolos podem aparecer nas palavras? |
| Palavra | Qual sequência de símbolos está sendo processada? |
| Linguagem | Quais palavras pertencem ao conjunto? |
| AFD | O que cada estado precisa lembrar? |
| AFN | Existem vários caminhos possíveis de execução? |
| AP | Que informação precisa ser armazenada na pilha? |
| `push` | Qual símbolo será empilhado? |
| `pop` | Qual informação está sendo removida da pilha? |
| MT | O que precisa ser lido, escrito ou marcado na fita? |
| Transição de MT | O que é lido, escrito e para onde a cabeça se move? |
| Problema computacional | Qual tarefa geral queremos resolver? |
| Instância | Qual caso específico estamos analisando? |
| Decisão | A resposta esperada é SIM ou NÃO? |
| Busca | Precisamos encontrar uma solução concreta? |
| Otimização | Precisamos encontrar a melhor solução? |
| Decisor | O algoritmo sempre termina? |
| Reconhecedor | O que acontece quando a entrada não pertence à linguagem? |
| Problema da Parada | Existe um algoritmo geral que determine a terminação de qualquer programa? |
| Redução | Como transformar uma instância de A em uma instância de B? |
| Correção da redução | A transformação preserva respostas SIM e NÃO? |
| Redução polinomial | A transformação é executada em tempo polinomial? |
| P | O problema pode ser resolvido em tempo polinomial? |
| NP | Uma solução candidata pode ser verificada em tempo polinomial? |
| NP-difícil | Todo problema de NP reduz para esse problema? |
| NP-completo | O problema está em NP e também é NP-difícil? |
| TSP decisão | Existe uma rota de custo <= k? |
| TSP otimização | Qual é a melhor rota possível? |
| Ciclo Hamiltoniano | Existe um ciclo que visita todos os vértices exatamente uma vez? |

---

# Estratégia para resolver questões de autômatos e máquinas

```text
1. Qual linguagem deve ser reconhecida?
2. O que a máquina precisa lembrar?
3. Uma quantidade finita de estados é suficiente?
4. É necessário contar ou comparar quantidades?
5. Uma pilha resolve o problema?
6. É necessário voltar na entrada ou alterar símbolos?
7. Se sim, uma Máquina de Turing pode ser necessária.
8. Defina claramente o significado de cada estado.
9. Simule pelo menos uma entrada aceita.
10. Simule pelo menos uma entrada rejeitada.
```

---

# Estratégia para resolver questões de decidibilidade

```text
1. Qual é o problema de decisão?
2. Qual é a entrada?
3. Qual é a resposta SIM?
4. Existe um algoritmo para resolver o problema?
5. Esse algoritmo sempre termina?
6. Se não termina em todas as entradas, ele é apenas um reconhecedor?
7. Existe alguma prova de que nenhum decisor pode existir?
```

---

# Estratégia para resolver questões de redução

```text
1. Qual é o problema de origem A?
2. Qual é o problema de destino B?
3. Como transformar uma instância de A em uma instância de B?
4. A resposta SIM de A corresponde a SIM em B?
5. A resposta NÃO de A corresponde a NÃO em B?
6. A transformação é calculável em tempo polinomial?
7. O que podemos concluir a partir de A <=p B?
```

---

# Estratégia para classificar problemas em P, NP, NP-difícil e NP-completo

```text
1. O problema é de decisão?
2. Existe algoritmo polinomial conhecido?
   -> se sim, ele pertence a P.
3. Uma solução candidata pode ser verificada em tempo polinomial?
   -> se sim, ele pertence a NP.
4. Um problema NP-completo conhecido reduz para ele?
   -> isso ajuda a provar NP-dificuldade.
5. O problema está em NP e é NP-difícil?
   -> então é NP-completo.
6. Se for um problema de otimização que recebe redução de um problema NP-completo,
   ele pode ser NP-difícil sem ser chamado de NP-completo.
```
