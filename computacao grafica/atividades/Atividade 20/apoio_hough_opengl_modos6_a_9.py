"""Estudo autonomo - Hough linear e circular, secoes 7-10.

Dependencias: pip install numpy glfw PyOpenGL
Execucao: python apoio_hough_opengl_modos6_a_9.py
Teclas: 6,7,8,9 para modos; N ruido; H ajuda; ESC sair.
As matrizes binárias são criadas no próprio Python (sem Pillow/OpenCV).
"""


import ctypes
import sys
from collections import deque
import numpy as np
import glfw
from OpenGL.GL import (
    GL_ARRAY_BUFFER, GL_COLOR_BUFFER_BIT, GL_COMPILE_STATUS,
    GL_DYNAMIC_DRAW, GL_FALSE, GL_FLOAT, GL_FRAGMENT_SHADER,
    GL_LINK_STATUS, GL_TRIANGLES, GL_TRUE, GL_VERTEX_SHADER,
    glAttachShader, glBindBuffer, glBindVertexArray, glBufferData,
    glClear, glClearColor, glCompileShader, glCreateProgram,
    glCreateShader, glDeleteBuffers, glDeleteProgram, glDeleteShader,
    glDeleteVertexArrays, glDrawArrays, glEnableVertexAttribArray,
    glGenBuffers, glGenVertexArrays, glGetProgramInfoLog,
    glGetProgramiv, glGetShaderInfoLog, glGetShaderiv, glLinkProgram,
    glShaderSource, glUseProgram, glVertexAttribPointer, glViewport,
)

WINDOW_W, WINDOW_H = 1150, 760
SIZE = 80
MODE = 6
NOISE = False
DIRTY = True
MODE_LABELS = {
    6: 'Hough: imagem binaria de entrada',
    7: 'Hough linear: matriz de votos (rho, theta)',
    8: 'Hough linear: retas detectadas',
    9: 'Hough circular: centros com raio 13',
}

VERTEX_SHADER = """#version 330 core
layout(location = 0) in vec2 aPos;
layout(location = 1) in vec3 aColor;
out vec3 vColor;
void main() { gl_Position = vec4(aPos, 0.0, 1.0); vColor = aColor; }
"""
FRAGMENT_SHADER = """#version 330 core
in vec3 vColor;
out vec4 FragColor;
void main() { FragColor = vec4(vColor, 1.0); }
"""


def desenhar_segmento(imagem, p0, p1, cor):
    """Rasterizacao simples de segmento, inclusive para contornos/ruido."""
    x0, y0 = map(int, p0)
    x1, y1 = map(int, p1)
    passos = max(abs(x1 - x0), abs(y1 - y0), 1)
    h, w = imagem.shape[:2]
    for t in np.linspace(0., 1., passos * 2 + 1):
        x = int(round(x0 * (1 - t) + x1 * t))
        y = int(round(y0 * (1 - t) + y1 * t))
        if 0 <= x < w and 0 <= y < h:
            imagem[y, x] = cor


def desenhar_circulo(imagem, centro, raio, cor):
    cx, cy = centro
    for a in np.linspace(0, 2 * np.pi, 720, endpoint=False):
        x = int(round(cx + raio * np.cos(a)))
        y = int(round(cy + raio * np.sin(a)))
        if 0 <= y < imagem.shape[0] and 0 <= x < imagem.shape[1]:
            imagem[y, x] = cor


def criar_cenario_linhas(n=SIZE, ruido=False):
    """Matriz binaria de pontos que pertencem a possiveis retas."""
    mask = np.zeros((n, n), dtype=np.uint8)
    desenhar_segmento(mask, (10, 12), (69, 65), 1)
    desenhar_segmento(mask, (8, 63), (70, 15), 1)
    desenhar_segmento(mask, (45, 9), (45, 71), 1)
    if ruido:
        rng = np.random.default_rng(17)
        ys = rng.integers(0, n, 65)
        xs = rng.integers(0, n, 65)
        mask[ys, xs] = 1
    return mask


def criar_cenario_circulos(n=SIZE, raio=13, ruido=False):
    """Dois circulos de mesmo raio, para Hough circular de raio fixo."""
    mask = np.zeros((n, n), dtype=np.uint8)
    desenhar_circulo(mask, (22, 29), raio, 1)
    desenhar_circulo(mask, (55, 47), raio, 1)
    if ruido:
        rng = np.random.default_rng(29)
        ys = rng.integers(0, n, 55)
        xs = rng.integers(0, n, 55)
        mask[ys, xs] = 1
    return mask


def mascara_para_rgb(mask):
    mask = np.asarray(mask, dtype=np.float32)
    return np.repeat(np.clip(mask[..., None], 0., 1.), 3, axis=2)


def acumulador_hough_linear(bordas, passo_angular=2):
    """Cada pixel de borda vota em rho=x*cos(theta)+y*sin(theta)."""
    h, w = bordas.shape
    thetas = np.deg2rad(np.arange(0, 180, passo_angular, dtype=np.float32))
    dist_max = int(np.ceil(np.hypot(h - 1, w - 1)))
    rhos = np.arange(-dist_max, dist_max + 1, dtype=np.int32)
    votos = np.zeros((len(rhos), len(thetas)), dtype=np.int32)
    ys, xs = np.nonzero(bordas)
    for y, x in zip(ys, xs):
        for ti, th in enumerate(thetas):
            rho = int(round(x * np.cos(th) + y * np.sin(th)))
            votos[rho + dist_max, ti] += 1
    return votos, rhos, thetas


def picos_hough_linear(votos, rhos, thetas, quantidade=3, min_votos=27):
    """Maximos com supressao local, reduz linhas duplicadas proximas."""
    candidatos = np.argsort(votos.ravel())[::-1]
    selecionados = []
    for pos in candidatos:
        ri, ti = np.unravel_index(pos, votos.shape)
        n = int(votos[ri, ti])
        if n < min_votos:
            break
        rho, theta = float(rhos[ri]), float(thetas[ti])
        # Este teste e propositalmente simples: nao cobre equivalencia
        # (rho,theta) ~ (-rho,theta+pi) nos extremos.
        if any(abs(ri - other_ri) <= 7 and abs(ti - other_ti) <= 6
               for other_ri, other_ti, *_ in selecionados):
            continue
        selecionados.append((ri, ti, rho, theta, n))
        if len(selecionados) >= quantidade:
            break
    return [(rho, theta, n) for _, _, rho, theta, n in selecionados]


def desenhar_retas_hough(bordas, retas):
    out = np.zeros((*bordas.shape, 3), dtype=np.uint8)
    out[bordas > 0] = (230, 233, 242)
    yy, xx = np.indices(bordas.shape)
    for rho, theta, _ in retas:
        sobre_reta = np.abs(xx * np.cos(theta) + yy * np.sin(theta) - rho) <= 0.65
        out[sobre_reta] = (253, 101, 101)
    return out


def visualizacao_acumulador(votos):
    f = np.log1p(votos.astype(np.float32))
    f /= max(float(np.max(f)), 1e-9)
    out = np.zeros((*votos.shape, 3), dtype=np.uint8)
    out[..., 0] = (255 * np.sqrt(f)).astype(np.uint8)
    out[..., 1] = (202 * f).astype(np.uint8)
    out[..., 2] = (55 + 185 * f).astype(np.uint8)
    return out


def acumulador_hough_circular(bordas, raio=13, amostras=72):
    """Para cada ponto de borda, vota em possiveis centros (a,b)."""
    h, w = bordas.shape
    votos = np.zeros((h, w), dtype=np.int32)
    angulos = np.linspace(0, 2 * np.pi, amostras, endpoint=False)
    offsets = [(int(round(raio*np.cos(a))), int(round(raio*np.sin(a))))
               for a in angulos]
    offsets = sorted(set(offsets))  # evita votos repetidos por mesmo pixel
    for y, x in zip(*np.nonzero(bordas)):
        for dx, dy in offsets:
            cx, cy = x - dx, y - dy
            if 0 <= cx < w and 0 <= cy < h:
                votos[cy, cx] += 1
    return votos


def picos_hough_circular(votos, quantidade=2, min_votos=22, distancia=14):
    result = []
    for pos in np.argsort(votos.ravel())[::-1]:
        y, x = np.unravel_index(pos, votos.shape)
        n = int(votos[y, x])
        if n < min_votos:
            break
        if any((x-cx)**2 + (y-cy)**2 < distancia**2 for cx, cy, _ in result):
            continue
        result.append((int(x), int(y), n))
        if len(result) >= quantidade:
            break
    return result


def preparar_paineis():
    if MODE <= 8:
        bordas = criar_cenario_linhas(ruido=NOISE)
        original = (mascara_para_rgb(bordas) * 255).astype(np.uint8)
        if MODE == 6:
            # Visualizacao preparatoria: pontos de bordas sao entrada de Hough.
            return [original, original.copy()]
        votos, rhos, thetas = acumulador_hough_linear(bordas)
        if MODE == 7:
            return [original, visualizacao_acumulador(votos)]
        retas = picos_hough_linear(votos, rhos, thetas)
        print('Retas (rho, theta em graus, votos):',
              [(round(r,1), round(float(np.rad2deg(t)),1), n) for r,t,n in retas])
        return [original, desenhar_retas_hough(bordas, retas)]
    bordas = criar_cenario_circulos(ruido=NOISE)
    original = (mascara_para_rgb(bordas) * 255).astype(np.uint8)
    votos = acumulador_hough_circular(bordas, raio=13)
    centros = picos_hough_circular(votos)
    novo = original.copy()
    for x,y,_ in centros:
        desenhar_circulo(novo, (x,y), 13, (253, 103, 102))
        desenhar_segmento(novo, (x-2,y), (x+2,y), (87, 245, 155))
        desenhar_segmento(novo, (x,y-2), (x,y+2), (87, 245, 155))
    print('Centros Hough circular (x,y,votos):', centros)
    return [original, novo]


def adicionar_quadrado(vertices, x0, y0, x1, y1, color):
    r, g, b = (float(z) / 255.0 for z in color)
    vertices.extend((
        x0,y0,r,g,b, x1,y0,r,g,b, x1,y1,r,g,b,
        x0,y0,r,g,b, x1,y1,r,g,b, x0,y1,r,g,b,
    ))


def geometria_painel(imagem, posicao):
    h, w = imagem.shape[:2]
    centro_x = (-0.5, 0.5)[posicao]
    size = min(0.83 / w, 1.42 / h)
    return centro_x - w * size / 2, 0.71, size


def painel_para_vertices(vertices, imagem, posicao):
    ox, top, tamanho = geometria_painel(imagem, posicao)
    for y in range(imagem.shape[0]):
        y1 = top - y * tamanho
        y0 = y1 - tamanho
        for x in range(imagem.shape[1]):
            x0 = ox + x * tamanho
            adicionar_quadrado(vertices, x0, y0, x0 + tamanho, y1, imagem[y, x])


def gerar_vertices():
    vertices = []
    for ind, imagem in enumerate(preparar_paineis()):
        painel_para_vertices(vertices, imagem, ind)
    return np.asarray(vertices, dtype=np.float32)


def shader(tipo, fonte):
    obj = glCreateShader(tipo)
    glShaderSource(obj, fonte)
    glCompileShader(obj)
    if not glGetShaderiv(obj, GL_COMPILE_STATUS):
        msg = glGetShaderInfoLog(obj)
        glDeleteShader(obj)
        raise RuntimeError(msg)
    return obj


def criar_programa():
    vs = shader(GL_VERTEX_SHADER, VERTEX_SHADER)
    fs = shader(GL_FRAGMENT_SHADER, FRAGMENT_SHADER)
    prog = glCreateProgram()
    glAttachShader(prog, vs)
    glAttachShader(prog, fs)
    glLinkProgram(prog)
    if not glGetProgramiv(prog, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(prog))
    glDeleteShader(vs)
    glDeleteShader(fs)
    return prog


def criar_buffers():
    vao, vbo = glGenVertexArrays(1), glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, 0, None, GL_DYNAMIC_DRAW)
    step = np.dtype(np.float32).itemsize
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5*step, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5*step, ctypes.c_void_p(2*step))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)
    return vao, vbo


def atualizar_titulo(window):
    glfw.set_window_title(window,
        f'Estudo complementar: Hough | {MODE}: {MODE_LABELS[MODE]} | '
        f'ruido={"ligado" if NOISE else "desligado"}')


def ajuda():
    print('\n=== HOUGH: ESTUDO INDEPENDENTE (SECOES 7-10) ===')
    for m, label in MODE_LABELS.items():
        print(f'{m}: {label}')
    print('N: adicionar/remover ruido | H: ajuda | ESC: sair')
    print('Painel esquerdo = matriz de entrada; direito = saida/acumulador.\n')


def teclado(window, key, scancode, action, mods):
    global MODE, NOISE, DIRTY
    if action != glfw.PRESS:
        return
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
        return
    numeric = {glfw.KEY_6: 6, glfw.KEY_7: 7, glfw.KEY_8: 8,
               glfw.KEY_9: 9, glfw.KEY_KP_6: 6, glfw.KEY_KP_7: 7,
               glfw.KEY_KP_8: 8, glfw.KEY_KP_9: 9}
    if key in numeric:
        MODE = numeric[key]
    elif key == glfw.KEY_N:
        NOISE = not NOISE
    elif key == glfw.KEY_H:
        ajuda()
        return
    else:
        return
    DIRTY = True
    atualizar_titulo(window)
    print('Modo:', MODE_LABELS[MODE])


def framebuffer_redimensionado(window, largura, altura):
    glViewport(0, 0, largura, altura)


def main():
    global DIRTY
    if not glfw.init():
        raise RuntimeError('GLFW nao iniciou. Necessario desktop com interface grafica.')
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    if sys.platform == 'darwin':
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    window = glfw.create_window(WINDOW_W, WINDOW_H, 'Aula 17', None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError('Falha na criacao da janela OpenGL 3.3 Core.')
    glfw.make_context_current(window)
    glfw.set_key_callback(window, teclado)
    glfw.set_framebuffer_size_callback(window, framebuffer_redimensionado)
    program = criar_programa()
    vao, vbo = criar_buffers()
    framebuffer_redimensionado(window, *glfw.get_framebuffer_size(window))
    atualizar_titulo(window)
    ajuda()
    count = 0
    try:
        while not glfw.window_should_close(window):
            glfw.poll_events()
            if DIRTY:
                vertices = gerar_vertices()
                glBindBuffer(GL_ARRAY_BUFFER, vbo)
                glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
                glBindBuffer(GL_ARRAY_BUFFER, 0)
                count = len(vertices) // 5
                DIRTY = False
            glClearColor(0.06, 0.08, 0.12, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)
            glUseProgram(program)
            glBindVertexArray(vao)
            glDrawArrays(GL_TRIANGLES, 0, count)
            glBindVertexArray(0)
            glfw.swap_buffers(window)
    finally:
        glDeleteVertexArrays(1, [vao])
        glDeleteBuffers(1, [vbo])
        glDeleteProgram(program)
        glfw.destroy_window(window)
        glfw.terminate()


if __name__ == '__main__':
    main()
