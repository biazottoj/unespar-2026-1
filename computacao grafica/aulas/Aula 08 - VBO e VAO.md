# Walkthrough — VBO e VAO com OpenGL em Python

## Objetivo deste material

Neste walkthrough, você vai aprender o básico do **OpenGL moderno** usando:

- **Python**
- **GLFW**
- **PyOpenGL**
- **NumPy**

Ao final, você deverá ser capaz de explicar:

- o que é um **VBO**;
- o que é um **VAO**;
- o que faz um **vertex shader**;
- o que faz um **fragment shader**;
- como desenhar um triângulo usando OpenGL moderno.

---

# 1. O que vamos construir

Vamos implementar um programa que:

1. cria uma janela com GLFW;
2. cria um triângulo;
3. envia os dados dos vértices para a GPU;
4. usa um **VBO** para armazenar os dados;
5. usa um **VAO** para descrever como esses dados devem ser lidos;
6. usa um **vertex shader** e um **fragment shader**;
7. desenha o triângulo colorido na tela.

---

# 2. O que é VBO?

**VBO** significa **Vertex Buffer Object**.

Ele é um buffer usado para armazenar, na GPU, os dados dos vértices.

Esses dados podem incluir:

- posição;
- cor;
- normal;
- coordenadas de textura.

Neste exemplo, cada vértice terá:

- **posição**: `(x, y, z)`
- **cor**: `(r, g, b)`

## Ideia simples
O VBO é o lugar onde os dados brutos dos vértices ficam guardados.

---

# 3. O que é VAO?

**VAO** significa **Vertex Array Object**.

Ele guarda a configuração que diz ao OpenGL:

- quantos atributos cada vértice possui;
- onde começa cada atributo;
- qual é o tamanho de cada atributo;
- qual buffer está sendo usado como fonte dos dados.

## Ideia simples
O VAO guarda **a forma como esses dados devem ser interpretados**.

---

# 4. O que é o vertex shader?

O **vertex shader** é um programa executado para **cada vértice**.

Ele recebe como entrada os atributos do vértice, como:
- posição;
- cor.

Depois disso, ele produz:
- a posição final do vértice;
- outros dados que serão passados para a próxima etapa.

Neste exemplo, ele vai:
- receber posição e cor;
- enviar a posição para `gl_Position`;
- repassar a cor para o fragment shader.

---

# 5. O que é o fragment shader?

O **fragment shader** é executado para cada fragmento gerado depois da rasterização.

Na prática, ele ajuda a definir a **cor final** dos pixels desenhados.

Neste exemplo, ele vai:
- receber a cor interpolada do triângulo;
- devolver essa cor como saída final.

---

# 6. Estrutura geral do programa

Nosso programa terá estas etapas:

1. importar bibliotecas;
2. criar a janela;
3. definir os shaders;
4. compilar os shaders;
5. criar o programa de shader;
6. criar os dados do triângulo;
7. criar e configurar VBO e VAO;
8. entrar no loop principal;
9. desenhar o triângulo;
10. encerrar o programa.

---

# 7. Instalação das bibliotecas

Antes de rodar o exemplo, instale:

```bash
pip install glfw PyOpenGL numpy
```

---

# 8. Código completo

```python
import ctypes
import glfw
import numpy as np
from OpenGL.GL import *

vertex_shader_source = """
#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aColor;

out vec3 vColor;

void main()
{
    gl_Position = vec4(aPos, 1.0);
    vColor = aColor;
}
"""

fragment_shader_source = """
#version 330 core
in vec3 vColor;
out vec4 FragColor;

void main()
{
    FragColor = vec4(vColor, 1.0);
}
"""

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    success = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not success:
        info = glGetShaderInfoLog(shader).decode()
        raise Exception(f"Erro de compilação do shader:\n{info}")

    return shader

if not glfw.init():
    raise Exception("Falha ao inicializar o GLFW")

window = glfw.create_window(800, 600, "Exemplo VBO e VAO", None, None)
if not window:
    glfw.terminate()
    raise Exception("Falha ao criar a janela")

glfw.make_context_current(window)

vertices = np.array([
     0.0,  0.5, 0.0,   1.0, 0.0, 0.0,
    -0.5, -0.5, 0.0,   0.0, 1.0, 0.0,
     0.5, -0.5, 0.0,   0.0, 0.0, 1.0,
], dtype=np.float32)

vertex_shader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
fragment_shader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)

shader_program = glCreateProgram()
glAttachShader(shader_program, vertex_shader)
glAttachShader(shader_program, fragment_shader)
glLinkProgram(shader_program)

success = glGetProgramiv(shader_program, GL_LINK_STATUS)
if not success:
    info = glGetProgramInfoLog(shader_program).decode()
    raise Exception(f"Erro de linkedição do programa:\n{info}")

glDeleteShader(vertex_shader)
glDeleteShader(fragment_shader)

VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)

glBindVertexArray(VAO)

glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))
glEnableVertexAttribArray(1)

glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

while not glfw.window_should_close(window):
    glClearColor(0.1, 0.1, 0.15, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader_program)
    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, 3)

    glfw.swap_buffers(window)
    glfw.poll_events()

glDeleteVertexArrays(1, [VAO])
glDeleteBuffers(1, [VBO])
glDeleteProgram(shader_program)
glfw.terminate()
```

---

# 9. Explicação passo a passo

## 9.1 Imports

```python
import ctypes
import glfw
import numpy as np
from OpenGL.GL import *
```

### O que cada um faz
- `ctypes`: ajuda a informar offsets de memória;
- `glfw`: cria a janela e o loop;
- `numpy`: organiza os dados dos vértices;
- `OpenGL.GL`: fornece as funções do OpenGL.

---

## 9.2 Código-fonte do vertex shader

```python
vertex_shader_source = """
#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aColor;

out vec3 vColor;

void main()
{
    gl_Position = vec4(aPos, 1.0);
    vColor = aColor;
}
"""
```

### O que esse shader faz
- `layout(location = 0) in vec3 aPos;`  
  recebe a posição do vértice;

- `layout(location = 1) in vec3 aColor;`  
  recebe a cor do vértice;

- `out vec3 vColor;`  
  declara uma saída que será enviada ao fragment shader;

- `gl_Position = vec4(aPos, 1.0);`  
  define a posição final do vértice;

- `vColor = aColor;`  
  repassa a cor para a próxima etapa.

---

## 9.3 Código-fonte do fragment shader

```python
fragment_shader_source = """
#version 330 core
in vec3 vColor;
out vec4 FragColor;

void main()
{
    FragColor = vec4(vColor, 1.0);
}
"""
```

### O que esse shader faz
- recebe `vColor` do vertex shader;
- transforma essa cor em um `vec4`;
- escreve a cor final em `FragColor`.

### Resultado
O triângulo será desenhado com interpolação de cor entre os vértices.

---

## 9.4 Função para compilar shader

```python
def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    success = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not success:
        info = glGetShaderInfoLog(shader).decode()
        raise Exception(f"Erro de compilação do shader:\n{info}")

    return shader
```

### O que ela faz
Essa função:
1. cria um shader;
2. envia o código-fonte;
3. compila;
4. verifica se houve erro.

### Por que isso é importante
Se o shader tiver erro, o programa não conseguirá desenhar corretamente.

---

## 9.5 Inicialização do GLFW

```python
if not glfw.init():
    raise Exception("Falha ao inicializar o GLFW")
```

### O que faz
Inicializa o GLFW.

### Por que isso é necessário
Sem isso, não conseguimos criar a janela.

---

## 9.6 Criação da janela

```python
window = glfw.create_window(800, 600, "Exemplo VBO e VAO", None, None)
if not window:
    glfw.terminate()
    raise Exception("Falha ao criar a janela")
```

### O que faz
Cria uma janela de 800x600 com um contexto OpenGL.

---

## 9.7 Tornar o contexto atual

```python
glfw.make_context_current(window)
```

### O que faz
Define a janela criada como contexto atual do OpenGL.

### Por que isso é necessário
Sem contexto atual, o OpenGL não sabe onde desenhar.

---

## 9.8 Definição dos vértices

```python
vertices = np.array([
     0.0,  0.5, 0.0,   1.0, 0.0, 0.0,
    -0.5, -0.5, 0.0,   0.0, 1.0, 0.0,
     0.5, -0.5, 0.0,   0.0, 0.0, 1.0,
], dtype=np.float32)
```

### Como ler esse array
Cada linha representa um vértice:

- 3 primeiros valores → posição
- 3 últimos valores → cor

### Vértice 1
- posição: `(0.0, 0.5, 0.0)`
- cor: vermelho `(1.0, 0.0, 0.0)`

### Vértice 2
- posição: `(-0.5, -0.5, 0.0)`
- cor: verde `(0.0, 1.0, 0.0)`

### Vértice 3
- posição: `(0.5, -0.5, 0.0)`
- cor: azul `(0.0, 0.0, 1.0)`

---

## 9.9 Compilação dos shaders

```python
vertex_shader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
fragment_shader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)
```

### O que faz
Compila o vertex shader e o fragment shader.

---

## 9.10 Criação do programa de shader

```python
shader_program = glCreateProgram()
glAttachShader(shader_program, vertex_shader)
glAttachShader(shader_program, fragment_shader)
glLinkProgram(shader_program)
```

### O que faz
- cria um programa;
- anexa os shaders;
- faz o link entre eles.

### Ideia importante
O programa de shader é o conjunto final que será usado pelo OpenGL na hora de desenhar.

---

## 9.11 Verificação do link

```python
success = glGetProgramiv(shader_program, GL_LINK_STATUS)
if not success:
    info = glGetProgramInfoLog(shader_program).decode()
    raise Exception(f"Erro de linkedição do programa:\n{info}")
```

### O que faz
Verifica se os shaders são compatíveis entre si e se o programa foi ligado corretamente.

---

## 9.12 Remoção dos shaders individuais

```python
glDeleteShader(vertex_shader)
glDeleteShader(fragment_shader)
```

### O que faz
Apaga os objetos de shader individuais após o link.

### Por que isso pode ser feito
Porque o programa já foi montado e agora eles não precisam mais existir separadamente.

---

## 9.13 Criação do VAO e VBO

```python
VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)
```

### O que isso faz
- cria 1 VAO;
- cria 1 VBO.

---

## 9.14 Bind do VAO

```python
glBindVertexArray(VAO)
```

### O que isso faz
Torna esse VAO o VAO atual.

### Por que isso importa
Tudo que for configurado agora em relação aos atributos ficará associado a esse VAO.

---

## 9.15 Bind do VBO e envio dos dados

```python
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
```

### O que isso faz
- liga o VBO ao alvo `GL_ARRAY_BUFFER`;
- copia os dados dos vértices para o buffer da GPU.

### Significado de `GL_STATIC_DRAW`
Indica que os dados serão enviados uma vez e usados várias vezes.

---

## 9.16 Configuração do atributo de posição

```python
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
```

### Interpretação dos parâmetros
- `0` → atributo da posição (`location = 0`);
- `3` → três componentes;
- `GL_FLOAT` → tipo float;
- `GL_FALSE` → sem normalização;
- `6 * 4` → stride de 24 bytes;
- `offset 0` → posição começa no início.

### O que isso significa
O OpenGL vai ler:
- 3 floats por vértice;
- começando no início de cada bloco de 6 floats.

---

## 9.17 Configuração do atributo de cor

```python
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))
glEnableVertexAttribArray(1)
```

### Interpretação
- `1` → atributo da cor (`location = 1`);
- `3` → três componentes;
- `6 * 4` → stride de 24 bytes;
- `offset 12 bytes` → começa após os 3 floats da posição.

### O que isso significa
O OpenGL vai buscar a cor a partir do quarto float de cada vértice.

---

## 9.18 Desfazer binds

```python
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)
```

### O que isso faz
Desativa o VBO e o VAO ativos.

### Por que isso é útil
Ajuda a evitar alterações acidentais depois.

---

# 10. Loop principal

```python
while not glfw.window_should_close(window):
    glClearColor(0.1, 0.1, 0.15, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader_program)
    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, 3)

    glfw.swap_buffers(window)
    glfw.poll_events()
```

## Explicação passo a passo

### `glClearColor(...)`
Define a cor de fundo.

### `glClear(GL_COLOR_BUFFER_BIT)`
Limpa a tela com essa cor.

### `glUseProgram(shader_program)`
Ativa o programa de shader.

### `glBindVertexArray(VAO)`
Ativa o VAO que contém a configuração dos atributos.

### `glDrawArrays(GL_TRIANGLES, 0, 3)`
Desenha 3 vértices como um triângulo.

### `glfw.swap_buffers(window)`
Exibe a imagem na tela.

### `glfw.poll_events()`
Processa os eventos da janela.

---

# 11. Encerramento

```python
glDeleteVertexArrays(1, [VAO])
glDeleteBuffers(1, [VBO])
glDeleteProgram(shader_program)
glfw.terminate()
```

### O que isso faz
Libera os recursos usados e encerra o GLFW.

---

# 12. O que o aluno deve guardar desse exemplo

## VBO
Guarda os dados dos vértices.

## VAO
Guarda a configuração de como esses dados devem ser lidos.

## Vertex shader
Processa cada vértice.

## Fragment shader
Define a cor final dos fragmentos.

## `glVertexAttribPointer`
É a função que conecta os dados do VBO aos atributos esperados pelo shader.

---

# 13. Erros comuns

## 1. Esquecer de ativar o VAO antes da configuração
Sem o VAO correto ativo, a configuração pode não ficar onde você espera.

## 2. Errar stride ou offset
Se isso estiver errado:
- a cor pode aparecer incorreta;
- a posição pode ficar errada;
- o triângulo pode nem aparecer.

## 3. Não verificar erro de shader
Se o shader não compilar, o triângulo não será desenhado corretamente.

## 4. Esquecer `glUseProgram`
Sem isso, o programa de shader não será usado.

## 5. Usar formato de dados incompatível
O array precisa estar em `float32` para esse exemplo funcionar corretamente.

---

# 14. Exercícios sugeridos

## Exercício 1
Troque as cores dos vértices.

## Exercício 2
Mude a posição dos vértices para formar outro triângulo.

## Exercício 3
Faça os três vértices terem a mesma cor e observe o resultado.

## Exercício 4
Altere a cor de fundo da janela.

## Exercício 5
Adicione mais um triângulo usando outro VBO e outro VAO.

---

# 15. Conclusão

Este exemplo mostra o fluxo mínimo de OpenGL moderno para desenhar um triângulo com VBO e VAO.

A sequência essencial é:

1. criar a janela;
2. compilar shaders;
3. criar programa de shader;
4. criar VBO;
5. criar VAO;
6. configurar atributos;
7. desenhar com `glDrawArrays`.

Se você entendeu esse exemplo, já possui a base para estudar:

- EBO/índices;
- transformações;
- matrizes;
- texturas;
- múltiplos objetos;
- pipeline gráfico moderno.
