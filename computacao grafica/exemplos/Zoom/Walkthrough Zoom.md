# Walkthrough — Cores, Imagem como Matriz e Zoom com Python/OpenGL

## Objetivo

Este walkthrough acompanha o conteúdo da aula **Matriz de Imagem e Zoom** e pode ser utilizado tanto durante a aula quanto posteriormente como material de estudo.

A proposta é alternar entre:

- conceitos apresentados nos slides;
- análise de exemplos;
- implementação incremental em Python/OpenGL;
- observação dos resultados na tela.

Ao final, deve ser possível compreender:

- como representar cores numericamente;
- como uma imagem pode ser tratada como uma matriz;
- como representar canais RGB;
- como uma matriz pode ser transformada em geometria para renderização com OpenGL;
- como implementar Zoom In;
- como implementar Zoom Out;
- a diferença entre ampliação por repetição e por interpolação;
- a diferença entre redução por amostragem e por média de vizinhos.

---

# 1. Arquivos utilizados

A aula utiliza quatro arquivos:

1. `slides_matriz_imagem_zoom_beamer.tex`  
   Conjunto de slides com os conceitos principais.

2. `walkthrough_matriz_imagem_zoom_opengl.md`  
   Este roteiro, utilizado para acompanhar a sequência entre teoria e implementação.

3. `imagem_zoom_base_aula.py`  
   Código com pontos a serem completados ao longo da aula.

4. `imagem_zoom_completo.py`  
   Versão completa do programa para comparação e testes.

Uma sequência recomendada é:

```text
Slides
  ↓
Conceito
  ↓
Código base
  ↓
Implementação
  ↓
Execução
  ↓
Observação do resultado
```

---

# 2. Visão geral da aplicação

Antes de implementar cada operação, execute a versão completa:

```bash
python imagem_zoom_completo.py
```

O programa possui os seguintes modos:

```text
1 → imagem original
2 → canais RGB
3 → Zoom In quadrado
4 → Zoom In linear
5 → Zoom Out quadrado
6 → Zoom Out por média
H → ajuda no terminal
ESC → sair
```

Alterne entre os modos e observe que todos partem da **mesma matriz de imagem**, mas produzem representações diferentes.

A pergunta que orienta a aula é:

> Se uma imagem pode ser representada como uma matriz, como podemos modificar essa matriz para ampliar, reduzir ou separar suas informações de cor?

---

# 3. Cores e representação RGB

## 3.1 Conceito

Computadores não armazenam uma cor como uma sensação visual. Uma cor precisa ser representada numericamente.

No modelo RGB:

```text
R = Red   = Vermelho
G = Green = Verde
B = Blue  = Azul
```

Uma cor pode ser representada como:

```text
[R, G, B]
```

No código OpenGL utilizado nesta aula, os valores dos canais são normalizados para o intervalo:

```text
0.0 → intensidade mínima
1.0 → intensidade máxima
```

Alguns exemplos:

```text
Vermelho = [1.0, 0.0, 0.0]
Verde    = [0.0, 1.0, 0.0]
Azul     = [0.0, 0.0, 1.0]
Branco   = [1.0, 1.0, 1.0]
Preto    = [0.0, 0.0, 0.0]
Amarelo  = [1.0, 1.0, 0.0]
Ciano    = [0.0, 1.0, 1.0]
Magenta  = [1.0, 0.0, 1.0]
```

### Para observar

Compare:

```text
[1.0, 0.0, 0.0]
```

com:

```text
[0.5, 0.0, 0.0]
```

Nos dois casos o canal predominante é vermelho, mas a intensidade é diferente.

---

# 4. Construindo uma imagem como matriz

Abra o arquivo:

```text
imagem_zoom_base_aula.py
```

Localize:

```python
def create_demo_image():
    # CRIAR MATRIZ DE IMAGEM AQUI
```

A imagem será representada por uma matriz NumPy com o formato:

```text
altura × largura × canais
```

Para uma imagem RGB:

```text
canais = 3
```

Portanto, uma imagem `4 × 4` terá a forma:

```text
4 linhas × 4 colunas × 3 valores por pixel
```

Complete a função com:

```python
def create_demo_image():
    return np.array([
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 1.0, 1.0],
        ],
        [
            [1.0, 0.5, 0.0],
            [0.5, 0.0, 1.0],
            [0.0, 1.0, 1.0],
            [0.0, 0.0, 0.0],
        ],
        [
            [1.0, 1.0, 0.0],
            [0.2, 0.8, 0.2],
            [0.2, 0.4, 1.0],
            [0.9, 0.9, 0.9],
        ],
        [
            [0.6, 0.2, 0.1],
            [0.9, 0.3, 0.6],
            [0.4, 0.4, 0.4],
            [1.0, 0.0, 0.0],
        ],
    ], dtype=np.float32)
```

Execute:

```bash
python imagem_zoom_base_aula.py
```

Selecione:

```text
1
```

A matriz agora aparece visualmente como uma pequena imagem formada por células coloridas.

---

# 5. Imagem = matriz

## 5.1 Conceito

Uma imagem digital pode ser interpretada como uma função:

```text
f(x, y) = cor
```

Em uma imagem RGB:

```text
f(x, y) = [R, G, B]
```

No NumPy, a mesma ideia aparece como:

```python
image[row, col]
```

Por exemplo:

```python
color = image[0, 0]
```

retorna a cor do pixel localizado na primeira linha e primeira coluna.

Se esse pixel for vermelho:

```text
color = [1.0, 0.0, 0.0]
```

---

# 6. Como a matriz aparece no OpenGL

A função:

```python
build_grid_vertices(...)
```

transforma a matriz da imagem em geometria que pode ser desenhada pelo OpenGL.

A lógica é:

```text
matriz
  ↓
percorrer linhas e colunas
  ↓
obter a cor de cada célula
  ↓
criar um quadrado para cada pixel
  ↓
dividir cada quadrado em dois triângulos
  ↓
enviar os vértices ao VBO
  ↓
renderizar
```

Dentro da função aparece:

```python
color = image[row, col]
```

Essa instrução recupera os três canais do pixel.

Depois:

```python
add_cell(
    vertices,
    x0,
    y0,
    x1,
    y1,
    color
)
```

cria a geometria correspondente.

## 6.1 Relação com o VBO

`VBO` significa **Vertex Buffer Object**.

Neste exemplo, cada vértice possui:

```text
x, y, r, g, b
```

Portanto:

```text
2 valores → posição
3 valores → cor
```

Cada pixel da matriz é transformado em um quadrado composto por dois triângulos.

Isso permite visualizar literalmente a relação:

```text
pixel da matriz
        ↓
quadrado colorido na tela
```

---

# 7. Canais RGB

## 7.1 Conceito

Uma imagem RGB possui três canais de informação:

```text
R
G
B
```

Podemos observar cada canal separadamente.

Por exemplo, se o pixel é:

```text
[0.8, 0.3, 0.1]
```

seus canais possuem:

```text
R = 0.8
G = 0.3
B = 0.1
```

Para visualizar apenas o canal vermelho, podemos zerar os outros:

```text
[0.8, 0.0, 0.0]
```

---

# 8. Implementando a separação dos canais

Localize:

```python
def only_channel(image, channel_index):
    # SEPARAR CANAL RGB AQUI
```

O parâmetro:

```text
channel_index
```

indica:

```text
0 → vermelho
1 → verde
2 → azul
```

Complete:

```python
def only_channel(image, channel_index):
    result = np.zeros_like(image)

    result[:, :, channel_index] = (
        image[:, :, channel_index]
    )

    return result
```

Execute novamente e pressione:

```text
2
```

A tela apresenta três versões da mesma imagem.

Observe:

```text
esquerda → canal vermelho
centro   → canal verde
direita  → canal azul
```

### Questão para análise

Considere um pixel branco:

```text
[1.0, 1.0, 1.0]
```

Separado em canais, ele produzirá:

```text
R → [1.0, 0.0, 0.0]
G → [0.0, 1.0, 0.0]
B → [0.0, 0.0, 1.0]
```

---

# 9. Zoom In

## 9.1 O problema

A imagem original possui um número fixo de pixels.

Se desejamos ampliá-la, precisamos criar uma matriz maior.

Por exemplo:

```text
2 × 2
```

pode se tornar:

```text
4 × 4
```

A questão é:

> Quais valores devem ser colocados nos novos pixels?

Nesta aula serão utilizadas duas estratégias:

```text
Zoom In quadrado
Zoom In linear
```

---

# 10. Zoom In quadrado

## 10.1 Conceito

No Zoom In quadrado, cada pixel é repetido.

Considere:

```text
A B
C D
```

Aplicando fator `2`:

```text
A A B B
A A B B
C C D D
C C D D
```

Não são criadas novas cores.

Cada cor original simplesmente passa a ocupar uma região maior.

Esse comportamento é semelhante ao que se observa quando uma imagem de baixa resolução é ampliada e os pixels ficam claramente visíveis.

---

# 11. Implementando o Zoom In quadrado

Localize:

```python
def zoom_in_quadrado(image, factor):
    # ZOOM IN QUADRADO AQUI
```

Complete:

```python
def zoom_in_quadrado(image, factor):
    zoomed = np.repeat(
        image,
        factor,
        axis=0
    )

    zoomed = np.repeat(
        zoomed,
        factor,
        axis=1
    )

    return zoomed
```

Primeiro são repetidas as linhas:

```python
axis=0
```

Depois são repetidas as colunas:

```python
axis=1
```

Execute e pressione:

```text
3
```

### Observe

A imagem ficou maior, porém os limites entre os pixels continuam bem definidos.

Esse efeito pode ser descrito como:

```text
pixelado
```

ou:

```text
blocada
```

---

# 12. Zoom In por interpolação

## 12.1 Problema

No método quadrado, apenas repetimos os valores existentes.

Para produzir uma ampliação mais suave, podemos criar valores intermediários.

Considere dois valores:

```text
A = 10
B = 20
```

Entre os dois podemos criar:

```text
15
```

Esse processo é chamado de **interpolação**.

---

# 13. Interpolação linear

Uma interpolação linear pode ser representada por:

```text
valor = (1 - t) × A + t × B
```

onde `t` varia entre:

```text
0.0 e 1.0
```

Quando:

```text
t = 0
```

temos:

```text
valor = A
```

Quando:

```text
t = 1
```

temos:

```text
valor = B
```

Quando:

```text
t = 0.5
```

temos um ponto exatamente no meio:

```text
valor = 0.5 × A + 0.5 × B
```

---

# 14. Interpolação em uma imagem

Em uma imagem existem duas direções:

```text
horizontal
vertical
```

Por isso, a implementação utilizada no exemplo considera quatro pixels vizinhos.

Para uma nova posição, são localizados:

```text
superior esquerdo
superior direito
inferior esquerdo
inferior direito
```

Primeiro ocorre a interpolação horizontal.

Depois ocorre a interpolação vertical.

Essa combinação é conhecida como **interpolação bilinear**.

---

# 15. Implementando o Zoom In linear

Localize:

```python
def zoom_in_linear(image, factor):
    # ZOOM IN LINEAR AQUI
```

A implementação pode ser construída em etapas.

## Etapa 1 — determinar o novo tamanho

```python
height, width, channels = image.shape

new_height = height * factor
new_width = width * factor
```

Crie a matriz de resultado:

```python
result = np.zeros(
    (new_height, new_width, channels),
    dtype=np.float32
)
```

---

## Etapa 2 — mapear o novo pixel para a imagem original

Para cada nova linha:

```python
source_y = new_row / factor
```

Para cada nova coluna:

```python
source_x = new_col / factor
```

Esses valores podem ser fracionários.

Exemplo:

```text
source_x = 1.5
```

significa que a nova posição está entre:

```text
coluna 1
coluna 2
```

---

## Etapa 3 — encontrar os vizinhos

```python
y0 = int(np.floor(source_y))

y1 = min(
    y0 + 1,
    height - 1
)

x0 = int(np.floor(source_x))

x1 = min(
    x0 + 1,
    width - 1
)
```

Calcule a parte fracionária:

```python
ty = source_y - y0
tx = source_x - x0
```

---

## Etapa 4 — interpolar horizontalmente

```python
top = (
    (1.0 - tx) * image[y0, x0]
    +
    tx * image[y0, x1]
)
```

```python
bottom = (
    (1.0 - tx) * image[y1, x0]
    +
    tx * image[y1, x1]
)
```

---

## Etapa 5 — interpolar verticalmente

```python
result[new_row, new_col] = (
    (1.0 - ty) * top
    +
    ty * bottom
)
```

Ao final:

```python
return result
```

Execute e pressione:

```text
4
```

Compare repetidamente:

```text
3 → Zoom In quadrado
4 → Zoom In linear
```

### Para analisar

- No modo quadrado, as cores originais são repetidas.
- No modo linear, aparecem cores que não estavam explicitamente na matriz original.
- Essas novas cores são calculadas a partir dos vizinhos.

---

# 16. Zoom Out

## 16.1 O problema

No Zoom Out, o objetivo é reduzir a matriz.

Por exemplo:

```text
4 × 4
```

pode se tornar:

```text
2 × 2
```

Agora ocorre o problema inverso:

> Como representar vários pixels originais utilizando apenas um pixel?

Serão utilizadas duas estratégias:

```text
Zoom Out quadrado
Zoom Out por média
```

---

# 17. Zoom Out quadrado

## 17.1 Conceito

Uma forma simples de reduzir uma imagem é selecionar apenas alguns pixels.

Por exemplo:

```text
A B C D
E F G H
I J K L
M N O P
```

Com fator 2, podemos selecionar:

```text
A C
I K
```

Os demais pixels são ignorados.

Essa abordagem é rápida, mas pode perder informação importante.

---

# 18. Implementando o Zoom Out quadrado

Localize:

```python
def zoom_out_quadrado(image, factor):
    # ZOOM OUT QUADRADO AQUI
```

Complete:

```python
def zoom_out_quadrado(image, factor):
    return image[
        ::factor,
        ::factor
    ]
```

O fatiamento:

```text
::factor
```

significa:

```text
selecionar um elemento
pular factor posições
selecionar o próximo
```

Execute e pressione:

```text
5
```

Observe quais cores permaneceram e quais desapareceram.

---

# 19. Zoom Out por média

## 19.1 Conceito

Em vez de ignorar os pixels vizinhos, podemos considerar sua influência.

Considere um bloco:

```text
A B
C D
```

O novo pixel pode ser calculado como:

```text
novo = média(A, B, C, D)
```

Para RGB, a média é realizada separadamente em cada canal.

Exemplo:

```text
A = [1, 0, 0]
B = [0, 1, 0]
C = [0, 0, 1]
D = [1, 1, 1]
```

O resultado é aproximadamente:

```text
[0.5, 0.5, 0.5]
```

---

# 20. Implementando o Zoom Out por média

Localize:

```python
def zoom_out_media(image, factor):
    # ZOOM OUT MEDIA AQUI
```

Comece recuperando as dimensões:

```python
height, width, channels = image.shape
```

Calcule o novo tamanho:

```python
new_height = max(
    1,
    height // factor
)

new_width = max(
    1,
    width // factor
)
```

Crie o resultado:

```python
result = np.zeros(
    (new_height, new_width, channels),
    dtype=np.float32
)
```

Percorra a nova matriz:

```python
for row in range(new_height):
    for col in range(new_width):
```

Selecione o bloco correspondente:

```python
block = image[
    row * factor:(row + 1) * factor,
    col * factor:(col + 1) * factor
]
```

Calcule a média:

```python
result[row, col] = block.mean(
    axis=(0, 1)
)
```

Ao final:

```python
return result
```

Execute e pressione:

```text
6
```

Compare:

```text
5 → Zoom Out quadrado
6 → Zoom Out por média
```

---

# 21. Comparação das quatro estratégias

| Operação | Estratégia | O que acontece |
|---|---|---|
| Zoom In | Quadrado | Repete pixels |
| Zoom In | Linear | Cria pixels intermediários |
| Zoom Out | Quadrado | Seleciona alguns pixels |
| Zoom Out | Média | Resume grupos de pixels pela média |

Uma forma de lembrar:

```text
Zoom In
→ precisamos criar pixels

Zoom Out
→ precisamos reduzir pixels
```

No Zoom In:

```text
repetição ou interpolação
```

No Zoom Out:

```text
amostragem ou combinação
```

---

# 22. Comparação visual no programa

Use as teclas em sequência:

```text
1 → original
3 → Zoom In quadrado
4 → Zoom In linear
1 → original
5 → Zoom Out quadrado
6 → Zoom Out por média
```

Para cada comparação, observe:

- tamanho da matriz;
- quantidade de pixels;
- cores criadas ou descartadas;
- suavidade;
- perda de informação.

---

# 23. Relação com o pipeline OpenGL

Neste exemplo, o OpenGL não realiza diretamente o cálculo do zoom.

As funções Python produzem uma nova matriz:

```text
imagem original
      ↓
algoritmo de zoom
      ↓
nova matriz
```

Depois essa matriz é transformada em vértices:

```text
nova matriz
    ↓
build_grid_vertices()
    ↓
VBO
    ↓
Vertex Shader
    ↓
Fragment Shader
    ↓
imagem na tela
```

Isso permite separar dois problemas:

```text
Processamento da imagem
        +
Renderização da imagem
```

---

# 24. O Vertex Shader

O Vertex Shader utilizado é simples:

```glsl
#version 330 core

layout(location = 0) in vec2 aPos;
layout(location = 1) in vec3 aColor;

out vec3 vertexColor;

void main()
{
    gl_Position =
        vec4(
            aPos,
            0.0,
            1.0
        );

    vertexColor = aColor;
}
```

Ele recebe:

```text
posição
cor
```

e envia a cor para o Fragment Shader.

Nesta aula, a principal transformação ocorre na matriz da imagem, antes da renderização.

---

# 25. O Fragment Shader

```glsl
#version 330 core

in vec3 vertexColor;

out vec4 FragColor;

void main()
{
    FragColor =
        vec4(
            vertexColor,
            1.0
        );
}
```

O Fragment Shader recebe a cor interpolada pelo pipeline e produz a cor final.

---

# 26. Revisão guiada

Ao final da implementação, tente responder sem consultar o código.

### Cores

1. O que representam R, G e B?
2. Qual a diferença entre `[1, 0, 0]` e `[0.5, 0, 0]`?
3. Como uma cor branca é representada?

### Imagem como matriz

4. O que significa `image[row, col]`?
5. Por que uma imagem RGB possui três valores por pixel?
6. O que representa `image.shape`?

### Zoom In

7. O que o Zoom In quadrado faz com cada pixel?
8. Por que o resultado fica pixelado?
9. O que é interpolação?
10. Por que a interpolação pode criar cores novas?

### Zoom Out

11. O que o Zoom Out quadrado descarta?
12. Como funciona o Zoom Out por média?
13. Por que a média pode preservar melhor a informação local?

### OpenGL

14. Como um pixel da matriz é transformado em algo desenhável pelo OpenGL?
15. Qual é o papel do VBO?
16. O zoom ocorre no shader ou antes de enviar a geometria nesta implementação?

---

# 27. Experimentos opcionais

Depois que o programa estiver funcionando, alguns experimentos podem ser realizados.

## Experimento 1 — alterar uma cor

Na matriz original, altere:

```python
[1.0, 0.0, 0.0]
```

para:

```python
[0.5, 0.0, 0.0]
```

Observe a diferença.

---

## Experimento 2 — fator de Zoom In

Altere:

```python
factor=2
```

para:

```python
factor=3
```

Compare o tamanho da matriz produzida.

---

## Experimento 3 — fator de Zoom Out

Teste um fator maior e observe a quantidade de informação perdida.

---

## Experimento 4 — imagem monocromática

Crie uma matriz em que todos os pixels tenham:

```text
R = G = B
```

Observe que a imagem passa a apresentar apenas tons de cinza.

---

## Experimento 5 — verificar dimensões

Adicione:

```python
print(original_image.shape)
print(zoomed_image.shape)
```

Compare as dimensões antes e depois das operações.

---

# 28. Síntese

A aula conecta três ideias principais:

```text
COR
↓
representação numérica
```

```text
IMAGEM
↓
matriz de pixels
```

```text
ZOOM
↓
transformação da matriz
```

A sequência completa é:

```text
cores
  ↓
pixels
  ↓
matriz
  ↓
algoritmo de Zoom
  ↓
nova matriz
  ↓
geometria OpenGL
  ↓
renderização
```

Esses conceitos servem como base para conteúdos posteriores, como:

- texturas;
- filtros;
- processamento digital de imagens;
- interpolação;
- amostragem;
- aliasing;
- mipmapping.
