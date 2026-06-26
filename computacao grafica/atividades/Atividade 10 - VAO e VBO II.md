# Lista de Atividades — Shaders, VAO e VBO


## 1. Diferença entre VBO e VAO
Explique, com suas palavras, a diferença entre **VBO** e **VAO** no OpenGL moderno.  
Em sua resposta, deixe claro:
- o que cada um armazena;
- por que eles são usados em conjunto;
- o que poderia acontecer se um programa tivesse VBO, mas não configurasse corretamente o VAO.

---

## 2. Papel do vertex shader e do fragment shader
Descreva a função de cada um dos shaders abaixo no pipeline gráfico:
- **vertex shader**
- **fragment shader**

Na resposta, explique:
- em que momento cada shader é executado;
- que tipo de dado cada um recebe;
- que tipo de resultado cada um produz.

---

## 3. Por que o OpenGL moderno usa shaders?
Explique por que o OpenGL moderno passou a utilizar shaders programáveis, em vez de depender apenas de uma pipeline fixa.

Na resposta, discuta:
- flexibilidade;
- controle sobre o processamento gráfico;
- desempenho

---

## 4. Análise de um erro conceitual
Um aluno afirmou:

> “O VAO guarda os vértices do objeto, e o VBO guarda a forma como os atributos serão interpretados.”

Explique por que essa afirmação está incorreta.  
Apresente a correção conceitual e dê um exemplo simples para justificar sua resposta.

---

## 5. Fluxo de dados do programa até a tela
Descreva o caminho percorrido pelos dados de um triângulo desde o momento em que são criados no programa até o momento em que aparecem na tela (i.e., pipeline grafico moderno)

---

# Atividades práticas

## 6. Dois triângulos com cores diferentes
Crie um programa em OpenGL moderno que desenhe **dois triângulos** em posições diferentes da tela, usando **VAO** e **VBO**.

Requisitos:
- cada triângulo deve ter cores próprias;
- o programa deve usar shaders;
- organize o código em `init()` e `render()`.

---

## 7. Deformação simples no vertex shader
Implemente um programa que desenhe uma forma geométrica simples e aplique uma **deformação no eixo y diretamente no vertex shader**.

Requisitos:
- use VAO e VBO;
- a deformação deve ser visível;
- mantenha o fragment shader simples.

---

# Entrega:

