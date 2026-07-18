# Atividade 11 — Curvas de Bézier, shaders e `uniform`

---

# Atividade 1 — Colorir a curva com `uniform`

## Objetivo
Praticar o uso de `uniform` no fragment shader.

## Enunciado
Modifique o programa para que a curva de Bézier seja desenhada com uma cor escolhida pelo aluno usando a variável `uColor`.

### Requisitos
- manter a curva de Bézier já implementada;
- enviar a cor para o shader com `glUniform3f`;
- testar pelo menos 3 cores diferentes;
- registrar no código onde o `uniform` é localizado e atualizado.

---

# Atividade 2 — Desenhar curva e polígono de controle

## Objetivo
Relacionar a curva de Bézier com seus pontos de controle.

## Enunciado
Adicione ao programa o desenho do **polígono de controle** da curva.

### Requisitos
- desenhar os 4 pontos de controle;
- desenhar os segmentos entre os pontos de controle;
- desenhar a curva com uma cor e o polígono de controle com outra;
- usar `uniform` para diferenciar visualmente os dois elementos.

---

# Atividade 3 — Comparar duas curvas de Bézier

## Objetivo
Observar como os pontos de controle afetam a forma da curva.

## Enunciado
Crie duas curvas de Bézier cúbicas na mesma janela.

### Requisitos
- as duas curvas devem ter o mesmo ponto inicial e final;
- os pontos de controle intermediários devem ser diferentes;
- cada curva deve ser desenhada com uma cor diferente usando `uniform`;
- usar dois conjuntos de vértices e dois desenhos separados.

---

# Atividade 4 — Animar a cor da curva com `uniform`

## Objetivo
Usar `uniform` de forma dinâmica.

## Enunciado
Faça a cor da curva mudar ao longo do tempo.

### Requisitos
- manter a geometria da curva fixa;
- alterar a cor a cada quadro;
- usar `glfw.get_time()` para gerar valores variáveis;
- atualizar o `uniform` dentro da função `render()`.

---

# Atividade 5 — Controlar a espessura e a cor de múltiplas curvas

## Objetivo
Combinar mais de uma curva com configuração visual independente.

## Enunciado
Desenhe três curvas de Bézier diferentes na mesma janela.

### Requisitos
- cada curva deve usar um conjunto próprio de pontos de controle;
- cada curva deve ter uma cor própria enviada por `uniform`;
- alterar a espessura da linha antes de cada desenho;
- organizar o código para evitar repetição desnecessária.


---

# Atividade 6 — Alterar a curva em tempo real por teclado

## Objetivo
Relacionar diretamente os pontos de controle com a forma da curva.

## Enunciado
Permita ao usuário mover pelo menos um dos pontos de controle usando o teclado.

### Requisitos
- escolher um ponto de controle para ser alterado;
- mover esse ponto com teclas definidas pelo aluno;
- recalcular a curva sempre que houver alteração;
- manter a curva e o polígono de controle desenhados;
- usar `uniform` para diferenciar visualmente:
  - curva;
  - polígono de controle;
  - ponto selecionado.

---
### Entrega:
- Utilize o link a seguir para a entrega: [https://forms.gle/VSWN8bf6QfGsvUtG6](https://forms.gle/VSWN8bf6QfGsvUtG6)
