# Atividade — Comparando Profundidade com Projeções 3D

## Objetivo

A partir do código desenvolvido em aula, modifique a cena para demonstrar experimentalmente como **projeção paralela** e **projeção em perspectiva** tratam objetos posicionados em diferentes profundidades.

Ao final, o programa deverá permitir observar claramente a influência de:

- profundidade;
- tipo de projeção;
- centro de projeção;
- campo de visão.

---

# Situação inicial

O código desenvolvido em aula possui um único cubo e permite alternar entre:

```text
1 → projeção paralela
2 → projeção em perspectiva
```

O objeto também pode sofrer:

- translação;
- escala;
- rotação.

Sua tarefa será criar uma nova versão desse programa.

---

# Parte 1 — Adicionar novos objetos à cena

Utilize o **mesmo cubo já existente** para desenhar pelo menos **três cubos**.

Não crie novos VAOs ou VBOs.

A mesma geometria deve ser reutilizada.

Posicione os cubos em profundidades diferentes, por exemplo:

```text
Cubo A → z = 0
Cubo B → z = -2
Cubo C → z = -4
```

Eles também devem possuir posições em X diferentes para que seja possível enxergá-los simultaneamente.

Uma possível disposição seria:

```text
Cubo A
x = -1.2
z = 0

Cubo B
x = 0
z = -2

Cubo C
x = 1.2
z = -4
```

## Ideia

Para cada cubo, crie uma matriz `Model` diferente.

Por exemplo:

```python
model_a = translation_matrix(
    -1.2,
    0.0,
    0.0
)

model_b = translation_matrix(
    0.0,
    0.0,
    -2.0
)

model_c = translation_matrix(
    1.2,
    0.0,
    -4.0
)
```

Antes de desenhar cada cubo:

```python
glUniformMatrix4fv(
    model_location,
    1,
    GL_TRUE,
    model_a
)

draw_cube()
```

Depois:

```python
glUniformMatrix4fv(
    model_location,
    1,
    GL_TRUE,
    model_b
)

draw_cube()
```

E assim por diante.

---

# Parte 2 — Comparar as projeções

Execute a cena usando:

```text
1 → projeção paralela
```

Observe os três cubos.

Depois altere para:

```text
2 → projeção em perspectiva
```

Observe novamente.

## Responda

1. Os três cubos possuem o mesmo tamanho geométrico?
2. Na projeção paralela, eles aparecem com o mesmo tamanho?
3. Na perspectiva, qual cubo aparece menor?
4. Por que isso acontece?
5. Qual elemento da fórmula da perspectiva provoca essa diferença?

Relacione sua resposta com:

\[
x' \propto \frac{x}{z}
\]

\[
y' \propto \frac{y}{z}
\]

---

# Parte 3 — Criar um objeto móvel em profundidade

Escolha um dos três cubos.

Adicione duas teclas para alterar apenas sua posição em Z.

Por exemplo:

```text
N → aproximar
M → afastar
```

Crie uma variável:

```python
cube_z = -2.0
```

E utilize:

```python
model_b = translation_matrix(
    0.0,
    0.0,
    cube_z
)
```

## Experimento

Com projeção paralela:

1. aproxime o cubo;
2. afaste o cubo;
3. observe seu tamanho.

Depois faça o mesmo usando perspectiva.

### Explique

> Por que movimentar o objeto em Z produz resultados visualmente diferentes nas duas projeções?

---

# Parte 4 — Alterar o campo de visão

Agora modifique o programa para permitir controlar o:

\[
FOV
\]

da projeção em perspectiva.

Crie:

```python
fov = 60.0
```

Adicione controles, por exemplo:

```text
Q → diminuir FOV
E → aumentar FOV
```

Depois reconstrua a matriz:

```python
perspective_projection = perspective_projection_matrix(
    fov,
    aspect,
    near,
    far
)
```

Mantenha o FOV em um intervalo razoável, por exemplo:

```python
fov = max(
    20.0,
    min(
        fov,
        120.0
    )
)
```

## Teste

Compare:

```text
FOV = 30°
FOV = 60°
FOV = 100°
```

## Responda

1. Em qual valor a cena parece mais aproximada?
2. Em qual valor conseguimos enxergar uma região maior?
3. O tamanho real dos cubos foi alterado?
4. O que realmente mudou?

---

# Parte 5 — Alterar o centro de projeção

Agora modifique a posição do observador.

O código possui algo semelhante a:

```python
center_of_projection = np.array([
    0.0,
    0.0,
    3.0
])
```

Adicione controles para alterar:

```python
center_x
```

Por exemplo:

```text
A → mover observador para a esquerda
D → mover observador para a direita
```

Reconstrua:

```python
center_of_projection = np.array([
    center_x,
    0.0,
    3.0
])
```

e então:

```python
view = translation_matrix(
    -center_of_projection[0],
    -center_of_projection[1],
    -center_of_projection[2]
)
```

## Observe

Ao mover o centro de projeção para a direita, aparentemente a cena se desloca para o lado oposto.

### Explique

Por que a matriz de View utiliza:

\[
T(-C)
\]

em vez de:

\[
T(C)
\]

---

# Parte 6 — Adicionar uma referência visual de profundidade

Adicione pelo menos **um elemento novo** à cena que ajude a perceber profundidade.

Escolha uma das opções:

- um quarto cubo;
- uma fileira de cubos;
- um chão formado por linhas;
- dois postes em profundidades diferentes;
- uma parede formada por cubos;
- um corredor simples;
- uma sequência de objetos igualmente espaçados no eixo Z.

Por exemplo:

```text
Cubo 1 → z = 0
Cubo 2 → z = -1
Cubo 3 → z = -2
Cubo 4 → z = -3
Cubo 5 → z = -4
```

Ao alternar entre as projeções, a diferença deve ficar evidente.

---

# Desafio — Criar um corredor 3D

Crie duas fileiras de cubos:

```text
x = -1.0
```

e:

```text
x = 1.0
```

em várias profundidades:

```text
z = 0
z = -1
z = -2
z = -3
z = -4
```

Por exemplo:

```text
●                 ●
   ●           ●
      ●     ●
        ● ●
```

Na projeção em perspectiva, o corredor deverá parecer convergir em direção ao fundo.

Na projeção paralela, esse efeito deverá ser significativamente menor ou inexistente.

---

# Requisitos mínimos

O programa entregue deve:

1. reutilizar o cubo original;
2. possuir pelo menos três objetos em profundidades diferentes;
3. continuar permitindo alternar entre projeção paralela e perspectiva;
4. permitir mover pelo menos um objeto no eixo Z;
5. permitir modificar o FOV;
6. permitir modificar pelo menos uma coordenada do centro de projeção;
7. adicionar pelo menos um novo elemento visual à cena.

---

# Restrição importante

Não é necessário:

- criar outro VAO;
- criar outro VBO para cada cubo;
- alterar a geometria original;
- implementar uma nova janela;
- modificar a estrutura básica do programa.

O objetivo é reutilizar o que já existe e trabalhar principalmente com:

```text
Model
View
Projection
```

---

# Questões para entregar

Junto ao código, responda brevemente:

1. Qual é a principal diferença visual entre projeção paralela e perspectiva?
2. Por que objetos mais distantes ficam menores somente na perspectiva?
3. Qual o papel do centro de projeção?
4. Por que transladamos o centro de projeção para a origem?
5. O que ocorre quando o FOV aumenta?
6. Alterar a matriz de projeção modifica a geometria armazenada no VBO? Explique.
7. Se dois cubos idênticos estiverem em profundidades diferentes, por que eles podem possuir tamanhos diferentes na tela mesmo usando exatamente o mesmo VBO?

---

# Resultado esperado

Ao final, o aluno deve conseguir produzir uma cena semelhante conceitualmente a:

```text
PROJEÇÃO PARALELA

┌───┐      ┌───┐      ┌───┐
│   │      │   │      │   │
└───┘      └───┘      └───┘


PROJEÇÃO EM PERSPECTIVA

┌─────┐       ┌───┐         ┌─┐
│     │       │   │         └─┘
└─────┘       └───┘
 perto          ↓           longe
```

