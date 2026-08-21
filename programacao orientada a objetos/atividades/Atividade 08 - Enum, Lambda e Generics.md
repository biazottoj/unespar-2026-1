# Lista de Exercícios — Sobrecarga, Sobrescrita, Collections, Generics, Enum e Lambdas

## Parte A — Sobrecarga e Sobrescrita

### Exercício 1

Crie uma classe `Hospede` com:

- nome;
- CPF.

Sobrescreva `toString()` para apresentar os dados do hóspede.

### Exercício 2

Crie dois construtores para `Hospede`:

```java
Hospede(String nome, String cpf)
```

e:

```java
Hospede(String nome)
```

Explique qual conceito está sendo utilizado.

### Exercício 3

Crie uma classe `ServicoHotel` com:

```java
double calcularPreco()
```

Crie uma subclasse `CafeDaManha` e sobrescreva esse método.

### Exercício 4

Crie:

```java
class Pagamento
```

com o método:

```java
void processar()
```

Crie `PagamentoCartao` e sobrescreva `processar()`.

### Exercício 5

Analise:

```java
public void reservar(int quarto) {
}

public void reservar(int quarto, int dias) {
}
```

Identifique o conceito utilizado e explique.

### Exercício 6

Analise:

```java
class Pessoa {

    void identificar() {
        System.out.println("Pessoa");
    }
}

class Hospede extends Pessoa {

    @Override
    void identificar() {
        System.out.println("Hóspede");
    }
}
```

Identifique o conceito utilizado.

### Exercício 7

Crie três versões sobrecarregadas de:

```java
buscarQuarto(...)
```

utilizando diferentes parâmetros.

### Exercício 8

Crie um exemplo no contexto de hotel que utilize simultaneamente:

- herança;
- sobrescrita;
- sobrecarga.

---

## Parte B — Collections

### Exercício 9

Crie uma:

```java
List<String>
```

contendo nomes de cinco hóspedes.

Percorra-a utilizando `for`.

### Exercício 10

Crie:

```java
List<Quarto>
```

com cinco quartos.

Exiba todos os elementos.

### Exercício 11

Adicione três quartos a uma lista e depois remova um deles.

Apresente a lista antes e depois.

### Exercício 12

Crie uma lista de quartos e calcule manualmente a média do valor das diárias.

### Exercício 13

Crie:

```java
Set<String> servicos
```

e adicione:

```text
Wi-Fi
Piscina
Academia
Wi-Fi
```

Explique o resultado.

### Exercício 14

Crie:

```java
Map<Integer, String>
```

associando números de quartos aos nomes dos hóspedes.

### Exercício 15

Crie:

```java
Map<Integer, Quarto>
```

e implemente uma busca pelo número do quarto.

---

## Parte C — Generics

### Exercício 16

Explique a diferença entre:

```java
List lista
```

e:

```java
List<Quarto> lista
```


## Parte D — Enum

### Exercício 17

Crie:

```java
enum StatusReserva
```

contendo:

```text
PENDENTE
CONFIRMADA
CANCELADA
FINALIZADA
```

### Exercício 18

Adicione `StatusReserva` à classe `Reserva` e atualize seu `toString()` para exibir o status.

### Exercício 19

Crie:

```java
enum FormaPagamento
```

contendo:

```text
DINHEIRO
PIX
CARTAO_CREDITO
CARTAO_DEBITO
```

### Exercício 20

Crie um enum:

```java
CategoriaHospede
```

com:

```text
NORMAL
VIP
PREMIUM
```

Cada categoria deve armazenar um percentual de desconto.

---

## Parte E — Comparator

### Exercício 21

Crie:

```java
ComparadorPorNumero
```

implementando:

```java
Comparator<Quarto>
```

Ordene os quartos pelo número.

### Exercício 22

Crie:

```java
ComparadorPorPreco
```

e ordene os quartos da diária mais barata para a mais cara.

### Exercício 23

Modifique o Comparator anterior para ordenar do preço mais alto para o mais baixo.

### Exercício 24

Explique o significado de cada retorno:

```text
compare(q1, q2) < 0
compare(q1, q2) == 0
compare(q1, q2) > 0
```

Explique também a diferença de responsabilidade entre `sort()` e `Comparator`.

---

## Parte F — Funções Lambda


### Exercício 25

Ordene os quartos pelo número utilizando uma lambda.
