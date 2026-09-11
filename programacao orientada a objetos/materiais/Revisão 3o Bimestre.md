# Material de Estudo — Revisão de Java Orientado a Objetos e Recursos Modernos

## Conteúdos

| Data | Conteúdo |
|---|---|
| 07/08/2026 | Classes e Métodos Abstratos. Classes `final` |
| 14/08/2026 | Interfaces, Sobrecarga e Sobrescrita |
| 21/08/2026 | Collections e Generics |
| 28/08/2026 | Enum e Funções Lambda |
| 04/09/2026 | Streams e Processamento de Coleções |

Os exemplos deste material utilizam como contexto um **Sistema de Hotel**.

---

# 1. Classes e Métodos Abstratos

## Conceito

Uma classe abstrata representa um conceito genérico que serve como base para outras classes.

```java
public abstract class Pessoa {

    private String nome;

    public Pessoa(String nome) {
        this.nome = nome;
    }

    public String getNome() {
        return nome;
    }
}
```

Uma classe abstrata **não pode ser instanciada diretamente**:

```java
Pessoa pessoa = new Pessoa("Ana"); // erro
```

Ela pode ser herdada:

```java
public class Hospede extends Pessoa {

    public Hospede(String nome) {
        super(nome);
    }
}
```

## Aplicações mais comuns

Use uma classe abstrata quando:

- existe uma relação de herança;
- várias classes compartilham atributos e comportamentos;
- a superclasse representa um conceito genérico;
- não faz sentido criar objetos diretamente da superclasse.

Exemplos:

```text
Pessoa
├── Hospede
└── Funcionario
```

```text
Pagamento
├── PagamentoPix
├── PagamentoCartao
└── PagamentoDinheiro
```

---

# 2. Métodos abstratos

Um método abstrato define uma operação que deverá ser implementada pelas subclasses.

```java
public abstract class Pagamento {

    public abstract double calcularTaxa();
}
```

Cada subclasse define sua própria regra:

```java
public class PagamentoPix extends Pagamento {

    @Override
    public double calcularTaxa() {
        return 0.0;
    }
}
```

```java
public class PagamentoCartao extends Pagamento {

    @Override
    public double calcularTaxa() {
        return 5.0;
    }
}
```

Uma classe abstrata também pode possuir métodos concretos:

```java
public abstract class Pessoa {

    private String nome;

    public String getNome() {
        return nome;
    }

    public abstract String getDescricao();
}
```

## Aplicações mais comuns

Métodos abstratos são úteis quando:

- todas as subclasses precisam oferecer a mesma operação;
- não existe uma implementação genérica adequada;
- cada subclasse deve especializar o comportamento.

---

# 3. `final`

A palavra-chave `final` possui significados diferentes.

## Classe `final`

Uma classe `final` não pode ser herdada.

```java
public final class ConfiguracaoHotel {
}
```

## Método `final`

Um método `final` não pode ser sobrescrito.

```java
public final void gerarCodigo() {
}
```

## Variável `final`

Uma variável `final` só pode receber uma atribuição.

```java
final double TAXA = 0.10;
```

É comum em constantes:

```java
public static final double TAXA_SERVICO = 0.10;
```

## `abstract` versus `final`

```text
abstract
→ abre para especialização

final
→ fecha para especialização
```

Uma classe não pode ser simultaneamente `abstract` e `final`.

---

# 4. Interfaces

## Conceito

Uma interface define um contrato.

```java
public interface Calculavel {

    double calcularValor();
}
```

Uma classe implementa esse contrato:

```java
public class Reserva implements Calculavel {

    private double valorDiaria;
    private int dias;

    @Override
    public double calcularValor() {
        return valorDiaria * dias;
    }
}
```

Uma forma útil de pensar:

```text
Herança
→ É UM TIPO DE

Interface
→ É CAPAZ DE
```

Exemplo:

```text
Hospede É UMA Pessoa.
Reserva É CAPAZ DE calcular um valor.
```

## Aplicações mais comuns

Interfaces são utilizadas para:

- definir contratos;
- representar capacidades;
- permitir implementações diferentes;
- reduzir acoplamento;
- permitir polimorfismo entre classes diferentes.

Uma classe pode implementar várias interfaces:

```java
public class Reserva
        implements Calculavel, Cancelavel {
}
```

---

# 5. Sobrecarga

## Conceito

Sobrecarga ocorre quando existem métodos com:

```text
mesmo nome
+
parâmetros diferentes
```

Exemplo:

```java
public void buscarQuarto(int numero) {
}

public void buscarQuarto(TipoQuarto tipo) {
}

public void buscarQuarto(
        TipoQuarto tipo,
        double valorMaximo) {
}
```

Também pode ocorrer em construtores:

```java
public Quarto(
        int numero,
        double valorDiaria) {
}

public Quarto(
        int numero,
        double valorDiaria,
        TipoQuarto tipo) {
}
```

## Aplicações mais comuns

- oferecer diferentes formas de executar uma operação;
- fornecer diferentes construtores;
- tornar uma API mais conveniente.

---

# 6. Sobrescrita

## Conceito

Sobrescrita ocorre quando uma subclasse fornece uma nova implementação para um método herdado.

```java
public class Pessoa {

    public String getDescricao() {
        return "Pessoa";
    }
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

É recomendável utilizar:

```java
@Override
```

Outro exemplo comum é `toString()`:

```java
@Override
public String toString() {

    return "Quarto "
        + numero
        + " - R$ "
        + valorDiaria;
}
```

---

# 7. Sobrecarga versus Sobrescrita

| Sobrecarga | Sobrescrita |
|---|---|
| Mesmo nome | Mesmo nome |
| Parâmetros diferentes | Mesmos parâmetros |
| Pode ocorrer na mesma classe | Envolve herança |
| Não utiliza `@Override` | `@Override` é recomendado |
| Oferece variações | Especializa comportamento |

Resumo:

```text
Sobrecarga
→ mesma operação em formatos diferentes

Sobrescrita
→ nova implementação de uma operação herdada
```

---

# 8. Collections

Collections são estruturas utilizadas para armazenar e manipular grupos de objetos.

Principais estruturas:

```text
List
Set
Map
```

---

# 9. `List`

Uma `List` representa uma coleção ordenada de elementos.

```java
List<Quarto> quartos =
    new ArrayList<>();

quartos.add(q1);
quartos.add(q2);
quartos.add(q3);
```

Acesso:

```java
Quarto primeiro =
    quartos.get(0);
```

Percurso:

```java
for (Quarto quarto : quartos) {
    System.out.println(quarto);
}
```

## Aplicações mais comuns

- lista de quartos;
- lista de hóspedes;
- histórico de reservas;
- produtos de uma venda;
- elementos exibidos em uma tabela.

---

# 10. `Set`

Um `Set` não permite elementos duplicados segundo suas regras de igualdade.

```java
Set<String> servicos =
    new HashSet<>();

servicos.add("Wi-Fi");
servicos.add("Piscina");
servicos.add("Wi-Fi");
```

Resultado conceitual:

```text
Wi-Fi
Piscina
```

## Aplicações mais comuns

- categorias únicas;
- permissões;
- tags;
- valores que não devem se repetir.

---

# 11. `Map`

Um `Map` trabalha com pares:

```text
chave → valor
```

Exemplo:

```java
Map<Integer, Quarto> quartos =
    new HashMap<>();

quartos.put(101, q1);
```

Busca:

```java
Quarto quarto =
    quartos.get(101);
```

## Aplicações mais comuns

```text
número do quarto → Quarto
CPF → Hospede
código → Produto
```

---

# 12. Escolhendo uma Collection

| Necessidade | Estrutura |
|---|---|
| Sequência de elementos | `List` |
| Elementos únicos | `Set` |
| Busca por chave | `Map` |

---

# 13. Generics

## Conceito

Generics permitem parametrizar tipos.

```java
List<Quarto>
```

significa:

> Esta lista trabalha com objetos do tipo `Quarto`.

Sem Generics:

```java
List lista =
    new ArrayList();

lista.add(q1);
lista.add("Texto");
lista.add(10);
```

Com Generics:

```java
List<Quarto> quartos =
    new ArrayList<>();
```

Agora:

```java
quartos.add("Texto");
```

gera erro de compilação.

## Vantagens

- segurança de tipos;
- erros detectados em compilação;
- menos casts;
- reutilização;
- código mais claro.

---

# 14. Classe genérica

```java
public class Repositorio<T> {

    private List<T> itens =
        new ArrayList<>();

    public void adicionar(T item) {
        itens.add(item);
    }

    public List<T> listar() {
        return itens;
    }
}
```

Uso:

```java
Repositorio<Quarto> quartos =
    new Repositorio<>();

Repositorio<Hospede> hospedes =
    new Repositorio<>();
```

A mesma classe pode trabalhar com tipos diferentes.

---

# 15. Método genérico

```java
public static <T>
        void imprimir(T objeto) {

    System.out.println(objeto);
}
```

Uso:

```java
imprimir(q1);
imprimir("Hotel");
imprimir(100);
```

---

# 16. Enum

## Conceito

Um `enum` representa um conjunto fechado de valores conhecidos.

```java
public enum Disponibilidade {

    DISPONIVEL,
    OCUPADO,
    MANUTENCAO
}
```

Com `String`:

```java
String status = "DISPONIVEL";
```

alguém poderia escrever:

```text
DISP
Disponivel
DISPONIVELLL
```

Com enum:

```java
Disponibilidade.DISPONIVEL
```

o conjunto de valores é controlado pelo compilador.

## Aplicações mais comuns

- status;
- categorias;
- tipos;
- níveis;
- estados;
- opções fechadas.

---

# 17. Enum com atributos

```java
public enum TipoQuarto {

    SIMPLES(1),
    DUPLO(2),
    COBERTURA(4);

    private final int capacidade;

    TipoQuarto(int capacidade) {
        this.capacidade = capacidade;
    }

    public int getCapacidade() {
        return capacidade;
    }
}
```

Uso:

```java
int capacidade =
    TipoQuarto.DUPLO
              .getCapacidade();
```

---

# 18. Funções Lambda

## Conceito

Uma expressão lambda é uma forma compacta de representar um comportamento.

```java
(a, b) -> a + b
```

Ela pode ser utilizada quando Java espera uma **interface funcional**.

---

# 19. Interface funcional

Uma interface funcional possui um único método abstrato.

```java
public interface Calculadora {

    double calcular(
        double a,
        double b
    );
}
```

Com lambda:

```java
Calculadora soma =
    (a, b) -> a + b;
```

Interfaces funcionais comuns:

```text
Predicate<T>
Function<T, R>
Consumer<T>
Comparator<T>
```

---

# 20. `Predicate<T>`

Representa uma condição.

```text
T → boolean
```

Método:

```java
test()
```

Exemplo:

```java
Predicate<Quarto> disponivel =
    quarto ->
        quarto.getDisponibilidade()
        == Disponibilidade.DISPONIVEL;
```

Teste:

```java
boolean resultado =
    disponivel.test(q1);
```

## Aplicações mais comuns

- filtros;
- validações;
- buscas;
- regras booleanas;
- seleção de elementos.

---

# 21. Composição de Predicate

```java
Predicate<Quarto> disponivel =
    q ->
        q.getDisponibilidade()
        == Disponibilidade.DISPONIVEL;

Predicate<Quarto> barato =
    q ->
        q.getValorDiaria()
        <= 300;
```

Combinação:

```java
Predicate<Quarto> criterio =
    disponivel.and(barato);
```

Também existem:

```java
.or(...)
```

e:

```java
.negate()
```

---

# 22. `Function<T, R>`

Representa uma transformação.

```text
T → R
```

Método:

```java
apply()
```

Exemplo:

```java
Function<Quarto, String> descricao =
    quarto ->
        "Quarto "
        + quarto.getNumero();
```

Uso:

```java
String texto =
    descricao.apply(q1);
```

## Aplicações mais comuns

- transformar objeto em texto;
- extrair atributos;
- converter tipos;
- calcular valores;
- gerar dados para relatórios.

---

# 23. `Consumer<T>`

Representa uma ação que recebe um objeto e não retorna resultado.

```java
Consumer<Quarto> imprimir =
    quarto ->
        System.out.println(quarto);
```

Método:

```java
accept()
```

---

# 24. `Comparator<T>`

Representa uma regra de comparação.

```java
Comparator<Quarto> porPreco =
    (q1, q2) ->
        Double.compare(
            q1.getValorDiaria(),
            q2.getValorDiaria()
        );
```

Uso:

```java
quartos.sort(porPreco);
```

---

# 25. Streams

## Conceito

Stream é uma forma de processar sequências de elementos através de uma cadeia de operações.

```java
quartos.stream()
```

Importante:

```text
Collection
→ armazena dados

Stream
→ processa dados
```

---

# 26. Pipeline de Stream

```text
Fonte
↓
Operações intermediárias
↓
Operação terminal
```

Exemplo:

```java
quartos.stream()
       .filter(...)
       .sorted(...)
       .forEach(...);
```

Operações intermediárias comuns:

```text
filter
map
sorted
distinct
limit
skip
```

Operações terminais comuns:

```text
forEach
toList
count
min
max
findFirst
anyMatch
allMatch
```

---

# 27. `filter`

Seleciona elementos.

```java
List<Quarto> disponiveis =
    quartos.stream()
        .filter(
            quarto ->
                quarto.getDisponibilidade()
                == Disponibilidade.DISPONIVEL
        )
        .toList();
```

O `filter()` utiliza conceitualmente:

```java
Predicate<T>
```

---

# 28. `map`

Transforma elementos.

```java
List<Integer> numeros =
    quartos.stream()
        .map(
            quarto ->
                quarto.getNumero()
        )
        .toList();
```

Antes:

```text
Stream<Quarto>
```

Depois:

```text
Stream<Integer>
```

O `map()` utiliza conceitualmente:

```java
Function<T, R>
```

---

# 29. Method Reference

Quando uma lambda apenas chama um método:

```java
quarto ->
    quarto.getNumero()
```

podemos escrever:

```java
Quarto::getNumero
```

Exemplo:

```java
List<Integer> numeros =
    quartos.stream()
        .map(
            Quarto::getNumero
        )
        .toList();
```

---

# 30. `sorted`

Ordena elementos.

```java
List<Quarto> ordenados =
    quartos.stream()
        .sorted(
            Comparator.comparingDouble(
                Quarto::getValorDiaria
            )
        )
        .toList();
```

---

# 31. Combinando operações

Queremos:

> quartos disponíveis com diária de até R$ 300, ordenados pelo preço.

```java
List<Quarto> resultado =
    quartos.stream()
        .filter(
            q ->
                q.getDisponibilidade()
                == Disponibilidade.DISPONIVEL
        )
        .filter(
            q ->
                q.getValorDiaria()
                <= 300
        )
        .sorted(
            Comparator.comparingDouble(
                Quarto::getValorDiaria
            )
        )
        .toList();
```

Leitura:

```text
pegue os quartos
↓
mantenha disponíveis
↓
mantenha valor <= 300
↓
ordene pelo preço
↓
produza uma lista
```

---

# 32. Outras operações úteis

## `count`

```java
long quantidade =
    quartos.stream()
        .filter(
            q ->
                q.getDisponibilidade()
                == Disponibilidade.DISPONIVEL
        )
        .count();
```

## `anyMatch`

```java
boolean existeCobertura =
    quartos.stream()
        .anyMatch(
            q ->
                q.getTipo()
                == TipoQuarto.COBERTURA
        );
```

## `allMatch`

```java
boolean todosComPrecoValido =
    quartos.stream()
        .allMatch(
            q ->
                q.getValorDiaria() > 0
        );
```

## `min`

```java
Optional<Quarto> maisBarato =
    quartos.stream()
        .min(
            Comparator.comparingDouble(
                Quarto::getValorDiaria
            )
        );
```

---

# 33. `Optional`

Algumas operações podem não encontrar resultado.

Por isso:

```java
findFirst()
min()
max()
```

podem retornar:

```java
Optional<T>
```

Exemplo:

```java
quartos.stream()
    .filter(...)
    .findFirst()
    .ifPresent(
        System.out::println
    );
```

---

# 34. Stream versus `for`

Forma tradicional:

```java
List<Quarto> resultado =
    new ArrayList<>();

for (Quarto quarto : quartos) {

    if (
        quarto.getValorDiaria()
        <= 300
    ) {

        resultado.add(quarto);
    }
}
```

Com Stream:

```java
List<Quarto> resultado =
    quartos.stream()
        .filter(
            q ->
                q.getValorDiaria()
                <= 300
        )
        .toList();
```

Streams não eliminam a necessidade de conhecer `for`.

Eles oferecem outra maneira de expressar o processamento.

---

# 35. Relação entre todos os conceitos

```text
Classe abstrata
→ organiza uma hierarquia

Interface
→ define capacidades

Sobrescrita
→ especializa comportamentos

Collections
→ armazenam objetos

Generics
→ controlam os tipos

Enum
→ representa valores fechados

Lambda
→ representa comportamento

Predicate
→ representa condições

Function
→ representa transformações

Comparator
→ representa comparação

Stream
→ combina essas operações
```

---

# 36. Exemplo integrado

Queremos:

> localizar quartos disponíveis, do tipo DUPLO, com diária de até R$ 300, ordenados pelo preço, e produzir uma lista apenas com seus números.

```java
List<Integer> numeros =
    quartos.stream()
        .filter(
            q ->
                q.getDisponibilidade()
                == Disponibilidade.DISPONIVEL
        )
        .filter(
            q ->
                q.getTipo()
                == TipoQuarto.DUPLO
        )
        .filter(
            q ->
                q.getValorDiaria()
                <= 300
        )
        .sorted(
            Comparator.comparingDouble(
                Quarto::getValorDiaria
            )
        )
        .map(
            Quarto::getNumero
        )
        .toList();
```

Nesse trecho aparecem:

```text
List
Generics
Enum
Lambda
Predicate
Comparator
Function
Stream
```

---

# 37. Erros conceituais comuns

- Classe abstrata pode possuir métodos concretos.
- Interface não deve ser vista apenas como “classe abstrata diferente”.
- Sobrecarga não depende de herança.
- Sobrescrita depende de um método herdado.
- `List`, `Set` e `Map` atendem necessidades diferentes.
- Generics não servem apenas para Collections.
- Lambda representa comportamento associado a uma interface funcional.
- Stream não armazena dados.
- `filter()` seleciona.
- `map()` transforma.

---

# 38. Quadro de revisão rápida

| Conceito | Pergunta principal |
|---|---|
| Classe abstrata | O conceito faz sentido ser instanciado sozinho? |
| Método abstrato | Todas as subclasses precisam definir esse comportamento? |
| `final` | Quero impedir alteração/herança? |
| Interface | Que capacidade/contrato quero representar? |
| Sobrecarga | Preciso de versões diferentes da mesma operação? |
| Sobrescrita | A subclasse precisa redefinir um comportamento? |
| `List` | Preciso de sequência? |
| `Set` | Preciso evitar duplicidade? |
| `Map` | Preciso buscar por chave? |
| Generics | Qual tipo essa estrutura manipula? |
| Enum | Existe um conjunto fechado de valores? |
| Lambda | Quero fornecer um comportamento? |
| Predicate | Quero testar uma condição? |
| Function | Quero transformar um valor? |
| Comparator | Quero definir uma ordem? |
| Stream | Quero montar um pipeline de processamento? |

---

# 39. Questões de autoavaliação

1. Quando uma classe deve ser abstrata?
2. Uma classe abstrata pode possuir construtor?
3. Uma classe abstrata pode possuir métodos concretos?
4. Qual a diferença entre `abstract` e `final`?
5. Quando uma interface é preferível a uma classe abstrata?
6. Qual a diferença entre sobrecarga e sobrescrita?
7. Por que utilizar `@Override`?
8. Quando escolher `List`, `Set` ou `Map`?
9. Qual problema Generics resolve?
10. O que significa `T` em uma classe genérica?
11. Quando um `enum` é melhor que uma `String`?
12. O que é uma interface funcional?
13. Qual é o método de `Predicate<T>`?
14. Qual é o método de `Function<T,R>`?
15. O que representam `T` e `R`?
16. Qual a diferença entre `filter()` e `map()`?
17. O que faz `sorted()`?
18. Qual a diferença entre operação intermediária e terminal?
19. O que é `Optional`?
20. Uma Stream altera automaticamente a lista original?

---

# 40. Síntese final

Uma possível progressão dos conteúdos é:

```text
Abstração
    ↓
Herança e contratos
    ↓
Polimorfismo
    ↓
Collections
    ↓
Generics
    ↓
Enum
    ↓
Interfaces funcionais
    ↓
Lambda
    ↓
Predicate / Function / Comparator
    ↓
Streams
```

A ideia principal é perceber que Java oferece diferentes mecanismos para separar:

```text
dados
+
estrutura
+
comportamento
+
regras
+
processamento
```

e combiná-los na construção de aplicações organizadas e reutilizáveis.
