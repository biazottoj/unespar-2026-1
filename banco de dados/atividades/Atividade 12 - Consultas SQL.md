# Atividade prática — Consultas SQL em um sistema de streaming

## Objetivo

Praticar os conceitos de consultas SQL estudados em aula por meio de um banco de dados que representa uma plataforma de streaming. A atividade trabalha com:

- `SELECT` e projeção de colunas;
- cláusula `WHERE`;
- operadores relacionais e lógicos;
- tratamento de valores `NULL`;
- funções `UPPER` e `LOWER`;
- operador `LIKE`;
- consultas envolvendo várias tabelas;

## Banco de dados

O banco contém quatro tabelas:

| Tabela | Finalidade |
|---|---|
| `plano` | Armazena os planos oferecidos pela plataforma. |
| `usuario` | Armazena os usuários e o plano contratado por cada um. |
| `conteudo` | Armazena filmes, séries e documentários disponíveis no catálogo. |
| `visualizacao` | Registra quais conteúdos foram assistidos pelos usuários. |

### Relacionamentos principais

- `usuario.id_plano` referencia `plano.id_plano`;
- `visualizacao.id_usuario` referencia `usuario.id_usuario`;
- `visualizacao.id_conteudo` referencia `conteudo.id_conteudo`.

## Preparação

1. Acesse o compilador SQL do Programiz.
2. Importe o arquivo `Atividade 12 - BD Sistema de Streaming.sql`.
3. Execute o script para criar e preencher as tabelas.
4. Apague ou comente a consulta de verificação localizada ao final do arquivo.
5. Escreva e execute uma consulta para cada questão.

> Nas questões que envolvem várias tabelas, utilize preferencialmente a sintaxe apresentada em aula: nomes de tabelas separados por vírgula na cláusula `FROM` e condições de associação na cláusula `WHERE`.

---

## Parte 1 — Consultas básicas e projeção

### Questão 1

Obtenha todos os dados cadastrados na tabela `usuario`.

### Questão 2

Obtenha todos os dados cadastrados na tabela `conteudo`.

### Questão 3

Obtenha apenas o identificador, o título e o tipo de cada conteúdo.

### Questão 4

Obtenha o identificador, o nome, o e-mail e a cidade de cada usuário.

### Questão 5

Obtenha o título, o gênero, o ano de lançamento e a duração de cada conteúdo.

### Questão 6

Obtenha o nome, o preço mensal, a qualidade de vídeo e a quantidade de telas simultâneas de todos os planos.

---

## Parte 2 — Seleção e expressões lógicas

### Questão 7

Obtenha todos os dados dos usuários cuja cidade seja exatamente `Curitiba`.

### Questão 8

Obtenha o identificador, o título e a duração dos conteúdos cuja duração seja maior que 120 minutos.

### Questão 9

Obtenha todos os dados dos conteúdos que sejam do tipo `Filme`, pertençam ao gênero `Drama` **e** possuam classificação indicativa menor ou igual a 16 anos.

### Questão 10

Obtenha o identificador, o título e o gênero dos conteúdos que pertençam ao gênero `Animação` **ou** ao gênero `Suspense`.

### Questão 11

Obtenha o identificador, o nome e o preço mensal dos planos cujo preço seja maior ou igual a 30 reais.

### Questão 12

Obtenha todos os dados dos usuários cuja cidade seja diferente exatamente da cadeia `São Paulo`, incluindo os usuários que não possuem cidade informada.

### Questão 13

Obtenha o identificador, o nome e o e-mail dos usuários que não possuem cidade informada.

### Questão 14

Obtenha o identificador, o título, o país de origem e o idioma original dos conteúdos que possuem idioma original informado.

### Questão 15

Obtenha os usuários da cidade de São Paulo, considerando que o nome da cidade pode ter sido registrado com diferentes combinações de letras maiúsculas e minúsculas. Resolva usando a função `LOWER`.

---

## Parte 3 — Consultas com `LIKE`

### Questão 16

Obtenha o identificador e o nome dos usuários cujo nome começa com a letra `A` maiúscula.

### Questão 17

Obtenha o identificador e o título dos conteúdos cujo título termina com a letra `a` minúscula.

### Questão 18

Obtenha o identificador e o título dos conteúdos cujo título possui exatamente quatro caracteres.

### Questão 19

Obtenha o identificador e o título dos conteúdos cujo título começa com a letra `O` maiúscula e termina com a letra `o` minúscula.

### Questão 20

Obtenha o identificador, o título e o gênero dos conteúdos cujo título contenha a cadeia `ção` escrita em letras minúsculas.

---

## Parte 4 — Consultas envolvendo várias tabelas

### Questão 21

Para cada visualização do conteúdo denominado `Horizonte Perdido`, obtenha o identificador do usuário, o nome do usuário, a data da visualização e o percentual assistido.

### Questão 22

Para cada visualização registrada, obtenha o nome do usuário, o título do conteúdo, a data da visualização e o percentual assistido.

### Questão 23

Para cada visualização registrada, obtenha o nome do usuário, o nome do plano contratado, o título do conteúdo e a data da visualização.

### Questão 24

Obtenha o identificador e o nome de cada usuário que tenha assistido a um conteúdo do tipo `Documentário`. Nesta questão, linhas duplicadas podem permanecer no resultado.

### Questão 25

Obtenha o identificador e o título dos conteúdos assistidos por usuários cuja cidade seja `Curitiba`. Nesta questão, linhas duplicadas podem permanecer no resultado.

### Questão 26

Obtenha o nome do usuário, o título do conteúdo e o percentual assistido das visualizações cujo percentual seja maior que 80.

### Questão 27

Obtenha o nome de cada usuário, sua cidade, o nome do plano contratado e o preço mensal do plano.

### Questão 28

Para cada visualização de um conteúdo do tipo `Série`, obtenha o nome do usuário, o título da série, a data da visualização e o percentual assistido.


## Entrega

Para cada questão, apresente:

- o número da questão;
- o comando SQL utilizado;

- Utilize o link para entregar a atividade: [https://forms.gle/ABg3n6dQs9PF5zTq9](https://forms.gle/ABg3n6dQs9PF5zTq9)
- Até 11/08/2026