# Trabalho Prático — Computação Gráfica

## Curvas de Bézier, Shaders, Uniforms e Interação com o Teclado

**Disciplina:** Computação Gráfica  
**Linguagem:** Python (GLFW + PyOpenGL + NumPy)

## Objetivo

Desenvolver uma aplicação gráfica utilizando OpenGL Moderno que permita ao usuário interagir com uma curva de Bézier cúbica por meio do teclado. O projeto deve integrar os conceitos estudados em sala: shaders, uniforms, VAO/VBO e curvas de Bézier.

---

## Requisitos

### 1. Curva de Bézier
Implemente uma curva de Bézier cúbica com quatro pontos de controle e desenhe-a utilizando `GL_LINE_STRIP`.

### 2. Polígono de controle
Desenhe também os quatro pontos de controle e os segmentos que os conectam.

### 3. Alteração de cor com Uniform
Implemente as teclas:

- R → vermelho
- G → verde
- B → azul
- W → branco

A cor deve ser enviada ao fragment shader usando `uniform`.

### 4. Movimentação dos pontos de controle
Selecione um ponto pelas teclas **1, 2, 3 e 4**.

Movimente o ponto selecionado utilizando as setas do teclado.

Após qualquer movimentação:
- recalcule a curva;
- atualize o VBO;
- redesenhe a cena.

### 5. Alteração da resolução da curva
Permita alterar o número de amostras da curva.

Sugestão:

- "+" → aumenta
- "-" → diminui

Utilize entre 100 e 2000 pontos.

### 6. Mostrar ou ocultar o polígono de controle
Implemente a tecla **P** para mostrar/esconder o polígono de controle.

### 7. Alterar a espessura da curva
Implemente:

- ] → aumenta
- [ → diminui

### 8. Destacar o ponto selecionado
O ponto atualmente selecionado deve ser desenhado com cor diferente e tamanho maior.

---

## Requisitos técnicos

O trabalho deve utilizar obrigatoriamente:

- Python
- GLFW
- PyOpenGL
- NumPy
- Vertex Shader
- Fragment Shader
- VAO
- VBO
- Uniforms

Não é permitido utilizar bibliotecas prontas para curvas.

---

## Organização sugerida

```
main.py
init()
render()
process_input()

compile_shader()
create_shader_program()

gerar_curva_bezier()
atualizar_vbo()

desenhar_curva()
desenhar_poligono()
desenhar_pontos()
```

---

## Entrega

Entregar um zip com:

- código-fonte;
- README com instruções de execução;
- captura de tela da aplicação;
- breve relatório descrevendo as funcionalidades implementadas.
- Utilize o link para entrega: [https://forms.gle/cwQjWUQ7nm9oGTD36](https://forms.gle/cwQjWUQ7nm9oGTD36)
