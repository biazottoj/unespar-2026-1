# Atividade Prática — Recuperação e Esqueletização de Imagens Binárias

**Disciplina:** Computação Gráfica  
**Conteúdo:** Morfologia Matemática e Esqueletização  
**Tecnologias:** Python, NumPy e OpenGL

## 1. Contexto

Uma aplicação de reconhecimento de padrões recebe imagens binárias que representam símbolos, letras e outros objetos.

Entretanto, essas imagens podem apresentar problemas decorrentes de falhas na captura ou no processamento, como ruídos isolados, interrupções nos traços e pequenos buracos.

O objetivo desta atividade é desenvolver uma ferramenta capaz de **recuperar a estrutura de uma imagem binária e extrair seu esqueleto**, utilizando as operações morfológicas estudadas em aula.

**Fluxo esperado:**

```text
Imagem com defeitos
        ↓
Operações morfológicas
        ↓
Imagem tratada
        ↓
Esqueletização
        ↓
Esqueleto final
```

## 2. Parte 1 — Construção da imagem

Utilizando o código Python/OpenGL desenvolvido durante a aula, crie uma nova imagem binária de pelo menos **25 × 25 pixels**.

A imagem deverá representar um símbolo reconhecível, como uma letra, seta, número ou outro objeto geométrico. Não utilize as figuras B ou anel já fornecidas no exemplo.

A matriz deverá utilizar:

```python
0  # Fundo
1  # Objeto
```

Adicione propositalmente **três tipos de imperfeições** à imagem:

- Pelo menos três pixels isolados, representando ruído.
- Uma interrupção de um pixel em um dos traços do símbolo.
- Um pequeno buraco em uma região interna do objeto.

A imagem deve ser construída manualmente utilizando NumPy, sem bibliotecas externas de processamento de imagens.

## 3. Parte 2 — Aplicação das operações morfológicas

Utilize as funções implementadas durante a aula:

```python
erosao(image, se)
dilatacao(image, se)
abertura(image, se)
fechamento(image, se)
```

Aplique as quatro operações à imagem original, primeiro utilizando o elemento estruturante em forma de **cruz** e depois em forma de **quadrado**:

```python
cruz = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
], dtype=bool)

quadrado = np.ones((3, 3), dtype=bool)
```

Compare os resultados e registre quais modificações ocorreram no objeto, principalmente em relação ao ruído, às interrupções dos traços e aos pequenos buracos.

## 4. Parte 3 — Construção de um processo de recuperação

Desenvolva uma função:

```python
def recuperar_imagem(image, se):
    # TODO
```

Essa função deve combinar operações morfológicas com o objetivo de reduzir os defeitos da imagem.

Experimente, no mínimo, as duas sequências:

**Sequência A:**

```text
Imagem → Abertura → Fechamento
```

**Sequência B:**

```text
Imagem → Fechamento → Abertura
```

Compare os resultados e escolha qual sequência recupera melhor a imagem criada.

A escolha deve ser justificada considerando a remoção de ruído, a continuidade dos traços e a preservação do formato original.

## 5. Parte 4 — Esqueletização

Utilize o algoritmo de esqueletização estudado em aula para obter o esqueleto da imagem recuperada.

A aplicação deverá permitir visualizar:

- A imagem original, antes do tratamento.
- A imagem após a recuperação.
- O resultado das erosões sucessivas.
- As camadas obtidas pelo método de esqueletização.
- O esqueleto final.

Utilize o **método de Lantuéjoul** implementado no walkthrough, baseado em erosões sucessivas e na diferença entre cada imagem erodida e sua abertura.

**Importante:** a esqueletização deve utilizar a imagem tratada como entrada, e não somente a imagem original.

Compare também os esqueletos produzidos com os elementos estruturantes cruz e quadrado.

## 6. Parte 5 — Visualização OpenGL

Adapte o programa desenvolvido em aula para apresentar pelo menos três painéis simultaneamente:

```text
+----------------------+----------------------+----------------------+
|                      |                      |                      |
|   IMAGEM ORIGINAL    |   IMAGEM TRATADA     |      ESQUELETO       |
|                      |                      |                      |
|                      |                      |                      |
+----------------------+----------------------+----------------------+
```

A visualização deve ser atualizada quando o elemento estruturante for alterado.

Não é necessário implementar textos dentro da janela OpenGL. A identificação dos painéis pode aparecer no terminal.

## 7. Parte 6 — Análise dos resultados

Após completar a implementação, responda:

1. Qual operação foi mais eficiente para eliminar os pixels isolados? Explique seu funcionamento.
2. Qual operação apresentou melhores resultados para corrigir as interrupções nos traços?
3. A ordem de aplicação das operações morfológicas alterou o resultado? Explique por que isso ocorreu.
4. Qual foi a diferença observada entre os elementos estruturantes em cruz e quadrado?
5. Qual é o objetivo da esqueletização? Quais características do objeto são preservadas e quais deixam de ser representadas diretamente?
6. A esqueletização da imagem tratada apresentou diferenças em relação à esqueletização da imagem original? Justifique.

## 8. Desafio adicional

Crie uma segunda imagem binária com uma estrutura diferente da primeira.

Por exemplo, se a primeira imagem representa uma letra, a segunda pode representar uma figura com buraco interno ou diversos ramos.

Execute exatamente o mesmo processo de recuperação e esqueletização, sem modificar as funções dos algoritmos.

Analise se a sequência de operações escolhida para a primeira imagem também é adequada para a segunda.

O desafio é compreender que **uma combinação de operações morfológicas pode funcionar bem para determinado tipo de imagem, mas eliminar detalhes importantes em outra**.

## 9. Entrega

A entrega deverá conter:

- `atividade_esqueletizacao.py` — código Python/OpenGL completo, incluindo a nova figura, o processo de recuperação e a visualização comparativa.
- `respostas.md` — respostas às seis questões da Parte 6, com a justificativa da sequência de operações escolhida e capturas de tela dos resultados.

## Resultado esperado

Ao final da atividade, o programa deverá demonstrar o seguinte processo:

```text
Imagem binária com imperfeições
             ↓
    Operações morfológicas
             ↓
       Imagem recuperada
             ↓
       Erosões sucessivas
             ↓
  Extração das camadas do esqueleto
             ↓
        Esqueleto final
```

O principal objetivo é compreender **como selecionar e combinar operações morfológicas para resolver um problema concreto**, e não apenas reproduzir individualmente os algoritmos apresentados durante a aula.
