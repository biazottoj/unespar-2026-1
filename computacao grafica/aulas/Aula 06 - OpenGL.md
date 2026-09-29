# Explicação detalhada do exemplo: triângulo com clique usando OpenGL, Python e GLFW

Este material explica os principais conceitos aplicados em um exemplo de **OpenGL com Python usando GLFW**, cujo objetivo é:

> Desenhar um triângulo na tela a partir de um clique do mouse.

O exemplo combina conceitos de criação de janela, contexto OpenGL, eventos de mouse, sistema de coordenadas, conversão de coordenadas, primitivas gráficas, vértices, cores e loop de renderização.

---

## Código-base considerado

```python
import glfw
from OpenGL.GL import *


triangulo = None


def converter_para_opengl(x_mouse, y_mouse, largura, altura):
    x = (x_mouse / largura) * 2 - 1
    y = 1 - (y_mouse / altura) * 2
    return x, y


def criar_triangulo(x, y):
    largura = 0.25
    altura = 0.30

    return [
        (x, y),
        (x - largura, y - altura),
        (x + largura, y - altura)
    ]


def clique_mouse(window, button, action, mods):
    global triangulo

    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        x_mouse, y_mouse = glfw.get_cursor_pos(window)
        largura, altura = glfw.get_window_size(window)

        x, y = converter_para_opengl(x_mouse, y_mouse, largura, altura)

        triangulo = criar_triangulo(x, y)


def desenhar_triangulo():
    if triangulo is None:
        return

    glBegin(GL_TRIANGLES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(triangulo[0][0], triangulo[0][1])

    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(triangulo[1][0], triangulo[1][1])

    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(triangulo[2][0], triangulo[2][1])

    glEnd()


def atualizar_viewport(window):
    largura, altura = glfw.get_framebuffer_size(window)
    glViewport(0, 0, largura, altura)


def main():
    if not glfw.init():
        print("Erro ao inicializar o GLFW")
        return

    largura = 800
    altura = 600

    window = glfw.create_window(
        largura,
        altura,
        "Triângulo com clique - GLFW",
        None,
        None
    )

    if not window:
        glfw.terminate()
        print("Erro ao criar a janela")
        return

    glfw.make_context_current(window)

    glfw.set_mouse_button_callback(window, clique_mouse)

    glClearColor(0.1, 0.1, 0.1, 1.0)

    while not glfw.window_should_close(window):
        atualizar_viewport(window)

        glClear(GL_COLOR_BUFFER_BIT)

        desenhar_triangulo()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
```

---

# 1. GLFW

## O que é GLFW?

O **GLFW** é uma biblioteca usada para criar janelas, criar um contexto OpenGL e lidar com entradas do usuário, como teclado, mouse e eventos da janela.

No exemplo, o GLFW é responsável por:

- iniciar o ambiente gráfico;
- criar a janela;
- associar a janela ao OpenGL;
- capturar cliques do mouse;
- manter a janela aberta;
- processar eventos da aplicação.

O GLFW não desenha diretamente o triângulo. Quem faz o desenho é o OpenGL. O GLFW prepara o ambiente para que o OpenGL possa desenhar.

## Como aparece no código?

```python
import glfw
```

Esse comando importa a biblioteca GLFW para o programa Python.

Depois, o GLFW é inicializado com:

```python
if not glfw.init():
    print("Erro ao inicializar o GLFW")
    return
```

Essa parte verifica se o GLFW conseguiu ser iniciado corretamente. Se não conseguir, o programa termina.

Esse passo é necessário porque, antes de criar qualquer janela ou contexto OpenGL, o GLFW precisa preparar seus recursos internos.

---

# 2. PyOpenGL

## O que é PyOpenGL?

O **PyOpenGL** é uma biblioteca que permite usar comandos OpenGL dentro do Python.

No exemplo, ela é importada assim:

```python
from OpenGL.GL import *
```

Essa linha permite usar funções como:

```python
glClearColor()
glClear()
glBegin()
glEnd()
glColor3f()
glVertex2f()
glViewport()
```

Essas funções pertencem ao OpenGL.

Enquanto o GLFW cuida da janela e dos eventos, o PyOpenGL permite chamar as funções de desenho do OpenGL.

---

# 3. Criação da janela

## O que é a janela?

A janela é o espaço visual onde o OpenGL vai desenhar. No exemplo, é criada uma janela de 800 pixels de largura por 600 pixels de altura.

```python
largura = 800
altura = 600

window = glfw.create_window(
    largura,
    altura,
    "Triângulo com clique - GLFW",
    None,
    None
)
```

Aqui, o programa cria uma janela com:

- largura: `800`;
- altura: `600`;
- título: `"Triângulo com clique - GLFW"`.

A variável `window` guarda uma referência para essa janela. Essa referência será usada em várias partes do código, por exemplo, para verificar se a janela deve continuar aberta, capturar eventos e obter a posição do mouse.

## Verificação da criação da janela

```python
if not window:
    glfw.terminate()
    print("Erro ao criar a janela")
    return
```

Essa parte verifica se a janela foi criada corretamente.

Se a criação falhar, o programa chama:

```python
glfw.terminate()
```

Esse comando libera os recursos usados pelo GLFW.

Essa verificação é importante porque o programa não pode continuar se não existir uma janela onde o OpenGL possa desenhar.

---

# 4. Contexto OpenGL

## O que é um contexto OpenGL?

O **contexto OpenGL** é o ambiente que armazena o estado do OpenGL e permite que os comandos de desenho sejam executados.

De forma simplificada:

> A janela é onde o desenho aparece.  
> O contexto OpenGL é o ambiente que permite desenhar nessa janela.

Antes de chamar comandos como `glClearColor`, `glBegin`, `glVertex2f` ou `glColor3f`, é necessário informar qual janela está associada ao contexto OpenGL atual.

Isso é feito com:

```python
glfw.make_context_current(window)
```

Esse comando informa ao GLFW que, a partir daquele momento, os comandos OpenGL devem desenhar naquela janela.

Sem essa linha, os comandos OpenGL não saberiam em qual janela desenhar.

---

# 5. Loop principal de renderização

## O que é o loop principal?

Aplicações gráficas geralmente ficam executando um ciclo repetidamente. Esse ciclo é chamado de **loop principal**, **loop de renderização** ou **render loop**.

No exemplo:

```python
while not glfw.window_should_close(window):
    atualizar_viewport(window)

    glClear(GL_COLOR_BUFFER_BIT)

    desenhar_triangulo()

    glfw.swap_buffers(window)
    glfw.poll_events()
```

Esse loop continua rodando enquanto a janela não for fechada.

Cada repetição desse loop representa um novo ciclo de atualização da tela.

Em cada ciclo, o programa:

1. atualiza a área de desenho;
2. limpa a tela;
3. desenha o triângulo, se existir;
4. troca os buffers;
5. processa eventos de teclado, mouse e janela.

---

# 6. Verificação se a janela deve fechar

```python
while not glfw.window_should_close(window):
```

Essa linha pergunta ao GLFW se a janela deve ser fechada.

A função:

```python
glfw.window_should_close(window)
```

retorna `True` quando o usuário tenta fechar a janela, por exemplo, clicando no botão de fechar.

Enquanto ela retornar `False`, o programa continua rodando.

---

# 7. Limpeza da tela

## Por que limpar a tela?

Antes de desenhar um novo quadro, é comum limpar a tela. Isso evita que desenhos antigos fiquem acumulados.

No exemplo, a limpeza acontece com:

```python
glClear(GL_COLOR_BUFFER_BIT)
```

Esse comando limpa o buffer de cor, ou seja, a área onde as cores dos pixels são armazenadas.

A cor usada para limpar a tela foi definida antes com:

```python
glClearColor(0.1, 0.1, 0.1, 1.0)
```

Essa função define a cor de fundo da janela.

Os valores seguem o padrão RGBA:

```python
glClearColor(vermelho, verde, azul, alpha)
```

No exemplo:

```python
glClearColor(0.1, 0.1, 0.1, 1.0)
```

significa:

- vermelho: `0.1`;
- verde: `0.1`;
- azul: `0.1`;
- transparência/alpha: `1.0`.

Como os valores de vermelho, verde e azul são iguais e baixos, o fundo fica em um tom de cinza escuro.

---

# 8. Sistema de coordenadas da janela

## Como o mouse usa coordenadas?

Quando o usuário clica na janela, o GLFW informa a posição do mouse em coordenadas da janela.

Essas coordenadas normalmente funcionam assim:

- o canto superior esquerdo da janela é `(0, 0)`;
- o eixo `x` cresce para a direita;
- o eixo `y` cresce para baixo.

Por exemplo, em uma janela de 800x600:

| Posição na janela | Coordenada aproximada |
|---|---:|
| canto superior esquerdo | `(0, 0)` |
| canto superior direito | `(800, 0)` |
| canto inferior esquerdo | `(0, 600)` |
| canto inferior direito | `(800, 600)` |
| centro da tela | `(400, 300)` |

Essa é a forma comum de coordenadas em janelas gráficas.

---

# 9. Sistema de coordenadas do OpenGL

## Como o OpenGL usa coordenadas neste exemplo?

Neste exemplo, o OpenGL está usando coordenadas normalizadas, aproximadamente entre `-1` e `1`.

O sistema funciona assim:

- o centro da janela é `(0, 0)`;
- o lado esquerdo da janela é `x = -1`;
- o lado direito da janela é `x = 1`;
- a parte inferior da janela é `y = -1`;
- a parte superior da janela é `y = 1`.

Ou seja:

| Posição na tela | Coordenada OpenGL |
|---|---:|
| centro | `(0, 0)` |
| canto superior esquerdo | `(-1, 1)` |
| canto superior direito | `(1, 1)` |
| canto inferior esquerdo | `(-1, -1)` |
| canto inferior direito | `(1, -1)` |

Esse sistema é diferente do sistema de coordenadas do mouse.

Por isso, não é possível usar diretamente a posição retornada pelo mouse para desenhar no OpenGL.

Se o mouse retorna, por exemplo:

```python
x_mouse = 400
y_mouse = 300
```

isso representa o centro da janela em coordenadas de tela. Mas, para o OpenGL, o centro é:

```python
x = 0
y = 0
```

Por isso é necessário fazer uma conversão.

---

# 10. Conversão de coordenadas do mouse para coordenadas OpenGL

A função responsável por isso é:

```python
def converter_para_opengl(x_mouse, y_mouse, largura, altura):
    x = (x_mouse / largura) * 2 - 1
    y = 1 - (y_mouse / altura) * 2
    return x, y
```

Essa é uma das partes mais importantes do exemplo.

Ela converte a posição do clique, dada em pixels, para coordenadas OpenGL.

## Conversão do eixo X

```python
x = (x_mouse / largura) * 2 - 1
```

Essa fórmula converte o intervalo de pixels da janela para o intervalo usado pelo OpenGL.

A posição horizontal do mouse varia de:

```text
0 até largura
```

Mas, no OpenGL, a posição horizontal varia de:

```text
-1 até 1
```

Exemplo com uma janela de largura 800:

### Clique no lado esquerdo

```python
x_mouse = 0
```

```python
x = (0 / 800) * 2 - 1
x = 0 * 2 - 1
x = -1
```

O lado esquerdo da janela vira `-1` no OpenGL.

### Clique no centro

```python
x_mouse = 400
```

```python
x = (400 / 800) * 2 - 1
x = 0.5 * 2 - 1
x = 1 - 1
x = 0
```

O centro da janela vira `0`.

### Clique no lado direito

```python
x_mouse = 800
```

```python
x = (800 / 800) * 2 - 1
x = 1 * 2 - 1
x = 1
```

O lado direito da janela vira `1`.

Portanto, a fórmula converte:

```text
0 até largura
```

para:

```text
-1 até 1
```

## Conversão do eixo Y

```python
y = 1 - (y_mouse / altura) * 2
```

O eixo Y precisa de um cuidado especial.

Na janela, o eixo Y cresce para baixo:

```text
topo = 0
baixo = altura
```

No OpenGL, o eixo Y cresce para cima:

```text
baixo = -1
topo = 1
```

Por isso a fórmula do Y é invertida.

Exemplo com uma janela de altura 600:

### Clique no topo

```python
y_mouse = 0
```

```python
y = 1 - (0 / 600) * 2
y = 1 - 0
y = 1
```

O topo vira `1` no OpenGL.

### Clique no centro

```python
y_mouse = 300
```

```python
y = 1 - (300 / 600) * 2
y = 1 - 0.5 * 2
y = 1 - 1
y = 0
```

O centro vira `0`.

### Clique embaixo

```python
y_mouse = 600
```

```python
y = 1 - (600 / 600) * 2
y = 1 - 2
y = -1
```

A parte inferior vira `-1`.

Essa inversão é essencial. Sem ela, o triângulo apareceria espelhado verticalmente em relação ao clique.

---

# 11. Captura da posição do mouse

Quando o usuário clica, o programa captura a posição do mouse com:

```python
x_mouse, y_mouse = glfw.get_cursor_pos(window)
```

Essa função retorna a posição atual do cursor dentro da janela.

Depois, o programa obtém o tamanho atual da janela:

```python
largura, altura = glfw.get_window_size(window)
```

Isso é necessário porque a conversão depende da largura e da altura da janela.

Em seguida, a posição do mouse é convertida:

```python
x, y = converter_para_opengl(x_mouse, y_mouse, largura, altura)
```

Depois dessa linha, `x` e `y` já estão no sistema de coordenadas usado pelo OpenGL.

---

# 12. Eventos de mouse

## O que é um evento?

Um evento é uma ação realizada pelo usuário ou pelo sistema. Por exemplo:

- clicar com o mouse;
- mover o mouse;
- pressionar uma tecla;
- fechar a janela;
- redimensionar a janela.

No exemplo, o evento mais importante é o clique do mouse.

---

# 13. Callback de mouse

Um **callback** é uma função que será chamada automaticamente quando determinado evento acontecer.

No exemplo, esta função é o callback de mouse:

```python
def clique_mouse(window, button, action, mods):
    global triangulo

    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        x_mouse, y_mouse = glfw.get_cursor_pos(window)
        largura, altura = glfw.get_window_size(window)

        x, y = converter_para_opengl(x_mouse, y_mouse, largura, altura)

        triangulo = criar_triangulo(x, y)
```

Essa função não é chamada diretamente pelo programador.

Ela é registrada com:

```python
glfw.set_mouse_button_callback(window, clique_mouse)
```

A partir desse momento, sempre que o usuário clicar com o mouse na janela, o GLFW chama automaticamente a função `clique_mouse`.

---

# 14. Parâmetros do callback de mouse

A função callback recebe estes parâmetros:

```python
def clique_mouse(window, button, action, mods):
```

## `window`

Representa a janela onde o evento aconteceu.

No exemplo, é usado para obter:

```python
glfw.get_cursor_pos(window)
glfw.get_window_size(window)
```

Ou seja, permite saber a posição do cursor e o tamanho da janela.

## `button`

Indica qual botão do mouse foi usado.

No exemplo:

```python
button == glfw.MOUSE_BUTTON_LEFT
```

Essa verificação garante que o triângulo só será criado quando o usuário clicar com o botão esquerdo do mouse.

Se o usuário clicar com o botão direito ou com o botão do meio, nada acontece.

## `action`

Indica a ação realizada com o botão.

No exemplo:

```python
action == glfw.PRESS
```

Isso significa que o triângulo será criado quando o botão for pressionado.

Um clique de mouse pode gerar diferentes ações, por exemplo:

- pressionar o botão;
- soltar o botão.

Se o programa não verificasse `glfw.PRESS`, ele poderia criar ou atualizar o triângulo também quando o botão fosse solto.

## `mods`

Representa teclas modificadoras pressionadas junto com o clique, como:

- Shift;
- Ctrl;
- Alt.

No exemplo, esse parâmetro não é usado, mas ele precisa aparecer na assinatura da função porque o GLFW espera que o callback tenha esse formato.

---

# 15. Variável global para armazenar o triângulo

No exemplo, existe esta variável:

```python
triangulo = None
```

Ela começa com valor `None`, indicando que ainda não existe triângulo para desenhar.

Depois que o usuário clica, essa variável recebe uma lista com os três vértices do triângulo:

```python
triangulo = criar_triangulo(x, y)
```

A palavra-chave `global` aparece dentro da função de clique:

```python
global triangulo
```

Isso permite modificar a variável `triangulo` que foi declarada fora da função.

Sem `global`, o Python entenderia que `triangulo` dentro da função é uma nova variável local, e o triângulo não seria atualizado para a função de desenho.

---

# 16. Estado da aplicação

O programa precisa lembrar se existe ou não um triângulo para desenhar.

Esse estado é armazenado na variável:

```python
triangulo = None
```

Antes do clique:

```python
triangulo = None
```

Depois do clique:

```python
triangulo = [
    (x, y),
    (x - largura, y - altura),
    (x + largura, y - altura)
]
```

Ou seja, o clique altera o estado da aplicação.

O loop principal desenha com base nesse estado.

Esse é um conceito importante em programas gráficos: geralmente existe um estado que representa o que deve aparecer na tela.

---

# 17. Criação do triângulo

O triângulo é criado nesta função:

```python
def criar_triangulo(x, y):
    largura = 0.25
    altura = 0.30

    return [
        (x, y),
        (x - largura, y - altura),
        (x + largura, y - altura)
    ]
```

Essa função recebe o ponto `(x, y)` do clique já convertido para coordenadas OpenGL.

Ela cria três vértices:

```python
(x, y)
```

Esse é o primeiro vértice. Ele fica exatamente no ponto clicado.

```python
(x - largura, y - altura)
```

Esse é o segundo vértice. Ele fica abaixo e à esquerda do ponto clicado.

```python
(x + largura, y - altura)
```

Esse é o terceiro vértice. Ele fica abaixo e à direita do ponto clicado.

Assim, o triângulo fica com o primeiro vértice no clique e a base abaixo dele.

## Exemplo prático

Se o usuário clicar no centro da janela, a conversão gera aproximadamente:

```python
x = 0
y = 0
```

A função cria:

```python
[
    (0, 0),
    (-0.25, -0.30),
    (0.25, -0.30)
]
```

Ou seja:

- o vértice superior fica no centro;
- o vértice inferior esquerdo fica um pouco à esquerda e abaixo;
- o vértice inferior direito fica um pouco à direita e abaixo.

Visualmente:

```text
       clique
         *
        / \
       /   \
      *-----*
```

---

# 18. Diferença entre usar o clique como centro e usar o clique como vértice

Esse foi o problema da primeira versão do código.

Antes, a função fazia algo como:

```python
return [
    (x, y + tamanho),
    (x - tamanho, y - tamanho),
    (x + tamanho, y - tamanho)
]
```

Nesse caso, o ponto `(x, y)` não era um vértice do triângulo. Ele era uma referência aproximada para montar o triângulo em volta daquele ponto.

Por isso, o triângulo aparecia próximo ao clique, mas não exatamente “a partir” do clique.

Na versão corrigida:

```python
return [
    (x, y),
    (x - largura, y - altura),
    (x + largura, y - altura)
]
```

Agora o ponto clicado é literalmente o primeiro vértice do triângulo.

Portanto, o triângulo passa a nascer a partir do clique.

---

# 19. Vértices

## O que é um vértice?

Um vértice é um ponto usado para formar uma figura geométrica.

Um triângulo precisa de três vértices.

No exemplo:

```python
(x, y)
(x - largura, y - altura)
(x + largura, y - altura)
```

Esses três pontos formam o triângulo.

No OpenGL, as figuras são desenhadas a partir de vértices. Quando dizemos ao OpenGL que queremos desenhar um triângulo, precisamos informar três pontos.

---

# 20. Primitiva `GL_TRIANGLES`

## O que é uma primitiva?

Uma primitiva é um tipo básico de desenho que o OpenGL consegue renderizar.

Algumas primitivas comuns são:

- pontos;
- linhas;
- triângulos.

No exemplo, usamos:

```python
glBegin(GL_TRIANGLES)
```

Isso informa ao OpenGL:

> os próximos vértices enviados formarão triângulos.

Depois, cada grupo de três vértices forma um triângulo.

Como o programa envia exatamente três vértices, apenas um triângulo é desenhado.

--

# 21. Função `glVertex2f`

## Para que serve?

A função:

```python
glVertex2f(x, y)
```

envia um vértice 2D para o OpenGL.

O `2f` significa:

- `2`: dois valores, `x` e `y`;
- `f`: valores do tipo float.

No exemplo:

```python
glVertex2f(triangulo[0][0], triangulo[0][1])
```

Essa linha desenha o primeiro vértice do triângulo.

A lista `triangulo` possui este formato:

```python
[
    (x1, y1),
    (x2, y2),
    (x3, y3)
]
```

Então:

```python
triangulo[0]
```

é o primeiro vértice.

```python
triangulo[0][0]
```

é o valor de `x` do primeiro vértice.

```python
triangulo[0][1]
```

é o valor de `y` do primeiro vértice.

---

# 22. Função `glColor3f`

## Para que serve?

A função:

```python
glColor3f(r, g, b)
```

define a cor do próximo vértice ou dos próximos desenhos.

Ela recebe três valores:

- `r`: vermelho;
- `g`: verde;
- `b`: azul.

Cada valor vai de `0.0` até `1.0`.

No exemplo:

```python
glColor3f(1.0, 0.0, 0.0)
```

define a cor vermelha.

```python
glColor3f(0.0, 1.0, 0.0)
```

define a cor verde.

```python
glColor3f(0.0, 0.0, 1.0)
```

define a cor azul.

Como cada vértice recebe uma cor diferente, o OpenGL interpola as cores entre os vértices, gerando um degradê no triângulo.

---

# 23. Função de desenho do triângulo

A função de desenho é:

```python
def desenhar_triangulo():
    if triangulo is None:
        return

    glBegin(GL_TRIANGLES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(triangulo[0][0], triangulo[0][1])

    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(triangulo[1][0], triangulo[1][1])

    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(triangulo[2][0], triangulo[2][1])

    glEnd()
```

A primeira verificação é:

```python
if triangulo is None:
    return
```

Isso significa:

> se ainda não existe triângulo, não desenhe nada.

No início do programa, o usuário ainda não clicou. Portanto:

```python
triangulo = None
```

Nesse momento, a função `desenhar_triangulo()` não faz nada.

Depois que o usuário clica, `triangulo` recebe os três vértices, e a função passa a desenhar a figura.

---

# 24. Viewport

## O que é viewport?

O viewport define a região da janela onde o OpenGL desenha.

No exemplo:

```python
def atualizar_viewport(window):
    largura, altura = glfw.get_framebuffer_size(window)
    glViewport(0, 0, largura, altura)
```

A função:

```python
glViewport(0, 0, largura, altura)
```

diz ao OpenGL que ele deve desenhar usando toda a área disponível da janela.

Os parâmetros são:

```python
glViewport(x, y, largura, altura)
```

No exemplo:

```python
glViewport(0, 0, largura, altura)
```

significa:

- começa no ponto `(0, 0)`;
- usa toda a largura;
- usa toda a altura.

## Por que usar `get_framebuffer_size`?

```python
largura, altura = glfw.get_framebuffer_size(window)
```

Em algumas telas, principalmente telas de alta densidade de pixels, o tamanho da janela e o tamanho real do framebuffer podem ser diferentes.

Por exemplo:

- janela lógica: `800 x 600`;
- framebuffer real: `1600 x 1200`.

Isso pode acontecer em telas com escala de pixels, como telas Retina ou HiDPI.

Usar `glfw.get_framebuffer_size(window)` ajuda a configurar corretamente o espaço real de desenho do OpenGL.

---

# 25. Diferença entre `get_window_size` e `get_framebuffer_size`

No exemplo, aparecem duas funções parecidas:

```python
glfw.get_window_size(window)
```

e:

```python
glfw.get_framebuffer_size(window)
```

Elas não são exatamente a mesma coisa.

## `get_window_size`

Retorna o tamanho da janela em coordenadas de tela.

No exemplo, é usado para converter a posição do mouse:

```python
largura, altura = glfw.get_window_size(window)
```

Isso faz sentido porque a posição do mouse também vem em coordenadas da janela.

## `get_framebuffer_size`

Retorna o tamanho real do buffer onde o OpenGL desenha.

No exemplo, é usado para configurar o viewport:

```python
largura, altura = glfw.get_framebuffer_size(window)
glViewport(0, 0, largura, altura)
```

Isso faz sentido porque o OpenGL desenha no framebuffer.

---

# 26. Double buffering

## O que é double buffering?

O OpenGL geralmente usa dois buffers:

- um buffer visível, que o usuário está vendo;
- um buffer oculto, onde o próximo quadro está sendo desenhado.

Quando o desenho do quadro termina, os buffers são trocados.

Isso evita que o usuário veja a imagem sendo desenhada aos poucos.

No código:

```python
glfw.swap_buffers(window)
```

Esse comando faz a troca dos buffers.

Em termos simples:

> o programa desenha no buffer oculto e, quando termina, mostra esse buffer na tela.

Isso deixa a renderização mais suave.

---

# 27. Processamento de eventos

No final do loop principal, aparece:

```python
glfw.poll_events()
```

Essa função processa os eventos pendentes da janela.

Entre esses eventos estão:

- clique do mouse;
- movimento do mouse;
- teclado;
- tentativa de fechar a janela;
- redimensionamento da janela.

Sem essa função, o programa não responderia corretamente às ações do usuário.

O clique do mouse só chega ao callback porque o programa chama `glfw.poll_events()` repetidamente.
