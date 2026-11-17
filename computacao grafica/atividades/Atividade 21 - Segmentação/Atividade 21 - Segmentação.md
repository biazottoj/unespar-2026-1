# Atividade prática — Inspeção de peças por segmentação de imagens

**Disciplina:** Computação Gráfica  
**Conteúdo:** Aula 19 — Segmentação de imagens, K-Médias e ISODATA  
**Ferramentas:** Python, NumPy e OpenGL (GLFW/PyOpenGL)  
**Material de apoio:** walkthrough de estudo independente, **seções 4 a 6**, e o código Python disponível na pasta de exemplos.

## 1. Situação-problema

Uma empresa utiliza uma câmera para inspecionar peças sobre uma esteira. A imagem contém um fundo, duas peças avermelhadas e uma peça amarelada. O sistema deve **identificar os pixels que pertencem às peças avermelhadas**, mesmo quando há pequenas variações de iluminação e ruído.

Nesta atividade, você utilizará os algoritmos **K-Médias** e **ISODATA** implementados no estudo guiado para resolver o problema e comparar os resultados. O objetivo não é reimplementar esses algoritmos, mas **aplicá-los, escolher parâmetros, medir resultados e interpretar limitações**.

> **Pré-requisito:** conclua as seções 4 e 5 do walkthrough, incluindo os `TODOs 04–08`. As seções 1–3 do código disponibilizado na pasta de exemplos já estão prontas e devem ser preservadas.

## 2. Parte A — Construção da imagem de inspeção

Crie uma nova cena diretamente como matriz NumPy RGB, de **72 linhas, 96 colunas e 3 canais**, sem Pillow ou arquivos de imagem externos. Utilize o código a seguir como ponto de partida:

```python
import numpy as np


def criar_cena_inspecao():
    h, w = 72, 96
    yy, xx = np.mgrid[:h, :w]

    imagem = np.full((h, w, 3), (70, 90, 115), dtype=np.uint8)

    # Duas peças da mesma família de cor, mas desconectadas.
    peca_1 = (xx - 24)**2 + (yy - 26)**2 <= 11**2
    peca_2 = (xx - 72)**2 + (yy - 47)**2 <= 9**2
    mascara_referencia = peca_1 | peca_2

    # Uma terceira peça de outra cor.
    peca_3 = (xx >= 48) & (xx < 64) & (yy >= 12) & (yy < 31)

    imagem[mascara_referencia] = (205, 95, 70)
    imagem[peca_3] = (208, 161, 72)

    # Variações controladas de iluminação e ruído.
    rng = np.random.default_rng(25)
    luz = 14.0 * (xx / (w - 1) - 0.5)
    ruido = rng.normal(0, 4, size=(h, w, 1))
    imagem = np.clip(
        imagem.astype(float) + luz[..., None] + ruido,
        0, 255
    ).astype(np.uint8)

    return imagem, mascara_referencia
```

A variável `mascara_referencia` é uma matriz booleana que indica os pixels das **duas peças vermelhas**. Ela representa a resposta correta conhecida para este cenário sintético e será usada na avaliação quantitativa dos resultados.

**Integração com o programa:** adapte `criar_cena(variacao)` para que a cena `1`, acessível pela tecla `T`, utilize `criar_cena_inspecao()[0]`. Preserve a cena `0` original. A máscara de referência pode ser recuperada separadamente por `_, referencia = criar_cena_inspecao()` para os cálculos solicitados adiante.

**Observe:** existem *três objetos* sobre o fundo, mas somente *duas famílias principais de cor dos objetos*. O número de objetos físicos não precisa coincidir com o número de clusters.

## 3. Parte B — Segmentar com K-Médias

Execute o programa e visualize a nova cena (`T`). Utilize os modos `5` (classificação inicial), `6` (iterações) e `7` (resultado final). Faça os seguintes testes, mantendo a cena idêntica:

| Teste | K | Semente (`seed`) | O que observar |
|---|---:|---:|---|
| A | 2 | 5 | Cores diferentes acabam no mesmo grupo? |
| B | 3 | 5 | As duas peças vermelhas recebem o mesmo rótulo? |
| C | 5 | 5 | Alguma peça é dividida em grupos de cores semelhantes? |
| D | 3 | 6 | A mudança da inicialização altera o resultado? |

As teclas `K` e `R` permitem modificar `K` e a semente na demonstração. Para os resultados **reproduzíveis**, você também pode chamar diretamente a função existente:

```python
centros, rotulos = executar_kmedias(
    imagem, k=3, passos=20, seed=5
)
```

As dimensões esperadas são `centros.shape == (K, 3)` e `rotulos.shape == (72, 96)`. Cada valor da matriz `rotulos` é o **índice de um cluster**, não o valor RGB nem o número de um objeto.

**Implementação nova:** crie uma função `mascara_por_cor(centros, rotulos, cor_alvo)` que encontre o centroide RGB mais próximo da cor `(205, 95, 70)` e produza uma máscara booleana com os pixels pertencentes a esse cluster. Esta função não precisa alterar os algoritmos de K-Médias; deve utilizar seus resultados.

**Cuidado conceitual:** selecionar o centroide mais próximo da cor desejada é apenas uma estratégia para escolher um cluster. Ela pode falhar se duas cores diferentes forem agrupadas ou se uma peça for dividida em vários clusters.

## 4. Parte C — Segmentar com ISODATA

Utilize a mesma cena e execute o algoritmo simplificado de ISODATA disponível no programa. Acompanhe os modos `8` e `9` (tecla `N` para avançar as etapas) e compare os resultados no modo `0`.

Faça um teste iniciado com dois grupos e limite de seis grupos:

```python
centros_i, rotulos_i, eventos = executar_isodata(
    imagem, k=2, passos=12, seed=5, max_grupos=6
)
```

Registre a **quantidade inicial e final de grupos** e a sequência de eventos (`divisao`, `fusao`, `reajuste`). Repita com `seed=6` e compare os resultados. **Não é obrigatório que ocorram divisão e fusão em todos os testes**: registre os eventos observados, sem inventar resultados.

Aplique a função `mascara_por_cor` também ao resultado do ISODATA. Lembre-se de que, nesta implementação didática, o algoritmo pode alterar o número de grupos com base na **dispersão RGB** e na **distância entre centroides**.

## 5. Parte D — Medir a qualidade da segmentação

Como a imagem foi criada no próprio programa, conhecemos exatamente os pixels das duas peças vermelhas. Essa informação permite comparar quantitativamente as máscaras estimadas com a máscara de referência.

Implemente uma função `calcular_iou(mascara_estimada, mascara_referencia)`, que devolva a métrica **Intersection over Union (IoU)**:

\[
IoU = \frac{|M_{estimada} \cap M_{referencia}|}{|M_{estimada} \cup M_{referencia}|}.
\]

O valor varia de `0` a `1`: `1` significa correspondência perfeita; `0` significa ausência de interseção. Para implementar, utilize operações booleanas do NumPy (`&` e `|`) e a contagem de pixels verdadeiros. Trate explicitamente o caso de união vazia.

Preencha a tabela com os resultados reais de sua execução:

| Método | Configuração | Grupos finais | IoU das peças vermelhas | Observação |
|---|---|---:|---:|---|
| K-Médias | K=2, seed=5 | | | |
| K-Médias | K=3, seed=5 | | | |
| K-Médias | K=5, seed=5 | | | |
| K-Médias | K=3, seed=6 | | | |
| ISODATA | inicial=2, seed=5 | | | |
| ISODATA | inicial=2, seed=6 | | | |

**Questão central:** um algoritmo que produz mais grupos necessariamente identifica melhor as peças vermelhas? Utilize os valores de IoU para fundamentar a resposta.

## 6. Análise e questões conceituais

Com base **nos resultados que você obteve**, responda:

1. Por que as duas peças vermelhas, mesmo distantes na imagem, podem pertencer a um **único cluster** de K-Médias?
2. Qual é a diferença entre identificar um **cluster de cor** e identificar um **objeto conectado**?
3. Em que situação aumentar `K` melhora a separação? Quando pode piorá-la?
4. Qual foi o efeito da mudança da semente (`seed`) sobre a segmentação?
5. Quais eventos ocorreram no ISODATA? Explique por que os limiares de **desvio padrão** e de **distância entre centroides** podem provocar divisão e fusão.
6. Qual configuração apresentou o melhor resultado de IoU? Esse resultado também foi o mais adequado visualmente? Justifique.

**Desafio opcional — conexão com a Seção 3:** utilize `crescimento_regiao` com uma semente dentro da primeira peça vermelha. Compare sua máscara com a máscara formada por cluster RGB. Explique por que o crescimento pode selecionar **somente uma peça**, enquanto a máscara por cluster pode incluir **as duas peças desconectadas**.

## 7. Entrega

Envie um único arquivo `.zip` contendo:

- **Código Python** que execute a imagem de inspeção e os experimentos; as funções `mascara_por_cor` e `calcular_iou` devem estar implementadas.
- **Relatório curto em Markdown ou PDF**, com a tabela preenchida, as seis respostas e comentários sobre os melhores e piores resultados.
- **Três capturas do OpenGL:** imagem original, segmentação por K-Médias e segmentação por ISODATA (informe a configuração de cada captura).

Utilize os algoritmos desenvolvidos nas seções 4–6 do walkthrough. Não substitua a implementação por `sklearn.cluster.KMeans`, `cv2.kmeans` ou uma biblioteca pronta de ISODATA. Não é necessário recriar os algoritmos já concluídos na aula nem modificar os conteúdos das seções 1–3.

### Critérios de avaliação

| Critério | Peso |
|---|---:|
| Integração da cena sintética à aplicação OpenGL | 20% |
| Experimentos reproduzíveis com K-Médias e ISODATA | 25% |
| Implementação das máscaras e cálculo correto de IoU | 25% |
| Análise dos resultados e respostas conceituais | 30% |
| **Total** | **100%** |

---

**Resultado esperado da atividade:** demonstrar, com exemplos visuais e uma métrica quantitativa, que **segmentar pixels por similaridade de cor não é o mesmo que reconhecer objetos individuais**. O K-Médias utiliza um número fixo de clusters; o ISODATA didático pode dividi-los ou fundi-los. A adequação dos resultados depende das características da imagem e dos parâmetros utilizados.


## Entrega

Entrega via link: [https://forms.gle/chYU4i3rT6Cv5X6r5](https://forms.gle/chYU4i3rT6Cv5X6r5)

Entrega até 24/11/2026
