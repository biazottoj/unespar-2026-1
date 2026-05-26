# Atividade 07 - Conversão de Herenca

## Disciplina

Banco de Dados

## Tema

Conversão de hierarquias de **generalização/especialização** para o modelo relacional.

## Objetivo

Praticar a conversão de herança do modelo Entidade-Relacionamento para o modelo relacional, considerando três estratégias:

1. **Uma tabela para toda a hierarquia**;
2. **Uma tabela para cada entidade da hierarquia**;
3. **Subdivisão da entidade genérica**.

## Instruções gerais

Para cada questão, represente o modelo relacional usando a seguinte notação:

```text
TABELA (
    atributo PK,
    atributo FK,
    atributo,
    ...
)
```

Quando uma chave for, ao mesmo tempo, chave primária e chave estrangeira, use:

```text
atributo PK/FK
```

Quando necessário, indique também a tabela referenciada pela chave estrangeira.

Exemplo:

```text
ALUNO (
    id_pessoa PK/FK,
    matricula,
    ano_ingresso,
    id_curso FK
)

id_pessoa referencia PESSOA(id_pessoa)
id_curso referencia CURSO(id_curso)
```

---

# Questão 1 — Identificação da hierarquia e conversão inicial

Considere o seguinte domínio de um sistema acadêmico:

Toda **pessoa** possui:

- código;
- nome;
- CPF;
- e-mail.

Uma pessoa pode ser especializada em:

- **Aluno**;
- **Professor**;
- **Técnico-administrativo**.

Cada especialização possui os seguintes atributos:

```text
ALUNO:
- matrícula
- ano de ingresso

PROFESSOR:
- SIAPE
- titulação

TECNICO_ADMINISTRATIVO:
- cargo
- setor
```

## Tarefa

a) Identifique a entidade genérica.  
b) Identifique as entidades especializadas.  
c) Separe os atributos genéricos dos atributos específicos.  
d) Converta essa hierarquia usando a estratégia de **uma tabela para toda a hierarquia**.

## Modelo esperado de resposta

```text
PESSOA (
    ...
)
```

---

# Questão 2 — Uma tabela para toda a hierarquia com relacionamentos específicos

Considere agora uma variação do mesmo sistema acadêmico:

Toda **pessoa** possui:

- código;
- nome;
- CPF;
- e-mail.

Uma pessoa pode ser:

- **Aluno**;
- **Professor**.

Um **aluno** possui:

- matrícula;
- ano de ingresso;
- curso ao qual pertence.

Um **professor** possui:

- SIAPE;
- titulação;
- departamento ao qual pertence.

Além disso:

- Um curso possui vários alunos.
- Cada aluno pertence a um único curso.
- Um departamento possui vários professores.
- Cada professor pertence a um único departamento.

## Tarefa

Converta a hierarquia usando a estratégia de **uma tabela para toda a hierarquia**.

Seu modelo deve incluir as tabelas:

```text
PESSOA
CURSO
DEPARTAMENTO
```

Lembre-se de que a tabela única da hierarquia deve conter:

- chave primária da entidade genérica;
- coluna de tipo;
- atributos da entidade genérica;
- atributos das especializações;
- chaves estrangeiras dos relacionamentos específicos.

## Modelo esperado de resposta

```text
PESSOA (
    id_pessoa PK,
    tipo_pessoa,
    ...
)

CURSO (
    ...
)

DEPARTAMENTO (
    ...
)
```

Após montar o modelo, responda:

a) Quais colunas ficarão vazias quando a pessoa for um aluno?  
b) Quais colunas ficarão vazias quando a pessoa for um professor?  
c) Qual é a principal desvantagem dessa estratégia nesse exemplo?

---

# Questão 3 — Uma tabela para cada entidade da hierarquia

Considere a seguinte hierarquia em um sistema de biblioteca universitária:

Toda **pessoa** possui:

- código;
- nome;
- CPF;
- e-mail.

Uma pessoa pode ser:

- **Aluno**;
- **Professor**;
- **Bibliotecário**.

Atributos específicos:

```text
ALUNO:
- matrícula
- curso

PROFESSOR:
- SIAPE
- departamento

BIBLIOTECARIO:
- registro_funcional
- turno
```

## Tarefa

Converta a hierarquia usando a estratégia de **uma tabela para cada entidade da hierarquia**.

Seu modelo deve conter:

```text
PESSOA
ALUNO
PROFESSOR
BIBLIOTECARIO
```

Lembre-se de que as tabelas especializadas devem usar a chave primária da entidade genérica como **PK/FK**.

## Modelo esperado de resposta

```text
PESSOA (
    id_pessoa PK,
    ...
)

ALUNO (
    id_pessoa PK/FK,
    ...
)

PROFESSOR (
    id_pessoa PK/FK,
    ...
)

BIBLIOTECARIO (
    id_pessoa PK/FK,
    ...
)
```

Depois de converter, responda:

a) Por que `id_pessoa` aparece nas tabelas especializadas?  
b) Por que `id_pessoa` deve ser chave primária e chave estrangeira ao mesmo tempo?  
c) Qual é a principal vantagem dessa estratégia em relação à tabela única?

---

# Questão 4 — Relacionamentos envolvendo entidades especializadas

Considere um sistema acadêmico com a seguinte hierarquia:

```text
PESSOA
   ├── ALUNO
   └── PROFESSOR
```

Atributos:

```text
PESSOA:
- id_pessoa
- nome
- cpf
- email

ALUNO:
- matricula
- ano_ingresso

PROFESSOR:
- siape
- titulacao
```

Relacionamentos:

1. Um aluno pode se matricular em várias turmas.
2. Uma turma pode ter vários alunos matriculados.
3. Para cada matrícula, devem ser armazenadas:
   - data da matrícula;
   - nota final;
   - frequência;
   - situação.
4. Um professor pode ministrar várias turmas.
5. Cada turma é ministrada por um único professor.
6. Cada turma possui:
   - código;
   - ano;
   - semestre;
   - nome da disciplina.

## Tarefa

Converta o modelo usando a estratégia de **uma tabela para cada entidade da hierarquia**.

Seu modelo deve incluir:

```text
PESSOA
ALUNO
PROFESSOR
TURMA
MATRICULA
```

Atenção:

- `MATRICULA` deve referenciar `ALUNO`, e não apenas `PESSOA`.
- `TURMA` deve referenciar `PROFESSOR`, e não apenas `PESSOA`.

## Modelo esperado de resposta

```text
PESSOA (
    ...
)

ALUNO (
    ...
)

PROFESSOR (
    ...
)

TURMA (
    ...
)

MATRICULA (
    ...
)
```

Depois de converter, responda:

a) Por que é melhor `MATRICULA` referenciar `ALUNO` em vez de `PESSOA`?  
b) Por que é melhor `TURMA` referenciar `PROFESSOR` em vez de `PESSOA`?  
c) Qual atributo da tabela `MATRICULA` pertence ao relacionamento, e não isoladamente a `ALUNO` ou `TURMA`?

---

# Questão 5 — Subdivisão da entidade genérica

Considere a seguinte hierarquia de um sistema de usuários institucionais:

```text
USUARIO
   ├── ALUNO
   ├── PROFESSOR
   └── VISITANTE
```

Atributos:

```text
USUARIO:
- id_usuario
- nome
- email

ALUNO:
- matricula
- curso

PROFESSOR:
- siape
- departamento

VISITANTE:
- instituicao_origem
- data_validade_acesso
```

Nesta questão, você deve usar a estratégia de **subdivisão da entidade genérica**.

Nessa estratégia, cada tabela especializada deve conter:

- os atributos da entidade genérica;
- os atributos da entidade especializada.

## Tarefa

Converta a hierarquia usando **subdivisão da entidade genérica**.

Seu modelo deve conter:

```text
ALUNO
PROFESSOR
VISITANTE
```

Não crie uma tabela `USUARIO`.

## Modelo esperado de resposta

```text
ALUNO (
    id_usuario PK,
    nome,
    email,
    ...
)

PROFESSOR (
    id_usuario PK,
    nome,
    email,
    ...
)

VISITANTE (
    id_usuario PK,
    nome,
    email,
    ...
)
```

Depois de converter, responda:

a) Quais atributos foram repetidos nas tabelas especializadas?  
b) Qual problema essa estratégia pode causar em relação à unicidade de `id_usuario`?  
c) Por que essa estratégia dificulta criar uma chave estrangeira para um usuário genérico?  
d) Em que tipo de situação essa estratégia poderia ser aceitável?

---

# Questão 6 — Escolha da melhor estratégia de conversão

Considere o seguinte cenário:

Uma universidade possui uma hierarquia chamada `PESSOA`, com as especializações:

```text
ALUNO
PROFESSOR
TECNICO_ADMINISTRATIVO
COORDENADOR
```

Atributos comuns de `PESSOA`:

```text
id_pessoa
nome
cpf
email
telefone
```

Atributos específicos:

```text
ALUNO:
- matricula
- ano_ingresso
- id_curso

PROFESSOR:
- siape
- titulacao
- id_departamento

TECNICO_ADMINISTRATIVO:
- registro_funcional
- cargo
- setor

COORDENADOR:
- data_inicio_gestao
- id_curso_coordenado
```

Relacionamentos:

1. Alunos se matriculam em turmas.
2. Professores ministram turmas.
3. Coordenadores coordenam cursos.
4. Técnicos-administrativos são alocados em setores.
5. O sistema frequentemente precisa listar todas as pessoas da instituição.
6. O sistema também precisa consultar dados específicos de alunos e professores.

## Tarefa

Escolha uma das três estratégias de conversão:

```text
1. Uma tabela para toda a hierarquia
2. Uma tabela para cada entidade da hierarquia
3. Subdivisão da entidade genérica
```

Depois, faça o que se pede:

a) Indique a estratégia escolhida.  
b) Converta a hierarquia usando a estratégia escolhida.  
c) Justifique tecnicamente sua escolha.  
d) Aponte uma vantagem da estratégia escolhida.  
e) Aponte uma desvantagem da estratégia escolhida.  
f) Explique por que as outras duas estratégias seriam menos adequadas para esse cenário.

---
