# Gabarito comentado — Revisão para a Prova de Programação Orientada a Objetos

**UNESPAR — Ciência da Computação**  
**Correspondência:** *Revisao-Prova-POO-Pos-3o-Bimestre.md*  
**Abrangência:** 15 tópicos e 30 questões

Este gabarito reúne **respostas comentadas** para as 30 questões da revisão. As resoluções apresentam os principais conceitos e exemplos de implementação; nas questões de código, outras soluções equivalentes também podem ser corretas.

---

# Bloco I — Padrões de projeto

## Tópico 1 — Strategy

### Questão 1 — Elementos do Strategy e justificativa

**Resposta esperada:**

| Elemento | Identificação no exemplo |
|---|---|
| **Strategy** | Interface `FreteStrategy` |
| **ConcreteStrategy** | Classes `FreteNormal`, `FreteExpresso` e, quando adicionada, `FreteRetirada` |
| **Context** | Classe `CalculadoraFrete` |
| **Client** | Código que escolhe a estratégia e instancia `CalculadoraFrete`, como uma classe `Main` ou camada de aplicação |

O Strategy separa os algoritmos de frete em classes diferentes, todas com o mesmo contrato `calcular(Pedido)`. `CalculadoraFrete` delega o cálculo a uma implementação recebida pelo construtor. Assim, criar uma nova modalidade costuma exigir uma nova classe que implemente `FreteStrategy`, sem modificar os cálculos existentes nem o método `CalculadoraFrete.calcular()`. Isso reduz condicionais concentradas, melhora a manutenção e permite testar regras independentemente.

### Questão 2 — Implementar `FreteRetirada`

**Uma solução correta:**

```java
public class FreteRetirada implements FreteStrategy {

    @Override
    public double calcular(Pedido pedido) {
        return 0.0;
    }
}
```

Linha de criação solicitada:

```java
CalculadoraFrete calculadora =
    new CalculadoraFrete(new FreteRetirada());
```

Também é válida a atribuição intermediária a `FreteStrategy`.

---

## Tópico 2 — Factory Method

### Questão 3 — Elementos do Factory Method

**Resposta esperada:**

| Elemento | Identificação |
|---|---|
| **Product** | Interface `Comprovante` |
| **ConcreteProduct** | Classe `ComprovanteTexto` |
| **Creator** | Classe abstrata `ComprovanteFactory` |
| **ConcreteCreator** | Classe `ComprovanteTextoFactory` |
| **Factory Method** | Método `criarComprovante()` |

O método `emitir()` está implementado na classe criadora e utiliza um objeto do tipo `Comprovante`, sem depender da classe concreta. A fábrica concreta determina qual implementação será criada. Isso permite acrescentar produtos, como comprovantes HTML, preservando o código de `emitir()`.

### Questão 4 — `ComprovanteHTMLFactory`

**Solução de referência:**

```java
public class ComprovanteHTMLFactory extends ComprovanteFactory {

    @Override
    public Comprovante criarComprovante() {
        return new ComprovanteHTML();
    }
}
```

A classe **`ComprovanteFactory`**, especialmente seu método concreto `emitir()`, continua a utilizar qualquer produto que implemente `Comprovante` sem precisar ser modificada.

---

# Bloco II — Maven, SQLite, JDBC e DAO

## Tópico 3 — Maven

### Questão 5 — Bibliotecas do Java, dependências e plugins

`ArrayList` pertence à biblioteca padrão de Java (`java.util`) e já está disponível com o JDK utilizado pelo projeto; não exige dependência externa no `pom.xml`. O driver `sqlite-jdbc`, por outro lado, é uma biblioteca de terceiros. Sua dependência precisa ser declarada para que Maven a obtenha e a disponibilize conforme o escopo configurado.

- **Dependência:** código/biblioteca necessário para compilar, executar ou testar a aplicação (ex.: driver SQLite).
- **Plugin:** ferramenta que executa tarefas do processo de build (ex.: Maven Compiler Plugin ou Surefire, responsável por executar testes).

### Questão 6 — Escopo `test` e coordenadas Maven

`<scope>test</scope>` é inadequado para o driver SQLite quando a **aplicação principal** abre conexões durante a execução: o driver ficaria disponível apenas no classpath de testes, não no classpath de execução normal.

Duas opções válidas:

```xml
<!-- Opção simples: escopo compile, que é o padrão. -->
<dependency>
    <groupId>org.xerial</groupId>
    <artifactId>sqlite-jdbc</artifactId>
    <version>3.53.4.0</version>
</dependency>
```

Ou, caso o código da aplicação dependa apenas da API `java.sql` e precise do driver somente ao executar:

```xml
<scope>runtime</scope>
```

Em Maven, **`groupId`** identifica o grupo ou organização, **`artifactId`** identifica o artefato/biblioteca e **`version`** identifica sua versão.

---

## Tópico 4 — SQLite, JDBC e conexões

### Questão 7 — JDBC × driver × arquivo do banco

- **JDBC:** API do Java para conexão, execução de comandos e leitura de dados em bancos.
- **Driver SQLite:** implementação que permite ao código JDBC se comunicar com o SQLite.
- **`hotel.db`:** arquivo que guarda os dados persistidos no banco SQLite.

Ao encerrar a aplicação, o conteúdo do arquivo `hotel.db` permanece, desde que o arquivo seja preservado e as alterações tenham sido efetivamente registradas. Os objetos armazenados somente em uma `ArrayList`, por sua vez, vivem na memória do processo e não são automaticamente salvos ao final da execução.

### Questão 8 — URL JDBC e encerramento da conexão

**Problemas:** `getConnection("hotel.db")` não usa a URL reconhecida pelo driver SQLite; manter conexões abertas sem necessidade pode consumir recursos e manter bloqueios.

**Correção possível:**

```java
try (Connection conn =
         DriverManager.getConnection("jdbc:sqlite:hotel.db")) {

    // Executar operações JDBC aqui.

} catch (SQLException e) {
    System.err.println(e.getMessage());
}
```

`try-with-resources` chama `close()` automaticamente ao sair do bloco, inclusive quando há exceção.

---

## Tópico 5 — Modelo relacional e criação de tabelas

### Questão 9 — `id`, `numero` e restrições

`id` é a identificação técnica interna do registro e pode ser gerada automaticamente; `numero` é uma informação de negócio (o número do quarto exibido aos usuários). Separá-los permite modificar regras de identificação do domínio sem necessariamente modificar todas as referências internas a registros.

- **`PRIMARY KEY`:** identifica unicamente cada linha; em SQLite, `id INTEGER PRIMARY KEY` também funciona como identificador associado ao rowid.
- **`UNIQUE`:** impede a repetição de valores não nulos, útil para números de quarto.
- **`NOT NULL`:** exige a presença de valor, útil para número e disponibilidade.

A chave primária já impõe unicidade para `id`. Para `numero`, o uso conjunto de `NOT NULL UNIQUE` evita tanto valores ausentes quanto números repetidos.

### Questão 10 — Completar DDL

**Resposta:**

```sql
CREATE TABLE quarto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER NOT NULL UNIQUE,
    disponibilidade TEXT NOT NULL
);
```

---

## Tópico 6 — `PreparedStatement`

### Questão 11 — SQL parametrizado

Concatenar diretamente dados digitados pelo usuário ao texto SQL mistura a estrutura do comando com os dados. Isso pode produzir consultas inválidas por caracteres especiais e cria risco de **SQL Injection**. `PreparedStatement` utiliza marcadores `?` e métodos `set...()` para vincular valores com tipos apropriados, sem tratá-los como parte da sintaxe SQL.

Exemplo conceitual:

```java
String sql = "SELECT * FROM quarto WHERE numero = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setInt(1, numero);
```

### Questão 12 — Preencher quatro parâmetros do `INSERT`

**Resposta:**

```java
ps.setInt(1, quarto.getNumero());
ps.setDouble(2, quarto.getValorDiaria());
ps.setString(3, quarto.getTipo().name());
ps.setString(4, quarto.getDisponibilidade().name());
```

Os índices `1` a `4` seguem exatamente a ordem das colunas em `INSERT INTO quarto (numero, valor_diaria, tipo, disponibilidade)`.

---

## Tópico 7 — `ResultSet`

### Questão 13 — Iteração e conversão de registros

Cada linha do `ResultSet` representa um quarto encontrado. Para montar cinco objetos, precisamos percorrer as cinco linhas, usando `while (rs.next())`. O cursor começa antes da primeira linha; `rs.next()` move o cursor e confirma a existência de uma linha válida para a leitura.

O método `criarQuarto(rs)` centraliza a conversão coluna → atributo, inclusive a reconstrução dos enums, evitando repetição em diferentes métodos do DAO e facilitando futuras alterações.

### Questão 14 — Ler colunas e converter enum

**Linhas solicitadas:**

```java
int numero = rs.getInt("numero");
double valorDiaria = rs.getDouble("valor_diaria");
```

O código existente:

```java
Tipo tipo = Tipo.valueOf(rs.getString("tipo"));
```

lançará **`IllegalArgumentException`** se o texto não corresponder exatamente a nenhuma constante do enum, como `"DUPLOO"` ou `"duplo"` para um enum que define apenas `DUPLO`.

---

## Tópico 8 — `UPDATE`, `DELETE` e linhas afetadas

### Questão 15 — Perigo do `DELETE` sem `WHERE`

O comando:

```sql
DELETE FROM quarto;
```

remove **todas as linhas da tabela** (na ausência de restrições/erros), e não apenas o quarto selecionado na interface. Para excluir uma linha específica:

```sql
DELETE FROM quarto WHERE id = ?;
```

O parâmetro é preenchido com `ps.setInt(1, id)`. O retorno de `executeUpdate()` indica quantos registros foram afetados: `0` significa que nenhum registro foi removido; um valor positivo indica ao menos uma remoção. É importante verificar isso antes de informar sucesso ao usuário.

### Questão 16 — `UPDATE` da diária pelo ID

**Resposta:**

```java
String sql = "UPDATE quarto SET valor_diaria = ? WHERE id = ?";
PreparedStatement ps = conn.prepareStatement(sql);

ps.setDouble(1, novoValor);
ps.setInt(2, id);
```

A execução, se mostrada, pode ser:

```java
int afetadas = ps.executeUpdate();
```

---

## Tópico 9 — DAO e separação de responsabilidades

### Questão 17 — Centralização do acesso a dados

O `QuartoDAO` deve concentrar os comandos SQL, abertura e encerramento de conexões, criação de statements e transformação de `ResultSet` em objetos. A tela Swing deve cuidar da entrada de dados, eventos de interface, exibição de mensagens e atualização de componentes visuais, chamando operações do DAO (ou de um Service intermediário).

A separação reduz duplicação de SQL, facilita manutenção e evita acoplar a interface às particularidades do banco.

`try-with-resources` é importante porque fecha automaticamente recursos como `Connection`, `PreparedStatement` e `ResultSet`, inclusive se ocorrer uma exceção.

### Questão 18 — Novo fluxo arquitetural e assinaturas

**Fluxo possível:**

```text
JFrame → QuartoDAO → JDBC/SQL → SQLite
```

Uma arquitetura com Service também é válida:

```text
JFrame → QuartoService → QuartoDAO → JDBC/SQL → SQLite
```

**Duas assinaturas de exemplo:**

```java
public Quarto buscarPorId(int id) throws SQLException;
public boolean atualizar(Quarto quarto) throws SQLException;
```

Também seriam válidas, por exemplo:

```java
public List<Quarto> listarTodos() throws SQLException;
public boolean remover(int id) throws SQLException;
```

A tela Swing, tipicamente em um `ActionListener` ou método acionado por botão, chama os métodos de consulta/alteração; o DAO executa o SQL. Quando houver Service, a tela chama o Service, que por sua vez usa o DAO.

---

# Bloco III — Hibernate e Jakarta Persistence

## Tópico 10 — ORM, JPA, Hibernate e JDBC

### Questão 19 — Diferenças e limitações do ORM

- **JDBC:** API de baixo nível para manipular conexões, comandos SQL e resultados.
- **Jakarta Persistence (JPA):** especificação e API para persistência orientada a entidades Java.
- **Hibernate:** framework ORM que, entre outras funções, implementa Jakarta Persistence e realiza o mapeamento objeto-relacional.

Hibernate **não elimina JDBC**: ao acessar bancos relacionais, utiliza drivers e mecanismos JDBC internamente. Também **não elimina a necessidade de conhecer SQL**: o desenvolvedor precisa compreender consultas, tabelas, chaves, relacionamentos, transações e eficiência do acesso a dados.

### Questão 20 — Objeto `Quarto` × tabela

**Correspondência esperada:**

| Modelo Java | Modelo relacional |
|---|---|
| Classe `Quarto` | Tabela, por exemplo `quartos` |
| Um objeto `Quarto` | Uma linha/registro |
| `id` | Coluna identificadora/chave primária |
| `numero` | Coluna `numero` |
| `tipo` | Coluna que armazena o valor do enum |
| `valorDiaria` | Coluna `valor_diaria` (dependendo do mapeamento) |
| Referência entre entidades | Associação/chave estrangeira, quando aplicável |

Com JDBC manual, o programador cria SQL, define parâmetros e reconstrói objetos com valores de um `ResultSet`. Com ORM, o mapeamento é declarado e o framework pode gerar SQL e criar/popular entidades a partir dos registros.

---

## Tópico 11 — Entidades e anotações JPA

### Questão 21 — Papel das anotações

- **`@Entity`:** identifica a classe como entidade persistente.
- **`@Id`:** indica o atributo de identificação/chave primária.
- **`@GeneratedValue`:** indica que o identificador será gerado segundo a estratégia configurada.
- **`@Enumerated(EnumType.STRING)`:** armazena o nome da constante do enum, como `"DUPLO"`, em vez de um ordinal.

Armazenar o nome tende a ser mais seguro porque inserir ou reorganizar constantes em um enum pode mudar seus valores ordinais, causando interpretações incorretas de registros antigos. O texto também favorece a leitura humana.

### Questão 22 — Anotações da entidade `Hospede`

**Resposta:**

```java
@Entity
@Table(name = "hospedes")
public class Hospede {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    protected Hospede() { }
}
```

O exemplo mantém o construtor `protected` sem argumentos, como previsto para uma entidade JPA. `GenerationType.AUTO` também pode ser aceito se o aluno justificar a geração automática do ID e não houver exigência de uma estratégia específica.

---

## Tópico 12 — `EntityManager`, transações e ciclo de vida

### Questão 23 — Estados da entidade e dirty checking

- **New/transient:** `new Quarto(...)` criou um objeto Java que ainda não está sendo gerenciado pelo contexto de persistência.
- **Managed:** depois de tornar o objeto persistente com `persist()` ou carregá-lo com `find()` em um `EntityManager` ativo, seu estado é acompanhado pelo contexto.
- **Detached:** após fechamento/limpeza do contexto, o objeto continua existindo em Java, mas não é mais acompanhado por aquele `EntityManager`.

O **dirty checking** compara/acompanha alterações feitas em entidades **managed** e pode gerar o `UPDATE` necessário na sincronização (`flush`/`commit`) dentro da transação. Um objeto detached não recebe persistência automática de alterações realizadas após sua desconexão.

### Questão 24 — Alteração após `em.close()`

Ao executar `em.close()`, o objeto `q` deixa de ser gerenciado pelo contexto encerrado. O setter posterior modifica apenas o objeto na memória; **não existe dirty checking automático por aquele EntityManager** e tampouco uma transação ativa que grave o novo valor.

**Ordem correta de referência:**

```java
EntityManager em = JPAUtil.criarEntityManager();

try {
    em.getTransaction().begin();

    Quarto q = em.find(Quarto.class, 1L);

    if (q != null) {
        q.setValorDiaria(300.0);
    }

    em.getTransaction().commit();

} catch (RuntimeException e) {

    if (em.getTransaction().isActive()) {
        em.getTransaction().rollback();
    }

    throw e;

} finally {
    em.close();
}
```

Outra resposta válida seria explicar o uso de uma nova transação/contexto e `merge()` para reanexar o estado detached, sem exigir essa implementação, pois a questão pede a ordem básica do fluxo.

---

## Tópico 13 — JPQL e relacionamentos

### Questão 25 — SQL × JPQL e parâmetros

**SQL** usa os nomes de tabelas e colunas:

```sql
SELECT * FROM quartos WHERE valor_diaria <= 300;
```

**JPQL** usa nomes de entidades e atributos do modelo Java:

```java
List<Quarto> lista = em.createQuery(
    "SELECT q FROM Quarto q WHERE q.valorDiaria <= :maximo",
    Quarto.class
).setParameter("maximo", 300.0).getResultList();
```

Por isso `SELECT * FROM quartos` não é a forma JPQL equivalente: `*` e o nome da tabela pertencem ao SQL; em JPQL selecionamos `q` da **entidade `Quarto`**. `setParameter()` vincula um valor ao parâmetro nomeado (`:maximo`), permitindo consultas parametrizadas com tipos adequados e sem concatenação manual de dados.

### Questão 26 — Associação `Reserva` → `Hospede`

**Resposta:**

```java
@ManyToOne
@JoinColumn(name = "hospede_id")
private Hospede hospede;
```

`@ManyToOne` indica que muitas reservas podem fazer referência ao mesmo hóspede. `@JoinColumn(name = "hospede_id")` define a coluna de ligação na tabela de **reservas**. Essa coluna funciona como chave estrangeira que referencia a chave primária do registro de `Hospede`.

---

# Bloco IV — Spring Boot e APIs REST

## Tópico 14 — Spring, Beans e injeção de dependência

### Questão 27 — Spring Framework, Spring Boot, Bean e DI

**Spring Framework** fornece a infraestrutura de componentes, Inversão de Controle e Injeção de Dependência, entre outros recursos. **Spring Boot** simplifica a criação e execução de aplicações Spring com starters, auto-configuração e frequentemente um servidor HTTP embutido.

**Bean** é um objeto cujo ciclo de vida é gerenciado pelo contêiner Spring. **Injeção de Dependência** ocorre quando o contêiner fornece a um componente um objeto de que ele precisa, por exemplo um `QuartoService` recebido no construtor de `QuartoController`.

A injeção por construtor deixa as dependências explícitas, diminui o acoplamento com a criação de objetos concretos e facilita substituí-las em testes.

### Questão 28 — Injeção de `ReservaService`

**Resposta:**

```java
private final ReservaService service;

public ReservaController(ReservaService service) {
    this.service = service;
}
```

Também pode ser:

```java
private final ReservaService reservaService;

public ReservaController(ReservaService reservaService) {
    this.reservaService = reservaService;
}
```

O **contêiner do Spring** identifica `ReservaService` como componente/Bean por meio de `@Service` e injeta sua instância no construtor de `ReservaController`, desde que o Controller seja também gerenciado pelo Spring e os componentes estejam no escopo de descoberta/configuração da aplicação.

---

## Tópico 15 — REST, JSON e Controllers

### Questão 29 — HTTP, CRUD e códigos de status

| Endpoint | Operação |
|---|---|
| `GET /quartos` | READ — listar quartos |
| `POST /quartos` | CREATE — criar quarto |
| `PUT /quartos/7` | UPDATE — atualizar/substituir quarto 7 |
| `DELETE /quartos/7` | DELETE — excluir quarto 7 |

**Status HTTP:**

- **`201 Created`:** resposta apropriada quando um `POST` cria um novo quarto.
- **`204 No Content`:** sucesso sem corpo de resposta, por exemplo após exclusão bem-sucedida por `DELETE`.
- **`400 Bad Request`:** requisição inválida, por exemplo JSON malformado, tipo de enum inválido ou dados de entrada não aceitos.
- **`404 Not Found`:** recurso não existe, por exemplo `GET /quartos/999` quando o ID 999 não está cadastrado.

Outros comportamentos válidos dependem do contrato da API: `200 OK` pode ser usado em consultas e atualizações bem-sucedidas; `204` também pode sinalizar atualização sem conteúdo.

### Questão 30 — Endpoint de busca por tipo

**Resposta:**

```java
@GetMapping("/tipo")
public List<Quarto> buscarPorTipo(@RequestParam Tipo tipo) {
    return service.buscarPorTipo(tipo);
}
```

Como o Controller já possui `@RequestMapping("/quartos")`, o método responde a:

```text
GET /quartos/tipo?tipo=DUPLO
```

`@RequestParam` lê `tipo` da **query string**. O mecanismo de conversão do Spring consegue converter o texto `DUPLO` para a constante `Tipo.DUPLO` quando essa constante existe no enum. Um valor inexistente normalmente provoca erro de conversão e resposta de cliente inválido, como `400 Bad Request`.

---
