# Trabalho Prático — Aplicação Desktop Completa com Java Swing

## 1. Objetivo

Desenvolver uma **aplicação desktop completa utilizando Java e Swing**, aplicando de forma integrada os principais conceitos estudados nas últimas aulas.

A aplicação deverá possuir interface gráfica funcional, organização em classes e pacotes, regras de negócio, consultas, movimentações e armazenamento dos dados em memória.

> **Não deverá ser utilizado banco de dados.**

Todos os dados deverão ser mantidos utilizando Collections durante a execução da aplicação.

O objetivo principal do trabalho é demonstrar que os conceitos estudados podem ser combinados na construção de uma aplicação maior, organizada e reutilizável.

---

# 2. Conteúdos obrigatórios

O projeto deverá utilizar, de maneira coerente, os seguintes conceitos:

- Sobrecarga;
- Sobrescrita;
- Herança;
- Classes abstratas;
- Interfaces;
- Collections;
- Generics;
- Enum;
- `Comparator`;
- Funções Lambda;
- `Predicate`;
- `Function`;
- Java Swing;
- Separação de responsabilidades entre classes.

Os conceitos deverão fazer parte do funcionamento real da aplicação.

Não serão considerados exemplos criados apenas para demonstrar que determinado recurso foi utilizado.

---

# 3. Tema do projeto

Cada grupo deverá escolher um domínio para desenvolver o sistema.

Algumas possibilidades:

- Sistema de reservas de hotel;
- Biblioteca;
- Clínica;
- Academia;
- Pet shop;
- Cinema;
- Restaurante;
- Loja;
- Locadora de veículos;
- Sistema de cursos;
- Gestão de eventos;
- Agência de viagens;
- Sistema de estoque;
- Sistema de campeonatos;
- Sistema de oficina mecânica.

Outros temas poderão ser utilizados.

O domínio escolhido deverá permitir a criação de uma aplicação com:

```text
cadastros
+
movimentações
+
consultas
+
regras de negócio
+
filtros
+
ordenações
```

---

# 4. Escopo mínimo obrigatório

O sistema deverá possuir, no mínimo:

```text
6 entidades
3 telas de cadastro
2 telas de consulta
2 movimentos
```

Além disso, deverá existir:

- uma tela principal;
- navegação entre as funcionalidades;
- regras de negócio;
- filtros;
- ordenações;
- uso de Collections;
- uso de Predicate e Function.

---

# 5. Entidades

Uma entidade representa um conceito relevante do domínio do sistema.

Exemplo em um sistema de hotel:

```text
Quarto
Hospede
Reserva
Funcionario
Servico
Pagamento
```

Exemplo em uma biblioteca:

```text
Livro
Autor
Usuario
Emprestimo
Reserva
Categoria
```

Exemplo em uma clínica:

```text
Paciente
Medico
Consulta
Especialidade
Receita
Pagamento
```

O projeto deverá possuir **pelo menos 6 entidades**, relacionadas de forma coerente.

---

# 6. Exemplo de modelagem — Sistema de Hotel

Um possível conjunto de entidades seria:

```text
Pessoa
Hospede
Funcionario
Quarto
Reserva
Servico
Pagamento
```

Nesse caso, `Pessoa` poderia ser abstrata:

```text
Pessoa (abstract)
├── Hospede
└── Funcionario
```

E as demais entidades:

```text
Quarto
Reserva
Servico
Pagamento
```

Essa modelagem permite trabalhar com:

- herança;
- sobrescrita;
- classes abstratas;
- interfaces;
- relacionamentos entre entidades;
- Collections.

---

# 7. Cadastros

O sistema deverá possuir **pelo menos 3 telas de cadastro**.

Cada tela deverá permitir, quando fizer sentido:

```text
Cadastrar
Alterar
Remover
Consultar
Limpar formulário
```

Exemplo no sistema de hotel:

```text
Cadastro de Hóspedes
Cadastro de Quartos
Cadastro de Serviços
```

---

# 8. Requisitos das telas de cadastro

As telas de cadastro deverão:

- permitir entrada de dados;
- validar campos obrigatórios;
- impedir valores evidentemente inválidos;
- atualizar a Collection correspondente;
- exibir os objetos cadastrados;
- permitir seleção de objetos para alteração;
- permitir remoção;
- utilizar `JComboBox` quando houver valores de `enum`.

---

# 9. Consultas

O sistema deverá possuir **pelo menos 2 telas de consulta**.

Uma tela de consulta não deve ser apenas uma cópia da tela de cadastro.

Ela deverá permitir ao usuário:

- escolher critérios;
- aplicar filtros;
- ordenar resultados;
- visualizar informações relacionadas;
- produzir algum resumo dos dados.



# 10. Movimentos

Neste trabalho, um **movimento** representa uma operação que envolve uma ação de negócio e normalmente relaciona duas ou mais entidades.

Exemplos:

```text
Realizar reserva
Cancelar reserva
Realizar empréstimo
Registrar devolução
Realizar venda
Registrar pagamento
Agendar consulta
Finalizar atendimento
Alugar veículo
Registrar devolução do veículo
```

Um movimento não é apenas um cadastro simples.

Ele modifica o estado do sistema.

---

# 11. Requisitos dos movimentos

O sistema deverá possuir **pelo menos 2 movimentos**.

Cada movimento deverá:

- envolver pelo menos duas entidades;
- possuir uma ou mais regras de negócio;
- alterar o estado de algum objeto;
- atualizar as Collections;
- possuir uma tela própria ou uma interface claramente identificável.

---

# 12. Exemplo de movimento 1 — Realizar reserva

No sistema de hotel:

```text
Hospede
+
Quarto
+
Reserva
```

A tela poderá permitir:

```text
Selecionar hóspede
Selecionar quarto
Informar quantidade de dias
Confirmar reserva
```

Ao confirmar:

```text
Reserva é criada
+
Quarto passa para OCUPADO
```

---

# 13. Exemplo de regras do movimento

Uma reserva só poderá ser realizada se:

```text
o quarto estiver DISPONIVEL
```

Também pode existir:

```text
quantidade de hóspedes
<=
capacidade do quarto
```

Caso a regra não seja atendida, uma mensagem deverá informar o problema.

Exemplo:

```java
JOptionPane.showMessageDialog(...)
```

---

# 14. Exemplo de movimento 2 — Cancelar reserva

O segundo movimento poderia ser:

```text
Cancelamento de Reserva
```

Ao cancelar:

```text
StatusReserva → CANCELADA
```

e:

```text
Quarto → DISPONIVEL
```

Pode existir a regra:

```text
Uma reserva já FINALIZADA
não pode ser CANCELADA
```


# 15. Requisitos mínimos resumidos

O projeto deverá possuir:

- [ ] Aplicação Java Swing;
- [ ] Pelo menos 6 entidades;
- [ ] Pelo menos 3 telas de cadastro;
- [ ] Pelo menos 2 telas de consulta;
- [ ] Pelo menos 2 movimentos;
- [ ] Uma tela principal;
- [ ] Navegação entre telas;
- [ ] `JTable` para exibição de dados;
- [ ] Collections;
- [ ] Generics;
- [ ] Estrutura genérica criada pelo grupo;
- [ ] Pelo menos 2 enums;
- [ ] Herança;
- [ ] Pelo menos 1 classe abstrata;
- [ ] Pelo menos 1 interface;
- [ ] Pelo menos 2 exemplos de sobrecarga;
- [ ] Pelo menos 2 exemplos de sobrescrita;
- [ ] `Comparator`;
- [ ] Pelo menos 3 lambdas;
- [ ] Pelo menos 4 critérios de filtro;
- [ ] `Predicate`;
- [ ] Composição de Predicates;
- [ ] Pelo menos 2 usos de `Function`;
- [ ] Método genérico de transformação;
- [ ] Pelo menos 5 regras de negócio;
- [ ] Validação de dados;
- [ ] Organização em pacotes;
- [ ] Separação entre interface gráfica e lógica.

---

# 16. Entregáveis

Cada grupo deverá entregar:

## 1. Código-fonte

Projeto completo e executável.

## 2. README

O README deverá apresentar:

- nome do sistema;
- objetivo;
- domínio escolhido;
- integrantes;
- principais funcionalidades;
- lista das entidades;
- lista dos cadastros;
- lista das consultas;
- lista dos movimentos;
- instruções para execução.
