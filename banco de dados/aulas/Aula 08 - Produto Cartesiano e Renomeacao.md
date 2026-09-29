# Walkthrough — Produto Cartesiano e Renomeação na Álgebra Relacional

## 1. Objetivo do walkthrough

Este walkthrough tem como objetivo explicar, passo a passo, duas operações importantes da álgebra relacional:

1. **Produto cartesiano** (`×`)
2. **Renomeação** (`ρ`)

A ideia é construir a explicação de forma progressiva, começando com tabelas simples e usando essas mesmas tabelas ao longo dos exemplos. Primeiro, veremos como o produto cartesiano combina linhas de duas tabelas. Depois, veremos como a renomeação ajuda a dar nomes temporários para tabelas e atributos, principalmente quando precisamos evitar ambiguidades ou melhorar a legibilidade das consultas.

---

## 2. Tabelas usadas nos exemplos

Considere o seguinte pequeno banco de dados de uma instituição de ensino.

### Tabela `aluno`

| id_aluno | nome_aluno | curso |
|---|---|---|
| 1 | Ana | Engenharia de Software |
| 2 | Bruno | Ciência da Computação |
| 3 | Carla | Engenharia de Software |

### Tabela `disciplina`

| id_disciplina | nome_disciplina | area |
|---|---|---|
| BD | Banco de Dados | Dados |
| ES | Engenharia de Software | Software |

### Tabela `matricula`

| id_aluno | id_disciplina | semestre |
|---|---|---|
| 1 | BD | 2026-1 |
| 1 | ES | 2026-1 |
| 2 | BD | 2026-1 |
| 3 | ES | 2026-1 |

Essas três tabelas representam:

- `aluno`: os estudantes cadastrados.
- `disciplina`: as disciplinas disponíveis.
- `matricula`: quais alunos estão matriculados em quais disciplinas.

---

# Parte 1 — Produto Cartesiano

## 3. O que é produto cartesiano?

O **produto cartesiano** é uma operação que combina cada linha de uma tabela com cada linha de outra tabela.

Em álgebra relacional, a operação é representada pelo símbolo:

```text
×
```

A forma geral é:

```text
TabelaA × TabelaB
```

O resultado também é uma tabela.

Se uma tabela possui `m` linhas e a outra possui `n` linhas, o produto cartesiano terá:

```text
m × n linhas
```

Por exemplo:

- `aluno` possui 3 linhas.
- `disciplina` possui 2 linhas.

Logo:

```text
aluno × disciplina
```

terá:

```text
3 × 2 = 6 linhas
```

---

## 4. Produto cartesiano entre `aluno` e `disciplina`

### Consulta textual completa

Obter todas as combinações possíveis entre alunos e disciplinas.

```text
aluno × disciplina
```

### Quebrando a expressão

A expressão possui três partes principais:

```text
aluno
```

Representa a primeira tabela usada na operação.

```text
×
```

Representa a operação de produto cartesiano.

```text
disciplina
```

Representa a segunda tabela usada na operação.

### Como interpretar

A consulta diz:

> Combine cada linha da tabela `aluno` com cada linha da tabela `disciplina`.

Isso significa que:

- Ana será combinada com Banco de Dados.
- Ana será combinada com Engenharia de Software.
- Bruno será combinado com Banco de Dados.
- Bruno será combinado com Engenharia de Software.
- Carla será combinada com Banco de Dados.
- Carla será combinada com Engenharia de Software.

### Resultado

| aluno.id_aluno | nome_aluno | curso | disciplina.id_disciplina | nome_disciplina | area |
|---|---|---|---|---|---|
| 1 | Ana | Engenharia de Software | BD | Banco de Dados | Dados |
| 1 | Ana | Engenharia de Software | ES | Engenharia de Software | Software |
| 2 | Bruno | Ciência da Computação | BD | Banco de Dados | Dados |
| 2 | Bruno | Ciência da Computação | ES | Engenharia de Software | Software |
| 3 | Carla | Engenharia de Software | BD | Banco de Dados | Dados |
| 3 | Carla | Engenharia de Software | ES | Engenharia de Software | Software |

### Observação importante

O produto cartesiano **não verifica se existe relação real entre os dados**. Ele apenas combina tudo com tudo.

Por isso, o resultado pode conter combinações que não fazem sentido no contexto do banco de dados.

Por exemplo, o produto cartesiano mostra que Carla está combinada com Banco de Dados, mas isso não significa que Carla está matriculada em Banco de Dados. Para saber as matrículas reais, precisamos usar a tabela `matricula` e aplicar uma condição de seleção.

---

## 5. Produto cartesiano com seleção

O produto cartesiano costuma ser usado junto com a **seleção** para manter apenas as combinações que fazem sentido.

### Consulta textual completa

Obter as combinações entre alunos e matrículas em que o código do aluno seja igual nas duas tabelas.

```text
σ aluno.id_aluno = matricula.id_aluno (aluno × matricula)
```

### Quebrando a expressão

Começamos pela parte mais interna:

```text
aluno × matricula
```

Essa parte gera todas as combinações possíveis entre alunos e matrículas.

Depois aplicamos a seleção:

```text
σ aluno.id_aluno = matricula.id_aluno
```

Essa condição mantém apenas as linhas em que o `id_aluno` da tabela `aluno` é igual ao `id_aluno` da tabela `matricula`.

### Como interpretar

A consulta diz:

> Primeiro, combine todos os alunos com todas as matrículas. Depois, mantenha apenas as combinações em que o aluno da tabela `aluno` corresponde ao aluno registrado na tabela `matricula`.

### Resultado

| aluno.id_aluno | nome_aluno | curso | matricula.id_aluno | id_disciplina | semestre |
|---|---|---|---|---|---|
| 1 | Ana | Engenharia de Software | 1 | BD | 2026-1 |
| 1 | Ana | Engenharia de Software | 1 | ES | 2026-1 |
| 2 | Bruno | Ciência da Computação | 2 | BD | 2026-1 |
| 3 | Carla | Engenharia de Software | 3 | ES | 2026-1 |

### Conclusão do exemplo

A seleção eliminou as combinações inválidas e manteve apenas as combinações em que o aluno realmente aparece na matrícula.

Esse padrão é muito importante porque mostra a base conceitual de uma junção:

```text
produto cartesiano + seleção
```

---

## 6. Produto cartesiano com seleção e projeção

Agora vamos combinar três operações:

1. Produto cartesiano
2. Seleção
3. Projeção

### Consulta textual completa

Obter o nome dos alunos e o código das disciplinas em que eles estão matriculados.

```text
π nome_aluno, id_disciplina (
    σ aluno.id_aluno = matricula.id_aluno (aluno × matricula)
)
```

### Quebrando a expressão

A primeira operação executada é:

```text
aluno × matricula
```

Ela combina todos os alunos com todas as matrículas.

Depois aplicamos:

```text
σ aluno.id_aluno = matricula.id_aluno
```

Essa seleção mantém somente as combinações corretas entre aluno e matrícula.

Por fim, aplicamos:

```text
π nome_aluno, id_disciplina
```

Essa projeção mostra apenas as colunas `nome_aluno` e `id_disciplina`.

### Como interpretar

A consulta diz:

> Encontre as matrículas correspondentes a cada aluno e mostre apenas o nome do aluno e o código da disciplina.

### Resultado

| nome_aluno | id_disciplina |
|---|---|
| Ana | BD |
| Ana | ES |
| Bruno | BD |
| Carla | ES |

### Observação didática

Essa consulta mostra por que as operações da álgebra relacional podem ser combinadas. Cada operação recebe uma tabela e produz outra tabela. Assim, o resultado de uma operação pode ser usado como entrada para outra.

---

## 7. Produto cartesiano envolvendo três tabelas

Agora queremos obter o nome do aluno e o nome da disciplina em que ele está matriculado.

Para isso, precisamos combinar:

- `aluno`
- `matricula`
- `disciplina`

### Consulta textual completa

```text
π nome_aluno, nome_disciplina (
    σ aluno.id_aluno = matricula.id_aluno AND
      matricula.id_disciplina = disciplina.id_disciplina
      (aluno × matricula × disciplina)
)
```

### Quebrando a expressão

A parte mais interna é:

```text
aluno × matricula × disciplina
```

Essa parte gera todas as combinações possíveis entre as três tabelas.

Depois aplicamos a condição:

```text
σ aluno.id_aluno = matricula.id_aluno AND
  matricula.id_disciplina = disciplina.id_disciplina
```

Essa condição mantém apenas as linhas em que:

- o aluno combinado é o mesmo aluno da matrícula;
- a disciplina combinada é a mesma disciplina da matrícula.

Por fim, usamos a projeção:

```text
π nome_aluno, nome_disciplina
```

Essa projeção mantém apenas as colunas que interessam para a resposta final.

### Resultado

| nome_aluno | nome_disciplina |
|---|---|
| Ana | Banco de Dados |
| Ana | Engenharia de Software |
| Bruno | Banco de Dados |
| Carla | Engenharia de Software |

### Interpretação

A consulta responde:

> Quais alunos estão matriculados em quais disciplinas?

---

## 8. Cuidado com atributos de mesmo nome

Quando usamos produto cartesiano entre tabelas que possuem atributos com o mesmo nome, pode surgir ambiguidade.

No nosso exemplo, `aluno` e `matricula` possuem o atributo:

```text
id_aluno
```

Por isso, usamos nomes qualificados:

```text
aluno.id_aluno
matricula.id_aluno
```

Isso evita confusão e deixa claro de qual tabela vem cada atributo.

---

# Parte 2 — Renomeação

## 9. O que é renomeação?

A **renomeação** é uma operação usada para atribuir um novo nome temporário a uma tabela ou aos seus atributos.

Em álgebra relacional, a renomeação costuma ser representada pela letra grega rho:

```text
ρ
```

A renomeação é útil para:

1. Melhorar a legibilidade de uma consulta.
2. Evitar nomes ambíguos.
3. Permitir usar a mesma tabela mais de uma vez na mesma expressão.
4. Ajustar nomes de atributos antes de operações como união, interseção e diferença.

---

## 10. Renomeando uma tabela

### Consulta textual completa

Renomear temporariamente a tabela `aluno` para `A`.

```text
ρ A (aluno)
```

### Quebrando a expressão

```text
ρ
```

Representa a operação de renomeação.

```text
A
```

É o novo nome temporário da tabela.

```text
(aluno)
```

É a tabela original que está sendo renomeada.

### Como interpretar

A consulta diz:

> Use a tabela `aluno`, mas chame essa tabela temporariamente de `A` nesta expressão.

### Resultado conceitual

A tabela continua com os mesmos dados, mas passa a ser referenciada como `A`.

| A.id_aluno | nome_aluno | curso |
|---|---|---|
| 1 | Ana | Engenharia de Software |
| 2 | Bruno | Ciência da Computação |
| 3 | Carla | Engenharia de Software |

### Observação importante

A renomeação **não altera o banco de dados original**. Ela apenas muda o nome usado dentro da expressão de álgebra relacional.

---

## 11. Renomeando tabela para simplificar uma consulta

Sem renomeação, poderíamos escrever:

```text
σ aluno.id_aluno = matricula.id_aluno (aluno × matricula)
```

Com renomeação, podemos escrever:

```text
σ A.id_aluno = M.id_aluno (ρ A(aluno) × ρ M(matricula))
```

### Quebrando a expressão

Primeiro:

```text
ρ A(aluno)
```

Renomeia `aluno` para `A`.

Depois:

```text
ρ M(matricula)
```

Renomeia `matricula` para `M`.

Em seguida:

```text
ρ A(aluno) × ρ M(matricula)
```

Faz o produto cartesiano entre as tabelas renomeadas.

Por fim:

```text
σ A.id_aluno = M.id_aluno
```

Mantém apenas as linhas em que o aluno de `A` corresponde ao aluno da matrícula em `M`.

### Resultado

| A.id_aluno | nome_aluno | curso | M.id_aluno | id_disciplina | semestre |
|---|---|---|---|---|---|
| 1 | Ana | Engenharia de Software | 1 | BD | 2026-1 |
| 1 | Ana | Engenharia de Software | 1 | ES | 2026-1 |
| 2 | Bruno | Ciência da Computação | 2 | BD | 2026-1 |
| 3 | Carla | Engenharia de Software | 3 | ES | 2026-1 |

### Interpretação

A consulta tem o mesmo resultado da versão sem renomeação, mas fica mais curta e mais legível em consultas maiores.

---

## 12. Renomeando atributos

Além de renomear tabelas, também podemos renomear os atributos de uma relação.

Uma forma comum de escrever é:

```text
ρ NovoNome(novo_atributo1, novo_atributo2, ...)(TabelaOriginal)
```

### Consulta textual completa

Renomear a tabela `disciplina` para `D` e seus atributos para `codigo`, `nome` e `categoria`.

```text
ρ D(codigo, nome, categoria)(disciplina)
```

### Quebrando a expressão

```text
ρ
```

Representa a operação de renomeação.

```text
D
```

É o novo nome da tabela.

```text
(codigo, nome, categoria)
```

São os novos nomes dos atributos.

```text
(disciplina)
```

É a tabela original.

### Resultado conceitual

| codigo | nome | categoria |
|---|---|---|
| BD | Banco de Dados | Dados |
| ES | Engenharia de Software | Software |

### Interpretação

A tabela `disciplina` foi temporariamente chamada de `D`, e suas colunas foram temporariamente chamadas de:

- `codigo`
- `nome`
- `categoria`

---

## 13. Por que renomear atributos?

Renomear atributos é útil quando queremos:

1. Padronizar nomes antes de aplicar operações de conjunto.
2. Evitar conflito entre colunas com o mesmo nome.
3. Tornar o resultado mais compreensível.

Por exemplo, se duas tabelas possuem atributos equivalentes, mas com nomes diferentes, a renomeação pode deixar as estruturas compatíveis para uma operação como união, interseção ou diferença.

---

## 14. Renomeação para usar a mesma tabela duas vezes

A renomeação é essencial quando precisamos comparar linhas de uma tabela com outras linhas da mesma tabela.

Considere agora a tabela `aluno` novamente.

### Tabela `aluno`

| id_aluno | nome_aluno | curso |
|---|---|---|
| 1 | Ana | Engenharia de Software |
| 2 | Bruno | Ciência da Computação |
| 3 | Carla | Engenharia de Software |

Queremos encontrar pares de alunos que pertencem ao mesmo curso.

Para isso, precisamos usar a tabela `aluno` duas vezes:

- uma cópia representando o primeiro aluno do par;
- outra cópia representando o segundo aluno do par.

Se usarmos apenas `aluno × aluno`, os nomes dos atributos ficam ambíguos. Por isso, usamos renomeação.

### Consulta textual completa

```text
σ A.curso = B.curso AND A.id_aluno < B.id_aluno (
    ρ A(aluno) × ρ B(aluno)
)
```

### Quebrando a expressão

Primeiro, criamos duas versões temporárias da mesma tabela:

```text
ρ A(aluno)
```

Essa versão representa o primeiro aluno do par.

```text
ρ B(aluno)
```

Essa versão representa o segundo aluno do par.

Depois fazemos o produto cartesiano:

```text
ρ A(aluno) × ρ B(aluno)
```

Esse produto combina todos os alunos com todos os alunos.

Em seguida, aplicamos a seleção:

```text
σ A.curso = B.curso AND A.id_aluno < B.id_aluno
```

Essa condição mantém apenas os pares em que:

- os dois alunos são do mesmo curso;
- o `id_aluno` de `A` é menor que o `id_aluno` de `B`.

A condição `A.id_aluno < B.id_aluno` evita pares repetidos, como:

```text
(Ana, Carla)
(Carla, Ana)
```

Também evita que um aluno seja combinado com ele mesmo.

### Resultado

| A.id_aluno | A.nome_aluno | A.curso | B.id_aluno | B.nome_aluno | B.curso |
|---|---|---|---|---|---|
| 1 | Ana | Engenharia de Software | 3 | Carla | Engenharia de Software |

### Interpretação

A consulta encontrou que Ana e Carla pertencem ao mesmo curso.

---

## 15. Renomeação combinada com projeção

Agora vamos mostrar apenas os nomes dos alunos que pertencem ao mesmo curso.

### Consulta textual completa

```text
π A.nome_aluno, B.nome_aluno (
    σ A.curso = B.curso AND A.id_aluno < B.id_aluno (
        ρ A(aluno) × ρ B(aluno)
    )
)
```

### Quebrando a expressão

A parte mais interna é:

```text
ρ A(aluno) × ρ B(aluno)
```

Ela cria duas versões da tabela `aluno` e combina todos os alunos entre si.

Depois aplicamos:

```text
σ A.curso = B.curso AND A.id_aluno < B.id_aluno
```

Essa seleção mantém apenas os pares de alunos do mesmo curso, sem duplicidade.

Por fim, aplicamos:

```text
π A.nome_aluno, B.nome_aluno
```

Essa projeção mantém apenas os nomes dos alunos.

### Resultado

| A.nome_aluno | B.nome_aluno |
|---|---|
| Ana | Carla |

### Interpretação

A consulta mostra os pares de alunos que cursam o mesmo curso.

---

# Parte 3 — Comparação entre produto cartesiano e renomeação

## 16. Produto cartesiano e renomeação têm papéis diferentes

O produto cartesiano e a renomeação podem aparecer juntos, mas eles têm funções diferentes.

| Operação | Símbolo | Função principal |
|---|---|---|
| Produto cartesiano | `×` | Combinar todas as linhas de uma tabela com todas as linhas de outra tabela |
| Renomeação | `ρ` | Dar nomes temporários a tabelas ou atributos |

O produto cartesiano altera a quantidade de linhas, pois cria combinações.

A renomeação não muda os dados. Ela apenas muda nomes usados na expressão.

---

## 17. Exemplo completo combinando produto cartesiano, renomeação, seleção e projeção

### Problema

Obter o nome dos alunos e o nome das disciplinas em que eles estão matriculados.

### Consulta textual completa

```text
π A.nome_aluno, D.nome_disciplina (
    σ A.id_aluno = M.id_aluno AND
      M.id_disciplina = D.id_disciplina (
        ρ A(aluno) × ρ M(matricula) × ρ D(disciplina)
    )
)
```

### Quebrando a expressão

Primeiro, renomeamos as tabelas:

```text
ρ A(aluno)
```

A tabela `aluno` passa a ser chamada temporariamente de `A`.

```text
ρ M(matricula)
```

A tabela `matricula` passa a ser chamada temporariamente de `M`.

```text
ρ D(disciplina)
```

A tabela `disciplina` passa a ser chamada temporariamente de `D`.

Depois fazemos o produto cartesiano:

```text
ρ A(aluno) × ρ M(matricula) × ρ D(disciplina)
```

Essa operação combina todas as linhas das três tabelas.

Em seguida, aplicamos a seleção:

```text
σ A.id_aluno = M.id_aluno AND
  M.id_disciplina = D.id_disciplina
```

Essa seleção mantém apenas as combinações em que:

- o aluno corresponde à matrícula;
- a matrícula corresponde à disciplina.

Por fim, aplicamos a projeção:

```text
π A.nome_aluno, D.nome_disciplina
```

Essa projeção mostra apenas o nome do aluno e o nome da disciplina.

### Resultado

| nome_aluno | nome_disciplina |
|---|---|
| Ana | Banco de Dados |
| Ana | Engenharia de Software |
| Bruno | Banco de Dados |
| Carla | Engenharia de Software |

### Interpretação

Essa consulta é uma versão mais organizada da consulta com três tabelas. A renomeação tornou a expressão mais legível, principalmente nas condições da seleção.

---

# Parte 4 — Exercícios de fixação

## Exercício 1

Considere as tabelas `aluno` e `disciplina` apresentadas no início do walkthrough.

Construa uma expressão em álgebra relacional para obter todas as combinações possíveis entre alunos e disciplinas.

---

## Exercício 2

Construa uma expressão em álgebra relacional para obter todas as combinações entre alunos e matrículas em que o aluno da tabela `aluno` corresponda ao aluno da tabela `matricula`.

---

## Exercício 3

Construa uma expressão em álgebra relacional para obter apenas o nome dos alunos e o código das disciplinas em que eles estão matriculados.

---

## Exercício 4

Construa uma expressão em álgebra relacional para obter o nome dos alunos e o nome das disciplinas em que eles estão matriculados.

---

## Exercício 5

Use renomeação para construir uma expressão que compare a tabela `aluno` com ela mesma e encontre pares de alunos do mesmo curso.

---

## Exercício 6

Reescreva a expressão abaixo usando renomeação para simplificar os nomes das tabelas:

```text
π aluno.nome_aluno, disciplina.nome_disciplina (
    σ aluno.id_aluno = matricula.id_aluno AND
      matricula.id_disciplina = disciplina.id_disciplina
      (aluno × matricula × disciplina)
)
```

---

# Parte 5 — Resumo final

## Produto cartesiano

O produto cartesiano combina todas as linhas de uma tabela com todas as linhas de outra tabela.

Forma geral:

```text
TabelaA × TabelaB
```

Se `TabelaA` tem `m` linhas e `TabelaB` tem `n` linhas, o resultado terá `m × n` linhas.

## Renomeação

A renomeação atribui nomes temporários a tabelas ou atributos.

Forma geral para renomear uma tabela:

```text
ρ NovoNome(TabelaOriginal)
```

Forma geral para renomear tabela e atributos:

```text
ρ NovoNome(novo_atributo1, novo_atributo2, ...)(TabelaOriginal)
```

## Ideia central

O produto cartesiano cria combinações. A renomeação organiza a consulta e evita ambiguidade.

Em consultas mais completas, é comum combinar:

```text
renomeação + produto cartesiano + seleção + projeção
```

