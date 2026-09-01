# Atividade — Construindo um Robô 3D com Transformações

## Objetivo

Nesta atividade, você irá partir do **código-base do cubo 3D** utilizado em sala e transformá-lo em um **robô formado por vários cubos**.

---

# Parte 1 — Entendendo o código-base

O código-base já possui:

- criação da janela;
- configuração do OpenGL;
- Vertex Shader e Fragment Shader;
- VAO e VBO;
- geometria do cubo;
- cores das faces;
- funções de transformação;
- laço principal da aplicação.

Você **não deve recriar essas partes**.

A atividade consiste em modificar o programa para reutilizar o cubo várias vezes.

Antes de começar, localize no código:

```python
translation_matrix(...)
```

```python
scale_matrix(...)
```

```python
rotation_x_matrix(...)
```

```python
rotation_y_matrix(...)
```

```python
rotation_z_matrix(...)
```

e identifique onde a matriz:

```python
model
```

é enviada ao shader.

---

# Parte 2 — Criando uma função para desenhar um cubo

Atualmente o programa desenha um único cubo.

Vamos criar uma função que permita desenhar o mesmo cubo várias vezes, utilizando matrizes diferentes.

Crie uma função:

```python
def draw_cube(model):
```

Ela deverá:

1. enviar `model` para o `uniform uModel`;
2. desenhar as faces;
3. desenhar as arestas.

Uma estrutura possível é:

```python
def draw_cube(model):

    glUniformMatrix4fv(
        model_location,
        1,
        GL_TRUE,
        model
    )

    # Faces
    glBindVertexArray(face_vao)

    glDrawArrays(
        GL_TRIANGLES,
        0,
        face_vertex_count
    )

    # Arestas
    glBindVertexArray(edge_vao)

    glDrawArrays(
        GL_LINES,
        0,
        edge_vertex_count
    )

    glBindVertexArray(0)
```

Ajuste os nomes das variáveis de acordo com o código-base fornecido.

---

# Parte 3 — Construindo o tronco

Comece utilizando o cubo original como tronco do robô.

O cubo deve ser:

- mais alto no eixo Y;
- um pouco mais largo no eixo X;
- mais fino no eixo Z.

Por exemplo:

```python
tronco = (
    translation_matrix(
        0.0,
        0.0,
        0.0
    )
    @
    scale_matrix(
        0.35,
        0.50,
        0.20
    )
)
```

Depois:

```python
draw_cube(tronco)
```

Execute o programa.

Você deverá visualizar apenas o tronco.

## Teste

Altere os três valores utilizados em:

```python
scale_matrix(...)
```

e observe qual dimensão do tronco é modificada.

---

# Parte 4 — Adicionando a cabeça

A cabeça será outro desenho do **mesmo cubo**.

Ela deverá:

- ser menor;
- ficar acima do tronco.

Crie uma nova matriz:

```python
cabeca = (
    translation_matrix(
        0.0,
        0.65,
        0.0
    )
    @
    scale_matrix(
        0.22,
        0.22,
        0.22
    )
)
```

Depois:

```python
draw_cube(cabeca)
```

Execute novamente.

Agora deverão aparecer:

- tronco;
- cabeça.

## Observe

Nenhum novo VBO foi criado.

O mesmo cubo foi desenhado duas vezes.

O que mudou foi:

```python
uModel
```

---

# Parte 5 — Criando os braços

Agora adicione dois braços.

## Braço esquerdo

Crie algo semelhante a:

```python
braco_esquerdo = (
    translation_matrix(
        -0.50,
        0.10,
        0.0
    )
    @
    scale_matrix(
        0.12,
        0.45,
        0.12
    )
)
```

Depois:

```python
draw_cube(braco_esquerdo)
```

## Braço direito

Repita o processo do outro lado:

```python
braco_direito = (
    translation_matrix(
        0.50,
        0.10,
        0.0
    )
    @
    scale_matrix(
        0.12,
        0.45,
        0.12
    )
)
```

Depois:

```python
draw_cube(braco_direito)
```

Execute o programa.

Faça pequenos ajustes nos valores de translação e escala até que os braços fiquem visualmente conectados ao tronco.

---

# Parte 6 — Criando as pernas

Agora crie duas pernas.

## Perna esquerda

```python
perna_esquerda = (
    translation_matrix(
        -0.20,
        -0.75,
        0.0
    )
    @
    scale_matrix(
        0.14,
        0.45,
        0.14
    )
)
```

## Perna direita

```python
perna_direita = (
    translation_matrix(
        0.20,
        -0.75,
        0.0
    )
    @
    scale_matrix(
        0.14,
        0.45,
        0.14
    )
)
```

Desenhe:

```python
draw_cube(perna_esquerda)
draw_cube(perna_direita)
```

Neste ponto, seu robô deve possuir:

- 1 tronco;
- 1 cabeça;
- 2 braços;
- 2 pernas.

Total:

\[
6
\]

cubos renderizados usando a mesma geometria.

---

# Parte 7 — Organizando a construção do robô

Agora crie uma função:

```python
def draw_robot():
```

Mova para ela a construção de:

- tronco;
- cabeça;
- braços;
- pernas.

A estrutura será semelhante a:

```python
def draw_robot():

    tronco = ...
    draw_cube(tronco)

    cabeca = ...
    draw_cube(cabeca)

    braco_esquerdo = ...
    draw_cube(braco_esquerdo)

    braco_direito = ...
    draw_cube(braco_direito)

    perna_esquerda = ...
    draw_cube(perna_esquerda)

    perna_direita = ...
    draw_cube(perna_direita)
```

No laço principal, o desenho deverá ficar mais simples:

```python
draw_robot()
```

---

# Parte 8 — Criando a transformação geral do robô

Até agora, cada peça possui sua própria posição.

Agora queremos mover o **robô inteiro**.

Crie variáveis:

```python
robot_x = 0.0
robot_y = 0.0
robot_z = 0.0

robot_angle = 0.0

robot_scale = 1.0
```

Crie uma matriz geral:

```python
robot_transform = (
    translation_matrix(
        robot_x,
        robot_y,
        robot_z
    )
    @
    rotation_y_matrix(
        robot_angle
    )
    @
    scale_matrix(
        robot_scale,
        robot_scale,
        robot_scale
    )
)
```

Essa matriz representa a transformação do personagem inteiro.

---

# Parte 9 — Aplicando a transformação geral às peças

Agora cada parte deve combinar:

1. transformação do robô;
2. transformação local da peça.

Por exemplo, o tronco:

```python
tronco = (
    robot_transform
    @
    translation_matrix(
        0.0,
        0.0,
        0.0
    )
    @
    scale_matrix(
        0.35,
        0.50,
        0.20
    )
)
```

A cabeça:

```python
cabeca = (
    robot_transform
    @
    translation_matrix(
        0.0,
        0.65,
        0.0
    )
    @
    scale_matrix(
        0.22,
        0.22,
        0.22
    )
)
```

Faça o mesmo para:

- braço esquerdo;
- braço direito;
- perna esquerda;
- perna direita.

---

# Parte 10 — Movimentando o robô

Adicione controles de teclado.

## Movimento em X

```python
if glfw.get_key(
    window,
    glfw.KEY_RIGHT
) == glfw.PRESS:

    robot_x += 0.02
```

```python
if glfw.get_key(
    window,
    glfw.KEY_LEFT
) == glfw.PRESS:

    robot_x -= 0.02
```

## Movimento em Y

```python
if glfw.get_key(
    window,
    glfw.KEY_UP
) == glfw.PRESS:

    robot_y += 0.02
```

```python
if glfw.get_key(
    window,
    glfw.KEY_DOWN
) == glfw.PRESS:

    robot_y -= 0.02
```

## Movimento em Z

Use:

```text
W
S
```

para modificar:

```python
robot_z
```

Teste o programa e verifique se **todas as partes se movem juntas**.

---

# Parte 11 — Rotacionando o robô inteiro

Utilize duas teclas para modificar:

```python
robot_angle
```

Por exemplo:

```text
J → girar para um lado
L → girar para o outro
```

Exemplo:

```python
if glfw.get_key(
    window,
    glfw.KEY_J
) == glfw.PRESS:

    robot_angle += 1.0
```

```python
if glfw.get_key(
    window,
    glfw.KEY_L
) == glfw.PRESS:

    robot_angle -= 1.0
```

A rotação deverá ser aplicada no eixo Y.

Teste se:

- cabeça;
- tronco;
- braços;
- pernas;

rotacionam juntos.

---

# Parte 12 — Alterando a escala do robô

Use:

```text
+
-
```

para modificar:

```python
robot_scale
```

Exemplo:

```python
robot_scale += 0.01
```

e:

```python
robot_scale -= 0.01
```

Evite valores muito pequenos:

```python
robot_scale = max(
    robot_scale,
    0.1
)
```

Agora o personagem inteiro deve aumentar e diminuir mantendo suas proporções.

---

# Parte 13 — Criando uma parte articulada

Agora faça uma alteração que afete **somente uma parte** do robô.

Utilize o braço direito.

Crie:

```python
right_arm_angle = 0.0
```

Associe:

```text
I
K
```

à alteração desse valor.

Por exemplo:

```python
if glfw.get_key(
    window,
    glfw.KEY_I
) == glfw.PRESS:

    right_arm_angle += 1.0
```

```python
if glfw.get_key(
    window,
    glfw.KEY_K
) == glfw.PRESS:

    right_arm_angle -= 1.0
```

---

# Parte 14 — Rotacionando o braço

Inicialmente, experimente adicionar uma rotação ao braço:

```python
braco_direito = (
    robot_transform
    @
    translation_matrix(
        0.50,
        0.10,
        0.0
    )
    @
    rotation_z_matrix(
        right_arm_angle
    )
    @
    scale_matrix(
        0.12,
        0.45,
        0.12
    )
)
```

Execute e observe o comportamento.

## Analise

O braço está girando exatamente da maneira esperada?

Ele gira em torno:

- do próprio centro?
- da origem?
- da região onde estaria o ombro?

Faça ajustes na ordem das transformações e nos deslocamentos para que a rotação fique visualmente próxima de uma articulação do ombro.

A ideia que pode ajudar é:

\[
T(C)\;R\;T(-C)
\]

onde \(C\) representa o ponto em torno do qual desejamos girar.

---

# Parte 15 — Reset das transformações

Adicione uma tecla:

```text
SPACE
```

para restaurar:

```python
robot_x = 0.0
robot_y = 0.0
robot_z = 0.0

robot_angle = 0.0
robot_scale = 1.0

right_arm_angle = 0.0
```

---

# Parte 16 — Resultado mínimo esperado

Ao final, o programa deverá permitir:

```text
Setas
→ movimentar o robô em X e Y

W / S
→ movimentar em Z

J / L
→ rotacionar o robô em Y

+ / -
→ alterar a escala do robô

I / K
→ movimentar o braço direito

SPACE
→ restaurar as transformações
```

O robô deverá continuar sendo construído reutilizando **a mesma geometria do cubo**.

---

# Parte 18 — Perguntas conceituais

Após finalizar o programa, responda às questões abaixo.

## Questão 1

O programa desenha várias partes do robô, mas utiliza o mesmo VAO/VBO.

Explique por que não é necessário criar um VBO diferente para:

- cabeça;
- tronco;
- braços;
- pernas.

---

## Questão 2

Considere:

```python
draw_cube(tronco)
draw_cube(cabeca)
```

Se os dois utilizam a mesma geometria, explique o que faz com que apareçam:

- em posições diferentes;
- com tamanhos diferentes.

---

## Questão 3

Explique a função de:

```glsl
uniform mat4 uModel;
```

no Vertex Shader.

---

## Questão 4

No shader temos:

```glsl
uModel * vec4(aPos, 1.0)
```

Explique:

1. o que representa `aPos`;
2. por que ele é convertido para `vec4`;
3. qual é a função do valor `1.0`.

---

## Questão 5

Considere:

```python
model = T @ R @ S
```

Qual transformação será aplicada primeiro ao vértice?

Explique por quê.

---

## Questão 6

Por que:

```python
T @ R
```

pode produzir um resultado diferente de:

```python
R @ T
```

?

Utilize algum comportamento observado no programa como exemplo.

---

## Questão 7

Explique a diferença entre:

```python
robot_transform
```

e a matriz utilizada especificamente para a cabeça ou braço.

---

## Questão 8

Quando:

```python
robot_angle
```

é alterado, todas as partes do robô rotacionam.

Quando:

```python
right_arm_angle
```

é alterado, apenas o braço direito deve rotacionar.

Explique como a composição de matrizes permite esses dois comportamentos.

---

## Questão 9

Durante a movimentação do robô:

- os vértices originais armazenados no VBO são alterados?
- ou apenas a matriz enviada ao Vertex Shader é alterada?

Explique.

---

## Questão 10

Explique por que o uso de transformações permite construir um objeto complexo a partir de uma geometria simples.

## Entrega

- Utilize o link a seguir para entrega: [https://forms.gle/9o1Dhytv7JaLvFMf7](https://forms.gle/9o1Dhytv7JaLvFMf7)
