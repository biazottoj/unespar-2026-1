# Atividade — Laboratório de Zoom e Representação de Imagens

## Objetivo

Modificar o programa desenvolvido em aula para criar um **comparador de técnicas de zoom**, utilizando uma imagem construída manualmente como matriz RGB.

Ao final, o programa deverá permitir comparar visualmente:

```text
Imagem original
Zoom In quadrado
Zoom In linear
Zoom Out quadrado
Zoom Out por média
```

A atividade deve ser realizada utilizando o código Python/OpenGL desenvolvido durante a aula.

---

# Parte 1 — Criando uma nova imagem

Substitua a matriz utilizada no exemplo por uma imagem própria de pelo menos:

```text
6 × 6 pixels
```

Cada pixel deve ser representado por:

```text
[R, G, B]
```

com valores entre:

```text
0.0 e 1.0
```

A imagem deve possuir pelo menos **6 cores diferentes**.

Não utilize arquivos externos de imagem. A imagem deve ser criada diretamente como uma matriz NumPy.

Exemplo:

```python
image = np.array([
    [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        ...
    ],
    ...
], dtype=np.float32)
```

Tente formar algum padrão visual simples, como:

- uma cruz;
- uma bandeira;
- uma letra;
- um símbolo;
- um padrão geométrico.

---

# Parte 2 — Inspecionando a matriz

Antes de aplicar qualquer transformação, exiba no terminal:

```python
print(image.shape)
```

Registre:

```text
altura =
largura =
quantidade de canais =
```

Depois escolha três pixels diferentes e apresente:

```python
print(image[linha, coluna])
```

Para cada pixel, indique qual cor ele representa aproximadamente.

---

# Parte 3 — Canais RGB

Adicione um modo ao programa que exiba separadamente:

```text
canal vermelho
canal verde
canal azul
```

Utilize a função desenvolvida em aula:

```python
only_channel(...)
```

Observe uma região colorida da imagem original e compare como ela aparece nos três canais.

## Responda

1. O que acontece com um pixel branco ao separar os três canais?
2. O que acontece com um pixel vermelho no canal verde?
3. Um pixel amarelo possui intensidade em quais canais RGB?

---

# Parte 4 — Comparação do Zoom In

Aplique fator:

```text
2
```

utilizando as duas técnicas:

```python
zoom_in_quadrado(...)
```

e:

```python
zoom_in_linear(...)
```

Crie um modo de visualização que permita alternar entre:

```text
3 → Zoom In quadrado
4 → Zoom In linear
```

Depois imprima:

```python
print(original.shape)
print(zoom_quadrado.shape)
print(zoom_linear.shape)
```

## Analise

Compare visualmente os dois resultados.

Responda:

1. Quantos pixels possui a imagem original?
2. Quantos pixels possui a imagem depois do Zoom In?
3. O Zoom In quadrado cria novas cores?
4. O Zoom In linear pode criar cores que não estavam explicitamente na matriz original?
5. Por que o resultado linear tende a apresentar transições mais suaves?

---

# Parte 5 — Encontrando um pixel interpolado

Escolha um pixel da imagem produzida pelo:

```text
Zoom In linear
```

que não corresponda exatamente a um pixel original.

Exiba seu valor:

```python
print(zoom_linear[linha, coluna])
```

Depois identifique os pixels da imagem original que influenciaram esse valor.

Não é necessário reproduzir todos os cálculos da interpolação bilinear, mas explique de onde surgiu a nova cor.

---

# Parte 6 — Comparação do Zoom Out

Agora utilize fator:

```text
2
```

para comparar:

```python
zoom_out_quadrado(...)
```

e:

```python
zoom_out_media(...)
```

Permita alternar:

```text
5 → Zoom Out quadrado
6 → Zoom Out por média
```

Imprima as dimensões das imagens resultantes.

## Responda

1. Qual dos métodos simplesmente descarta pixels?
2. Qual considera a informação dos vizinhos?
3. Em qual método existe maior chance de uma pequena região desaparecer completamente?
4. Por que a média pode produzir uma cor que não existia exatamente na imagem original?

---

# Parte 7 — Modo de comparação

Adicione dois novos modos ao programa.

```text
7 → comparação Zoom In
8 → comparação Zoom Out
```

## Modo 7

Exiba lado a lado:

```text
Original | Quadrado | Linear
```

## Modo 8

Exiba lado a lado:

```text
Original | Quadrado | Média
```

Não é necessário adicionar textos dentro da janela OpenGL. Basta organizar as três matrizes em regiões diferentes da tela.

---

# Parte 8 — Alterando o fator

Modifique o programa para testar:

```text
factor = 2
```

e:

```text
factor = 3
```

Compare os resultados.

Responda:

1. Uma imagem `6 × 6` submetida a Zoom In de fator 3 terá quais dimensões?
2. O aumento do fator torna mais evidente qual limitação do método quadrado?
3. No Zoom Out, o que acontece com a quantidade de informação quando o fator aumenta?

---

# Entrega

Entregue:

- código Python completo;
- imagem `6 × 6` criada pelo grupo;
- modos de comparação funcionando;
- respostas às questões da atividade.

O programa deve possuir, no mínimo:

```text
1 → original
2 → canais RGB
3 → Zoom In quadrado
4 → Zoom In linear
5 → Zoom Out quadrado
6 → Zoom Out por média
7 → comparação Zoom In
8 → comparação Zoom Out
```

---

# Desafio adicional

Crie uma imagem contendo uma fronteira forte entre duas cores, por exemplo:

```text
vermelho | azul
```

Aplique Zoom In quadrado e linear e compare especificamente os pixels próximos à fronteira.

Explique por que o método linear cria uma **transição de cores**, enquanto o método quadrado mantém uma separação abrupta.
