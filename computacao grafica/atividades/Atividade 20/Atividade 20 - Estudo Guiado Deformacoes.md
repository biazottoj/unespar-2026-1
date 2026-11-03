# Estudo guiado dos alunos — Aula 17, seções 7 a 10: Transformada de Hough

**Disciplina:** Computação Gráfica  
**Formato:** teoria → cálculo manual → experimento com matrizes NumPy → visualização OpenGL → interpretação.  
**Material de referência:** parte *Transformada de Hough* do PDF *17 Deformações* (UNESPAR), correspondente às seções 7–10 do roteiro ampliado da aula.  
**Objetivo:** compreender como pixels de borda podem votar em retas e círculos sem recorrer a bibliotecas prontas de visão computacional.

> **Este estudo é independente da aula presencial (etapas 1–6).** O programa principal da aula vai até o preenchimento por borda e oferece modos `0` a `5`. Para realizar os experimentos aqui, execute **`apoio_hough_opengl_modos6_a_9.py`**, um programa complementar com modos `6` a `9`.

## Preparação do ambiente

Instale uma única vez:

```bash
python -m pip install numpy glfw PyOpenGL
```

Abra o programa de estudo:

```bash
python apoio_hough_opengl_modos6_a_9.py
```

| Tecla | O que observar |
|---|---|
| `6` | Matriz binária contendo três conjuntos de pixels alinhados |
| `7` | Acumulador de votos de retas — parâmetros $(\rho,\theta)$ |
| `8` | Três retas reconstruídas a partir dos picos do acumulador |
| `9` | Dois círculos de raio conhecido e centros identificados |
| `N` | Adiciona ou remove ruído sintético, reprodutível |
| `H` / `Esc` | Ajuda no terminal / encerrar |

As imagens são matrizes NumPy. A CPU calcula Hough; o OpenGL **apenas desenha** os resultados. Não há Pillow, OpenCV nem arquivos PNG.

---

## 7. Transformada de Hough: definição, representação e aplicações

### 7.1. O que é?

A **Transformada de Hough** é uma técnica de detecção de formas descritas por parâmetros. Cada pixel identificado como candidato (por exemplo, um pixel de borda) **vota nos parâmetros das formas que poderiam passar por ele**. O resultado é um **acumulador**: uma matriz em que células com muitos votos indicam formas apoiadas por muitos pixels.

- **Entrada:** normalmente uma matriz binária de bordas, com `1` representando um pixel candidato.
- **Processamento:** transformar coordenadas dos pixels em votos em um espaço de parâmetros.
- **Saída:** parâmetros das linhas, círculos ou outras formas com altos votos.
- **Aplicações:** faixas de rodagem, alinhamento de documentos, localização de círculos/furos e inspeção de peças industriais.

**Diferença para os conteúdos anteriores:** deformação muda posições; preenchimento propaga uma cor entre vizinhos; Hough **encontra regularidades geométricas** a partir de muitos pontos.

### 7.2. Um ponto pertence a infinitas retas

Uma reta pode ser descrita por `y = mx + b`, mas a representação por inclinação tem uma dificuldade para retas verticais. Usaremos a forma polar da reta:

$$
\rho=x\cos\theta+y\sin\theta.
$$

- $(x,y)$: coordenadas de um pixel de borda.
- $\theta$: ângulo da **normal** à reta, não o ângulo da própria linha.
- $\rho$: distância orientada da origem à reta.

Para um mesmo ponto, ângulos diferentes produzem distâncias diferentes. Ou seja, **um pixel gera vários votos**, um por ângulo testado.

### 7.3. Cálculo manual

Para o pixel $(x,y)=(3,4)$:

| $\theta$ | Expressão | $\rho$ aproximado |
|---|---|---:|
| $0°$ | $3(1)+4(0)$ | $3$ |
| $45°$ | $3(0,7071)+4(0,7071)$ | $4,95$ |
| $90°$ | $3(0)+4(1)$ | $4$ |

**Faça antes de executar:** considerando também os pixels `(3,5)` e `(3,6)`, qual par $(\rho,\theta)$ deve receber votos repetidos? Como os três pontos têm a mesma coluna `x=3`, a linha vertical `x=3` corresponde a $\theta=0°$ e $\rho=3$.

### 7.4. Experimento no OpenGL

1. Pressione `6` para ver os três agrupamentos lineares.
2. Responda: onde estão as linhas diagonais? Há também uma linha vertical?
3. Pressione `N`. Identifique os pontos adicionais que não obedecem às linhas anteriores.
4. Explique por que o programa cria **uma matriz binária** para esse cenário, em vez de aplicar Hough diretamente à imagem RGB.

---

## 8. Hough linear: matriz acumuladora e detecção de retas

### 8.1. Discretizar o espaço de parâmetros

Na prática, não podemos testar todos os ângulos reais. O programa utiliza $\theta=0,2,4,\ldots,178°$ e distâncias $\rho$ inteiras.

Para uma imagem de altura `h` e largura `w`:

```python
thetas = np.deg2rad(np.arange(0, 180, 2, dtype=np.float32))
dist_max = int(np.ceil(np.hypot(h - 1, w - 1)))
rhos = np.arange(-dist_max, dist_max + 1, dtype=np.int32)
votos = np.zeros((len(rhos), len(thetas)), dtype=np.int32)
```

**Por que `dist_max`?** A diagonal limita a magnitude de $\rho$ necessária para cobrir os pontos da imagem. **Por que somar `dist_max` ao índice?** Para converter distâncias negativas e positivas em índices não negativos de NumPy.

### 8.2. Como funciona a votação

Abra `acumulador_hough_linear(...)` no arquivo de apoio. O núcleo da função é:

```python
for y, x in zip(*np.nonzero(bordas)):
    for ti, theta in enumerate(thetas):
        rho = int(round(x * np.cos(theta) + y * np.sin(theta)))
        votos[rho + dist_max, ti] += 1
```

**Leia com atenção:** o código não procura linhas diretamente. Para cada pixel ativo, soma votos às células correspondentes às retas compatíveis com esse pixel.

**Teste rápido no terminal (sem abrir janela):**

```python
import numpy as np
from apoio_hough_opengl_modos6_a_9 import acumulador_hough_linear

imagem = np.zeros((20, 20), dtype=np.uint8)
imagem[2:18, 7] = 1  # 16 pixels na coluna x=7
A, rhos, angulos = acumulador_hough_linear(imagem)
indice_rho = int(np.where(rhos == 7)[0][0])
print(A[indice_rho, 0])  # esperado: 16 votos em rho=7, theta=0
```

### 8.3. Interpretação do acumulador

Pressione `7`. No painel direito, o eixo horizontal representa **ângulo theta** e o vertical representa **distância rho**. Esse painel **não é a imagem original**: é uma visualização da matriz de votos.

- Um **pico** indica que muitos pontos compartilham um conjunto de parâmetros de reta.
- O ruído (`N`) distribui votos em muitas células, normalmente de forma dispersa.
- A discretização pode deslocar picos para células próximas.

### 8.4. Selecionar picos e reconstruir

Abra `picos_hough_linear(...)`:

1. Ordene as células por votação decrescente.
2. Ignore aquelas com menos de `min_votos`.
3. Descarte picos muito próximos dos já selecionados (supressão local).
4. Converta os índices de células em $(\rho,\theta)$.

O desenho das linhas testa, aproximadamente,

$$|x\cos\theta+y\sin\theta-\rho|\leq 0,65.$$

Pressione `8` para comparar as retas detectadas em vermelho com os pontos de borda.

**Limitação proposital da demonstração:** as linhas são prolongadas em toda a imagem e a supressão de picos é simples. Ela não resolve completamente equivalências entre representações próximas dos limites angulares.

### 8.5. Pequeno experimento orientado

Modifique **um parâmetro por vez** e registre os resultados:

| Parâmetro | Valor original | Valor experimental | O que registrar? |
|---|---|---|---|
| `passo_angular` | `2` | `5` graus | Precisão dos picos e tempo |
| `min_votos` (retas) | `27` | `45` | Quantas retas sobrevivem? |
| `quantidade` | `3` | `1` | Quais retas deixam de aparecer? |
| Ruído `N` | desligado | ligado | Picos mais ou menos nítidos? |

---

## 9. Hough circular: votar nos centros possíveis

### 9.1. Parâmetros do círculo

Um círculo pode ser descrito por:

$$
(x-a)^2+(y-b)^2=r^2,
$$

em que $(a,b)$ é o centro e $r$ é o raio. Se o raio também fosse desconhecido, precisaríamos procurar o espaço **tridimensional** $(a,b,r)$. Aqui o programa fixa `r=13`, como simplificação didática.

### 9.2. Como um ponto de borda vota em centros

Para cada pixel da circunferência $(x,y)$ e ângulo candidato $\alpha$:

$$a=x-r\cos\alpha,\qquad b=y-r\sin\alpha.$$

Abra `acumulador_hough_circular(...)` no arquivo de apoio e encontre:

```python
for y, x in zip(*np.nonzero(bordas)):
    for dx, dy in offsets:
        cx, cy = x - dx, y - dy
        if 0 <= cx < w and 0 <= cy < h:
            votos[cy, cx] += 1
```

Os pares de deslocamentos são arredondados e repetidos removidos. Assim, vários pixels na mesma circunferência reforçam os votos no seu centro verdadeiro.

### 9.3. Como selecionar os centros

A função `picos_hough_circular` usa duas verificações: **limiar mínimo de votos** e **distância mínima entre centros aceitos**. Sem a segunda, os dois picos selecionados poderiam ser dois pixels próximos do mesmo círculo.

### 9.4. Teste OpenGL e previsão

1. Pressione `9` e observe os dois círculos de raio 13.
2. Os centros esperados na matriz sintética são **`(22, 29)` e `(55, 47)`**, na ordem `(x,y)`.
3. Pressione `N` e verifique se a detecção continua estável.
4. Altere o raio de busca de `13` para `11` **somente na chamada** a `acumulador_hough_circular` em `preparar_paineis`; observe o resultado e restaure para `13`.
5. Explique por que a matriz de votos se dispersa quando o raio está incorreto.

---

## 10. Roteiro de estudo e integração teoria–prática

Siga a ordem abaixo, preferencialmente anotando uma previsão antes de cada execução:

| Momento | Teoria a explicar | Prática Python/OpenGL | Verificação |
|---|---|---|---|
| A | O que é Hough e o que é um pixel de borda | `criar_cenario_linhas`; modo `6` | Três padrões de linha |
| B | Equação polar e votos de um ponto | `acumulador_hough_linear`; modo `7` | Pico em $(\rho,\theta)$ |
| C | Limiar e supressão local | `picos_hough_linear`; modo `8` | Três retas sem ruído |
| D | Equação do círculo e centros candidatos | `acumulador_hough_circular`; modo `9` | Dois centros corretos |
| E | Robustez e escolha de parâmetros | Tecla `N` e edição de limiares | Discutir erros e limitações |

### Perguntas para entregar junto aos testes

1. Qual a diferença entre acumular votos e percorrer pixels vizinhos no flood fill?
2. Por que usamos $(\rho,\theta)$, e não apenas $(m,b)$, para detecção de retas?
3. Por que um único pixel de borda não determina uma reta?
4. O que representa um pico intenso na matriz acumuladora?
5. Por que Hough circular com raio desconhecido precisa de uma dimensão adicional?
6. Explique a diferença entre **detectar a reta infinita** e identificar um **segmento** de reta.
7. O que mudou com o ruído? Faça referência a pelo menos um teste concreto.

### Critérios para concluir o estudo

- Você sabe explicar as fórmulas de Hough linear e circular e interpretar cada parâmetro.
- Executou os modos `6`–`9` e testou o ruído.
- Identificou as três retas sintéticas e os dois centros circulares em cenário sem ruído.
- Sabe justificar os limiares e as limitações da discretização, em vez de apenas copiar a saída do programa.

**Conexão com a atividade semanal:** as técnicas de deformação/preenchimento e Hough podem ser usadas em um mesmo cenário de inspeção de peças. A atividade semanal apresenta requisitos e entregáveis próprios.
