import glfw
import numpy as np
from OpenGL.GL import *


vertex_shader_source = """
#version 330 core

layout (location = 0) in vec2 aPos;

void main()
{
    gl_Position = vec4(aPos.x, aPos.y, 0.0, 1.0);
}
"""


fragment_shader_source = """
#version 330 core

out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0, 0.4, 0.0, 1.0);
}
"""


def compilar_shader(codigo_fonte, tipo_shader):
    shader = glCreateShader(tipo_shader)
    glShaderSource(shader, codigo_fonte)
    glCompileShader(shader)

    sucesso = glGetShaderiv(shader, GL_COMPILE_STATUS)

    if not sucesso:
        erro = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"Erro ao compilar shader: {erro}")

    return shader


def criar_programa_shader(vertex_source, fragment_source):
    vertex_shader = compilar_shader(vertex_source, GL_VERTEX_SHADER)
    fragment_shader = compilar_shader(fragment_source, GL_FRAGMENT_SHADER)

    programa = glCreateProgram()
    glAttachShader(programa, vertex_shader)
    glAttachShader(programa, fragment_shader)
    glLinkProgram(programa)

    sucesso = glGetProgramiv(programa, GL_LINK_STATUS)

    if not sucesso:
        erro = glGetProgramInfoLog(programa).decode()
        raise RuntimeError(f"Erro ao linkar programa: {erro}")

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return programa


def criar_janela():
    if not glfw.init():
        print("Erro ao inicializar GLFW")
        return None

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "Primeiro Triângulo Moderno", None, None)

    if not window:
        glfw.terminate()
        print("Erro ao criar a janela")
        return None

    glfw.make_context_current(window)
    return window


def main():
    window = criar_janela()

    if window is None:
        return

    vertices = np.array([
        -0.5, -0.5,
         0.5, -0.5,
         0.0,  0.5
    ], dtype=np.float32)

    programa_shader = criar_programa_shader(
        vertex_shader_source,
        fragment_shader_source
    )

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(
        0,
        2,
        GL_FLOAT,
        GL_FALSE,
        2 * vertices.itemsize,
        None
    )
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    glClearColor(0.1, 0.1, 0.1, 1.0)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(programa_shader)
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteVertexArrays(1, [vao])
    glDeleteBuffers(1, [vbo])
    glDeleteProgram(programa_shader)

    glfw.terminate()


if __name__ == "__main__":
    main()