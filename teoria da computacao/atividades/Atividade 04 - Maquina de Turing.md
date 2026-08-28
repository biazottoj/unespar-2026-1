# Lista de Exercícios — Máquina de Turing


## Exercício 1 — Interpretando transições

Explique, o significado de cada transição abaixo:

1. \(\delta(q_0,0)=(q_1,1,R)\)
2. \(\delta(q_1,1)=(q_1,0,L)\)
3. \(\delta(q_2,\square)=(q_f,\square,R)\)

Para cada uma, indique:

- estado atual;
- símbolo lido;
- símbolo escrito;
- novo estado;
- direção do movimento.

---

## Exercício 2 — Substituição de símbolos

Construa uma MT que receba uma palavra sobre:

\[
\Sigma=\{a,b\}
\]

e faça a troca:

```text
a → b
b → a
```

Exemplo:

```text
abba → baab
```

---

## Exercício 3 — Multiplicação por 4 em binário

Em binário, multiplicar por 4 equivale a acrescentar dois zeros ao final do número.

Exemplo:

```text
101 → 10100
```

Construa uma MT que faça essa transformação.

Depois, determine a saída para:

1. `1`
2. `10`
3. `101`
4. `1111`
5. `10000`

---

## Exercício 4 — Incremento binário

Considere uma MT que recebe um número binário e soma 1.

Determine a saída para:

1. `0`
2. `1`
3. `10`
4. `1011`
5. `111`
6. `1111`

Mostre o passo a passo para pelo menos duas entradas.

---

## Exercício 5 — Reconhecimento de \(a^n b^n c^n\)

Construa uma MT que reconheça:

\[
L=\{a^n b^n c^n | n >= 0}
\]

usando marcas:

- `X` para `a` processado;
- `Y` para `b` processado;
- `Z` para `c` processado.

Depois, classifique:

1. `abc`
2. `aabbcc`
3. `aaabbbccc`
4. `aabcc`
5. `abbcc`
6. `aabbc`

---

## Exercício 6 — Palíndromos sobre \(\{a,b\}\)

Descreva, conceitualmente, uma MT que reconheça palíndromos sobre:

\[
\Sigma=\{a,b\}
\]

Exemplos aceitos:

```text
a
aa
aba
abba
baab
```

Exemplos rejeitados:

```text
ab
abb
abab
```

Explique como a máquina compara o primeiro e o último símbolo ainda não processados.

---

## Exercício 7 — Duplicação de palavra

Descreva conceitualmente uma MT que recebe uma palavra \(w\in\{a,b\}^*\) e produz \(ww\).

Exemplo:

```text
ab → abab
```

Sua resposta deve explicar:

1. como marcar símbolos já copiados;
2. como encontrar o final da palavra;
3. como escrever a cópia;
4. quando a máquina deve parar.

---

## Exercício 8 — Comparação conceitual

Para cada tarefa abaixo, indique se ela é mais naturalmente resolvida por:

- AFD;
- Autômato com Pilha;
- Máquina de Turing.

Justifique.

1. Reconhecer palavras binárias com quantidade par de `1`s.
2. Reconhecer \(\{a^n b^n\mid n\geq0\}\).
3. Reconhecer \(\{a^n b^n c^n\mid n\geq0\}\).
4. Trocar todos os `0`s por `1`s e todos os `1`s por `0`s.
5. Somar 1 a um número binário.
