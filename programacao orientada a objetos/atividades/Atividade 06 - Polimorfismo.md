# Atividade — Polimorfismo em Java

---

## Exercício 1 — Animais e sons

**Nível:** introdutório  
**Conceitos:** herança, sobrescrita de métodos.

Crie uma classe `Animal` com o método:

```java
void emitirSom()
```

Depois, crie as classes:

```java
Cachorro
Gato
Vaca
```

Cada classe deve sobrescrever o método `emitirSom()` com uma mensagem diferente.

No `main`, crie um objeto de cada classe e chame o método `emitirSom()`.

**Objetivo do exercício:** perceber que classes diferentes podem ter métodos com o mesmo nome, mas comportamentos diferentes.

---

## Exercício 2 — Vetor de animais

**Nível:** introdutório  
**Conceitos:** polimorfismo com vetor de objetos.

Usando as classes do exercício anterior, crie um vetor do tipo `Animal`:

```java
Animal[] animais = new Animal[3];
```

Armazene nesse vetor objetos de `Cachorro`, `Gato` e `Vaca`.

Depois, percorra o vetor com um laço `for` e chame:

```java
animais[i].emitirSom();
```

**Objetivo do exercício:** entender que uma variável do tipo `Animal` pode referenciar objetos de subclasses diferentes.

---

## Exercício 3 — Formas geométricas

**Nível:** básico/intermediário  
**Conceitos:** classe abstrata, método abstrato, polimorfismo.

Crie uma classe abstrata `FormaGeometrica` com o método abstrato:

```java
double calcularArea();
```

Depois, crie as classes:

```java
Retangulo
Circulo
Triangulo
```

Cada classe deve implementar o cálculo de área correspondente.

No `main`, crie um vetor de `FormaGeometrica` e armazene diferentes formas.

Depois, percorra o vetor e exiba a área de cada uma.

**Regras:**

- `Retangulo`: base × altura;
- `Circulo`: π × raio²;
- `Triangulo`: base × altura / 2.

**Objetivo do exercício:** praticar o uso de uma classe abstrata como tipo comum para diferentes objetos.

---

