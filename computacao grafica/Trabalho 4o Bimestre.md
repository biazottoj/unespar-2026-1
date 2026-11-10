# Trabalho 4o Bimestre — Computação Gráfica

**Tema:** Processamento e transformação de uma imagem utilizando Zoom, Histograma, Esqueletização, Convolução e Deformações  
**Valor:** **4,0 pontos**  
**Prazo:** 24/11/2026  
**Linguagem e ambiente:** **Python**, com **NumPy** para manipulação de matrizes e **OpenGL** para visualização dos resultados.

## 1. Contextualização e objetivo

Ao longo da disciplina, estudamos diferentes formas de representar, analisar e transformar imagens digitais. Embora cada técnica tenha uma finalidade específica, elas também podem ser combinadas em um mesmo fluxo de processamento.

Neste trabalho, vocês deverão desenvolver uma aplicação que utilize **uma única imagem-base** para investigar cinco técnicas:

1. **Zoom:** ampliação de imagens por reamostragem dos pixels;
2. **Histograma:** análise da distribuição de intensidades e melhoria de contraste;
3. **Esqueletização:** obtenção de uma representação simplificada da estrutura de um objeto;
4. **Convolução:** aplicação de kernels para alterar características locais da imagem;
5. **Deformações:** transformação da geometria da imagem por meio de um mapeamento espacial.

O trabalho está dividido em **três partes obrigatórias**: fundamentação teórica, demonstrações individuais e aplicação integrada.

### Escolha da imagem

A mesma imagem deve ser utilizada em **todas as demonstrações da Parte 2 e na aplicação da Parte 3**. Escolham uma imagem que apresente:

- Um **objeto principal facilmente identificável**, com forma ou silhueta definida;
- Contraste suficiente entre objeto e fundo para permitir segmentação e esqueletização;
- Regiões com diferentes tonalidades ou intensidades, para observar o histograma;
- Detalhes ou contornos que permitam comparar filtros de convolução.

Exemplos: símbolo, folha, peça mecânica, objeto de uso cotidiano, personagem em pixel art ou ilustração simples. A imagem pode ser criada diretamente por uma **matriz NumPy** ou carregada de um arquivo.

---

## 2. Parte 1 — Questões teóricas (**1,0 ponto**)

Respondam às **cinco questões discursivas** com suas próprias palavras. Sempre que pertinente, utilizem um exemplo numérico, um pequeno esquema ou uma referência ao comportamento observado no programa.

**Questão 1 — Zoom (0,20 ponto)**  
Explique o que significa ampliar uma imagem digital e por que o processo exige calcular valores para novos pixels. Compare os métodos do **vizinho mais próximo** e da **interpolação bilinear**, indicando uma vantagem e uma limitação de cada um.

**Questão 2 — Histograma (0,20 ponto)**  
Defina histograma de uma imagem em tons de cinza. Explique o que um histograma revela sobre a distribuição das intensidades e como a **equalização ou expansão de contraste** pode modificar a aparência de uma imagem. Duas imagens diferentes podem possuir o mesmo histograma? Justifique.

**Questão 3 — Esqueletização (0,20 ponto)**  
Defina esqueletização e explique qual informação da forma do objeto se busca preservar. Por que normalmente utilizamos uma **imagem binária** como entrada? Cite uma situação em que o resultado pode ser prejudicado por ruído ou falhas na segmentação.

**Questão 4 — Convolução (0,20 ponto)**  
Explique como um **kernel** é aplicado a uma imagem e por que diferentes valores do kernel produzem efeitos diferentes. Compare um kernel de suavização (média ou Gaussiano) com um kernel de realce de bordas ou nitidez. Relacione os **pesos do kernel** ao efeito produzido.

**Questão 5 — Deformações (0,20 ponto)**  
Explique o que é uma **deformação geométrica** e diferencie-a de uma simples alteração de cor. Descreva o papel do **mapeamento das coordenadas** e explique por que é necessário decidir o que fazer quando uma coordenada da imagem de origem fica fora dos limites.

---

## 3. Parte 2 — Aplicação individual das técnicas (**1,5 ponto**)

Desenvolvam um programa Python que aplique **cada técnica separadamente à mesma imagem-base**, sem que o resultado de uma técnica seja utilizado como entrada da próxima nesta parte.

Para cada técnica, apresentem: **(a)** imagem original, **(b)** resultado processado, **(c)** parâmetros utilizados e **(d)** uma breve análise do efeito observado.

### 3.1. Zoom — **0,30 ponto**

- Implementem a ampliação da imagem em um fator à escolha (sugestão: **2×**).
- Apresentem uma ampliação por **vizinho mais próximo** e outra por **interpolação bilinear**.
- Comparem as bordas, a aparência dos pixels e a suavidade dos resultados.

### 3.2. Histograma — **0,30 ponto**

- Convertam a imagem para tons de cinza, quando necessário.
- Calculem e apresentem o **histograma original** (frequência por intensidade).
- Realizem **equalização de histograma ou expansão de contraste**.
- Calculem e apresentem o **histograma da imagem processada** e comparem as distribuições.

### 3.3. Esqueletização — **0,30 ponto**

- Obtenham uma **máscara binária** do objeto principal, explicitando o critério de binarização.
- Implementem a esqueletização utilizando uma técnica estudada em aula (**esqueleto morfológico** ou **afinamento iterativo**).
- Mostrem lado a lado **imagem binária** e **esqueleto resultante**.

### 3.4. Convolução — **0,30 ponto**

- Utilizem uma **função genérica de convolução** que receba um kernel como parâmetro.
- Apliquem **dois kernels diferentes**: um de **suavização** (média ou Gaussiano) e outro de **nitidez ou detecção de bordas**.
- Apresentem os kernels escolhidos e mostrem os dois resultados.

### 3.5. Deformações — **0,30 ponto**

- Implementem uma **deformação geométrica** que altere a forma ou disposição espacial do objeto, como **cisalhamento**, **escala não uniforme** ou **deformação por três pontos/triângulo**.
- Informem os parâmetros, pontos de referência ou matriz de transformação utilizados.
- Exibam a imagem original e a deformada.

### Requisitos da Parte 2

- A imagem de entrada deve ser **a mesma** nas cinco demonstrações.
- Os algoritmos de cada técnica devem estar **identificáveis no código** (funções separadas ou organização equivalente).
- Cada técnica deve poder ser executada e visualizada independentemente das demais.
- A visualização deve ser feita em **OpenGL**, aproveitando a infraestrutura desenvolvida durante a disciplina. São permitidos gráficos auxiliares para histogramas.
- São permitidas bibliotecas auxiliares para entrada e saída de arquivos e apresentação de gráficos, mas **não** funções prontas de bibliotecas externas que executem diretamente as cinco técnicas avaliadas (por exemplo, `cv2.resize`, `cv2.equalizeHist`, `cv2.filter2D`, `cv2.warpAffine` ou funções prontas de esqueletização). A lógica central deverá estar implementada pelos alunos.

---

## 4. Parte 3 — Aplicação integrada (**1,5 ponto**)

Construam **um exemplo de processamento com uma finalidade definida**, no qual as cinco técnicas sejam utilizadas **em conjunto**, em uma sequência lógica. Nesta parte, diferentemente da Parte 2, **a saída de uma etapa deverá alimentar a etapa seguinte**, sempre que for tecnicamente adequado.

### Cenário sugerido: preparação da estrutura de um objeto para análise

Considere que um sistema precisa analisar a estrutura de um objeto representado em uma imagem. A imagem de entrada pode apresentar baixo contraste, pequenas irregularidades e uma orientação ou proporção inadequada para a análise.

Um exemplo de fluxo possível é:

```text
IMAGEM ORIGINAL
      |
      v
[1] CONVOLUÇÃO
    Suavizar pequenas irregularidades
      |
      v
[2] HISTOGRAMA
    Analisar e ajustar o contraste
      |
      v
[3] DEFORMAÇÃO
    Corrigir ou modificar a geometria do objeto
      |
      v
[4] ZOOM
    Ampliar a região de interesse para visualização/análise
      |
      v
[5] BINARIZAÇÃO (etapa auxiliar)
    Separar objeto e fundo
      |
      v
[6] ESQUELETIZAÇÃO
    Obter a estrutura simplificada do objeto
      |
      v
RESULTADO FINAL
```

### Requisitos da integração

1. **Definição do objetivo:** descrevam em um parágrafo o problema que o fluxo procura resolver e por que a imagem escolhida é adequada.
2. **Processamento sequencial:** implementem uma função ou rotina que execute as etapas e passe os resultados entre elas.
3. **Uso das cinco técnicas:** zoom, histograma (com análise e uma transformação associada, como equalização/contraste), esqueletização, convolução e deformação devem ter funções identificáveis no fluxo.
4. **Resultados intermediários:** exibam ou permitam consultar a imagem original, cada etapa relevante e o resultado final. A apresentação pode utilizar modos selecionados pelo teclado no OpenGL.
5. **Justificativa técnica:** expliquem **por que escolheram aquela ordem**, quais parâmetros foram usados e como cada etapa influencia a seguinte.

---

## 5. Entregáveis

### Parte 01 (Até 13/11)
- **Relatório (.pdf ou .md)** contendo as respostas das cinco questões teóricas;

### Parte 02 (Até 24/11)

Arquivo **.zip** contendo os seguinte documentos:

1. **Código-fonte Python** da aplicação, com instruções claras de execução e dependências;
2. **Arquivo `README.md`**, com identificação dos autores, descrição da imagem utilizada, teclas/modos do programa e explicação de como executar as demonstrações individuais e a integração;
3. **Imagem-base**, caso ela seja carregada de um arquivo externo. Se a imagem for criada diretamente com NumPy, basta incluir o código que a gera.

---


---

## 8. Entrega

- Parte 01 (Questões Teóricas): Até 13/11 (Sexta-Feira)
- Partes 02 e 03 (Parte Prática) Até 24/11 (Terça-Feira)

Ambas as entregas devem ser feitas pelo formulário: [https://forms.gle/7YmmNz57VDdNtowd6](https://forms.gle/7YmmNz57VDdNtowd6)
