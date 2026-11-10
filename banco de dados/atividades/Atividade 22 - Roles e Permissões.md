# Atividade Prática — Usuários, Roles e Permissões no PostgreSQL


Utilize o Banco de Dados do Exemplo 09

---

# Parte I — Conceitos e reconhecimento

## Exercício 1

Explique a diferença entre **autenticação** e **autorização**. Dê um exemplo de cada no sistema de reservas de hotel.

## Exercício 2

Explique o que são **roles** no PostgreSQL. Qual é a diferença entre roles com `LOGIN` e roles com `NOLOGIN`?

## Exercício 3

Conecte-se ao banco `hotel_seguranca`. Utilize comandos do `psql` para listar:

1. os bancos de dados;
2. as tabelas;
3. as views;
4. as roles existentes;
5. os privilégios cadastrados para a tabela `reserva`.

## Exercício 4

Execute uma consulta que apresente `current_user`, `session_user` e `current_database()`. Explique o significado de cada resultado.

---

# Parte II — Criando roles e usuários

## Exercício 5

Como administrador, crie uma role **sem login** chamada `papel_atendimento_aluno`. Explique por que uma role de setor normalmente não precisa se conectar diretamente.

## Exercício 6

Crie uma conta **com login** chamada `usuario_atendimento_aluno` e defina sua senha interativamente pelo `psql`.

## Exercício 7

Associe `usuario_atendimento_aluno` ao papel `papel_atendimento_aluno`. Utilize o comando apropriado para verificar a associação.

## Exercício 8

Conceda ao papel `papel_atendimento_aluno` as permissões necessárias para **se conectar ao banco** `hotel_seguranca` e **acessar o schema** `public`. Explique por que uma dessas permissões não substitui a outra.

---

# Parte III — Permissões de leitura e escrita

## Exercício 9

Conceda a `papel_atendimento_aluno` permissão para consultar as tabelas `hospede`, `quarto`, `tipo_quarto` e `reserva`, mas **não** a tabela `pagamento`.

## Exercício 10

Conecte-se como `usuario_atendimento_aluno` e execute consultas `SELECT` nas tabelas `hospede` e `quarto`. Registre o resultado.

## Exercício 11

Como `usuario_atendimento_aluno`, tente consultar `pagamento`. Registre o erro e explique qual privilégio está faltando.

## Exercício 12

Conceda ao papel de atendimento a permissão necessária para **cadastrar novas reservas**, mas não para excluí-las.

Como usuário de atendimento, cadastre uma reserva fictícia com um hóspede e quarto existentes. Utilize datas válidas e consulte o registro inserido.

## Exercício 13

Conceda a `papel_atendimento_aluno` permissão de atualização **somente da coluna `status`** da tabela `reserva`.

Como usuário de atendimento, altere o status de uma reserva existente e confirme o resultado.

## Exercício 14

Ainda como usuário de atendimento, tente alterar `valor_total` de uma reserva. Explique por que o PostgreSQL permite o Exercício 13, mas bloqueia este.

## Exercício 15

Como usuário de atendimento, tente excluir uma reserva. Registre o resultado. Qual privilégio seria necessário para executar esse comando?

---

# Parte IV — Papéis para outros setores

## Exercício 16

Crie a role `papel_financeiro_aluno` (`NOLOGIN`) e a conta `usuario_financeiro_aluno` (`LOGIN`). Associe ambas, configure o acesso ao banco e ao schema e defina a senha da conta.

## Exercício 17

Conceda ao financeiro as permissões para:

- consultar `reserva` e `pagamento`;
- inserir registros em `pagamento`;
- **não** consultar `funcionario` ou `hospede`.

Teste as quatro situações com a conta financeira e registre o resultado.

---

# Parte V — Views e proteção de informações

## Exercício 18

Conceda a `papel_atendimento_aluno` permissão de leitura na view `vw_funcionarios_publico`, **sem conceder acesso direto** à tabela `funcionario`.

Teste as duas consultas:

```sql
SELECT * FROM vw_funcionarios_publico;
SELECT * FROM funcionario;
```

Explique o resultado.

## Exercício 19

Como administrador, crie uma view `vw_quartos_precos_aluno` que mostre **número do quarto, tipo e valor da diária**. Conceda `SELECT` sobre essa view ao papel financeiro, sem conceder `SELECT` direto às tabelas `quarto` e `tipo_quarto`.

Teste se a conta financeira consegue ler a view e se consegue ler as tabelas de origem.

## Exercício 20

Explique por que fornecer acesso apenas a uma view pode ser mais seguro do que conceder acesso direto à tabela original. Uma view, isoladamente, garante segurança se o usuário já tiver acesso à tabela base?

---

# Parte VI — REVOKE e verificação

## Exercício 21

Revogue **apenas a permissão de atualização da coluna `status`** da tabela `reserva` concedida a `papel_atendimento_aluno`.

Teste novamente o `UPDATE` como `usuario_atendimento_aluno`. Depois restaure a permissão.

# Entrega

Realizar a entrega via link: [https://forms.gle/Q3b9tXptKdsgtAmN6](https://forms.gle/Q3b9tXptKdsgtAmN6)

Entrega até o dia 17/11/2026
