# Atividade 10 — Análise de algoritmos e demonstração de Big O

## Objetivo

Analisar **10 algoritmos**, apresentados em pseudocódigo e contextualizados em situações reais. Em cada um, determinar o tamanho da entrada, simular a execução, encontrar uma função de contagem `C(n)`, justificar o custo total e **demonstrar formalmente** um limite Big O.

## Regra matemática que deve ser usada

Para demonstrar que `C(n)` pertence a `O(g(n))`, encontre valores **fixos** `c > 0` e `n0 >= 1` de modo que:

```text
0 <= C(n) <= c * g(n), para todo n >= n0.
```

- `C(n)` é a quantidade da operação escolhida para a contagem.
- `g(n)` é a função de referência proposta para Big O.
- `c` **não pode variar** com `n`.
- `n0` marca a partir de qual tamanho de entrada a desigualdade é válida.
- Uma tabela com valores pequenos ajuda a conferir, mas **não substitui** a demonstração geral.
- A prova sobre `C(n)` deve ser complementada por uma explicação do custo total: inicializações, condições dos laços, incrementos, chamadas e outras operações também devem ser consideradas.

**Convenções:** operações simples, acesso a posições, atribuições e comparações têm custo constante. `//` significa divisão inteira; `log2(n)` é o logaritmo na base 2; `teto(x)` e `piso(x)` são arredondamentos. Quando houver comportamento variável, analise o pior caso. Se uma função auxiliar tiver custo constante, isso será informado. Considere as entradas válidas descritas em cada exercício.

### Modelo obrigatório de resposta (reproduzir em cada questão)

```text
1. Tamanho da entrada: o que representa n?
2. Operação básica: o que será contado?
3. Simulação: para n = ____, quais operações são executadas?
4. Contagem: C(n) = ... (explicar a dedução).
5. Função de referência: g(n) = ...
6. Prova: mostrar C(n) <= c * g(n) para n >= n0;
          explicitar c e n0.
7. Custo total: justificar a classificação Big O do algoritmo.
8. Conclusão: escrever O(...).
```

---

## Exercício 1 — Identificação de região de um código postal

**Dificuldade: fácil**

Um sistema identifica uma região verificando os três primeiros símbolos de um código de comprimento `n`.

```text
função identificarRegiao(codigo):
    n = tamanho(codigo)
    se n < 3:
        retornar "CODIGO_INVALIDO"

    se codigo[0] == 'S':
        se codigo[1] == 'U':
            se codigo[2] == 'L':
                retornar "REGIAO_SUL"

    retornar "OUTRA_REGIAO"
```
---

## Exercício 2 — Validar medições de temperatura

**Dificuldade: fácil**

Um centro de armazenamento percorre `n` medições e contabiliza quantas ultrapassam o limite permitido.

```text
função contarTemperaturasAltas(temperaturas, limite):
    n = tamanho(temperaturas)
    quantidade = 0

    para i de 0 até n - 1:
        se temperaturas[i] > limite:
            quantidade = quantidade + 1

    retornar quantidade
```

---

## Exercício 3 — Intercalar duas filas ordenadas

**Dificuldade: média**

Uma transportadora possui **duas listas já ordenadas**, cada uma com `n` códigos de encomenda, e deseja produzir uma única lista ordenada. A ordenação inicial **não** deve ser computada.

```text
função intercalar(filaA, filaB):
    n = tamanho(filaA)   // filaB também tem n elementos
    i = 0
    j = 0
    saida = listaVazia()

    enquanto i < n e j < n:
        se filaA[i] <= filaB[j]:
            adicionarNoFim(saida, filaA[i])
            i = i + 1
        senão:
            adicionarNoFim(saida, filaB[j])
            j = j + 1

    enquanto i < n:
        adicionarNoFim(saida, filaA[i])
        i = i + 1

    enquanto j < n:
        adicionarNoFim(saida, filaB[j])
        j = j + 1

    retornar saida
```


---

## Exercício 4 — Expandir a capacidade de um buffer

**Dificuldade: média**

Um serviço aumenta uma reserva de capacidade por duplicação até conseguir acomodar `n` eventos.

```text
função calcularExpansoes(n):
    // n >= 1
    capacidade = 1
    expansoes = 0

    enquanto capacidade < n:
        capacidade = capacidade * 2
        expansoes = expansoes + 1

    retornar expansoes
```

---

## Exercício 5 — Comunicação entre equipes diferentes

**Dificuldade: média**

Em uma rede com `n` equipes, uma mensagem de teste será enviada de cada equipe para **todas as outras**, mas nunca para ela mesma. A ordem emissor–destinatário importa.

```text
procedimento testarComunicacao(equipes):
    n = tamanho(equipes)

    para origem de 0 até n - 1:
        para destino de 0 até n - 1:
            se origem != destino:
                enviarMensagemTeste(equipes[origem], equipes[destino])
```

---

## Exercício 6 — Consultar todas as janelas de tempo

**Dificuldade: média**

Um analista tem `n` dias de registro. Uma tabela de **somas prefixadas já está disponível**, de modo que consultar a soma de qualquer intervalo `[inicio, fim]` leva tempo constante. O algoritmo consulta todos os intervalos contíguos possíveis.

```text
procedimento analisarJanelas(prefixos, n):
    para tamanhoJanela de 1 até n:
        para inicio de 0 até n - tamanhoJanela:
            fim = inicio + tamanhoJanela - 1
            soma = consultarSomaPrefixada(prefixos, inicio, fim)
            registrarResumo(soma)
```


---

## Exercício 7 — Testar escalas de amostragem para todos os sensores

**Dificuldade: difícil**

Um sistema dispõe de `n` sensores. Para cada um, avalia escalas de amostragem com tamanhos `1`, `2`, `4`, `8`, ... enquanto forem **menores que** `n`.

```text
procedimento testarEscalas(sensores):
    n = tamanho(sensores)  // n >= 1

    para i de 0 até n - 1:
        escala = 1
        enquanto escala < n:
            testarEscala(sensores[i], escala)
            escala = escala * 2
```
---

## Exercício 8 — Validar configurações de três etapas

**Dificuldade: difícil**

Uma fábrica combina `n` linhas de produção, diferentes possibilidades de turnos dependentes da linha e `n` opções de inspeção.

```text
procedimento validarConfiguracoes(n):
    // n >= 1
    para linha de 1 até n:
        para turno de 1 até linha:
            para inspecao de 1 até n:
                validarOpcao(linha, turno, inspecao)
```

---

## Exercício 9 — Explorar decisões binárias de planejamento

**Dificuldade: difícil**

Um software de planejamento avalia possibilidades de escolher ou não uma ação em cada uma de `n` etapas. A cada nó da exploração, registra uma visita. **Não** constrói nem imprime listas de tamanho `n` em cada nó.

```text
procedimento explorar(etapa, n):
    registrarVisita()  // custo constante

    se etapa == n:
        retornar

    explorar(etapa + 1, n)  // opcao NAO
    explorar(etapa + 1, n)  // opcao SIM

// chamada inicial: explorar(0, n), com n >= 1
``

---

## Exercício 10 — Auditoria de pares em escalas crescentes

**Dificuldade: difícil**

Uma auditoria testa cada par ordenado de unidades em várias escalas de amostragem, dobrando a escala até atingir `n`.

```text
procedimento auditarPares(unidades):
    n = tamanho(unidades)  // n >= 1

    para i de 0 até n - 1:
        para j de 0 até n - 1:
            escala = 1
            enquanto escala < n:
                registrarTeste(unidades[i], unidades[j], escala)
                escala = escala * 2
```


## Entrega

Entrega via link: [https://forms.gle/ikqZVPm3iVprPBd86](https://forms.gle/ikqZVPm3iVprPBd86)

Entrega até 13/11/2026.
