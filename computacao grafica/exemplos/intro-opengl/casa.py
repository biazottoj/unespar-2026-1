import glfw
from OpenGL.GL import *

def desenhar_casa():

    # Corpo
    glColor3f(0.85,0.55,0.35)
    glBegin(GL_QUADS)
    glVertex2f(-0.6, -0.45)
    glVertex2f(-0.2, -0.45)
    glVertex2f(-0.2, -0.05)
    glVertex2f(-0.6, -0.05)
    glEnd()

    # Porta
    glColor3f(0.35,0.2,0.1)
    glBegin(GL_QUADS)
    glVertex2f(-0.46, -0.45)
    glVertex2f(-0.34, -0.45)
    glVertex2f(-0.34, -0.2)
    glVertex2f(-0.46, -0.2)
    glEnd()

    #Teto
    glColor3f(0.35,0.2,0.1)
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.65, -0.05)
    glVertex2f(-0.15, -0.05)
    glVertex2f(-0.40, 0.22)
    glEnd()



def desenhar_chao():
    glColor3f(0.25,0.60,0.25)
    glBegin(GL_QUADS)
    glVertex2f(-1.0, -1.0)
    glVertex2f(1.0, -1.0)
    glVertex2f(1.0, -0.45)
    glVertex2f(-1.0, -0.45)
    glEnd()


def display():
    glClearColor(0.53, 0.81, 0.98, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    desenhar_chao()
    desenhar_casa()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    if not glfw.init():
        raise RuntimeError("Erro ao inicializar OpenGL")
    
    window = glfw.create_window(900,700, "Casa", None, None)

    if not window:
        glfw.terminate()
        raise RuntimeError("Não foi possível criar a janela")
    
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        display()
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.destroy_window(window)
    glfw.terminate()

main()

