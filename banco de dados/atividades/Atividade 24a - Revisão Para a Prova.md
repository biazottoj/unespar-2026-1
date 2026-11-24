# Revisão de Banco de Dados — Conteúdos após a última prova

**Material de estudo para os alunos | PostgreSQL e MongoDB**  
**Abrangência:** procedures e triggers; transações e ACID; views; índices; usuários, roles e permissões; NoSQL e MongoDB.

## Como utilizar este material

Este roteiro contém **explicações conceituais, exemplos comentados e 60 questões** distribuídas em seis unidades. Leia a teoria de cada unidade antes de resolver suas dez questões. Algumas questões pedem explicações, outras exigem interpretar ou escrever SQL/JavaScript. As respostas estão em um arquivo de gabarito separado.

### Banco de referência

Os exemplos SQL adotam a estrutura didática do sistema de hotel usada nas aulas:

| Tabela | Campos principais |
|---|---|
| `hospede` | `id_hospede`, `nome`, `email`, `cidade` |
| `tipo_quarto` | `id_tipo`, `nome_tipo`, `valor_diaria` |
| `quarto` | `id_quarto`, `numero`, `status`, `id_tipo` |
| `reserva` | `id_reserva`, `id_hospede`, `id_quarto`, `data_checkin`, `data_checkout`, `status`, `valor_total` |
| `pagamento` | `id_pagamento`, `id_reserva`, `valor`, `data_pagamento` |
| `funcionario` | `id_funcionario`, `nome`, `cargo`, `salario` |

**Observações:** os nomes de colunas e a existência de `pagamento` podem variar entre as versões do banco de hotel. As questões são autocontidas e devem ser adaptadas se a estrutura instalada for diferente. Considere os estados de reserva `Confirmada`, `Cancelada` e `Concluída` e os estados de quarto `Disponível`, `Ocupado` e `Manutenção`. Nas questões de MongoDB, as coleções são `hospedes`, `quartos` e `reservas`, com os campos do estudo guiado (`hospedeId`, `quartoId`, `valorTotal`, `contato.email`, `tags`, etc.).

> **Atenção ao ambiente:** comandos como `\d`, `\du` e `\dp` são do **psql**; instruções como `db.hospedes.find()` são do **mongosh**; comandos `docker` são executados no terminal do sistema operacional. Nos exemplos de alteração de dados, prefira um banco de testes.

---

# Unidade 1 — Procedures e triggers

## 1.1. Por que automatizar operações no banco?

Em aplicações reais, algumas operações são recorrentes ou dependem de regras que devem ser respeitadas por qualquer sistema que acesse o banco. No hotel, cancelar uma reserva, validar as datas de uma hospedagem e registrar alterações no status são exemplos. O PostgreSQL permite organizar essas responsabilidades com **procedures** e **triggers**, mas os dois recursos são usados de maneiras diferentes.

## 1.2. Stored procedures: conceito, parâmetros e execução

Uma *procedure* é uma rotina armazenada no banco, executada explicitamente com `CALL`. Ela pode receber parâmetros e executar vários comandos SQL, como `INSERT`, `UPDATE` e `DELETE`. Em PostgreSQL, `CREATE PROCEDURE` define essa rotina; `LANGUAGE plpgsql` indica a linguagem procedimental e o trecho entre `$$ ... $$` é o corpo da rotina.

```sql
CREATE OR REPLACE PROCEDURE sp_cancelar_reserva(p_id BIGINT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE reserva
    SET status = 'Cancelada'
    WHERE id_reserva = p_id;
END;
$$;

CALL sp_cancelar_reserva(1);
```

A rotina acima **não é executada quando é criada**. O `UPDATE` acontece quando alguém executa o `CALL`. A variável `p_id` é o parâmetro de entrada; ela permite reutilizar a rotina para diferentes reservas. Em uma aplicação real, podem ser necessárias outras verificações, como impedir o cancelamento de uma reserva já concluída.

## 1.3. Triggers: evento, momento e granularidade

Uma *trigger* (gatilho) é uma ação configurada para ocorrer **automaticamente** quando determinado evento atinge uma tabela ou view. No PostgreSQL, normalmente criamos uma **função de trigger** (`RETURNS TRIGGER`) e, depois, associamos essa função a um evento com `CREATE TRIGGER`.

| Elemento | Significado | Exemplo |
|---|---|---|
| Evento | Operação que dispara o gatilho | `INSERT`, `UPDATE`, `DELETE` |
| Momento | Quando a função é executada | `BEFORE`, `AFTER` |
| Granularidade | Quantas vezes é executada | `FOR EACH ROW` ou `FOR EACH STATEMENT` |
| Condição | Restringe quando deve executar | `WHEN (...)`, quando aplicável |
| Função | Código invocado pelo gatilho | `EXECUTE FUNCTION fn_...()` |

Triggers `BEFORE` são úteis para **validar ou ajustar dados antes** da gravação. Triggers `AFTER` são úteis para **auditoria e efeitos associados** à operação concluída no contexto da transação. `FOR EACH ROW` executa a função para cada linha afetada; `FOR EACH STATEMENT`, uma vez por comando, independentemente da quantidade de linhas atingidas.

## 1.4. NEW e OLD

Em triggers por linha, as variáveis especiais disponibilizam os valores relacionados ao registro:

- `NEW`: valores novos de uma linha inserida ou atualizada (não existe em `DELETE`).
- `OLD`: valores antigos de uma linha atualizada ou excluída (não existe em `INSERT`).

Por exemplo, numa atualização de `status` em `reserva`, `OLD.status` é o status anterior e `NEW.status` é o status proposto.

## 1.5. Exemplo: validação de datas com BEFORE INSERT

```sql
CREATE OR REPLACE FUNCTION fn_validar_periodo_reserva()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.data_checkout <= NEW.data_checkin THEN
        RAISE EXCEPTION 'O checkout deve ocorrer após o checkin';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_validar_periodo_reserva
BEFORE INSERT ON reserva
FOR EACH ROW
EXECUTE FUNCTION fn_validar_periodo_reserva();
```

`RAISE EXCEPTION` interrompe a operação com erro. `RETURN NEW` permite que o processamento prossiga com os dados da nova linha. No cenário de hotel, essa regra **também pode ser implementada por uma restrição `CHECK`**, que geralmente é preferível para uma condição simples e declarativa; usamos o gatilho aqui para compreender seu funcionamento.

## 1.6. Exemplo: auditoria de mudança de status com AFTER UPDATE

Considere a tabela auxiliar:

```sql
CREATE TABLE IF NOT EXISTS auditoria_status_reserva (
    id_auditoria BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_reserva BIGINT NOT NULL,
    status_anterior VARCHAR(20),
    status_novo VARCHAR(20),
    alterado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

```sql
CREATE OR REPLACE FUNCTION fn_auditar_status_reserva()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_status_reserva
        (id_reserva, status_anterior, status_novo)
    VALUES
        (NEW.id_reserva, OLD.status, NEW.status);
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_auditar_status_reserva
AFTER UPDATE OF status ON reserva
FOR EACH ROW
WHEN (OLD.status IS DISTINCT FROM NEW.status)
EXECUTE FUNCTION fn_auditar_status_reserva();
```

A cláusula `WHEN` evita criar um registro de auditoria quando o valor de `status` permanece igual. O uso de `IS DISTINCT FROM` também é seguro diante de valores `NULL`, embora a coluna possa ser obrigatória no banco didático.

## 1.7. Cuidados: triggers, constraints e transações

A existência de uma trigger não dispensa a análise de restrições como `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL` e `CHECK`. Muitas regras de integridade devem ser expressas diretamente por constraints. Além disso, os efeitos de uma trigger **fazem parte da transação que disparou o evento**. Se a transação inteira receber `ROLLBACK`, a alteração e a auditoria inserida pela trigger serão desfeitas.

### Questões — Unidade 1

**1.** Explique a diferença entre uma *procedure* e uma *trigger*. Como cada uma é executada? Apresente um exemplo de aplicação no hotel.

**2.** Escreva uma procedure chamada `sp_concluir_reserva` que receba um identificador de reserva e altere seu status para `Concluída`. Mostre também o comando para executá-la para a reserva `1`.

**3.** Diferencie `BEFORE` e `AFTER`, bem como `FOR EACH ROW` e `FOR EACH STATEMENT`. Em qual combinação seria mais natural validar cada nova reserva antes de inseri-la?

**4.** Para os eventos `INSERT`, `UPDATE` e `DELETE`, indique quando os registros `NEW` e `OLD` ficam disponíveis em uma trigger por linha e o que cada um representa.

**5.** Escreva uma função de trigger que rejeite reservas em que `data_checkout <= data_checkin`. Depois, associe-a à tabela `reserva` para executar antes de cada `INSERT`.

**6.** Considere a trigger `AFTER UPDATE OF status ON reserva FOR EACH ROW WHEN (OLD.status IS DISTINCT FROM NEW.status)`. Explique quando ela é executada e por que utiliza essa condição.

**7.** Suponha que a função de auditoria insira `OLD.status` e `NEW.status` em `auditoria_status_reserva`. Se uma reserva passar de `Confirmada` para `Cancelada`, quais valores devem ser registrados?

**8.** Uma regra impede a inclusão de valores negativos em `pagamento.valor`. Você escolheria uma constraint `CHECK` ou uma trigger para essa validação simples? Justifique.

**9.** Um `UPDATE` altera o status de quatro reservas. Quantas vezes será executada uma trigger `FOR EACH ROW`? E uma trigger `FOR EACH STATEMENT` para o mesmo evento? Considere que o comando atinja as quatro linhas.

**10.** Um `UPDATE` dispara uma trigger que insere dados na auditoria. Em seguida, a transação recebe `ROLLBACK`. O registro de auditoria permanece? Explique.

---

# Unidade 2 — Transações e propriedades ACID

## 2.1. O que é uma transação?

Uma transação é uma **unidade lógica de trabalho**, que pode envolver um ou vários comandos. No hotel, concluir um checkout pode exigir registrar o pagamento, concluir a reserva e liberar o quarto. A aplicação não deve deixar somente uma parte dessas alterações confirmada caso alguma falhe.

```sql
BEGIN;

INSERT INTO pagamento (id_reserva, valor)
VALUES (1, 360.00);

UPDATE reserva
SET status = 'Concluída'
WHERE id_reserva = 1;

UPDATE quarto
SET status = 'Disponível'
WHERE id_quarto = 101;

COMMIT;
```

Neste exemplo os identificadores devem existir e os comandos precisam respeitar as restrições do banco. O objetivo é perceber que o `COMMIT` confirma o **conjunto**. Se ocorrer algum problema antes da confirmação, usamos `ROLLBACK`.

## 2.2. Propriedades ACID

| Propriedade | Significado | Exemplo no hotel |
|---|---|---|
| **Atomicidade** | A transação é confirmada integralmente ou desfeita | Não registrar pagamento isoladamente se o checkout falhar |
| **Consistência** | A transação válida preserva regras e restrições do banco | Não inserir pagamento referenciando uma reserva inexistente |
| **Isolamento** | Transações concorrentes devem observar regras controladas de visibilidade e interferência | Duas recepções alterando reservas simultaneamente |
| **Durabilidade** | Alterações confirmadas sobrevivem a falhas conforme as garantias do SGBD | Checkout confirmado continua registrado após reinício |

## 2.3. BEGIN, COMMIT, ROLLBACK e autocommit

- `BEGIN` inicia uma transação explícita.
- `COMMIT` confirma as alterações dessa transação.
- `ROLLBACK` desfaz as alterações ainda não confirmadas.
- No uso comum do `psql`, quando não existe transação explícita, cada comando bem-sucedido costuma ser confirmado automaticamente (**autocommit**).

```sql
BEGIN;
UPDATE quarto SET status = 'Manutenção' WHERE id_quarto = 101;
SELECT * FROM quarto WHERE id_quarto = 101;
ROLLBACK;
SELECT * FROM quarto WHERE id_quarto = 101;
```

A consulta feita **dentro** da transação observa a própria alteração ainda não confirmada. Depois do `ROLLBACK`, o valor anterior volta a valer.

## 2.4. SAVEPOINT e desfazimento parcial

O `SAVEPOINT` cria um ponto de retorno dentro de uma transação:

```sql
BEGIN;
UPDATE quarto SET status = 'Manutenção' WHERE id_quarto = 101;
SAVEPOINT etapa1;
UPDATE quarto SET status = 'Manutenção' WHERE id_quarto = 201;
ROLLBACK TO SAVEPOINT etapa1;
COMMIT;
```

Somente a alteração **posterior** ao savepoint é desfeita; a primeira é confirmada. `RELEASE SAVEPOINT etapa1` libera esse ponto de retorno, mas **não confirma** a transação inteira.

## 2.5. Erros e estado de transação abortada

No PostgreSQL, se um comando provocar um erro dentro de uma transação explícita, ela normalmente passa para um estado de falha. Comandos posteriores podem retornar `current transaction is aborted` até que a situação seja tratada por `ROLLBACK` ou, quando aplicável, `ROLLBACK TO SAVEPOINT`. Isso impede continuar de forma inadvertida após uma operação que falhou.

## 2.6. Concorrência e isolamento

Duas sessões podem executar transações ao mesmo tempo. O nível de isolamento estabelece quais efeitos de outras transações são visíveis e quais anomalias podem ocorrer. O PostgreSQL utiliza **Read Committed** como nível padrão, mas também oferece **Repeatable Read** e **Serializable**. Garantir que uma reserva não conflite com outra pode exigir restrições e uma estratégia apropriada de concorrência; uma transação por si só não cria automaticamente essa regra.

## 2.7. Integração com procedures e triggers

Se uma procedure é chamada dentro de `BEGIN ... COMMIT`, seus comandos normalmente participam dessa transação. Da mesma forma, uma trigger que registra auditoria participa da transação que disparou a alteração. Não se deve presumir que `CALL` ou a execução de uma trigger façam uma confirmação automática das alterações.

### Questões — Unidade 2

**11.** Explique as quatro propriedades ACID e apresente um exemplo de cada uma no contexto do hotel.

**12.** Uma transação executa `BEGIN`, altera um quarto de `Disponível` para `Manutenção`, consulta o quarto e depois executa `ROLLBACK`. Qual status aparecerá dentro da transação? E depois do `ROLLBACK`?

**13.** Escreva uma transação que registre um pagamento de `360.00` para a reserva `1`, marque a reserva como `Concluída` e libere o quarto `101`. A transação deve ser confirmada ao final.

**14.** Explique a mensagem `current transaction is aborted, commands ignored until end of transaction block`. Qual comando normalmente resolve esse estado se não houver savepoint adequado?

**15.** Considere a sequência `BEGIN; UPDATE A; SAVEPOINT s1; UPDATE B; ROLLBACK TO SAVEPOINT s1; COMMIT;`. Quais atualizações permanecem? Explique.

**16.** Explique o que é *autocommit* e como ele se diferencia de `BEGIN ... COMMIT`.

**17.** Duas recepcionistas tentam confirmar a reserva do mesmo quarto para datas coincidentes. Qual propriedade ACID está mais relacionada ao controle da interferência entre as transações? O uso de `BEGIN` sozinho garante que não haverá reservas conflitantes?

**18.** Uma trigger registra uma auditoria após o `UPDATE` do status de uma reserva. A transação é desfeita. O que acontece com a mudança de status e com a auditoria?

**19.** Uma procedure é chamada dentro de `BEGIN ... ROLLBACK`. Em condições normais, as alterações que ela realizou são mantidas? Por quê?

**20.** Diferencie `ROLLBACK`, `ROLLBACK TO SAVEPOINT` e `RELEASE SAVEPOINT` e indique quando cada um seria útil.

---

# Unidade 3 — Views

## 3.1. Conceito

Uma **view** é uma consulta armazenada no banco, exposta por um nome e utilizada como uma tabela virtual. Ao contrário de uma tabela comum, a view tradicional **não armazena uma cópia independente do resultado**; sua definição é aplicada quando é consultada. Uma mudança nas tabelas-base pode modificar o resultado da view.

Views servem para **reutilizar consultas**, **reduzir repetição de joins**, **padronizar relatórios**, **abstrair a organização interna dos dados** e, com permissões corretamente configuradas, **limitar a exposição de informações**.

## 3.2. CREATE VIEW e consulta

```sql
CREATE VIEW vw_quartos_disponiveis AS
SELECT id_quarto, numero, status
FROM quarto
WHERE status = 'Disponível';

SELECT * FROM vw_quartos_disponiveis;
```

Note que a condição `WHERE` da definição passa a fazer parte do comportamento da view. Também é possível filtrar e ordenar o resultado ao consultá-la:

```sql
SELECT numero
FROM vw_quartos_disponiveis
ORDER BY numero;
```

## 3.3. Views com JOIN e agregação

```sql
CREATE VIEW vw_reservas_hospedes AS
SELECT r.id_reserva, h.nome AS hospede, r.status, r.valor_total
FROM reserva AS r
INNER JOIN hospede AS h ON h.id_hospede = r.id_hospede;
```

Outra possibilidade é uma view com resumo por hóspede:

```sql
CREATE VIEW vw_total_reservas_hospede AS
SELECT h.id_hospede, h.nome,
       COUNT(r.id_reserva) AS quantidade,
       COALESCE(SUM(r.valor_total), 0) AS total
FROM hospede AS h
LEFT JOIN reserva AS r ON r.id_hospede = h.id_hospede
GROUP BY h.id_hospede, h.nome;
```

Nesse caso, `LEFT JOIN` preserva hóspedes sem reservas; `COUNT(r.id_reserva)` retorna zero quando não há correspondência, e `COALESCE` substitui a soma `NULL` por zero.

## 3.4. CREATE OR REPLACE VIEW, DROP VIEW e dependências

`CREATE OR REPLACE VIEW` redefine uma view existente, desde que preserve as colunas anteriores em nome, ordem e tipo (novas colunas podem ser acrescentadas ao final). `DROP VIEW` remove a definição, sem remover as tabelas-base. Se outra view depender dela, o PostgreSQL pode impedir a remoção; `CASCADE` permite remover os objetos dependentes e deve ser usado com cuidado.

No `psql`, `\dv` lista views e `\d nome_da_view` mostra sua estrutura.

## 3.5. Views atualizáveis e WITH CHECK OPTION

Algumas views simples, construídas sobre uma única tabela e sem operações que impeçam a correspondência direta com suas linhas, podem aceitar `INSERT`, `UPDATE` e `DELETE`. Views com agregação normalmente **não são automaticamente atualizáveis**.

```sql
CREATE VIEW vw_hospedes_curitiba AS
SELECT id_hospede, nome, email, cidade
FROM hospede
WHERE cidade = 'Curitiba'
WITH CHECK OPTION;
```

`WITH CHECK OPTION` exige que inserções e atualizações **feitas por essa view** respeitem seu filtro. Assim, não é possível mudar a cidade para `Londrina` por meio dela e produzir um registro fora do conjunto permitido.

## 3.6. Views e segurança

Uma view pode mostrar `id_funcionario`, `nome` e `cargo` sem mostrar `salario`. **Isso só representa uma barreira efetiva de acesso** se os privilégios forem configurados de modo que o usuário possa consultar a view, mas não a tabela que contém o salário. Criar uma view, isoladamente, não revoga acessos existentes.

## 3.7. View comum versus materialized view

Uma **materialized view** armazena o resultado fisicamente, podendo ser útil em relatórios custosos. Como os dados materializados não são atualizados automaticamente a cada mudança das tabelas-base, é preciso executar `REFRESH MATERIALIZED VIEW`. Portanto, view comum prioriza dados atualizados conforme sua consulta; materialized view trabalha com uma cópia cujo conteúdo precisa ser renovado.

### Questões — Unidade 3

**21.** Explique a diferença entre tabela, view comum e materialized view. Qual dessas estruturas precisa de `REFRESH MATERIALIZED VIEW` para atualizar sua cópia do resultado?

**22.** Crie uma view `vw_quartos_disponiveis` que apresente `id_quarto`, `numero` e `status` apenas dos quartos disponíveis. Escreva um `SELECT` que consulte a view.

**23.** Crie uma view `vw_reservas_hospedes` com o identificador da reserva, o nome do hóspede, o status e o valor total. Utilize `INNER JOIN`.

**24.** Crie uma view que apresente todos os hóspedes, inclusive os sem reservas, com a quantidade de reservas de cada um. Por que utilizar `LEFT JOIN` e `COUNT(r.id_reserva)`?

**25.** Usando a view `vw_reservas_hospedes`, escreva uma consulta que liste reservas `Confirmada` com `valor_total > 500`, em ordem decrescente de valor.

**26.** Explique a finalidade de `CREATE OR REPLACE VIEW` e uma limitação importante desse comando no PostgreSQL.

**27.** O que acontece ao executar `DROP VIEW` em uma view utilizada por outra? Qual é o efeito de acrescentar `CASCADE`?

**28.** Uma view `vw_hospedes_curitiba` foi criada com `WHERE cidade = 'Curitiba' WITH CHECK OPTION`. O que acontece se tentarmos alterar a cidade de um registro para `Londrina` **por meio dessa view**?

**29.** Uma view de funcionários não apresenta o campo `salario`. Isso é suficiente para impedir que um usuário consulte salários? Explique o que deve ser configurado.

**30.** Explique duas vantagens e uma possível desvantagem de criar várias views que dependem umas das outras.

---

# Unidade 4 — Índices e análise de desempenho

## 4.1. O que é um índice?

Um índice é uma **estrutura auxiliar** associada a uma tabela, usada pelo SGBD para localizar registros de maneira eficiente em determinadas consultas. É semelhante ao índice remissivo de um livro: em vez de percorrer todas as páginas, a busca consulta um caminho organizado até a informação. No PostgreSQL, o tipo padrão é **B-tree**, adequado para várias comparações de igualdade, intervalos e ordenação.

```sql
CREATE INDEX idx_reserva_hospede ON reserva(id_hospede);
```

O índice não cria uma nova coluna e não altera o conteúdo da tabela.

## 4.2. Vantagens e custos

Índices podem acelerar acessos por `WHERE`, `JOIN` e alguns `ORDER BY`. Em contrapartida, consomem espaço em disco e precisam ser mantidos em operações `INSERT`, `UPDATE` e `DELETE`. Portanto, **mais índices nem sempre significam maior desempenho global**. Um índice é mais promissor quando recupera uma pequena parcela de uma tabela grande; isso se relaciona à **seletividade** da condição.

## 4.3. EXPLAIN e EXPLAIN ANALYZE

`EXPLAIN` mostra o **plano estimado** de execução. `EXPLAIN ANALYZE` **executa a instrução** e apresenta medições reais, incluindo tempos e quantidades de linhas. Por esse motivo, tome cuidado ao usá-lo com comandos que modificam dados.

```sql
EXPLAIN
SELECT * FROM reserva WHERE id_hospede = 10;

EXPLAIN ANALYZE
SELECT * FROM reserva WHERE id_hospede = 10;
```

- `Seq Scan`: leitura sequencial da tabela.
- `Index Scan`: acesso com auxílio de índice para localizar linhas.
- `Bitmap Index Scan` / `Bitmap Heap Scan`: estratégia que usa índice para organizar os acessos a várias linhas.

**Criar um índice não obriga o otimizador a utilizá-lo**. Em tabelas pequenas ou quando a consulta retorna grande parte das linhas, `Seq Scan` pode ser mais barato.

## 4.4. Índices automáticos e chaves

O PostgreSQL cria automaticamente índice único para suportar uma `PRIMARY KEY` ou uma restrição `UNIQUE`. Em contraste, declarar uma `FOREIGN KEY` **não cria automaticamente** índice na coluna da tabela que referencia outra. Dependendo dos joins, filtros e alterações na tabela referenciada, pode ser útil criá-lo manualmente.

## 4.5. Índice simples, composto, parcial e por expressão

**Simples:** uma coluna.

```sql
CREATE INDEX idx_reserva_status ON reserva(status);
```

**Composto:** mais de uma coluna; a ordem importa para os padrões de consulta atendidos. Em índices B-tree, condições sobre colunas iniciais costumam ser especialmente relevantes.

```sql
CREATE INDEX idx_reserva_hospede_status
ON reserva(id_hospede, status);
```

**Parcial:** indexa somente linhas que satisfazem uma condição.

```sql
CREATE INDEX idx_reserva_confirmada_checkin
ON reserva(data_checkin) WHERE status = 'Confirmada';
```

**Por expressão:** indexa o resultado de uma expressão.

```sql
CREATE INDEX idx_hospede_email_minusculo
ON hospede(LOWER(email));
```

## 4.6. Administrando índices

```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'reserva';

DROP INDEX IF EXISTS idx_reserva_status;
```

O comando `ANALYZE reserva;` atualiza estatísticas que ajudam o otimizador a estimar planos. Para avaliar um índice, compare planos e tempos **em dados representativos**, não apenas em tabelas com poucos registros.

### Questões — Unidade 4

**31.** Defina índice e explique uma vantagem e dois custos de sua utilização.

**32.** Escreva comandos para criar um índice `idx_hospede_email` em `hospede(email)`, listar os índices dessa tabela usando SQL e remover o índice criado.

**33.** Diferencie `Seq Scan` e `Index Scan`. Por que uma consulta pode continuar usando `Seq Scan` mesmo depois da criação de um índice?

**34.** Diferencie `EXPLAIN` de `EXPLAIN ANALYZE`. Que cuidado é necessário ao analisar uma instrução `UPDATE` com `EXPLAIN ANALYZE`?

**35.** Quais restrições criam automaticamente índices no PostgreSQL: `PRIMARY KEY`, `UNIQUE` e `FOREIGN KEY`? Explique a diferença.

**36.** Para a consulta `SELECT * FROM reserva WHERE id_hospede = 10 AND status = 'Confirmada';`, proponha um índice composto e explique por que a ordem das colunas é relevante.

**37.** Em uma tabela com 1 milhão de hóspedes, `email` tem valores quase únicos, enquanto `cidade` repete poucos valores. Qual coluna tende a oferecer buscas por igualdade mais seletivas? Isso garante uso do índice?

**38.** Crie um índice parcial sobre `reserva(data_checkin)` que inclua somente reservas com status `Confirmada`. Explique quando ele pode ser útil.

**39.** Uma aplicação consulta frequentemente `WHERE LOWER(email) = 'ana@exemplo.com'`. Crie um índice apropriado e explique por que um índice simples em `email` não é exatamente o mesmo.

**40.** Explique um processo responsável para decidir se um índice deve ser criado. Inclua o papel de `EXPLAIN ANALYZE`, o tamanho da tabela e a frequência de escrita.

---

# Unidade 5 — Usuários, roles e permissões

## 5.1. Segurança: autenticação e autorização

**Autenticação** verifica **quem** está tentando acessar o SGBD; **autorização** determina **o que** essa identidade pode fazer após conectar. No PostgreSQL, o controle de acesso combina *roles*, atributos de login, concessão de privilégios e políticas de conexão do servidor. Criar uma senha não garante, por si só, que um cliente consiga se conectar; a configuração de autenticação também deve permitir a conexão.

## 5.2. CREATE ROLE e CREATE USER

Uma **role** é uma identidade que pode receber privilégios e participar de outras roles. `LOGIN` permite autenticação como aquela role; `NOLOGIN` é adequado para papéis que apenas agrupam permissões. `CREATE USER` é uma conveniência para criar uma role com `LOGIN`.

```sql
CREATE ROLE papel_recepcao NOLOGIN;
CREATE USER usuario_recepcao;
GRANT papel_recepcao TO usuario_recepcao;
```

A role `papel_recepcao` representa um **perfil**; `usuario_recepcao` representa uma **conta que pode conectar**. A herança efetiva de permissões depende dos atributos de participação e da configuração da role. As roles são definidas no **cluster PostgreSQL**, não somente em um banco isolado.

## 5.3. GRANT e REVOKE

`GRANT` concede privilégios; `REVOKE` retira concessões especificadas. Principais privilégios de tabelas: `SELECT`, `INSERT`, `UPDATE`, `DELETE`. Também existem permissões em outros objetos e níveis.

```sql
GRANT SELECT ON hospede, quarto TO papel_recepcao;
GRANT SELECT, INSERT ON reserva TO papel_recepcao;
GRANT UPDATE (status) ON reserva TO papel_recepcao;
REVOKE INSERT ON reserva FROM papel_recepcao;
```

O último comando retira a permissão de inserção **concedida àquela role**; se outro caminho de privilégios existir, a operação ainda poderá ser permitida.

## 5.4. Banco, schema, tabela e coluna

Uma operação costuma exigir uma combinação de autorizações:

- `CONNECT` no **database**;
- `USAGE` no **schema**;
- privilégios como `SELECT` ou `UPDATE` na **tabela/view**, ou permissões em determinadas colunas.

```sql
GRANT CONNECT ON DATABASE hotel_seguranca TO papel_recepcao;
GRANT USAGE ON SCHEMA public TO papel_recepcao;
GRANT SELECT ON hospede TO papel_recepcao;
```

Permissões em sequências também podem ser necessárias quando a aplicação usa certos mecanismos de geração de identificadores, dependendo de como a coluna foi definida.

## 5.5. Controle de acesso com views

```sql
CREATE VIEW vw_funcionarios_publico AS
SELECT id_funcionario, nome, cargo
FROM funcionario;

GRANT SELECT ON vw_funcionarios_publico TO papel_recepcao;
```

O usuário da recepção pode consultar a view sem necessariamente possuir acesso à tabela `funcionario` (considerando a configuração usual da view e as demais permissões). A privacidade do salário depende também de **não conceder acesso direto indevido** à tabela original.

## 5.6. Inspeção e testes

No `psql`:

| Comando | Finalidade |
|---|---|
| `\du` | Ver roles e atributos |
| `\dp` ou `\z` | Ver privilégios em objetos |
| `\dn+` | Ver schemas e permissões |
| `\conninfo` | Ver conexão atual |

`SET ROLE papel_recepcao;` pode ser usado para trocar a role efetiva dentro de uma sessão autorizada. `current_user` identifica a role efetiva; `session_user`, a identidade que estabeleceu a sessão (salvo alterações administrativas autorizadas). Para testar autenticação real, é necessário conectar como a conta pretendida.

## 5.7. Princípio do menor privilégio

Conceda somente as operações necessárias para cada setor. Uma recepcionista não precisa ler salários nem alterar preços apenas porque consulta quartos; o financeiro não precisa apagar hóspedes apenas porque registra pagamentos. Recomenda-se agrupar privilégios por função e realizar testes tanto de **operações permitidas** quanto de **operações negadas**.

### Questões — Unidade 5

**41.** Diferencie autenticação e autorização. Dê um exemplo de cada uma no cenário do hotel.

**42.** Qual é a diferença entre `CREATE ROLE papel_auditoria NOLOGIN` e `CREATE USER usuario_auditor`? Por que pode ser útil associar a conta de login a uma role de perfil?

**43.** Escreva comandos `GRANT` que permitam à role `papel_auditoria` conectar ao banco `hotel_seguranca`, utilizar o schema `public` e consultar a tabela `reserva`.

**44.** Escreva comandos para criar `papel_recepcao`, permitir `SELECT` em `hospede` e `quarto`, e permitir somente `UPDATE` na coluna `status` de `reserva` (sem conceder atualização de outras colunas).

**45.** Explique o efeito de `REVOKE UPDATE (status) ON reserva FROM papel_recepcao;`. Isso garante, em todas as circunstâncias, que ninguém dessa role poderá modificar o status? Justifique.

**46.** Crie a view `vw_funcionarios_publico`, mostrando `id_funcionario`, `nome` e `cargo`, mas não `salario`. Conceda permissão para `papel_recepcao` consultá-la e explique uma condição necessária para proteger realmente os salários.

**47.** Um usuário consegue conectar ao PostgreSQL, mas recebe `permission denied for table reserva` ao executar `SELECT * FROM reserva`. Que níveis e privilégios devem ser verificados?

**48.** Explique a diferença entre `session_user` e `current_user` e o objetivo de `SET ROLE`.

**49.** Um usuário pode consultar hóspedes, mas não deve excluí-los. Quais privilégios seriam suficientes para permitir a consulta sem conceder exclusão? Mostre um exemplo de `GRANT`.

**50.** Proponha uma política de menor privilégio para três perfis do hotel: recepção, financeiro e auditoria. Indique pelo menos duas operações permitidas e uma proibida para cada perfil.

---

# Unidade 6 — NoSQL e MongoDB com Docker

## 6.1. Conceito de NoSQL e modelos

**NoSQL** é um conjunto de abordagens de armazenamento que não se limita às tabelas relacionais. Modelos comuns incluem **chave–valor**, **documentos**, **grafos** e **colunas amplas**. MongoDB é orientado a **documentos**: cada registro pode conter campos simples, objetos aninhados e arrays. Isso não significa que todo banco NoSQL dispense esquema ou que qualquer modelagem seja automaticamente melhor que a relacional.

## 6.2. Banco, coleção, documento e BSON

| PostgreSQL | MongoDB | Observação |
|---|---|---|
| Database | Database | Agrupa os dados da aplicação |
| Tabela | Collection | Agrupa documentos |
| Linha | Document | Pode conter estruturas aninhadas |
| Coluna | Field | Propriedade de um documento |
| Chave primária | `_id` | Identificador único do documento |

MongoDB utiliza **BSON** para armazenar documentos, um formato relacionado ao JSON que oferece tipos adicionais, como datas. Exemplo:

```javascript
{
  _id: 1,
  nome: "Ana Martins",
  cidade: "Curitiba",
  contato: { email: "ana@exemplo.com", telefone: "41999990001" },
  tags: ["frequente", "corporativo"]
}
```

`contato` é um objeto aninhado; `tags` é um array. Para as reservas do hotel didático, `hospedeId` e `quartoId` são referências que a aplicação interpreta; **não são chaves estrangeiras SQL aplicadas automaticamente pelo MongoDB**.

## 6.3. Docker, imagem, contêiner e volume

Docker executa o servidor MongoDB em um **contêiner**, criado a partir de uma **imagem**. O Docker Compose usa um arquivo YAML para declarar o serviço, as portas, as variáveis de ambiente e um **volume persistente**. O volume protege os dados contra a simples remoção do contêiner.

Exemplo local:

```yaml
services:
  mongo:
    image: mongo:8.0
    container_name: mongo_hotel_aula
    ports:
      - "127.0.0.1:27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin_aula
      MONGO_INITDB_ROOT_PASSWORD: senha_apenas_de_laboratorio
    volumes:
      - mongo_hotel_dados:/data/db
volumes:
  mongo_hotel_dados:
```

A senha ilustrativa não deve ser utilizada em produção. No Windows, normalmente usa-se Docker Desktop com WSL 2; no Ubuntu, Docker Engine e Compose. Após criar o arquivo `docker-compose-hotel-nosql.yml`, os comandos básicos são:

```bash
docker compose -f docker-compose-hotel-nosql.yml up -d
docker compose -f docker-compose-hotel-nosql.yml ps
docker exec -it mongo_hotel_aula mongosh -u admin_aula --authenticationDatabase admin
```

O último comando solicita a senha e abre o **mongosh** dentro do contêiner. No Ubuntu, a instalação pode exigir `sudo` antes de `docker`.

Dentro do **mongosh**:

```javascript
use hotel_nosql
show collections
```

## 6.4. Inserção de documentos

```javascript
db.hospedes.insertOne({
  _id: 20, nome: "Luiza Teste", cidade: "Curitiba",
  contato: { email: "luiza@exemplo.com" }, tags: ["novo"]
})
```

`insertOne` insere um documento, e `insertMany` recebe um array de documentos. `_id` deve ser único.

## 6.5. Consultas, filtros, projeção e operadores

```javascript
db.hospedes.find({ cidade: "Curitiba" })
db.hospedes.find({}, { nome: 1, cidade: 1, _id: 0 })
db.quartos.find({ diaria: { $gt: 250 } }).sort({ diaria: -1 })
db.hospedes.find({ "contato.email": "ana@exemplo.com" })
db.hospedes.find({ tags: "corporativo" })
```

O primeiro objeto de `find(filtro, projecao)` define **quais documentos** serão retornados; o segundo, **quais campos** serão exibidos. Operadores comuns são `$gt`, `$gte`, `$lt`, `$lte`, `$ne`, `$in`, `$or`. `sort({ diaria: -1 })` ordena de modo decrescente.

## 6.6. Atualização e exclusão

```javascript
db.hospedes.updateOne({ _id: 20 }, { $set: { cidade: "Maringá" } })
db.hospedes.updateOne({ _id: 20 }, { $push: { tags: "vip" } })
db.quartos.updateOne({ _id: 301 }, { $inc: { diaria: 10 } })
db.hospedes.deleteOne({ _id: 20 })
```

- `$set`: atribui/substitui um valor.
- `$push`: acrescenta elemento a um array.
- `$inc`: incrementa um campo numérico.
- `$unset`: remove um campo.
- `deleteOne`: remove um documento correspondente; `deleteMany`: pode remover vários. Um filtro vazio em `deleteMany({})` atinge **todos os documentos da coleção**.

## 6.7. Agregações e relacionamentos

Um **pipeline** de agregação processa documentos em estágios:

```javascript
db.reservas.aggregate([
  { $match: { status: "Confirmada" } },
  { $group: { _id: "$hospedeId", quantidade: { $sum: 1 }, total: { $sum: "$valorTotal" } } },
  { $sort: { total: -1 } }
])
```

`$match` filtra, `$group` agrupa e calcula, `$sort` ordena. `$lookup` combina dados de coleções, aproximando-se da finalidade de um `JOIN` em consultas SQL. Em MongoDB também é possível **incorporar** dados ao documento (*embedding*), em vez de manter apenas referências; a escolha depende do padrão de acesso e atualização da aplicação.

## 6.8. Índices, persistência e encerramento

```javascript
db.hospedes.createIndex({ "contato.email": 1 }, { unique: true })
db.hospedes.getIndexes()
```

Índices no MongoDB, assim como no PostgreSQL, auxiliam buscas específicas e possuem custos de manutenção. Para encerrar o ambiente **sem remover o volume**:

```bash
docker compose -f docker-compose-hotel-nosql.yml down
```

Para reiniciar:

```bash
docker compose -f docker-compose-hotel-nosql.yml up -d
```

**Cuidado:** `down -v` também remove volumes gerenciados pelo projeto e pode apagar os dados do laboratório.

### Questões — Unidade 6

**51.** Explique o que significa NoSQL e diferencie, de forma resumida, os modelos chave–valor, documentos e grafos. Qual deles é utilizado pelo MongoDB?

**52.** Diferencie banco, coleção, documento, campo, `_id` e BSON. No documento `{ _id: 1, contato: { email: "ana@exemplo.com" }, tags: ["vip"] }`, identifique o objeto aninhado e o array.

**53.** Explique o papel de imagem, contêiner, Docker Compose, mapeamento de porta e volume. O que ocorre com os dados quando executamos `docker compose down` sem `-v`?

**54.** Escreva os comandos para iniciar o MongoDB com o arquivo `docker-compose-hotel-nosql.yml`, verificar os serviços, acessar o `mongosh` no contêiner `mongo_hotel_aula` como `admin_aula` e selecionar `hotel_nosql`.

**55.** Escreva um `insertOne` para inserir um hóspede de `_id: 20`, nome `Luiza Teste`, cidade `Curitiba`, email `luiza@exemplo.com` dentro de `contato` e tag `novo`. Qual problema ocorre se inserirmos novamente outro documento com `_id: 20`?

**56.** Escreva uma consulta que retorne somente `nome` e `cidade` dos hóspedes de `Curitiba`, ocultando `_id`. Em seguida, escreva uma consulta para listar quartos com `diaria > 250`, ordenados do mais caro ao mais barato.

**57.** Diferencie `$set`, `$push`, `$inc` e `$unset`. Escreva um comando para acrescentar a tag `vip` ao hóspede de `_id: 1`, sem substituir suas tags existentes.

**58.** Escreva um comando para excluir somente o hóspede de `_id: 20`. Por que `db.hospedes.deleteMany({})` representa um risco nesse laboratório?

**59.** Escreva uma agregação que retorne a quantidade de reservas por status utilizando `$group`. Explique a finalidade de `$match` e `$lookup`.

**60.** Escreva o comando MongoDB para criar um índice único em `hospedes.contato.email`. Depois explique por que a existência de um volume é importante quando interrompemos e reiniciamos o contêiner.

---

# Orientações para a entrega

Responda às questões **1 a 60**, preservando a numeração. Nas questões que exigem SQL ou JavaScript, apresente os comandos completos com a sintaxe apropriada. Em questões discursivas, responda com suas próprias palavras, demonstrando o conceito e relacionando-o ao cenário apresentado.

**Importante:** esta é uma lista de revisão; exemplos de comandos podem ter mais de uma solução correta. O gabarito comentado é disponibilizado separadamente.
