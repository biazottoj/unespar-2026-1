# Lista de 40 exercícios em Java

## Orientações gerais

Esta lista foi organizada de forma progressiva, começando por sintaxe básica e avançando até classes, encapsulamento, herança e polimorfismo. Os exercícios não precisam ser resolvidos todos em uma única aula. A ideia é que cada bloco reforce conceitos anteriores e introduza novos desafios.

---

## 1. Saída simples no console

**Conceitos:** `main`, `System.out.println`, estrutura básica de um programa Java.

Crie um programa em Java que exiba no console:

```text
Olá, mundo!
Meu primeiro programa em Java.
```

---

## 2. Exibição de dados pessoais

**Conceitos:** variáveis, tipos primitivos, saída formatada.

Crie um programa que armazene em variáveis:

- nome;
- idade;
- altura;
- cidade.

Depois, exiba uma mensagem organizada no console com essas informações.

---

## 3. Cálculo de média simples

**Conceitos:** variáveis numéricas, operadores aritméticos.

Crie um programa que armazene três notas de um aluno e calcule a média aritmética.

Ao final, exiba:

```text
A média do aluno é: X
```

---

## 4. Conversão de temperatura

**Conceitos:** operadores aritméticos, uso de `double`.

Crie um programa que receba uma temperatura em Celsius e converta para Fahrenheit usando a fórmula:

```text
F = C * 1.8 + 32
```

---

## 5. Cálculo de área de figuras

**Conceitos:** variáveis, operadores, organização de cálculos.

Crie um programa que calcule:

- área de um retângulo;
- área de um triângulo;
- área de um círculo.

Use valores fixos nas variáveis e exiba os três resultados.

---

## 6. Leitura de dados com Scanner

**Conceitos:** entrada de dados, `Scanner`.

Crie um programa que solicite ao usuário:

- nome;
- idade;
- curso.

Depois, exiba uma mensagem como:

```text
Olá, Ana! Você tem 20 anos e está matriculada no curso de Engenharia de Software.
```

---

## 7. Calculadora de soma e subtração

**Conceitos:** entrada de dados, operadores aritméticos.

Crie um programa que leia dois números inteiros e exiba:

- soma;
- subtração;
- multiplicação;
- divisão.

---

## 8. Cálculo de salário

**Conceitos:** entrada de dados, `double`, operações matemáticas.

Crie um programa que leia:

- valor da hora trabalhada;
- quantidade de horas trabalhadas no mês.

Depois, calcule e exiba o salário bruto do funcionário.

---

## 9. Verificação de maioridade

**Conceitos:** estruturas condicionais, `if` e `else`.

Crie um programa que leia a idade de uma pessoa e informe se ela é maior de idade ou menor de idade.

---

## 10. Número positivo, negativo ou zero

**Conceitos:** condicionais encadeadas.

Crie um programa que leia um número inteiro e informe se ele é:

- positivo;
- negativo;
- igual a zero.

---

## 11. Aprovação de aluno

**Conceitos:** condicionais, operadores relacionais.

Crie um programa que leia duas notas de um aluno, calcule a média e informe:

- `Aprovado`, se a média for maior ou igual a 7;
- `Recuperação`, se a média for maior ou igual a 5 e menor que 7;
- `Reprovado`, se a média for menor que 5.

---

## 12. Desconto em compra

**Conceitos:** condicionais, porcentagem.

Crie um programa que leia o valor de uma compra.

Aplique as seguintes regras:

- compras acima de R$ 500,00 recebem 15% de desconto;
- compras entre R$ 200,00 e R$ 500,00 recebem 10% de desconto;
- compras abaixo de R$ 200,00 não recebem desconto.

Exiba o valor final da compra.

---

## 13. Menu com switch

**Conceitos:** `switch`, menus simples.

Crie um programa que exiba o seguinte menu:

```text
1 - Cadastrar usuário
2 - Listar usuários
3 - Sair
```

Leia a opção escolhida e exiba uma mensagem correspondente.

---

## 14. Calculadora com switch

**Conceitos:** `switch`, entrada de dados, operadores.

Crie uma calculadora que leia dois números e uma operação:

- `+`
- `-`
- `*`
- `/`

Use `switch` para executar a operação escolhida.

---

## 15. Contagem de 1 até N

**Conceitos:** laço `for`.

Crie um programa que leia um número inteiro positivo `N` e exiba todos os números de 1 até `N`.

---

## 16. Soma de números de 1 até N

**Conceitos:** repetição, acumulador.

Crie um programa que leia um número inteiro positivo `N` e calcule a soma de todos os números de 1 até `N`.

Exemplo:

```text
N = 5
Soma = 15
```

---

## 17. Tabuada

**Conceitos:** `for`, multiplicação, repetição.

Crie um programa que leia um número inteiro e exiba sua tabuada de 1 a 10.

---

## 18. Validação de senha

**Conceitos:** `while`, comparação de Strings.

Crie um programa que solicite uma senha ao usuário.

Enquanto a senha digitada for diferente de `"java123"`, o programa deve solicitar novamente.

Quando a senha correta for digitada, exiba:

```text
Acesso permitido.
```

---

## 19. Cálculo de média com repetição

**Conceitos:** `while`, acumulador, contador.

Crie um programa que leia notas de alunos até que o usuário digite `-1`.

Ao final, exiba:

- quantidade de notas digitadas;
- média das notas.

---

## 20. Identificação do maior número

**Conceitos:** repetição, comparação, variável auxiliar.

Crie um programa que leia 10 números inteiros e informe qual foi o maior número digitado.

---

## 21. Vetor de números inteiros

**Conceitos:** arrays, laço `for`.

Crie um programa que leia 5 números inteiros, armazene-os em um vetor e depois exiba todos os valores na ordem em que foram digitados.

---

## 22. Soma dos elementos de um vetor

**Conceitos:** arrays, acumulador.

Crie um programa que leia 8 números inteiros em um vetor.

Depois, calcule e exiba:

- soma dos elementos;
- média dos elementos.

---

## 23. Contagem de números pares

**Conceitos:** arrays, operador módulo `%`, condicionais.

Crie um programa que leia 10 números inteiros em um vetor e informe quantos deles são pares.

---

## 24. Maior e menor valor em um vetor

**Conceitos:** arrays, comparação, percorrer coleção.

Crie um programa que leia 10 números inteiros em um vetor e informe:

- maior valor;
- menor valor.

---

## 25. Busca em vetor

**Conceitos:** arrays, busca sequencial.

Crie um programa que armazene 10 nomes em um vetor.

Depois, leia um nome informado pelo usuário e verifique se ele está presente no vetor.

---

## 26. Manipulação de Strings

**Conceitos:** `String`, métodos `length`, `toUpperCase`, `toLowerCase`, `contains`.

Crie um programa que leia uma frase e exiba:

- quantidade de caracteres;
- frase em letras maiúsculas;
- frase em letras minúsculas;
- se a frase contém a palavra `"Java"`.

---

## 27. Criação de métodos simples

**Conceitos:** métodos estáticos, reutilização de código.

Crie um programa com os seguintes métodos:

```java
static int somar(int a, int b)
static int subtrair(int a, int b)
static int multiplicar(int a, int b)
static double dividir(int a, int b)
```

No método `main`, leia dois números e use esses métodos para exibir os resultados.

---

## 28. Método para verificar número par

**Conceitos:** métodos com retorno booleano.

Crie um método chamado `ehPar` que receba um número inteiro e retorne `true` se ele for par ou `false` caso contrário.

Use esse método no `main` para verificar vários números digitados pelo usuário.

---

## 29. Método para calcular média

**Conceitos:** métodos, arrays como parâmetro.

Crie um método que receba um vetor de notas e retorne a média.

Depois, no `main`, leia as notas de 5 alunos, armazene em um vetor e use o método para calcular a média geral.

---

## 30. Método para encontrar maior valor

**Conceitos:** métodos, arrays, retorno de valor.

Crie um método chamado `encontrarMaior` que receba um vetor de inteiros e retorne o maior valor presente nele.

---

## 31. Classe Produto

**Conceitos:** criação de classe, atributos, objetos.

Crie uma classe `Produto` com os atributos:

- `nome`;
- `preco`;
- `quantidade`.

No `main`, crie dois produtos, atribua valores aos atributos e exiba as informações de cada um.

---

## 32. Classe Aluno com método de média

**Conceitos:** classe, atributos, métodos de instância.

Crie uma classe `Aluno` com os atributos:

- `nome`;
- `nota1`;
- `nota2`.

Adicione um método chamado `calcularMedia`.

No `main`, crie um aluno, atribua notas e exiba sua média.

---

## 33. Classe ContaBancaria

**Conceitos:** classe, estado de objeto, métodos.

Crie uma classe `ContaBancaria` com os atributos:

- `titular`;
- `saldo`.

Adicione os métodos:

- `depositar(double valor)`;
- `sacar(double valor)`;
- `exibirSaldo()`.

No saque, verifique se há saldo suficiente.

---

## 34. Encapsulamento em Produto

**Conceitos:** `private`, getters, setters, validação.

Refatore a classe `Produto` para que seus atributos sejam privados.

Implemente:

- `getNome`;
- `setNome`;
- `getPreco`;
- `setPreco`;
- `getQuantidade`;
- `setQuantidade`.

Não permita preço ou quantidade negativos.

---

## 35. Encapsulamento em ContaBancaria

**Conceitos:** encapsulamento, proteção de estado.

Refatore a classe `ContaBancaria` para que o saldo não possa ser alterado diretamente.

Regras:

- o saldo só pode mudar por meio de `depositar` e `sacar`;
- não deve ser possível depositar valor negativo;
- não deve ser possível sacar valor maior que o saldo;
- o método `getSaldo` deve apenas retornar o saldo atual.

---

## 36. Sistema simples de cadastro de alunos

**Conceitos:** classes, arrays de objetos, métodos.

Crie uma classe `Aluno` com:

- nome;
- RA;
- média.

Crie um programa que permita cadastrar 5 alunos em um vetor.

Depois, exiba:

- todos os alunos;
- apenas os alunos aprovados;
- a média geral da turma.

Considere aprovado o aluno com média maior ou igual a 7.

---

## 37. Classe Pedido e ItemPedido

**Conceitos:** composição simples entre objetos.

Crie uma classe `ItemPedido` com:

- nome do produto;
- quantidade;
- preço unitário.

Crie uma classe `Pedido` com:

- nome do cliente;
- vetor de itens.

A classe `Pedido` deve ter um método para calcular o valor total da compra.

---

## 38. Herança com Pessoa, Aluno e Professor

**Conceitos:** herança, reutilização de atributos e métodos.

Crie uma classe `Pessoa` com:

- nome;
- idade.

Crie as classes `Aluno` e `Professor` herdando de `Pessoa`.

A classe `Aluno` deve ter:

- RA;
- curso.

A classe `Professor` deve ter:

- matrícula;
- disciplina.

Crie objetos das duas classes e exiba suas informações.

---

## 39. Herança com Funcionário

**Conceitos:** herança, sobrescrita de métodos.

Crie uma classe `Funcionario` com:

- nome;
- salário base;
- método `calcularSalario()`.

Crie duas subclasses:

- `FuncionarioComum`;
- `Gerente`.

O gerente deve receber um bônus de 20% sobre o salário base.

No `main`, crie um funcionário comum e um gerente, e exiba o salário calculado de cada um.

---

## 40. Sistema de pagamentos com polimorfismo

**Conceitos:** herança, sobrescrita, polimorfismo.

Crie uma classe abstrata `FormaPagamento` com o método:

```java
public abstract void pagar(double valor);
```

Crie as subclasses:

- `PagamentoCartaoCredito`;
- `PagamentoPix`;
- `PagamentoBoleto`.

Cada classe deve implementar o método `pagar` exibindo uma mensagem diferente.

No `main`, crie um vetor de `FormaPagamento` e armazene diferentes formas de pagamento.

Depois, percorra o vetor chamando o método `pagar`.

O objetivo é perceber que o mesmo método pode executar comportamentos diferentes dependendo do objeto utilizado.

## Entrega
Até 22/05/2026 (antes da aula)
Entregue um .zip com todos os códigos
Use esse link para a entrega: [https://forms.gle/TmFkcykFQxxyNfwh9](https://forms.gle/TmFkcykFQxxyNfwh9)
