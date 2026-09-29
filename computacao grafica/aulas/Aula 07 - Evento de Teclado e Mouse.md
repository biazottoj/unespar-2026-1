# Aula 07 - Eventos de Teclado e Mouse em OpenGL

Este walkthrough apresenta uma prática em **OpenGL com Python + GLFW**. O objetivo é construir uma aplicação que:

1. captura informações do teclado;
2. captura cliques do mouse;
3. desenha um triângulo a partir de **3 cliques**;
4. muda a cor do triângulo quando o usuário pressiona `R`, `G` ou `B`.

---

## 1. Objetivo da prática

Nesta prática, vamos criar uma aplicação gráfica em OpenGL que permite ao usuário desenhar um triângulo clicando em três pontos da tela.

Além disso, o usuário poderá mudar a cor do triângulo usando o teclado:

| Tecla | Ação |
|---|---|
| `R` | Define a cor do triângulo como vermelho |
| `G` | Define a cor do triângulo como verde |
| `B` | Define a cor do triângulo como azul |
| `C` | Limpa os pontos |
| `ESC` | Fecha a janela |

---

## 2. Instalação das bibliotecas

Antes de executar o código, instale as bibliotecas necessárias:

```bash
pip install glfw PyOpenGL
```

Neste exemplo, usaremos:

```python
import glfw
from OpenGL.GL import *
```

A biblioteca `glfw` será responsável por criar a janela e capturar eventos de teclado e mouse.

A biblioteca `PyOpenGL` será usada para executar comandos OpenGL.

---

## 3. Ideia geral da aplicação

A aplicação terá três partes principais:

### Entrada do usuário

A entrada do usuário envolve capturar:

- teclas pressionadas;
- cliques do mouse.

### Estado da aplicação

O estado da aplicação envolve guardar:

- os pontos clicados;
- a cor atual do triângulo.

### Renderização

A renderização envolve:

- limpar a tela;
- desenhar os pontos clicados;
- desenhar o triângulo quando houver 3 pontos.

---

## 4. Estado da aplicação

Vamos começar pensando nos dados que precisam ser armazenados.

```python
pontos = []
cor_atual = [1.0, 0.0, 0.0]
```

A lista `pontos` armazenará os pontos clicados pelo usuário.

Cada ponto será representado como uma tupla:

```python
(x, y)
```

Por exemplo:

```python
pontos = [
    (-0.5, 0.2),
    (0.3, 0.7),
    (0.6, -0.4)
]
```

A variável `cor_atual` guarda a cor atual do triângulo no formato RGB.

```python
cor_atual = [1.0, 0.0, 0.0]
```

Esse valor representa vermelho, porque:

| Componente | Valor |
|---|---|
| R | `1.0` |
| G | `0.0` |
| B | `0.0` |

Em OpenGL, normalmente as cores variam entre `0.0` e `1.0`.

---

## 5. Capturando informações do teclado

Para capturar teclas com GLFW, criamos uma função de callback.

Uma função de callback é uma função chamada automaticamente quando algum evento acontece.

No caso do teclado:

```python
def key_callback(window, key, scancode, action, mods):
    global cor_atual, pontos

    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

        elif key == glfw.KEY_R:
            cor_atual = [1.0, 0.0, 0.0]

        elif key == glfw.KEY_G:
            cor_atual = [0.0, 1.0, 0.0]

        elif key == glfw.KEY_B:
            cor_atual = [0.0, 0.0, 1.0]

        elif key == glfw.KEY_C:
            pontos.clear()
```

Essa função recebe vários parâmetros:

| Parâmetro | Significado |
|---|---|
| `window` | Janela onde o evento aconteceu |
| `key` | Tecla pressionada |
| `scancode` | Código físico da tecla |
| `action` | Tipo de ação: pressionar, soltar ou repetir |
| `mods` | Modificadores, como Shift, Ctrl e Alt |

A linha:

```python
if action == glfw.PRESS:
```

garante que o código execute apenas quando a tecla for pressionada.

Assim, evitamos que a ação seja executada várias vezes enquanto a tecla estiver sendo segurada.

---

## 6. Registrando o callback de teclado

Depois de criar a janela, precisamos informar ao GLFW qual função deve ser chamada quando uma tecla for pressionada.

```python
glfw.set_key_callback(window, key_callback)
```

Sem essa linha, a função `key_callback` existe no código, mas nunca será chamada.

---

## 7. Capturando cliques do mouse

Agora precisamos capturar os cliques do mouse.

Para isso, criamos outro callback:

```python
def mouse_button_callback(window, button, action, mods):
    global pontos

    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        x_mouse, y_mouse = glfw.get_cursor_pos(window)

        largura, altura = glfw.get_window_size(window)

        x_opengl = (x_mouse / largura) * 2 - 1
        y_opengl = 1 - (y_mouse / altura) * 2

        if len(pontos) < 3:
            pontos.append((x_opengl, y_opengl))
```

Esse código faz quatro coisas:

1. verifica se o botão esquerdo foi pressionado;
2. obtém a posição do mouse;
3. converte a posição do mouse para coordenadas OpenGL;
4. armazena o ponto na lista `pontos`.

---

## 8. Convertendo coordenadas do mouse para coordenadas OpenGL

O mouse trabalha com coordenadas em pixels.

Por exemplo, em uma janela de `800 x 600`:

| Posição | Coordenada do mouse |
|---|---|
| Canto superior esquerdo | `(0, 0)` |
| Centro da janela | `(400, 300)` |
| Canto inferior direito | `(800, 600)` |

Já o OpenGL trabalha, neste exemplo, com coordenadas normalizadas:

| Posição | Coordenada OpenGL |
|---|---|
| Esquerda | `-1` |
| Direita | `1` |
| Baixo | `-1` |
| Cima | `1` |
| Centro | `(0, 0)` |

Por isso, precisamos converter as coordenadas do mouse.

Para o eixo X:

```python
x_opengl = (x_mouse / largura) * 2 - 1
```

Essa fórmula transforma o intervalo:

```text
0 até largura
```

em:

```text
-1 até 1
```

Para o eixo Y:

```python
y_opengl = 1 - (y_mouse / altura) * 2
```

Aqui fazemos uma inversão porque o mouse considera `y = 0` no topo da janela, enquanto o OpenGL considera o topo como `y = 1`.

---

## 9. Registrando o callback do mouse

Assim como fizemos com o teclado, precisamos registrar o callback do mouse:

```python
glfw.set_mouse_button_callback(window, mouse_button_callback)
```

Agora, sempre que o usuário clicar na janela, a função `mouse_button_callback` será chamada.

---

## 10. Desenhando os pontos clicados

Antes de desenhar o triângulo, é útil mostrar os pontos clicados.

```python
def desenhar_pontos():
    glPointSize(8)
    glColor3f(1.0, 1.0, 1.0)

    glBegin(GL_POINTS)
    for x, y in pontos:
        glVertex2f(x, y)
    glEnd()
```

Aqui usamos:

```python
glPointSize(8)
```

para aumentar o tamanho dos pontos.

Depois usamos:

```python
glBegin(GL_POINTS)
```

para indicar que queremos desenhar pontos.

Cada ponto é desenhado com:

```python
glVertex2f(x, y)
```

---

## 11. Desenhando o triângulo

O triângulo só deve ser desenhado quando existirem exatamente três pontos.

```python
def desenhar_triangulo():
    if len(pontos) == 3:
        glColor3f(cor_atual[0], cor_atual[1], cor_atual[2])

        glBegin(GL_TRIANGLES)
        for x, y in pontos:
            glVertex2f(x, y)
        glEnd()
```

A condição:

```python
if len(pontos) == 3:
```

verifica se o usuário já clicou três vezes.

Se houver três pontos, desenhamos um triângulo usando:

```python
glBegin(GL_TRIANGLES)
```

A cor do triângulo é definida por:

```python
glColor3f(cor_atual[0], cor_atual[1], cor_atual[2])
```

Portanto, se o usuário pressionar `R`, `G` ou `B`, o valor de `cor_atual` muda, e o triângulo passa a ser desenhado com a nova cor.

---

## 12. Código completo

```python
import glfw
from OpenGL.GL import *


pontos = []
cor_atual = [1.0, 0.0, 0.0]


def key_callback(window, key, scancode, action, mods):
    global cor_atual, pontos

    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

        elif key == glfw.KEY_R:
            cor_atual = [1.0, 0.0, 0.0]

        elif key == glfw.KEY_G:
            cor_atual = [0.0, 1.0, 0.0]

        elif key == glfw.KEY_B:
            cor_atual = [0.0, 0.0, 1.0]

        elif key == glfw.KEY_C:
            pontos.clear()


def mouse_button_callback(window, button, action, mods):
    global pontos

    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        x_mouse, y_mouse = glfw.get_cursor_pos(window)

        largura, altura = glfw.get_window_size(window)

        x_opengl = (x_mouse / largura) * 2 - 1
        y_opengl = 1 - (y_mouse / altura) * 2

        if len(pontos) < 3:
            pontos.append((x_opengl, y_opengl))


def desenhar_pontos():
    glPointSize(8)
    glColor3f(1.0, 1.0, 1.0)

    glBegin(GL_POINTS)
    for x, y in pontos:
        glVertex2f(x, y)
    glEnd()


def desenhar_triangulo():
    if len(pontos) == 3:
        glColor3f(cor_atual[0], cor_atual[1], cor_atual[2])

        glBegin(GL_TRIANGLES)
        for x, y in pontos:
            glVertex2f(x, y)
        glEnd()


def main():
    if not glfw.init():
        print("Erro ao inicializar GLFW")
        return

    window = glfw.create_window(800, 600, "Triângulo com 3 cliques", None, None)

    if not window:
        glfw.terminate()
        print("Erro ao criar a janela")
        return

    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)

    glClearColor(0.1, 0.1, 0.1, 1.0)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        desenhar_triangulo()
        desenhar_pontos()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
```

---

## 13. Como testar o programa

Ao executar o programa:

```bash
python triangulo_interativo.py
```

A janela será aberta.

Em seguida:

1. clique em três pontos diferentes da tela;
2. um triângulo será desenhado usando esses três pontos;
3. pressione `R` para deixar o triângulo vermelho;
4. pressione `G` para deixar o triângulo verde;
5. pressione `B` para deixar o triângulo azul;
6. pressione `C` para limpar os pontos e desenhar outro triângulo;
7. pressione `ESC` para fechar a janela.

---

## 14. Fluxo lógico da aplicação

A lógica geral é esta:

```text
Iniciar GLFW
Criar janela
Registrar callbacks de teclado e mouse

Enquanto a janela estiver aberta:
    Limpar a tela
    Desenhar o triângulo, se houver 3 pontos
    Desenhar os pontos clicados
    Atualizar a janela
    Processar eventos

Encerrar GLFW
```

---

## 15. O que acontece quando o usuário pressiona uma tecla?

Quando o usuário pressiona uma tecla, o GLFW chama automaticamente:

```python
key_callback(...)
```

Se a tecla for `R`, a cor atual vira vermelho:

```python
cor_atual = [1.0, 0.0, 0.0]
```

Se for `G`, a cor atual vira verde:

```python
cor_atual = [0.0, 1.0, 0.0]
```

Se for `B`, a cor atual vira azul:

```python
cor_atual = [0.0, 0.0, 1.0]
```

Como a cena é redesenhada continuamente dentro do loop principal, a alteração de cor aparece imediatamente na tela.

---

## 16. O que acontece quando o usuário clica?

Quando o usuário clica com o botão esquerdo, o GLFW chama:

```python
mouse_button_callback(...)
```

Dentro dessa função, o programa captura a posição do mouse:

```python
x_mouse, y_mouse = glfw.get_cursor_pos(window)
```

Depois converte essa posição para coordenadas OpenGL:

```python
x_opengl = (x_mouse / largura) * 2 - 1
y_opengl = 1 - (y_mouse / altura) * 2
```

Por fim, armazena o ponto:

```python
pontos.append((x_opengl, y_opengl))
```

Quando a lista tiver três pontos, o triângulo será desenhado.

---

## 17. Por que armazenar os pontos?

Em OpenGL, normalmente a tela é redesenhada várias vezes por segundo.

Isso significa que o clique do mouse não deve ser pensado como algo que “desenha permanentemente” na tela.

O clique apenas altera o estado da aplicação.

Neste exemplo, o estado é a lista:

```python
pontos
```

A cada frame, o programa consulta essa lista e redesenha os pontos e o triângulo.

Essa é uma ideia central em aplicações gráficas interativas:

```text
Entrada do usuário altera o estado.
O estado define o que será desenhado.
A cena é redesenhada continuamente.
```
