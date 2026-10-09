# Atividade Prática — Factory Method e Strategy

## Contexto

Uma loja virtual precisa processar pedidos e calcular o valor do frete.

O sistema possui diferentes formas de entrega:

- **Entrega Normal**
- **Entrega Expressa**
- **Retirada na Loja**

Cada forma de entrega possui uma regra diferente para o cálculo do frete.

Além disso, o sistema pode gerar diferentes tipos de comprovante após a finalização do pedido:

- **Comprovante em Texto**
- **Comprovante em HTML**

O objetivo da atividade é utilizar os padrões **Strategy** e **Factory Method** para organizar essas responsabilidades.

---

## Parte 1 — Strategy: cálculo de frete

Implemente o padrão **Strategy** para representar as diferentes formas de cálculo de frete.

Considere a seguinte classe:

```java
public class Pedido {

    private double valor;
    private double peso;

    public Pedido(double valor, double peso) {
        this.valor = valor;
        this.peso = peso;
    }

    public double getValor() {
        return valor;
    }

    public double getPeso() {
        return peso;
    }
}
```

As regras de frete são:

| Tipo | Regra |
|---|---|
| Normal | peso × R$ 5,00 |
| Expressa | peso × R$ 9,00 + R$ 15,00 |
| Retirada | R$ 0,00 |

Crie:

```text
FreteStrategy
FreteNormal
FreteExpresso
FreteRetirada
CalculadoraFrete
```

A interface `FreteStrategy` deve possuir:

```java
double calcular(Pedido pedido);
```

A classe `CalculadoraFrete` deve representar o **Context** do padrão Strategy.

Ela deve receber uma estratégia e delegar o cálculo para ela.

Exemplo esperado:

```java
FreteStrategy estrategia = new FreteNormal();

CalculadoraFrete calculadora =
        new CalculadoraFrete(estrategia);

double frete =
        calculadora.calcular(pedido);
```

---

## Parte 2 — Factory Method: criação de comprovantes

Após finalizar um pedido, o sistema deve gerar um comprovante.

Existem inicialmente dois formatos:

```text
Texto
HTML
```

Crie uma interface:

```java
public interface Comprovante {

    void gerar(Pedido pedido, double frete);
}
```

Implemente dois produtos concretos:

```text
ComprovanteTexto
ComprovanteHTML
```

Cada implementação deve apresentar pelo menos:

- valor do pedido;
- valor do frete;
- valor total.

Exemplo de saída para `ComprovanteTexto`:

```text
PEDIDO FINALIZADO

Valor do pedido: R$ 200.00
Frete: R$ 25.00
Total: R$ 225.00
```

Para `ComprovanteHTML`, a saída pode ser:

```html
<h1>Pedido Finalizado</h1>
<p>Valor do pedido: R$ 200.00</p>
<p>Frete: R$ 25.00</p>
<p>Total: R$ 225.00</p>
```

---

## Aplicando Factory Method

Crie a classe abstrata:

```text
ComprovanteFactory
```

Ela deve declarar o Factory Method:

```java
public abstract Comprovante criarComprovante();
```

Depois, crie:

```text
ComprovanteTextoFactory
ComprovanteHTMLFactory
```

Cada Factory deve criar seu respectivo produto.

Exemplo:

```java
public class ComprovanteTextoFactory
        extends ComprovanteFactory {

    @Override
    public Comprovante criarComprovante() {
        return new ComprovanteTexto();
    }
}
```

---

## Parte 3 — Integração dos padrões

Agora integre as duas soluções.

Crie um pedido:

```java
Pedido pedido =
        new Pedido(200.0, 5.0);
```

Escolha uma Strategy:

```java
FreteStrategy estrategia =
        new FreteExpresso();
```

Calcule o frete:

```java
CalculadoraFrete calculadora =
        new CalculadoraFrete(estrategia);

double frete =
        calculadora.calcular(pedido);
```

Depois, escolha uma Factory:

```java
ComprovanteFactory factory =
        new ComprovanteTextoFactory();
```

Crie o comprovante:

```java
Comprovante comprovante =
        factory.criarComprovante();
```

E gere a saída:

```java
comprovante.gerar(pedido, frete);
```

---

## Parte 4 — Classe Main

A classe `Main` deve demonstrar pelo menos os seguintes cenários.

### Cenário 1

```text
Frete: Normal
Comprovante: Texto
```

### Cenário 2

```text
Frete: Expresso
Comprovante: HTML
```

### Cenário 3

```text
Frete: Retirada
Comprovante: Texto
```

O resultado deve mostrar que é possível trocar:

```text
a estratégia de frete
```

e:

```text
o tipo de comprovante
```

sem alterar as classes responsáveis pelas regras já implementadas.

---

## Parte 5 — Extensão

Após implementar o sistema inicial, adicione:

### Nova Strategy

Crie:

```text
FreteEconomico
```

Regra:

```text
peso × R$ 3,00
```

Ela deve implementar:

```java
FreteStrategy
```

### Novo produto do Factory Method

Crie:

```text
ComprovanteJSON
```

A saída pode seguir o formato:

```json
{
    "valorPedido": 200.0,
    "frete": 15.0,
    "total": 215.0
}
```

Crie também:

```text
ComprovanteJSONFactory
```

---

## Parte 6 — Identificação dos elementos dos padrões

Ao final do código, responda:

### Strategy

1. Qual classe representa a **Strategy**?
2. Quais classes representam as **ConcreteStrategies**?
3. Qual classe representa o **Context**?
4. Em qual ponto do código a Strategy é escolhida?
5. Qual vantagem existe ao adicionar `FreteEconomico` dessa forma?

### Factory Method

6. Qual classe representa o **Product**?
7. Quais classes representam os **ConcreteProducts**?
8. Qual classe representa o **Creator**?
9. Quais classes representam os **ConcreteCreators**?
10. Qual método representa o **Factory Method**?
11. Qual vantagem existe ao adicionar `ComprovanteJSON` dessa forma?

---

## Estrutura esperada

Ao final, o projeto deverá possuir aproximadamente:

```text
src/
│
├── Pedido.java
│
├── Main.java
│
├── FreteStrategy.java
├── FreteNormal.java
├── FreteExpresso.java
├── FreteRetirada.java
├── FreteEconomico.java
├── CalculadoraFrete.java
│
├── Comprovante.java
├── ComprovanteTexto.java
├── ComprovanteHTML.java
├── ComprovanteJSON.java
│
├── ComprovanteFactory.java
├── ComprovanteTextoFactory.java
├── ComprovanteHTMLFactory.java
└── ComprovanteJSONFactory.java
```

---

## Resultado esperado da atividade

Ao final da atividade, o aluno deverá perceber que os dois padrões resolvem problemas diferentes.

| Padrão | Problema resolvido |
|---|---|
| **Strategy** | Permite trocar o algoritmo utilizado |
| **Factory Method** | Permite delegar a criação de objetos |

No sistema desenvolvido:

```text
Strategy
    ↓
Como calcular o frete?

Factory Method
    ↓
Qual tipo de comprovante criar?
```

O **Strategy** organiza diferentes comportamentos.

O **Factory Method** organiza a criação de diferentes objetos.
