from OpenGL.GL import *
import glfw

triangulo = None

def atualizar_viewport(window):
    largura, altura = glfw.get_framebuffer_size(window)
    glViewport(0, 0, largura, altura)

def criar_triangulo(x, y):
    largura = 0.25
    altura = 0.3

    return [(x, y), 
            (x - largura, y - altura), 
            (x + largura, y - altura)]

def desenhar_triangulo():
    if triangulo is None:
        return
    
    glBegin(GL_TRIANGLES)

    glColor3f(1.0,0.0,0.0)
    glVertex2f(triangulo[0][0], triangulo[0][1])

    glColor3f(0.0,1.0,0.0)
    glVertex2f(triangulo[1][0], triangulo[1][1])

    glColor3f(0.0,0.0,1.0)
    glVertex2f(triangulo[2][0], triangulo[2][1])
    glEnd()

def converter_para_opengl(x_mouse, y_mouse, largura, altura):
    x = (x_mouse/largura) * 2 - 1
    y = 1 - (y_mouse/altura) * 2

    return (x, y)


def clique_mouse(window, button, action, mods):
    global triangulo
    if(button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS):
        x_mouse, y_mouse = glfw.get_cursor_pos(window)
        largura, altura = glfw.get_window_size(window)
        x, y = converter_para_opengl(x_mouse, y_mouse, largura, altura)
        triangulo = criar_triangulo(x, y)


def main():
    if not glfw.init():
        print("Erro ao inicializar o GLFW")
        return

    largura = 800
    altura = 600

    window = glfw.create_window(
        largura,
        altura,
        "Triângulo com clique - GLFW",
        None,
        None
    )

    if not window:
        glfw.terminate()
        print("Erro ao criar a janela")
        return

    glfw.make_context_current(window)

    glfw.set_mouse_button_callback(window, clique_mouse)

    glClearColor(0.1, 0.1, 0.1, 1.0)

    while not glfw.window_should_close(window):
        atualizar_viewport(window)

        glClear(GL_COLOR_BUFFER_BIT)

        desenhar_triangulo()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

main()