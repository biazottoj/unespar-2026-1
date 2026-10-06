# Atividade Prática — Diagnóstico e Correção de Contraste com Histograma

## Contexto

Uma aplicação de processamento de imagens recebe imagens que podem apresentar problemas de iluminação e contraste.

O objetivo é desenvolver, em **Python + OpenGL**, uma ferramenta simples capaz de executar o seguinte fluxo:

```text
Imagem
   ↓
Conversão para intensidade
   ↓
Histograma
   ↓
Diagnóstico
   ↓
Equalização
   ↓
Comparação antes/depois
```

A atividade utiliza os conceitos de imagem digital, varredura pixel a pixel, sistemas de cores, histograma e equalização trabalhados em aula.

---

# Parte 1 — Criando a imagem

Crie manualmente uma imagem RGB utilizando uma matriz NumPy de pelo menos:

```text
12 × 12 pixels
```

A imagem deve possuir regiões com diferentes cores e intensidades.

Não utilize um arquivo de imagem pronto.

Exemplo de estrutura:

```python
image = np.array([
    [
        [0.2, 0.1, 0.1],
        [0.3, 0.2, 0.2],
        ...
    ],
    ...
], dtype=np.float32)
```

A imagem deve conter propositalmente um problema de contraste.

Por exemplo, utilize predominantemente valores próximos de:

```text
0.30
0.35
0.40
0.45
0.50
```

Assim, apesar de existirem diferenças entre os pixels, grande parte da imagem estará concentrada em uma faixa relativamente pequena de intensidades.

---

# Parte 2 — Varredura pixel a pixel

Implemente uma função:

```python
def marcar_diagonal(image):
```

A função deve percorrer a imagem e alterar os pixels que satisfazem:

```text
linha == coluna
```

Esses pixels devem ficar com uma cor claramente identificável.

Por exemplo:

```text
preto
```

ou:

```text
vermelho
```

O objetivo desta etapa é demonstrar a manipulação direta de uma imagem por meio de **varredura pixel a pixel**, utilizando a ideia da reta:

```text
y = x
```

---

# Parte 3 — Conversão para intensidade

Converta a imagem RGB para uma representação em tons de cinza utilizando:

```text
Y = 0.299R + 0.587G + 0.114B
```

Crie:

```python
def converter_para_cinza(image):
```

A função deve produzir uma matriz bidimensional contendo apenas os valores de luminosidade.

Depois, converta-a novamente para três canais apenas para visualização no OpenGL:

```text
[Y, Y, Y]
```

---

# Parte 4 — Construção do histograma

Implemente:

```python
def calcular_histograma(gray, levels):
```

Utilize inicialmente:

```python
levels = 8
```

O histograma deve contar quantos pixels pertencem a cada nível.

Considere:

```text
rk → nível de cinza
nk → quantidade de pixels no nível
N  → quantidade total de pixels
```

Para cada nível, calcule também:

```text
P(rk) = nk / N
```

Apresente no terminal uma tabela como:

```text
Nível    Pixels    Probabilidade

0        3         0.0208
1        12        0.0833
2        35        0.2430
3        52        0.3611
...
```

---

# Parte 5 — Diagnóstico automático

Crie:

```python
def diagnosticar_histograma(hist):
```

A função deve classificar a imagem em uma destas três categorias:

```text
IMAGEM PREDOMINANTEMENTE ESCURA

IMAGEM PREDOMINANTEMENTE CLARA

IMAGEM COM NÍVEIS CONCENTRADOS
```

Não existe uma única regra obrigatória.

O grupo deve criar sua própria estratégia com base na distribuição dos pixels.

Por exemplo, vocês podem dividir o histograma em:

```text
níveis baixos
níveis intermediários
níveis altos
```

e comparar a quantidade de pixels em cada região.

Além do diagnóstico, o programa deve imprimir uma justificativa.

Exemplo:

```text
Diagnóstico: POUCO CONTRASTE

Justificativa:
78% dos pixels estão concentrados nos níveis 3 e 4.
```

---

# Parte 6 — Equalização

Implemente:

```python
def equalizar(gray, levels):
```

A função deve seguir as etapas estudadas:

```text
histograma
    ↓
probabilidade
    ↓
distribuição acumulada
    ↓
novo valor para cada nível
```

Utilize:

```text
P(rk) = nk / N
```

e:

```text
Sk = T(rk)
```

como base para o mapeamento dos níveis.

O resultado deverá ser uma nova imagem em tons de cinza.

---

# Parte 7 — Comparação visual

Adicione os seguintes modos ao programa OpenGL:

```text
1 → imagem RGB original
2 → imagem com a diagonal y = x
3 → imagem em tons de cinza
4 → histograma original
5 → imagem equalizada
6 → histograma equalizado
7 → comparação original × equalizada
```

No modo `7`, apresente lado a lado:

```text
+----------------------+----------------------+
|                      |                      |
|   Imagem Original    | Imagem Equalizada    |
|                      |                      |
+----------------------+----------------------+
|                      |                      |
| Histograma Original  | Hist. Equalizado     |
|                      |                      |
+----------------------+----------------------+
```

Não é necessário escrever os textos dentro da janela OpenGL.

Basta organizar corretamente as quatro visualizações.

---

# Parte 8 — Análise dos resultados

Após executar a equalização, responda:

1. Em quais níveis o histograma original estava mais concentrado?
2. O diagnóstico automático classificou corretamente a imagem?
3. O histograma equalizado utiliza uma faixa maior de níveis?
4. O contraste visual aumentou?
5. A quantidade de pixels da imagem mudou?
6. A resolução da imagem mudou?
7. O que foi efetivamente alterado pela equalização?
8. Por que o histograma é útil mesmo antes de modificar a imagem?

---

# Desafio

Modifique a imagem original para produzir três versões:

```text
A → imagem predominantemente escura
B → imagem predominantemente clara
C → imagem com pouco contraste
```

Execute **o mesmo algoritmo**, sem alterar o código de diagnóstico.

Para cada imagem, apresente:

```text
imagem
histograma
diagnóstico automático
imagem equalizada
histograma equalizado
```

O desafio é fazer com que o algoritmo consiga identificar adequadamente as três situações.