# Atividade – CRUD com PostgreSQL

## Contexto

Utilize o banco de dados `streaming_aula`, criado nas aulas anteriores, contendo as tabelas `plano`, `usuario`, `conteudo`, `visualizacao` e `log_auditoria`.

A atividade deve ser realizada utilizando o **PostgreSQL via terminal (`psql`)**.

## Objetivo

Praticar as quatro operações fundamentais de CRUD:

- **Create** → `INSERT`
- **Read** → `SELECT`
- **Update** → `UPDATE`
- **Delete** → `DELETE`

> Antes de executar um `UPDATE` ou `DELETE`, sempre que possível execute primeiro um `SELECT` com a mesma condição.

---

## 1. Cadastro e consulta de usuário

Cadastre um novo usuário com os seguintes dados:

- código: `10`
- nome: `Marcos`
- e-mail: `marcos@email.com`
- cidade: `Curitiba`
- plano: `1`

Depois:

1. consulte apenas o usuário cadastrado;
2. confirme o nome do plano utilizando um `JOIN`.

---

## 2. Cadastro de vários conteúdos

Cadastre, em um único comando `INSERT`, os conteúdos:

| Código | Título | Tipo | Gênero | Duração |
|---|---|---|---|---:|
| 201 | Código Oculto | Filme | Suspense | 110 |
| 202 | Mundo Digital | Série | Ficção Científica | 50 |
| 203 | Cozinha em Família | Série | Comédia | 40 |

Depois, consulte apenas esses três registros utilizando `WHERE`.

---

## 3. Alteração simples

O usuário `Marcos` mudou de cidade.

Altere sua cidade de `Curitiba` para `Londrina`.

Depois:

1. consulte o registro antes da alteração;
2. execute o `UPDATE`;
3. consulte novamente para confirmar a mudança.

---

## 4. Alteração de várias colunas

O usuário de código `10`:

- mudou para `Maringá`;
- passou a utilizar o plano `Premium`.

Atualize as duas informações em um único comando.

Depois, mostre:

- nome do usuário;
- cidade;
- nome do plano.

---

## 5. Atualização com expressão

A plataforma decidiu aumentar em **8%** o valor de todos os planos com preço inferior a `50.00`.

Antes de atualizar:

1. consulte os planos que serão afetados;
2. execute o `UPDATE`;
3. consulte novamente os valores atualizados.

---

## 6. Cadastro de visualização

Cadastre uma visualização para o usuário `10` do conteúdo `201`.

Utilize:

- id da visualização: `20`;
- data atual com `CURRENT_DATE`;
- minutos assistidos: `80`.

Depois, consulte a visualização mostrando:

- usuário;
- conteúdo;
- data;
- minutos assistidos.

---

## 7. Atualização com condição composta

Atualize para `Drama Histórico` o gênero de todos os conteúdos que:

- sejam do tipo `Filme`;
- estejam atualmente cadastrados com gênero `Drama`.

Antes do `UPDATE`, execute um `SELECT` com a mesma condição.

---

## 8. DELETE seguro

Cadastre temporariamente o seguinte usuário:

- código: `30`
- nome: `Usuário Temporário`
- e-mail: `temporario@email.com`
- cidade: `Curitiba`
- plano: `1`

Depois:

1. consulte o registro;
2. exclua apenas esse usuário;
3. execute um novo `SELECT` para confirmar que o registro foi removido.

---

## 9. Exclusão utilizando LIKE

Cadastre os conteúdos:

```text
301 | Teste Filme A
302 | Teste Filme B
303 | Conteúdo Permanente
```

Preencha os demais campos com valores válidos.

Em seguida:

1. utilize `SELECT` e `LIKE` para localizar os conteúdos cujo título começa com `Teste`;
2. exclua somente esses conteúdos;
3. confirme que `Conteúdo Permanente` continua cadastrado.

---

## 10. Testando integridade referencial

Tente cadastrar um usuário utilizando um `id_plano` que não existe, por exemplo `999`.

Responda:

1. o PostgreSQL permitiu a operação?
2. qual mensagem de erro foi apresentada?
3. por que a operação foi bloqueada?
4. qual restrição da tabela está relacionada ao erro?

---

## 11. Tentativa de exclusão com dependência

Escolha um usuário que possua pelo menos uma visualização.

Antes de excluir:

1. consulte suas visualizações;
2. tente excluir o usuário;
3. observe o resultado;
4. explique por que o PostgreSQL impede a exclusão.

---

## 12. Alteração de e-mail

Altere o e-mail de `Carla` para:

```text
carla.silva@email.com
```

Faça a alteração identificando o usuário pelo código, e não pelo nome.

Depois consulte apenas:

- código;
- nome;
- e-mail.

---

## 13. Atualização de vários registros

Todos os conteúdos do tipo `Série` com duração inferior a `50` minutos passarão a ter duração de `50` minutos.

Faça:

1. um `SELECT` para identificar os registros afetados;
2. o `UPDATE`;
3. outro `SELECT` para conferir o resultado.

---

## 14. Exclusão condicionada

Exclua conteúdos que satisfaçam simultaneamente:

- título começando com `Teste`;
- nenhuma visualização associada.

Primeiro localize os conteúdos, confirme que não possuem visualizações e só então execute o `DELETE`.

---

## 15. Ciclo CRUD completo

Implemente o ciclo CRUD completo para um usuário fictício.

### Create

Cadastre:

- código: `50`
- nome: `Juliana`
- e-mail: `juliana@email.com`
- cidade: `Cascavel`
- plano: `1`

### Read

Consulte o usuário e seu plano.

### Update

Altere:

- cidade para `Curitiba`;
- plano para `2`.

### Read novamente

Confira as alterações.

### Delete

Remova o usuário.

### Verificação final

Confirme que ele não existe mais.

---

## 16. Cadastro seguido de movimentação

Cadastre:

1. um novo usuário;
2. um novo conteúdo;
3. uma visualização relacionando os dois.

Depois, utilizando `JOIN`, apresente:

- nome do usuário;
- título do conteúdo;
- data;
- minutos assistidos.

Por fim, tente excluir o usuário antes de excluir sua visualização e explique o resultado.

---

## 17. Correção de dados em massa

Considere que todos os usuários cadastrados em `Londrina` precisam ter sua cidade corrigida para:

```text
Londrina - PR
```

Execute:

1. um `SELECT` mostrando quais usuários serão afetados;
2. o `UPDATE`;
3. um `SELECT` final.

---

## 18. Exclusão em ordem correta

Crie um usuário e uma visualização relacionada a ele.

Depois remova completamente os dados desse usuário do banco.

A exclusão deve respeitar a integridade referencial.

Determine e execute a ordem correta dos comandos `DELETE` e explique por que essa ordem é necessária.

