# Trabalho 2o Bimestre — Evolução do Cadastro de Filmes com Java Swing e MVC

## Objetivo

Evolua o sistema de cadastro de filmes desenvolvido anteriormente. A nova versão deve permitir cadastrar **gêneros** e **atores** separadamente e utilizar essas informações no cadastro de filmes.

A aplicação deve continuar utilizando **Java Swing**, o padrão arquitetural **MVC** e persistência simulada em memória por meio de listas (`ArrayList`). Não utilize banco de dados nesta atividade.

---

## Contexto

Na primeira versão do sistema, o filme possuía título, gênero e duração. Entretanto, os gêneros eram definidos em uma lista estática dentro da classe `Filme`.

Agora, a aplicação precisa permitir que o usuário cadastre seus próprios gêneros e atores. Depois disso, esses dados devem estar disponíveis ao cadastrar ou editar um filme.

---

## Requisitos gerais

- Utilize Java Swing para a interface gráfica.
- Organize o projeto utilizando MVC.
- Não utilize banco de dados, arquivos, JSON ou bibliotecas externas.
- Simule a persistência usando `ArrayList`.
- Cada entidade deve possuir um identificador numérico (`id`) gerado automaticamente.
- A aplicação deve permitir incluir, listar, editar e excluir registros.
- Os campos obrigatórios devem ser validados.
- Exiba mensagens de sucesso e erro usando `JOptionPane`.

---

# Parte 1 — Cadastro de gêneros

Crie um cadastro completo de gêneros de filmes.

## Classe `Genero`

A classe deve possuir, no mínimo:

```java
private int id;
private String nome;
```

Implemente construtores, getters e setters.

## Funcionalidades esperadas

A tela de gêneros deve permitir:

1. Informar o nome de um gênero;
2. Salvar um novo gênero;
3. Exibir os gêneros cadastrados em uma `JTable`;
4. Selecionar um gênero na tabela para carregar seus dados no formulário;
5. Atualizar o nome de um gênero selecionado;
6. Excluir um gênero selecionado;
7. Limpar o formulário para iniciar um novo cadastro.

## Validações

- O nome do gênero não pode ficar vazio.
- Não permita o cadastro de dois gêneros com o mesmo nome.
- Ao excluir um gênero que esteja associado a algum filme, a aplicação deve impedir a exclusão e apresentar uma mensagem explicativa.

---

# Parte 2 — Cadastro de atores

Crie um cadastro completo de atores.

## Classe `Ator`

A classe deve possuir, no mínimo:

```java
private int id;
private String nome;
```

Implemente construtores, getters e setters.

## Funcionalidades esperadas

A tela de atores deve permitir:

1. Informar o nome de um ator;
2. Salvar um novo ator;
3. Exibir os atores cadastrados em uma `JTable`;
4. Selecionar um ator na tabela para carregar seus dados no formulário;
5. Atualizar os dados de um ator selecionado;
6. Excluir um ator selecionado;
7. Limpar o formulário para iniciar um novo cadastro.

## Validações

- O nome do ator não pode ficar vazio.
- Não permita o cadastro de dois atores com o mesmo nome.
- Ao excluir um ator que esteja associado a algum filme, a aplicação deve impedir a exclusão e apresentar uma mensagem explicativa.

---

# Parte 3 — Atualização do cadastro de filmes

Atualize a classe `Filme` e sua tela para utilizar os novos cadastros.

## Estrutura esperada da classe `Filme`

A classe `Filme` deve possuir, no mínimo:

```java
private int id;
private String titulo;
private int duracao;
private Genero genero;
private List<Ator> atores;
```

O atributo `genero` representa o gênero escolhido para o filme.

O atributo `atores` representa os atores que participam do filme. Um filme pode possuir **um ou mais atores**.

> Remova a lista estática de gêneros que existia na versão anterior do sistema.

## Atualizações na interface de filmes

A tela de filmes deve possuir:

- Um `JTextField` para o título;
- Um componente para informar a duração em minutos;
- Um `JComboBox<Genero>` para selecionar o gênero;
- Um `JList<Ator>` que permita selecionar vários atores;
- Uma `JTable` para exibir os filmes cadastrados;
- Botões para novo cadastro, salvar e excluir.

Para permitir a seleção de mais de um ator, configure a lista com:

```java
listaAtores.setSelectionMode(
    ListSelectionModel.MULTIPLE_INTERVAL_SELECTION
);
```

## Funcionalidades esperadas

1. Ao abrir a tela de filmes, o sistema deve carregar os gêneros e atores cadastrados nos respectivos componentes.
2. O usuário deve conseguir selecionar um gênero para o filme.
3. O usuário deve conseguir selecionar um ou mais atores para o filme.
4. Ao salvar, o filme deve manter as referências ao gênero e aos atores selecionados.
5. A tabela de filmes deve exibir, no mínimo:
   - ID;
   - Título;
   - Gênero;
   - Duração;
   - Quantidade de atores.
6. Ao selecionar um filme na tabela, seus dados devem ser carregados novamente no formulário.
7. Ao editar um filme, o gênero e os atores previamente associados devem aparecer selecionados.
8. Ao excluir um filme, seus relacionamentos com gênero e atores deixam de existir apenas para aquele filme.

## Validações

- O título do filme não pode ficar vazio.
- A duração deve ser maior que zero.
- Um gênero deve ser selecionado.
- Pelo menos um ator deve ser selecionado.
- Não deve ser possível cadastrar filmes enquanto não existir pelo menos um gênero e um ator cadastrados.

---

# Organização sugerida do projeto

A estrutura abaixo é uma sugestão. Você pode adaptá-la, desde que mantenha a separação entre Model, View e Controller.

```text
src/
├── model/
│   ├── Filme.java
│   ├── Genero.java
│   ├── Ator.java
│   ├── FilmeRepository.java
│   ├── GeneroRepository.java
│   └── AtorRepository.java
│
├── view/
│   ├── FilmeView.java
│   ├── GeneroView.java
│   ├── AtorView.java
│   └── MenuPrincipalView.java
│
├── controller/
│   ├── FilmeController.java
│   ├── GeneroController.java
│   └── AtorController.java
│
└── Main.java
```

---

# Interface principal

Crie uma tela principal para permitir o acesso aos três cadastros.

Você pode utilizar uma das opções abaixo:

- Botões: **Filmes**, **Gêneros** e **Atores**;
- Barra de menus;
- `JTabbedPane`, com uma aba para cada cadastro.

A escolha é livre, mas as três partes da aplicação devem ser acessíveis a partir da interface.

---

# Cenário de teste

Antes de finalizar, teste a aplicação seguindo esta sequência:

1. Cadastre os gêneros **Ação**, **Drama** e **Comédia**.
2. Cadastre os atores **Fernanda Montenegro**, **Wagner Moura**, **Selton Mello** e **Alice Braga**.
3. Cadastre um filme com:
   - Título: `O Auto da Compadecida`;
   - Gênero: `Comédia`;
   - Duração: `104`;
   - Atores: `Selton Mello` e `Fernanda Montenegro`.
4. Cadastre outro filme com:
   - Título: `Tropa de Elite`;
   - Gênero: `Ação`;
   - Duração: `115`;
   - Ator: `Wagner Moura`.
5. Edite um dos filmes e altere sua duração.
6. Tente excluir o gênero `Comédia` enquanto ele estiver associado a um filme.
7. Tente excluir o ator `Wagner Moura` enquanto ele estiver associado a um filme.
8. Exclua o filme `Tropa de Elite`.
9. Tente novamente excluir o ator `Wagner Moura`. 

___

## Entrega

- Até dia 18/07/2026 as 23:59
- Link para entrega: [https://forms.gle/6zd7n9bQmAJtkfJHA](https://forms.gle/6zd7n9bQmAJtkfJHA)