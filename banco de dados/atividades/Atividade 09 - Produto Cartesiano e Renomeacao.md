# Lista de Exercícios — Álgebra Relacional II

## Produto Cartesiano, Renomeação e Operações da Aula Anterior

Esta lista tem como objetivo praticar os conceitos de **produto cartesiano** e **renomeação**, combinando-os com as operações estudadas anteriormente: **seleção**, **projeção**, **união**, **diferença** e **interseção**.

Todas as questões são discursivas. Em cada exercício, construa a expressão em álgebra relacional correspondente ao enunciado.

---

## Conjunto de tabelas

Use as tabelas abaixo em todos os exercícios.

### Tabela `aluno`

| cod_aluno | nome_aluno | cidade_aluno | curso |
|---|---|---|---|
| A1 | Ana | Maringá | Computação |
| A2 | Bruno | Londrina | Computação |
| A3 | Carla | Maringá | Sistemas |
| A4 | Diego | Curitiba | Sistemas |
| A5 | Elisa | Londrina | Computação |
| A6 | Felipe | Maringá | Sistemas |

### Tabela `disciplina`

| cod_disc | nome_disc | area | carga_horaria |
|---|---|---|---|
| D1 | Banco de Dados | Dados | 80 |
| D2 | Programação | Desenvolvimento | 80 |
| D3 | Engenharia de Software | Engenharia | 60 |
| D4 | Redes | Infraestrutura | 60 |
| D5 | Inteligência Artificial | Dados | 80 |

### Tabela `matricula`

| cod_aluno | cod_disc | ano | nota |
|---|---|---|---|
| A1 | D1 | 2026 | 8.5 |
| A1 | D2 | 2026 | 7.0 |
| A2 | D1 | 2026 | 6.5 |
| A2 | D3 | 2026 | 8.0 |
| A3 | D1 | 2026 | 9.0 |
| A3 | D4 | 2025 | 7.5 |
| A4 | D2 | 2026 | 5.5 |
| A4 | D3 | 2026 | 6.0 |
| A5 | D5 | 2026 | 9.5 |
| A6 | D1 | 2025 | 7.0 |
| A6 | D5 | 2026 | 8.0 |

---

## Exercícios

### Parte 1 — Produto cartesiano e seleção

**1.** Construa uma expressão em álgebra relacional para obter todas as combinações possíveis entre alunos e disciplinas.

**2.** Construa uma expressão em álgebra relacional para obter as combinações entre alunos e matrículas em que o `cod_aluno` da tabela `aluno` seja igual ao `cod_aluno` da tabela `matricula`.

**3.** Construa uma expressão em álgebra relacional para obter o nome dos alunos e os códigos das disciplinas em que eles estão matriculados. Use produto cartesiano, seleção e projeção.

**4.** Construa uma expressão em álgebra relacional para obter o nome dos alunos, o nome das disciplinas e as notas obtidas. Use as tabelas `aluno`, `matricula` e `disciplina`.

**5.** Construa uma expressão em álgebra relacional para obter o nome dos alunos de Maringá e os nomes das disciplinas em que eles estão matriculados no ano de 2026.

---

### Parte 2 — Renomeação

**6.** Considere que seja necessário comparar alunos entre si. Use renomeação para criar duas versões da tabela `aluno`, chamadas `a1` e `a2`, e construa uma expressão que gere todos os pares possíveis de alunos.

**7.** Usando renomeação, construa uma expressão para obter pares de alunos que moram na mesma cidade, mas que não sejam o mesmo aluno.

**8.** Usando renomeação, construa uma expressão para obter pares de alunos que pertencem ao mesmo curso, mas possuem códigos diferentes.

**9.** Use renomeação para comparar duas versões da tabela `matricula` e obter pares de alunos diferentes que cursaram a mesma disciplina no mesmo ano.

**10.** Use renomeação para comparar duas versões da tabela `disciplina` e obter pares de disciplinas da mesma área, mas com códigos diferentes.

---

### Parte 3 — Combinação com seleção, projeção, união, interseção e diferença

**11.** Construa uma expressão para obter os nomes dos alunos que cursaram disciplinas da área de `Dados` em 2026. Use produto cartesiano, seleção e projeção.

**12.** Construa uma expressão para obter os nomes dos alunos que cursaram `Banco de Dados` ou `Inteligência Artificial`. Use produto cartesiano, seleção, projeção e união.

**13.** Construa uma expressão para obter os nomes dos alunos que cursaram disciplinas da área de `Dados` e também cursaram alguma disciplina com carga horária igual a 80. Use interseção.

**14.** Construa uma expressão para obter os nomes dos alunos de `Computação` que não cursaram nenhuma disciplina da área de `Engenharia`. Use diferença.

**15.** Construa uma expressão para obter os nomes dos alunos que cursaram disciplinas da área de `Dados`, mas que não cursaram `Banco de Dados`. Use produto cartesiano, seleção, projeção e diferença.

---

## Observações para resolução

- O produto cartesiano combina linhas de duas tabelas.
- A seleção deve ser usada para filtrar as combinações relevantes.
- A projeção deve ser usada para manter apenas os atributos solicitados.
- A renomeação é útil quando a mesma tabela precisa aparecer mais de uma vez na expressão.
- União, interseção e diferença exigem que as tabelas envolvidas sejam compatíveis, ou seja, tenham o mesmo conjunto de atributos projetados.

## Entrega
Faca a entrega utilizando o link: [https://forms.gle/ok6KeLPynUnwuWPJ8](https://forms.gle/ok6KeLPynUnwuWPJ8)