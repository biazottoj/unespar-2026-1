import glfw
from OpenGL.GL import *

pontos = []
cor = {"r":1.0, "g":1.0, "b":1.0}

objetos = []

def criar_triangulo(x, y):
    largura = 0.25
    altura = 0.3

    return [(x, y), 
            (x - largura, y - altura), 
            (x + largura, y - altura)]


def criar_quadrado(x, y):
    largura = 0.25
    altura = 0.25

    return [(x, y), 
            (x + largura, y), 
            (x, y - altura),
            (x + largura, y - altura)]

def desenhar_quadrado(x, y):
    quadrado = criar_quadrado(x, y)
    print(quadrado)
    glColor3f(cor["r"],cor["g"], cor["b"])  
    glBegin(GL_QUADS)
    glVertex2f(quadrado[0][0], quadrado[0][1])
    glVertex2f(quadrado[1][0], quadrado[1][1])
    glVertex2f(quadrado[2][0], quadrado[1][1])
    glVertex2f(quadrado[3][0], quadrado[0][1])

    glEnd()

def desenhar_triangulo(x, y):
    triangulo = criar_triangulo(x, y)
    
    glBegin(GL_TRIANGLES)

    glColor3f(cor["r"], cor["g"], cor["b"])
    glVertex2f(triangulo[0][0], triangulo[0][1])
    glVertex2f(triangulo[1][0], triangulo[1][1])
    glVertex2f(triangulo[2][0], triangulo[2][1])
    glEnd()

def converter_para_opengl(x_mouse, y_mouse, window):
    largura, altura = glfw.get_window_size(window)
    x = (x_mouse/largura) * 2 - 1
    y = 1 - (y_mouse/altura) * 2

    return (x, y)

def atualizar_viewport(window):
    largura, altura = glfw.get_framebuffer_size(window)
    glViewport(0, 0, largura, altura)

def desenhar_objetos():
    if len(objetos) == 0:
        return
    for objeto in objetos:
        if objeto["forma"] == "triangulo":
            desenhar_triangulo(objeto["x"], objeto["y"])
        
        if objeto["forma"] == "quadrado":
            print("desenhando quadrado")
            desenhar_quadrado(objeto["x"], objeto["y"])

def mouse_button_callback(window, button, action, mods):
    if(button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS):
        x_mouse, y_mouse = glfw.get_cursor_pos(window)
        x,y =  converter_para_opengl(x_mouse, y_mouse, window)
        objetos.append(
            {"forma":forma_atual, "x":x, "y":y, "cor":cor}
        )
    if(button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS):
        objetos.clear()
    
    print(objetos)

def mover_ultima_forma(dx, dy):
    if len(objetos) == 0:
        return
    
    objetos[-1]["x"] += dx  
    objetos[-1]["y"] += dy

def key_callback(window, key, scancode, action, mods):
    global cor
    global forma_atual
    if(action == glfw.PRESS or action == glfw.REPEAT):
        if(key == glfw.KEY_ESCAPE):
            glfw.set_window_should_colse(window, True)
            
        if(key == glfw.KEY_R):
            cor = {"r":1.0, "g":0.0, "b":0.0}

        if(key == glfw.KEY_G):
            cor = {"r":0.0, "g":1.0, "b":0.0}

        if(key == glfw.KEY_B):
            cor = {"r":0.0, "g":0.0, "b":1.0}
        
        if(key == glfw.KEY_Y):
            cor = {"r":1.0, "g":1.0, "b":0.0}
        
        if(key == glfw.KEY_M):
            cor = {"r":1.0, "g":0.0, "b":1.0}
        
        if(key == glfw.KEY_W):
            cor = {"r":1.0, "g":1.0, "b":1.0}
        
        if(key == glfw.KEY_P):
            forma_atual = "ponto"
        
        if(key == glfw.KEY_L):
            forma_atual = "linha"

        if(key == glfw.KEY_T):
            forma_atual = "triangulo"

        if(key == glfw.KEY_Q):
            forma_atual = "quadrado"

        if(key == glfw.KEY_C):
            objetos.clear()

        if(key == glfw.KEY_LEFT):
            mover_ultima_forma(-0.05,0.0)
            return
        
        if(key == glfw.KEY_RIGHT):
            mover_ultima_forma(0.05,0.0)
            return
        
        if(key == glfw.KEY_UP):
            mover_ultima_forma(0.0,0.05)
            return
        
        if(key == glfw.KEY_DOWN):
            mover_ultima_forma(0.0,-0.05)
            return

    print(cor)
    print(forma_atual)

def desenhar_pontos():
    glPointSize(8)
    glColor3f(1.0,1.0,1,0)
    glBegin(GL_POINTS)
    for p in pontos:
        glVertex2f(p[0], p[1])
    glEnd()

def main():
    if not glfw.init():
        print("Erro ao inicializar o GLFW.")
        return
    
    window = glfw.create_window(800, 600, "Triangulo com Eventos de Mouse e Teclado", 
    None, None)

    if not window:
        print("Erro ao criar a janela principal.")
        return

    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window,mouse_button_callback)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        atualizar_viewport(window)

        glClear(GL_COLOR_BUFFER_BIT)
        
        desenhar_objetos()

        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()