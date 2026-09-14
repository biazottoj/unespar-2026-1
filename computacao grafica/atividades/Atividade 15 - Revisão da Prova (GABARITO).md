# Gabarito — Estudo Guiado de Revisão de Computação Gráfica

> Este gabarito corresponde aos 30 exercícios e aos 5 desafios integradores do estudo guiado.

---

# Transformações 2D

## Exercício 1

a)

```text
(2, 3) → [2, 3, 1]
```

b)

```text
(-4, 1) → [-4, 1, 1]
```

c)

```text
(0, -5) → [0, -5, 1]
```

A terceira coordenada é uma coordenada homogênea usada para permitir que transformações como translação sejam representadas por multiplicação matricial. O objeto continua sendo 2D.

---

## Exercício 2

Aplicando a identidade:

```text
| 1  0  0 |   | 2 |   | 2 |
| 0  1  0 | × | 5 | = | 5 |
| 0  0  1 |   | 1 |   | 1 |
```

Resultado:

```text
[2, 5, 1]
```

A matriz identidade mantém o ponto inalterado.

---

## Exercício 3

Matriz:

```text
| 1  0   3 |
| 0  1  -2 |
| 0  0   1 |
```

Aplicando ao ponto `(2, 4)`:

```text
x' = 2 + 3 = 5
y' = 4 - 2 = 2
```

Resultado:

```text
(5, 2)
```

---

## Exercício 4

Matriz:

```text
| 2    0   0 |
| 0   0.5  0 |
| 0    0   1 |
```

A largura dobra e a altura é reduzida pela metade.

Em uma escala uniforme de fator `2`:

```text
sx = 2
sy = 2
```

largura e altura aumentam na mesma proporção.

---

## Exercício 5

Para `90°`:

```text
cos(90°) ≈ 0
sin(90°) ≈ 1
```

O ponto:

```text
(1, 0)
```

vai aproximadamente para:

```text
(0, 1)
```

Função:

```python
def rotation_matrix(angle_degrees):
    angle = np.radians(angle_degrees)

    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [c, -s, 0.0],
        [s,  c, 0.0],
        [0.0, 0.0, 1.0]
    ], dtype=np.float32)
```

---

## Exercício 6

Para:

```python
model = T @ R @ S
```

a ordem efetiva é:

```text
1. S
2. R
3. T
```

A matriz mais à direita é aplicada primeiro ao vetor coluna.

---

## Exercício 7

### Sequência A

Escala primeiro:

```text
(1, 0) → (2, 0)
```

Depois translação:

```text
(2, 0) → (5, 0)
```

Resultado:

```text
(5, 0)
```

### Sequência B

Translação primeiro:

```text
(1, 0) → (4, 0)
```

Depois escala:

```text
(4, 0) → (8, 0)
```

Resultado:

```text
(8, 0)
```

As transformações não são comutativas.

---

## Exercício 8

```python
translation @ rotation
```

aplica primeiro a rotação e depois a translação.

```python
rotation @ translation
```

aplica primeiro a translação e depois a rotação.

Uma forma de comparar é usar uma variável booleana ou uma tecla para escolher:

```python
if mode == 1:
    model = T @ R
else:
    model = R @ T
```

---

## Exercício 9

A composição correta é:

```text
M = T(C) × R × T(-C)
```

Para:

```text
C = (2, 1)
```

primeiro:

```text
T(-C) = T(-2, -1)
```

depois aplica-se `R`.

Por fim:

```text
T(C) = T(2, 1)
```

A primeira translação leva o pivô à origem, e a última restaura sua posição.

---

## Exercício 10

Exemplo:

```python
model = (
    translation_matrix(
        pivot_x,
        pivot_y
    )
    @ rotation_matrix(angle)
    @ translation_matrix(
        -pivot_x,
        -pivot_y
    )
)
```

Se `T(C)` for omitida, o objeto permanecerá no sistema transladado e não retornará à posição original do pivô.

---

# Transformações 3D

## Exercício 11

a)

```text
(2, 3, 4) → [2, 3, 4, 1]
```

b)

```text
(-1, 0, 5) → [-1, 0, 5, 1]
```

c)

```text
(0, 0, 0) → [0, 0, 0, 1]
```

Matrizes `4 × 4` permitem representar uniformemente translação, escala e rotação em 3D usando coordenadas homogêneas.

---

## Exercício 12

Matriz:

```text
| 1  0  0   2 |
| 0  1  0  -1 |
| 0  0  1  -4 |
| 0  0  0   1 |
```

Aplicando ao ponto `(1, 2, 3)`:

```text
x' = 3
y' = 1
z' = -1
```

Resultado:

```text
(3, 1, -1)
```

---

## Exercício 13

```python
scale_matrix(
    1.0,
    2.0,
    0.5
)
```

produz:

```text
X → não muda
Y → dobra
Z → reduz à metade
```

Em um cubo:

- largura permanece;
- altura dobra;
- profundidade é reduzida à metade.

---

## Exercício 14

```text
Rx → preserva X; modifica Y e Z
Ry → preserva Y; modifica X e Z
Rz → preserva Z; modifica X e Y
```

---

## Exercício 15

Para uma rotação de `90°` em Z:

```text
(1, 0, 0) → aproximadamente (0, 1, 0)
```

`Rz` possui, no bloco X/Y, a mesma estrutura da matriz de rotação 2D.

---

## Exercício 16

```python
def rotation_y_matrix(angle_degrees):
    angle = np.radians(angle_degrees)

    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [c, 0.0, s, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [-s, 0.0, c, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)
```

Y permanece inalterado porque a segunda linha mantém diretamente o valor original de Y.

---

## Exercício 17

Para:

```python
model = T @ Rz @ Ry @ Rx @ S
```

a ordem é:

```text
1. S
2. Rx
3. Ry
4. Rz
5. T
```

A matriz `Model` posiciona, orienta e escala o objeto na cena.

Se a translação for aplicada antes de uma rotação, o vetor de deslocamento também pode ser afetado pela rotação, alterando a trajetória/posição final.

---

## Exercício 18

```python
glUniformMatrix4fv(
    model_location,
    1,
    GL_TRUE,
    model
)
```

`glGetUniformLocation` recupera a localização do uniform dentro do programa shader.

Os vértices originais do VBO não precisam ser alterados porque a matriz é aplicada pelo Vertex Shader durante a renderização.

---

## Exercício 19

1. `T(-C)` leva o eixo/ponto de referência para a origem.
2. `Rx(α)` e `Ry(β)` alinham o eixo arbitrário com um eixo conhecido.
3. `Rz(θ)` executa a rotação desejada.
4. `Ry(-β)` e `Rx(-α)` desfazem o alinhamento.
5. `T(C)` devolve o sistema à posição original.

---

## Exercício 20

Exemplo conceitual:

```python
models = [
    translation_matrix(-1.0, 0.0, 0.0)
        @ rotation_y_matrix(20.0),

    translation_matrix(0.0, 0.0, 0.0)
        @ scale_matrix(0.7, 0.7, 0.7),

    translation_matrix(1.0, 0.0, 0.0)
        @ rotation_x_matrix(30.0)
]

for model in models:
    glUniformMatrix4fv(
        model_location,
        1,
        GL_TRUE,
        model
    )

    draw_cube()
```

Não é necessário criar três VBOs porque a geometria é a mesma. O que muda é a matriz `Model` usada em cada chamada de desenho.

---

# Projeções

## Exercício 21

### Plano de projeção

É a superfície 2D, ou “tela virtual”, onde a imagem é formada.

### Centro de projeção

É o ponto associado à posição do observador na perspectiva.

### Projetores

São retas que relacionam os pontos 3D ao plano de projeção.

Na projeção paralela, os projetores são paralelos.

Na perspectiva, os projetores passam pelo centro de projeção.

---

## Exercício 22

### Projeção paralela

Os dois cubos tendem a manter o mesmo tamanho projetado, mesmo estando em profundidades diferentes.

### Perspectiva

O cubo mais distante tende a aparecer menor.

---

## Exercício 23

Na ortográfica:

```text
w' = 1
```

Na perspectiva:

```text
w' = -Z
```

Na perspectiva, a divisão posterior por `w` faz X e Y dependerem da profundidade.

Esse é o mecanismo que produz o efeito de “mais distante = menor”.

---

## Exercício 24

Para:

```text
C = (2, 1, 5)
```

a View deve usar:

```text
T(-2, -1, -5)
```

Usamos `T(-C)` porque queremos expressar a cena como se o observador estivesse na origem.

A View transforma coordenadas do mundo para coordenadas relativas ao observador.

---

## Exercício 25

Para:

```text
d = 1
P1 = (2, 2, -2)
```

temos:

```text
xp = -(1 × 2) / -2 = 1
yp = -(1 × 2) / -2 = 1
```

Resultado:

```text
P1' = (1, 1)
```

Para:

```text
P2 = (2, 2, -4)
```

temos:

```text
xp = -(1 × 2) / -4 = 0.5
yp = -(1 × 2) / -4 = 0.5
```

Resultado:

```text
P2' = (0.5, 0.5)
```

O segundo ponto está mais distante e aparece mais próximo do centro da projeção.

---

## Exercício 26

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
            np.radians(
                fov_degrees
            ) / 2.0
        )
    )
```

FOV é o campo de visão da projeção.

Ele controla quão aberta ou fechada é a região visualizada.

---

## Exercício 27

```text
FOV = 30° → visão mais fechada
FOV = 60° → intermediária
FOV = 100° → visão mais aberta
```

O FOV maior mostra uma região maior.

O tamanho real do cubo não muda.

O que muda é a matriz `Projection`.

---

## Exercício 28

`near` e `far` definem os limites de profundidade considerados pela projeção.

Objetos fora dessa região podem ser recortados ou não aparecer.

Eles também participam do mapeamento da profundidade para o intervalo utilizado pelo OpenGL.

---

## Exercício 29

```glsl
uniform mat4 uModel;
uniform mat4 uView;
uniform mat4 uProjection;

void main()
{
    gl_Position =
        uProjection *
        uView *
        uModel *
        vec4(aPos, 1.0);
}
```

A ordem efetiva é:

```text
1. Model
2. View
3. Projection
```

---

## Exercício 30

Solução conceitual:

1. desenhar o mesmo VAO/VBO três vezes;
2. alterar apenas `uModel` entre as chamadas;
3. manter `uView`;
4. alternar `uProjection`.

Na paralela, a profundidade não reduz o tamanho dos cubos.

Na perspectiva, os cubos mais distantes aparecem menores.

A diferença é introduzida pela matriz `Projection`.

A geometria original permanece no VBO sem alteração.

---

# Gabarito dos Desafios Integradores

## Desafio 1 — Dois cubos, duas profundidades

Na projeção paralela, os cubos tendem a manter o mesmo tamanho aparente.

Na perspectiva, o cubo mais distante aparece menor.

A diferença vem da matriz `Projection`.

O VBO não precisa ser alterado, pois a geometria é a mesma.

---

## Desafio 2 — Ordem das transformações e perspectiva

```python
T @ Ry @ S
```

aplica:

```text
S → Ry → T
```

Já:

```python
Ry @ T @ S
```

aplica:

```text
S → T → Ry
```

A translação também pode ser afetada pela rotação no segundo caso, modificando a posição final.

A projeção não altera a ordem interna de `Model`.

A perspectiva pode tornar a diferença mais evidente porque mudanças em Z também afetam o tamanho aparente.

---

## Desafio 3 — Cubo orbitando em torno de um ponto

Com:

```text
M = T(C) × Ry(θ) × T(-C)
```

o cubo gira em torno do ponto `C`, produzindo uma órbita em relação a esse pivô.

As translações servem para levar o pivô à origem e depois devolvê-lo.

Na perspectiva, o cubo parece maior quando sua posição está mais próxima do observador e menor quando está mais distante.

---

## Desafio 4 — Alterando o observador

O objeto não é movido no mundo.

A matriz que muda é a `View`.

Para:

```text
C = (0, 0, 3)
```

temos:

```text
View = T(0, 0, -3)
```

Para:

```text
C = (1, 0, 3)
```

temos:

```text
View = T(-1, 0, -3)
```

A cena parece se mover porque passamos a observá-la a partir de outro ponto.

---

## Desafio 5 — Diagnóstico de pipeline

A expressão correta é:

```glsl
gl_Position =
    uProjection *
    uView *
    uModel *
    vec4(aPos, 1.0);
```

Em:

```python
model = T @ Rz @ Ry @ Rx @ S
```

a primeira operação é `S`.

`View` representa a cena em relação ao observador.

`Projection` define como a cena 3D é projetada.

Uma ordem incorreta mistura transformações que deveriam ocorrer em espaços diferentes e pode produzir posições, escalas e orientações inesperadas.
