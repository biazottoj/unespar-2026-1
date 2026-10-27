# Atividade Prática — Aplicação de Filtros Diferentes aos Canais RGB

**Disciplina:** Computação Gráfica  
**Conteúdo:** Convolução 2D e processamento de imagens RGB  
**Tecnologias:** Python, NumPy e OpenGL

## 1. Contexto

Na aula de convolução, implementamos kernels de média, Gaussiano, nitidez e Sobel. Também utilizamos a função `aplicar_convolucao_2d()` para processar imagens e a função `aplicar_kernel_rgb()` para aplicar **o mesmo kernel** separadamente aos canais vermelho (R), verde (G) e azul (B).

Nesta atividade, vamos explorar uma possibilidade diferente: **aplicar um kernel específico a cada canal da mesma imagem** e recombinar os resultados. Dessa maneira, poderemos observar como a alteração independente dos componentes RGB afeta não apenas os detalhes da imagem, mas também suas cores.

**Atenção:** o objetivo **não** é implementar novamente os kernels ou o algoritmo genérico de convolução. Reutilize as funções desenvolvidas no walkthrough da aula.

## 2. Objetivo

Modificar o programa Python/OpenGL da aula para apresentar uma nova versão da imagem do Naruto na qual:

- O **canal vermelho (R)** receba o **filtro Gaussiano 3 × 3**.
- O **canal verde (G)** receba o **filtro de nitidez 3 × 3**.
- O **canal azul (B)** permaneça **inalterado**, como se recebesse o kernel identidade.

A aplicação deverá exibir a **imagem original à esquerda** e a **imagem resultante à direita**, permitindo compará-las.

## 3. Parte 1 — Separação dos canais

Utilize como ponto de partida o arquivo Python desenvolvido e completado durante a aula (`convolucao_naruto_base_aula_alinhado.py`) ou sua versão com os algoritmos já implementados.

A imagem criada por `criar_imagem_exemplo()` possui formato `(64, 64, 3)` e valores de `0.0` a `1.0`. Cada posição da terceira dimensão corresponde a um canal:

| Índice | Canal | Componente da cor |
|---|---|---|
| `0` | R | Vermelho |
| `1` | G | Verde |
| `2` | B | Azul |

**Tarefas:**

1. Localize no código como os canais são acessados (`image[:, :, 0]`, `image[:, :, 1]` e `image[:, :, 2]`).
2. Identifique as funções `kernel_gaussiano()`, `kernel_nitidez()` e `aplicar_convolucao_2d()`.
3. Explique, em um comentário no código, por que `aplicar_kernel_rgb()` **não atende diretamente** ao novo requisito sem alguma adaptação.

## 4. Parte 2 — Processamento independente dos canais

Crie a seguinte função no seu programa:

```python
def filtrar_canais_independentes(image, contorno='refletir'):
    # Aplicar o Gaussiano somente ao canal vermelho.
    # Aplicar a nitidez somente ao canal verde.
    # Manter o canal azul sem alteração.
    # Recombinar os três canais em uma imagem RGB.
    # Limitar o resultado ao intervalo [0.0, 1.0].
    # Retornar a imagem resultante.
    pass
```

**Requisitos da implementação:**

- Reutilizar `aplicar_convolucao_2d()` com os kernels existentes, sem escrever outro algoritmo de convolução.
- Preservar as dimensões `(64, 64, 3)` e a ordem **R, G, B** ao recombinar os canais.
- Respeitar o parâmetro `contorno`, que será controlado pela tecla `B` do programa.
- Preservar o canal azul exatamente como ele aparece na entrada.
- Utilizar `np.clip()` **após** o processamento e a recombinação, para que os valores RGB apresentados ao OpenGL permaneçam entre `0.0` e `1.0`.
- Não modificar a matriz da imagem original durante o processamento.

**Dica:** `np.stack()` permite reunir três matrizes 2D em uma nova matriz RGB. Observe como essa função já é utilizada em `aplicar_kernel_rgb()`.

## 5. Parte 3 — Integração com a visualização OpenGL

O programa já utiliza as funções `gerar_versao()`, `imagens_do_modo()` e `vertices_da_cena()` para preparar os painéis exibidos no OpenGL.

Acrescente um novo modo de visualização, associado à **tecla `0`**, sem remover ou alterar os modos de `1` a `9`.

**Tarefas:**

1. Acrescente uma descrição para o modo `0` no dicionário `MODES`.
2. Inclua `glfw.KEY_0` no mapeamento de teclas da função `teclado()`.
3. Adicione uma condição na função `gerar_versao()` para executar `filtrar_canais_independentes()` quando o modo selecionado for `0`.
4. Verifique se o modo `0` apresenta dois painéis: imagem original à esquerda e resultado à direita. A função `imagens_do_modo()` já utiliza esse formato para os modos que não são `8` ou `9`.
5. Mantenha o funcionamento das demais teclas, especialmente `B` (tratamento das bordas) e `T` (imagem limpa/com ruído).

## 6. Parte 4 — Testes e análise dos resultados

Execute o programa e realize os testes abaixo.

| Teste | Procedimento | O que observar |
|---|---|---|
| 1 | Selecionar `0` com a imagem limpa | Comparar cores e contornos entre os painéis |
| 2 | Selecionar `0` e pressionar `T` | Verificar o comportamento dos filtros na presença de ruído |
| 3 | Alternar `B` entre os tratamentos de borda | Identificar possíveis diferenças nas extremidades da imagem |
| 4 | Comparar o modo `0` com o modo `3` | Distinguir filtros diferentes por canal de um Gaussiano aplicado aos três canais |
| 5 | Comparar o modo `0` com o modo `4` | Distinguir filtros diferentes por canal de uma nitidez aplicada aos três canais |

Além da observação visual, confirme por código que o **canal azul da imagem resultante não foi modificado**. Você pode utilizar `np.allclose()` para comparar o canal azul original e o processado.

### Questões para responder

1. Por que o resultado da atividade apresenta mudanças de cor, além de alterações na nitidez ou suavização da imagem?
2. Qual a diferença entre aplicar Gaussiano aos três canais RGB e aplicá-lo apenas ao canal vermelho?
3. Por que o canal azul deve permanecer igual ao original, mesmo que o aspecto visual da imagem recombinada seja diferente?
4. Na sua avaliação, filtros diferentes por canal são uma boa estratégia para suavizar uma fotografia preservando suas cores originais? Justifique.
5. Que comportamento você observou ao alternar entre o Naruto limpo e a versão com ruído?

## 7. Critérios de verificação

- Os kernels existentes são reutilizados corretamente.
- Cada canal RGB recebe o tratamento solicitado.
- Os canais são recombinados na ordem correta, com valores RGB válidos.
- O modo `0` apresenta os painéis original e processado sem comprometer os modos anteriores.
- As capturas e respostas demonstram compreensão das diferenças entre **filtragem RGB convencional** e **filtragem independente por canal**.

## 8. Desafio opcional

Permita que o usuário escolha, pelo teclado, diferentes combinações de kernels para os canais R, G e B, incluindo a opção **identidade**. Compare os resultados e identifique quais combinações preservam melhor as cores originais e quais produzem efeitos visuais mais intensos.

## 9. Entrega

Entregue:

1. **Arquivo `.py`** com a implementação e o novo modo `0` funcionando.
2. **Duas capturas de tela** do programa: uma usando a imagem limpa e outra usando a imagem com ruído, ambas no novo modo.
3. **Respostas às cinco questões** da seção anterior, em um arquivo `.md`, `.txt` ou `.pdf`.

Entrega via link: [https://forms.gle/hmAo5kBQBSaHLXgb6](https://forms.gle/hmAo5kBQBSaHLXgb6)

Entrega atẽ dia 03/11/2026