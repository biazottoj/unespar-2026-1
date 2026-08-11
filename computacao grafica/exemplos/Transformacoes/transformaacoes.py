import ctypes
import sys

import glfw
import numpy as np
from OpenGL.Gl import *

VERTEX_SHADER_SOURCE = """
    #version 330 core

    layout(location = 0) in vec2 aPos;

    uniform mat3 uTransform;

    void main()
    {
        vec3 p = vec3(aPos, 1.0);
        vec3 transformed =  uTransform * p;
        gl_Position = vec4(transformed.xy, 0.0, 1.0);
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

def matriz_translacao(delta_x, delta_y):
    matriz = np.array(
        [1.0, 0.0, delta_x],
        [0.0, 1.0, delta_y],
        [0.0, 0.0, 1.0], dtype = float32)
    
    return matriz


def matriz_escala(fator_x, fator_y):
    matriz = np.array(
        [fator_x, 0.0, 0.0],
        [0.0, fator_y, 0.0],
        [0.0, 0.0, 1.0], dtype = float32)


def matriz_rotacao(angulo_graus):
    angulo_rad = np.radians(angulo_graus)
    sin = np.sin(angulo_rad)
    cos = np.cos(angulo_rad)

    matriz = np.array(
        [cos, -sin, 0.0],
        [sin, cos, 0.0],
        [0.0, 0.0, 1.0], dtype = float32)

