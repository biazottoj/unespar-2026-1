"""Esqueletizacao e morfologia binaria - Python / OpenGL moderno.

Requisitos: python -m pip install numpy glfw PyOpenGL

Controles:
  1 original        2 elemento estruturante   3 erosao
  4 dilatacao       5 abertura                6 fechamento
  7 erosao por etapa ([/])                     8 camada do esqueleto
  9 esqueleto final 0 comparacao                ESPACO alterna kernel
  T alterna figura [/] muda etapa              H ajuda  ESC sair
"""
import ctypes
import sys
import numpy as np
import glfw
from OpenGL.GL import *

LARGURA = 1200
ALTURA = 760
MODO = 1
KERNEL = 'cruz'
FIGURA = 'B'
ETAPA = 0
SUJO = True

MODOS = {
    0: 'Comparacao: original / abertura / esqueleto',
    1: 'Imagem binaria original',
    2: 'Elemento estruturante (SE)',
    3: 'Erosao',
    4: 'Dilatacao',
    5: 'Abertura: erosao + dilatacao',
    6: 'Fechamento: dilatacao + erosao',
    7: 'Erosoes sucessivas (use [ e ])',
    8: 'Camada S_k (use [ e ])',
    9: 'Esqueleto morfologico final',
}

VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec2 aPosition;
layout (location = 1) in vec3 aColor;
out vec3 vColor;
void main() {
    gl_Position = vec4(aPosition, 0.0, 1.0);
    vColor = aColor;
}
"""
FRAGMENT_SHADER = """
#version 330 core
in vec3 vColor;
out vec4 FragColor;
void main() { FragColor = vec4(vColor, 1.0); }
"""


def imagem_binaria(nome='B'):
    """1 significa objeto; 0 significa fundo. Gera exemplos sem arquivos."""
    h, w = 29, 35
    a = np.zeros((h, w), dtype=bool)
    if nome == 'B':
        a[4:25, 5:10] = True   # haste vertical
        a[4:9, 8:23] = True   # barras horizontais
        a[12:17, 8:23] = True
        a[20:25, 8:23] = True
        a[7:15, 20:25] = True # lacos da letra B
        a[15:23, 20:25] = True
        a[2, 30] = True       # ruido isolado: desaparece na abertura
        a[26, 29] = True
        a[14, 31] = True
    elif nome == 'anel':
        yy, xx = np.ogrid[:h, :w]
        distancia = ((yy-14.0)/11.0)**2 + ((xx-17.0)/13.0)**2
        a = (distancia <= 1.0) & (distancia >= 0.30)
        a[1, 3] = True
        a[27, 31] = True
    else:
        raise ValueError('Figura desconhecida')
    return a


def elemento_estruturante(nome='cruz'):
    """Ambos possuem centro bem definido: index (1,1)."""
    if nome == 'cruz':
        return np.array([[0,1,0], [1,1,1], [0,1,0]], dtype=bool)
    if nome == 'quadrado':
        return np.ones((3,3), dtype=bool)
    raise ValueError('Kernel desconhecido')

def _verificar(imagem, se):
    if imagem.ndim != 2 or se.ndim != 2:
        raise ValueError('Imagem e elemento devem ser matrizes 2D')
    if min(se.shape) < 1 or any(t % 2 == 0 for t in se.shape):
        raise ValueError('Elemento deve possuir dimensoes impares')
    if not np.any(se):
        raise ValueError('Elemento nao pode ser vazio')
    return np.asarray(imagem, dtype=bool), np.asarray(se, dtype=bool)


def erosao(imagem, se):
    """Erosao binaria: todos os pontos ativos do SE devem caber no objeto."""
    imagem, se = _verificar(imagem, se)
    h, w = imagem.shape
    kh, kw = se.shape
    ph, pw = kh // 2, kw // 2
    padded = np.pad(imagem, ((ph, ph), (pw, pw)), constant_values=False)
    resultado = np.zeros_like(imagem)
    for row in range(h):
        for col in range(w):
            vizinhanca = padded[row:row + kh, col:col + kw]
            resultado[row, col] = np.all(vizinhanca[se])
    return resultado


def dilatacao(imagem, se):
    """Dilatacao binaria: algum ponto ativo do SE toca o objeto."""
    imagem, se = _verificar(imagem, se)
    h, w = imagem.shape
    kh, kw = se.shape
    ph, pw = kh // 2, kw // 2
    padded = np.pad(imagem, ((ph, ph), (pw, pw)), constant_values=False)
    resultado = np.zeros_like(imagem)
    for row in range(h):
        for col in range(w):
            vizinhanca = padded[row:row + kh, col:col + kw]
            resultado[row, col] = np.any(vizinhanca[se])
    return resultado


def abertura(imagem, se):
    """Abertura: (A erosao B) dilatacao B."""
    return dilatacao(erosao(imagem, se), se)


def fechamento(imagem, se):
    """Fechamento: (A dilatacao B) erosao B."""
    return erosao(dilatacao(imagem, se), se)


def construir_camadas_esqueleto(imagem, se):
    """Esqueleto morfologico por erosoes/aberturas (Lantuejoul).

    A_k = erosao repetida k vezes; S_k = A_k - abertura(A_k).
    Esqueleto: uniao de todos os S_k. Ao fim, A_k vazio.
    """
    current = np.asarray(imagem, dtype=bool).copy()
    etapas = [current.copy()]
    camadas = []
    limite_seguro = current.size + 1
    for _ in range(limite_seguro):
        if not np.any(current):
            return etapas, camadas
        opened = abertura(current, se)
        camada = np.logical_and(current, np.logical_not(opened))
        camadas.append(camada)
        prox = erosao(current, se)
        if np.array_equal(prox, current):
            raise RuntimeError('Erosao nao progrediu: confira o kernel')
        current = prox
        etapas.append(current.copy())
    raise RuntimeError('Limite de iteracoes atingido')

\
# ================================================================
# INFRAESTRUTURA DE VISUALIZACAO: ja esta completa nos dois arquivos
# ================================================================

def _retangulo(destino, x0, y0, x1, y1, cor):
    r, g, b = cor
    destino.extend((
        x0,y0,r,g,b, x1,y0,r,g,b, x1,y1,r,g,b,
        x0,y0,r,g,b, x1,y1,r,g,b, x0,y1,r,g,b,
    ))


def painel_matriz(imagem, cx, cy, maxw, maxh, cor=(0.20,0.82,0.78)):
    """Representa cada pixel como quadrado (2 triangulos) em OpenGL."""
    imagem = np.asarray(imagem, dtype=bool)
    h, w = imagem.shape
    if h == 0 or w == 0:
        return np.empty((0,), dtype=np.float32)
    gap = 0.0024 if min(h, w) > 10 else 0.011
    tamanho = min((maxw - (w-1)*gap)/w, (maxh - (h-1)*gap)/h)
    tamanho = max(0.001, tamanho)
    totalw = w*tamanho + (w-1)*gap
    totalh = h*tamanho + (h-1)*gap
    esquerda = cx-totalw/2
    topo = cy+totalh/2
    bg = (0.11,0.16,0.21)
    vert = []
    for row in range(h):
        for col in range(w):
            x0 = esquerda + col*(tamanho+gap)
            y1 = topo - row*(tamanho+gap)
            _retangulo(vert, x0, y1-tamanho, x0+tamanho, y1,
                       cor if imagem[row, col] else bg)
    return np.asarray(vert, dtype=np.float32)


def unir(*partes):
    return np.concatenate([p for p in partes if p.size], axis=0) \
        if any(p.size for p in partes) else np.empty((0,), dtype=np.float32)


def construir_cena():
    original = imagem_binaria(FIGURA)
    se = elemento_estruturante(KERNEL)
    esqueleto_cor = (1.0, 0.73, 0.20)
    if MODO == 1:
        return painel_matriz(original,0,0,1.75,1.68)
    if MODO == 2:
        # O SE e exibido ampliado e com uma borda falsa de 0.
        elemento_ampliado = np.pad(se, 2, constant_values=False)
        return unir(
            painel_matriz(original,-0.52,0,0.94,1.55),
            painel_matriz(elemento_ampliado,0.60,0,0.78,0.78,cor=esqueleto_cor),
        )
    if MODO == 3:
        imagem = erosao(original, se)
    elif MODO == 4:
        imagem = dilatacao(original, se)
    elif MODO == 5:
        imagem = abertura(original, se)
    elif MODO == 6:
        imagem = fechamento(original, se)
    elif MODO in (7, 8, 9, 0):
        etapas, camadas = construir_camadas_esqueleto(original, se)
        if MODO == 7:
            index = min(ETAPA, len(etapas)-1)
            imagem = etapas[index]
        elif MODO == 8:
            index = min(ETAPA, len(camadas)-1)
            imagem = (camadas[index] if camadas
                      else np.zeros_like(original))
        else:
            imagem = np.zeros_like(original)
            for camada in camadas:
                imagem = np.logical_or(imagem, camada)
            if MODO == 0:
                return unir(
                    painel_matriz(original,-0.64,0,0.54,1.25),
                    painel_matriz(abertura(original,se),0,0,0.54,1.25),
                    painel_matriz(imagem,0.64,0,0.54,1.25,cor=esqueleto_cor),
                )
    else:
        imagem = original
    return painel_matriz(imagem,0,0,1.75,1.68,
                          cor=esqueleto_cor if MODO in (8,9) else (0.20,0.82,0.78))


def compilar_shader(codigo, tipo):
    shader = glCreateShader(tipo)
    glShaderSource(shader,codigo)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        erro = glGetShaderInfoLog(shader)
        glDeleteShader(shader)
        raise RuntimeError(f'Erro no shader: {erro}')
    return shader


def programa_shaders():
    vs = compilar_shader(VERTEX_SHADER,GL_VERTEX_SHADER)
    fs = compilar_shader(FRAGMENT_SHADER,GL_FRAGMENT_SHADER)
    prog=glCreateProgram()
    glAttachShader(prog,vs)
    glAttachShader(prog,fs)
    glLinkProgram(prog)
    if not glGetProgramiv(prog,GL_LINK_STATUS):
        erro=glGetProgramInfoLog(prog)
        glDeleteProgram(prog)
        raise RuntimeError(f'Erro no programa: {erro}')
    glDeleteShader(vs)
    glDeleteShader(fs)
    return prog


def criar_geometria():
    vao=glGenVertexArrays(1)
    vbo=glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER,vbo)
    glBufferData(GL_ARRAY_BUFFER,0,None,GL_DYNAMIC_DRAW)
    passo=5*np.dtype(np.float32).itemsize
    glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,passo,ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,passo,ctypes.c_void_p(8))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER,0)
    return vao,vbo


def ajuda():
    print('\n--- Esqueletizacao: teclas ---')
    for k in range(10):
        print(f'{k}: {MODOS[k]}')
    print('ESPACO: alternar SE cruz/quadrado')
    print('T: alternar figura B/anel')
    print('[ e ]: escolher etapa de erosao/camada')
    print('H: ajuda | ESC: sair\n')


def titulo(janela):
    adicional = f' | SE={KERNEL} | figura={FIGURA}'
    if MODO in (7,8):
        adicional += f' | etapa={ETAPA}'
    glfw.set_window_title(janela,f'Morfologia e Esqueletizacao | {MODO}: {MODOS[MODO]}' + adicional)


def teclado(janela, tecla, scan, acao, modificadores):
    global MODO,KERNEL,FIGURA,ETAPA,SUJO
    if acao not in (glfw.PRESS,glfw.REPEAT):
        return
    if tecla == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(janela,True)
        return
    if acao == glfw.PRESS:
        mapa={glfw.KEY_0:0,glfw.KEY_1:1,glfw.KEY_2:2,
              glfw.KEY_3:3,glfw.KEY_4:4,glfw.KEY_5:5,
              glfw.KEY_6:6,glfw.KEY_7:7,glfw.KEY_8:8,
              glfw.KEY_9:9,
              glfw.KEY_KP_0:0,glfw.KEY_KP_1:1,glfw.KEY_KP_2:2,
              glfw.KEY_KP_3:3,glfw.KEY_KP_4:4,glfw.KEY_KP_5:5,
              glfw.KEY_KP_6:6,glfw.KEY_KP_7:7,glfw.KEY_KP_8:8,
              glfw.KEY_KP_9:9}
        if tecla in mapa:
            MODO=mapa[tecla]
            ETAPA=0
            SUJO=True
        elif tecla == glfw.KEY_SPACE:
            KERNEL = 'quadrado' if KERNEL=='cruz' else 'cruz'
            ETAPA=0
            SUJO=True
        elif tecla == glfw.KEY_T:
            FIGURA = 'anel' if FIGURA=='B' else 'B'
            ETAPA=0
            SUJO=True
        elif tecla == glfw.KEY_H:
            ajuda()
    if tecla in (glfw.KEY_LEFT_BRACKET,glfw.KEY_KP_SUBTRACT):
        ETAPA=max(0,ETAPA-1)
        SUJO=True
    elif tecla in (glfw.KEY_RIGHT_BRACKET,glfw.KEY_KP_ADD):
        ETAPA+=1
        SUJO=True
    if SUJO:
        titulo(janela)
        print(f'Modo {MODO}: {MODOS[MODO]} | SE {KERNEL} | figura {FIGURA} | etapa {ETAPA}')


def executar():
    global SUJO
    if not glfw.init():
        raise RuntimeError('GLFW nao inicializou. Verifique sistema grafico/drivers.')
    try:
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,3)
        glfw.window_hint(glfw.OPENGL_PROFILE,glfw.OPENGL_CORE_PROFILE)
        if sys.platform == 'darwin':
            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT,glfw.TRUE)
        janela=glfw.create_window(LARGURA,ALTURA,'Morfologia e Esqueletizacao',None,None)
        if not janela:
            raise RuntimeError('Janela OpenGL 3.3 nao criada.')
        glfw.make_context_current(janela)
        glfw.swap_interval(1)
        glfw.set_key_callback(janela,teclado)
        titulo(janela)
        prog=programa_shaders()
        vao,vbo=criar_geometria()
        ajuda()
        vertices=np.empty((0,),dtype=np.float32)
        while not glfw.window_should_close(janela):
            glfw.poll_events()
            if SUJO:
                vertices=construir_cena()
                glBindBuffer(GL_ARRAY_BUFFER,vbo)
                glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_DYNAMIC_DRAW)
                glBindBuffer(GL_ARRAY_BUFFER,0)
                SUJO=False
            glViewport(0,0,LARGURA,ALTURA)
            glClearColor(0.045,0.065,0.09,1.0)
            glClear(GL_COLOR_BUFFER_BIT)
            glUseProgram(prog)
            glBindVertexArray(vao)
            glDrawArrays(GL_TRIANGLES,0,vertices.size//5)
            glBindVertexArray(0)
            glfw.swap_buffers(janela)
        glDeleteBuffers(1,[vbo])
        glDeleteVertexArrays(1,[vao])
        glDeleteProgram(prog)
        glfw.destroy_window(janela)
    finally:
        glfw.terminate()


if __name__ == '__main__':
    executar()
