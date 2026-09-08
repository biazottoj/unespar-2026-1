# Trabalho Bimestral — Manipulador e Visualizador de um Objeto 3D

## Objetivo

Neste trabalho, o grupo deverá desenvolver uma aplicação em **Python + OpenGL** capaz de manipular e visualizar **um único objeto 3D**, integrando os principais conteúdos estudados durante o bimestre:

---

# 1. Objeto principal

A aplicação deve possuir **um único objeto 3D principal**.

Você pode utilizar o mesmo cubo colorido desenvolvido durante as aulas ou outro objeto simples construído a partir da mesma estrutura.

O objetivo é utilizar o objeto como base para explorar diferentes transformações e formas de visualização.

---

# 2. Transformações 3D

O objeto deve permitir as seguintes transformações:

- translação em X;
- translação em Y;
- translação em Z;
- escala uniforme;
- rotação em X;
- rotação em Y;
- rotação em Z.

As transformações devem ser combinadas por meio da matriz `Model`.

Um exemplo de composição é:

```python
model = (
    T
    @ Rz
    @ Ry
    @ Rx
    @ S
)
```

Você deve compreender e conseguir explicar a ordem em que as transformações são aplicadas.

---

# 3. Comparação da ordem das transformações

A aplicação deve permitir comparar **pelo menos duas ordens diferentes de composição**.

Por exemplo:

```text
Modo 1:
T × R × S
```

```text
Modo 2:
R × T × S
```

O programa deve possuir uma tecla para alternar entre os modos.

Exemplo:

```text
O → alterar ordem de composição
```

O objetivo é demonstrar visualmente que:

```text
A × B ≠ B × A
```

e que a ordem das transformações pode alterar significativamente o resultado final.

---

# 4. Rotação em torno de um pivô

O objeto deve permitir dois modos de rotação:

```text
Modo 1 → rotação em torno da própria origem
Modo 2 → rotação em torno de um pivô externo
```

O pivô pode ser definido, por exemplo, como:

```text
C = (1, 0, 0)
```

A transformação deve utilizar a ideia:

```text
M = T(C) × R × T(-C)
```

Uma tecla pode ser utilizada para alternar entre os dois modos.

Exemplo:

```text
P → origem / pivô externo
```

---

# 5. Órbita

A aplicação deve possuir também um modo em que o objeto **orbita em torno de um ponto externo**.

Por exemplo:

```text
C = (1, 0, 0)
```

A composição pode seguir a ideia:

```text
M = T(C) × Ry(θ) × T(-C)
```

O objetivo é mostrar a diferença entre:

- rotacionar o objeto em torno de sua própria origem;
- rotacionar o objeto em torno de um ponto externo.

---

# 6. Projeção paralela e perspectiva

A aplicação deve permitir alternar em tempo de execução entre:

```text
1 → projeção paralela
2 → projeção em perspectiva
```

A mesma cena e o mesmo objeto devem ser utilizados nos dois casos.

No Vertex Shader, o pipeline deve utilizar:

```glsl
gl_Position =
    uProjection *
    uView *
    uModel *
    vec4(aPos, 1.0);
```

O objetivo é permitir a comparação direta entre as duas formas de projeção.

---

# 7. Experimento de profundidade

O objeto deve poder ser movimentado no eixo Z.

Por exemplo:

```text
W → aproximar
S → afastar
```

Ao movimentar o objeto, deve ser possível observar a diferença entre as projeções.

Na projeção paralela:

```text
a profundidade não altera significativamente o tamanho aparente
```

Na projeção em perspectiva:

```text
objetos mais distantes aparecem menores
```

O comportamento deve ser claramente observável durante a execução do programa.

---

# 8. Campo de visão — FOV

Na projeção em perspectiva, o usuário deve poder modificar o:

```text
FOV
```

Exemplo de controles:

```text
Q → diminuir FOV
E → aumentar FOV
```

Utilize limites adequados, por exemplo:

```text
20° até 120°
```

A aplicação deve permitir observar que:

```text
FOV menor → visão mais fechada
FOV maior → visão mais aberta
```

---

# 9. Centro de projeção e matriz View

O programa deve definir explicitamente um centro de projeção.

Por exemplo:

```python
center_of_projection = np.array([
    0.0,
    0.0,
    3.0
])
```

A matriz `View` deve ser construída utilizando:

```python
view = translation_matrix(
    -center_of_projection[0],
    -center_of_projection[1],
    -center_of_projection[2]
)
```

A aplicação deve permitir modificar **pelo menos uma coordenada do observador**.

Por exemplo:

```text
A → mover observador para a esquerda
D → mover observador para a direita
```

O objetivo é observar como a cena muda quando o ponto de vista é alterado.

---

# 10. Visualização 2D auxiliar

Além da visualização principal em 3D, a aplicação deve possuir uma pequena representação 2D auxiliar do objeto.

Essa visualização pode funcionar como um **minimapa visto de cima**.

Uma possível correspondência é:

```text
X do mundo → X do mapa
Z do mundo → Y do mapa
```

A representação 2D deve acompanhar a posição do objeto na cena.

### Exemplo ilustrativo da tela

A imagem abaixo representa **apenas um exemplo de organização da interface**.  
Você não precisa seguir exatamente esse layout, mas sua aplicação deve deixar claro:

- onde está a visualização principal em 3D;
- onde está a representação 2D auxiliar;
- qual é o objeto e sua orientação;
- quais informações ou controles estão ativos.

```text
+--------------------------------------------------------------+
|                                                              |
|                    VISUALIZAÇÃO PRINCIPAL 3D                 |
|                                                              |
|                           ______                             |
|                         /|     /|                            |
|                        /_|____/ |                            |
|                        | |    | |                            |
|                        | |____|_/                            |
|                        |/_____|/                             |
|                                                              |
|                 Objeto 3D manipulado pelo usuário            |
|                                                              |
|-----------------------------------------+--------------------|
|           VISUALIZAÇÃO 2D AUXILIAR      |     INFORMAÇÕES    |
|                                         |                    |
|              +------------------+       | Projeção: Persp.   |
|              |                  |       | FOV: 60°           |
|              |        ↑         |       | Pivô: Externo      |
|              |        □         |       | Ordem: T × R × S   |
|              |                  |       | Observador X: 0.0  |
|              |                  |       | Z do objeto: -2.0  |
|              +------------------+       |                    |
|                                         | 1/2  → projeção    |
|        minimapa / vista superior        | Q/E  → FOV         |
|        X do mundo → X do mapa           | P    → pivô        |
|        Z do mundo → Y do mapa           | O    → ordem       |
+--------------------------------------------------------------+
```

Nesse exemplo:

- a área superior mostra o **objeto 3D principal**;
- a área inferior esquerda mostra o **minimapa 2D**;
- o símbolo `□` representa a posição do objeto;
- a seta `↑` representa sua orientação no plano;
- o painel da direita mostra algumas informações úteis ao usuário.



---

# 11. Transformações 2D no minimapa

A representação 2D deve aplicar conceitos de Transformações 2D.

Ela deve acompanhar pelo menos:

- posição em X;
- posição em Z;
- rotação em Y.

Por exemplo, uma seta ou pequeno símbolo pode indicar a orientação do objeto.

Ao rotacionar o objeto em Y, a representação 2D deve também mudar sua orientação.

A composição pode utilizar:

```text
M2D = T × R × S
```

O objetivo é integrar Transformações 2D à aplicação de forma funcional.

---

# 12. Modo de comparação

A aplicação deve possuir um modo de comparação que configure automaticamente o objeto em uma posição conhecida.

Exemplo:

```text
x = 0
y = 0
z = -2
rotation_y = 30°
```

Uma tecla pode ativar esse modo:

```text
C → modo de comparação
```

Depois disso, o usuário deve conseguir alternar entre:

```text
1 → projeção paralela
2 → projeção em perspectiva
```

O objetivo é facilitar a comparação entre as projeções utilizando exatamente a mesma configuração do objeto.

---

# 13. Requisitos obrigatórios

| Item | Requisito |
|---|---|
| Objeto | 1 objeto 3D |
| Translação | X, Y e Z |
| Escala | uniforme |
| Rotação | X, Y e Z |
| Composição | pelo menos duas ordens diferentes |
| Pivô | origem e pivô externo |
| Órbita | rotação em torno de ponto externo |
| Model | utilizada corretamente |
| View | centro de projeção explícito |
| Projeção paralela | implementada |
| Projeção em perspectiva | implementada |
| FOV | modificável em execução |
| Profundidade | movimento no eixo Z |
| Visualização 2D | minimapa ou representação auxiliar |
| Transformações 2D | posição e rotação no minimapa |
| Shader | `Projection × View × Model` |

---

# 15. Controles

Os controles são livres, desde que sejam claramente informados.

Uma possibilidade é:

```text
Setas → translação em X e Y
W / S → translação em Z

I / K → rotação em X
J / L → rotação em Y
U / O → rotação em Z

+ / - → escala

1 → projeção paralela
2 → projeção em perspectiva

Q / E → alterar FOV

A / D → mover observador em X

P → alternar pivô
C → modo de comparação
```

Você pode utilizar outras teclas, desde que não existam conflitos e os controles sejam apresentados de forma clara.


# 16. Entrega

A entrega deve conter:

- código-fonte completo da aplicação;
- arquivo `README.md` com instruções de execução;
- lista dos controles utilizados;
- identificação dos integrantes;
