# Trabalho Avaliativo — Teoria da Computação

# Parte I — Autômatos e Linguagens

## Questão 1

Considere:

```text
Σ = {0,1}
```

e a linguagem:

```text
L = { palavras que terminam em 01 }
```

Classifique as palavras abaixo como pertencentes ou não pertencentes a `L`:

```text
01
101
1101
0110
1
ε
```

Justifique duas das respostas.

---

## Questão 2

Construa um **AFD** sobre:

```text
Σ = {0,1}
```

que reconheça palavras que possuam **quantidade par de símbolos `1`**.

Para cada estado, explique o que ele precisa lembrar.

---

## Questão 3

Considere o AFD:

| Estado | a | b |
|---|---|---|
| q0 | q1 | q0 |
| q1 | q1 | q2 |
| q2 | q1 | q0 |

Considere:

```text
estado inicial = q0
estado final = q2
```

Simule:

```text
ab
aab
abb
baab
bbb
```

Depois descreva, em português, uma propriedade das palavras aceitas.

---

## Questão 4

Construa um **AFN** sobre `{a,b}` que aceite palavras que contenham a sequência:

```text
abb
```

em qualquer posição.

Depois explique por que seria possível construir um AFD equivalente.

---

# Parte II — Autômatos com Pilha

## Questão 5

Considere:

```text
L = { a^n b^n : n >= 0 }
```

Projete um **Autômato com Pilha** capaz de reconhecer a linguagem.

Sua solução deve indicar:

```text
quando ocorre push
quando ocorre pop
quando ocorre aceitação
```

---

## Questão 6

Utilizando o AP da questão anterior, simule:

```text
aaabbb
```

Mostre o conteúdo da pilha após cada símbolo processado.

---

## Questão 7

Agora simule:

```text
aabbb
```

Indique exatamente em que momento fica evidente que a palavra deve ser rejeitada.

---

## Questão 8

Projete uma estratégia para um AP reconhecer:

```text
L = { a^n b^m a^n : n >= 1 e m >= 1 }
```

Explique:

- o que será armazenado na pilha;
- o papel do bloco de `b`;
- quando começa o desempilhamento;
- qual condição determina a aceitação.

---

# Parte III — Máquina de Turing

## Questão 9

Considere:

```text
(q2, 1) -> (q3, X, L)
```

Explique detalhadamente:

- estado atual;
- símbolo lido;
- símbolo escrito;
- próximo estado;
- movimento da cabeça.

---

## Questão 10

Construa uma Máquina de Turing que receba uma palavra binária e troque:

```text
0 -> 1
1 -> 0
```

Por exemplo:

```text
10110
```

deve se tornar:

```text
01001
```

Apresente as transições necessárias.

---

## Questão 11

Construa uma Máquina de Turing que receba um número binário e **multiplique seu valor por 2**.

Exemplo:

```text
101
```

deve resultar em:

```text
1010
```

Explique a ideia antes de apresentar as transições.

---

## Questão 12

Modifique a estratégia anterior para multiplicar um número binário por:

```text
4
```

Explique por que a modificação funciona.

---

## Questão 13

Projete uma Máquina de Turing para reconhecer:

```text
L = { a^n b^n : n >= 1 }
```

Use símbolos auxiliares para marcar caracteres já utilizados.

Além das transições, explique o papel de cada grupo de estados.

---

## Questão 14

Projete uma estratégia de Máquina de Turing para reconhecer:

```text
L = { a^n b^n c^n : n >= 1 }
```

Use, por exemplo:

```text
X
Y
Z
```

para marcar símbolos já processados.

Não é necessário listar todas as transições, mas a estratégia deve ser suficientemente detalhada para permitir que a máquina seja implementada.

---

# Parte IV — Problemas Computacionais e Computabilidade

## Questão 15

Considere o problema:

> Dado um grafo `G` e dois vértices `s` e `t`, existe um caminho entre `s` e `t`?

Identifique:

- problema;
- uma possível instância;
- entrada;
- saída;
- tipo do problema.

---

## Questão 16

Transforme cada problema abaixo em sua versão de **decisão**:

a. encontrar o menor caminho entre duas cidades;  
b. encontrar a melhor rota para o caixeiro viajante;  
c. encontrar um ciclo Hamiltoniano em um grafo.

---

## Questão 17

Considere:

```text
ADFA = { <B,w> : B é um AFD que aceita w }
```

Descreva um algoritmo que decida `ADFA`.

Explique também por que esse algoritmo **sempre termina**.

---

## Questão 18

Considere:

```text
ATM = { <M,w> : M é uma Máquina de Turing que aceita w }
```

Um aluno propõe:

```text
1. Simule M sobre w.
2. Se M aceitar, aceite.
3. Se M rejeitar, rejeite.
```

Explique por que essa estratégia pode funcionar como **reconhecedor**, mas não necessariamente como **decisor**.

---

# Parte V — Problema da Parada

## Questão 19

Considere os programas:

```text
Programa A:

for i = 1 até 100:
    imprimir(i)
```

e:

```text
Programa B:

while verdadeiro:
    imprimir("Executando")
```

É possível determinar se esses dois programas terminam?

Explique por que isso **não contradiz** a indecidibilidade do Problema da Parada.

---

## Questão 20

Suponha que exista:

```text
HALT(P,x)
```

que responda corretamente:

```text
SIM -> P termina sobre x
NÃO -> P não termina sobre x
```

Construa o programa:

```text
D(P)
```

utilizado na ideia da prova de indecidibilidade.

Depois explique o que acontece ao executar:

```text
D(D)
```

## Entrga
Realize a entrega do trabalho utilizando o link> [https://forms.gle/HVYsyNyyzJSBjY2F7](https://forms.gle/HVYsyNyyzJSBjY2F7)

Entrega até dia 23/10/2026