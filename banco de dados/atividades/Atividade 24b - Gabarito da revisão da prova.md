# Gabarito comentado — Revisão de Banco de Dados

**Correspondente à lista:** `revisao_banco_dados_pos_prova.md`  
**Conteúdos:** procedures e triggers; transações e ACID; views; índices; usuários, roles e permissões; NoSQL e MongoDB.

> **Orientações de correção:** os códigos abaixo apresentam soluções de referência. Outras soluções estão corretas se preservarem o objetivo, a semântica e as restrições da questão. Os exemplos pressupõem o banco de hotel descrito na lista; se as colunas ou os identificadores diferirem na instalação do aluno, serão necessárias adaptações. Em PostgreSQL, execute exemplos que criam funções, triggers e views em banco de testes; objetos de mesmo nome devem ser criados apenas uma vez.

---

# Unidade 1 — Procedures e triggers

## 1. Procedure × trigger

Uma **procedure** é invocada explicitamente, normalmente por `CALL`, para executar um conjunto de comandos. Por exemplo, a recepção solicita o cancelamento de uma reserva. Uma **trigger** é disparada automaticamente em consequência de um evento de banco (`INSERT`, `UPDATE` ou `DELETE`) previamente configurado. Por exemplo, sempre que o status de uma reserva muda, uma trigger registra o valor anterior e o novo em uma tabela de auditoria. Logo, a primeira organiza uma operação solicitada; a segunda reage a eventos de persistência.

## 2. Procedure que conclui reserva

```sql
CREATE OR REPLACE PROCEDURE sp_concluir_reserva(p_id BIGINT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE reserva
    SET status = 'Concluída'
    WHERE id_reserva = p_id;
END;
$$;

CALL sp_concluir_reserva(1);
```

**Comentário:** `p_id` é o parâmetro recebido; o `WHERE` é essencial para não atualizar todas as reservas. Criar a procedure não a executa. Se nenhuma reserva com esse ID existir, o `UPDATE` simplesmente afetará zero linhas; uma implementação mais robusta pode verificar isso e emitir um erro.

## 3. BEFORE / AFTER e ROW / STATEMENT

`BEFORE` executa o gatilho antes da alteração; é adequado para validar dados ou ajustar `NEW` antes da gravação. `AFTER` atua após o evento para a operação, sendo apropriado para auditorias. `FOR EACH ROW` executa para cada linha afetada; `FOR EACH STATEMENT` executa uma vez por comando. Para validar cada reserva na inserção, a escolha mais natural é **`BEFORE INSERT ... FOR EACH ROW`**, pois precisamos verificar as datas específicas de cada linha.

## 4. Disponibilidade de NEW e OLD

| Evento | `NEW` | `OLD` |
|---|---|---|
| `INSERT` | Nova linha disponível | Não disponível |
| `UPDATE` | Versão nova da linha | Versão anterior da linha |
| `DELETE` | Não disponível | Linha que está sendo excluída |

O uso de `NEW.status` e `OLD.status` é típico de uma atualização. Essas variáveis especiais se referem à linha processada por uma trigger por linha.

## 5. Função de validação e trigger

```sql
CREATE OR REPLACE FUNCTION fn_validar_datas_reserva()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.data_checkout <= NEW.data_checkin THEN
        RAISE EXCEPTION 'Checkout deve ocorrer depois do checkin';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_validar_datas_reserva
BEFORE INSERT ON reserva
FOR EACH ROW
EXECUTE FUNCTION fn_validar_datas_reserva();
```

**Comentário:** `RAISE EXCEPTION` rejeita a operação inválida e `RETURN NEW` mantém o fluxo de inserção quando o período é válido. Em um sistema real, um `CHECK (data_checkout > data_checkin)` também implementa muito bem essa regra simples. A trigger foi pedida para praticar a automação.

## 6. Condição do trigger de auditoria

A trigger é disparada depois de um `UPDATE` que mencione a coluna `status` e examina **cada linha** afetada. O `WHEN (OLD.status IS DISTINCT FROM NEW.status)` garante que a função só execute se o status realmente mudar; atualizar uma linha com o mesmo valor não gera registro de auditoria. A comparação trata corretamente possíveis valores `NULL`.

## 7. Valores esperados na auditoria

A tabela de auditoria deve receber:

```text
status_anterior = 'Confirmada'
status_novo     = 'Cancelada'
```

`OLD` indica a versão anterior da linha; `NEW`, a versão produzida pela atualização.

## 8. CHECK ou trigger para valores positivos?

Para a regra simples “o valor deve ser positivo”, **`CHECK` é a escolha preferencial**:

```sql
ALTER TABLE pagamento
ADD CONSTRAINT pagamento_valor_positivo CHECK (valor > 0);
```

Restrições declarativas são diretas, concisas e aplicadas pelo SGBD. Uma trigger pode fazer validações mais complexas ou executar efeitos adicionais, mas geralmente é desnecessária aqui. Se a tabela já possui esse `CHECK`, não crie uma restrição duplicada.

## 9. Quantidade de execuções

Se o `UPDATE` altera quatro linhas e a trigger é aplicável ao comando, uma trigger **`FOR EACH ROW`** executa quatro vezes (uma por linha). Uma trigger **`FOR EACH STATEMENT`** executa uma vez para o comando, independentemente de afetar quatro linhas. O resultado de `WHEN` poderia restringir o número de execuções por linha caso essa cláusula também estivesse presente.

## 10. Auditoria após ROLLBACK

**Não permanece**, desde que a auditoria tenha sido inserida pela trigger na mesma transação normal do `UPDATE`. O `ROLLBACK` desfaz tanto a alteração da reserva quanto o registro de auditoria. Essa consequência é uma manifestação da **atomicidade**.

---

# Unidade 2 — Transações e ACID

## 11. As quatro propriedades ACID

| Propriedade | Explicação | Exemplo |
|---|---|---|
| **Atomicidade** | Ou todas as operações da transação são confirmadas ou nenhuma permanece | Pagamento e fechamento da reserva são confirmados juntos |
| **Consistência** | Uma transação válida deve respeitar as regras do banco | Uma `FOREIGN KEY` impede pagamento associado a reserva inexistente |
| **Isolamento** | Controla o efeito e a visibilidade de operações simultâneas | Duas recepcionistas executam transações sobre o mesmo quarto |
| **Durabilidade** | Alterações confirmadas continuam persistidas de acordo com as garantias do sistema | Após `COMMIT`, uma queda seguida de recuperação não deve apagar a confirmação |

**Observação:** isolamento não significa necessariamente que todas as transações sempre se comportam como uma execução estritamente serial; isso depende do nível de isolamento.

## 12. UPDATE seguido de ROLLBACK

**Dentro da própria transação**, após o `UPDATE`, o `SELECT` mostra `Manutenção`. Após o `ROLLBACK`, a alteração é desfeita e o quarto volta ao status que tinha antes de `BEGIN` (no enunciado, `Disponível`). O resultado se refere à própria sessão; outras sessões não necessariamente veem alterações não confirmadas.

## 13. Checkout em transação

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

**Comentário:** essa solução demonstra a estrutura pedida. Pressupõe que os identificadores existam, que não haja restrições impedindo o procedimento e que não se esteja duplicando um pagamento indevidamente. Em uma implementação real, a transação precisaria validar a reserva, o quarto correto, a ausência de pagamento duplicado e as regras de negócio antes de confirmar.

## 14. `current transaction is aborted`

O PostgreSQL informa que um comando anterior falhou e que a transação explícita ficou em estado de erro. Em geral, novos comandos serão ignorados até que a transação seja encerrada adequadamente. O comando mais comum é:

```sql
ROLLBACK;
```

Caso um `SAVEPOINT` apropriado tenha sido criado antes do erro, pode ser possível recuperar parcialmente a transação por `ROLLBACK TO SAVEPOINT nome;`.

## 15. SAVEPOINT e persistência

Permanece somente **`UPDATE A`**. O `SAVEPOINT s1` cria um ponto de retorno depois de A. O `ROLLBACK TO SAVEPOINT s1` desfaz B; o `COMMIT` confirma A. É possível utilizar savepoints para descartar etapas intermediárias sem perder tudo o que veio antes.

## 16. Autocommit

Com o comportamento usual de autocommit, cada instrução executada isoladamente é confirmada ao terminar com sucesso. Já `BEGIN ... COMMIT` agrupa diversas operações em uma única transação explícita; elas são confirmadas em conjunto. Se necessário, um `ROLLBACK` pode descartar as operações ainda não confirmadas.

## 17. Concorrência de reservas

A propriedade mais diretamente ligada ao controle da interferência entre transações é **isolamento**. **Não**, o uso de `BEGIN` por si só não impede reservas conflitantes. É necessário projetar regras de negócio e mecanismos de concorrência adequados, como restrições apropriadas, bloqueios ou estratégia de serialização das reservas, conforme o modelo da aplicação.

## 18. Trigger e rollback

Tanto a atualização do status quanto a inserção de auditoria são desfeitas, pois fazem parte da mesma transação. Uma trigger normal não realiza uma transação independente do comando que a disparou.

## 19. Procedure chamada em transação

Normalmente **não**: se a procedure é chamada dentro de uma transação explícita e seus comandos participam dela, `ROLLBACK` desfaz suas alterações. O `CALL` não equivale automaticamente a `COMMIT`. O PostgreSQL possui regras específicas para controle de transação em procedures, mas esse comportamento não está implícito na situação descrita.

## 20. Três comandos de controle

- `ROLLBACK;`: desfaz toda a transação ativa e a encerra.
- `ROLLBACK TO SAVEPOINT s1;`: desfaz as operações posteriores a `s1`, preservando a transação e o trabalho anterior ao savepoint.
- `RELEASE SAVEPOINT s1;`: libera o savepoint; não confirma a transação inteira.

Exemplo: ao registrar a saída do hóspede, um savepoint permitiria refazer somente uma etapa facultativa sem descartar uma alteração anterior válida.

---

# Unidade 3 — Views

## 21. Tabela × view × materialized view

Uma **tabela** armazena registros; uma **view** comum armazena a definição de uma consulta usada como tabela virtual e, em geral, consulta os dados atuais das tabelas-base; uma **materialized view** armazena fisicamente o resultado de uma consulta. É esta última que precisa de:

```sql
REFRESH MATERIALIZED VIEW nome_da_view;
```

para renovar sua cópia do resultado.

## 22. View dos quartos disponíveis

```sql
CREATE VIEW vw_quartos_disponiveis AS
SELECT id_quarto, numero, status
FROM quarto
WHERE status = 'Disponível';

SELECT * FROM vw_quartos_disponiveis;
```

A view restringe o conjunto de quartos na definição. Um `SELECT` posterior pode acrescentar projeções, ordenação e filtros.

## 23. View de reservas e hóspedes

```sql
CREATE VIEW vw_reservas_hospedes AS
SELECT r.id_reserva,
       h.nome AS hospede,
       r.status,
       r.valor_total
FROM reserva AS r
INNER JOIN hospede AS h
    ON h.id_hospede = r.id_hospede;
```

O `INNER JOIN` associa reservas aos hóspedes por suas chaves. A expressão `h.nome AS hospede` define um nome claro para o resultado.

## 24. Resumo incluindo hóspedes sem reserva

```sql
CREATE VIEW vw_quantidade_reservas_hospede AS
SELECT h.id_hospede,
       h.nome,
       COUNT(r.id_reserva) AS quantidade_reservas
FROM hospede AS h
LEFT JOIN reserva AS r
    ON r.id_hospede = h.id_hospede
GROUP BY h.id_hospede, h.nome;
```

**`LEFT JOIN`** preserva todos os hóspedes, mesmo quando não existe reserva. **`COUNT(r.id_reserva)`** conta somente IDs de reservas não nulos e retorna `0` para hóspedes sem correspondência. `COUNT(*)` não seria uma escolha equivalente nesse `LEFT JOIN`, pois contaria a linha preservada do hóspede sem reserva.

## 25. Filtro e ordenação sobre uma view

```sql
SELECT id_reserva, hospede, status, valor_total
FROM vw_reservas_hospedes
WHERE status = 'Confirmada'
  AND valor_total > 500
ORDER BY valor_total DESC;
```

A view permite escrever o relatório sem repetir o `JOIN` entre `reserva` e `hospede`.

## 26. CREATE OR REPLACE VIEW

Redefine uma view existente, evitando removê-la para mudanças compatíveis. No PostgreSQL, a nova definição **deve preservar nomes, tipos e ordem das colunas já existentes**; novas colunas podem ser acrescentadas ao final. Alterações incompatíveis podem exigir uma estratégia mais elaborada, levando em conta objetos dependentes.

## 27. DROP VIEW e CASCADE

Se outra view depende da view que será removida, o PostgreSQL normalmente impede o `DROP VIEW` padrão (`RESTRICT`). `DROP VIEW nome CASCADE;` remove a view **e os objetos que dependem dela**. Não apaga automaticamente as tabelas-base, mas pode eliminar outras views e dependências relevantes; por isso deve ser utilizado com cautela.

## 28. WITH CHECK OPTION

Se a atualização é feita **pela view**, o PostgreSQL rejeita alterar `cidade` para `Londrina`, pois o registro deixaria de satisfazer `WHERE cidade = 'Curitiba'`. `WITH CHECK OPTION` controla inserções/atualizações efetuadas por views atualizáveis; não é uma proibição global de modificar o registro pela tabela original.

## 29. View e proteção do salário

**Não basta criar a view.** O usuário também não pode ter privilégio para consultar o salário diretamente na tabela `funcionario` (nem por outro caminho autorizado). Uma possibilidade é conceder `SELECT` somente à view e não conceder leitura da tabela-base. Na configuração usual, o PostgreSQL verifica os privilégios subjacentes pela role proprietária da view, salvo modos/configurações específicas. O importante é controlar corretamente os privilégios.

## 30. Vantagens e desvantagens de views encadeadas

**Vantagens:** (1) reduzem repetição de joins e fórmulas; (2) padronizam as definições usadas por relatórios diferentes. **Possível desvantagem:** muitas dependências podem dificultar manutenção, compreensão dos planos de execução e alterações de definição. Também podem ocultar consultas de custo elevado.

---

# Unidade 4 — Índices e análise de desempenho

## 31. Índice e trade-offs

É uma estrutura auxiliar que organiza referências para localizar linhas de forma eficiente em determinadas buscas. **Vantagem:** pode acelerar consultas seletivas por filtros, relações e algumas ordenações. **Custos:** (1) ocupa armazenamento; (2) pode tornar `INSERT`, `UPDATE` e `DELETE` mais caros, pois o SGBD precisa manter o índice. Por isso não se deve indexar todas as colunas indiscriminadamente.

## 32. Criar, listar e remover índice

```sql
CREATE INDEX idx_hospede_email
ON hospede(email);

SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'hospede';

DROP INDEX IF EXISTS idx_hospede_email;
```

No `psql`, `\d hospede` também mostra índices existentes. Não confunda índice comum com o índice que mantém uma constraint `UNIQUE` ou `PRIMARY KEY`.

## 33. Seq Scan × Index Scan

`Seq Scan` percorre a tabela sequencialmente. `Index Scan` utiliza um índice para auxiliar a localização das linhas. O índice pode ser ignorado porque a tabela é pequena, grande parte das linhas atende ao filtro ou o custo previsto do acesso por índice é maior. O otimizador **seleciona** a estratégia; criar índice não a impõe.

## 34. EXPLAIN × EXPLAIN ANALYZE

`EXPLAIN` mostra um plano estimado. `EXPLAIN ANALYZE` **executa a instrução** e mostra métricas reais. Portanto, `EXPLAIN ANALYZE UPDATE ...` modifica dados de verdade. Para medir sem preservar a alteração, pode-se executar o comando em uma transação e desfazê-la:

```sql
BEGIN;
EXPLAIN ANALYZE
UPDATE quarto
SET status = 'Manutenção'
WHERE id_quarto = 101;
ROLLBACK;
```

Esse teste ainda executa a operação e seus possíveis gatilhos; use um banco de testes e avalie efeitos externos de integrações, caso existam.

## 35. Restrições e índices automáticos

- `PRIMARY KEY`: **sim**, cria índice único para a chave.
- `UNIQUE`: **sim**, cria índice único para dar suporte à restrição.
- `FOREIGN KEY`: **não**, a definição da chave estrangeira não cria automaticamente um índice na coluna da tabela referenciadora.

Uma chave estrangeira muito usada em `JOIN` e filtros pode merecer índice explícito na tabela filha.

## 36. Índice composto

```sql
CREATE INDEX idx_reserva_hospede_status
ON reserva(id_hospede, status);
```

Ele é compatível com a consulta que filtra por `id_hospede` e `status`. A ordem importa porque a organização B-tree favorece determinados padrões de acesso, especialmente condições sobre as colunas iniciais. A escolha ideal deve considerar as consultas reais, não apenas uma regra fixa.

## 37. Seletividade

`email` tende a ser mais seletivo, pois normalmente identifica uma parcela muito pequena dos registros. Uma cidade presente em muitas linhas tende a selecionar um conjunto maior. **Isso não garante** que um índice será utilizado: o otimizador também avalia quantidade de linhas, estatísticas, custo de acesso, ordenação e outros fatores.

## 38. Índice parcial

```sql
CREATE INDEX idx_reserva_confirmada_checkin
ON reserva(data_checkin)
WHERE status = 'Confirmada';
```

Ele armazena entradas somente de reservas confirmadas. Pode beneficiar consultas frequentes sobre datas de check-in **que também restringem as reservas às confirmadas**. Sua condição deve ser reconhecida pelo planejamento da consulta.

## 39. Índice por expressão

```sql
CREATE INDEX idx_hospede_email_lower
ON hospede(LOWER(email));
```

A consulta aplica `LOWER(email)`, não usa diretamente o valor bruto da coluna. O índice por expressão guarda o resultado da transformação, podendo atender a essa forma de filtro. Um índice simples em `email` não é automaticamente equivalente para todos os planos dessa expressão.

## 40. Processo de análise de índices

Uma abordagem adequada é: (1) identificar a consulta que realmente precisa melhorar; (2) obter `EXPLAIN ANALYZE` em ambiente controlado; (3) observar scans, linhas retornadas e tempo; (4) verificar índices já existentes e o volume de dados; (5) criar **um índice compatível com o padrão de filtro ou join**; (6) atualizar estatísticas, quando necessário, e comparar novamente; (7) avaliar custo extra de gravação e espaço. Com tabelas pequenas, o ganho pode não aparecer.

---

# Unidade 5 — Usuários, roles e permissões

## 41. Autenticação × autorização

**Autenticação:** confirma a identidade de quem tenta conectar; por exemplo, a recepcionista entra com a própria conta e senha. **Autorização:** determina o que essa conta pode fazer; por exemplo, consultar hóspedes, mas não visualizar o salário de funcionários.

## 42. Role sem login × usuário

```sql
CREATE ROLE papel_auditoria NOLOGIN;
CREATE USER usuario_auditor;
```

`papel_auditoria` não se conecta diretamente; serve como perfil de privilégios. `CREATE USER` cria uma role com capacidade de login. Podemos associá-las:

```sql
GRANT papel_auditoria TO usuario_auditor;
```

Assim, as permissões são administradas por **perfil**, em vez de serem concedidas individualmente a cada pessoa. O funcionamento da herança depende das opções de participação/roles configuradas.

## 43. Permissões no banco, schema e tabela

```sql
GRANT CONNECT ON DATABASE hotel_seguranca TO papel_auditoria;
GRANT USAGE ON SCHEMA public TO papel_auditoria;
GRANT SELECT ON TABLE reserva TO papel_auditoria;
```

Esses três níveis são importantes: conectar ao banco não significa poder usar todos os schemas e tabelas. Os comandos devem ser executados por uma conta que tenha autoridade para conceder esses privilégios.

## 44. Role de recepção e UPDATE por coluna

```sql
CREATE ROLE papel_recepcao NOLOGIN;
GRANT SELECT ON TABLE hospede, quarto TO papel_recepcao;
GRANT UPDATE (status) ON TABLE reserva TO papel_recepcao;
```

Essa solução não concede `UPDATE` nas demais colunas. Dependendo do `UPDATE` que o usuário executar, também precisará de `SELECT` sobre colunas lidas pelo filtro ou pela expressão; por exemplo:

```sql
GRANT SELECT (id_reserva) ON TABLE reserva TO papel_recepcao;
```

para permitir localizar uma reserva pelo identificador no comando de atualização. É importante **não** conceder `UPDATE` amplo sobre `reserva` se o objetivo é restringir somente a coluna `status`.

## 45. REVOKE e privilégios indiretos

```sql
REVOKE UPDATE (status) ON TABLE reserva FROM papel_recepcao;
```

Remove o privilégio concedido diretamente a essa role sobre a coluna. **Não garante** que a ação será impossível em todos os casos: a identidade pode possuir outro privilégio direto, herdado de outra role, derivado de uma concessão abrangente ou atuar como proprietária do objeto. A avaliação correta considera os caminhos de autorização disponíveis.

## 46. View pública de funcionários

```sql
CREATE VIEW vw_funcionarios_publico AS
SELECT id_funcionario, nome, cargo
FROM funcionario;

GRANT SELECT ON vw_funcionarios_publico TO papel_recepcao;
```

A proteção real exige que os usuários da recepção **não possuam privilégios que permitam consultar `funcionario.salario` diretamente**. Também se devem considerar outras views, funções ou roles que possam expor os dados.

## 47. Diagnóstico de permission denied

Se o usuário já conectou, `CONNECT` provavelmente não é o problema da sessão. Verifique principalmente: (1) `USAGE` no schema onde está `reserva`; (2) `SELECT` sobre a tabela ou as colunas requisitadas; (3) a role efetiva e quais outras roles ela herda; (4) se está usando o database/schema esperado. Em termos gerais, também vale confirmar o privilégio `CONNECT` na configuração de acesso.

Comandos úteis: `\conninfo`, `\du`, `\dn+` e `\dp reserva`.

## 48. session_user, current_user e SET ROLE

`session_user` representa a identidade original da sessão; `current_user`, a identidade efetiva usada no contexto atual para diversas verificações de privilégios. `SET ROLE papel_recepcao;` altera a role efetiva **quando a sessão tem autorização**, sendo útil para testar ou assumir permissões de um perfil. Não substitui um teste real de autenticação como usuário do setor.

## 49. Leitura sem exclusão

```sql
GRANT SELECT ON TABLE hospede TO papel_recepcao;
```

O privilégio `SELECT` permite leitura e **não implica `DELETE`**. Como medida complementar, confirme que não há outras concessões de exclusão diretas ou herdadas.

## 50. Política de menor privilégio (exemplo aceitável)

| Perfil | Operações permitidas | Operação proibida |
|---|---|---|
| **Recepção** | `SELECT` em `hospede` e `quarto`; `INSERT` em `reserva` | `SELECT` em salários de `funcionario` |
| **Financeiro** | `SELECT` em `reserva`; `INSERT` em `pagamento` | `UPDATE` de preços em `tipo_quarto` |
| **Auditoria** | `SELECT` em `reserva` e `pagamento`; `SELECT` em views de relatório | `DELETE` em `reserva` |

Outras políticas coerentes podem receber crédito integral. O importante é que os privilégios correspondam às funções e que **operações não necessárias sejam negadas**.

---

# Unidade 6 — NoSQL e MongoDB

## 51. NoSQL e modelos

NoSQL agrupa sistemas de dados que não dependem exclusivamente do modelo relacional tradicional. **Chave–valor** associa uma chave a um valor; **documentos** armazena registros com campos e estruturas aninhadas; **grafos** enfatiza nós, relacionamentos e percursos. O **MongoDB é orientado a documentos**. A escolha do modelo deve considerar os dados e os acessos necessários.

## 52. Elementos do MongoDB e BSON

- **Banco:** conjunto lógico de coleções.
- **Coleção:** conjunto de documentos.
- **Documento:** registro com campos e valores.
- **Campo:** propriedade dentro do documento.
- **`_id`:** identificador único por documento na coleção.
- **BSON:** formato de armazenamento binário com tipos adicionais em relação ao JSON comum, como datas.

No documento apresentado, `contato: { email: ... }` é um **objeto aninhado** e `tags: ["vip"]` é um **array**.

## 53. Docker e persistência

**Imagem** contém os componentes necessários para iniciar o programa; **contêiner** é a execução isolada dessa imagem; **Docker Compose** descreve e gerencia serviços por YAML; **mapeamento de porta** conecta uma porta do host à do contêiner; **volume** mantém os arquivos de banco além da vida do contêiner. `docker compose down` **sem `-v`** normalmente remove os contêineres e a rede do projeto, mas preserva o volume nomeado; portanto, ao recriar o serviço com o mesmo volume, os dados permanecem.

## 54. Iniciar, verificar, conectar e selecionar banco

**Terminal Ubuntu/PowerShell**, na pasta do YAML:

```bash
docker compose -f docker-compose-hotel-nosql.yml up -d
docker compose -f docker-compose-hotel-nosql.yml ps
docker exec -it mongo_hotel_aula mongosh -u admin_aula --authenticationDatabase admin
```

O `mongosh` solicita a senha de laboratório. **Dentro do mongosh**:

```javascript
use hotel_nosql
```

No Ubuntu pode ser necessário prefixar os comandos Docker com `sudo`. A opção `--authenticationDatabase admin` corresponde à conta administrativa inicial do ambiente didático.

## 55. Inserção e unicidade de `_id`

```javascript
db.hospedes.insertOne({
  _id: 20,
  nome: "Luiza Teste",
  cidade: "Curitiba",
  contato: { email: "luiza@exemplo.com" },
  tags: ["novo"]
})
```

Se outro documento com `_id: 20` já existir, a inserção viola o índice único de `_id` e gera erro de **chave duplicada** (por exemplo, `E11000 duplicate key error`).

## 56. Consultas com projeção, filtro e ordenação

```javascript
db.hospedes.find(
  { cidade: "Curitiba" },
  { nome: 1, cidade: 1, _id: 0 }
)
```

O primeiro objeto é o filtro e o segundo a projeção. Em seguida:

```javascript
db.quartos.find({ diaria: { $gt: 250 } }).sort({ diaria: -1 })
```

`$gt` significa “maior que”, e `sort({ diaria: -1 })` indica ordem decrescente.

## 57. Operadores de atualização

- `$set` define ou substitui o valor de campo.
- `$push` acrescenta elemento a um array.
- `$inc` acrescenta numericamente um valor ao campo existente.
- `$unset` remove um campo do documento.

Para adicionar uma tag sem apagar as anteriores:

```javascript
db.hospedes.updateOne(
  { _id: 1 },
  { $push: { tags: "vip" } }
)
```

`$push` pode adicionar valores repetidos; caso o requisito fosse evitar duplicatas, seria possível utilizar `$addToSet`.

## 58. Exclusão de um documento

```javascript
db.hospedes.deleteOne({ _id: 20 })
```

`deleteOne` atinge no máximo um documento correspondente. `db.hospedes.deleteMany({})` é perigoso porque o objeto vazio seleciona **todos os documentos**, podendo esvaziar a coleção.

## 59. Agregação e outros estágios

```javascript
db.reservas.aggregate([
  {
    $group: {
      _id: "$status",
      quantidade: { $sum: 1 }
    }
  },
  { $sort: { quantidade: -1 } }
])
```

`$group` organiza os documentos pela chave de agrupamento (`status`) e `$sum: 1` conta cada reserva. **`$match`** restringe os documentos que seguem no pipeline, funcionando de forma semelhante a um filtro `WHERE`. **`$lookup`** combina documentos de outra coleção, lembrando a finalidade de um `JOIN` relacional.

## 60. Índice único e volume

```javascript
db.hospedes.createIndex(
  { "contato.email": 1 },
  { unique: true }
)
```

O índice facilita determinados filtros no email e impõe unicidade aos valores indexados de acordo com suas regras. O **volume** preserva os arquivos de dados quando o contêiner é interrompido ou recriado. Assim, `docker compose down` seguido de `up -d` não exige repopular o banco, desde que o mesmo volume seja reutilizado. **Evite `down -v`** se quiser preservar os dados.

---

# Critérios gerais de correção

O objetivo da revisão é verificar **compreensão e aplicação**, não memorização literal. Em questões conceituais, valorize respostas que distingam claramente os conceitos, mesmo com outra redação. Em questões práticas, considere corretas soluções equivalentes que respeitem os nomes, restrições e efeitos solicitados. Em particular:

- Em **triggers**, valide o evento, o momento, o uso de `NEW`/`OLD` e o efeito esperado; a sintaxe pode variar conforme a versão do PostgreSQL.
- Em **transações**, exija o entendimento de quais operações são confirmadas ou revertidas.
- Em **views**, confira joins, filtros, agrupamentos e o tratamento de registros sem correspondência.
- Em **índices**, não exija que um plano de execução sempre escolha `Index Scan`: essa escolha depende dos dados e do otimizador.
- Em **permissões**, verifique se o aluno entende herança e privilégios em múltiplos níveis, sem assumir que uma concessão isolada controla todos os caminhos de acesso.
- Em **MongoDB**, confira a distinção entre comandos de terminal e comandos do `mongosh` e a preservação correta de objetos aninhados e arrays.
