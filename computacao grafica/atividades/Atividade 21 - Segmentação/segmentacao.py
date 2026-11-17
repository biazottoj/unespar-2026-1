"""Aula 19 — BASE para completar (NumPy + OpenGL 3.3).

Executar: python aula19_segmentacao_completo.py
Instalar: python -m pip install numpy glfw PyOpenGL

A imagem é construída diretamente como matriz NumPy. O OpenGL apenas exibe
as matrizes processadas na CPU; nenhum OpenCV ou Pillow é necessário.

Nota didática: a solução de referência de ISODATA é uma VERSÃO SIMPLIFICADA, baseada
em realocação de K-Médias, divisão por desvio padrão e fusão por distância
entre centroides. O algoritmo clássico possui outras regras/parâmetros.
"""

import math
from collections import deque
import numpy as np

LARGURA_IMAGEM = 96
ALTURA_IMAGEM = 72
MODOS = {
    1: 'Imagem de entrada (RGB)',
    2: 'Limiar fixo na luminância',
    3: 'Limiar automático de Otsu',
    4: 'Crescimento de região por semente',
    5: 'K-Médias: sementes / atribuição inicial',
    6: 'K-Médias: iterações (aperte N)',
    7: 'K-Médias: resultado após convergência',
    8: 'ISODATA: grupos iniciais',
    9: 'ISODATA simplificado: iterações (aperte N)',
    0: 'Comparação: original / K-Médias / ISODATA',
}


def criar_cena(variacao=0):
    """Gera cenas RGB [0,255] sintéticas sem arquivos externos.

    Há uma mistura de áreas discretas, gradientes e ruído leve para expor
    os limites de agrupamento somente por cor (sem noção de conectividade).
    """
    h, w = ALTURA_IMAGEM, LARGURA_IMAGEM
    yy, xx = np.mgrid[:h, :w]
    img = np.empty((h, w, 3), dtype=np.float64)
    if variacao % 2 == 0:
        img[:] = (91, 160, 227)                        # céu
        img[yy > 34 + 5 * np.sin(xx / 12)] = (86, 178, 100)  # colina
        img[yy > 53 + 4 * np.sin(xx / 9)] = (39, 113, 71)    # solo
        sol = (xx - 75)**2 + (yy - 14)**2 < 11**2
        img[sol] = (246, 201, 80)
        casa = (xx >= 19) & (xx <= 41) & (yy >= 33) & (yy < 55)
        img[casa] = (208, 91, 77)
        telhado = (yy >= 24) & (yy < 34) & (np.abs(xx - 30) < 13 - (34 - yy))
        img[telhado] = (116, 69, 64)
        janela = (xx >= 25) & (xx <= 32) & (yy >= 41) & (yy < 49)
        img[janela] = (236, 223, 143)
    else:
        img[:] = (57, 82, 126)                         # fundo escuro
        img[yy > 45] = (173, 151, 114)                 # mesa
        img[(xx - 23)**2 + (yy - 31)**2 < 16**2] = (221, 83, 75)
        img[(xx - 56)**2 + (yy - 27)**2 < 13**2] = (236, 184, 65)
        img[(xx - 78)**2 + (yy - 34)**2 < 9**2] = (65, 183, 143)
        img[50:64, 31:72] = (75, 123, 192)
        img[53:61, 36:67] = (84, 149, 209)
    # Variabilidade interna controlada: cores próximas, mas não idênticas.
    luz = (xx / max(1, w - 1) - 0.5) * 18 + 7 * np.sin(yy / 10)
    rng = np.random.default_rng(41 + variacao)
    ru = rng.normal(0.0, 3.2, size=(h, w, 1))
    img = np.clip(img + luz[..., None] + ru, 0, 255)
    return img.astype(np.uint8)


def luminancia(imagem):
    """Converte para cinza aproximado com pesos perceptuais (0..255)."""
    rgb = imagem.astype(np.float64)
    return rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114


def limiar_fixo(cinza, limiar=30):
    return cinza >= float(limiar)


def limiar_otsu(cinza):
    """Escolhe T que maximiza a variância entre as duas classes."""
    intensidades = np.clip(np.rint(cinza), 0, 255).astype(np.uint8)
    hist = np.bincount(intensidades.ravel(), minlength=256).astype(float)
    total = hist.sum()
    if total == 0:
        return 0
    prob = hist / total
    peso_fundo = np.cumsum(prob)
    media_acumulada = np.cumsum(np.arange(256, dtype=float) * prob)
    media_total = media_acumulada[-1]
    denominador = peso_fundo * (1 - peso_fundo)
    variancia_entre = np.zeros(256, dtype=float)
    validos = denominador > 1e-12
    variancia_entre[validos] = (
        (media_total * peso_fundo[validos] - media_acumulada[validos]) ** 2
        / denominador[validos]
    )
    return int(np.argmax(variancia_entre))


def crescimento_regiao(imagem, semente=(28, 43), tolerancia=35.0, conectividade=4):
    h, w = imagem.shape[:2]
    sx, sy = int(semente[0]), int(semente[1])
    sx, sy = min(max(0, sx), w - 1), min(max(0, sy), h - 1)
    cor_base = imagem[sy, sx].astype(float)
    visitados = np.zeros((h, w), dtype=bool)
    mascara = np.zeros((h, w), dtype=bool)
    fila = deque([(sx, sy)])
    vizinhos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if conectividade == 8:
        vizinhos += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    while fila:
        x, y = fila.popleft()
        if not (0 <= x < w and 0 <= y < h) or visitados[y, x]:
            continue
        visitados[y, x] = True
        if np.linalg.norm(imagem[y, x].astype(float) - cor_base) > tolerancia:
            continue
        mascara[y, x] = True
        for dx, dy in vizinhos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not visitados[ny, nx]:
                fila.append((nx, ny))
    return mascara


def iniciar_centroides(pixels, k=4, semente_aleatoria=5):
    # TODO 04: selecionar K pixels reais como sementes iniciais
    # usando np.random.default_rng(semente_aleatoria).
    return np.linspace(30, 220, int(k))[:, None] * np.ones((1, 3))  # PROVISÓRIO


def atribuir_clusters(pixels, centroides):
    # TODO 05: calcular a distância euclidiana RGB para cada centroide
    # e escolher o índice do mais próximo com np.argmin.
    n = np.asarray(pixels).reshape(-1, 3).shape[0]
    return np.zeros(n, dtype=np.int32)  # PROVISÓRIO: grupo 0 para todos


def atualizar_centroides(pixels, rotulos, centroides):
    # TODO 06: para cada grupo calcular a média dos RGB atribuídos
    # e tratar adequadamente clusters vazios.
    return np.asarray(centroides, dtype=float).copy()  # PROVISÓRIO


def iteracao_kmedias(pixels, centroides):
    # TODO 07: combinar atribuir_clusters + atualizar_centroides.
    # Retornar (novos_centroides, rotulos).
    dados = np.asarray(pixels).reshape(-1, 3)
    return np.asarray(centroides, dtype=float).copy(), np.zeros(len(dados), dtype=np.int32)  # PROVISÓRIO


def executar_kmedias(imagem, k=4, passos=12, seed=5):
    """Executa até 'passos' iterações ou até estabilizar (limite 20)."""
    pixels = imagem.reshape(-1, 3).astype(float)
    centros = iniciar_centroides(pixels, k, seed)
    anterior = None
    for _ in range(max(0, min(20, int(passos)))):
        novos, labels = iteracao_kmedias(pixels, centros)
        centros = novos
        if anterior is not None and np.array_equal(labels, anterior):
            break
        anterior = labels
    labels = atribuir_clusters(pixels, centros)
    return centros, labels.reshape(imagem.shape[:2])


def iteracao_isodata(pixels, centroides, max_grupos=6, min_pixels=35,
                     desvio_divisao=25.0, distancia_fusao=28.0):
    # TODO 08: aproveitar uma etapa de K-Médias e depois: 
    # (a) fundir centroides próximos (se a distância for pequena);
    # (b) dividir grupos muito dispersos (desvio padrão alto);
    # (c) atualizar o conjunto de centroides dinamicamente.
    novos, rotulos = iteracao_kmedias(pixels, centroides)
    return novos, 'ISODATA ainda não implementado'  # PROVISÓRIO


def executar_isodata(imagem, k=3, passos=9, seed=5, max_grupos=6):
    """Executa a versão pedagógica de ISODATA por número de etapas."""
    dados = imagem.reshape(-1, 3).astype(float)
    cs = iniciar_centroides(dados, min(k, max_grupos), seed)
    eventos = []
    for _ in range(max(0, min(20, int(passos)))):
        cs, evento = iteracao_isodata(dados, cs, max_grupos=max_grupos)
        eventos.append(evento)
    labs = atribuir_clusters(dados, cs).reshape(imagem.shape[:2])
    return cs, labs, eventos


def exibir_rotulos(imagem, centroides, rotulos, mostrar_bordas=False):
    """Recolore cada pixel pelo RGB de seu respectivo centroide."""
    rgb = np.clip(centroides[np.asarray(rotulos, dtype=int)], 0, 255).astype(np.uint8)
    if mostrar_bordas:
        borda = np.zeros(rotulos.shape, dtype=bool)
        borda[1:, :] |= rotulos[1:, :] != rotulos[:-1, :]
        borda[:, 1:] |= rotulos[:, 1:] != rotulos[:, :-1]
        rgb[borda] = [15, 15, 20]
    return rgb


def mascara_rgb(mascara, cor=(239, 192, 69)):
    """Mostra um conjunto selecionado em amarelo sobre fundo escuro."""
    saida = np.full((*mascara.shape, 3), (25, 32, 48), dtype=np.uint8)
    saida[mascara] = cor
    return saida


def rotulo_do_modo(modo, k, limiar, passo_k, passo_i):
    return f'{MODOS[modo]}  |  K={k}  T={limiar}  passo-K={passo_k}  passo-I={passo_i}'


def produzir_paineis(cena=0, modo=1, k=4, limiar=30, passo_k=1, passo_i=1,
                     seed=5, pixel_semente=(28, 43), contorno=False):
    """Gera as imagens do modo; sem dependência OpenGL, para testes em CPU."""
    img = criar_cena(cena)
    if modo == 1:
        return [img], 'A entrada é uma matriz NumPy RGB.'
    if modo == 2:
        mask = limiar_fixo(luminancia(img), limiar)
        return [img, mascara_rgb(mask)], f'limiar fixo = {limiar} | brancos = {mask.sum()}'
    if modo == 3:
        t = limiar_otsu(luminancia(img))
        mask = limiar_fixo(luminancia(img), t)
        return [img, mascara_rgb(mask)], f'Otsu selecionou T = {t}'
    if modo == 4:
        mask = crescimento_regiao(img, pixel_semente, tolerancia=35, conectividade=4)
        return [img, mascara_rgb(mask)], f'semente = {pixel_semente} | regiao = {mask.sum()} pixels'
    pixels = img.reshape(-1, 3).astype(float)
    if modo == 5:
        c = iniciar_centroides(pixels, k, seed)
        r = atribuir_clusters(pixels, c).reshape(img.shape[:2])
        return [img, exibir_rotulos(img, c, r, contorno)], f'K-Médias: {k} sementes iniciais'
    if modo in (6, 7):
        n = passo_k if modo == 6 else 20
        c, r = executar_kmedias(img, k=k, passos=n, seed=seed)
        return [img, exibir_rotulos(img, c, r, contorno)], f'K-Médias: {n} iterações | K = {k}'
    if modo == 8:
        c = iniciar_centroides(pixels, max(2, k - 1), seed)
        r = atribuir_clusters(pixels, c).reshape(img.shape[:2])
        return [img, exibir_rotulos(img, c, r, contorno)], f'ISODATA: {len(c)} grupos iniciais'
    if modo == 9:
        c, r, eventos = executar_isodata(img, k=max(2, k - 1), passos=passo_i,
                                       seed=seed, max_grupos=k + 2)
        return [img, exibir_rotulos(img, c, r, contorno)], (
            f'ISODATA: {len(c)} grupos | etapa {passo_i} | último: {eventos[-1] if eventos else "inicial"}'
        )
    if modo == 0:
        ck, rk = executar_kmedias(img, k, 20, seed)
        ci, ri, eventos = executar_isodata(img, max(2, k - 1), 12, seed, k + 2)
        return [img, exibir_rotulos(img, ck, rk, contorno),
                exibir_rotulos(img, ci, ri, contorno)], (
                f'original / K-Médias ({len(ck)}) / ISODATA didático ({len(ci)})')
    raise ValueError('Modo inválido')


def imprimir_ajuda():
    print('''\n=== AULA 19: SEGMENTAÇÃO (OpenGL + NumPy) ===
1 original | 2 limiar fixo | 3 Otsu | 4 crescimento de região
5 sementes do K-Médias | 6 K-Médias passo a passo | 7 K-Médias final
8 sementes ISODATA | 9 ISODATA passo a passo | 0 comparação
N avança UMA etapa nos modos 6 e 9
K muda o número K entre 2 e 6 (também ajusta limite no ISODATA)
+ / - alteram o limiar fixo | T alterna a cena | R muda a inicialização
B sobrepõe fronteiras entre grupos | clique na imagem original escolhe
semente do crescimento por região | H mostra ajuda | ESC fecha
Observação: K-Médias em RGB não garante contiguidade espacial.
ISODATA desta aula é uma versão didática simplificada.\n''')


def executar_opengl():
    import glfw
    from OpenGL.GL import (
        glGenTextures, glBindTexture, glTexParameteri, glTexImage2D, glTexSubImage2D,
        glGenVertexArrays, glBindVertexArray, glGenBuffers, glBindBuffer,
        glBufferData, glVertexAttribPointer, glEnableVertexAttribArray,
        glCreateShader, glShaderSource, glCompileShader, glGetShaderiv,
        glGetShaderInfoLog, glCreateProgram, glAttachShader, glLinkProgram,
        glGetProgramiv, glGetProgramInfoLog, glUseProgram, glUniform1i,
        glGetUniformLocation, glActiveTexture, glViewport, glClearColor,
        glClear, glDrawArrays, glDeleteTextures, glDeleteBuffers,
        glDeleteVertexArrays, glDeleteProgram, glPixelStorei,
        GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T,
        GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_CLAMP_TO_EDGE,
        GL_NEAREST, GL_RGB, GL_UNSIGNED_BYTE, GL_ARRAY_BUFFER, GL_STATIC_DRAW,
        GL_FLOAT, GL_FALSE, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER,
        GL_COMPILE_STATUS, GL_LINK_STATUS, GL_COLOR_BUFFER_BIT,
        GL_TEXTURE0, GL_TRIANGLE_STRIP, GL_UNPACK_ALIGNMENT,
    )
    if not glfw.init():
        raise RuntimeError('GLFW não inicializou. É necessário ambiente gráfico.')
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(1120, 650, 'Aula 19 — Segmentação', None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError('Janela OpenGL 3.3 Core não foi criada.')
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    vert_src = '''#version 330 core
    layout(location = 0) in vec2 a_pos;
    layout(location = 1) in vec2 a_uv;
    out vec2 uv;
    void main() { gl_Position = vec4(a_pos, 0.0, 1.0); uv = a_uv; }
    '''
    frag_src = '''#version 330 core
    in vec2 uv; out vec4 color; uniform sampler2D tex;
    void main() { color = texture(tex, uv); }
    '''

    def shader(tipo, fonte):
        s = glCreateShader(tipo)
        glShaderSource(s, fonte)
        glCompileShader(s)
        if not glGetShaderiv(s, GL_COMPILE_STATUS):
            raise RuntimeError(glGetShaderInfoLog(s).decode(errors='replace'))
        return s

    vs, fs = shader(GL_VERTEX_SHADER, vert_src), shader(GL_FRAGMENT_SHADER, frag_src)
    prog = glCreateProgram()
    glAttachShader(prog, vs)
    glAttachShader(prog, fs)
    glLinkProgram(prog)
    if not glGetProgramiv(prog, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(prog).decode(errors='replace'))
    # Dois triângulos com coordenadas de textura invertidas verticalmente:
    # linhas NumPy crescem de cima para baixo, OpenGL de baixo para cima.
    vertices = np.array([
        -1, -1, 0, 1,
         1, -1, 1, 1,
        -1,  1, 0, 0,
         1,  1, 1, 0,
    ], dtype=np.float32)
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 16, None)
    glEnableVertexAttribArray(0)
    from ctypes import c_void_p
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 16, c_void_p(8))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)
    texturas = glGenTextures(3)
    if isinstance(texturas, int):
        texturas = [texturas]
    for tex in texturas:
        glBindTexture(GL_TEXTURE_2D, tex)
        for parametro, valor in (
            (GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE),
            (GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE),
            (GL_TEXTURE_MIN_FILTER, GL_NEAREST),
            (GL_TEXTURE_MAG_FILTER, GL_NEAREST),
        ):
            glTexParameteri(GL_TEXTURE_2D, parametro, valor)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glUseProgram(prog)
    glUniform1i(glGetUniformLocation(prog, 'tex'), 0)

    estado = dict(modo=1, cena=0, k=4, limiar=178, passo_k=1,
                  passo_i=1, seed=5, pixel_semente=(12, 80), contorno=False,
                  recalcular=True)
    painel_original = [0, 0, 1, 1]

    def tecla(janela, key, scancode, action, mods):
        if action not in (glfw.PRESS, glfw.REPEAT):
            return
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(janela, True)
            return
        numeros = {glfw.KEY_1: 1, glfw.KEY_2: 2, glfw.KEY_3: 3,
                   glfw.KEY_4: 4, glfw.KEY_5: 5, glfw.KEY_6: 6,
                   glfw.KEY_7: 7, glfw.KEY_8: 8, glfw.KEY_9: 9,
                   glfw.KEY_0: 0}
        if key in numeros:
            estado['modo'] = numeros[key]
        elif key == glfw.KEY_T:
            estado['cena'] = 1 - estado['cena']
        elif key == glfw.KEY_R:
            estado['seed'] += 1
            estado['passo_k'] = 1
            estado['passo_i'] = 1
        elif key == glfw.KEY_K:
            estado['k'] = 2 if estado['k'] == 6 else estado['k'] + 1
            estado['passo_k'] = estado['passo_i'] = 1
        elif key in (glfw.KEY_EQUAL, glfw.KEY_KP_ADD):
            estado['limiar'] = min(255, estado['limiar'] + 10)
        elif key in (glfw.KEY_MINUS, glfw.KEY_KP_SUBTRACT):
            estado['limiar'] = max(0, estado['limiar'] - 10)
        elif key == glfw.KEY_N:
            if estado['modo'] == 6:
                estado['passo_k'] = min(20, estado['passo_k'] + 1)
            if estado['modo'] == 9:
                estado['passo_i'] = min(20, estado['passo_i'] + 1)
        elif key == glfw.KEY_B:
            estado['contorno'] = not estado['contorno']
        elif key == glfw.KEY_H:
            imprimir_ajuda()
        else:
            return
        estado['recalcular'] = True

    def clique(janela, button, action, mods):
        if button != glfw.MOUSE_BUTTON_LEFT or action != glfw.PRESS:
            return
        x_win, y_win = glfw.get_cursor_pos(janela)
        win_w, win_h = glfw.get_window_size(janela)
        fb_w, fb_h = glfw.get_framebuffer_size(janela)
        x = x_win * fb_w / max(1, win_w)
        y = fb_h - y_win * fb_h / max(1, win_h)
        vx, vy, vw, vh = painel_original
        if vx <= x < vx + vw and vy <= y < vy + vh:
            col = int((x - vx) / max(1, vw) * LARGURA_IMAGEM)
            lin = int((vy + vh - y) / max(1, vh) * ALTURA_IMAGEM)
            estado['pixel_semente'] = (
                max(0, min(LARGURA_IMAGEM - 1, col)),
                max(0, min(ALTURA_IMAGEM - 1, lin))
            )
            estado['modo'] = 4
            estado['recalcular'] = True
            print('Clique -> semente:', estado['pixel_semente'])

    glfw.set_key_callback(window, tecla)
    glfw.set_mouse_button_callback(window, clique)
    imprimir_ajuda()
    paineis = []
    try:
        while not glfw.window_should_close(window):
            glfw.poll_events()
            if estado['recalcular']:
                paineis, texto = produzir_paineis(**{
                    'cena': estado['cena'], 'modo': estado['modo'], 'k': estado['k'],
                    'limiar': estado['limiar'], 'passo_k': estado['passo_k'],
                    'passo_i': estado['passo_i'], 'seed': estado['seed'],
                    'pixel_semente': estado['pixel_semente'], 'contorno': estado['contorno'],
                })
                print(texto)
                glfw.set_window_title(window, 'Aula 19: ' + rotulo_do_modo(
                    estado['modo'], estado['k'], estado['limiar'],
                    estado['passo_k'], estado['passo_i']) + ' | ' + texto)
                estado['recalcular'] = False
            fb_w, fb_h = glfw.get_framebuffer_size(window)
            glViewport(0, 0, fb_w, fb_h)
            glClearColor(0.08, 0.11, 0.17, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)
            glUseProgram(prog)
            glBindVertexArray(vao)
            n = len(paineis)
            fatia = fb_w / n
            for i, img in enumerate(paineis):
                altura, largura = img.shape[:2]
                fator = min(fatia * 0.89 / largura, fb_h * 0.83 / altura)
                larg_v = max(1, int(fator * largura))
                alt_v = max(1, int(fator * altura))
                px = int(i * fatia + (fatia - larg_v) / 2)
                py = int((fb_h - alt_v) / 2)
                if i == 0:
                    painel_original[:] = [px, py, larg_v, alt_v]
                glViewport(px, py, larg_v, alt_v)
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, texturas[i])
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, largura, altura, 0,
                             GL_RGB, GL_UNSIGNED_BYTE, np.ascontiguousarray(img))
                glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
            glfw.swap_buffers(window)
    finally:
        glDeleteTextures(len(texturas), texturas)
        glDeleteBuffers(1, [vbo])
        glDeleteVertexArrays(1, [vao])
        glDeleteProgram(prog)
        glfw.destroy_window(window)
        glfw.terminate()


if __name__ == '__main__':
    executar_opengl()
