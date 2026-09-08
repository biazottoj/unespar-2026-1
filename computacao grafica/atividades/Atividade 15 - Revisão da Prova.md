# Estudo Guiado de Revisão — Computação Gráfica

## Objetivo

A lista possui **30 exercícios de revisão**, distribuídos entre os três tópicos, além de **5 desafios integradores** ao final.

Nos exercícios práticos, considere como base os códigos utilizados durante as aulas, nos quais já existem:

- janela criada com GLFW;
- VAO (*Vertex Array Object*), responsável por armazenar a configuração dos atributos dos vértices;
- VBO (*Vertex Buffer Object*), responsável por armazenar os dados dos vértices na GPU;
- shaders;
- desenho dos objetos;
- laço principal;
- controles básicos pelo teclado.

---

# Parte I — Transformações 2D

## 1. Contextualização

Em Computação Gráfica, um objeto 2D pode ser representado por um conjunto de vértices. Um triângulo, um quadrado ou qualquer outra forma é, essencialmente, definido pelas posições de seus pontos.

Quando desejamos mover, redimensionar ou rotacionar um objeto, poderíamos calcular manualmente a nova posição de cada vértice. Porém, essa abordagem se torna pouco prática à medida que o objeto possui mais pontos ou quando várias transformações precisam ser combinadas.

Por isso, utilizamos **matrizes de transformação**.

Vamos utilizar a seguinte notação:

- `P` = ponto original;
- `P'` = ponto depois da transformação;
- `M` = matriz de transformação aplicada ao ponto.

Assim, a ideia geral é:

```text
P' = M × P
```

A matriz `M` pode representar uma única transformação, como uma translação, ou uma combinação de várias transformações.

Nos códigos desenvolvidos em aula, construímos essas matrizes em Python e utilizamos a multiplicação matricial para determinar como os vértices deveriam ser posicionados durante a renderização.

O mais importante é compreender que a geometria original pode permanecer a mesma enquanto a matriz determina **como o objeto será apresentado**.

---

## 2. Coordenadas homogêneas e matriz identidade

Um ponto bidimensional é normalmente representado por duas coordenadas:

```text
P = (x, y)
```

onde:

- `x` representa a posição horizontal;
- `y` representa a posição vertical.

Para que possamos representar translação, rotação e escala de maneira uniforme por meio de multiplicação matricial, adicionamos uma terceira coordenada e passamos a utilizar a representação homogênea:

```text
P = [x, y, 1]
```

Essa terceira coordenada é um recurso matemático que nos permite trabalhar com matrizes `3 × 3`.

A **matriz identidade**, que chamaremos de `I`, é:

```text
I = | 1  0  0 |
	 | 0  1  0 |
	 | 0  0  1 |
```

Aplicar a identidade não modifica o ponto:

```text
P' = I × P
```

Portanto:

```text
P' = P
```

A identidade também é útil como ponto inicial quando construímos uma transformação que será modificada ao longo da execução.

### Pontos importantes

- A terceira coordenada homogênea não transforma o objeto em 3D.
- Coordenadas homogêneas permitem representar a translação usando multiplicação matricial.
- A matriz identidade representa a ausência de transformação.
- Em 2D, utilizamos matrizes `3 × 3` para manter translação, escala e rotação no mesmo formato matemático.

---

## 3. Translação, escala e rotação

### Translação

A **translação** desloca um ponto sem alterar seu tamanho ou orientação.

Vamos definir:

- `tx` = deslocamento no eixo X;
- `ty` = deslocamento no eixo Y.

A matriz de translação, que chamaremos de `T`, é:

```text
T = | 1  0  tx |
	 | 0  1  ty |
	 | 0  0   1 |
```

Aplicando essa matriz ao ponto `(x, y)`, obtemos:

```text
x' = x + tx
y' = y + ty
```

Portanto, a translação altera a posição do objeto.

### Escala

A **escala** modifica o tamanho do objeto.

Vamos definir:

- `sx` = fator de escala no eixo X;
- `sy` = fator de escala no eixo Y.

A matriz de escala, chamada de `S`, é:

```text
S = | sx  0   0 |
	 | 0   sy  0 |
	 | 0   0   1 |
```

Se:

```text
sx = sy
```

a escala é **uniforme**, pois o objeto cresce ou diminui na mesma proporção em ambos os eixos.

Se os valores forem diferentes, a escala é **não uniforme** e pode alterar as proporções do objeto.

### Rotação

A **rotação** altera a orientação do objeto.

Vamos definir:

- `θ` = ângulo de rotação;
- `cos(θ)` = cosseno do ângulo;
- `sin(θ)` = seno do ângulo.

A matriz de rotação, chamada de `R`, é:

```text
R = | cos(θ)  -sin(θ)  0 |
	 | sin(θ)   cos(θ)  0 |
	 |   0        0     1 |
```

Essa matriz realiza a rotação em torno da origem `(0, 0)`.

Isso é importante porque, se desejarmos girar o objeto em torno de outro ponto, precisaremos primeiro reposicionar temporariamente esse ponto na origem.

---

## 4. Composição e pivô

Uma única matriz pode representar várias transformações combinadas.

Para facilitar a leitura, utilizaremos:

- `T` = matriz de translação;
- `R` = matriz de rotação;
- `S` = matriz de escala;
- `M` = matriz final, resultante da composição.

Por exemplo:

```text
M = T × R × S
```

Com a convenção de **vetores coluna** utilizada nas aulas, a transformação mais à direita é aplicada primeiro.

Assim:

```text
M = T × R × S
```

significa:

```text
1. Escala
2. Rotação
3. Translação
```

A ordem é importante porque, em geral:

```text
T × R ≠ R × T
```

Ou seja, transladar e depois rotacionar pode produzir um resultado diferente de rotacionar e depois transladar.

### Rotação em torno de um pivô

A rotação básica acontece em torno da origem. Para girar em torno de outro ponto, definimos:

- `C` = ponto usado como pivô;
- `T(-C)` = translação que leva o pivô até a origem;
- `R` = rotação desejada;
- `T(C)` = translação que devolve o pivô para sua posição original.

A composição é:

```text
M = T(C) × R × T(-C)
```

Como a transformação da direita acontece primeiro, a sequência efetiva é:

```text
1. T(-C) → levar o pivô para a origem
2. R     → realizar a rotação
3. T(C)  → voltar para a posição original
```

O ponto principal é entender que as translações são auxiliares: elas permitem utilizar uma rotação conhecida, feita em torno da origem, para produzir uma rotação em torno de qualquer ponto.

---

# Exercícios — Transformações 2D

## Exercício 1

Converta os pontos abaixo para coordenadas homogêneas:

a) `(2, 3)`  
b) `(-4, 1)`  
c) `(0, -5)`

Depois explique por que a coordenada adicional não significa que o objeto passou a ser tridimensional.

---

## Exercício 2

Considere o ponto:

```text
P = [2, 5, 1]
```

Aplique a matriz identidade:

```text
| 1  0  0 |
| 0  1  0 |
| 0  0  1 |
```

Determine o ponto resultante e explique o papel da matriz identidade.

---

## Exercício 3

Construa a matriz que translada um objeto:

```text
tx = 3
ty = -2
```

Depois aplique essa transformação ao ponto:

```text
P = (2, 4)
```

---

## Exercício 4

Construa uma matriz que:

- dobre a largura;
- reduza a altura pela metade.

Depois explique a diferença entre essa transformação e uma escala uniforme de fator `2`.

---

## Exercício 5

Considere uma rotação de `90°` em torno da origem.

Determine aproximadamente a nova posição do ponto:

```text
P = (1, 0)
```

Depois complete:

```python
def rotation_matrix(angle_degrees):
    angle = np.radians(angle_degrees)

    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        # COMPLETE
    ], dtype=np.float32)
```

---

## Exercício 6

Considere:

- `T` = matriz de translação;
- `R` = matriz de rotação;
- `S` = matriz de escala.

```python
model = T @ R @ S
```

Responda:

1. Qual transformação acontece primeiro?
2. Qual acontece por último?
3. Por que a expressão deve ser lida da direita para a esquerda?

---

## Exercício 7

Considere o ponto:

```text
P = (1, 0)
```

Compare estas duas sequências:

### Sequência A

```text
Escala S(2,2)
Translação T(3,0)
```

### Sequência B

```text
Translação T(3,0)
Escala S(2,2)
```

Calcule a posição final em cada caso e explique por que os resultados são diferentes.

---

## Exercício 8

Explique por que os códigos abaixo podem produzir resultados diferentes:

```python
model_a = translation @ rotation
```

```python
model_b = rotation @ translation
```

Depois proponha uma pequena modificação no código da aula para alternar entre os dois casos.

---

## Exercício 9

Considere um pivô:

```text
C = (2, 1)
```

Escreva a composição necessária para rotacionar um objeto em torno desse ponto.

Explique o papel de:

```text
T(-C)
R
T(C)
```

---

## Exercício 10

Complete o trecho abaixo para rotacionar em torno de um pivô:

```python
pivot_x = 0.4
pivot_y = 0.3

model = (
    # COMPLETE
)
```

Use:

```python
translation_matrix(...)
rotation_matrix(...)
```

Depois expliq

---

# Parte II — Transformações 3D

## 5. Contextualização

Em uma cena 3D, um ponto possui três coordenadas:

```text
P = (x, y, z)
```

onde:

- `x` representa a posição horizontal;
- `y` representa a posição vertical;
- `z` representa a profundidade.

Assim como em 2D, utilizamos coordenadas homogêneas para representar as transformações de maneira uniforme:

```text
P = [x, y, z, 1]
```

Agora utilizamos matrizes `4 × 4`.

A quarta coordenada não significa que estamos trabalhando com um objeto fisicamente 4D. Ela é novamente um recurso matemático para permitir que translação, escala e rotação sejam representadas no mesmo formato.

Nos códigos desenvolvidos em aula, utilizamos um cubo colorido e aplicamos as transformações por meio da matriz chamada `Model`, enviada ao Vertex Shader no uniform:

```glsl
uniform mat4 uModel;
```

A matriz `Model` descreve como o objeto sai de suas coordenadas locais e passa a ocupar determinada posição, orientação e tamanho na cena.

---

## 6. Identidade, translação e escala 3D

### Matriz identidade

Chamaremos a matriz identidade de `I`.

```text
I = | 1  0  0  0 |
	 | 0  1  0  0 |
	 | 0  0  1  0 |
	 | 0  0  0  1 |
```

Ela mantém o ponto inalterado.

### Translação

Vamos definir:

- `tx` = deslocamento no eixo X;
- `ty` = deslocamento no eixo Y;
- `tz` = deslocamento no eixo Z.

A matriz de translação, chamada de `T`, é:

```text
T = | 1  0  0  tx |
 	 | 0  1  0  ty |
	 | 0  0  1  tz |
	 | 0  0  0   1 |
```

A translação modifica a posição do objeto sem alterar sua forma.

### Escala

Vamos definir:

- `sx` = fator de escala em X;
- `sy` = fator de escala em Y;
- `sz` = fator de escala em Z.

A matriz de escala, chamada de `S`, é:

```text
S = | sx  0   0   0 |
    | 0   sy  0   0 |
    | 0   0   sz  0 |
    | 0   0   0   1 |
```

Com essa matriz podemos alterar largura, altura e profundidade de forma independente.

---

## 7. Rotações em X, Y e Z

Em 3D, uma rotação precisa indicar **em torno de qual eixo** ela acontece.

Vamos utilizar:

- `θ` = ângulo de rotação;
- `Rx` = matriz de rotação em torno do eixo X;
- `Ry` = matriz de rotação em torno do eixo Y;
- `Rz` = matriz de rotação em torno do eixo Z.

Uma maneira útil de compreender cada matriz é observar qual eixo permanece inalterado.

### Rotação em torno do eixo X

Na rotação `Rx`, a coordenada X permanece preservada. As coordenadas Y e Z são combinadas.

```text
Rx =

| 1    0        0      0 |
| 0   cos(θ)  -sin(θ)  0 |
| 0   sin(θ)   cos(θ)  0 |
| 0    0        0      1 |
```

### Rotação em torno do eixo Y

Na rotação `Ry`, a coordenada Y permanece preservada. As coordenadas X e Z são combinadas.

```text
Ry = | cos(θ)   0   sin(θ)   0 |
     |   0      1     0      0 |
     | -sin(θ)  0   cos(θ)   0 |
     |   0      0     0      1 |
```

### Rotação em torno do eixo Z

Na rotação `Rz`, a coordenada Z permanece preservada. As coordenadas X e Y são combinadas.

```text
Rz = | cos(θ)  -sin(θ)   0   0 |
     | sin(θ)   cos(θ)   0   0 |
     |   0        0      1   0 |
     |   0        0      0   1 |
```

A rotação em Z é especialmente familiar porque, no plano XY, ela possui a mesma estrutura da rotação 2D.

Resumo:

| Rotação | Significado | Eixo preservado | Coordenadas modificadas |
|---|---|---|---|
| `Rx` | rotação em torno de X | X | Y e Z |
| `Ry` | rotação em torno de Y | Y | X e Z |
| `Rz` | rotação em torno de Z | Z | X e Y |

---

## 8. Matriz Model

A matriz `Model` reúne as transformações aplicadas ao objeto.

Vamos utilizar:

- `T` = matriz de translação;
- `Rx` = rotação em torno de X;
- `Ry` = rotação em torno de Y;
- `Rz` = rotação em torno de Z;
- `S` = matriz de escala.

No código da aula:

```python
model = (
    T
    @ Rz
    @ Ry
    @ Rx
    @ S
)
```

Com vetores coluna, a ordem efetiva é:

```text
1. Escala
2. Rotação em X
3. Rotação em Y
4. Rotação em Z
5. Translação
```

A matriz `Model` é então enviada ao Vertex Shader:

```glsl
uniform mat4 uModel;
```

e aplicada aos vértices.

Isso permite que os dados originais armazenados no VBO (*Vertex Buffer Object*) permaneçam inalterados. O mesmo conjunto de vértices pode ser desenhado em posições, escalas ou orientações diferentes simplesmente alterando a matriz `Model`.

---

## 9. Rotação em torno de um ponto ou eixo

### Rotação em torno de um ponto

Definimos:

- `C` = ponto usado como pivô;
- `T(-C)` = translação que leva o pivô à origem;
- `R` = matriz da rotação desejada;
- `T(C)` = translação que devolve o pivô à posição original.

Assim:

```text
M = T(C) × R × T(-C)
```

onde `M` representa a matriz final da transformação.

### Rotação em torno de um eixo arbitrário

Quando o eixo desejado não coincide com X, Y ou Z, podemos transformá-lo temporariamente até que ele coincida com um eixo conhecido.

Vamos definir:

- `C` = ponto de referência do eixo;
- `α` = ângulo usado no alinhamento em torno de X;
- `β` = ângulo usado no alinhamento em torno de Y;
- `θ` = ângulo da rotação que realmente desejamos realizar;
- `Rx(α)` = rotação de alinhamento em torno de X;
- `Ry(β)` = rotação de alinhamento em torno de Y;
- `Rz(θ)` = rotação desejada, depois que o eixo foi alinhado com Z.

A sequência estudada foi:

```text
1. T(-C)      → levar o eixo para passar pela origem
2. Rx(α)      → realizar parte do alinhamento
3. Ry(β)      → terminar o alinhamento com o eixo Z
4. Rz(θ)      → executar a rotação desejada
5. Ry(-β)     → desfazer o alinhamento em Y
6. Rx(-α)     → desfazer o alinhamento em X
7. T(C)       → voltar à posição original
```

A composição completa é:

```text
M =
T(C)
× Rx(-α)
× Ry(-β)
× Rz(θ)
× Ry(β)
× Rx(α)
× T(-C)
```

O ponto principal não é apenas memorizar a expressão. A estratégia é:

> levar o problema para uma situação conhecida, realizar a transformação e depois desfazer as transformações auxiliares.

---

# Exercícios — Transformações 3D

## Exercício 11

Converta os pontos abaixo para coordenadas homogêneas:

a) `(2, 3, 4)`  
b) `(-1, 0, 5)`  
c) `(0, 0, 0)`

Depois explique por que usamos matrizes `4 × 4` em transformações 3D.

---

## Exercício 12

Construa uma matriz que translade um objeto:

```text
tx = 2
ty = -1
tz = -4
```

Depois aplique-a ao ponto:

```text
P = (1, 2, 3)
```

---

## Exercício 13

Considere:

```python
model = scale_matrix(
    1.0,
    2.0,
    0.5
)
```

Explique o que acontecerá com:

- largura;
- altura;
- profundidade;

de um cubo.

---

## Exercício 14

Para cada rotação, indique:

1. qual eixo permanece preservado;
2. quais duas coordenadas são combinadas.

Analise:

```text
Rx
Ry
Rz
```

---

## Exercício 15

Considere:

```text
P = (1, 0, 0)
```

Aplique uma rotação de `90°` em torno do eixo Z.

Depois explique a relação entre `Rz` e a matriz de rotação 2D.

---

## Exercício 16

Complete:

```python
def rotation_y_matrix(angle_degrees):
    angle = np.radians(angle_degrees)

    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        # COMPLETE
    ], dtype=np.float32)
```

Depois explique por que Y permanece inalterado.

---

## Exercício 17

Considere:

- `T` = matriz de translação;
- `Rx` = rotação em torno de X;
- `Ry` = rotação em torno de Y;
- `Rz` = rotação em torno de Z;
- `S` = matriz de escala.

```python
model = T @ Rz @ Ry @ Rx @ S
```

Responda:

1. Qual operação acontece primeiro?
2. Qual acontece por último?
3. Qual é o papel dessa matriz no pipeline?
4. O que mudaria visualmente se a translação fosse aplicada antes das rotações?

---

## Exercício 18

Complete o envio da matriz `model` ao shader:

```python
glUniformMatrix4fv(
    ___________,
    1,
    GL_TRUE,
    ___________
)
```

Depois explique:

1. o que `glGetUniformLocation` faz;
2. por que os vértices originais do VBO não precisam ser modificados.

---

## Exercício 19

Considere:

- `C` = ponto de referência do eixo;
- `α` = ângulo de alinhamento em torno de X;
- `β` = ângulo de alinhamento em torno de Y;
- `θ` = ângulo da rotação desejada.

A rotação em torno de um eixo arbitrário é:

```text
T(C) × Rx(-α) × Ry(-β) × Rz(θ) × Ry(β) × Rx(α) × T(-C)
```

Explique a função de cada grupo:

1. `T(-C)`
2. `Rx(α)` e `Ry(β)`
3. `Rz(θ)`
4. `Ry(-β)` e `Rx(-α)`
5. `T(C)`

---

## Exercício 20

Utilizando o mesmo VAO/VBO do cubo, modifique o código para desenhar três cubos.

Cada cubo deve possuir uma matriz `Model` diferente:

- um à esquerda;
- um no centro;
- um à direita.

Use pelo menos duas transformações diferentes em cada objeto.

Explique por que não é necessário criar três VBOs.

---

# Parte III — Projeções

## 10. Contextualização

Depois de transformar e posicionar um objeto 3D, ainda existe um problema fundamental:

```text
a cena possui três dimensões,
mas a tela possui duas.
```

Precisamos, portanto, determinar como os pontos tridimensionais serão representados em uma superfície bidimensional.

Esse processo é chamado de **projeção**.

No walkthrough de aula, partimos do mesmo cubo usado nas transformações 3D e adicionamos novas etapas ao pipeline:

- plano de projeção;
- centro de projeção;
- projetores;
- matriz `View`;
- projeção paralela;
- projeção em perspectiva;
- uniform `uView`;
- uniform `uProjection`.

A ideia é separar três perguntas:

```text
Model      → Onde está o objeto e como ele foi transformado?
View       → Como a cena fica em relação ao observador?
Projection → Como o espaço 3D será representado na tela 2D?
```

---

## 11. Plano de projeção, centro de projeção e projetores

### Plano de projeção

O **plano de projeção** é uma superfície 2D sobre a qual os pontos da cena são projetados.

Didaticamente, podemos imaginá-lo como uma:

> **tela virtual** posicionada entre o observador e a cena.

Ele não precisa ser entendido como a tela física do monitor. É uma construção geométrica utilizada para determinar onde os pontos 3D aparecerão na imagem.

### Centro de projeção

Vamos representar o centro de projeção por:

```text
C = (cx, cy, cz)
```

onde:

- `C` = centro de projeção;
- `cx` = posição do observador em X;
- `cy` = posição do observador em Y;
- `cz` = posição do observador em Z.

Na projeção em perspectiva, esse ponto representa a posição do observador.

### Projetores

Os **projetores** são as retas utilizadas para relacionar os pontos 3D da cena com o plano de projeção.

Na projeção paralela:

```text
os projetores são paralelos entre si
```

Na projeção em perspectiva:

```text
os projetores passam pelo centro de projeção
```

Essa diferença geométrica é responsável por uma das diferenças visuais mais importantes entre os dois tipos de projeção.

---

## 12. Projeção paralela

Na projeção paralela, a distância do objeto até o observador não provoca a redução de seu tamanho aparente.

Na forma ortográfica mais simples:

```text
(X, Y, Z) → (X, Y)
```

onde:

- `X`, `Y` e `Z` são as coordenadas do ponto no espaço 3D;
- as coordenadas X e Y determinam a posição projetada;
- Z continua sendo útil para representar profundidade, mas não é usado para diminuir X e Y.

Para construir uma matriz ortográfica completa, precisamos definir os limites do volume visível:

- `left` = limite esquerdo;
- `right` = limite direito;
- `bottom` = limite inferior;
- `top` = limite superior;
- `near` = plano de profundidade mais próximo considerado;
- `far` = plano de profundidade mais distante considerado.

Usando nomes descritivos, a matriz pode ser escrita como:

```text
| 2/(right-left)       0                  0          -(right+left)/(right-left) |
|       0         2/(top-bottom)          0          -(top+bottom)/(top-bottom) |
|       0              0            -2/(far-near)   -(far+near)/(far-near)     |
|       0              0                  0                     1               |
```

Observe a última linha:

```text
[0, 0, 0, 1]
```

Ela mantém a coordenada homogênea final como:

```text
w' = 1
```

Por isso, X e Y não serão divididos pela profundidade para criar o efeito de perspectiva.

---

## 13. Matriz View e centro de projeção

A matriz `View` representa a cena em relação ao observador.

Vamos definir novamente:

```text
C = (cx, cy, cz)
```

onde `C` é a posição do centro de projeção.

Para simplificar os cálculos, queremos trabalhar como se o observador estivesse na origem:

```text
(0, 0, 0)
```

Por isso aplicamos uma translação no sentido oposto:

```text
View = T(-C)
```

Aqui:

- `View` = matriz de visualização;
- `T(-C)` = matriz de translação por `(-cx, -cy, -cz)`.

Em outras palavras:

```text
View = T(-cx, -cy, -cz)
```

Exemplo:

```python
center_of_projection = np.array([
    0.0,
    0.0,
    3.0
])

view = translation_matrix(
    -center_of_projection[0],
    -center_of_projection[1],
    -center_of_projection[2]
)
```

Se o observador está em:

```text
C = (0, 0, 3)
```

a cena é transladada por:

```text
(0, 0, -3)
```

É importante distinguir:

```text
Model → transforma o objeto no mundo
View  → transforma o mundo para o referencial do observador
```

A `View` não realiza a projeção. Ela prepara as coordenadas para que a projeção seja aplicada em relação a um observador colocado na origem.

---

## 14. Projeção em perspectiva

Na projeção em perspectiva, objetos mais distantes aparecem menores.

Depois de aplicar a matriz `View`, consideramos que o observador está na origem.

Vamos definir:

- `P = (X, Y, Z)` = ponto 3D no espaço do observador;
- `d` = distância entre o observador e o plano de projeção;
- `xp` = coordenada X do ponto projetado;
- `yp` = coordenada Y do ponto projetado.

Considerando o plano de projeção em:

```text
z = -d
```

obtemos:

```text
xp = -(d × X) / Z
yp = -(d × Y) / Z
```

A característica mais importante é que `Z` aparece no denominador.

Isso significa que, mantendo X e Y iguais:

```text
|Z| maior → ponto mais distante → valores projetados menores
```

Portanto:

```text
mais distante → menor na tela
```

Essa é a base matemática do efeito de profundidade da projeção em perspectiva.

---

## 15. Coordenada homogênea w, campo de visão, near e far

### Coordenada w e divisão de perspectiva

Na projeção em perspectiva, as coordenadas homogêneas ganham uma função adicional.

Uma forma comum da matriz de perspectiva é:

```text
| f/aspect   0      0       0 |
|    0       f      0       0 |
|    0       0   depthA  depthB |
|    0       0     -1       0 |
```

onde:

- `f` = fator relacionado ao campo de visão;
- `aspect` = razão entre largura e altura da janela;
- `depthA` e `depthB` = valores calculados a partir de `near` e `far` para mapear a profundidade;
- `near` = limite próximo do volume de visualização;
- `far` = limite distante do volume de visualização.

A última linha faz com que:

```text
w' = -Z
```

Após o Vertex Shader, o OpenGL realiza automaticamente a divisão de perspectiva.

Vamos definir:

- `x_clip` e `y_clip` = coordenadas antes da divisão;
- `w_clip` = coordenada homogênea usada na divisão;
- `x_ndc` e `y_ndc` = coordenadas normalizadas após a divisão.

`NDC` significa *Normalized Device Coordinates*, ou **coordenadas normalizadas do dispositivo**.

A divisão é:

```text
x_ndc = x_clip / w_clip
y_ndc = y_clip / w_clip
```

Como:

```text
w_clip = -Z
```

a profundidade passa a influenciar X e Y.

### Campo de visão

`FOV` significa *Field of View*, ou **campo de visão**.

Vamos utilizar:

- `FOV` = ângulo do campo de visão;
- `f` = fator de escala derivado desse ângulo.

A relação é:

```text
f = 1 / tan(FOV / 2)
```

Em geral:

```text
FOV menor → visão mais fechada, com aparência de aproximação
FOV maior → visão mais aberta, mostrando uma região maior
```

Alterar o FOV não modifica a geometria do objeto. Ele modifica apenas a forma como a cena é projetada.

### near e far

Os parâmetros:

```text
near
far
```

definem os limites de profundidade do volume de visualização.

- `near` indica a distância do plano próximo;
- `far` indica a distância do plano distante.

Eles ajudam a determinar quais pontos estão dentro da região de visualização e como a profundidade será mapeada pelo OpenGL.

---

## 16. Model, View e Projection

No pipeline utilizado em aula, cada vértice passa por três transformações principais.

Vamos definir:

- `Model` = matriz que posiciona, orienta e escala o objeto;
- `View` = matriz que representa a cena em relação ao observador;
- `Projection` = matriz que define como o espaço 3D será projetado.

No Vertex Shader:

```glsl
gl_Position =
    uProjection *
    uView *
    uModel *
    vec4(aPos, 1.0);
```

Como utilizamos vetores coluna, a ordem efetiva é:

```text
1. Model
2. View
3. Projection
```

Podemos representar o fluxo como:

```text
Vértice local
   ↓
Model
   ↓
Coordenada no mundo
   ↓
View
   ↓
Coordenada em relação ao observador
   ↓
Projection
   ↓
Coordenada de projeção
```

Uma associação útil é:

```text
Model      → objeto
View       → observador
Projection → forma de projetar a cena
```

O ponto principal é perceber que as três matrizes têm responsabilidades diferentes. Uma transformação `Model` não deve ser usada para substituir a `View`, e a `View` não deve ser confundida com a `Projection`.

---

# Exercícios — Projeções

## Exercício 21

Defina com suas palavras:

1. plano de projeção;
2. centro de projeção;
3. projetores.

Depois explique a diferença entre projetores paralelos e projetores em perspectiva.

---

## Exercício 22

Dois cubos idênticos estão em:

```text
Cubo A → z = -2
Cubo B → z = -8
```

Explique como seus tamanhos aparentes devem se comportar:

1. na projeção paralela;
2. na projeção em perspectiva.

---

## Exercício 23

Considere a última linha de uma matriz ortográfica:

```text
[0, 0, 0, 1]
```

e a última linha da matriz de perspectiva:

```text
[0, 0, -1, 0]
```

Explique a principal diferença entre os valores de `w'` produzidos e por que isso é importante.

---

## Exercício 24

Se o centro de projeção é:

```text
C = (2, 1, 5)
```

responda:

1. qual translação deve ser utilizada na View;
2. por que usamos `T(-C)`;
3. qual é o papel da View antes da projeção.

---

## Exercício 25

Considere:

- `d` = distância até o plano de projeção;
- `X`, `Y` e `Z` = coordenadas do ponto 3D;
- `xp` e `yp` = coordenadas projetadas.

```text
d = 1
P1 = (2, 2, -2)
P2 = (2, 2, -4)
```

Use:

```text
xp = -(d × X) / Z
yp = -(d × Y) / Z
```

Calcule a projeção dos dois pontos e explique por que um deles aparece mais próximo do centro da imagem.

---

## Exercício 26

Complete a parte principal da função:

```python
def perspective_projection_matrix(
    fov_degrees,
    aspect,
    near,
    far
):
    f = (
        1.0 /
        np.tan(
            # COMPLETE
        )
    )
```

Depois explique o significado de `FOV` (*Field of View*, ou campo de visão).

---

## Exercício 27

Compare:

```text
FOV = 30°
FOV = 60°
FOV = 100°
```

Responda:

1. qual oferece uma visão mais fechada;
2. qual mostra uma região maior;
3. se o tamanho real do cubo é alterado;
4. qual parte do pipeline está sendo modificada.

---

## Exercício 28

Explique o papel de:

```text
near
far
```

na projeção em perspectiva.

Depois discuta por que um objeto fora dessa faixa pode não aparecer corretamente.

---

## Exercício 29

Complete o Vertex Shader:

```glsl
uniform mat4 uModel;
uniform mat4 __________;
uniform mat4 __________;

void main()
{
    gl_Position =
        __________ *
        __________ *
        __________ *
        vec4(aPos, 1.0);
}
```

Depois explique a ordem das três matrizes.

---

## Exercício 30

Modifique o código do cubo para desenhar três cubos em profundidades diferentes.

O programa deve permitir:

```text
1 → projeção paralela
2 → projeção em perspectiva
```

Os três cubos devem reutilizar o mesmo VAO/VBO.

Depois responda:

1. o que muda visualmente entre as projeções;
2. qual matriz é responsável pela diferença;
3. por que os objetos podem aparecer com tamanhos diferentes mesmo usando o mesmo VBO;
4. se a geometria original foi alterada.

---

# Parte IV — Desafios Integradores

## Desafio 1 — Ordem das transformações e perspectiva

Considere:

- `T` = matriz de translação;
- `Ry` = matriz de rotação em torno do eixo Y;
- `S` = matriz de escala.

```python
model_a = T @ Ry @ S
```

e:

```python
model_b = Ry @ T @ S
```

Desenhe o mesmo cubo utilizando as duas matrizes.

Faça o teste primeiro em projeção paralela e depois em perspectiva.

Explique:

1. Por que os objetos aparecem em posições diferentes?
2. A projeção modifica a ordem das operações de `Model`?
3. Por que a perspectiva pode tornar a diferença visual ainda mais evidente?

---

## Desafio 2 — Cubo orbitando em torno de um ponto

Escolha um ponto que será usado como pivô:

```text
C = (1, 0, 0)
```

Considere:

- `C` = ponto de pivô;
- `T(-C)` = translação que leva o pivô à origem;
- `Ry(θ)` = rotação de ângulo `θ` em torno do eixo Y;
- `T(C)` = translação que devolve o pivô à posição original;
- `M` = matriz final.

Faça o cubo rotacionar em torno desse ponto utilizando:

```text
M = T(C) × Ry(θ) × T(-C)
```

Depois aplique a projeção em perspectiva.

Analise:

1. O cubo está rotacionando em torno do próprio centro ou orbitando?
2. Qual é o papel das duas translações?
3. Em quais posições da órbita o cubo parece maior?
4. Por que seu tamanho aparente muda ao longo do movimento?
