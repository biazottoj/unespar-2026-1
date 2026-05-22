# Atividade 08 — Teclado e Mouse com OpenGL

---

# Exercício 1 — Desenhar formas diferentes com teclas

Modifique o programa para que o usuário possa escolher qual forma será desenhada a partir de um clique do mouse.

## Requisitos

A aplicação deve permitir:

| Tecla | Forma selecionada |
|---|---|
| `P` | Ponto |
| `L` | Linha |
| `T` | Triângulo |
| `Q` | Quadrado |

## Comportamento esperado

- Ao pressionar uma tecla, o programa altera o **modo de desenho**.
- Depois, ao clicar com o botão esquerdo do mouse, a forma selecionada deve ser desenhada na posição clicada.
- Por exemplo:
  - se o usuário pressionar `T` e clicar na tela, um triângulo deve aparecer no local do clique;
  - se pressionar `Q` e clicar, um quadrado deve aparecer.

---

# Exercício 2 — Criar cores customizadas

Expanda o programa para permitir o uso de cores além de vermelho, verde e azul.

## Requisitos

A aplicação deve permitir selecionar pelo menos **6 cores diferentes** usando o teclado.

Exemplo:

| Tecla | Cor |
|---|---|
| `R` | Vermelho |
| `G` | Verde |
| `B` | Azul |
| `Y` | Amarelo |
| `M` | Roxo/Magenta |
| `W` | Branco |

## Comportamento esperado

- A cor selecionada deve ser aplicada à próxima forma desenhada.
- Cada forma deve manter a cor que estava selecionada no momento em que foi criada.

---

# Exercício 3 — Limpar a tela com a tecla `C`

Adicione uma funcionalidade para limpar todos os objetos desenhados na tela quando o usuário pressionar a tecla `C`.

## Requisitos

- A tecla `C` deve apagar todas as formas desenhadas.
- Depois de limpar a tela, o usuário deve conseguir desenhar novas formas normalmente.
- A forma e a cor selecionadas podem continuar as mesmas após a limpeza.

---

# Exercício 4 — Limpar a tela com o botão direito do mouse

Implemente também a limpeza da tela usando o **botão direito do mouse**.

## Requisitos

- Clique com o botão esquerdo: desenha a forma atual.
- Clique com o botão direito: limpa a tela.
- A limpeza com o botão direito deve ter o mesmo efeito da tecla `C`.

---

# Exercício 5 — Mini editor gráfico com teclado e mouse

Integre os conceitos anteriores em uma aplicação única, funcionando como um pequeno editor gráfico.

## Requisitos

A aplicação deve permitir:

- escolher a forma pelo teclado;
- escolher a cor pelo teclado;
- desenhar a forma com clique esquerdo do mouse;
- limpar a tela com a tecla `C`;
- limpar a tela com o botão direito do mouse;
- manter na tela múltiplas formas desenhadas;
- cada forma deve manter sua própria cor e tipo.

## Exemplo de uso esperado

1. O usuário pressiona `T`.
2. O usuário pressiona `Y`.
3. O usuário clica na tela.
4. Um triângulo amarelo é desenhado.
5. O usuário pressiona `Q`.
6. O usuário pressiona `M`.
7. O usuário clica em outro ponto.
8. Um quadrado magenta é desenhado.
9. O usuário pressiona `C` ou clica com o botão direito.
10. A tela é limpa.

---

# Mover a última forma desenhada

Adicione a possibilidade de mover a última forma criada usando as setas do teclado.

## Requisitos

| Tecla | Ação |
|---|---|
| `←` | Move a última forma para a esquerda |
| `→` | Move a última forma para a direita |
| `↑` | Move a última forma para cima |
| `↓` | Move a última forma para baixo |

## Comportamento esperado

- Apenas a última forma desenhada deve se mover.
- Se nenhuma forma tiver sido desenhada, as setas não devem causar erro.

---

# Alterar a cor da última forma desenhada

Permita que o usuário altere a cor da última forma desenhada.

## Requisitos

- As teclas de cor devem mudar a cor atual.
- Se uma forma já tiver sido desenhada, pressionar `Enter` deve aplicar a cor atual à última forma criada.

## Exemplo

1. O usuário desenha um triângulo vermelho.
2. Pressiona `G`.
3. Pressiona `Enter`.
4. O último triângulo desenhado passa a ser verde.

