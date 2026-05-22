import glfw
from OpenGL.GL import *


pontos = []
cor_atual = [1.0, 0.0, 0.0]

deslocamento_x = 0.0
deslocamento_y = 0.0
velocidade = 0.05


def key_callback(window, key, scancode, action, mods):
    global pontos
    global cor_atual
    global deslocamento_x, deslocamento_y

    if action == glfw.PRESS or action == glfw.REPEAT:

        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

        elif key == glfw.KEY_R:
            cor_atual = [1.0, 0.0, 0.0]

        elif key == glfw.KEY_G:
            cor_atual = [0.0, 1.0, 0.0]

        elif key == glfw.KEY_B:
            cor_atual = [0.0, 0.0, 1.0]

        elif key == glfw.KEY_C:
            pontos.clear()
            deslocamento_x = 0.0
            deslocamento_y = 0.0


def mouse_button_callback(window, button, action, mods):
    global pontos

    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        if len(pontos) < 3:
            x_mouse, y_mouse = glfw.get_cursor_pos(window)

            largura, altura = glfw.get_window_size(window)

            x_opengl = (x_mouse / largura) * 2 - 1
            y_opengl = 1 - (y_mouse / altura) * 2

            pontos.append((x_opengl, y_opengl))


def desenhar_pontos():
    glPointSize(8)
    glColor3f(1.0, 1.0, 1.0)

    glBegin(GL_POINTS)
    for x, y in pontos:
        glVertex2f(x + deslocamento_x, y + deslocamento_y)
    glEnd()


def desenhar_triangulo():
    if len(pontos) == 3:
        glColor3f(cor_atual[0], cor_atual[1], cor_atual[2])

        glBegin(GL_TRIANGLES)
        for x, y in pontos:
            glVertex2f(x + deslocamento_x, y + deslocamento_y)
        glEnd()

def atualizar_viewport(window):
    largura, altura = glfw.get_framebuffer_size(window)
    glViewport(0, 0, largura, altura)

def main():
    if not glfw.init():
        print("Erro ao inicializar GLFW")
        return

    window = glfw.create_window(800, 600, "Triângulo interativo", None, None)

    if not window:
        glfw.terminate()
        print("Erro ao criar a janela")
        return

    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)

    glClearColor(0.1, 0.1, 0.1, 1.0)

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