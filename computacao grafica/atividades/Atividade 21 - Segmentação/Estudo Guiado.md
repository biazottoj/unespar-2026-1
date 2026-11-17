# Estudo guiado — Segmentação de Imagens: K-Médias e ISODATA

**Disciplina:** Computação Gráfica  
**Aula 19 — continuação a partir da Seção 4**  
**Linguagens e bibliotecas:** Python, NumPy e OpenGL (GLFW/PyOpenGL)  
**Material de apoio:** slides da aula de Segmentação de Imagens; arquivo Python disponibilizado na **pasta de exemplos**.

## Antes de começar: como utilizar este material

O objetivo é continuar o programa de segmentação, não iniciar outro projeto. Em cada seção, leia a explicação, faça a conta proposta, localize a função indicada no código, implemente-a e execute o modo OpenGL correspondente. **Salve o arquivo e teste após cada mudança**: não deixe todos os testes para o final.

No terminal, abra a pasta em que está o código da aula e instale as dependências, caso ainda não estejam presentes:

```bash
python -m pip install numpy glfw PyOpenGL
```

Execute o arquivo da pasta de exemplos (na versão original, ele se chama `segmentacao.py`):

```bash
python segmentacao.py
```

Se o professor disponibilizou o arquivo com outro nome, use esse nome no comando. Não é necessário baixar imagens: o programa cria duas cenas sintéticas diretamente como matrizes NumPy de **72 linhas × 96 colunas × 3 canais RGB**, com valores de **0 a 255**. O **NumPy calcula** a segmentação; o **OpenGL exibe** as matrizes resultantes.

### Controles que você utilizará

| Tecla | Resultado / função |
|---|---|
| `5` | Inicialização e atribuição inicial do K-Médias |
| `6` | K-Médias após um determinado número de iterações |
| `7` | K-Médias após até 20 iterações ou convergência |
| `8` | Inicialização dos grupos do ISODATA |
| `9` | ISODATA passo a passo |
| `0` | Comparação entre original, K-Médias e ISODATA |
| `N` | Avança uma etapa **somente** nos modos `6` e `9` |
| `K` | Altera o valor de `K` entre `2` e `6` |
| `R` | Muda a semente aleatória usada para iniciar os grupos |
| `T` | Alterna entre as duas imagens sintéticas |
| `B` | Mostra ou esconde as fronteiras entre **rótulos** |
| `H` | Exibe os atalhos no terminal |
| `Esc` | Encerra o programa |

**Atenção:** os modos podem abrir antes de suas funções estarem completas, porque o arquivo inicial contém **retornos provisórios**. Uma imagem quase uniforme ou um único grupo não prova que a segmentação está funcionando. Os títulos e dados dos resultados aparecem **no título da janela e no terminal**, não necessariamente desenhados sobre a imagem.

---

# Seção 4 — K-Médias: como formar grupos de pixels

**Slides para acompanhar:** “K-Médias: conceito” até “Experimento: qualidade e limitações”.  
**Funções a concluir:** `iniciar_centroides`, `atribuir_clusters`, `atualizar_centroides` e `iteracao_kmedias` (`TODOs 04–07`).

## 4.1. O que é K-Médias?

**K-Médias (K-Means)** é um algoritmo de **agrupamento não supervisionado**. Ele procura dividir um conjunto de dados em `K` grupos, aproximando cada elemento do **centroide** mais próximo. Um centroide é um vetor que representa os valores médios dos elementos do grupo.

Nesta aula, cada pixel é representado por um vetor RGB:

```text
Pixel p = (R, G, B)
         (210, 88, 65)
```

Portanto, um centroide também tem três componentes, como `(200, 80, 70)`. O algoritmo não conhece nomes como “céu”, “árvore” ou “casa”: ele **agrupa cores semelhantes**.

Uma iteração de K-Médias tem duas operações principais:

1. **Atribuição:** encontrar o centroide mais próximo de cada pixel.
2. **Atualização:** calcular a média RGB dos pixels atribuídos a cada centroide.

Essas operações se repetem enquanto a composição dos grupos continua mudando, respeitando o limite de iterações.

### Uma distinção importante: cor não é posição

Dois pixels verdes, mesmo em partes distantes da imagem, podem receber o **mesmo rótulo**, porque a versão implementada usa **somente os três valores RGB**, sem considerar as coordenadas `(x, y)`. Assim, **um grupo de cor não é necessariamente uma única região conectada**. Isso diferencia K-Médias do crescimento de regiões estudado na Seção 3.

### Aplicações

O K-Médias pode ser empregado para reduzir a paleta de cores de uma imagem, separar grandes regiões de aparência semelhante, preparar máscaras para outras técnicas e explorar imagens com vários materiais ou cores dominantes. A qualidade depende da imagem, do valor de `K` e da inicialização dos centroides.

## 4.2. Como o programa representa os pixels?

Procure, no arquivo Python, a função `produzir_paineis`. Antes de executar os modos de agrupamento, ela transforma a imagem em uma matriz de pixels:

```python
pixels = img.reshape(-1, 3).astype(float)
```

Se a imagem possui `72 × 96` pixels, o resultado tem `6912` linhas e `3` colunas:

```text
Imagem original:  (72, 96, 3)
Lista de pixels:  (6912, 3)

[[ R0, G0, B0 ],
 [ R1, G1, B1 ],
 [ R2, G2, B2 ],
 ...]
```

O tipo `float` é importante: durante o cálculo de diferenças e médias, precisamos de valores negativos e fracionários intermediários; usar aritmética sem cuidado em `uint8` poderia provocar estouro.

## 4.3. Primeiro cálculo manual: distância RGB

Para decidir qual centroide representa um pixel, usamos a **distância euclidiana**:

\[
d(p,c)=\sqrt{(R_p-R_c)^2+(G_p-G_c)^2+(B_p-B_c)^2}.
\]

Considere:

```text
Pixel:      p  = (210, 88, 65)
Centroide:  c0 = (200, 80, 70)
Centroide:  c1 = ( 80,170,115)
```

Para `c0`:

\[
d^2(p,c_0)=10^2+8^2+(-5)^2=189.
\]

Para `c1`:

\[
d^2(p,c_1)=130^2+(-82)^2+(-50)^2=26124.
\]

**Resultado:** o pixel pertence ao grupo `0`, pois `189 < 26124`. Observe que **não precisamos calcular a raiz quadrada** para identificar o menor valor: a ordem das distâncias permanece igual.

**Verifique antes de continuar:** se dois centroides tiverem exatamente a mesma distância, `np.argmin` escolhe o de **menor índice** entre os empatados.

## 4.4. Prática 1 — `TODO 04`: inicializar os centroides

Encontre no seu código a função:

```python
def iniciar_centroides(pixels, k=4, semente_aleatoria=5):
```

A tarefa é selecionar `K` pixels **existentes na imagem** para servir de centroides iniciais. A seleção é pseudoaleatória: ao informar a mesma semente, obtemos a mesma escolha, o que facilita reproduzir os experimentos.

**Substitua o retorno provisório** desta função pelo código:

```python
def iniciar_centroides(pixels, k=4, semente_aleatoria=5):
    dados = np.asarray(pixels, dtype=float).reshape(-1, 3)
    rng = np.random.default_rng(semente_aleatoria)
    inds = rng.choice(len(dados), size=k, replace=False)
    return dados[inds].copy()
```

**Entenda cada linha:**

- `reshape(-1, 3)` garante uma linha por pixel RGB, independentemente da organização de entrada.
- `default_rng(semente_aleatoria)` inicializa o gerador de números pseudoaleatórios.
- `choice(..., replace=False)` escolhe `K` **posições distintas** da lista de pixels; pixels diferentes ainda podem ter a **mesma cor**.
- `dados[inds]` recupera os valores RGB escolhidos.

**Checkpoint:** por enquanto, a imagem do modo `5` pode continuar errada, pois `atribuir_clusters` ainda é provisória. Não confunda **concluir a inicialização** com **concluir o K-Médias**.

## 4.5. Prática 2 — `TODO 05`: atribuir cada pixel a um grupo

Procure:

```python
def atribuir_clusters(pixels, centroides):
```

Precisamos de uma matriz em que cada **linha** representa um pixel e cada **coluna** representa um centroide. Se houver `6912` pixels e `4` centroides, teremos **6912 × 4 distâncias**.

Use a implementação:

```python
def atribuir_clusters(pixels, centroides):
    dados = np.asarray(pixels, dtype=float).reshape(-1, 3)
    cs = np.asarray(centroides, dtype=float).reshape(-1, 3)

    distancias_quadradas = np.sum(
        (dados[:, None, :] - cs[None, :, :]) ** 2,
        axis=2
    )

    return np.argmin(distancias_quadradas, axis=1).astype(np.int32)
```

**Como entender o NumPy:**

- `dados[:, None, :]` tem dimensões `(N, 1, 3)`.
- `cs[None, :, :]` tem dimensões `(1, K, 3)`.
- O NumPy combina os vetores para calcular as diferenças RGB para **cada par pixel–centroide**.
- `np.sum(..., axis=2)` soma os três quadrados `(R, G, B)`, produzindo a matriz `(N, K)`.
- `np.argmin(..., axis=1)` encontra o índice do centroide mais próximo para cada pixel.

A função devolve um vetor **inteiro de rótulos**, como `[0, 0, 2, 1, 2, ...]`, e **não** a imagem RGB segmentada. A conversão de rótulos em cores já é feita pelo programa, por meio de `exibir_rotulos`.

**Teste na janela:** pressione `5`. Deve aparecer a imagem original e, ao lado, a imagem recolorida pelos centroides iniciais. Pressione `R` para mudar a escolha inicial e `K` para mudar a quantidade de grupos. Ainda não espere a melhor segmentação: os centroides **não foram recalculados**.

## 4.6. Segundo cálculo manual: atualização dos centroides

Considere agora quatro pixels em tons de cinza, representados aqui por um único valor para facilitar a conta:

```text
Pixels:           [20, 30, 200, 210]
Centroides iniciais: [20, 200]
```

A atribuição gera dois grupos:

```text
Grupo 0: [20, 30]
Grupo 1: [200, 210]
```

As novas médias são:

\[
\mu_0=\frac{20+30}{2}=25,
\qquad
\mu_1=\frac{200+210}{2}=205.
\]

Com RGB, a atualização funciona da mesma maneira, mas cada canal recebe sua própria média. Por exemplo, a média entre `(200, 80, 70)` e `(220, 100, 90)` é `(210, 90, 80)`.

## 4.7. Prática 3 — `TODO 06`: atualizar os centroides

Encontre:

```python
def atualizar_centroides(pixels, rotulos, centroides):
```

Substitua o retorno provisório por:

```python
def atualizar_centroides(pixels, rotulos, centroides):
    dados = np.asarray(pixels, dtype=float).reshape(-1, 3)
    novos = np.asarray(centroides, dtype=float).copy()

    for i in range(len(novos)):
        membros = dados[rotulos == i]
        if len(membros):
            novos[i] = np.mean(membros, axis=0)
        # Se o grupo estiver vazio, mantemos o centroide anterior.

    return novos
```

O trecho `rotulos == i` seleciona as posições de todos os pixels atribuídos ao grupo `i`. O cálculo `np.mean(..., axis=0)` obtém **as três médias RGB**.

**Por que verificar `if len(membros)`?** Um grupo pode ficar vazio caso nenhum pixel seja mais próximo de seu centroide. Nesse caso, a política deste programa é **manter o centroide anterior**, evitando uma média sobre uma lista vazia. Existem outras políticas possíveis, mas não as utilizaremos nesta versão.

## 4.8. Prática 4 — `TODO 07`: completar uma iteração

Agora conecte as duas funções implementadas. Procure:

```python
def iteracao_kmedias(pixels, centroides):
```

Substitua seu corpo por:

```python
def iteracao_kmedias(pixels, centroides):
    rotulos = atribuir_clusters(pixels, centroides)
    novos = atualizar_centroides(pixels, rotulos, centroides)
    return novos, rotulos
```

**Atenção à ordem do retorno:** o código que executa o K-Médias espera **`(centroides, rotulos)`**, exatamente nessa ordem. Não troque os valores.

A função `executar_kmedias`, que já existe no arquivo, chama repetidamente `iteracao_kmedias` e verifica se os rótulos estabilizaram. Ao terminar, faz uma classificação final usando os centroides resultantes. Você **não precisa reescrever** `executar_kmedias`.

### Checkpoint de K-Médias no terminal

Salve o arquivo e execute este teste simples **na mesma pasta do programa**. Caso o arquivo tenha outro nome, altere apenas o `import`:

```bash
python - <<'PY'
import numpy as np
from aula19_segmentacao_base import iteracao_kmedias

pixels = np.array([
    [20, 20, 20],
    [30, 30, 30],
    [200, 200, 200],
    [210, 210, 210],
], dtype=float)
centroides = np.array([[20, 20, 20], [200, 200, 200]], dtype=float)

novos, rotulos = iteracao_kmedias(pixels, centroides)
print('Centroides:', novos)
print('Rótulos:', rotulos)
PY
```

**Resultado esperado:** centroides `[[25.,25.,25.],[205.,205.,205.]]` (o NumPy pode exibir espaços diferentes) e rótulos `[0, 0, 1, 1]`.

**Se não funcionar:** confira se `atribuir_clusters` retorna **um rótulo por pixel**, se as médias são calculadas com `axis=0` e se os dados estão em `float`.

### Checkpoint visual do K-Médias

Execute novamente o programa OpenGL e compare:

1. Pressione `5`: **classificação inicial**, sem otimização iterativa.
2. Pressione `6`: **uma iteração**. Pressione `N` algumas vezes para aumentar o número de iterações exibido. O programa recalcula o resultado a partir das mesmas sementes iniciais até o número de etapas indicado.
3. Pressione `7`: resultado de **até 20 iterações**, encerrando antes se os rótulos estabilizarem.
4. Pressione `K` para avaliar mais ou menos grupos. Reinicie o programa para retornar à configuração inicial, se necessário.
5. Pressione `R` para mudar a inicialização e `T` para trocar a cena.
6. Pressione `B` para visualizar as fronteiras entre os **rótulos produzidos**.

**Perguntas de reflexão:** o que muda quando `K` aumenta? Por que pressionar `R` pode mudar a segmentação sem alterar a imagem? Duas regiões desconectadas podem ter a mesma cor de saída? Por quê?

**Conclua a Seção 4 somente quando** os modos `5`, `6` e `7` exibirem agrupamentos diferentes conforme a etapa, `K` e `R` tiverem efeito e o teste numérico mostrar os centroides corretos.

---

# Seção 5 — ISODATA: como dividir e unir grupos automaticamente

**Slides para acompanhar:** “ISODATA: por que modificar a quantidade de grupos?” até “Comparação final: K-Médias e ISODATA”.  
**Função a concluir:** `iteracao_isodata` (`TODO 08`).

## 5.1. Por que não utilizar somente K-Médias?

O K-Médias convencional começa com um número fixo de grupos `K`. Entretanto, é possível escolher poucos grupos e misturar elementos diferentes ou escolher muitos grupos e separar desnecessariamente cores semelhantes.

O **ISODATA** (*Iterative Self-Organizing Data Analysis Technique Algorithm*) é uma família de procedimentos de agrupamento iterativo que combina atribuição/atualização de centroides com regras de **divisão** e **fusão** de grupos. Assim, o número de grupos pode mudar durante o processamento.

Nesta aula, usaremos um **ISODATA didático e simplificado**. Ele realiza inicialmente uma atualização de K-Médias, elimina centroides sem membros e pode realizar **no máximo uma fusão ou uma divisão em cada etapa**. Não se trata de uma implementação completa de todas as variantes clássicas de ISODATA.

### As duas decisões principais

**Fusão:** dois grupos possuem centroides próximos no espaço RGB. O algoritmo pode reuni-los em um só grupo para evitar divisões desnecessárias.

**Divisão:** um grupo apresenta **grande dispersão** de cores. O algoritmo pode criar dois centroides e permitir que, na próxima classificação, esses pixels sejam separados.

As distâncias e desvios considerados aqui usam **cores RGB na escala 0–255**, não a distância espacial entre os pixels da imagem.

## 5.2. Exemplo manual — fusão de grupos

Imagine dois grupos com médias escalares e quantidades diferentes de elementos:

```text
Grupo A: média = 100; 20 pixels
Grupo B: média = 110; 10 pixels
```

A distância entre os centroides é `10`. Se o limiar para fundir grupos for `28`, a distância `10 < 28` permite a fusão.

O centroide combinado é uma **média ponderada**:

\[
\mu_{AB}=\frac{20\cdot100+10\cdot110}{20+10}=103{,}33.
\]

Usar `(100+110)/2=105` seria incorreto para representar a média de **todos** os pixels, pois os grupos têm tamanhos diferentes. Em RGB, a média ponderada é calculada separadamente para os três canais.

## 5.3. Exemplo manual — divisão de grupos

Considere um grupo que contém muitas cores próximas de `(25, 55, 60)` e outras próximas de `(125, 55, 60)`.

A média do canal vermelho fica aproximadamente em `75`, mas os valores estão distantes da média: o **desvio padrão** do vermelho é alto. Isso sugere que o grupo pode estar misturando **duas distribuições**.

Uma simplificação utilizada na aula é:

1. Identificar o canal RGB de **maior desvio padrão**.
2. Criar duas cópias do centroide do grupo.
3. Diminuir `0,5 × desvio` em uma delas e aumentar `0,5 × desvio` na outra, **nesse canal**.
4. Deixar a próxima atribuição redistribuir os pixels entre os novos centroides.

A divisão não garante que os dois novos grupos correspondam a dois objetos reais; ela responde à **dispersão dos dados RGB**.

## 5.4. Conhecendo os parâmetros antes de programar

A assinatura encontrada no programa é:

```python
def iteracao_isodata(pixels, centroides, max_grupos=6, min_pixels=35,
                     desvio_divisao=25.0, distancia_fusao=28.0):
```

| Parâmetro | Função no algoritmo desta aula |
|---|---|
| `pixels` | Lista dos pixels RGB a classificar |
| `centroides` | Conjunto atual de grupos |
| `max_grupos` | Quantidade máxima de centroides após uma divisão |
| `min_pixels` | Parâmetro para impedir a divisão de grupos muito pequenos |
| `desvio_divisao` | Desvio padrão acima do qual a divisão pode ocorrer |
| `distancia_fusao` | Distância abaixo da qual dois centroides podem ser fundidos |

Nesta implementação, um grupo só pode ser dividido se possuir pelo menos `max(2 * min_pixels, 4)` pixels. Os limiares `25` e `28` são **parâmetros didáticos para estas cenas**, não valores ideais para qualquer imagem.

O **retorno** é uma tupla `(centroides_atualizados, evento)`. O evento será uma das strings `'fusao'`, `'divisao'` ou `'reajuste'`. O modo `9` usa essa string para mostrar o que aconteceu.

## 5.5. Prática — `TODO 08`: implementar um passo de ISODATA

Localize `iteracao_isodata`. A função de inicialização de centroides, de atribuição e de atualização do K-Médias **já deve estar pronta**, pois será reutilizada aqui.

O algoritmo será desenvolvido em quatro partes. Leia o propósito de cada uma **antes** de inserir a função completa apresentada abaixo.

**Parte A — Recalcular e remover grupos vazios.** Comece por `iteracao_kmedias`, conte quantos pixels pertencem a cada grupo e descarte os que não possuem membros. Atribua os rótulos novamente depois da remoção, porque os índices dos centroides podem ter mudado.

**Parte B — Tentar fundir.** Se houver mais de dois grupos, calcule as distâncias **entre os centroides** (não entre os pixels). Ignore a diagonal da matriz, porque a distância de um centroide para ele mesmo é zero. Se o par mais próximo estiver abaixo do limiar, calcule a média ponderada, remova um dos centroides e retorne `'fusao'`.

**Parte C — Tentar dividir.** Se ainda for permitido criar grupos, calcule o desvio padrão RGB dentro de cada grupo suficientemente grande. Escolha o grupo/canal com maior desvio que ultrapasse o limiar. Crie dois centroides deslocados no canal selecionado e retorne `'divisao'`.

**Parte D — Apenas reajustar.** Se nenhuma mudança estrutural for necessária, retorne os centroides atualizados e `'reajuste'`.

### Código guiado para substituir o `TODO 08`

```python
def iteracao_isodata(pixels, centroides, max_grupos=6, min_pixels=35,
                     desvio_divisao=25.0, distancia_fusao=28.0):
    # A. Executar uma atualização de K-Médias.
    dados = np.asarray(pixels, dtype=float).reshape(-1, 3)
    centros, labels = iteracao_kmedias(dados, centroides)

    # Remover grupos vazios e corrigir a indexação dos rótulos.
    contagens = np.bincount(labels, minlength=len(centros))
    ativos = [i for i, n in enumerate(contagens) if n > 0]
    centros = centros[ativos] if ativos else centros[:1]
    labels = atribuir_clusters(dados, centros)
    n = len(centros)

    # B. FUSÃO: procurar o par de centroides mais próximo.
    if n > 2:
        diferencas = centros[:, None, :] - centros[None, :, :]
        distancia = np.linalg.norm(diferencas, axis=2)
        np.fill_diagonal(distancia, np.inf)
        i, j = np.unravel_index(np.argmin(distancia), distancia.shape)

        if distancia[i, j] < distancia_fusao:
            ci, cj = np.sum(labels == i), np.sum(labels == j)
            media = (ci * centros[i] + cj * centros[j]) / max(1, ci + cj)
            centros = np.delete(centros, j, axis=0)
            centros[i if i < j else i - 1] = media
            return centros, 'fusao'

    # C. DIVISÃO: procurar um grupo suficientemente grande e disperso.
    if n < max_grupos:
        melhor = None
        for i in range(n):
            membros = dados[labels == i]
            if len(membros) < max(2 * min_pixels, 4):
                continue

            desvios = np.std(membros, axis=0)
            canal = int(np.argmax(desvios))
            if desvios[canal] > desvio_divisao:
                if melhor is None or desvios[canal] > melhor[0]:
                    melhor = (float(desvios[canal]), i, canal)

        if melhor is not None:
            desvio, i, canal = melhor
            a, b = centros[i].copy(), centros[i].copy()
            a[canal] = max(0, a[canal] - 0.5 * desvio)
            b[canal] = min(255, b[canal] + 0.5 * desvio)
            centros[i] = a
            centros = np.vstack((centros, b))
            return centros, 'divisao'

    # D. Nenhuma fusão ou divisão nesta etapa.
    return centros, 'reajuste'
```

**Leia com atenção:** a função tenta **fusão primeiro** e **divisão depois**. Esse detalhe é uma **escolha desta implementação didática** e influencia os resultados. A condição `n > 2` também significa que esta versão não funde grupos quando existem apenas dois. Não confunda esses parâmetros com propriedades universais do algoritmo ISODATA.

### Checkpoint de ISODATA no terminal

Salve seu arquivo e rode os dois cenários artificiais abaixo. O objetivo é provocar deliberadamente cada tipo de evento, sem depender da aparência da imagem no OpenGL.

```bash
python - <<'PY'
import numpy as np
from aula19_segmentacao_base import iteracao_isodata

# Três conjuntos: dois centroides têm cores próximas -> fusão.
fusao_pixels = np.vstack([
    np.tile([30., 30., 30.], (90, 1)),
    np.tile([45., 45., 45.], (90, 1)),
    np.tile([205., 205., 205.], (90, 1)),
])
fusao_centros = np.array([
    [30., 30., 30.], [45., 45., 45.], [205., 205., 205.]
])
novos, evento = iteracao_isodata(fusao_pixels, fusao_centros, max_grupos=5)
print('Teste de fusão:', evento, '| grupos:', len(novos))

# Dois conjuntos iniciais: um deles reúne vermelhos muito diferentes.
# O alto desvio provoca uma divisão.
divisao_pixels = np.vstack([
    np.tile([25., 55., 60.], (100, 1)),
    np.tile([125., 55., 60.], (100, 1)),
    np.tile([225., 220., 220.], (100, 1)),
])
divisao_centros = np.array([
    [75., 55., 60.], [225., 220., 220.]
])
novos, evento = iteracao_isodata(divisao_pixels, divisao_centros, max_grupos=4)
print('Teste de divisão:', evento, '| grupos:', len(novos))
PY
```

**Resultados esperados:**

```text
Teste de fusão: fusao | grupos: 2
Teste de divisão: divisao | grupos: 3
```

Se você obtiver somente `'reajuste'`, confira os cálculos de distância, os limites `n > 2` e `n < max_grupos`, a contagem mínima de pixels e o desvio padrão calculado com `axis=0`.

## 5.6. Checkpoint visual — observar a quantidade de grupos mudar

Execute o programa OpenGL:

1. Pressione `8` para inspecionar a **classificação inicial** do ISODATA; a configuração padrão começa com **3 grupos** (`K=4`, mas o modo usa `max(2, K-1)`).
2. Pressione `9` para executar **uma etapa**. Na cena inicial e com a semente aleatória padrão, o primeiro evento esperado é **`divisao`** (de 3 para 4 grupos).
3. Pressione `N` para avançar. Leia no **título da janela** e no **terminal** o evento mais recente.
4. **Reinicie o programa** para restaurar a semente inicial. Pressione `K` **duas vezes** para chegar a `K=6` e então pressione `9`: com essa configuração padrão, o primeiro evento esperado é **`fusao`**.
5. Pressione `T` para alterar a cena e `R` para experimentar outra escolha inicial. Observe se o mesmo evento ainda ocorre.
6. Pressione `0` para comparar **imagem original / K-Médias / ISODATA** em três painéis.

**Por que reiniciar no passo 4?** A tecla `K` altera a quantidade de grupos, mas **não redefine a semente aleatória**; `R` muda essa semente. Reiniciar torna o experimento reproduzível.

**Limitação importante:** o modo `9` **recalcula a sequência desde as mesmas sementes até a etapa selecionada**; não é uma execução em tempo real de um modelo que permanece evoluindo na memória entre os pressionamentos de `N`. Isso garante que uma mesma configuração mostre resultados reproduzíveis.

**Conclua a Seção 5 somente quando** o teste separado reproduzir `'fusao'` e `'divisao'`, e o modo `9` apresentar mudanças de grupos ou eventos coerentes com os parâmetros.

---

# Seção 6 — Comparação dos métodos e consolidação

**Slides para acompanhar:** “Controles do programa”, “Atividade prática orientada” e “Síntese da aula”.

## 6.1. Relembre as diferenças

| Técnica | Critério principal | Depende de semente? | Número de grupos | Região conectada? |
|---|---|---|---|---|
| Limiar fixo (Seção 2) | intensidade acima de `T` | não | duas classes | não necessariamente |
| Otsu (Seção 2) | limiar que separa estatisticamente intensidades | não | duas classes | não necessariamente |
| Crescimento (Seção 3) | conexão espacial + cor próxima da semente | **sim, pixel inicial** | uma região selecionada | sim, pela conectividade escolhida |
| K-Médias (Seção 4) | distância a centroides RGB | **sim, inicialização** | `K` fixo | não necessariamente |
| ISODATA didático (Seção 5) | centroides RGB + dispersão + proximidade | **sim, inicialização** | pode aumentar ou diminuir | não necessariamente |

**Não confunda:** a **semente do crescimento de regiões** é uma **posição `(x,y)`**; a **semente de K-Médias** é um **vetor inicial de características RGB**. São conceitos diferentes, apesar de ambos serem chamados de “sementes”.

## 6.2. Experimento integrado com duas cenas

Use **somente o arquivo Python desenvolvido a partir da pasta de exemplos**. Faça a sequência abaixo para cada uma das duas imagens (troque com `T`):

1. Abra o modo `5` com `K=4` e observe a atribuição inicial. Salve uma captura de tela.
2. Passe ao modo `7`, com o mesmo `K` e a mesma semente. Observe se a atualização dos centroides alterou o resultado.
3. Pressione `R`, repita o modo `7` e compare as duas inicializações.
4. Altere `K`, compare os resultados e identifique pelo menos um caso de **agrupamento excessivo** ou **insuficiente**.
5. Use os modos `8` e `9` para acompanhar ISODATA, registrando quando ocorrer divisão, fusão ou somente reajuste.
6. Use o modo `0` para comparar os dois algoritmos lado a lado. Opcionalmente, pressione `B` para facilitar a localização das transições entre rótulos.

A cor atribuída a um grupo representa seu **centroide RGB**. Não significa que o programa identificou a classe semântica “céu”, “solo”, “casa” etc. As linhas mostradas com `B` indicam mudanças de **rótulo**, e não necessariamente bordas reais de objetos.

## 6.3. Perguntas para responder depois dos experimentos

Responda com suas próprias palavras e relacione as respostas aos resultados observados:

1. O que são **rótulos** e **centroides**? Qual é a diferença entre seus formatos e significados?
2. Por que conseguimos encontrar o centroide mais próximo usando **distâncias quadradas**, sem calcular raízes?
3. Por que o K-Médias pode atribuir o **mesmo rótulo** a áreas distantes da imagem?
4. Qual é o efeito de aumentar o número de grupos `K`? Por que mais grupos não significa, necessariamente, uma segmentação melhor?
5. Por que o K-Médias pode gerar resultados diferentes ao mudar a inicialização (`R`)?
6. Qual medida o ISODATA didático usa para **dividir** e qual usa para **fundir** grupos?
7. Por que o centroide resultante de uma fusão deve ser uma **média ponderada**, e não a média simples dos dois centroides?
8. Em que situação seria mais apropriado utilizar o **crescimento de regiões** da Seção 3 do que o K-Médias?

## 6.4. Checklist final

Antes de encerrar, confira se todos os itens foram cumpridos:

- [ ] `TODO 04` — `iniciar_centroides` seleciona `K` pixels reais, de modo reproduzível.
- [ ] `TODO 05` — `atribuir_clusters` devolve um índice de grupo para **cada pixel**.
- [ ] `TODO 06` — `atualizar_centroides` calcula as médias RGB e trata grupos vazios.
- [ ] `TODO 07` — `iteracao_kmedias` devolve `(centroides, rotulos)` na ordem esperada.
- [ ] Modos `5`, `6` e `7` exibem resultados coerentes, inclusive ao alterar `K`, `R` e `N`.
- [ ] `TODO 08` — `iteracao_isodata` pode realizar **fusão, divisão ou reajuste**.
- [ ] Os testes de fusão e divisão imprimem os eventos esperados.
- [ ] Modo `9` indica eventos e número de grupos de maneira coerente.
- [ ] Modo `0` mostra três painéis comparáveis.
- [ ] As funções das **Seções 1–3 continuam funcionando**; nenhuma foi removida.

### Problemas frequentes e como diagnosticá-los

| Sintoma | O que verificar |
|---|---|
| A imagem inteira fica com uma cor | `atribuir_clusters` ainda retorna só zeros ou `K` está pequeno para a cena. |
| Os centroides não mudam | `atualizar_centroides` continua com o retorno provisório. |
| O resultado do modo `6` não evolui com `N` | `iteracao_kmedias` não encadeia atribuição e atualização, ou já houve convergência. |
| Erro de dimensões na comparação | `pixels` deve ter formato `(N,3)`; `rotulos` deve ter `N` elementos. |
| Erro na média RGB | Confira `axis=0` e se o conjunto `membros` está vazio. |
| Modo `9` sempre mostra `reajuste` | Confira distâncias entre centroides, desvios dos grupos e limites de divisão/fusão. |
| Tecla `B` revela linhas estranhas | Lembre-se de que são **fronteiras entre classes RGB**, não contornos semânticos. |
| `ModuleNotFoundError` | Instale dependências no Python que está executando o arquivo. |

## Encerramento

**O que você deve ter aprendido:** segmentar não é apenas desenhar regiões com cores diferentes. No K-Médias, cada pixel recebe o rótulo do centroide RGB mais próximo e os centroides são recalculados iterativamente. No ISODATA simplificado, os grupos também podem ser reorganizados por **divisão** e **fusão**. A escolha dos atributos, das sementes e dos parâmetros influencia diretamente a saída.

**Referência da aula:** *19 Segmentação.pdf* (seções de K-Médias e ISODATA) e slides Beamer “Aula 19 — Segmentação”. As fórmulas, implementações e parâmetros aqui empregados correspondem à demonstração didática em NumPy/OpenGL disponibilizada na pasta de exemplos.
