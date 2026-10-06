import ctypes
import sys

import glfw
import numpy as np
from OpenGL.GL import *


WIDTH = 1100
HEIGHT = 720

mode = 1

MODE_NAMES = {
    1: "Imagem original",
    2: "Linha y = x",
    3: "Inversao RGB/CMY",
    4: "Luminosidade Y",
    5: "HSV - componente V",
    6: "Histograma",
    7: "Equalizacao",
    8: "Comparacao",
}


VERTEX_SHADER = """
#version 330 core

layout(location = 0) in vec2 aPos;
layout(location = 1) in vec3 aColor;

out vec3 vertexColor;

void main()
{
    gl_Position = vec4(aPos, 0.0, 1.0);
    vertexColor = aColor;
}
"""


FRAGMENT_SHADER = """
#version 330 core

in vec3 vertexColor;

out vec4 FragColor;

void main()
{
    FragColor = vec4(vertexColor, 1.0);
}
"""


def create_demo_image():
    return np.array([
        [
            [0.10, 0.10, 0.10],
            [0.18, 0.12, 0.15],
            [0.28, 0.18, 0.12],
            [0.45, 0.25, 0.10],
            [0.70, 0.30, 0.10],
            [0.95, 0.45, 0.10],
            [1.00, 0.70, 0.20],
            [1.00, 0.90, 0.45],
        ],
        [
            [0.08, 0.12, 0.20],
            [0.12, 0.18, 0.32],
            [0.18, 0.28, 0.45],
            [0.25, 0.40, 0.60],
            [0.35, 0.55, 0.75],
            [0.50, 0.70, 0.90],
            [0.70, 0.85, 1.00],
            [0.90, 0.95, 1.00],
        ],
        [
            [0.05, 0.25, 0.10],
            [0.10, 0.38, 0.15],
            [0.20, 0.50, 0.20],
            [0.30, 0.62, 0.25],
            [0.40, 0.75, 0.35],
            [0.55, 0.85, 0.45],
            [0.75, 0.95, 0.65],
            [0.90, 1.00, 0.85],
        ],
        [
            [0.20, 0.05, 0.25],
            [0.30, 0.08, 0.38],
            [0.42, 0.10, 0.55],
            [0.55, 0.15, 0.70],
            [0.68, 0.25, 0.82],
            [0.80, 0.40, 0.90],
            [0.90, 0.60, 0.95],
            [1.00, 0.80, 1.00],
        ],
        [
            [0.05, 0.05, 0.05],
            [0.15, 0.15, 0.15],
            [0.25, 0.25, 0.25],
            [0.35, 0.35, 0.35],
            [0.50, 0.50, 0.50],
            [0.65, 0.65, 0.65],
            [0.80, 0.80, 0.80],
            [0.95, 0.95, 0.95],
        ],
        [
            [1.00, 0.00, 0.00],
            [0.80, 0.10, 0.10],
            [0.60, 0.20, 0.20],
            [0.40, 0.30, 0.30],
            [0.30, 0.40, 0.40],
            [0.20, 0.60, 0.60],
            [0.10, 0.80, 0.80],
            [0.00, 1.00, 1.00],
        ],
        [
            [0.00, 0.00, 1.00],
            [0.10, 0.10, 0.80],
            [0.20, 0.20, 0.60],
            [0.30, 0.30, 0.40],
            [0.40, 0.40, 0.30],
            [0.60, 0.60, 0.20],
            [0.80, 0.80, 0.10],
            [1.00, 1.00, 0.00],
        ],
        [
            [0.00, 0.00, 0.00],
            [0.20, 0.10, 0.00],
            [0.40, 0.20, 0.05],
            [0.60, 0.35, 0.10],
            [0.75, 0.50, 0.20],
            [0.85, 0.65, 0.35],
            [0.95, 0.80, 0.60],
            [1.00, 1.00, 1.00],
        ],
    ], dtype=np.float32)


def gray_to_rgb(gray):
    return np.stack(
        [gray, gray, gray],
        axis=2
    )


def draw_diagonal_line(image):
    result = image.copy()
    height, width, _ = result.shape

    limit = min(height, width)

    for index in range(limit):
        result[index, index] = [0.0, 0.0, 0.0]

    return result


def invert_rgb_to_cmy(image):
    return 1.0 - image


def rgb_to_luminance_y(image):
    r = image[:, :, 0]
    g = image[:, :, 1]
    b = image[:, :, 2]

    gray = (
        0.299 * r
        + 0.587 * g
        + 0.114 * b
    )

    return gray_to_rgb(gray)


def rgb_to_hsv_value(image):
    value = np.max(
        image,
        axis=2
    )

    return gray_to_rgb(value)


def to_gray(image):
    r = image[:, :, 0]
    g = image[:, :, 1]
    b = image[:, :, 2]

    return (
        0.299 * r
        + 0.587 * g
        + 0.114 * b
    )


def compute_histogram(gray, levels):
    hist = np.zeros(
        levels,
        dtype=np.float32
    )

    height, width = gray.shape

    for row in range(height):
        for col in range(width):
            value = np.clip(
                gray[row, col],
                0.0,
                1.0
            )

            level = int(
                value * (levels - 1)
            )

            hist[level] += 1.0

    return hist


def equalize_grayscale(gray, levels):
    hist = compute_histogram(
        gray,
        levels
    )

    total = hist.sum()

    if total == 0:
        return gray.copy()

    probability = hist / total
    cumulative = np.cumsum(probability)

    height, width = gray.shape

    result = np.zeros_like(
        gray,
        dtype=np.float32
    )

    for row in range(height):
        for col in range(width):
            value = np.clip(
                gray[row, col],
                0.0,
                1.0
            )

            old_level = int(
                value * (levels - 1)
            )

            result[row, col] = cumulative[old_level]

    return result


# ============================================================
# INFRAESTRUTURA OPENGL
# ============================================================

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
        "Histograma com Python/OpenGL",
        None,
        None
    )

    if not window:
        glfw.terminate()
        raise RuntimeError(
            "Nao foi possivel criar a janela."
        )

    glfw.make_context_current(window)
    glfw.set_key_callback(
        window,
        key_callback
    )

    update_window_title(window)

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
            f"Erro ao compilar shader:\\n{error}"
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
            f"Erro ao linkar programa:\\n{error}"
        )

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program


def add_rectangle(vertices, x0, y0, x1, y1, color):
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
    max_width,
    max_height,
    gap=0.006
):
    vertices = []

    height, width, _ = image.shape

    cell_size_x = (
        max_width - gap * max(0, width - 1)
    ) / width

    cell_size_y = (
        max_height - gap * max(0, height - 1)
    ) / height

    cell_size = max(
        0.001,
        min(
            cell_size_x,
            cell_size_y
        )
    )

    total_width = (
        width * cell_size
        + (width - 1) * gap
    )

    total_height = (
        height * cell_size
        + (height - 1) * gap
    )

    start_x = center_x - total_width / 2.0
    start_y = center_y + total_height / 2.0

    for row in range(height):
        for col in range(width):
            x0 = (
                start_x
                + col * (cell_size + gap)
            )

            y1 = (
                start_y
                - row * (cell_size + gap)
            )

            x1 = x0 + cell_size
            y0 = y1 - cell_size

            add_rectangle(
                vertices,
                x0,
                y0,
                x1,
                y1,
                image[row, col]
            )

    return np.array(
        vertices,
        dtype=np.float32
    )


def build_histogram_vertices(
    hist,
    center_x,
    center_y,
    max_width,
    max_height,
    color=(0.85, 0.70, 0.25)
):
    vertices = []

    if hist.size == 0:
        return np.array(
            vertices,
            dtype=np.float32
        )

    max_value = max(
        hist.max(),
        1.0
    )

    bar_width = max_width / len(hist)
    base_y = center_y - max_height / 2.0

    for index, value in enumerate(hist):
        normalized = value / max_value

        x0 = (
            center_x
            - max_width / 2.0
            + index * bar_width
        )

        x1 = x0 + bar_width * 0.85
        y0 = base_y
        y1 = base_y + normalized * max_height

        add_rectangle(
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
    levels = 8

    if mode == 1:
        return build_grid_vertices(
            original_image,
            center_x=0.0,
            center_y=0.0,
            max_width=1.25,
            max_height=1.25
        )

    if mode == 2:
        image = draw_diagonal_line(
            original_image
        )

        return build_grid_vertices(
            image,
            center_x=0.0,
            center_y=0.0,
            max_width=1.25,
            max_height=1.25
        )

    if mode == 3:
        image = invert_rgb_to_cmy(
            original_image
        )

        return build_grid_vertices(
            image,
            center_x=0.0,
            center_y=0.0,
            max_width=1.25,
            max_height=1.25
        )

    if mode == 4:
        image = rgb_to_luminance_y(
            original_image
        )

        return build_grid_vertices(
            image,
            center_x=0.0,
            center_y=0.0,
            max_width=1.25,
            max_height=1.25
        )

    if mode == 5:
        image = rgb_to_hsv_value(
            original_image
        )

        return build_grid_vertices(
            image,
            center_x=0.0,
            center_y=0.0,
            max_width=1.25,
            max_height=1.25
        )

    gray = to_gray(
        original_image
    )

    hist = compute_histogram(
        gray,
        levels
    )

    if mode == 6:
        gray_rgb = gray_to_rgb(
            gray
        )

        return np.concatenate([
            build_grid_vertices(
                gray_rgb,
                center_x=-0.45,
                center_y=0.20,
                max_width=0.85,
                max_height=0.85
            ),
            build_histogram_vertices(
                hist,
                center_x=0.45,
                center_y=0.15,
                max_width=0.85,
                max_height=0.85
            )
        ])

    if mode == 7:
        equalized = equalize_grayscale(
            gray,
            levels
        )

        return build_grid_vertices(
            gray_to_rgb(equalized),
            center_x=0.0,
            center_y=0.0,
            max_width=1.25,
            max_height=1.25
        )

    if mode == 8:
        equalized = equalize_grayscale(
            gray,
            levels
        )

        hist_equalized = compute_histogram(
            equalized,
            levels
        )

        return np.concatenate([
            build_grid_vertices(
                gray_to_rgb(gray),
                center_x=-0.55,
                center_y=0.38,
                max_width=0.65,
                max_height=0.65
            ),
            build_grid_vertices(
                gray_to_rgb(equalized),
                center_x=0.55,
                center_y=0.38,
                max_width=0.65,
                max_height=0.65
            ),
            build_histogram_vertices(
                hist,
                center_x=-0.55,
                center_y=-0.50,
                max_width=0.65,
                max_height=0.45,
                color=(0.85, 0.65, 0.20)
            ),
            build_histogram_vertices(
                hist_equalized,
                center_x=0.55,
                center_y=-0.50,
                max_width=0.65,
                max_height=0.45,
                color=(0.30, 0.75, 0.95)
            )
        ])

    return build_grid_vertices(
        original_image,
        center_x=0.0,
        center_y=0.0,
        max_width=1.25,
        max_height=1.25
    )


def create_geometry():
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(
        GL_ARRAY_BUFFER,
        vbo
    )

    glBufferData(
        GL_ARRAY_BUFFER,
        0,
        None,
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
    print("=" * 60)
    print("Histograma com Python/OpenGL")
    print("=" * 60)

    for number in range(1, 9):
        print(
            f"{number} -> {MODE_NAMES[number]}"
        )

    print("H -> ajuda")
    print("ESC -> sair")
    print("=" * 60)
    print()


def update_window_title(window):
    glfw.set_window_title(
        window,
        (
            "Histograma com Python/OpenGL"
            f" | Modo {mode}: {MODE_NAMES[mode]}"
        )
    )


def set_mode(window, new_mode):
    global mode

    if new_mode not in MODE_NAMES:
        return

    mode = new_mode

    print(
        f"Modo {mode}: {MODE_NAMES[mode]}"
    )

    update_window_title(window)


def key_callback(
    window,
    key,
    scancode,
    action,
    mods
):
    if action != glfw.PRESS:
        return

    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(
            window,
            True
        )
        return

    key_to_mode = {
        glfw.KEY_1: 1,
        glfw.KEY_2: 2,
        glfw.KEY_3: 3,
        glfw.KEY_4: 4,
        glfw.KEY_5: 5,
        glfw.KEY_6: 6,
        glfw.KEY_7: 7,
        glfw.KEY_8: 8,
        glfw.KEY_KP_1: 1,
        glfw.KEY_KP_2: 2,
        glfw.KEY_KP_3: 3,
        glfw.KEY_KP_4: 4,
        glfw.KEY_KP_5: 5,
        glfw.KEY_KP_6: 6,
        glfw.KEY_KP_7: 7,
        glfw.KEY_KP_8: 8,
    }

    if key in key_to_mode:
        set_mode(
            window,
            key_to_mode[key]
        )

    elif key == glfw.KEY_H:
        print_help()


def main():
    window = create_window()
    program = create_shader_program()
    original_image = create_demo_image()

    vao, vbo = create_geometry()

    glViewport(
        0,
        0,
        WIDTH,
        HEIGHT
    )

    print_help()

    last_mode = None
    vertices = np.array(
        [],
        dtype=np.float32
    )

    while not glfw.window_should_close(
        window
    ):
        glfw.poll_events()

        if mode != last_mode:
            vertices = build_scene_vertices(
                original_image
            )

            update_vbo(
                vbo,
                vertices
            )

            last_mode = mode

        glClearColor(
            0.08,
            0.08,
            0.10,
            1.0
        )
        glClear(
            GL_COLOR_BUFFER_BIT
        )

        glUseProgram(program)
        glBindVertexArray(vao)

        glDrawArrays(
            GL_TRIANGLES,
            0,
            len(vertices) // 5
        )

        glBindVertexArray(0)

        glfw.swap_buffers(window)

    glDeleteVertexArrays(
        1,
        [vao]
    )
    glDeleteBuffers(
        1,
        [vbo]
    )
    glDeleteProgram(program)

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
