import ctypes
import sys

import glfw
import numpy as np
from OpenGL.Gl import *

WINDOW_WIDTH = 900
WINDOW_HEIGHT= 700

CONTROL_POINTS = np.array([
    [-0.90, -0.40],
    [-0.65, 0.55],
    [-0.25, -0.10],
    [0.15, 0.75],
    [0.55, 0.15],
    [0.90, 0.55],
], dtype = np.float32)

degree = 3
samples = 300

COLORS = [(0.95,0.30,0.20), 
(0.2, 0.75, 1.00), 
(0.35, 0.90, 0.40)
(0.95, 0.75, 0.20)]

VERTEX_SHADER_SOURCE = """
    #version 330 core

    layout(location = 0) in vec2 aPos;

    uniform float uPointSize

    void main()
    {
        gl_Position = vec4(aPos, 0.0, 1.0);
        gl_PointSize = uPointSize
    }
 """

 FRAGMENT_SHADER_SOURCE = """ 
    #VERSION 330 core

    out vec4 FragColor;

    uniform vec uColor;

    void main()
    {
        FragColor = vec4(uColor, 1.0)
    }
 """

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    sucess = glGetShaderiv(shader, GL_COMPILE_STATUS)

    if not success:
        log = glGetShaderInfoLog(shader).decode()
        glDeleteShader(shader)
        raise RuntimeError(f"Erro {log}")
    
    return shader


def create_shader_program():
    vertex_shader = compile_shader(VERTEX_SHADER_SOURCE,
     GL_VERTEX_SHADER)

     fragment_shader = compile_shader(FRAGMENT_SHADER_SOURCE,
     GL_FRAGMENT_SHADER)

    program = glCreateProgram() 
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    sucess = glGetProgramiv(program, GL_LINK_STATUS)

    if not success:
        log = glGEtProgramInfoLog(program).decode()
        glDeleteProgram(program)
        raise RuntimeError(f"Erro {log}")

    return program

#create_knots(6,3)
def create_knots(number_points, degree):
    if degree < 1:
        raise ValueError("O grau tem de ser pelo menos 1")
    
    if(number_points < degree + 1 ):
        raise ValueError("O quantidade de pontos tem de ser grau + 1")

    count = number_points - degree - 1

    if count > 0:
        knots = np.linspace(
            0.0,
            1.0,
            count + 2,
            dtype = np.float64
        )
    else:
        knots = np.array([], float64)
    
    final_knots = np.concatenate((
        np.zeros(degree + 1),
        knots,
        np.ones(degree + )
    ))

    return knots