# Lista de Exercícios — Java Swing com Botão, Label e Campo Textual

## Orientações gerais

Nesta lista, os alunos devem usar apenas os seguintes componentes visuais do Java Swing:

```java
JLabel
JTextField
JButton
```

Também podem ser usados elementos de estrutura, como:

```java
JFrame
JPanel
FlowLayout
GridLayout
BorderLayout
```

Não utilizar:

```java
JOptionPane
JComboBox
JTable
JRadioButton
JCheckBox
JTextArea
```

Todas as respostas, mensagens e resultados devem aparecer em um `JLabel`.

---

# Exercício 1 — Primeira janela com mensagem

Crie uma tela com:

- um `JLabel` com o texto inicial `"Bem-vindo ao sistema"`;
- um `JButton` com o texto `"Clique aqui"`.

Quando o botão for clicado, o texto do `JLabel` deve mudar para:

```text
Botão clicado com sucesso!
```

---

# Exercício 2 — Saudação com nome

Crie uma tela com:

- um `JLabel` escrito `"Digite seu nome:"`;
- um `JTextField` para o nome;
- um `JButton` escrito `"Enviar"`;
- um `JLabel` para exibir o resultado.

Quando o botão for clicado, o sistema deve exibir:

```text
Olá, João!
```

O nome deve ser o valor digitado no campo textual.

---

# Exercício 3 — Soma de dois números

Crie uma tela com:

- um campo para o primeiro número;
- um campo para o segundo número;
- um botão `"Somar"`;
- um label para mostrar o resultado.

Quando o botão for clicado, o programa deve somar os dois valores e exibir:

```text
Resultado: 15
```

---

# Exercício 4 — Calculadora de média

Crie uma tela para calcular a média de duas notas.

A tela deve ter:

- campo para a primeira nota;
- campo para a segunda nota;
- botão `"Calcular média"`;
- label para exibir o resultado.

Exemplo de saída:

```text
Média: 8.5
```

---

# Exercício 5 — Verificação de maioridade

Crie uma tela com:

- um campo para o usuário digitar a idade;
- um botão `"Verificar"`;
- um label para exibir a resposta.

Regras:

- se a idade for maior ou igual a 18, exibir `"Maior de idade"`;
- caso contrário, exibir `"Menor de idade"`.

---

# Exercício 6 — Número positivo, negativo ou zero

Crie uma tela com:

- um campo para digitar um número inteiro;
- um botão `"Analisar"`;
- um label para mostrar o resultado.

O sistema deve informar se o número é:

```text
Positivo
Negativo
Zero
```

---

# Exercício 7 — Conversor de temperatura

Crie uma tela para converter Celsius para Fahrenheit.

A tela deve ter:

- campo para digitar a temperatura em Celsius;
- botão `"Converter"`;
- label para mostrar o resultado.

Use a fórmula:

```text
F = C * 1.8 + 32
```

Exemplo:

```text
Temperatura em Fahrenheit: 77.0
```

---

# Exercício 8 — Cálculo de salário

Crie uma tela com:

- campo para o valor da hora trabalhada;
- campo para a quantidade de horas trabalhadas;
- botão `"Calcular salário"`;
- label para mostrar o salário bruto.

Exemplo:

```text
Salário bruto: R$ 2400.0
```

---

# Exercício 9 — Validação de campo obrigatório

Crie uma tela de cadastro simples com:

- campo para o nome;
- botão `"Cadastrar"`;
- label para exibir a mensagem.

Regras:

- se o campo estiver vazio, exibir `"O nome é obrigatório"`;
- caso contrário, exibir `"Cadastro realizado para: Nome"`.

Dica: use `trim()` para ignorar espaços em branco.

---

# Exercício 10 — Login simples

Crie uma tela com:

- campo para usuário;
- campo para senha;
- botão `"Entrar"`;
- label para exibir o resultado.

Regras:

- usuário correto: `"admin"`;
- senha correta: `"1234"`.

Se os dados estiverem corretos, exibir:

```text
Login realizado com sucesso
```

Caso contrário:

```text
Usuário ou senha inválidos
```

---

# Exercício 11 — Calculadora com quatro operações

Crie uma tela com:

- campo para o primeiro número;
- campo para o segundo número;
- quatro botões:
  - `"Somar"`;
  - `"Subtrair"`;
  - `"Multiplicar"`;
  - `"Dividir"`;
- label para mostrar o resultado.

Cada botão deve executar uma operação diferente.

Exemplo:

```text
Resultado: 20.0
```

Regra adicional:

- se o usuário tentar dividir por zero, exibir `"Não é possível dividir por zero"`.

---

# Exercício 12 — Contador de cliques

Crie uma tela com:

- um label mostrando `"Cliques: 0"`;
- um botão `"Clique"`.

Cada vez que o botão for clicado, o contador deve aumentar em 1.

Exemplo:

```text
Cliques: 5
```

---

# Exercício 13 — Cadastro de aluno com situação

Crie uma tela com:

- campo para nome do aluno;
- campo para nota 1;
- campo para nota 2;
- botão `"Calcular situação"`;
- label para exibir o resultado.

Regras:

- calcular a média das duas notas;
- se a média for maior ou igual a 7, exibir `"Aluno aprovado"`;
- se a média for maior ou igual a 5 e menor que 7, exibir `"Aluno em recuperação"`;
- se a média for menor que 5, exibir `"Aluno reprovado"`.

A mensagem deve incluir o nome e a média.

Exemplo:

```text
Ana - Média: 8.0 - Aprovada
```

---

# Exercício 14 — Simulador de desconto

Crie uma tela com:

- campo para nome do produto;
- campo para valor do produto;
- campo para percentual de desconto;
- botão `"Calcular desconto"`;
- label para exibir o resultado.

O sistema deve calcular o valor final do produto.

Exemplo:

```text
Produto: Mouse | Valor final: R$ 72.0
```

Fórmula:

```text
valorFinal = valor - (valor * desconto / 100)
```

---

# Exercício 15 — Mini cadastro com resumo

Crie uma tela de cadastro com:

- campo para nome;
- campo para idade;
- campo para curso;
- campo para cidade;
- botão `"Gerar resumo"`;
- label para exibir o resumo.

Quando o botão for clicado, o sistema deve gerar uma frase com todos os dados.

Exemplo:

```text
João tem 20 anos, mora em Maringá e estuda Engenharia de Software.
```

Regras adicionais:

- nenhum campo pode ficar vazio;
- se algum campo estiver vazio, exibir `"Preencha todos os campos"`.

---

# Progressão da lista

| Exercícios | Foco principal |
|---|---|
| 1 e 2 | Primeiros eventos com botão e alteração de label |
| 3 e 4 | Entrada numérica e cálculo simples |
| 5 e 6 | Condicionais |
| 7 e 8 | Fórmulas e operações com `double` |
| 9 e 10 | Validação de entrada |
| 11 e 12 | Múltiplos botões e estado da tela |
| 13 e 14 | Regras de negócio simples |
| 15 | Integração de vários campos em uma tela |

---

# Desafio extra

Refatore pelo menos 5 exercícios para que a ação do botão seja feita em um método separado.

Exemplo:

```java
botao.addActionListener(e -> calcularMedia());
```

Em vez de colocar toda a lógica diretamente dentro do `addActionListener`.
