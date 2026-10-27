"""
Computacao Grafica - Convolucao 2D: Naruto em matriz RGB com Python e OpenGL.

Dependencias: pip install numpy glfw PyOpenGL
Execucao: python convolucao_naruto_base_aula_alinhado.py

O processamento dos pixels acontece no NumPy, em CPU.
O OpenGL desenha o resultado como uma grade de quadrados coloridos.

TECLAS
 1 original | 2 media | 3 gaussiano | 4 nitidez
 5 Sobel X | 6 Sobel Y | 7 magnitude das bordas
 8 comparacao original/media/gauss
 9 comparacao original/nitidez/bordas
 B alternar contorno | T Naruto limpo/com ruido | +/- media 3x3/5x5
 H ajuda | Esc sair
"""
import ctypes
import sys
import numpy as np

# As importacoes graficas foram mantidas no inicio. Os algoritmos de
# imagem podem ser testados sem inicializar a janela OpenGL.
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

WINDOW_W, WINDOW_H = 1120, 760
MODE = 1
BORDER = 'refletir'
IMAGE_INDEX = 0
MEAN_SIZE = 3
DIRTY = True

MODES = {
    1: 'Imagem original',
    2: 'Filtro media (box blur)',
    3: 'Filtro Gaussiano',
    4: 'Realce de nitidez',
    5: 'Bordas Sobel X',
    6: 'Bordas Sobel Y',
    7: 'Magnitude das bordas',
    8: 'Comparacao: original / media / gauss',
    9: 'Comparacao: original / nitidez / bordas',
}

VERTEX_SHADER = """#version 330 core
layout (location = 0) in vec2 aPos;
layout (location = 1) in vec3 aColor;
out vec3 vColor;
void main() {
    gl_Position = vec4(aPos, 0.0, 1.0);
    vColor = aColor;
}
"""

FRAGMENT_SHADER = """#version 330 core
in vec3 vColor;
out vec4 FragColor;
void main() { FragColor = vec4(vColor, 1.0); }
"""


# ==============================================================
# IMAGEM DE NARUTO CONSTRUIDA INTEIRAMENTE COMO MATRIZ NUMPY
# ==============================================================
# Paleta: cada simbolo identifica uma cor [R, G, B] entre 0 e 255.
# O mapa abaixo tem 64 linhas x 64 colunas: um simbolo por pixel.
# A imagem final sera uma matriz NumPy de formato (64, 64, 3).
#
# Exemplo de leitura: MAPA_NARUTO[0][0] e o simbolo do pixel (0,0),
# e PALETA_NARUTO[simbolo] fornece os tres canais RGB desse pixel.

PALETA_NARUTO = {
    '0': (  1,   2,   3),
    '1': (  4,   7,  12),
    '2': (244, 174, 124),
    '3': (242, 184,  30),
    '4': (242, 189,  38),
    '5': (  0,   2,   3),
    '6': (  4,   7,  11),
    '7': (236, 100,  29),
    '8': (  1,   3,   4),
    '9': ( 96,  51,  21),
    'A': ( 25,  27,  31),
    'B': ( 21,  23,  25),
    'C': (186, 105,  44),
    'D': (  1,   2,   4),
    'E': ( 16,  19,  22),
    'F': (189,  84,  28),
    'G': (230, 216, 178),
    'H': (  2,   2,   3),
    'I': (107,  73,  43),
    'J': ( 39,  29,  23),
    'K': ( 10,  10,  11),
    'L': (164, 134, 102),
    'M': ( 19,  13,  12),
    'N': (218, 138,  58),
    'O': ( 38,  34,  32),
    'P': (112,  91,  65),
    'Q': (  0,   0,   0),
    'R': (  4,  10,  14),
    'S': (241, 167,  92),
    'T': (  1,   1,   2),
    'U': (  1,   3,   3),
    'V': ( 41,  53,  62),
    'W': (  3,   5,   7),
    'X': (  2,   5,   9),
    'Y': (  4,   5,   8),
    'Z': ( 27,  22,  21),
    'a': (  1,   2,   2),
    'b': (  6,   8,  10),
    'c': (  0,   4,   8),
    'd': (  0,   1,   5),
    'e': (  0,   2,   6),
    'f': (242, 194,  49),
    'g': (  0,   2,   2),
    'h': (240, 149,  67),
    'i': (227, 182,  62),
}

MAPA_NARUTO = (
    '11116XXXXXXXXX6XXX6666666XX6666bXeXX66666b6X666XXXXXXX6X66661111',
    '11168D88888DD88D8888TRRQD808cWWTJCJQW888ddRbD8888D88888888886111',
    '1116D800800U0805055aQJ9KKYDaTWMJI39DUaHHZ9JKaU0808D0U8DDDDD86111',
    '111605000585000TTT0HTC3FZcTQQQM344I1UQQeIfI1H8D000000UD8UDD86111',
    '1116505550050UU0T0DKMNf3IJeHH9I44fCJWM9IC39cUU000080T500050D6111',
    '1116050000000T50UHTKZN433CBMK3f44479c934339TH8005T00000000D86111',
    '1116U0000000YMKKbUQM9N3333NCF343443CC4443N98HWWH8H05000000886111',
    '11165T000085KF9BKXQM933444377333343N34443791ddccKEW0000000086111',
    '11165g05050QKOCCCC9FC344433333444433344437FIFCCCIEWT000500D86111',
    '1116D555080QKBi443CN7344433344444433344437773443CEYT000T000U6111',
    '11160a00500aKEC3ff433333f4334333443344433333443F9DH0500088006111',
    '1116Ha0000DTKEC3f4333333f433333333334443333333N9JQH0Ta5000006111',
    '1116055UHHHUbMCN334333344433333333333333333337FWUHHHTg0000D06111',
    '11165Taddddc1RFN444433343333343333333333333337FccedQQa550D556111',
    '11165UeJ999IIIC3444443333333344443333333333333CIII99MDH008U06111',
    '11160HX9334f44334444444443333444443333444444444f4337JeH550506111',
    '11160HeJ9CN3334444444433443333444433333344444333NNI9MDU058006111',
    '11165DQTdF7N344444444433444444444443334344444337779QT00050506111',
    '111600TaHJ973443N34433IJIIII999999999IN3443N3337FJMHH0055g006111',
    '1116550HYdJ7333373443N9XAAAAAAAAAAAAEJ7343NC7337IQHa000g0a006111',
    '11165Da8cFN73339C344NZZEEBZBBBBAABBEBEJ7333I9777FFMQH800U0006111',
    '1116D8dZ9C7CN3COC33NCOVPPPPPPPPVPPPPPVVFN33CJ7FFFF9M08D000006111',
    '11168DZIh7FF7CEO73491PLGGGGGGGGGLLGGGLPcF33CcFFMF779TU0005506111',
    '1116H5JI99I7I9EJCN39OLLGGGGGLVVVPGGGGLLE9F3Cc9999999K58055a06111',
    '111655ecccMF9RBZC7NJVLGGGGGLVLLPLGGGGGLAZ97FcREIJdde800500006111',
    '111605HYY9F9MZBJ7FJJVLLGGGGVLPPPGGGGGGLAZMFIRAAM9MHWD00005006111',
    '111600THHI7JROBJC9XBVLLGGGLBPPLOLGGGGGLAB1IIEABTF9YUU0D005006111',
    '111600HQ9FIJEOOAZZBBOLLGGGGPOVVPGGGGGLPBAABBAABT97JT805000056111',
    '111600Hd9FM6BOOAEBOBOPLLGLLLLLLLLLGLLPPAOABAAAAYKJKT000000006111',
    '11160U0DYKX8EAEAABAABERc6RRREEEERRRR1REBAEBBEAAW5TT0T05000086111',
    '1116D88U55aHKM99J99JMJJPPPPPPPPPIIPPPJKJJ9JJ9JEYHUaT0055800U6111',
    '1116D55500QQQHFFCSShCIFh2222222222G2hFFCh2NF3JQQQa00055805506111',
    '1116055505M99OFCNNLII99ICSS22222S2NI9999PLSN399IJQU0H00805086111',
    '111600058QJh2LC32IMVAEEE9FCS2222NFFZQAEVVQLh7IN2IQH0005550506111',
    '11168088WQJSC9CN2PVGLVPAVIFS2222SCIVVVVGGJLNC9I2IQHU050050T06111',
    '1116UD00WQJ2PZF72NLGLVOVGGSS22222SGPVKVGGNSC7JO2PQ8000500TT06111',
    '11160DD88QJ2CI9F2S2GLVVVGG222222S2GPVVVGGS2CF9F2IQW0DD5055006111',
    '111600DDHQJSNF9F222GLVVVGG22222222GLVVVGG22C9IC2IQW08U0T05006111',
    '111680000QM9CSII2222SLLS222222222222SNNS22SCICCC9QH0D0000D086111',
    '1116808008YQPSCCS2222222222222222222222222SCCNCMb5DDa08808886111',
    '11160800D8YQP2SNNNCLL22222222222222222NNNNNCSSCQa0D08000880D6111',
    '1116DU00D88TOIII9CNCC2222222S22S222222NNNNI9II9TH0D000DD00006111',
    '1116D08UD5U5QQQTHN2222222222NNCS2222222222IQQQQ00800000DU0806111',
    '11168D0080D5HWb9HP2CPS2222222SS2222222CCNS9JMHH0000080U8DU886111',
    '11160058085a081I9ICCN22222222222222222SCICJ9Me8U05D8050080086111',
    '1116808800050Hc97JZ22S222SSSSSNSSN222SS2CQ9FKW08050D5058HDD06111',
    '1116U0DU80050aDJF9JPLN222NCCCCCNNC222SCCI9I9bbW00D0T005500506111',
    '11160D0580D5D5UDFFJQZS2222222222222222CQMFFdbKK0U55808D000086111',
    '11168D0UD05508aH9JMbZPCS222222222222SCIKMJ9WWKKbW50U50058D506111',
    '1116008055DU080adRBEKQJCNS22222222SNCMeEE1eW0bKKYQ00800008D06111',
    '111655055555080DBABKW99ZJIS22222Sh9ZJ9KEEAMYU8WKKb00880U50006111',
    '1116D085505T0T08EBEKK9JRTJCCLLLLCCZTKJYMEAEY0aHbKKW00U5005506111',
    '11160055505T0T08EBAAAEEAMbKKYHKMKcEBEREAAAEbTTTWKMK8000000006111',
    '1116D055500055g5KBAAABBABBAEKIIKZABAAEBBEAEWQQ5WYKKW0000g0006111',
    '11160g000005HHHYKBBBABAOBAAKKCPeEABAOEBBEAMYYHYHWKKY00U005g06111',
    '1116500555HK9FFIKBBBAEAOBBAKEGLbBOBBOEABMBRJF99HWYYW000U0T506111',
    '111600HHHHYZF77FYEBAOBAAEBOEAGGbAOEBOEAAMBR9FFFHaHHHD000D0506111',
    '11160HdJFFFF777FRREAOBAAEBOBALLYBOEBOBAAEEX9777FFF910H8000006111',
    '1116DHJ9777777779JRAABAAEBAEEPPKBOBBOBAAEKJ9777777F9MDT088006111',
    '1111EB9F777777777FKEKKEAEBABBPVBAOBBBEEEZJF777777777JEEY085T6111',
    '116ROOR97777777777FJMHWYKKKBAPPBBKEMHbMZ9F777777777FOOOEWW806111',
    '116ROOOOJ77777777777FABEBBBBBLLKEEEBABOF77777777779ZOOOOOOE51111',
    '116ROOOAEF7777777777FAAOAAOABLLKBAAAOAOF77777777779EOOOOOOBb1111',
    '1111RRRR1KMMMMMMMMMMMRRRRRRRRABRRRRRRRKMMMMMMMMMMM1RRRRRRRRR1111',
)


def criar_imagem_exemplo(indice=0):
    """Cria Naruto em pixel art so com matriz/paleta; sem PNG ou Pillow.

    indice=0: imagem original; indice=1: mesma imagem com ruido.
    """
    imagem = np.zeros((64, 64, 3), dtype=np.float32)

    # Transformar a matriz de simbolos em matriz RGB.
    for linha, texto in enumerate(MAPA_NARUTO):
        for coluna, simbolo in enumerate(texto):
            imagem[linha, coluna] = PALETA_NARUTO[simbolo]

    # Converter RGB de 0..255 para 0..1, formato usado nos shaders.
    imagem /= 255.0

    if indice == 1:
        rng = np.random.default_rng(7)
        # Ruido reproduzivel, sem alterar os pixels da imagem original.
        imagem = np.clip(imagem + rng.normal(0, 0.09, imagem.shape), 0, 1)
        h, w, _ = imagem.shape
        ys = rng.integers(0, h, 70)
        xs = rng.integers(0, w, 70)
        imagem[ys, xs] = rng.integers(0, 2, (70, 1))
    return imagem.astype(np.float32)


def para_cinza(image):
    """Retorna um canal de luminosidade; aplica Sobel a ele."""
    return (0.299 * image[..., 0] + 0.587 * image[..., 1]
            + 0.114 * image[..., 2]).astype(np.float32)


def cinza_para_rgb(gray):
    return np.repeat(gray[..., None], 3, axis=2)

# ==============================================================
# ETAPAS A COMPLETAR DURANTE A AULA
# Estas funcoes ainda NAO executam os filtros indicados.
# Retornos provisórios mantem todos os modos de teclado navegaveis.
# ==============================================================

def kernel_media(tamanho=3):
    """TODO 2: criar matriz tamanho x tamanho, valores 1/tamanho**2."""
    # TODO: implementar a media normalizada (3x3 e 5x5)
    kernel = np.zeros((tamanho, tamanho), dtype=np.float32)
    kernel[tamanho // 2, tamanho // 2] = 1.0  # provisoriamente, identidade
    return kernel


def kernel_gaussiano():
    return np.array([[1, 2, 1], 
                     [2, 4, 2], 
                     [1, 2, 1]], dtype=np.float32) / 16


def kernel_nitidez():
    """TODO 4: centro=5, vizinhos ortogonais=-1, demais=0."""
    # TODO: implementar filtro de nitidez
    return np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float32)


def kernel_sobel_x():
    """TODO 5: detectar variacao horizontal com pesos -1,-2,1,2."""
    # TODO: implementar mascara Sobel X
    return np.zeros((3, 3), dtype=np.float32)


def kernel_sobel_y():
    """TODO 6: detectar variacao vertical."""
    # TODO: implementar mascara Sobel Y
    return np.zeros((3, 3), dtype=np.float32)


def aplicar_convolucao_2d(canal, kernel, contorno='refletir'):
    canal = np.asarray(canal, dtype=np.float32)
    kernel = np.asarray(kernel, dtype=np.float32)
    kh, kw = kernel.shape
    py, px = kh // 2, kw // 2

    modos = {
        'zero': 'constant',
        'replicar': 'edge',
        'refletir': 'reflect'
    }

    extendido = np.pad(
        canal, ((py, py), (px, px)),
        mode = modos[contorno]
    )

    kernel_invertido = np.flip(kernel, axis = (0,1))

    height, width = canal.shape
    saida = np.zeros((height, width), dtype=np.float32)

    for row in range(height):
        for col in range(width):
            vizinhos = extendido[row:row + kh, col : col + kw]
            saida[row, col] = np.sum(vizinhos * kernel_invertido)

    return saida


def aplicar_kernel_rgb(image, kernel, contorno='refletir'):
    """Infraestrutura pronta: processa R, G e B separadamente."""
    channels = [aplicar_convolucao_2d(image[..., c], kernel, contorno)
                for c in range(3)]
    return np.stack(channels, axis=2)


def filtro_bordas(image, contorno='refletir', eixo='magnitude'):
    """TODO 7: aplicar Sobel X e Y ao canal cinza.

    Calcular |Gx|, |Gy| ou sqrt(Gx**2 + Gy**2), dividir por 4,
    limitar entre 0 e 1 e repetir o canal para exibir como RGB.
    """
    # TODO: substituir pelo calculo do gradiente. Ainda nao detecta bordas.
    return image.copy()

# ==============================================================
# INFRAESTRUTURA OPENGL - PRONTA NOS DOIS ARQUIVOS
# ==============================================================

def gerar_versao(image, modo, contorno, tamanho_media):
    if modo == 1:
        return image.copy()
    if modo == 2:
        return aplicar_kernel_rgb(image, kernel_media(tamanho_media), contorno)
    if modo == 3:
        return aplicar_kernel_rgb(image, kernel_gaussiano(), contorno)
    if modo == 4:
        return aplicar_kernel_rgb(image, kernel_nitidez(), contorno)
    if modo == 5:
        return filtro_bordas(image, contorno, 'x')
    if modo == 6:
        return filtro_bordas(image, contorno, 'y')
    if modo == 7:
        return filtro_bordas(image, contorno, 'magnitude')
    raise ValueError('gerar_versao espera modo de 1 a 7.')


def imagens_do_modo(image):
    if MODE == 8:
        return [gerar_versao(image, m, BORDER, MEAN_SIZE) for m in (1, 2, 3)]
    if MODE == 9:
        return [gerar_versao(image, m, BORDER, MEAN_SIZE) for m in (1, 4, 7)]
    return [image, gerar_versao(image, MODE, BORDER, MEAN_SIZE)]


def acrescentar_retangulo(vertices, x0, y0, x1, y1, color):
    r, g, b = color
    vertices.extend([
        x0, y0, r, g, b,  x1, y0, r, g, b,  x1, y1, r, g, b,
        x0, y0, r, g, b,  x1, y1, r, g, b,  x0, y1, r, g, b,
    ])


def acrescentar_painel(vertices, image, cx, cy, panel_width=0.78, panel_height=1.42):
    h, w, _ = image.shape
    pixel_size = min(panel_width / w, panel_height / h)
    start_x = cx - w * pixel_size / 2
    start_y = cy + h * pixel_size / 2
    for row in range(h):
        y1 = start_y - row * pixel_size
        y0 = y1 - pixel_size
        for col in range(w):
            x0 = start_x + col * pixel_size
            x1 = x0 + pixel_size
            acrescentar_retangulo(vertices, x0, y0, x1, y1, image[row, col])


def vertices_da_cena(image):
    images = imagens_do_modo(image)
    vertices = []
    if len(images) == 2:
        positions = (-0.50, 0.50)
        width = 0.87
    else:
        positions = (-0.64, 0.0, 0.64)
        width = 0.56
    for pic, x in zip(images, positions):
        acrescentar_painel(vertices, pic, x, 0.0, width, 1.35)
    return np.asarray(vertices, dtype=np.float32)


def compilar_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        message = glGetShaderInfoLog(shader)
        glDeleteShader(shader)
        raise RuntimeError(f'Erro no shader: {message}')
    return shader


def criar_programa():
    vs = compilar_shader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fs = compilar_shader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    glAttachShader(program, vs)
    glAttachShader(program, fs)
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        message = glGetProgramInfoLog(program)
        glDeleteProgram(program)
        raise RuntimeError(f'Erro no link: {message}')
    glDeleteShader(vs)
    glDeleteShader(fs)
    return program


def criar_vao_vbo():
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, 0, None, GL_DYNAMIC_DRAW)
    item = np.dtype(np.float32).itemsize
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * item, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * item, ctypes.c_void_p(2 * item))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vao, vbo


def imprimir_ajuda():
    print('\n=== CONVOLUCAO 2D / NUMPY + OPENGL ===')
    for key, label in MODES.items():
        print(f'{key}: {label}')
    print('B: borda zero / replicar / refletir')
    print('T: alternar Naruto limpo / com ruido')
    print('+ ou -: tamanho media 3x3 / 5x5')
    print('H: ajuda | ESC: sair')
    print('Os painéis seguem a ordem indicada pelo modo;')
    print('nos modos 1-7: esquerda=original, direita=resultado.')
    print('No codigo BASE, funcoes TODO nao apresentam filtragem verdadeira.\n')


def atualizar_titulo(window):
    glfw.set_window_title(window,
        f'Convolucao 2D | {MODE}: {MODES[MODE]} | '
        f'contorno={BORDER} | Naruto={"ruidoso" if IMAGE_INDEX else "limpo"} | media={MEAN_SIZE}x{MEAN_SIZE}')


def teclado(window, key, scancode, action, mods):
    global MODE, BORDER, IMAGE_INDEX, MEAN_SIZE, DIRTY
    if action != glfw.PRESS:
        return
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
        return
    numero = {
        glfw.KEY_1: 1, glfw.KEY_2: 2, glfw.KEY_3: 3,
        glfw.KEY_4: 4, glfw.KEY_5: 5, glfw.KEY_6: 6,
        glfw.KEY_7: 7, glfw.KEY_8: 8, glfw.KEY_9: 9,
        glfw.KEY_KP_1: 1, glfw.KEY_KP_2: 2, glfw.KEY_KP_3: 3,
        glfw.KEY_KP_4: 4, glfw.KEY_KP_5: 5, glfw.KEY_KP_6: 6,
        glfw.KEY_KP_7: 7, glfw.KEY_KP_8: 8, glfw.KEY_KP_9: 9,
    }
    if key in numero:
        MODE = numero[key]
    elif key == glfw.KEY_B:
        options = ('zero', 'replicar', 'refletir')
        BORDER = options[(options.index(BORDER) + 1) % 3]
    elif key == glfw.KEY_T:
        IMAGE_INDEX = 1 - IMAGE_INDEX
    elif key in (glfw.KEY_EQUAL, glfw.KEY_KP_ADD):
        MEAN_SIZE = 5
    elif key in (glfw.KEY_MINUS, glfw.KEY_KP_SUBTRACT):
        MEAN_SIZE = 3
    elif key == glfw.KEY_H:
        imprimir_ajuda()
        return
    else:
        return
    DIRTY = True
    atualizar_titulo(window)
    print(f'Modo {MODE}: {MODES[MODE]} | contorno={BORDER} | '
          f'Naruto={"ruidoso" if IMAGE_INDEX else "limpo"} | media={MEAN_SIZE}x{MEAN_SIZE}')


def main():
    global DIRTY
    if not glfw.init():
        raise RuntimeError('Falha ao inicializar GLFW. Requer sistema com display grafico.')
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    if sys.platform == 'darwin':
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    window = glfw.create_window(WINDOW_W, WINDOW_H, 'Convolucao 2D', None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError('Falha ao criar janela OpenGL 3.3 Core.')
    glfw.make_context_current(window)
    glfw.set_key_callback(window, teclado)
    program = criar_programa()
    vao, vbo = criar_vao_vbo()
    glViewport(0, 0, WINDOW_W, WINDOW_H)
    atualizar_titulo(window)
    imprimir_ajuda()
    numero_vertices = 0
    try:
        while not glfw.window_should_close(window):
            glfw.poll_events()
            if DIRTY:
                image = criar_imagem_exemplo(IMAGE_INDEX)
                vertices = vertices_da_cena(image)
                glBindBuffer(GL_ARRAY_BUFFER, vbo)
                glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
                glBindBuffer(GL_ARRAY_BUFFER, 0)
                numero_vertices = len(vertices) // 5
                DIRTY = False
            glClearColor(0.07, 0.075, 0.10, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)
            glUseProgram(program)
            glBindVertexArray(vao)
            glDrawArrays(GL_TRIANGLES, 0, numero_vertices)
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
