# Lista de Exercícios — SQL DDL I

## Sistema de Locação de Equipamentos

Esta atividade pratica os comandos de **DDL (Data Definition Language)** estudados em aula:

- `CREATE DATABASE`
- `CREATE TABLE`
- tipos de dados
- `NULL`, `NOT NULL` e `DEFAULT`
- `PRIMARY KEY`
- `UNIQUE`
- `FOREIGN KEY`
- `ON DELETE` e `ON UPDATE`
- `ALTER TABLE`
- `DROP TABLE`
- `CASCADE` e `RESTRICT`

Todas as questões são discursivas. Nas questões práticas, escreva o comando SQL completo solicitado. Considere o dialeto **PostgreSQL**.

> Não é necessário inserir dados nas tabelas. O foco da atividade é definir e alterar a estrutura do banco de dados.

---

# Contexto único

Uma empresa de locação de equipamentos precisa registrar clientes, equipamentos, locações e os equipamentos incluídos em cada locação.

O banco de dados possui as seguintes relações:

```text
cliente 1 -------- N locacao 1 -------- N item_locacao N -------- 1 equipamento
```

- Um cliente pode realizar várias locações.
- Cada locação pertence a um único cliente.
- Uma locação pode incluir vários equipamentos.
- Um mesmo equipamento pode aparecer em várias locações, em momentos diferentes.
- A tabela `item_locacao` representa os equipamentos de cada locação.

---

## Estrutura esperada do banco

### Tabela `cliente`

| Coluna | Descrição |
|---|---|
| `id_cliente` | identificador do cliente |
| `nome` | nome completo |
| `email` | e-mail para contato |
| `telefone` | telefone para contato |
| `cidade` | cidade do cliente |

### Tabela `equipamento`

| Coluna | Descrição |
|---|---|
| `id_equipamento` | identificador do equipamento |
| `nome` | nome do equipamento |
| `categoria` | categoria do equipamento |
| `valor_diaria` | valor cobrado por dia |
| `disponivel` | indica se o equipamento está disponível |

### Tabela `locacao`

| Coluna | Descrição |
|---|---|
| `id_locacao` | identificador da locação |
| `id_cliente` | cliente responsável pela locação |
| `data_locacao` | data em que a locação foi realizada |
| `data_prevista_devolucao` | data prevista para devolução |
| `status` | situação atual da locação |

### Tabela `item_locacao`

| Coluna | Descrição |
|---|---|
| `id_locacao` | locação à qual o item pertence |
| `id_equipamento` | equipamento incluído na locação |
| `quantidade` | quantidade locada |
| `valor_diaria_aplicado` | valor diário definido para aquele item |

---

# Exercícios

## Parte 1 — Conceitos iniciais e criação de tabelas

**1.** Explique, com suas palavras, a diferença entre DDL e DML.

---

**2.** Defina tipos de dados SQL adequados para cada uma das colunas abaixo. Justifique brevemente suas escolhas.

| Coluna | Tipo de informação |
|---|---|
| `id_cliente` | identificador numérico |
| `nome` | texto de até 80 caracteres |
| `telefone` | texto de até 20 caracteres |
| `valor_diaria` | valor monetário com duas casas decimais |
| `data_locacao` | data |
| `disponivel` | texto curto indicando `SIM` ou `NAO` |

---

**3.** Escreva o comando `CREATE TABLE` para criar a tabela `cliente`, considerando as regras abaixo:

- `id_cliente` é um número inteiro obrigatório;
- `nome` é um texto de até 80 caracteres e obrigatório;
- `email` é um texto de até 120 caracteres e obrigatório;
- `telefone` é um texto de até 20 caracteres e opcional;
- `cidade` é um texto de até 60 caracteres e opcional;
- `id_cliente` deve ser a chave primária;
- `email` não pode se repetir.

Dê nomes às restrições de chave primária e de unicidade.

---

**4.** Escreva o comando `CREATE TABLE` para criar a tabela `equipamento`, considerando as regras abaixo:

- `id_equipamento` é a chave primária;
- `nome` e `categoria` são obrigatórios;
- `valor_diaria` é obrigatório e deve armazenar até oito dígitos, incluindo duas casas decimais;
- `disponivel` é obrigatório e deve assumir `SIM` como valor padrão quando não for informado.

---

## Parte 2 — Chaves estrangeiras e tabela associativa

**5.** Escreva o comando `CREATE TABLE` para criar a tabela `locacao`, considerando as regras abaixo:

- `id_locacao` é a chave primária;
- `id_cliente` é obrigatório;
- `data_locacao` é obrigatória e deve assumir a data atual como valor padrão;
- `data_prevista_devolucao` é obrigatória;
- `status` é obrigatório e deve assumir `ABERTA` como valor padrão;
- `id_cliente` deve ser chave estrangeira que referencia `cliente(id_cliente)`.

Dê nomes às restrições criadas.

---

**6.** A empresa deseja impedir que um cliente seja removido enquanto ainda possuir locações registradas. Complete a definição da chave estrangeira de `locacao.id_cliente` usando uma ação adequada de `ON DELETE`. Explique por que essa ação é apropriada.

---

**7.** Escreva o comando `CREATE TABLE` para criar a tabela `item_locacao`, considerando as regras abaixo:

- `id_locacao` e `id_equipamento` são obrigatórios;
- `quantidade` é um número inteiro obrigatório;
- `valor_diaria_aplicado` é obrigatório e possui duas casas decimais;
- a chave primária deve ser composta por `id_locacao` e `id_equipamento`;
- `id_locacao` deve referenciar `locacao(id_locacao)`;
- `id_equipamento` deve referenciar `equipamento(id_equipamento)`.

Dê nomes às três restrições.

---

## Parte 2 — Alterações com `ALTER TABLE`

Considere que as tabelas já foram criadas.

**8.** Escreva o comando para adicionar à tabela `cliente` uma coluna opcional chamada `cpf`, capaz de armazenar até 14 caracteres.

---

**9.** Após cadastrar vários clientes, a empresa decidiu que o CPF não pode se repetir. Escreva o comando `ALTER TABLE` necessário para adicionar uma restrição `UNIQUE` à coluna `cpf`. Dê um nome adequado à restrição.

---

**10.** A empresa percebeu que todos os equipamentos precisam possuir uma categoria. Escreva o comando que transforma a coluna `categoria` da tabela `equipamento` de opcional para obrigatória.

---

**11.** A empresa alterou sua regra de negócio e definiu que novas locações devem iniciar com o status `AGUARDANDO_PAGAMENTO`. Escreva o comando para alterar o valor padrão da coluna `status` da tabela `locacao`.

## Entrega:
- Utilize a o link para entrega: [https://forms.gle/hvkczjS7k3T6oHrG6](https://forms.gle/hvkczjS7k3T6oHrG6)
- Entrga até 07/07/2026 as 23:59