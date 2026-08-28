# Atividade — Predicate e Function em Java

## Contexto

Utilize como base o projeto **SistemaHotel** desenvolvido em aula.

O projeto já possui as classes e enums:

```text
Hotel
Quarto
Tipo
Disponibilidade
```

Considere também os quartos cadastrados no `Main`:

```java
Quarto q1 = new Quarto(
    101,
    180.0,
    Tipo.SIMPLES,
    Disponibilidade.DISPONIVEL
);

Quarto q2 = new Quarto(
    102,
    110.0,
    Tipo.DUPLO,
    Disponibilidade.OCUPADO
);

Quarto q3 = new Quarto(
    103,
    500.0,
    Tipo.COBERTURA,
    Disponibilidade.DISPONIVEL
);

Hotel hotel = new Hotel();

hotel.adicionarQuarto(q1);
hotel.adicionarQuarto(q2);
hotel.adicionarQuarto(q3);
```

Para os exercícios, serão utilizadas principalmente as interfaces funcionais:

```java
import java.util.function.Predicate;
import java.util.function.Function;
```

---

# Parte A — Predicate

## Exercício 1 — Identificando quartos disponíveis

Crie um:

```java
Predicate<Quarto>
```

chamado:

```java
estaDisponivel
```

O predicado deve retornar `true` quando:

```java
quarto.getDisponibilidade()
```

for igual a:

```java
Disponibilidade.DISPONIVEL
```

Teste o predicado com `q1`, `q2` e `q3` utilizando:

```java
estaDisponivel.test(...)
```

### Resultado esperado

```text
q1 → true
q2 → false
q3 → true
```

---

## Exercício 2 — Quartos com diária barata

Crie um:

```java
Predicate<Quarto>
```

chamado:

```java
diariaBarata
```

Considere um quarto barato quando sua diária for inferior a:

```text
R$ 200,00
```

Teste o predicado com os três quartos existentes.

### Resultado esperado

```text
Quarto 101 → true
Quarto 102 → true
Quarto 103 → false
```

---

## Exercício 3 — Utilizando um Predicate em uma Collection

Utilizando o `Predicate<Quarto>` criado no Exercício 1, percorra:

```java
hotel.getQuartos()
```

com um `for`.

Dentro do `for`, utilize:

```java
estaDisponivel.test(quarto)
```

para imprimir somente os quartos disponíveis.

Não escreva novamente a condição:

```java
quarto.getDisponibilidade()
    == Disponibilidade.DISPONIVEL
```

A condição deve estar encapsulada no `Predicate`.

### Resultado esperado

Devem ser exibidos apenas:

```text
Quarto 101
Quarto 103
```

---

## Exercício 4 — Combinando Predicates

Crie os dois predicados:

```java
Predicate<Quarto> estaDisponivel
Predicate<Quarto> diariaBarata
```

Depois combine-os utilizando:

```java
.and(...)
```

Crie:

```java
Predicate<Quarto> disponivelEBarato
```

O novo predicado deve aceitar apenas quartos que sejam simultaneamente:

- disponíveis;
- abaixo de R$ 200,00.

Teste-o com os quartos do hotel.

### Resultado esperado

Somente o quarto:

```text
101
```

deve satisfazer as duas condições.

### Depois

Experimente também:

```java
.or(...)
```

para identificar quartos que:

> estejam disponíveis **OU** possuam diária inferior a R$ 200,00.

Compare os resultados.

---

# Parte B — Function

## Exercício 5 — Transformando Quarto em número

Crie uma:

```java
Function<Quarto, Integer>
```

chamada:

```java
obterNumero
```

Ela deve receber um `Quarto` e retornar:

```java
quarto.getNumero()
```

Teste utilizando:

```java
obterNumero.apply(q1)
```

e os demais quartos.

### Resultado esperado

```text
101
102
103
```

---

## Exercício 6 — Transformando Quarto em valor da diária

Crie:

```java
Function<Quarto, Double> obterValorDiaria
```

A função deve receber um quarto e retornar o valor de sua diária.

Depois percorra:

```java
hotel.getQuartos()
```

e utilize:

```java
obterValorDiaria.apply(quarto)
```

para imprimir somente os valores das diárias.

### Resultado esperado

```text
180.0
110.0
500.0
```

---

## Exercício 7 — Criando uma descrição para o quarto

Crie:

```java
Function<Quarto, String> descricaoQuarto
```

A função deve transformar um objeto `Quarto` em uma `String` no seguinte formato:

```text
Quarto 101 - Diária: R$ 180.0
```

Utilize:

- `getNumero()`;
- `getValorDiaria()`.

A função **não deve imprimir** diretamente.

Ela deve apenas retornar a `String`.

Depois utilize:

```java
System.out.println(
    descricaoQuarto.apply(quarto)
);
```

para apresentar os dados.

---

## Exercício 8 — Aplicando cálculo com Function

Crie:

```java
Function<Quarto, Double> valorTresDiarias
```

A função deve receber um `Quarto` e calcular quanto custariam:

```text
3 diárias
```

naquele quarto.

Exemplo:

```text
Quarto 101
R$ 180,00 por diária
3 diárias = R$ 540,00
```

Aplique a função aos três quartos.

### Desafio

Altere a função para acrescentar uma taxa de serviço de:

```text
10%
```

ao valor final.

---

# Parte C — Predicate + Function

## Exercício 9 — Filtrar e depois transformar

Crie:

```java
Predicate<Quarto> estaDisponivel
```

e:

```java
Function<Quarto, String> descricaoQuarto
```

Percorra:

```java
hotel.getQuartos()
```

Para cada quarto:

1. teste o quarto com `estaDisponivel`;
2. somente se o resultado for `true`, aplique `descricaoQuarto`;
3. imprima a descrição retornada pela função.

O objetivo é separar claramente:

```text
Predicate
→ decide se o quarto será utilizado

Function
→ transforma o quarto em outro valor
```

---

## Exercício 10 — Método `filtrar` na classe Hotel

Adicione à classe `Hotel` o método:

```java
public List<Quarto> filtrar(
        Predicate<Quarto> criterio)
```

O método deve:

1. criar uma nova `List<Quarto>`;
2. percorrer `this.quartos`;
3. chamar:

```java
criterio.test(quarto)
```

4. adicionar à nova lista apenas os quartos aprovados;
5. retornar a lista criada.

Depois utilize o mesmo método para realizar **três consultas diferentes**.

### Consulta A

Quartos disponíveis:

```java
hotel.filtrar(
    quarto -> ...
);
```

### Consulta B

Quartos abaixo de R$ 300,00.

### Consulta C

Quartos com diária acima de R$ 150,00.

### Questão

Explique por que não foi necessário criar:

```text
buscarDisponiveis()
buscarBaratos()
buscarCaros()
```

como três métodos diferentes.

---

## Exercício 11 — Método genérico `transformar`

Adicione à classe `Hotel` um método genérico:

```java
public <R> List<R> transformar(
        Function<Quarto, R> funcao)
```

O método deve:

1. criar uma:

```java
List<R>
```

2. percorrer todos os quartos;
3. aplicar:

```java
funcao.apply(quarto)
```

4. adicionar o resultado à nova lista;
5. retornar a lista.

Utilize esse método para produzir:

### A. Uma lista de números

O resultado deverá ser:

```java
List<Integer>
```

com:

```text
101
102
103
```

### B. Uma lista de valores

O resultado deverá ser:

```java
List<Double>
```

contendo os valores das diárias.

### C. Uma lista de descrições

O resultado deverá ser:

```java
List<String>
```

contendo descrições dos quartos.

### Questão

Explique o papel de:

```java
<R>
```

no método:

```java
public <R> List<R> transformar(...)
```

---

## Exercício 12 — Consulta reutilizável completa

Implemente na classe `Hotel` os métodos desenvolvidos anteriormente:

```java
public List<Quarto> filtrar(
        Predicate<Quarto> criterio)
```

e:

```java
public <R> List<R> transformar(
        Function<Quarto, R> funcao)
```

Depois resolva o seguinte problema:

> O hotel deseja apresentar ao cliente somente os quartos disponíveis com diária de até R$ 300,00. Para cada quarto encontrado, deve ser exibida uma mensagem contendo seu número e valor.

### Etapa 1

Crie:

```java
Predicate<Quarto> disponivel
```

### Etapa 2

Crie:

```java
Predicate<Quarto> ate300
```

### Etapa 3

Combine-os:

```java
Predicate<Quarto> criterio =
    disponivel.and(ate300);
```

### Etapa 4

Utilize:

```java
hotel.filtrar(criterio)
```

para obter os quartos.

### Etapa 5

Crie:

```java
Function<Quarto, String> formatar
```

que produza mensagens como:

```text
Quarto 101 disponível por R$ 180.0
```

### Etapa 6

Aplique a função aos resultados encontrados.

### Resultado esperado com os dados atuais

```text
Quarto 101 disponível por R$ 180.0
```
