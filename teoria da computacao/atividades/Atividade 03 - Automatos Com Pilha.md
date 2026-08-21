# Lista de Exercícios — Autômatos com Pilha

A lista abaixo contém **4 exercícios em ordem progressiva de dificuldade** sobre Autômatos com Pilha (AP).

---

## Exercício 1 — Simulação de um AP para (a^n b^n)

Considere um Autômato com Pilha que reconhece:

L={a^n b^n | n >= 0}

utilizando a estratégia:

- para cada `a`, empilhar um símbolo `X`;
- ao começar a ler `b`, desempilhar um `X` para cada `b`;
- aceitar se a entrada terminar e a pilha ficar vazia.

Para cada palavra abaixo:

1. mostre o conteúdo da pilha após cada símbolo lido;
2. indique se a palavra é aceita ou rejeitada.

Palavras:

a) `ab`  
b) `aabb`  
c) `aaabbb`  
d) `aaabb`  
e) `aabbb`

---

## Exercício 2 — Parênteses balanceados

Considere um AP que reconhece expressões com parênteses balanceados.

A estratégia é:

- ao ler `(`, empilhar `X`;
- ao ler `)`, desempilhar `X`;
- rejeitar se for necessário desempilhar quando não houver `X` disponível;
- aceitar se, ao final da entrada, a pilha estiver vazia.

Classifique as palavras abaixo como aceitas ou rejeitadas e mostre a evolução da pilha:

a) `()`  
b) `(())`  
c) `(()())`  
d) `())`  
e) `(()`

Depois, explique por que uma pilha é uma estrutura adequada para esse tipo de linguagem.

---

## Exercício 3 — Linguagem (a^n c b^n)

Construa a estratégia de um AP para reconhecer:

L={a^n c b^n | n >= 0}

Exemplos aceitos:

```text
c
acb
aacbb
aaacbbb
```

Exemplos rejeitados:

```text
ab
acbb
aacb
aaccbb
```

Apresente:

1. o significado de cada estado;
2. o símbolo utilizado na pilha;
3. quando ocorre o empilhamento;
4. quando ocorre o desempilhamento;
5. a condição de aceitação;
6. o processamento completo da palavra `aacbb`.

---

## Exercício 4 — Linguagem (a^n b^m a^n)

Construa conceitualmente um AP que reconheça:
L={a^n b^m a^n | n >= 0, m > 0}

Exemplos aceitos:

```text
b
bb
aba
abba
aabaa
aabbaa
aaabaaa
```

Exemplos rejeitados:

```text
aa
abaa
aabaaa
aaabb
```

Sua resposta deve apresentar:

1. as diferentes fases do processamento;
2. o significado de cada estado;
3. as operações realizadas sobre a pilha em cada fase;
4. a condição de aceitação;
5. a simulação completa da palavra `aabbaa`.

Ao final, explique por que a palavra `b` deve ser aceita.
