# Atividade — VBO, VAO e Fragment Shader em OpenGL

## Título
**Construindo uma cena 2D com múltiplos objetos usando VBO, VAO e fragment shader**

## Objetivo geral
Aplicar os conceitos de **VBO**, **VAO** e **fragment shader** na construção de uma cena 2D em OpenGL moderno, usando Python, GLFW e PyOpenGL.

## Objetivos específicos
Ao final da atividade, espera-se que o aluno consiga:

- criar uma janela com GLFW;
- compilar e usar shaders;
- criar e configurar mais de um VBO;
- criar e configurar mais de um VAO;
- desenhar múltiplos objetos na mesma cena;
- usar atributos de vértice;
- usar `uniform` no fragment shader;
- compreender a diferença entre dados armazenados no buffer e parâmetros enviados ao shader.

---

# 1. O que será construído

Nesta atividade, você deverá implementar uma cena 2D com:

- **um triângulo colorido**
- **um quadrado**
- **um segundo objeto de sua escolha**, como:
  - outro triângulo,
  - trapézio,
  - losango,
  - bandeira simples,
  - telhado,
  - montanha.

A cena deve usar:

- pelo menos **2 VAOs**
- pelo menos **2 VBOs**
- um **vertex shader**
- um **fragment shader**
- pelo menos **1 uniform** no fragment shader

---

# 2. Diferença em relação ao walkthrough

No walkthrough, foi construído:
- apenas **um triângulo**;
- com **um único VAO**;
- com **um único VBO**;
- e o fragment shader apenas devolvia a cor recebida.

Agora, nesta atividade, você deverá ir além:

- trabalhar com **múltiplos objetos**;
- configurar **múltiplos buffers**;
- organizar melhor o código;
- modificar o fragment shader para usar também um **uniform**.

---

# 3. Tecnologias utilizadas

Você deve usar:

- **Python**
- **GLFW**
- **PyOpenGL**
- **NumPy**

---

# 4. Requisitos obrigatórios

Seu programa deve:

1. abrir uma janela com GLFW;
2. criar e compilar vertex shader e fragment shader;
3. desenhar pelo menos **3 objetos**;
4. usar pelo menos **2 VBOs**;
5. usar pelo menos **2 VAOs**;
6. utilizar atributos de posição e cor;
7. usar pelo menos **1 uniform** no fragment shader;
8. organizar o código em funções.

---

# 5. Estrutura sugerida do programa

Seu código pode seguir esta organização:

1. imports  
2. código-fonte dos shaders  
3. função de compilação dos shaders  
4. criação da janela  
5. definição dos arrays de vértices  
6. criação/configuração dos VAOs e VBOs  
7. loop principal  
8. limpeza de recursos

---

# 6. Conceitos que devem aparecer no seu código

## 6.1 VBO
Você deverá usar VBO para armazenar os dados dos vértices dos objetos.

## 6.2 VAO
Você deverá usar VAO para guardar a configuração dos atributos de cada objeto.

## 6.3 Vertex shader
Seu vertex shader deve receber:
- posição;
- cor.

## 6.4 Fragment shader
Seu fragment shader deve:
- receber a cor interpolada;
- usar também um `uniform` para modificar ou combinar a cor final.

---

# 7. Proposta de implementação

## Objeto 1 — Triângulo colorido
Esse objeto pode seguir o padrão do walkthrough:
- cada vértice com uma cor diferente;
- cor interpolada na superfície.

## Objeto 2 — Quadrado
O quadrado pode ser desenhado como:
- dois triângulos em um mesmo VBO;
ou
- um conjunto separado de vértices.

## Objeto 3 — Forma livre
Você deve criar um terceiro objeto com sua própria escolha.

Esse terceiro objeto deve mostrar que você compreendeu:
- como definir vértices;
- como organizar os dados;
- como desenhar outra primitiva.

---

# 8. Requisito extra do fragment shader

No walkthrough, o fragment shader apenas fazia isso:

```glsl
FragColor = vec4(vColor, 1.0);
```

Agora, você deve torná-lo mais interessante usando um `uniform`.

## Exemplo de ideia
Você pode usar um uniform chamado `brightness`:

```glsl
FragColor = vec4(vColor * brightness, 1.0);
```

Ou um uniform chamado `tintColor`:

```glsl
FragColor = vec4(vColor * tintColor, 1.0);
```

## O que isso permite
- alterar a aparência dos objetos sem mudar o VBO;
- mostrar que o fragment shader pode combinar:
  - atributos interpolados;
  - valores externos enviados pelo programa.

---

# 9. Passo a passo sugerido

## Passo 1 — Criar a janela
Implemente a inicialização do GLFW e a criação da janela.

### O que verificar
- a janela abre corretamente;
- o contexto OpenGL está ativo.

---

## Passo 2 — Escrever os shaders
Crie:
- um vertex shader;
- um fragment shader.

### O que verificar
- o vertex shader recebe posição e cor;
- o fragment shader recebe a cor interpolada;
- o fragment shader usa um uniform.

---

## Passo 3 — Compilar e linkar os shaders
Implemente:
- compilação do vertex shader;
- compilação do fragment shader;
- criação do shader program.

### O que verificar
- erros de compilação;
- erros de linkedição.

---

## Passo 4 — Criar os dados do primeiro objeto
Defina o array de vértices do triângulo.

### O que verificar
- posição correta;
- cores corretas;
- tipo `float32`.

---

## Passo 5 — Criar VAO e VBO do primeiro objeto
Implemente:
- `glGenVertexArrays`
- `glGenBuffers`
- `glBindVertexArray`
- `glBindBuffer`
- `glBufferData`
- `glVertexAttribPointer`
- `glEnableVertexAttribArray`

### O que verificar
- o atributo de posição está correto;
- o atributo de cor está correto;
- stride e offsets estão corretos.

---

## Passo 6 — Criar os dados do segundo objeto
Defina os vértices do quadrado.

### Dica
Você pode:
- usar dois triângulos;
- manter a mesma estrutura de atributos do primeiro objeto.

---

## Passo 7 — Criar VAO e VBO do segundo objeto
Repita a lógica para o segundo objeto.

### O que verificar
- o segundo VAO está independente do primeiro;
- os dados do segundo VBO estão corretos.

---

## Passo 8 — Criar os dados do terceiro objeto
Crie um novo array para o terceiro objeto.

### O que verificar
- a forma é reconhecível;
- o objeto aparece em outra posição da tela;
- o desenho não sobrepõe totalmente os outros objetos.

---

## Passo 9 — Enviar valor para o uniform
Recupere a localização do uniform com `glGetUniformLocation` e envie um valor com `glUniform...`.

### Exemplo
Se o uniform for `brightness`, envie algo como:
- `1.0`
- `0.8`
- `0.6`

Você pode usar valores diferentes antes de desenhar objetos diferentes.

### O que verificar
- o fragment shader realmente reage ao uniform;
- os objetos podem ter aparências distintas.

---

## Passo 10 — Desenhar a cena
No loop principal:
- limpe a tela;
- ative o programa de shader;
- configure o uniform;
- faça bind do VAO correto;
- desenhe cada objeto.

### O que verificar
- todos os objetos aparecem;
- cada objeto usa seu VAO corretamente;
- a ordem de desenho está funcionando.

---

# 10. Perguntas de reflexão que o aluno deve responder

Ao final da atividade, responda:

1. O que o VBO armazena?
2. O que o VAO guarda?
3. Qual a função de `glVertexAttribPointer`?
4. Por que usamos mais de um VAO nesta atividade?
5. Qual a diferença entre atributo de vértice e uniform?
6. Por que o fragment shader é um bom lugar para controlar a cor final?
7. O que muda quando alteramos o uniform sem alterar o VBO?
8. Qual foi a principal dificuldade ao configurar os múltiplos objetos?

---

# 11. Entregáveis

O aluno ou dupla deve entregar:

1. o arquivo `.py` com o código;
2. um documento curto respondendo às perguntas de reflexão;
3. uma captura de tela da cena funcionando.

---

# 12. Critérios de avaliação

## 1. Funcionamento do programa
- a janela abre;
- os objetos aparecem;
- não há erro de compilação de shader.

## 2. Uso correto de VBO e VAO
- os buffers foram criados corretamente;
- os atributos foram configurados corretamente;
- o aluno entendeu a separação entre dados e configuração.

## 3. Uso do fragment shader
- o fragment shader foi usado corretamente;
- o uniform foi aplicado.

## 4. Organização do código
- o código está dividido em partes compreensíveis;
- há funções auxiliares quando necessário.

## 5. Compreensão conceitual
- as respostas mostram que o aluno entendeu os conceitos.

---

# 13. Desafio extra (opcional)

Se quiser deixar a atividade mais interessante, faça uma destas extensões:

## Opção A
Use valores diferentes do uniform para cada objeto.

## Opção B
Crie uma função genérica para configurar VAO e VBO.

## Opção C
Adicione um quarto objeto.

## Opção D
Faça o fundo da janela ter uma cor diferente da usada no walkthrough.

---

# 14. Sugestão de encaminhamento didático

Uma boa estratégia é:

1. reaproveitar o código do walkthrough;
2. manter o triângulo original;
3. duplicar a lógica para criar outro objeto;
4. só depois adicionar o uniform no fragment shader.

Assim, você evolui o exemplo base em vez de recomeçar do zero.

---

# 15. Resumo da atividade

Nesta atividade, você vai praticar OpenGL moderno em um nível acima do walkthrough, trabalhando com:

- múltiplos objetos;
- múltiplos VBOs;
- múltiplos VAOs;
- fragment shader com uniform;
- organização do pipeline gráfico básico.

Se você concluir essa atividade corretamente, estará pronto para estudar com mais segurança os próximos temas, como:

- EBO/índices;
- transformações;
- matrizes;
- câmera;
- projeção.
