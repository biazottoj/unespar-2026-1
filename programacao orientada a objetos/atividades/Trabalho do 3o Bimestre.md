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

# 9. Requisitos das telas de cadastro

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

# 10. Consultas

O sistema deverá possuir **pelo menos 2 telas de consulta**.

Uma tela de consulta não deve ser apenas uma cópia da tela de cadastro.

Ela deverá permitir ao usuário:

- escolher critérios;
- aplicar filtros;
- ordenar resultados;
- visualizar informações relacionadas;
- produzir algum resumo dos dados.

---

# 11. Exemplo de consulta 1 — Quartos

```text
+------------------------------------------------+
|             CONSULTA DE QUARTOS                |
+------------------------------------------------+
| Tipo:              [ TODOS ▼ ]                 |
| Disponibilidade:   [ TODOS ▼ ]                 |
| Valor máximo:      [__________]                |
|                                                |
| Ordenar por:       [ PREÇO ▼ ]                 |
| Ordem:             [ CRESCENTE ▼ ]             |
|                                                |
| [ Pesquisar ] [ Limpar ]                       |
+------------------------------------------------+
| Número | Tipo | Diária | Disponibilidade       |
|------------------------------------------------|
| 101    | ...  | ...    | ...                   |
+------------------------------------------------+
```

Essa consulta poderá integrar:

```text
Collection
+
Enum
+
Predicate
+
Lambda
+
Comparator
```

---

# 12. Exemplo de consulta 2 — Reservas

Filtros possíveis:

```text
Hospede
Status
Quarto
Valor mínimo
Valor máximo
```

Resultados:

```text
Reserva
Hospede
Quarto
Status
Valor total
```

Além da listagem, a consulta poderá exibir:

```text
Quantidade de reservas
Valor médio
Valor total
```

Nesse caso, `Function` pode ser utilizada para transformar objetos em valores ou descrições.

---

# 13. Movimentos

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

# 14. Requisitos dos movimentos

O sistema deverá possuir **pelo menos 2 movimentos**.

Cada movimento deverá:

- envolver pelo menos duas entidades;
- possuir uma ou mais regras de negócio;
- alterar o estado de algum objeto;
- atualizar as Collections;
- possuir uma tela própria ou uma interface claramente identificável.

---

# 15. Exemplo de movimento 1 — Realizar reserva

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

# 16. Exemplo de regras do movimento

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

# 17. Exemplo de movimento 2 — Cancelar reserva

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

---

# 18. Outros exemplos de movimentos

## Biblioteca

```text
Movimento 1:
Realizar empréstimo

Movimento 2:
Registrar devolução
```

## Clínica

```text
Movimento 1:
Agendar consulta

Movimento 2:
Finalizar atendimento
```

## Loja

```text
Movimento 1:
Realizar venda

Movimento 2:
Registrar pagamento
```

## Locadora

```text
Movimento 1:
Alugar veículo

Movimento 2:
Registrar devolução
```

---

# 19. Collections

Os dados deverão ser armazenados utilizando Collections.

Exemplo:

```java
private List<Quarto> quartos;
private List<Hospede> hospedes;
private List<Reserva> reservas;
private List<Servico> servicos;
```

Também podem ser utilizados:

```java
Set
Map
```

quando houver justificativa.

---

# 20. Generics

O projeto deverá utilizar Generics de forma explícita.

O uso de:

```java
List<Quarto>
```

já é uma aplicação de Generics.

Entretanto, deverá existir pelo menos mais uma estrutura genérica criada pelo grupo.

Exemplo:

```java
public class Repositorio<T> {

    private List<T> itens =
        new ArrayList<>();

    public void adicionar(T item) {
        itens.add(item);
    }

    public void remover(T item) {
        itens.remove(item);
    }

    public List<T> listar() {
        return itens;
    }
}
```

Uso:

```java
Repositorio<Quarto>
Repositorio<Hospede>
Repositorio<Servico>
```

---

# 21. Sobrecarga

O projeto deverá possuir pelo menos **dois exemplos de sobrecarga**.

Exemplo em construtores:

```java
public Quarto(
        int numero,
        double valorDiaria) {
}
```

```java
public Quarto(
        int numero,
        double valorDiaria,
        TipoQuarto tipo) {
}
```

Exemplo em métodos:

```java
buscar(int codigo)
```

```java
buscar(String nome)
```

---

# 22. Sobrescrita

O projeto deverá possuir pelo menos **dois usos de sobrescrita**.

Um deles pode ser:

```java
@Override
public String toString()
```

Outro deverá estar relacionado à hierarquia de classes.

Exemplo:

```java
public abstract class Pessoa {

    public abstract String getDescricao();
}
```

```java
public class Hospede extends Pessoa {

    @Override
    public String getDescricao() {
        return "Hóspede";
    }
}
```

---

# 23. Classe abstrata

O projeto deverá possuir pelo menos **uma classe abstrata**.

Ela deverá representar um conceito genérico que não faça sentido ser instanciado diretamente.

Exemplo:

```java
public abstract class Pessoa {

    private String nome;
    private String documento;

    public abstract String getDescricao();
}
```

Subclasses:

```text
Hospede
Funcionario
```

---

# 24. Interfaces

O projeto deverá possuir pelo menos **uma interface**.

Ela deverá representar um contrato ou capacidade.

Exemplo:

```java
public interface Calculavel {

    double calcularValor();
}
```

Ela poderia ser implementada por diferentes entidades quando fizer sentido.

---

# 25. Enum

O projeto deverá possuir pelo menos **dois enums**.

Exemplo:

```java
public enum TipoQuarto {

    SIMPLES,
    DUPLO,
    COBERTURA

}
```

```java
public enum StatusReserva {

    PENDENTE,
    CONFIRMADA,
    CANCELADA,
    FINALIZADA

}
```

Sempre que possível, os enums deverão aparecer na interface através de:

```java
JComboBox
```

---

# 26. Comparator

Pelo menos uma das telas de consulta deverá permitir ordenar objetos de **duas formas diferentes**.

Exemplo:

```text
Ordenar quartos por:

Número
Preço
Tipo
```

Uma das ordenações deverá utilizar uma implementação explícita de:

```java
Comparator<T>
```

Exemplo:

```java
public class ComparadorPorPreco
        implements Comparator<Quarto> {

    @Override
    public int compare(
            Quarto q1,
            Quarto q2) {

        return Double.compare(
            q1.getValorDiaria(),
            q2.getValorDiaria()
        );
    }
}
```

---

# 27. Funções Lambda

O projeto deverá possuir pelo menos **três usos reais de lambda**.

Exemplos:

## Evento Swing

```java
botaoSalvar.addActionListener(
    e -> salvar()
);
```

## Ordenação

```java
quartos.sort(
    (q1, q2) ->
        Integer.compare(
            q1.getNumero(),
            q2.getNumero()
        )
);
```

## Predicate

```java
q ->
    q.getValorDiaria() <= 300
```

---

# 28. Predicate

Pelo menos uma tela de consulta deverá utilizar:

```java
Predicate<T>
```

para implementar filtros dinâmicos.

Exemplo:

```java
public List<Quarto> filtrar(
        Predicate<Quarto> criterio) {

    List<Quarto> resultado =
        new ArrayList<>();

    for (Quarto quarto : quartos) {

        if (criterio.test(quarto)) {

            resultado.add(quarto);
        }
    }

    return resultado;
}
```

---

# 29. Filtros obrigatórios

As duas telas de consulta deverão possuir filtros.

No total, o sistema deverá possuir pelo menos:

```text
4 critérios de filtro diferentes
```

Exemplos:

```text
tipo
status
faixa de valor
nome
categoria
data
disponibilidade
```

---

# 30. Composição de Predicates

Pelo menos uma consulta deverá combinar critérios.

Exemplo:

```java
Predicate<Quarto> disponivel =
    q ->
        q.getDisponibilidade()
        == Disponibilidade.DISPONIVEL;
```

```java
Predicate<Quarto> barato =
    q ->
        q.getValorDiaria()
        <= 300;
```

Depois:

```java
Predicate<Quarto> criterio =
    disponivel.and(barato);
```

---

# 31. Function

O projeto deverá utilizar:

```java
Function<T, R>
```

em pelo menos **duas funcionalidades**.

Exemplo:

```java
Function<Quarto, String> resumo =
    quarto ->
        "Quarto "
        + quarto.getNumero()
        + " - R$ "
        + quarto.getValorDiaria();
```

---

# 32. Método genérico de transformação

O grupo deverá criar pelo menos um método semelhante a:

```java
public <T, R> List<R> transformar(
        List<T> itens,
        Function<T, R> funcao) {

    List<R> resultado =
        new ArrayList<>();

    for (T item : itens) {

        resultado.add(
            funcao.apply(item)
        );
    }

    return resultado;
}
```

Esse método deverá ser utilizado em alguma funcionalidade real.

---

# 33. Possíveis usos de Function

Exemplos:

```text
Quarto → String
Reserva → Double
Hospede → String
Produto → String
Venda → Double
```

Uma tela de consulta poderá utilizar `Function` para criar:

- resumos;
- descrições;
- valores calculados;
- informações para relatórios.

---

# 34. Regras de negócio

O projeto deverá possuir pelo menos **cinco regras de negócio**.

Exemplo no hotel:

```text
1. Quarto ocupado não pode receber reserva.

2. Reserva cancelada não pode ser finalizada.

3. Quantidade de hóspedes não pode exceder capacidade.

4. Número do quarto não pode se repetir.

5. Valor da diária deve ser maior que zero.
```

Essas regras não deverão estar concentradas diretamente nas telas.

---

# 35. Validação de dados

As telas deverão validar:

- campos obrigatórios;
- números inválidos;
- valores negativos;
- duplicidade;
- estados incompatíveis;
- referências obrigatórias entre entidades.

Utilize:

```java
JOptionPane.showMessageDialog(...)
```

ou componente semelhante para informar erros.

---

# 36. Separação de responsabilidades

Evite colocar a lógica diretamente nos componentes Swing.

Não faça:

```java
botaoReservar.addActionListener(
    e -> {

        // muitas linhas de regra de negócio

    }
);
```

Prefira:

```java
botaoReservar.addActionListener(
    e -> realizarReserva()
);
```

E:

```java
private void realizarReserva() {

    service.realizarReserva(...);
}
```

---

# 37. Service

O projeto deverá possuir pelo menos uma classe responsável pelas operações e regras do sistema.

Exemplo:

```java
public class HotelService {

    private Repositorio<Quarto> quartos;

    private Repositorio<Hospede> hospedes;

    private Repositorio<Reserva> reservas;

    // operações
}
```

Fluxo:

```text
Swing
  ↓
Service
  ↓
Collections
```

---

# 38. Organização em pacotes

Sugestão:

```text
src/
│
├── app/
│   └── Main.java
│
├── model/
│   ├── Entidade1.java
│   ├── Entidade2.java
│   ├── Entidade3.java
│   ├── Entidade4.java
│   ├── Entidade5.java
│   └── Entidade6.java
│
├── service/
│   └── SistemaService.java
│
├── repository/
│   └── Repositorio.java
│
├── ui/
│   ├── TelaPrincipal.java
│   ├── TelaCadastro1.java
│   ├── TelaCadastro2.java
│   ├── TelaCadastro3.java
│   ├── TelaConsulta1.java
│   ├── TelaConsulta2.java
│   ├── TelaMovimento1.java
│   └── TelaMovimento2.java
│
└── util/
    └── Comparadores.java
```

Os nomes deverão ser adaptados ao domínio escolhido.

---

# 39. Arquitetura sugerida

```text
+------------------------------------+
|            Java Swing              |
|                                    |
| Cadastros                          |
| Consultas                          |
| Movimentos                         |
+----------------+-------------------+
                 |
                 v
+------------------------------------+
|              Service               |
|                                    |
| Regras de negócio                  |
| Movimentações                      |
| Filtros                            |
| Consultas                          |
+----------------+-------------------+
                 |
                 v
+------------------------------------+
|          Repositórios              |
|                                    |
| List<T>                            |
| Set<T>                             |
| Map<K,V>                           |
+----------------+-------------------+
                 |
                 v
+------------------------------------+
|               Model                |
|                                    |
| Entidades                          |
| Enums                              |
| Classes abstratas                  |
| Interfaces                         |
+------------------------------------+
```

---

# 40. Fluxo de um cadastro

```text
Usuário
   ↓
Tela de Cadastro
   ↓
Validação
   ↓
Service
   ↓
Entidade
   ↓
Collection
   ↓
Atualização da JTable
```

---

# 41. Fluxo de um movimento

```text
Usuário
   ↓
Tela de Movimento
   ↓
Seleciona entidades
   ↓
Service
   ↓
Valida regras
   ↓
Cria/altera movimento
   ↓
Atualiza entidades relacionadas
   ↓
Atualiza Collections
```

---

# 42. Fluxo de uma consulta

```text
Usuário
   ↓
Escolhe filtros
   ↓
Predicate
   ↓
Collection
   ↓
Comparator
   ↓
Function
   ↓
Resultado
   ↓
JTable
```

---

# 43. Requisitos mínimos resumidos

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

# 44. Restrições

Não utilizar:

```text
Banco de dados
JDBC
JPA
Hibernate
Spring
```

Os dados deverão existir apenas durante a execução da aplicação.

O armazenamento deverá utilizar:

```text
Collections Java
```

Quando o programa for encerrado, os dados podem ser perdidos.

---

# 45. Entregáveis

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

## 3. Diagrama de classes

O diagrama deverá apresentar:

- pelo menos 6 entidades;
- relacionamentos;
- heranças;
- classe abstrata;
- interfaces;
- principais atributos;
- principais métodos.

## 4. Mapeamento dos conceitos

Inclua uma tabela:

| Conceito | Onde foi utilizado | Por que foi utilizado |
|---|---|---|
| Sobrecarga | | |
| Sobrescrita | | |
| Herança | | |
| Classe abstrata | | |
| Interface | | |
| Collection | | |
| Generics | | |
| Enum | | |
| Comparator | | |
| Lambda | | |
| Predicate | | |
| Function | | |

A justificativa é obrigatória.

Não basta escrever apenas:

```text
Predicate → TelaConsulta
```

Explique qual problema foi resolvido pelo conceito.

---

# 46. Apresentação

Durante a apresentação, o grupo deverá demonstrar:

1. Tela principal;
2. Pelo menos 3 cadastros;
3. Inclusão de registros;
4. Alteração de registros;
5. Remoção de registros;
6. Pelo menos 2 movimentos;
7. Pelo menos 2 consultas;
8. Aplicação de filtros;
9. Combinação de filtros;
10. Ordenação;
11. Uso de `Function`;
12. Pelo menos uma regra de negócio impedindo uma operação inválida.

---

# 47. Perguntas possíveis na apresentação

Qualquer integrante poderá ser questionado sobre:

> Quais são as seis entidades do sistema?

> Como elas se relacionam?

> Onde existe herança?

> Por que determinada classe é abstrata?

> Onde existe sobrescrita?

> Onde existe sobrecarga?

> Por que foi utilizada uma interface?

> Por que foi utilizada uma `List` e não um `Set` ou `Map`?

> Como Generics aparecem no sistema?

> Qual é a função do `Comparator`?

> Como uma lambda utilizada no sistema funciona?

> Qual é o método de `Predicate`?

> Como os Predicates são combinados?

> Qual é o método de `Function`?

> O que representam `T` e `R` em `Function<T, R>`?

> Qual é a diferença entre cadastro e movimento?

> Que entidades são afetadas por um movimento?

> Onde estão implementadas as regras de negócio?

> Por que as regras não estão diretamente na tela Swing?

---

# 48. Sugestão de progressão

## Etapa 1 — Definição do domínio

Antes de programar, liste:

```text
6 ou mais entidades
3 cadastros
2 consultas
2 movimentos
5 regras de negócio
```

## Etapa 2 — Modelagem

Defina:

- entidades;
- atributos;
- relacionamentos;
- enums;
- herança;
- classes abstratas;
- interfaces.

## Etapa 3 — Implementação do Model

Implemente inicialmente:

```text
classes
construtores
sobrecarga
sobrescrita
herança
abstrações
interfaces
enums
```

## Etapa 4 — Repositórios

Implemente as Collections.

Exemplo:

```java
Repositorio<Quarto>
Repositorio<Hospede>
Repositorio<Reserva>
```

## Etapa 5 — Service

Implemente:

- cadastros;
- alterações;
- remoções;
- regras;
- movimentos;
- filtros;
- consultas.

## Etapa 6 — Predicate, Function e Comparator

Antes da interface, implemente e teste:

```text
filtros
combinação de filtros
ordenações
transformações
```

## Etapa 7 — Swing

Implemente:

```text
Tela Principal
3+ Cadastros
2+ Consultas
2+ Movimentos
```

## Etapa 8 — Integração

Teste:

```text
Tela
↓
Service
↓
Collections
↓
Entidades
```

---

# 49. Exemplo completo de escopo — Hotel

## Entidades

```text
1. Pessoa
2. Hospede
3. Funcionario
4. Quarto
5. Reserva
6. Servico
7. Pagamento
```

## Cadastros

```text
1. Cadastro de Hóspedes
2. Cadastro de Quartos
3. Cadastro de Serviços
```

## Consultas

```text
1. Consulta de Quartos
2. Consulta de Reservas
```

## Movimentos

```text
1. Realizar Reserva
2. Cancelar/Finalizar Reserva
```

## Possíveis regras

```text
Quarto ocupado não pode ser reservado.

Quarto em manutenção não pode ser reservado.

Número do quarto não pode se repetir.

Reserva finalizada não pode ser cancelada.

Quantidade de hóspedes deve respeitar a capacidade.

Pagamento não pode possuir valor negativo.
```

---

# 50. Exemplo completo de escopo — Biblioteca

## Entidades

```text
1. Pessoa
2. Usuario
3. Funcionario
4. Livro
5. Autor
6. Emprestimo
7. Categoria
```

## Cadastros

```text
1. Usuários
2. Livros
3. Autores
```

## Consultas

```text
1. Consulta de livros
2. Consulta de empréstimos
```

## Movimentos

```text
1. Realizar empréstimo
2. Registrar devolução
```

---

# 51. Exemplo completo de escopo — Loja

## Entidades

```text
1. Pessoa
2. Cliente
3. Funcionario
4. Produto
5. Categoria
6. Venda
7. ItemVenda
8. Pagamento
```

## Cadastros

```text
1. Clientes
2. Produtos
3. Categorias
```

## Consultas

```text
1. Consulta de produtos
2. Consulta de vendas
```

## Movimentos

```text
1. Realizar venda
2. Registrar/cancelar pagamento
```

---

# 52. O objetivo não é apenas usar todos os conceitos

Não será considerado adequado criar elementos artificiais como:

```java
Predicate<Quarto> predicate =
    quarto -> true;
```

apenas para afirmar que o projeto possui um `Predicate`.

Da mesma forma:

```java
interface MinhaInterface {
}
```

sem uma responsabilidade real não demonstra compreensão.

Cada conceito deverá possuir uma justificativa dentro da arquitetura.

---

# 53. Questão central do trabalho

Ao final, o grupo deve conseguir explicar:

> **Como os conceitos de Orientação a Objetos e os recursos modernos do Java foram utilizados para organizar uma aplicação desktop com cadastros, consultas e movimentos?**

O objetivo é integrar:

```text
Swing
+
OO
+
Collections
+
Generics
+
Enum
+
Comparator
+
Lambda
+
Predicate
+
Function
```

em uma única aplicação coerente.

O resultado esperado não é apenas uma interface que funciona, mas uma aplicação em que seja possível perceber claramente:

```text
Model
+
Regras
+
Dados
+
Interface
```

trabalhando de forma integrada.
