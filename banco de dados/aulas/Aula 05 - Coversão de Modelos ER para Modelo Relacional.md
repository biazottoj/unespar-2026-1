# Aula 05 - Conversão de modelo ER para modelo relacional

## 1. Objetivo da conversão

A conversão de modelos consiste em transformar um **modelo conceitual**, geralmente representado por um **DER — Diagrama Entidade-Relacionamento**, em um **modelo lógico relacional**, representado por um conjunto de **tabelas**, **atributos**, **chaves primárias** e **chaves estrangeiras**.

Em termos simples:

> O DER mostra os conceitos principais do problema.  
> O modelo relacional mostra como esses conceitos serão organizados em tabelas.

Por exemplo, em um sistema acadêmico, o DER pode representar que existem alunos, cursos, disciplinas, turmas, professores e matrículas. Já o modelo relacional define quais tabelas serão criadas para armazenar esses dados em um banco relacional.

---

## 2. Exemplo-base: sistema de gestão de alunos

Considere um sistema de gestão acadêmica com as seguintes regras de negócio:

- Um aluno pertence a um curso.
- Um curso possui vários alunos.
- Um curso possui várias disciplinas.
- Uma disciplina pertence a um curso.
- Uma disciplina pode ser ofertada em várias turmas.
- Uma turma corresponde à oferta de uma disciplina em um período letivo.
- Um professor pode ministrar várias turmas.
- Cada turma é ministrada por um professor.
- Um aluno pode se matricular em várias turmas.
- Uma turma pode ter vários alunos matriculados.
- Cada aluno pode possuir um perfil acadêmico complementar.
- Cada perfil acadêmico pertence a apenas um aluno.
- Um aluno pode ter mais de um telefone.
- O endereço de um aluno pode ser dividido em rua, número, cidade, estado e CEP.
- A idade do aluno pode ser calculada a partir da data de nascimento.

---

## 3. Visão geral das entidades do exemplo

A partir das regras de negócio, podemos identificar as seguintes entidades principais:

- `ALUNO`
- `CURSO`
- `DISCIPLINA`
- `TURMA`
- `PROFESSOR`
- `PERFIL_ACADEMICO`

Além disso, precisaremos criar algumas tabelas auxiliares durante a conversão, como:

- `MATRICULA`, para representar o relacionamento N:N entre aluno e turma;
- `ALUNO_TELEFONE`, para representar o atributo multivalorado telefone.

---

# Etapa 1 — Converter entidades em tabelas

Toda entidade forte do DER normalmente vira uma tabela.

## No DER

Entidades:

- Aluno
- Curso
- Disciplina
- Turma
- Professor
- Perfil Acadêmico

## No modelo relacional inicial

```text
ALUNO (
    id_aluno PK,
    nome,
    email,
    data_nascimento
)

CURSO (
    id_curso PK,
    nome,
    carga_horaria_total
)

DISCIPLINA (
    id_disciplina PK,
    nome,
    carga_horaria
)

TURMA (
    id_turma PK,
    ano,
    semestre,
    turno
)

PROFESSOR (
    id_professor PK,
    nome,
    email,
    titulacao
)

PERFIL_ACADEMICO (
    id_perfil PK,
    data_ingresso,
    situacao,
    coeficiente_rendimento
)
```

Cada entidade virou uma tabela, e cada identificador da entidade virou uma **chave primária**.

---

# Etapa 2 — Converter relacionamentos 1:N

Em um relacionamento **1:N**, a chave primária da entidade do lado **1** é colocada como **chave estrangeira** na tabela do lado **N**.

---

## 2.1 Exemplo: curso e aluno

Regra de negócio:

> Um curso possui vários alunos, mas cada aluno pertence a um único curso.

Representação conceitual:

```text
CURSO 1 ---- N ALUNO
```

Como `ALUNO` está no lado N, a chave estrangeira fica em `ALUNO`.

```text
ALUNO (
    id_aluno PK,
    nome,
    email,
    data_nascimento,
    id_curso FK
)
```

Isso significa que cada aluno armazena uma referência para o curso ao qual pertence.

---

## 2.2 Exemplo: curso e disciplina

Regra de negócio:

> Um curso possui várias disciplinas, mas cada disciplina pertence a um único curso.

Representação conceitual:

```text
CURSO 1 ---- N DISCIPLINA
```

Como `DISCIPLINA` está no lado N, a chave estrangeira fica em `DISCIPLINA`.

```text
DISCIPLINA (
    id_disciplina PK,
    nome,
    carga_horaria,
    id_curso FK
)
```

---

## 2.3 Exemplo: disciplina e turma

Regra de negócio:

> Uma disciplina pode ser ofertada em várias turmas, mas cada turma corresponde a uma única disciplina.

Representação conceitual:

```text
DISCIPLINA 1 ---- N TURMA
```

Como `TURMA` está no lado N, a chave estrangeira fica em `TURMA`.

```text
TURMA (
    id_turma PK,
    ano,
    semestre,
    turno,
    id_disciplina FK
)
```

---

## 2.4 Exemplo: professor e turma

Regra de negócio:

> Um professor pode ministrar várias turmas, mas cada turma é ministrada por um professor.

Representação conceitual:

```text
PROFESSOR 1 ---- N TURMA
```

Como `TURMA` está no lado N, a chave estrangeira fica em `TURMA`.

```text
TURMA (
    id_turma PK,
    ano,
    semestre,
    turno,
    id_disciplina FK,
    id_professor FK
)
```

Agora a tabela `TURMA` guarda tanto a disciplina ofertada quanto o professor responsável.

---

# Etapa 3 — Converter relacionamentos 1:1

Em um relacionamento **1:1**, uma ocorrência de uma entidade pode estar associada a, no máximo, uma ocorrência da outra entidade.

A conversão de relacionamentos **1:1** exige uma decisão importante:

> Em qual tabela ficará a chave estrangeira?

Diferentemente dos relacionamentos **1:N**, nos quais a chave estrangeira normalmente vai para o lado **N**, em relacionamentos **1:1** não existe um lado “muitos”. Por isso, a escolha depende principalmente da participação das entidades e do significado do relacionamento.

---

## 3.1 Exemplo: aluno e perfil acadêmico

Regra de negócio:

> Cada aluno pode possuir um perfil acadêmico complementar, e cada perfil acadêmico pertence a apenas um aluno.

Representação conceitual:

```text
ALUNO 1 ---- 1 PERFIL_ACADEMICO
```

Nesse caso, podemos representar a relação colocando a chave de `ALUNO` dentro de `PERFIL_ACADEMICO`.

```text
PERFIL_ACADEMICO (
    id_perfil PK,
    data_ingresso,
    situacao,
    coeficiente_rendimento,
    id_aluno FK UNIQUE
)
```

O atributo `id_aluno` é chave estrangeira porque referencia a tabela `ALUNO`.

Além disso, ele deve ter uma restrição `UNIQUE`, pois cada perfil pertence a um aluno, e cada aluno deve ter, no máximo, um perfil acadêmico associado.

---

## 3.2 Por que usar UNIQUE em relacionamento 1:1?

Apenas declarar `id_aluno` como chave estrangeira não garante, sozinho, que o relacionamento será 1:1.

Observe:

```text
PERFIL_ACADEMICO (
    id_perfil PK,
    data_ingresso,
    situacao,
    id_aluno FK
)
```

Sem a restrição `UNIQUE`, o banco poderia permitir várias linhas com o mesmo `id_aluno`, como:

```text
id_perfil | situacao | id_aluno
--------- | -------- | --------
1         | Ativo    | 10
2         | Ativo    | 10
3         | Trancado | 10
```

Isso significaria que o mesmo aluno possui vários perfis acadêmicos, o que violaria a regra de relacionamento 1:1.

Por isso, em uma relação 1:1 representada por chave estrangeira, normalmente usamos:

```text
id_aluno FK UNIQUE
```

---

## 3.3 Quando colocar a chave estrangeira em uma tabela ou na outra?

Em relacionamentos 1:1, uma regra prática é:

> Coloque a chave estrangeira na tabela cuja ocorrência depende mais da outra.

No exemplo:

- Um aluno pode existir sem perfil acadêmico complementar, dependendo do sistema.
- Um perfil acadêmico não faz sentido sem estar associado a um aluno.

Então, faz sentido colocar `id_aluno` dentro de `PERFIL_ACADEMICO`.

```text
ALUNO (
    id_aluno PK,
    nome,
    email,
    data_nascimento,
    id_curso FK
)

PERFIL_ACADEMICO (
    id_perfil PK,
    data_ingresso,
    situacao,
    coeficiente_rendimento,
    id_aluno FK UNIQUE
)
```

---

## 3.4 Alternativa: usar a mesma chave primária

Em alguns casos, a tabela dependente pode usar a chave da tabela principal como sua própria chave primária.

Exemplo:

```text
PERFIL_ACADEMICO (
    id_aluno PK/FK,
    data_ingresso,
    situacao,
    coeficiente_rendimento
)
```

Nesse caso, `id_aluno` é, ao mesmo tempo:

- chave primária de `PERFIL_ACADEMICO`;
- chave estrangeira para `ALUNO`.

Essa solução garante que cada aluno tenha, no máximo, um perfil acadêmico associado.

Ela é comum quando a entidade dependente existe apenas como uma extensão da entidade principal.

---

## 3.5 Alternativa: juntar as duas entidades em uma única tabela

Em alguns casos, se duas entidades possuem sempre uma correspondência obrigatória e são muito dependentes uma da outra, pode fazer sentido transformar tudo em uma única tabela.

Por exemplo, se todo aluno obrigatoriamente tivesse dados de perfil acadêmico desde o cadastro, poderíamos considerar:

```text
ALUNO (
    id_aluno PK,
    nome,
    email,
    data_nascimento,
    id_curso FK,
    data_ingresso,
    situacao,
    coeficiente_rendimento
)
```

No entanto, essa decisão deve ser tomada com cuidado.

Essa solução pode ser inadequada quando:

- nem todo aluno possui perfil acadêmico registrado;
- o perfil possui muitos atributos próprios;
- o perfil pode ter regras próprias de atualização;
- o perfil representa um conceito importante do domínio;
- deseja-se separar dados pessoais de dados acadêmicos.

---

## 3.6 Resumo da conversão de relacionamentos 1:1

| Situação | Possível solução |
|---|---|
| Uma entidade depende mais da outra | Colocar a FK na tabela dependente |
| É necessário garantir 1:1 com FK | Usar FK com restrição UNIQUE |
| A entidade dependente existe apenas junto da principal | Usar a mesma chave como PK/FK |
| As duas entidades são sempre obrigatórias e muito próximas | Avaliar a fusão em uma única tabela |
| O relacionamento possui atributos próprios | Colocar os atributos na tabela que recebeu a FK ou avaliar uma tabela própria |

---

# Etapa 4 — Converter relacionamentos N:N

Relacionamentos **N:N** não podem ser representados apenas colocando uma chave estrangeira em uma das tabelas.

Nesses casos, cria-se uma **nova tabela associativa**.

---

## 4.1 Exemplo: aluno e turma

Regra de negócio:

> Um aluno pode se matricular em várias turmas, e uma turma pode ter vários alunos matriculados.

Representação conceitual:

```text
ALUNO N ---- N TURMA
```

Esse relacionamento vira uma nova tabela:

```text
MATRICULA (
    id_aluno FK,
    id_turma FK,
    data_matricula,
    nota_final,
    frequencia,
    situacao,
    PK (id_aluno, id_turma)
)
```

Essa tabela representa a associação entre alunos e turmas.

Além das chaves estrangeiras, ela também pode armazenar atributos do relacionamento, como:

- `data_matricula`: data em que o aluno se matriculou na turma;
- `nota_final`: nota final do aluno naquela turma;
- `frequencia`: frequência do aluno naquela turma;
- `situacao`: situação do aluno na turma, como aprovado, reprovado ou cursando.

Esses atributos pertencem ao relacionamento, porque não fazem sentido apenas para `ALUNO` nem apenas para `TURMA`. Eles dependem da associação entre um aluno específico e uma turma específica.

---

## 4.2 Por que nota final fica em MATRICULA?

A `nota_final` não deve ficar diretamente em `ALUNO`, porque um aluno pode cursar várias turmas e ter uma nota diferente em cada uma.

Também não deve ficar diretamente em `TURMA`, porque uma turma possui vários alunos, cada um com sua própria nota.

Portanto, a nota pertence ao relacionamento entre aluno e turma:

```text
ALUNO + TURMA = MATRICULA
```

Por isso, `nota_final` fica na tabela `MATRICULA`.

---

# Etapa 5 — Converter atributos multivalorados

Um atributo multivalorado é aquele que pode ter vários valores para uma mesma entidade.

---

## 5.1 Exemplo: telefones do aluno

Um aluno pode ter vários telefones.

No DER, isso poderia aparecer como:

```text
ALUNO
- id_aluno
- nome
- email
- telefones
```

No modelo relacional, não é adequado guardar vários telefones em uma única coluna, como:

```text
telefones = "99999-1111, 98888-2222"
```

Essa solução dificulta consultas, filtros, validações e atualizações.

A solução é criar uma nova tabela:

```text
ALUNO_TELEFONE (
    id_aluno FK,
    telefone,
    tipo,
    PK (id_aluno, telefone)
)
```

Assim, cada telefone fica em uma linha separada.

Exemplo:

```text
id_aluno | telefone    | tipo
-------- | ----------- | --------
1        | 99999-1111  | Celular
1        | 3333-2222   | Residencial
2        | 98888-1234  | Celular
```

---

# Etapa 6 — Converter atributos compostos

Um atributo composto é aquele que pode ser dividido em partes menores.

---

## 6.1 Exemplo: endereço do aluno

O endereço de um aluno pode ser composto por:

- rua;
- número;
- bairro;
- cidade;
- estado;
- CEP.

Em vez de criar uma única coluna chamada `endereco`, pode-se criar colunas separadas:

```text
ALUNO (
    id_aluno PK,
    nome,
    email,
    data_nascimento,
    rua,
    numero,
    bairro,
    cidade,
    estado,
    cep,
    id_curso FK
)
```

Essa solução facilita consultas como:

- listar todos os alunos de uma cidade;
- filtrar alunos por estado;
- agrupar alunos por bairro;
- validar CEP separadamente.

A decisão depende do nível de detalhe necessário para o sistema.

---

# Etapa 7 — Tratar atributos derivados

Um atributo derivado é aquele que pode ser calculado a partir de outros dados.

---

## 7.1 Exemplo: idade do aluno

A idade de um aluno pode ser calculada a partir da data de nascimento.

Nesse caso, geralmente é melhor armazenar:

```text
data_nascimento
```

E não armazenar diretamente:

```text
idade
```

Porque a idade muda com o tempo e poderia ficar desatualizada.

Por exemplo:

```text
ALUNO (
    id_aluno PK,
    nome,
    email,
    data_nascimento,
    id_curso FK
)
```

A idade pode ser calculada quando necessário, usando a data atual e a data de nascimento.

---

# Etapa 8 — Modelo relacional final simplificado

Depois de aplicar as regras de conversão, podemos obter o seguinte modelo relacional:

```text
CURSO (
    id_curso PK,
    nome,
    carga_horaria_total
)

ALUNO (
    id_aluno PK,
    nome,
    email,
    data_nascimento,
    rua,
    numero,
    bairro,
    cidade,
    estado,
    cep,
    id_curso FK
)

ALUNO_TELEFONE (
    id_aluno FK,
    telefone,
    tipo,
    PK (id_aluno, telefone)
)

PERFIL_ACADEMICO (
    id_perfil PK,
    data_ingresso,
    situacao,
    coeficiente_rendimento,
    id_aluno FK UNIQUE
)

DISCIPLINA (
    id_disciplina PK,
    nome,
    carga_horaria,
    id_curso FK
)

PROFESSOR (
    id_professor PK,
    nome,
    email,
    titulacao
)

TURMA (
    id_turma PK,
    ano,
    semestre,
    turno,
    id_disciplina FK,
    id_professor FK
)

MATRICULA (
    id_aluno FK,
    id_turma FK,
    data_matricula,
    nota_final,
    frequencia,
    situacao,
    PK (id_aluno, id_turma)
)
```

---

# Etapa 9 — Interpretação das chaves estrangeiras

## 9.1 `ALUNO.id_curso`

```text
ALUNO (
    id_aluno PK,
    ...
    id_curso FK
)
```

Indica que cada aluno pertence a um curso.

Relacionamento representado:

```text
CURSO 1 ---- N ALUNO
```

---

## 9.2 `DISCIPLINA.id_curso`

```text
DISCIPLINA (
    id_disciplina PK,
    ...
    id_curso FK
)
```

Indica que cada disciplina pertence a um curso.

Relacionamento representado:

```text
CURSO 1 ---- N DISCIPLINA
```

---

## 9.3 `TURMA.id_disciplina`

```text
TURMA (
    id_turma PK,
    ...
    id_disciplina FK
)
```

Indica que cada turma corresponde à oferta de uma disciplina.

Relacionamento representado:

```text
DISCIPLINA 1 ---- N TURMA
```

---

## 9.4 `TURMA.id_professor`

```text
TURMA (
    id_turma PK,
    ...
    id_professor FK
)
```

Indica que cada turma é ministrada por um professor.

Relacionamento representado:

```text
PROFESSOR 1 ---- N TURMA
```

---

## 9.5 `PERFIL_ACADEMICO.id_aluno`

```text
PERFIL_ACADEMICO (
    id_perfil PK,
    ...
    id_aluno FK UNIQUE
)
```

Indica que cada perfil pertence a um aluno e que cada aluno pode ter, no máximo, um perfil acadêmico.

Relacionamento representado:

```text
ALUNO 1 ---- 1 PERFIL_ACADEMICO
```

---

## 9.6 `MATRICULA.id_aluno` e `MATRICULA.id_turma`

```text
MATRICULA (
    id_aluno FK,
    id_turma FK,
    ...
    PK (id_aluno, id_turma)
)
```

Indica quais alunos estão matriculados em quais turmas.

Relacionamento representado:

```text
ALUNO N ---- N TURMA
```

---

# Resumo das regras principais

| Elemento no DER | Conversão para o modelo relacional |
|---|---|
| Entidade forte | Vira uma tabela |
| Atributo simples | Vira uma coluna |
| Identificador da entidade | Vira chave primária |
| Relacionamento 1:N | Chave do lado 1 vai para a tabela do lado N |
| Relacionamento 1:1 | Uma das tabelas recebe a FK, normalmente a mais dependente |
| Restrição em relacionamento 1:1 | A FK deve ser UNIQUE ou pode ser PK/FK |
| Relacionamento N:N | Cria-se uma nova tabela associativa |
| Atributo de relacionamento N:N | Vai para a tabela associativa |
| Atributo multivalorado | Vira uma nova tabela |
| Atributo composto | Pode ser dividido em várias colunas |
| Atributo derivado | Geralmente não é armazenado |
