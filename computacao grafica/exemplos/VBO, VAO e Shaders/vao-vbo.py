import glfw
from OpenGL.GL import *
import numpy as np
import ctypes


# Shader que processa o VBO e calcula e posicao de cada vertice
VERTEX_SHADER_SOURCE = """
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

# Receber a cor de cada vertice (processada no VERTEX_SHADER) e cria uma cor para os fragmentos (i.e., pixels)
FRAGMENT_SHADER_SOURCE = """
#version 330 core

in vec3 vColor;
out vec4 FragColor;

void main()
{
    FragColor = vec4(vColor, 1.0);
}
"""

def compile_shader(shader_source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, shader_source)
    glCompileShader(shader)

    success = glGetShaderiv(shader, GL_COMPILE_STATUS)

    if not success:
        error_message = glGetShaderInfoLog(shader).decode()
        shader_name = "VERTEX" if shader_type == GL_VERTEX_SHADER else "FRAGMENT"
        raise RuntimeError(f"Erro ao compilar {shader} shader, ERRO: {error_message}")

    return shader

def create_shader_program():
    vertex_shader = compile_shader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER)

    shader_program = glCreateProgram()

    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    succees = glGetProgramiv(shader_program, GL_LINK_STATUS)

    if not succees:
        error_message = glGetProgramInfoLog(shader_program).decode()
        raise RuntimeError(f"Erro ao linkar o programa. ERRO: {error_message}")

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program      

def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


# Responsável por configuracoes iniciais
def init():
    vertices = np.array([
        0.0, 0.5, 0.0, 1.0, 0.0, 0.0,
        -0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
        0.5, -0.5, 0.0, 0.0, 0.0, 1.0
    ], dtype=np.float32)

    # Criar um buffer para salvar os vertices na GPU
    VBO = glGenBuffers(1)

    # Cria o VAO para guardar configuracoes sobre como renderizar os vetices
    VAO = glGenVertexArrays(1)

    # Indica para o OpenGL qual variavel contem as configuracoes para renderizar o buffer
    glBindVertexArray(VAO)

    # Informar ao OpenGL qual variavel representa o buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)

    # Enviar informacoes dos vertices para o OpenGL
    glBufferData(GL_ARRAY_BUFFER, 
                vertices.nbytes,
                vertices,
                GL_STATIC_DRAW)

    # Informar como a posicao de cada vertice no VBO deve ser interpretado
    glVertexAttribPointer(
        0,
        3,
        GL_FLOAT,
        GL_FALSE,
        6*4,
        ctypes.c_void_p(0)
    )
    glEnableVertexAttribArray(0)

    # Informar como a cor de cada vertice no VBO deve ser interpretado
    glVertexAttribPointer(
        1,
        3,
        GL_FLOAT,
        GL_FALSE,
        6*4,
        ctypes.c_void_p(1)
    )
    glEnableVertexAttribArray(1)

    shader_program = create_shader_program()

    glBindBuffer(GL_ARRAY_BUFFER,0)
    glBindVertexArray(0)

    return shader_program, VAO, VBO


# Renderizar as imagens
def render(shader_program, VAO):
    glClearColor(0.1, 0.1, 0.5, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader_program)
    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glBindVertexArray(0)


def main():
    if not glfw.init():
        raise RuntimeError("Falha ao inicializar o GLFW")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "Exemplo com init() e render()", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Falha ao criar a janela GLFW")

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    shader_program, VAO, VBO = init()

    while not glfw.window_should_close(window):
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        render(shader_program, VAO)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteProgram(shader_program)

    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    main()