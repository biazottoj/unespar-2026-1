import glfw
from OpenGL.GL import *

pontos = []
cor = {"r":1.0, "g":1.0, "b":1.0}

def converter_para_opengl(x_mouse, y_mouse, window):
    largura, altura = glfw.get_window_size(window)
    x = (x_mouse/largura) * 2 - 1
    y = 1 - (y_mouse/altura) * 2

    return (x, y)

def atualizar_viewport(window):
    largura, altura = glfw.get_framebuffer_size(window)
    glViewport(0, 0, largura, altura)

def mouse_button_callback(window, button, action, mods):
    if(button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS):
        x_mouse, y_mouse = glfw.get_cursor_pos(window)
        x,y =  converter_para_opengl(x_mouse, y_mouse, window)
        if len(pontos) < 3:
            pontos.append((x, y))

def key_callback(window, key, scancode, action, mods):
    global cor
    if(action == glfw.PRESS or action == glfw.REPEAT):
        if(key == glfw.KEY_ESCAPE):
            glfw.set_window_should_colse(window, True)
            
        if(key == glfw.KEY_R):
            cor = {"r":1.0, "g":0.0, "b":0.0}

        if(key == glfw.KEY_G):
            cor = {"r":0.0, "g":1.0, "b":0.0}

        if(key == glfw.KEY_B):
            cor = {"r":0.0, "g":0.0, "b":1.0}
    
    print(cor)

def desenhar_triangulo():
    if len(pontos) == 3:
        glColor3f(cor["r"], cor["g"], cor["b"])
        glBegin(GL_TRIANGLES)
        for p in pontos:
            glVertex2f(p[0], p[1])
        glEnd()

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
        
        desenhar_triangulo()
        desenhar_pontos()

        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()