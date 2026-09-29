import ctypes
import sys

import glfw
import numpy as np
from OpenGL.GL import *


WIDTH = 900
HEIGHT = 700


tx = 0.0
ty = 0.0
tz = 0.0

angle_x = 0.0
angle_y = 0.0
angle_z = 0.0

scale_value = 1.0

projection_mode = "parallel"


YELLOW = (0.95, 0.78, 0.25)
RED = (0.88, 0.30, 0.30)
BLUE = (0.30, 0.50, 0.88)
ORANGE = (0.95, 0.55, 0.25)
PURPLE = (0.60, 0.35, 0.80)
GREEN = (0.30, 0.70, 0.40)
WHITE = (0.95, 0.95, 0.95)


def vertex(x, y, z, color):
    return [
        x, y, z,
        color[0], color[1], color[2]
    ]


face_vertices = np.array(

    vertex(-0.5, -0.5,  0.5, YELLOW) +
    vertex( 0.5, -0.5,  0.5, YELLOW) +
    vertex( 0.5,  0.5,  0.5, YELLOW) +

    vertex(-0.5, -0.5,  0.5, YELLOW) +
    vertex( 0.5,  0.5,  0.5, YELLOW) +
    vertex(-0.5,  0.5,  0.5, YELLOW) +

    vertex(-0.5, -0.5, -0.5, RED) +
    vertex( 0.5,  0.5, -0.5, RED) +
    vertex( 0.5, -0.5, -0.5, RED) +

    vertex(-0.5, -0.5, -0.5, RED) +
    vertex(-0.5,  0.5, -0.5, RED) +
    vertex( 0.5,  0.5, -0.5, RED) +

    vertex(-0.5, -0.5, -0.5, BLUE) +
    vertex(-0.5, -0.5,  0.5, BLUE) +
    vertex(-0.5,  0.5,  0.5, BLUE) +

    vertex(-0.5, -0.5, -0.5, BLUE) +
    vertex(-0.5,  0.5,  0.5, BLUE) +
    vertex(-0.5,  0.5, -0.5, BLUE) +

    vertex(0.5, -0.5, -0.5, ORANGE) +
    vertex(0.5,  0.5,  0.5, ORANGE) +
    vertex(0.5, -0.5,  0.5, ORANGE) +

    vertex(0.5, -0.5, -0.5, ORANGE) +
    vertex(0.5,  0.5, -0.5, ORANGE) +
    vertex(0.5,  0.5,  0.5, ORANGE) +

    vertex(-0.5, 0.5, -0.5, PURPLE) +
    vertex(-0.5, 0.5,  0.5, PURPLE) +
    vertex( 0.5, 0.5,  0.5, PURPLE) +

    vertex(-0.5, 0.5, -0.5, PURPLE) +
    vertex( 0.5, 0.5,  0.5, PURPLE) +
    vertex( 0.5, 0.5, -0.5, PURPLE) +

    vertex(-0.5, -0.5, -0.5, GREEN) +
    vertex( 0.5, -0.5,  0.5, GREEN) +
    vertex(-0.5, -0.5,  0.5, GREEN) +

    vertex(-0.5, -0.5, -0.5, GREEN) +
    vertex( 0.5, -0.5, -0.5, GREEN) +
    vertex( 0.5, -0.5,  0.5, GREEN),

    dtype=np.float32
)


edge_vertices = np.array(

    vertex(-0.5, -0.5, -0.5, WHITE) +
    vertex( 0.5, -0.5, -0.5, WHITE) +

    vertex( 0.5, -0.5, -0.5, WHITE) +
    vertex( 0.5,  0.5, -0.5, WHITE) +

    vertex( 0.5,  0.5, -0.5, WHITE) +
    vertex(-0.5,  0.5, -0.5, WHITE) +

    vertex(-0.5,  0.5, -0.5, WHITE) +
    vertex(-0.5, -0.5, -0.5, WHITE) +

    vertex(-0.5, -0.5, 0.5, WHITE) +
    vertex( 0.5, -0.5, 0.5, WHITE) +

    vertex( 0.5, -0.5, 0.5, WHITE) +
    vertex( 0.5,  0.5, 0.5, WHITE) +

    vertex( 0.5,  0.5, 0.5, WHITE) +
    vertex(-0.5,  0.5, 0.5, WHITE) +

    vertex(-0.5,  0.5, 0.5, WHITE) +
    vertex(-0.5, -0.5, 0.5, WHITE) +

    vertex(-0.5, -0.5, -0.5, WHITE) +
    vertex(-0.5, -0.5,  0.5, WHITE) +

    vertex(0.5, -0.5, -0.5, WHITE) +
    vertex(0.5, -0.5,  0.5, WHITE) +

    vertex(0.5, 0.5, -0.5, WHITE) +
    vertex(0.5, 0.5,  0.5, WHITE) +

    vertex(-0.5, 0.5, -0.5, WHITE) +
    vertex(-0.5, 0.5,  0.5, WHITE),

    dtype=np.float32
)


VERTEX_SHADER = """
#version 330 core

layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aColor;

out vec3 vertexColor;

uniform mat4 uModel;
uniform mat4 uView;
uniform mat4 uProjection;

void main()
{
    gl_Position =
        uProjection *
        uView *
        uModel *
        vec4(aPos, 1.0);

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


def create_window():
    if not glfw.init():
        raise RuntimeError(
            "Não foi possível inicializar o GLFW."
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
        "Projecoes 3D - Paralela",
        None,
        None
    )

    if not window:
        glfw.terminate()
        raise RuntimeError(
            "Não foi possível criar a janela."
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
        GL_STATIC_DRAW
    )

    float_size = np.dtype(
        np.float32
    ).itemsize

    stride = 6 * float_size

    glVertexAttribPointer(
        0,
        3,
        GL_FLOAT,
        GL_FALSE,
        stride,
        ctypes.c_void_p(0)
    )

    glEnableVertexAttribArray(
        0
    )

    glVertexAttribPointer(
        1,
        3,
        GL_FLOAT,
        GL_FALSE,
        stride,
        ctypes.c_void_p(
            3 * float_size
        )
    )

    glEnableVertexAttribArray(
        1
    )

    glBindBuffer(
        GL_ARRAY_BUFFER,
        0
    )

    glBindVertexArray(
        0
    )

    return vao, vbo


def identity_matrix():
    return np.eye(
        4,
        dtype=np.float32
    )


def translation_matrix(tx, ty, tz):
    return np.array([
        [1.0, 0.0, 0.0, tx],
        [0.0, 1.0, 0.0, ty],
        [0.0, 0.0, 1.0, tz],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype=np.float32)


def scale_matrix(sx, sy, sz):
    return np.array([
        [sx, 0.0, 0.0, 0.0],
        [0.0, sy, 0.0, 0.0],
        [0.0, 0.0, sz, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype=np.float32)


def rotation_x_matrix(angle_degrees):
    angle = np.radians(
        angle_degrees
    )

    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, c, -s, 0.0],
        [0.0, s, c, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)


def rotation_y_matrix(angle_degrees):
    angle = np.radians(
        angle_degrees
    )

    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [c, 0.0, s, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [-s, 0.0, c, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)


def rotation_z_matrix(angle_degrees):
    angle = np.radians(
        angle_degrees
    )

    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [c, -s, 0.0, 0.0],
        [s, c, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)


def parallel_projection_matrix(
    left,
    right,
    bottom,
    top,
    near,
    far
):
    return np.array([
        [
            2.0 / (right - left),
            0.0,
            0.0,
            -(right + left) / (right - left)
        ],
        [
            0.0,
            2.0 / (top - bottom),
            0.0,
            -(top + bottom) / (top - bottom)
        ],
        [
            0.0,
            0.0,
            -2.0 / (far - near),
            -(far + near) / (far - near)
        ],
        [
            0.0,
            0.0,
            0.0,
            1.0
        ]
    ], dtype=np.float32)


def perspective_projection_matrix(
    fov_degrees,
    aspect,
    near,
    far
):
    f = (
        1.0 /
        np.tan(
            np.radians(
                fov_degrees
            ) / 2.0
        )
    )

    return np.array([
        [
            f / aspect,
            0.0,
            0.0,
            0.0
        ],
        [
            0.0,
            f,
            0.0,
            0.0
        ],
        [
            0.0,
            0.0,
            (far + near) /
            (near - far),
            (2.0 * far * near) /
            (near - far)
        ],
        [
            0.0,
            0.0,
            -1.0,
            0.0
        ]
    ], dtype=np.float32)


def reset_transformations():
    global tx
    global ty
    global tz

    global angle_x
    global angle_y
    global angle_z

    global scale_value

    tx = 0.0
    ty = 0.0
    tz = 0.0

    angle_x = 0.0
    angle_y = 0.0
    angle_z = 0.0

    scale_value = 1.0


def process_input(window):
    global tx
    global ty
    global tz

    global angle_x
    global angle_y
    global angle_z

    global scale_value
    global projection_mode

    movement_speed = 0.02
    rotation_speed = 1.0
    scale_speed = 0.01

    if glfw.get_key(
        window,
        glfw.KEY_ESCAPE
    ) == glfw.PRESS:
        glfw.set_window_should_close(
            window,
            True
        )

    if glfw.get_key(
        window,
        glfw.KEY_RIGHT
    ) == glfw.PRESS:
        tx += movement_speed

    if glfw.get_key(
        window,
        glfw.KEY_LEFT
    ) == glfw.PRESS:
        tx -= movement_speed

    if glfw.get_key(
        window,
        glfw.KEY_UP
    ) == glfw.PRESS:
        ty += movement_speed

    if glfw.get_key(
        window,
        glfw.KEY_DOWN
    ) == glfw.PRESS:
        ty -= movement_speed

    if glfw.get_key(
        window,
        glfw.KEY_W
    ) == glfw.PRESS:
        tz += movement_speed

    if glfw.get_key(
        window,
        glfw.KEY_S
    ) == glfw.PRESS:
        tz -= movement_speed

    if glfw.get_key(
        window,
        glfw.KEY_I
    ) == glfw.PRESS:
        angle_x += rotation_speed

    if glfw.get_key(
        window,
        glfw.KEY_K
    ) == glfw.PRESS:
        angle_x -= rotation_speed

    if glfw.get_key(
        window,
        glfw.KEY_J
    ) == glfw.PRESS:
        angle_y += rotation_speed

    if glfw.get_key(
        window,
        glfw.KEY_L
    ) == glfw.PRESS:
        angle_y -= rotation_speed

    if glfw.get_key(
        window,
        glfw.KEY_U
    ) == glfw.PRESS:
        angle_z += rotation_speed

    if glfw.get_key(
        window,
        glfw.KEY_O
    ) == glfw.PRESS:
        angle_z -= rotation_speed

    if glfw.get_key(
        window,
        glfw.KEY_EQUAL
    ) == glfw.PRESS:
        scale_value += scale_speed

    if glfw.get_key(
        window,
        glfw.KEY_MINUS
    ) == glfw.PRESS:
        scale_value -= scale_speed
        scale_value = max(
            scale_value,
            0.1
        )

    if glfw.get_key(
        window,
        glfw.KEY_SPACE
    ) == glfw.PRESS:
        reset_transformations()

    if glfw.get_key(
        window,
        glfw.KEY_1
    ) == glfw.PRESS:
        projection_mode = "parallel"

    if glfw.get_key(
        window,
        glfw.KEY_2
    ) == glfw.PRESS:
        projection_mode = "perspective"


def main():
    window = create_window()

    program = create_shader_program()

    face_vao, face_vbo = create_geometry(
        face_vertices
    )

    edge_vao, edge_vbo = create_geometry(
        edge_vertices
    )

    model_location = glGetUniformLocation(
        program,
        "uModel"
    )

    view_location = glGetUniformLocation(
        program,
        "uView"
    )

    projection_location = glGetUniformLocation(
        program,
        "uProjection"
    )

    center_of_projection = np.array(
        [0.0, 0.0, 3.0],
        dtype=np.float32
    )

    view = translation_matrix(
        -center_of_projection[0],
        -center_of_projection[1],
        -center_of_projection[2]
    )

    aspect = WIDTH / HEIGHT

    near = 1.0
    far = 20.0

    half_height = 1.5
    half_width = (
        half_height *
        aspect
    )

    parallel_projection = parallel_projection_matrix(
        -half_width,
        half_width,
        -half_height,
        half_height,
        near,
        far
    )

    perspective_projection = perspective_projection_matrix(
        60.0,
        aspect,
        near,
        far
    )

    glViewport(
        0,
        0,
        WIDTH,
        HEIGHT
    )

    glEnable(
        GL_DEPTH_TEST
    )

    glLineWidth(
        2.0
    )

    print()
    print("======================================")
    print("Projecoes 3D")
    print("======================================")
    print()
    print("Projecoes:")
    print("  1 -> paralela")
    print("  2 -> perspectiva")
    print()
    print("Transformacoes:")
    print("  Setas   -> X e Y")
    print("  W / S   -> Z")
    print("  I / K   -> rotacao X")
    print("  J / L   -> rotacao Y")
    print("  U / O   -> rotacao Z")
    print("  + / -   -> escala")
    print("  Espaco  -> reset")
    print()
    print("ESC -> sair")
    print()

    while not glfw.window_should_close(
        window
    ):
        process_input(
            window
        )

        if projection_mode == "parallel":
            projection = parallel_projection

            glfw.set_window_title(
                window,
                "Projecoes 3D - Paralela"
            )
        else:
            projection = perspective_projection

            glfw.set_window_title(
                window,
                "Projecoes 3D - Perspectiva"
            )

        glClearColor(
            0.08,
            0.08,
            0.10,
            1.0
        )

        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )

        T = translation_matrix(
            tx,
            ty,
            tz
        )

        S = scale_matrix(
            scale_value,
            scale_value,
            scale_value
        )

        Rx = rotation_x_matrix(
            angle_x
        )

        Ry = rotation_y_matrix(
            angle_y
        )

        Rz = rotation_z_matrix(
            angle_z
        )

        model = (
            T
            @ Rz
            @ Ry
            @ Rx
            @ S
        )

        glUseProgram(
            program
        )

        glUniformMatrix4fv(
            model_location,
            1,
            GL_TRUE,
            model
        )

        glUniformMatrix4fv(
            view_location,
            1,
            GL_TRUE,
            view
        )

        glUniformMatrix4fv(
            projection_location,
            1,
            GL_TRUE,
            projection
        )

        glEnable(
            GL_POLYGON_OFFSET_FILL
        )

        glPolygonOffset(
            1.0,
            1.0
        )

        glBindVertexArray(
            face_vao
        )

        glDrawArrays(
            GL_TRIANGLES,
            0,
            len(face_vertices) // 6
        )

        glBindVertexArray(
            0
        )

        glDisable(
            GL_POLYGON_OFFSET_FILL
        )

        glBindVertexArray(
            edge_vao
        )

        glDrawArrays(
            GL_LINES,
            0,
            len(edge_vertices) // 6
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
        [face_vao]
    )

    glDeleteBuffers(
        1,
        [face_vbo]
    )

    glDeleteVertexArrays(
        1,
        [edge_vao]
    )

    glDeleteBuffers(
        1,
        [edge_vbo]
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
