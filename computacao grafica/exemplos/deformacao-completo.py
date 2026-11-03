"""Aula 17 - Etapas 1 a 6: deformacoes e preenchimento de regioes.

Conceitos: distorcao e deformacao (definicao, tipos, aplicacoes),
escala em X, coordenadas baricentricas, conectividade 4/8,
flood fill e boundary fill. Hough fica no estudo independente (secoes 7-10).
Imagens geradas como matrizes NumPy; SEM arquivos PNG, Pillow ou OpenCV.
Instalacao: pip install numpy glfw PyOpenGL
Execucao: python aula17_deformacoes_preenchimento_completo_ate_etapa6.py

Modos: 0 revisao Sobel (opcional), 1 escala X, 2 triangulo,
       3 flood fill 4 vizinhos, 4 flood fill 8 vizinhos,
       5 boundary fill.
Teclas: S escala; O pivo centro/origem; P redefinir triangulos;
        C nova cor; R semente inicial; H ajuda; ESC sair.
Mouse: modo 2 -> P, 3 cliques esquerda e 3 direita;
       modos 3-5 -> clique na imagem esquerda para escolher semente.
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
MODE = 1
SCALE_LEVEL = 2   # corresponde a 1.4
SCALES = (0.65, 1.0, 1.4, 1.8)
PIVOT_CENTER = True
FILL_SEED = (20, 20)  # (linha, coluna)
FILL_COLOR_INDEX = 0
FILL_COLORS = ((244, 123, 95), (110, 214, 160), (252, 209, 87))
DIRTY = True
SRC_TRIANGLE = [(12., 14.), (63., 16.), (22., 66.)]  # (x, y)
DST_TRIANGLE = [(14., 22.), (69., 34.), (32., 72.)]
PICKS = []

MODE_LABELS = {
    0: 'Revisao opcional: convolucao e Sobel',
    1: 'Deformacao em X: escala e referencia',
    2: 'Deformacao 2D: triangulos e pesos baricentricos',
    3: 'Flood fill: 4-conectividade',
    4: 'Flood fill: 8-conectividade',
    5: 'Boundary fill: parar na borda',
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


def criar_cenario_deformacao(n=SIZE):
    """Composicao colorida e grade: facilita enxergar a deformacao."""
    img = np.empty((n, n, 3), dtype=np.uint8)
    img[:] = (225, 235, 246)
    for k in range(0, n, 10):
        img[k, :] = (195, 205, 217)
        img[:, k] = (195, 205, 217)
    img[18:48, 12:32] = (231, 113, 93)
    img[26:61, 40:64] = (86, 171, 202)
    img[12:26, 45:69] = (242, 206, 86)
    desenhar_segmento(img, (15, 55), (65, 12), (42, 69, 103))
    desenhar_segmento(img, (15, 12), (68, 64), (45, 69, 103))
    return img


def criar_cenario_preenchimento(n=SIZE):
    """Regioes delimitadas, uma barreira e conexao diagonal de pixels."""
    img = np.empty((n, n, 3), dtype=np.uint8)
    fundo = (235, 240, 249)
    parede = (30, 44, 65)
    img[:] = fundo
    img[8:46, 7] = parede
    img[8:46, 39] = parede
    img[8, 7:40] = parede
    img[45, 7:40] = parede
    img[17:37, 52] = parede
    img[17:37, 73] = parede
    img[17, 52:74] = parede
    img[36, 52:74] = parede
    # Obstaculo interno, ainda separa regioes: uma forma em L.
    img[14:38, 28] = parede
    img[37, 21:29] = parede
    # Dois pequenos conjuntos cor-de-rosa unidos apenas diagonalmente.
    rosa = (232, 129, 147)
    img[53:57, 13:17] = rosa
    img[57:61, 17:21] = rosa
    # Um pequeno ponto escuro como semente visual adicional.
    return img


def cinza_rgb(img):
    """Luminancia aproximada, em [0,1]."""
    f = img.astype(np.float32) / 255.0
    return .299 * f[..., 0] + .587 * f[..., 1] + .114 * f[..., 2]


def mascara_para_rgb(mask):
    mask = np.asarray(mask, dtype=np.float32)
    return np.repeat(np.clip(mask[..., None], 0., 1.), 3, axis=2)


def convolucao_2d(canal, kernel):
    """Convolucao discreta real, com inversao de 180 graus e padding refletido."""
    canal = np.asarray(canal, dtype=np.float32)
    kernel = np.asarray(kernel, dtype=np.float32)
    if canal.ndim != 2 or kernel.ndim != 2:
        raise ValueError('Canal e kernel precisam ser matrizes 2D.')
    kh, kw = kernel.shape
    if kh % 2 == 0 or kw % 2 == 0:
        raise ValueError('Kernel precisa ter dimensoes impares.')
    py, px = kh // 2, kw // 2
    padded = np.pad(canal, ((py, py), (px, px)), mode='reflect')
    flipped = np.flip(kernel, axis=(0, 1))
    output = np.zeros_like(canal)
    for y in range(canal.shape[0]):
        for x in range(canal.shape[1]):
            output[y, x] = np.sum(padded[y:y+kh, x:x+kw] * flipped)
    return output


def bordas_sobel(imagem):
    """Usa dois kernels Sobel e combina suas respostas."""
    gray = cinza_rgb(imagem)
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
    gx = convolucao_2d(gray, kx)
    gy = convolucao_2d(gray, ky)
    return np.clip(np.hypot(gx, gy) / 4., 0, 1)


def deformar_escala_x(imagem, fator=1.4, centro=True):
    """Mapeamento inverso x_origem = px+(x_destino-px)/fator."""
    h, w, _ = imagem.shape
    resultado = np.full_like(imagem, (243, 245, 250))
    referencia = (w - 1) / 2. if centro else 0.
    for y in range(h):
        for x in range(w):
            sx = referencia + (x - referencia) / fator
            ix = int(round(sx))
            if 0 <= ix < w:
                resultado[y, x] = imagem[y, ix]
    return resultado


def pesos_baricentricos(x, y, triangulo):
    """Retorna (c1,c2,c3) com soma 1; pode ser negativo fora do triangulo."""
    (x1, y1), (x2, y2), (x3, y3) = triangulo
    d = (y2-y3)*(x1-x3) + (x3-x2)*(y1-y3)
    if abs(d) < 1e-8:
        return None  # triangulo degenerado
    c1 = ((y2-y3)*(x-x3) + (x3-x2)*(y-y3)) / d
    c2 = ((y3-y1)*(x-x3) + (x1-x3)*(y-y3)) / d
    return c1, c2, 1. - c1 - c2


def deformar_triangulo(imagem, origem, destino):
    """Preenche pixels do triangulo destino amostrando o original (inverso)."""
    h, w, _ = imagem.shape
    out = np.full_like(imagem, (240, 244, 249))
    for y in range(h):
        for x in range(w):
            cs = pesos_baricentricos(x, y, destino)
            if cs is None or min(cs) < -1e-5:
                continue
            sx = sum(cs[i] * origem[i][0] for i in range(3))
            sy = sum(cs[i] * origem[i][1] for i in range(3))
            ix, iy = int(round(sx)), int(round(sy))
            if 0 <= ix < w and 0 <= iy < h:
                out[y, x] = imagem[iy, ix]
    return out


def vizinhos(y, x, conectividade=4):
    deslocamentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if conectividade == 8:
        deslocamentos += [(-1,-1), (-1,1), (1,-1), (1,1)]
    return [(y + dy, x + dx) for dy, dx in deslocamentos]


def preencher_regiao(imagem, semente, nova_cor, conectividade=4):
    """Flood fill iterativo BFS: pinta vizinhos com a mesma cor da semente."""
    if conectividade not in (4, 8):
        raise ValueError('Conectividade deve ser 4 ou 8.')
    h, w, _ = imagem.shape
    sy, sx = map(int, semente)
    resultado = imagem.copy()
    if not (0 <= sy < h and 0 <= sx < w):
        return resultado
    alvo = imagem[sy, sx].copy()
    nova = np.asarray(nova_cor, dtype=np.uint8)
    if np.array_equal(alvo, nova):
        return resultado
    fila = deque([(sy, sx)])
    visitados = np.zeros((h, w), dtype=bool)
    while fila:
        y, x = fila.popleft()
        if not (0 <= y < h and 0 <= x < w) or visitados[y, x]:
            continue
        visitados[y, x] = True
        if not np.array_equal(imagem[y, x], alvo):
            continue
        resultado[y, x] = nova
        fila.extend(vizinhos(y, x, conectividade))
    return resultado


def preencher_por_borda(imagem, semente, cor_borda, nova_cor, conectividade=4):
    """Preenche ate encontrar a cor da borda, independentemente da cor inicial."""
    h, w, _ = imagem.shape
    sy, sx = map(int, semente)
    resultado = imagem.copy()
    if not (0 <= sy < h and 0 <= sx < w):
        return resultado
    borda = np.asarray(cor_borda, dtype=np.uint8)
    nova = np.asarray(nova_cor, dtype=np.uint8)
    fila = deque([(sy, sx)])
    visitados = np.zeros((h, w), dtype=bool)
    while fila:
        y, x = fila.popleft()
        if not (0 <= y < h and 0 <= x < w) or visitados[y, x]:
            continue
        visitados[y, x] = True
        pixel = imagem[y, x]
        if np.array_equal(pixel, borda) or np.array_equal(pixel, nova):
            continue
        resultado[y, x] = nova
        fila.extend(vizinhos(y, x, conectividade))
    return resultado


def triangulo_valido(pontos):
    """Verifica geometria do mouse, mesmo antes de completar o TODO 03."""
    (x1, y1), (x2, y2), (x3, y3) = pontos
    return abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1)) >= 1e-8


def marcadores_triangulo(imagem, pontos, cor):
    img = imagem.copy()
    for i in range(3):
        desenhar_segmento(img, pontos[i], pontos[(i + 1) % 3], cor)
    for x, y in pontos:
        x, y = int(round(x)), int(round(y))
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if 0 <= x+dx < img.shape[1] and 0 <= y+dy < img.shape[0]:
                    img[y+dy,x+dx] = cor
    return img


def preparar_paineis():
    """Retorna [entrada, saida] para os seis modos da aula."""
    if MODE in (0, 1, 2):
        original = criar_cenario_deformacao()
        if MODE == 0:
            novo = (mascara_para_rgb(bordas_sobel(original)) * 255).astype(np.uint8)
        elif MODE == 1:
            novo = deformar_escala_x(original, SCALES[SCALE_LEVEL], PIVOT_CENTER)
        else:
            novo = deformar_triangulo(original, SRC_TRIANGLE, DST_TRIANGLE)
            original = marcadores_triangulo(original, SRC_TRIANGLE, (33, 42, 72))
            novo = marcadores_triangulo(novo, DST_TRIANGLE, (33, 42, 72))
        return [original, novo]

    original = criar_cenario_preenchimento()
    nova_cor = FILL_COLORS[FILL_COLOR_INDEX]
    if MODE == 3:
        novo = preencher_regiao(original, FILL_SEED, nova_cor, 4)
    elif MODE == 4:
        novo = preencher_regiao(original, FILL_SEED, nova_cor, 8)
    elif MODE == 5:
        novo = preencher_por_borda(original, FILL_SEED, (30, 44, 65), nova_cor, 4)
    else:
        raise ValueError(f'Modo inexistente: {MODE}')
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
        f'Aula 17 (etapas 1-6) | {MODE}: {MODE_LABELS[MODE]} | '
        f'escala={SCALES[SCALE_LEVEL]:.2f} | '
        f'pivo={"centro" if PIVOT_CENTER else "origem"} | semente={FILL_SEED}')


def ajuda():
    print('\n=== AULA 17: DEFORMACOES E PREENCHIMENTO ===')
    for m, label in MODE_LABELS.items():
        print(f'{m}: {label}')
    print('S: proxima escala X | O: alternar pivo centro/origem')
    print('P: reiniciar 6 cliques dos triangulos | C: trocar cor | R: restaurar semente')
    print('H: ajuda | ESC: sair')
    print('Modos 3-5: clique na imagem esquerda para escolher semente.')
    print('Modo 2: P, tres pontos na esquerda e tres na direita.')
    print('Painel esquerdo = entrada; painel direito = resultado.\n')


def teclado(window, key, scancode, action, mods):
    global MODE, SCALE_LEVEL, PIVOT_CENTER, FILL_COLOR_INDEX, FILL_SEED, DIRTY, PICKS
    if action != glfw.PRESS:
        return
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
        return
    numericos = {
        glfw.KEY_0: 0, glfw.KEY_1: 1, glfw.KEY_2: 2,
        glfw.KEY_3: 3, glfw.KEY_4: 4, glfw.KEY_5: 5,
        glfw.KEY_KP_0: 0, glfw.KEY_KP_1: 1, glfw.KEY_KP_2: 2,
        glfw.KEY_KP_3: 3, glfw.KEY_KP_4: 4, glfw.KEY_KP_5: 5,
    }
    if key in numericos:
        MODE = numericos[key]
    elif key == glfw.KEY_S:
        SCALE_LEVEL = (SCALE_LEVEL + 1) % len(SCALES)
    elif key == glfw.KEY_O:
        PIVOT_CENTER = not PIVOT_CENTER
    elif key == glfw.KEY_P:
        PICKS = []
        print('Novo triangulo: 3 pontos na esquerda, depois 3 na direita.')
    elif key == glfw.KEY_C:
        FILL_COLOR_INDEX = (FILL_COLOR_INDEX + 1) % len(FILL_COLORS)
    elif key == glfw.KEY_R:
        FILL_SEED = (20, 20)
    elif key == glfw.KEY_H:
        ajuda()
        return
    else:
        return
    DIRTY = True
    atualizar_titulo(window)
    print('Modo:', MODE_LABELS[MODE])


def click_mouse(window, botao, acao, mods):
    global FILL_SEED, SRC_TRIANGLE, DST_TRIANGLE, PICKS, DIRTY
    if botao != glfw.MOUSE_BUTTON_LEFT or acao != glfw.PRESS:
        return
    if MODE not in (2,3,4,5):
        return
    x, y = glfw.get_cursor_pos(window)
    ww, wh = glfw.get_window_size(window)
    if not ww or not wh:
        return
    nx, ny = 2.0 * x / ww - 1.0, 1.0 - 2.0 * y / wh
    lado = 0 if MODE in (3,4,5) or len(PICKS) < 3 else 1
    ox, top, ps = geometria_painel(np.empty((SIZE,SIZE,3)), lado)
    col = int((nx - ox) / ps)
    lin = int((top - ny) / ps)
    if not (0 <= lin < SIZE and 0 <= col < SIZE):
        print('Clique no painel', 'esquerdo' if lado == 0 else 'direito')
        return
    if MODE in (3,4,5):
        FILL_SEED = (lin, col)
        print('Nova semente (linha,coluna):', FILL_SEED)
    else:
        PICKS.append((float(col), float(lin)))
        print(f'Ponto {len(PICKS)}/6: (x={col}, y={lin})')
        if len(PICKS) == 6:
            if (not triangulo_valido(PICKS[:3]) or
                not triangulo_valido(PICKS[3:])):
                print('Triangulo degenerado. Pressione P para repetir.')
                PICKS = []
            else:
                SRC_TRIANGLE = list(PICKS[:3])
                DST_TRIANGLE = list(PICKS[3:])
                PICKS = []
                print('Deformacao aplicada. Pressione P para nova selecao.')
    DIRTY = True
    atualizar_titulo(window)


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
    glfw.set_mouse_button_callback(window, click_mouse)
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
