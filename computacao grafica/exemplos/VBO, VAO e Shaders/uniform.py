import ctypes
import glfw
import numpy as np
from OpenGL.GL import *

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

FRAGMENT_SHADER_SOURCE = """
#version 330 core

in vec3 vColor;
out vec4 FragColor;

uniform float brightness;

void main()
{
    FragColor = vec4(vColor * brightness, 1.0);
}
"""

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    success = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not success:
        error_message = glGetShaderInfoLog(shader).decode()
        shader_name = "VERTEX" if shader_type == GL_VERTEX_SHADER else "FRAGMENT"
        raise RuntimeError(f"Erro ao compilar {shader_name} SHADER:\n{error_message}")

    return shader

def create_shader_program():
    vertex_shader = compile_shader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER)

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    success = glGetProgramiv(shader_program, GL_LINK_STATUS)
    if not success:
        error_message = glGetProgramInfoLog(shader_program).decode()
        raise RuntimeError(f"Erro ao linkar o programa de shader:\n{error_message}")

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program

def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)

def init():
    vertices = np.array([
         0.0,  0.5, 0.0,       1.0, 0.0, 0.0,
        -0.5, -0.5, 0.0,       0.0, 1.0, 0.0,
         0.5, -0.5, 0.0,       0.0, 0.0, 1.0
    ], dtype=np.float32)

    shader_program = create_shader_program()

    brightness_loc = glGetUniformLocation(shader_program, "brightness")

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(
        0,
        3,
        GL_FLOAT,
        GL_FALSE,
        6 * 4,
        ctypes.c_void_p(0)
    )
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(
        1,
        3,
        GL_FLOAT,
        GL_FALSE,
        6 * 4,
        ctypes.c_void_p(3 * 4)
    )
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return shader_program, VAO, VBO, brightness_loc

def render(shader_program, VAO, brightness_loc, brightness_value):
    glClearColor(0.1, 0.1, 0.15, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader_program)
    glUniform1f(brightness_loc, brightness_value)
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

    shader_program, VAO, VBO, brightness_loc = init()

    while not glfw.window_should_close(window):
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        brightness_value = (np.sin(glfw.get_time() + 1.0) / 2.0)

        render(shader_program, VAO, brightness_loc, brightness_value)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteProgram(shader_program)

    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    main()