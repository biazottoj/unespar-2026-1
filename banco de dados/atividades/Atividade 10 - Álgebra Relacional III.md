# Atividade — Álgebra Relacional com Dados Vazios

# Conjunto de tabelas

Use as tabelas abaixo para responder todas as questões.

## Tabela `aluno`

| cod_aluno | nome_aluno | cidade | curso | email |
|---|---|---|---|---|
| A1 | Ana | Maringá | Computação | ana@email.com |
| A2 | Bruno | Londrina | Computação | `<N>` |
| A3 | Carla | `<N>` | Sistemas | carla@email.com |
| A4 | Diego | Curitiba | Sistemas | `<N>` |
| A5 | Elisa | Londrina | `<N>` | elisa@email.com |
| A6 | Felipe | Maringá | Computação | `<N>` |
| A7 | Gabriela | `<N>` | Sistemas | gabriela@email.com |

---

## Tabela `disciplina`

| cod_disc | nome_disc | area | carga_horaria | professor |
|---|---|---|---|---|
| D1 | Banco de Dados | Dados | 80 | João |
| D2 | Programação | Desenvolvimento | 80 | Maria |
| D3 | Engenharia de Software | Engenharia | 60 | `<N>` |
| D4 | Redes | Infraestrutura | 60 | Carlos |
| D5 | Inteligência Artificial | Dados | 80 | `<N>` |
| D6 | Computação Gráfica | `<N>` | 60 | Paula |

---

## Tabela `matricula`

| cod_aluno | cod_disc | ano | nota | situacao |
|---|---|---|---|---|
| A1 | D1 | 2026 | 8.5 | Aprovado |
| A1 | D2 | 2026 | 7.0 | Aprovado |
| A2 | D1 | 2026 | `<N>` | Cursando |
| A2 | D3 | 2026 | 6.0 | Aprovado |
| A3 | D4 | 2025 | 7.5 | Aprovado |
| A3 | D6 | 2026 | `<N>` | `<N>` |
| A4 | D2 | 2026 | 5.0 | Reprovado |
| A5 | D5 | 2026 | 9.0 | Aprovado |
| A6 | D1 | 2025 | 7.0 | Aprovado |
| A6 | D5 | 2026 | `<N>` | Cursando |
| A7 | D3 | 2026 | `<N>` | Cursando |

---

# Exercícios

## Parte 1 — Seleção e projeção com dados vazios

**1.** Construa uma expressão em álgebra relacional para obter todos os alunos que não possuem e-mail cadastrado.

**2.** Construa uma expressão em álgebra relacional para obter apenas o nome dos alunos cujo curso não foi cadastrado.

**3.** Construa uma expressão em álgebra relacional para obter o código e o nome das disciplinas que ainda não possuem professor cadastrado.

**4.** Construa uma expressão em álgebra relacional para obter as matrículas que ainda não possuem nota lançada.

**5.** Construa uma expressão em álgebra relacional para obter o código dos alunos que possuem cidade vazia ou e-mail vazio.

---

## Parte 2 — Produto cartesiano combinado com seleção e projeção

**6.** Construa uma expressão em álgebra relacional para obter o nome dos alunos e o nome das disciplinas em que eles estão matriculados. Use produto cartesiano, seleção e projeção.

**7.** Construa uma expressão em álgebra relacional para obter o nome dos alunos, o nome das disciplinas e a situação das matrículas em que a situação está vazia.

**8.** Construa uma expressão em álgebra relacional para obter o nome dos alunos que estão matriculados em disciplinas sem professor cadastrado.

**9.** Construa uma expressão em álgebra relacional para obter o nome dos alunos e o nome das disciplinas em que a nota ainda não foi lançada.

**10.** Construa uma expressão em álgebra relacional para obter o nome dos alunos de Computação matriculados em disciplinas da área de Dados que ainda não possuem nota lançada.

---

## Parte 3 — União, interseção e diferença com dados vazios

**11.** Construa uma expressão em álgebra relacional para obter os nomes dos alunos que possuem cidade vazia ou e-mail vazio. Use união.

**12.** Construa uma expressão em álgebra relacional para obter os nomes dos alunos que possuem e-mail cadastrado e que também possuem cidade cadastrada. Use interseção.

**13.** Construa uma expressão em álgebra relacional para obter os nomes dos alunos que possuem e-mail cadastrado, mas não possuem cidade cadastrada. Use diferença.

**14.** Construa uma expressão em álgebra relacional para obter os códigos dos alunos que estão matriculados em alguma disciplina da área de Dados e também possuem nota vazia. Use interseção.

---

## Parte 4 — Renomeação com dados vazios

**15.** Use renomeação para criar duas versões da tabela `aluno`, chamadas `a1` e `a2`. Em seguida, construa uma expressão em álgebra relacional para obter pares de alunos diferentes que pertencem ao mesmo curso e em que pelo menos um deles possui e-mail vazio.

## Entrega
Utilize o link para a entrega: [https://forms.gle/ubRXn3i7W9Kj2Xvi6](https://forms.gle/ubRXn3i7W9Kj2Xvi6)
