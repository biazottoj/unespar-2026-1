# Walkthrough do Aluno — Construindo Projeções 3D com Python e OpenGL

## Objetivo

Neste walkthrough, você irá completar o arquivo `projecoes_3d_base_aula.py`.

O código-base já possui:

- janela OpenGL;
- cubo 3D;
- cores das faces;
- VAO e VBO;
- translação, escala e rotações em X, Y e Z;
- controles pelo teclado;
- desenho das faces e arestas.

Você irá adicionar apenas as partes relacionadas a:

- centro de projeção;
- matriz `View`;
- projeção paralela;
- projeção em perspectiva;
- atualização do Vertex Shader;
- envio das novas matrizes para a GPU;
- alternância entre os dois tipos de projeção.

Ao final, o programa deverá permitir:

```text
1 → projeção paralela
2 → projeção em perspectiva
```

---

# 1. Execute o código-base

Antes de modificar qualquer coisa, execute:

```text
projecoes_3d_base_aula.py
```

Teste os controles já existentes:

```text
Setas → translação em X e Y
W / S → translação em Z

I / K → rotação em X
J / L → rotação em Y
U / O → rotação em Z

+ / - → escala
Espaço → reset
```

Rotacione o cubo em X ou Y e depois mova-o em Z.

## Observe

Em algumas posições o cubo pode parecer achatado ou visualmente estranho.

Isso **não significa que a geometria foi deformada**. As matrizes de transformação continuam corretas.

O problema é que ainda não estamos usando explicitamente uma etapa adequada de visualização e projeção.

> O modelo está correto; a maneira como estamos olhando para ele ainda é simplificada.

---

# 2. Qual problema precisamos resolver?

O cubo possui vértices tridimensionais:

\[
P=(x,y,z)
\]

Mas a tela é bidimensional.

Precisamos representar pontos 3D em uma superfície 2D:

\[
3D \rightarrow 2D
\]

Esse processo é chamado de:

\[
\boxed{\text{projeção}}
\]

Uma projeção determina **como os pontos de uma cena 3D aparecerão na tela**.

---

# 3. Conceitos essenciais

## 3.1 Plano de projeção

O **plano de projeção** é a superfície na qual a imagem é formada.

Podemos imaginá-lo como:

- uma tela;
- uma folha;
- um sensor de câmera;
- uma janela pela qual observamos a cena.

---

## 3.2 Centro de projeção

O **centro de projeção** representa a posição do observador na projeção em perspectiva.

Representamos por:

\[
C=(c_x,c_y,c_z)
\]

Ele pode ser entendido como:

- olho do observador;
- posição da câmera;
- ponto de vista.

---

## 3.3 Projetores

Os **projetores** são retas que relacionam os pontos 3D ao plano de projeção.

### Projeção paralela

Os projetores são paralelos:

```text
objeto                     plano

  ● ----------------------> ●
  ● ----------------------> ●
  ● ----------------------> ●
```

### Projeção em perspectiva

Os projetores passam pelo centro de projeção:

```text
                 ● ponto
                /
               /
C ●-----------/----------- plano
               \
                \
                 ● ponto
```

---

# 4. O novo pipeline

Atualmente, o Vertex Shader trabalha aproximadamente assim:

```text
Ponto
  ↓
Model
  ↓
gl_Position
```

Ao final, teremos:

```text
Ponto local
    ↓
Model
    ↓
Ponto no mundo
    ↓
View
    ↓
Ponto relativo ao observador
    ↓
Projection
    ↓
gl_Position
```

Matematicamente:

\[
P_{clip}
=
P_{projection}
P_{view}
P_{model}
P
\]

No shader:

```glsl
gl_Position =
    uProjection *
    uView *
    uModel *
    vec4(aPos, 1.0);
```

---

# 5. Atualize o Vertex Shader

Procure no código:

```text
UNIFORMS DE VIEW E PROJECAO
```

Depois de:

```glsl
uniform mat4 uModel;
```

adicione:

```glsl
uniform mat4 uView;
uniform mat4 uProjection;
```

Agora procure:

```text
APLICAR VIEW E PROJECAO AQUI
```

Substitua:

```glsl
gl_Position =
    uModel *
    vec4(aPos, 1.0);
```

por:

```glsl
gl_Position =
    uProjection *
    uView *
    uModel *
    vec4(aPos, 1.0);
```

O Vertex Shader deve ficar:

```glsl
#version 330 core

layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aColor;

out vec3 vertexColor;

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

    vertexColor = aColor;
}
```

Com vetores coluna, a transformação mais à direita acontece primeiro:

```text
Model → View → Projection
```

---

# 6. Defina o centro de projeção

Vamos colocar o observador em:

\[
C=(0,0,3)
\]

Procure:

```text
CENTRO DE PROJECAO E MATRIZ VIEW
```

Adicione:

```python
center_of_projection = np.array(
    [0.0, 0.0, 3.0],
    dtype=np.float32
)
```

---

# 7. Translade o centro de projeção para a origem

As fórmulas de perspectiva ficam mais simples quando o observador está em:

\[
C=(0,0,0)
\]

Como nosso centro está em:

\[
C=(0,0,3)
\]

aplicamos à cena:

\[
T(-C)
\]

Logo após `center_of_projection`, adicione:

```python
view = translation_matrix(
    -center_of_projection[0],
    -center_of_projection[1],
    -center_of_projection[2]
)
```

Neste caso:

```text
View = T(0, 0, -3)
```

## Interpretação

Em vez de mover fisicamente a câmera até a origem, movemos a cena na direção contrária.

A matriz `View` transforma coordenadas do mundo para coordenadas relativas ao observador.

Ela **não é a projeção**.

---

# 8. Projeção paralela

Na projeção paralela, os projetores são paralelos.

Vamos implementar uma projeção ortográfica.

Se, depois da View, temos:

\[
P=(X,Y,Z)
\]

geometricamente a projeção ortográfica mais simples mantém:

\[
X'=X
\]

\[
Y'=Y
\]

A profundidade continua existindo, mas não reduz o tamanho projetado.

Portanto:

> Na projeção paralela, afastar um objeto não faz com que ele fique menor.

---

# 9. Implemente a projeção paralela

Procure:

```text
FUNCAO DE PROJECAO PARALELA
```

Adicione:

```python
def parallel_projection_matrix(
    left,
    right,
    bottom,
    top,
    near,
    far
):
    return np.array([
        [
            2.0 / (right - left),
            0.0,
            0.0,
            -(right + left) / (right - left)
        ],
        [
            0.0,
            2.0 / (top - bottom),
            0.0,
            -(top + bottom) / (top - bottom)
        ],
        [
            0.0,
            0.0,
            -2.0 / (far - near),
            -(far + near) / (far - near)
        ],
        [
            0.0,
            0.0,
            0.0,
            1.0
        ]
    ], dtype=np.float32)
```

Não é necessário decorar todos os termos.

Observe principalmente:

\[
[0\quad0\quad0\quad1]
\]

Essa última linha mantém:

\[
w'=1
\]

Assim, não aparece uma divisão de X e Y pela profundidade.

---

# 10. Configure a projeção paralela

Procure:

```text
MATRIZES DE PROJECAO
```

Adicione:

```python
aspect = WIDTH / HEIGHT

near = 1.0
far = 20.0
```

Agora defina a região visível:

```python
half_height = 1.5

half_width = (
    half_height *
    aspect
)
```

Crie a matriz:

```python
parallel_projection = parallel_projection_matrix(
    -half_width,
    half_width,
    -half_height,
    half_height,
    near,
    far
)
```

---

# 11. Recupere os uniforms

O código já possui:

```python
model_location = glGetUniformLocation(
    program,
    "uModel"
)
```

Procure:

```text
UNIFORMS DE VIEW E PROJECAO
```

Adicione:

```python
view_location = glGetUniformLocation(
    program,
    "uView"
)

projection_location = glGetUniformLocation(
    program,
    "uProjection"
)
```

---

# 12. Teste somente a projeção paralela

Procure:

```text
ESCOLHA DA PROJECAO
```

Adicione temporariamente:

```python
projection = parallel_projection
```

Depois procure:

```text
ENVIAR VIEW E PROJECAO AO SHADER
```

Adicione:

```python
glUniformMatrix4fv(
    view_location,
    1,
    GL_TRUE,
    view
)

glUniformMatrix4fv(
    projection_location,
    1,
    GL_TRUE,
    projection
)
```

Execute o programa.

---

# 13. Experimento com a projeção paralela

Rotacione o cubo com:

```text
J / L
```

Depois mova em Z:

```text
W / S
```

Responda:

1. O cubo fica menor quando se afasta?
2. A profundidade altera seu tamanho projetado?
3. Isso está de acordo com a projeção paralela?

---

# 14. Projeção em perspectiva

Agora vamos implementar uma projeção em que:

\[
\boxed{\text{objetos mais distantes aparecem menores}}
\]

Como já aplicamos:

\[
View=T(-C)
\]

o centro de projeção está na origem.

Considere:

\[
P=(X,Y,Z)
\]

com o ponto à frente do observador.

---

# 15. Derive a relação da perspectiva

A reta que sai da origem e passa por P pode ser escrita como:

\[
P(\lambda)
=
(\lambda X,\lambda Y,\lambda Z)
\]

Considere o plano de projeção em:

\[
z=-d
\]

Queremos:

\[
\lambda Z=-d
\]

Portanto:

\[
\lambda=-\frac{d}{Z}
\]

Aplicando a X e Y:

\[
x_p=-\frac{dX}{Z}
\]

\[
y_p=-\frac{dY}{Z}
\]

A ideia principal é que Z aparece no denominador.

Se a distância aumenta:

\[
|Z|\uparrow
\]

então o tamanho projetado diminui.

---

# 16. Coordenadas homogêneas e perspectiva

A matriz de perspectiva pode fazer com que:

\[
w'=-Z
\]

Depois do Vertex Shader, o OpenGL realiza a divisão homogênea:

\[
x_{ndc}=\frac{x_{clip}}{w_{clip}}
\]

\[
y_{ndc}=\frac{y_{clip}}{w_{clip}}
\]

Como:

\[
w_{clip}=-Z
\]

surge a divisão por profundidade.

---

# 17. Implemente a projeção em perspectiva

Procure:

```text
FUNCAO DE PROJECAO EM PERSPECTIVA
```

Adicione:

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

    return np.array([
        [
            f / aspect,
            0.0,
            0.0,
            0.0
        ],
        [
            0.0,
            f,
            0.0,
            0.0
        ],
        [
            0.0,
            0.0,
            (far + near) /
            (near - far),
            (2.0 * far * near) /
            (near - far)
        ],
        [
            0.0,
            0.0,
            -1.0,
            0.0
        ]
    ], dtype=np.float32)
```

Observe principalmente a última linha:

\[
[0\quad0\quad-1\quad0]
\]

Ela faz com que:

\[
w'=-Z
\]

---

# 18. Entenda o FOV

A função recebe:

```python
fov_degrees
```

FOV significa **Field of View**, ou campo de visão.

A função calcula:

```python
f = (
    1.0 /
    np.tan(
        np.radians(
            fov_degrees
        ) / 2.0
    )
)
```

De forma geral:

```text
FOV menor → imagem parece mais aproximada
FOV maior → vemos uma região maior
```

---

# 19. Crie a matriz de perspectiva

Volte à região:

```text
MATRIZES DE PROJECAO
```

Depois de `parallel_projection`, adicione:

```python
perspective_projection = perspective_projection_matrix(
    60.0,
    aspect,
    near,
    far
)
```

Agora existem duas matrizes:

```text
parallel_projection
perspective_projection
```

---

# 20. Faça a seleção da projeção

O código-base já possui:

```text
1 → paralela
2 → perspectiva
```

A variável é:

```python
projection_mode
```

Procure:

```text
ESCOLHA DA PROJECAO
```

Substitua o teste temporário por:

```python
if projection_mode == "parallel":
    projection = parallel_projection
else:
    projection = perspective_projection
```

---

# 21. Execute o programa completo

Teste:

```text
1
```

para projeção paralela.

Depois:

```text
2
```

para perspectiva.

Rotacione o cubo e mova-o em Z.

---

# 22. Experimento principal

## Projeção paralela

Selecione:

```text
1
```

Use:

```text
W / S
```

para mover o cubo em profundidade.

## Projeção em perspectiva

Selecione:

```text
2
```

Repita o movimento.

## Responda

1. Em qual projeção o tamanho aparente muda com Z?
2. Por que isso acontece?
3. Qual papel Z exerce na perspectiva?
4. Por que o mesmo efeito não aparece na projeção paralela?

---

# 23. Experimento com FOV

Procure:

```python
perspective_projection_matrix(
    60.0,
    aspect,
    near,
    far
)
```

Teste:

```text
30°
60°
90°
```

Responda:

1. Qual FOV parece mais aproximado?
2. Qual mostra uma região maior?
3. A geometria do cubo mudou?
4. Qual parte do pipeline foi modificada?

---

# 24. Experimento com o centro de projeção

Procure:

```python
center_of_projection = np.array(
    [0.0, 0.0, 3.0],
    dtype=np.float32
)
```

Teste:

```python
[0.0, 0.0, 5.0]
```

Depois:

```python
[1.0, 0.0, 3.0]
```

Responda:

1. O que mudou na visualização?
2. Por que a View usa o negativo do centro?
3. Estamos movendo o objeto ou mudando o ponto de vista?

---

# 25. O Fragment Shader precisa mudar?

Não.

Ele pode continuar:

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

As projeções trabalham com a posição dos vértices, portanto a principal alteração está no Vertex Shader.

---

# 26. Pipeline final

Ao final, temos:

```text
VBO
 ↓
Ponto local
 ↓
uModel
 ↓
Mundo
 ↓
uView
 ↓
Espaço do observador
 ↓
uProjection
 ↓
Clip Space
 ↓
Divisão por w
 ↓
Tela
```
