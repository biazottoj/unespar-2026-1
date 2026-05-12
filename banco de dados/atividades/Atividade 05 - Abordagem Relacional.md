# Atividades práticas — Abordagem Relacional

## 1. Avaliação crítica de uma tabela mal projetada

Uma escola armazenou os dados dos alunos na seguinte tabela:

### Aluno

| RA | Nome | Telefones | Curso | Disciplinas |
|---|---|---|---|---|
| 2024001 | Ana Souza | 99999-1111, 98888-2222 | Engenharia de Software | Banco de Dados, Programação |
| 2024002 | Bruno Lima | 97777-3333 | Ciência da Computação | Banco de Dados, Redes |

Avalie o projeto dessa tabela.

Responda:

a) Quais colunas violam a ideia de valor atômico e monovalorado?  
b) Que problemas podem surgir ao consultar, alterar ou excluir informações nessa tabela?  
c) Proponha um novo conjunto de tabelas para representar esses dados.  
d) Defina as chaves primárias e estrangeiras do novo modelo.  
e) Justifique por que sua solução é melhor do que a tabela original.

---

## 2. Criação de um esquema relacional para biblioteca

Uma biblioteca deseja controlar livros, autores, exemplares físicos e empréstimos. Um livro pode ter vários autores. Um autor pode escrever vários livros. Um livro pode possuir vários exemplares. Um aluno pode realizar vários empréstimos, mas cada empréstimo se refere a apenas um exemplar.

Crie um esquema relacional completo contendo:

a) Tabelas necessárias.  
b) Colunas de cada tabela.  
c) Chaves primárias.  
d) Chaves estrangeiras.  
e) Pelo menos uma tabela associativa.  
f) Restrições de domínio e de vazio.  
g) Duas regras semânticas importantes para esse sistema.

Depois, explique quais decisões de modelagem foram mais importantes.

---

## 3. Avaliação de possíveis chaves primárias

Considere a tabela:

### Funcionario

| CodigoFunc | CPF | Email | Nome | DataNascimento | Setor |
|---|---|---|---|---|---|

Três analistas fizeram propostas diferentes:

- **Analista A:** usar `Nome` como chave primária.
- **Analista B:** usar `CPF` como chave primária.
- **Analista C:** usar `CodigoFunc` como chave primária e `CPF` como chave alternativa.

Avalie as três propostas.

Responda:

a) Qual proposta é mais adequada?  
b) Quais vantagens e desvantagens existem em usar `CPF` como chave primária?  
c) Em que situação `CodigoFunc` seria uma escolha melhor?

---

## 4. Criação de um banco relacional para sistema de vendas

Uma loja deseja controlar clientes, produtos, pedidos e itens de pedido. Cada cliente pode fazer vários pedidos. Cada pedido pode conter vários produtos. Cada produto pode aparecer em vários pedidos.

Crie o esquema relacional desse sistema.

O esquema deve conter:

a) Tabela `Cliente`.  
b) Tabela `Produto`.  
c) Tabela `Pedido`.  
d) Tabela `ItemPedido`.  
e) Chaves primárias simples e compostas, quando necessário.  
f) Chaves estrangeiras.  
g) Restrições de domínio para preço, quantidade e data.  
h) Restrições de vazio para campos obrigatórios e opcionais.

Depois, explique por que `ItemPedido` é necessária.

---

## 5. Criação de restrições de integridade para sistema acadêmico

Considere um sistema acadêmico com alunos, cursos, disciplinas, professores e matrículas.

Crie pelo menos **12 restrições de integridade**, classificando-as em:

a) Integridade de domínio.  
b) Integridade de vazio.  
c) Integridade de chave.  
d) Integridade referencial.  
e) Restrição semântica.

Exemplo de formato esperado:

| Regra | Tipo de restrição | Justificativa |
|---|---|---|
| A nota final deve estar entre 0 e 10 | Domínio | Evita valores inválidos de nota |

Inclua pelo menos duas regras para cada tipo.

---

## 6. Criação de um modelo para controle de projetos

Uma empresa deseja controlar projetos de software. Cada projeto possui um código, nome, data de início e data prevista de término. Cada projeto possui vários desenvolvedores. Um desenvolvedor pode atuar em vários projetos. Para cada participação, é necessário registrar o papel do desenvolvedor no projeto e a quantidade de horas semanais alocadas.

Crie o esquema relacional.

O modelo deve conter:

a) Tabelas necessárias.  
b) Chaves primárias.  
c) Chaves estrangeiras.  
d) Uma tabela para representar a participação dos desenvolvedores nos projetos.  
e) Restrições de domínio para horas semanais.  
f) Restrições semânticas, como data de término não poder ser anterior à data de início.

Depois, explique por que a relação entre desenvolvedor e projeto não deve ser representada em uma única coluna multivalorada.

---

## 7. Avaliação de integridade de domínio e vazio em dados reais

Considere os seguintes dados recebidos para cadastro de produtos:

| CodigoProduto | Nome | Preco | Estoque | Categoria |
|---|---|---|---|---|
| P01 | Teclado | 120.00 | 10 | Periférico |
| P02 | Mouse | -50.00 | 15 | Periférico |
| P03 | NULL | 300.00 | 5 | Monitor |
| P04 | Cadeira Gamer | 899.00 | -2 | Mobiliário |
| P05 | Webcam | 250.00 | NULL | Periférico |

Avalie os dados.

Responda:

a) Quais linhas violam restrições de domínio?  
b) Quais linhas violam restrições de vazio?  
c) Quais colunas deveriam ser obrigatórias?  
d) Proponha uma versão corrigida da tabela.