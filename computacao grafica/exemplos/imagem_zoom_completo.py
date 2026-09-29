import ctypes
import sys

import glfw
import numpy as np
from OpenGL.GL import *


WIDTH = 1000
HEIGHT = 700

mode = 1


VERTEX_SHADER = """
#version 330 core

layout(location = 0) in vec2 aPos;
layout(location = 1) in vec3 aColor;

out vec3 vertexColor;

void main()
{
    gl_Position =
        vec4(
            aPos,
            0.0,
            1.0
        );

    vertexColor = aColor;
}
"""


FRAGMENT_SHADER = """
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
"""


def create_demo_image():
    return np.array([
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 1.0, 1.0],
        ],
        [
            [1.0, 0.5, 0.0],
            [0.5, 0.0, 1.0],
            [0.0, 1.0, 1.0],
            [0.0, 0.0, 0.0],
        ],
        [
            [1.0, 1.0, 0.0],
            [0.2, 0.8, 0.2],
            [0.2, 0.4, 1.0],
            [0.9, 0.9, 0.9],
        ],
        [
            [0.6, 0.2, 0.1],
            [0.9, 0.3, 0.6],
            [0.4, 0.4, 0.4],
            [1.0, 0.0, 0.0],
        ],
    ], dtype=np.float32)


def only_channel(image, channel_index):
    result = np.zeros_like(
        image
    )

    result[:, :, channel_index] = image[:, :, channel_index]

    return result


def zoom_in_quadrado(image, factor):
    zoomed = np.repeat(
        image,
        factor,
        axis=0
    )

    zoomed = np.repeat(
        zoomed,
        factor,
        axis=1
    )

    return zoomed


def zoom_in_linear(image, factor):
    height, width, channels = image.shape

    new_height = height * factor
    new_width = width * factor

    result = np.zeros(
        (new_height, new_width, channels),
        dtype=np.float32
    )

    for new_row in range(new_height):
        source_y = new_row / factor

        y0 = int(
            np.floor(source_y)
        )

        y1 = min(
            y0 + 1,
            height - 1
        )

        ty = source_y - y0

        for new_col in range(new_width):
            source_x = new_col / factor

            x0 = int(
                np.floor(source_x)
            )

            x1 = min(
                x0 + 1,
                width - 1
            )

            tx = source_x - x0

            top = (
                (1.0 - tx) * image[y0, x0] +
                tx * image[y0, x1]
            )

            bottom = (
                (1.0 - tx) * image[y1, x0] +
                tx * image[y1, x1]
            )

            result[new_row, new_col] = (
                (1.0 - ty) * top +
                ty * bottom
            )

    return result


def zoom_out_quadrado(image, factor):
    return image[::factor, ::factor]


def zoom_out_media(image, factor):
    height, width, channels = image.shape

    new_height = max(
        1,
        height // factor
    )

    new_width = max(
        1,
        width // factor
    )

    result = np.zeros(
        (new_height, new_width, channels),
        dtype=np.float32
    )

    for row in range(new_height):
        for col in range(new_width):
            block = image[
                row * factor:(row + 1) * factor,
                col * factor:(col + 1) * factor
            ]

            result[row, col] = block.mean(
                axis=(0, 1)
            )

    return result


def create_window():
    if not glfw.init():
        raise RuntimeError(
            "Nao foi possivel inicializar o GLFW."
        )

    glfw.window_hint(
        glfw.CONTEXT_VERSION_MAJOR,
        3
    )

    glfw.window_hint(
        glfw.CONTEXT_VERSION_MINOR,
        3
    )

    glfw.window_hint(
        glfw.OPENGL_PROFILE,
        glfw.OPENGL_CORE_PROFILE
    )

    glfw.window_hint(
        glfw.RESIZABLE,
        glfw.FALSE
    )

    if sys.platform == "darwin":
        glfw.window_hint(
            glfw.OPENGL_FORWARD_COMPAT,
            GL_TRUE
        )

    window = glfw.create_window(
        WIDTH,
        HEIGHT,
        "Imagem como Matriz e Zoom",
        None,
        None
    )

    if not window:
        glfw.terminate()

        raise RuntimeError(
            "Nao foi possivel criar a janela."
        )

    glfw.make_context_current(window)

    return window


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)

    glShaderSource(
        shader,
        source
    )

    glCompileShader(shader)

    success = glGetShaderiv(
        shader,
        GL_COMPILE_STATUS
    )

    if not success:
        error = glGetShaderInfoLog(
            shader
        ).decode()

        glDeleteShader(shader)

        raise RuntimeError(
            f"Erro ao compilar shader:\n{error}"
        )

    return shader


def create_shader_program():
    vertex_shader = compile_shader(
        VERTEX_SHADER,
        GL_VERTEX_SHADER
    )

    fragment_shader = compile_shader(
        FRAGMENT_SHADER,
        GL_FRAGMENT_SHADER
    )

    program = glCreateProgram()

    glAttachShader(
        program,
        vertex_shader
    )

    glAttachShader(
        program,
        fragment_shader
    )

    glLinkProgram(program)

    success = glGetProgramiv(
        program,
        GL_LINK_STATUS
    )

    if not success:
        error = glGetProgramInfoLog(
            program
        ).decode()

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        glDeleteProgram(program)

        raise RuntimeError(
            f"Erro ao linkar programa:\n{error}"
        )

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program


def add_cell(vertices, x0, y0, x1, y1, color):
    r, g, b = color

    vertices.extend([
        x0, y0, r, g, b,
        x1, y0, r, g, b,
        x1, y1, r, g, b,

        x0, y0, r, g, b,
        x1, y1, r, g, b,
        x0, y1, r, g, b,
    ])


def build_grid_vertices(
    image,
    center_x,
    center_y,
    cell_size,
    gap
):
    vertices = []

    height, width, _ = image.shape

    total_width = width * cell_size + (width - 1) * gap
    total_height = height * cell_size + (height - 1) * gap

    start_x = center_x - total_width / 2.0
    start_y = center_y + total_height / 2.0

    for row in range(height):
        for col in range(width):
            x0 = start_x + col * (cell_size + gap)
            y1 = start_y - row * (cell_size + gap)

            x1 = x0 + cell_size
            y0 = y1 - cell_size

            color = image[row, col]

            add_cell(
                vertices,
                x0,
                y0,
                x1,
                y1,
                color
            )

    return np.array(
        vertices,
        dtype=np.float32
    )


def build_scene_vertices(original_image):
    if mode == 1:
        return build_grid_vertices(
            original_image,
            center_x=0.0,
            center_y=0.0,
            cell_size=0.18,
            gap=0.01
        )

    if mode == 2:
        red = only_channel(
            original_image,
            0
        )

        green = only_channel(
            original_image,
            1
        )

        blue = only_channel(
            original_image,
            2
        )

        return np.concatenate([
            build_grid_vertices(
                red,
                center_x=-0.55,
                center_y=0.0,
                cell_size=0.12,
                gap=0.008
            ),
            build_grid_vertices(
                green,
                center_x=0.0,
                center_y=0.0,
                cell_size=0.12,
                gap=0.008
            ),
            build_grid_vertices(
                blue,
                center_x=0.55,
                center_y=0.0,
                cell_size=0.12,
                gap=0.008
            ),
        ])

    if mode == 3:
        image = zoom_in_quadrado(
            original_image,
            factor=2
        )

    elif mode == 4:
        image = zoom_in_linear(
            original_image,
            factor=2
        )

    elif mode == 5:
        image = zoom_out_quadrado(
            original_image,
            factor=2
        )

    elif mode == 6:
        image = zoom_out_media(
            original_image,
            factor=2
        )

    else:
        image = original_image

    cell_size = min(
        0.15,
        1.4 / max(
            image.shape[0],
            image.shape[1]
        )
    )

    return build_grid_vertices(
        image,
        center_x=0.0,
        center_y=0.0,
        cell_size=cell_size,
        gap=0.006
    )


def create_geometry(vertices):
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)

    glBindBuffer(
        GL_ARRAY_BUFFER,
        vbo
    )

    glBufferData(
        GL_ARRAY_BUFFER,
        vertices.nbytes,
        vertices,
        GL_DYNAMIC_DRAW
    )

    float_size = np.dtype(
        np.float32
    ).itemsize

    stride = 5 * float_size

    glVertexAttribPointer(
        0,
        2,
        GL_FLOAT,
        GL_FALSE,
        stride,
        ctypes.c_void_p(0)
    )

    glEnableVertexAttribArray(0)

    glVertexAttribPointer(
        1,
        3,
        GL_FLOAT,
        GL_FALSE,
        stride,
        ctypes.c_void_p(
            2 * float_size
        )
    )

    glEnableVertexAttribArray(1)

    glBindBuffer(
        GL_ARRAY_BUFFER,
        0
    )

    glBindVertexArray(0)

    return vao, vbo


def update_vbo(vbo, vertices):
    glBindBuffer(
        GL_ARRAY_BUFFER,
        vbo
    )

    glBufferData(
        GL_ARRAY_BUFFER,
        vertices.nbytes,
        vertices,
        GL_DYNAMIC_DRAW
    )

    glBindBuffer(
        GL_ARRAY_BUFFER,
        0
    )


def print_help():
    print()
    print("==============================================")
    print("Imagem como Matriz e Zoom")
    print("==============================================")
    print("1 -> imagem original")
    print("2 -> canais RGB")
    print("3 -> Zoom In quadrado")
    print("4 -> Zoom In linear")
    print("5 -> Zoom Out quadrado")
    print("6 -> Zoom Out por media")
    print("H -> ajuda")
    print("ESC -> sair")
    print()


def process_input(window):
    global mode

    if glfw.get_key(
        window,
        glfw.KEY_ESCAPE
    ) == glfw.PRESS:
        glfw.set_window_should_close(
            window,
            True
        )

    keys = [
        glfw.KEY_1,
        glfw.KEY_2,
        glfw.KEY_3,
        glfw.KEY_4,
        glfw.KEY_5,
        glfw.KEY_6,
    ]

    for index, key in enumerate(keys, start=1):
        if glfw.get_key(window, key) == glfw.PRESS:
            mode = index

    if glfw.get_key(window, glfw.KEY_H) == glfw.PRESS:
        print_help()


def main():
    window = create_window()

    program = create_shader_program()

    original_image = create_demo_image()

    vertices = build_scene_vertices(
        original_image
    )

    vao, vbo = create_geometry(
        vertices
    )

    glViewport(
        0,
        0,
        WIDTH,
        HEIGHT
    )

    print_help()

    while not glfw.window_should_close(
        window
    ):
        process_input(
            window
        )

        vertices = build_scene_vertices(
            original_image
        )

        update_vbo(
            vbo,
            vertices
        )

        glClearColor(
            0.08,
            0.08,
            0.10,
            1.0
        )

        glClear(
            GL_COLOR_BUFFER_BIT
        )

        glUseProgram(
            program
        )

        glBindVertexArray(
            vao
        )

        glDrawArrays(
            GL_TRIANGLES,
            0,
            len(vertices) // 5
        )

        glBindVertexArray(
            0
        )

        glfw.swap_buffers(
            window
        )

        glfw.poll_events()

    glDeleteVertexArrays(
        1,
        [vao]
    )

    glDeleteBuffers(
        1,
        [vbo]
    )

    glDeleteProgram(
        program
    )

    glfw.destroy_window(
        window
    )

    glfw.terminate()


if __name__ == "__main__":
    main()
