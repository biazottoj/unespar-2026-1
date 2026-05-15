# Atividade 07 — Desenho interativo com OpenGL, Python e GLFW

## Objetivo da atividade

Esta atividade tem como objetivo exercitar o uso de **OpenGL com Python e GLFW** para criar desenhos interativos a partir de cliques do mouse.

---

# Orientações gerais

Cada exercício deve ser desenvolvido em Python, usando GLFW e OpenGL.

Os programas devem permitir interação com o mouse. O clique do usuário deve ser parte essencial da construção do desenho. Portanto, não basta desenhar figuras fixas na tela.

Em todos os exercícios, os alunos devem considerar:

1. como capturar o clique do mouse;
2. como converter a posição do clique para coordenadas OpenGL;
3. como armazenar as informações do desenho;
4. como organizar os vértices da figura;
5. como redesenhar a cena no loop principal;
6. como separar o código em funções com responsabilidades claras.

---

# Exercício 1 — Figura complexa usando linhas

## Descrição

Crie uma aplicação que desenhe uma figura complexa composta apenas por linhas a partir de um clique na tela.

A figura deve ser posicionada com base no ponto clicado. Esse ponto pode representar o centro da figura, a base, o vértice inicial ou outro ponto de referência definido pelo aluno.

O importante é que o desenho seja construído usando coordenadas relativas ao clique, e não apenas coordenadas fixas.

## Primitivas sugeridas

O aluno pode utilizar primitivas como:

- `GL_LINES`;
- `GL_LINE_STRIP`;
- `GL_LINE_LOOP`.

## Requisitos mínimos

A figura deve conter:

- pelo menos três partes visuais distintas;
- entre 10 e 20 segmentos de linha;
- pelo menos duas primitivas de linha diferentes;
- posicionamento baseado no clique do mouse;
- organização do desenho em funções separadas;
- atualização correta quando o usuário clicar em uma nova posição.

## Cuidados importantes

A figura não deve ser simples demais. Desenhos como apenas uma linha, um quadrado ou um triângulo simples não atendem ao objetivo do exercício.

Também não é adequado posicionar todos os vértices com valores fixos. A posição do clique deve influenciar diretamente o local onde a figura aparece.

---

# Exercício 2 — Figura complexa usando polígonos

## Descrição

Crie uma aplicação que desenhe uma figura complexa composta por polígonos preenchidos a partir de um clique na tela.

A figura deve ser formada pela combinação de várias partes geométricas. O objetivo não é criar uma única forma grande e complexa, mas sim decompor uma figura maior em polígonos menores.

Cada parte da figura deve ser posicionada em relação ao ponto clicado.

## Primitivas sugeridas

O aluno pode utilizar primitivas como:

- `GL_POLYGON`;
- `GL_TRIANGLES`;
- `GL_QUADS`;
- `GL_TRIANGLE_FAN`;
- `GL_TRIANGLE_STRIP`.

## Requisitos mínimos

A figura deve conter:

- pelo menos cinco polígonos preenchidos;
- pelo menos duas cores diferentes;
- pelo menos uma parte triangular;
- pelo menos uma parte com quatro ou mais vértices;
- pelo menos dois tipos de primitivas poligonais;
- posicionamento baseado no clique do mouse;
- organização em funções;
- redesenho correto após novo clique.

## Cuidados importantes

Evite criar polígonos muito irregulares ou difíceis de preencher corretamente.

Figuras complexas devem ser divididas em formas simples, como triângulos, quadriláteros e polígonos convexos. Essa decomposição torna o desenho mais previsível e facilita a implementação.

O exercício não deve ser resolvido usando apenas linhas. A maior parte da figura deve ser preenchida.

---

# Exercício 3 — Triângulo construído com três cliques

## Descrição

Crie uma aplicação em que o usuário desenhe triângulos na tela usando três cliques do mouse.

Neste exercício, cada triângulo deve ser construído manualmente pelo usuário:

1. o primeiro clique define o primeiro vértice;
2. o segundo clique define o segundo vértice;
3. o terceiro clique define o terceiro vértice;
4. após o terceiro clique, o triângulo deve ser desenhado;
5. depois disso, o programa deve permitir iniciar um novo triângulo.

Este exercício explora o controle de estado da aplicação, pois o programa precisa armazenar temporariamente os pontos clicados até que o triângulo esteja completo.

## Requisitos mínimos

A aplicação deve permitir:

- capturar vários cliques sucessivos;
- armazenar temporariamente os vértices ainda incompletos;
- formar um triângulo somente após três cliques;
- manter os triângulos anteriores desenhados na tela;
- permitir a criação de mais de um triângulo;
- desenhar todos os triângulos completos a cada ciclo do loop principal;
- implementar pelo menos uma forma de limpar a tela ou reiniciar a cena.

## Requisitos de estado

O programa deve diferenciar:

- pontos temporários ainda não finalizados;
- triângulos completos;
- novo triângulo em construção;
- triângulos já armazenados na cena.

A solução deve usar uma estrutura de dados adequada para guardar os triângulos completos e outra estrutura, ou lógica equivalente, para armazenar os pontos temporários.

## Cuidados importantes

O programa não deve desenhar apenas um triângulo por vez.

Os triângulos anteriores não devem desaparecer automaticamente quando um novo triângulo começa a ser construído.

O exercício também não deve ser resolvido usando coordenadas fixas. Cada vértice do triângulo deve ser definido a partir dos cliques do usuário.

---

# Entregáveis

Cada aluno ou grupo deve entregar:

1. o código-fonte dos três exercícios;
2. um pequeno relatório explicando as decisões tomadas;
3. uma breve explicação sobre como executar cada programa;

