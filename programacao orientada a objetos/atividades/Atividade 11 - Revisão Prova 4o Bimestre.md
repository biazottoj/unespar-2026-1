# Revisão para a prova — Programação Orientada a Objetos

**UNESPAR — Ciência da Computação**  
**Recorte:** conteúdos apresentados nos materiais posteriores à avaliação do 3º bimestre  
**Formato:** conceito, exemplo guiado e duas questões por tópico  
**Quantidade:** **15 tópicos · 30 questões**

## Como utilizar este material

A revisão retoma conteúdos de Java que foram aprofundados após a avaliação anterior, especialmente **Strategy**, **Factory Method**, **Maven**, **JDBC e SQLite**, **DAO**, **Hibernate/JPA** e **Spring Boot**. Cada tópico começa com uma explicação conceitual e apresenta um exemplo que pode ser acompanhado passo a passo. As duas questões seguintes foram elaboradas para exigir explicação, interpretação ou produção de **pequenos trechos de código**, sem pedir sistemas completos.

Os exemplos de persistência e Spring Boot utilizam o **SistemaHotel** como referência. Para os padrões de projeto, retomaremos o sistema de pedidos e cálculo de frete trabalhado nas atividades. Conceitos anteriores, como interfaces, herança, `enum`, `List`, lambda e `Stream`, são pré-requisitos e aparecem integrados aos novos conteúdos.

**Orientação:** antes de responder, identifique o problema que a tecnologia resolve, o papel de cada classe ou método e o fluxo de execução. Nas questões com código, considere que os imports e os atributos já apresentados no enunciado estão disponíveis, salvo indicação contrária.


# Bloco I — Padrões de projeto

## Tópico 1 — Strategy: encapsular algoritmos intercambiáveis

### Conceito

O padrão **Strategy** é indicado quando um sistema pode realizar uma mesma operação utilizando **algoritmos diferentes**. Em vez de colocar todas as regras dentro de uma classe que decide o comportamento por `if/else` ou `switch`, cada algoritmo fica em uma implementação separada de uma interface. A classe que utiliza o algoritmo é chamada de **Context**; ela conhece o contrato, mas não precisa conhecer os detalhes de cada implementação.

No exemplo de pedidos, existem regras diferentes para frete normal, expresso e retirada na loja. O cálculo depende do tipo de entrega, mas o restante do processamento do pedido não deveria precisar ser modificado toda vez que uma modalidade é criada.

### Exemplo guiado

Primeiro, definimos o comportamento comum das estratégias:

```
public interface FreteStrategy \{  
    double calcular(Pedido pedido);  
\}
```

Agora, implementamos duas regras. Considere que `Pedido` possui `getPeso()` e que o peso está expresso em quilogramas:

```
public class FreteNormal implements FreteStrategy \{  
    @Override  
    public double calcular(Pedido pedido) \{  
        return pedido.getPeso() \* 5.0;  
    \}  
\}  
  
public class FreteExpresso implements FreteStrategy \{  
    @Override  
    public double calcular(Pedido pedido) \{  
        return pedido.getPeso() \* 9.0 + 15.0;  
    \}  
\}
```

Por fim, o Context delega a responsabilidade à estratégia recebida:

```
public class CalculadoraFrete \{  
    private final FreteStrategy estrategia;  
  
    public CalculadoraFrete(FreteStrategy estrategia) \{  
        this.estrategia = estrategia;  
    \}  
  
    public double calcular(Pedido pedido) \{  
        return estrategia.calcular(pedido);  
    \}  
\}
```

**Acompanhamento:** para um pedido de 5 kg, a estratégia normal retorna R$ 25,00, enquanto a expressa retorna R$ 60,00. A classe `CalculadoraFrete` não precisou ser reescrita: apenas recebeu outra implementação de `FreteStrategy`.

### Questões

**Questão 1 — Conceitual.** Identifique os elementos **Strategy**, **ConcreteStrategy**, **Context** e **Client** no cenário descrito. Explique por que adicionar uma modalidade de frete é mais simples nessa organização do que em uma classe com todos os cálculos concentrados em `if/else`.

**Questão 2 — Criação de código.** Crie somente a classe `FreteRetirada`, que implementa `FreteStrategy` e retorna custo zero. Depois, escreva a linha que permitiria criar uma `CalculadoraFrete` utilizando essa nova estratégia, sem alterar `CalculadoraFrete`.


## Tópico 2 — Factory Method: separar a criação do uso de objetos

### Conceito

O **Factory Method** organiza a criação de objetos por meio de um método definido por uma classe criadora e implementado por criadores concretos. Ele permite que o código que usa um produto trabalhe com uma abstração, sem precisar conhecer a classe concreta a ser instanciada. Não confunda com Strategy: **Strategy varia o algoritmo executado**, enquanto **Factory Method varia a implementação criada**.

Na atividade de pedidos, o sistema precisava gerar comprovantes em texto ou HTML. Os dois seguem um mesmo contrato, mas possuem maneiras diferentes de produzir sua saída.

### Exemplo guiado

O produto é representado por uma interface:

```
public interface Comprovante \{  
    void gerar(Pedido pedido, double frete);  
\}
```

Uma implementação concreta gera texto simples:

```
public class ComprovanteTexto implements Comprovante \{  
    @Override  
    public void gerar(Pedido pedido, double frete) \{  
        System.out.println("Total: R$ " + (pedido.getValor() + frete));  
    \}  
\}
```

O **Creator** define o Factory Method e pode conter uma operação que usa o produto:

```
public abstract class ComprovanteFactory \{  
    public abstract Comprovante criarComprovante();  
  
    public void emitir(Pedido pedido, double frete) \{  
        Comprovante c = criarComprovante();  
        c.gerar(pedido, frete);  
    \}  
\}
```

Uma fábrica concreta decide o objeto produzido:

```
public class ComprovanteTextoFactory extends ComprovanteFactory \{  
    @Override  
    public Comprovante criarComprovante() \{  
        return new ComprovanteTexto();  
    \}  
\}
```

**Acompanhamento:** `new ComprovanteTextoFactory().emitir(pedido, 25)` chama `emitir`, que solicita um `Comprovante` através de `criarComprovante()` e depois executa `gerar()`. Considere um `Pedido` de R$ 200,00 para obter o total de R$ 225,00. Assim, a operação `emitir()` não precisa conter `new ComprovanteTexto()`.

### Questões

**Questão 3 — Análise.** Classifique `Comprovante`, `ComprovanteTexto`, `ComprovanteFactory` e `ComprovanteTextoFactory` como **Product**, **ConcreteProduct**, **Creator** e **ConcreteCreator**. Explique o benefício de o método `emitir()` depender da interface `Comprovante`.

**Questão 4 — Criação de código.** Considere que a classe `ComprovanteHTML implements Comprovante` já existe. Escreva apenas a classe `ComprovanteHTMLFactory`, sobrescrevendo o Factory Method. Indique qual classe já existente poderá continuar usando os produtos sem modificações.


# Bloco II — Maven, SQLite, JDBC e DAO

## Tópico 3 — Maven e gerenciamento de dependências

### Conceito

**Maven** organiza a construção de projetos Java e o uso de bibliotecas externas. O arquivo **`pom.xml`** identifica o projeto, declara dependências e configura ferramentas de build. Maven pode baixar bibliotecas de repositórios, inclusive as dependências transitivas necessárias para que outras bibliotecas funcionem. Uma **dependência** fornece código utilizado pelo projeto; um **plugin** executa tarefas do processo de construção, como compilar, testar ou empacotar.

Os escopos indicam quando uma dependência é necessária. Por exemplo, `compile` atende ao código principal; `test` é restrito à compilação e execução de testes; `runtime` é utilizado na execução. O comando `mvn package` percorre fases necessárias para produzir o artefato, enquanto `mvn dependency:tree` ajuda a inspecionar as dependências.

### Exemplo guiado

Para utilizar SQLite via JDBC, declaramos a biblioteca do driver:

```
\<dependencies\>  
    \<dependency\>  
        \<groupId\>org.xerial\</groupId\>  
        \<artifactId\>sqlite-jdbc\</artifactId\>  
        \<version\>3.53.4.0\</version\>  
    \</dependency\>  
\</dependencies\>
```

O código de `java.sql.Connection` já pertence à plataforma Java; o driver SQLite é uma biblioteca externa. Ao executar o build, Maven disponibiliza essa biblioteca no classpath. **Isso não significa que Maven seja o banco de dados**: sua função aqui é tornar o driver disponível.

### Questões

**Questão 5 — Conceitual.** Explique por que não precisamos declarar `java.util.ArrayList` no `pom.xml`, mas precisamos declarar o driver SQLite. Diferencie o papel de uma **dependência** e de um **plugin** Maven.

**Questão 6 — Análise de configuração.** Um aluno declarou `sqlite-jdbc` com `\<scope\>test\</scope\>`, mas a aplicação abre conexões ao ser executada normalmente. Analise o problema e indique qual escopo seria adequado. Explique ainda a finalidade de `groupId`, `artifactId` e `version`.


## Tópico 4 — SQLite, JDBC e abertura de conexões

### Conceito

**JDBC** é a API de Java que permite executar operações em bancos de dados por meio de drivers. **SQLite** é o sistema de banco de dados que, nesse exemplo, armazena as tabelas em um arquivo local. O **driver JDBC** liga a API Java ao banco. A classe `DriverManager` pode abrir uma conexão utilizando uma URL; essa conexão é representada por `Connection`.

Diferentemente de uma `List\<Quarto\>` em memória, o conteúdo de `hotel.db` permanece entre execuções enquanto o arquivo for preservado. Para usar o arquivo local, não é necessário iniciar um servidor SQLite separado.

### Exemplo guiado

A classe de conexão pode ser centralizada:

```
public final class Conexao \{  
    private static final String URL = "jdbc:sqlite:hotel.db";  
  
    private Conexao() \{ \}  
  
    public static Connection abrir() throws SQLException \{  
        return DriverManager.getConnection(URL);  
    \}  
\}
```

Para testar e liberar o recurso corretamente:

```
try (Connection conn = Conexao.abrir()) \{  
    System.out.println("Conexão aberta: " + !conn.isClosed());  
\} catch (SQLException e) \{  
    System.err.println("Falha ao acessar o SQLite: " + e.getMessage());  
\}
```

**Acompanhamento:** o programa solicita uma conexão; o driver interpreta `jdbc:sqlite:hotel.db`; o SQLite utiliza o arquivo como banco; o bloco `try-with-resources` encerra a conexão ao sair do escopo.

### Questões

**Questão 7 — Conceitual.** Explique as diferenças entre **JDBC**, **driver SQLite** e **arquivo `hotel.db`**. O que acontece com os dados quando o programa termina e por que esse comportamento é diferente de armazená-los apenas em uma `ArrayList`?

**Questão 8 — Análise de código.** Um aluno usa `DriverManager.getConnection("hotel.db")` e deixa a conexão aberta até o programa terminar. Identifique os dois problemas e apresente um pequeno trecho corrigido que utilize a URL JDBC adequada e `try-with-resources`.


## Tópico 5 — Modelo relacional e criação de tabelas no SQLite

### Conceito

Ao persistir um objeto com JDBC, é necessário definir como seus atributos serão representados em colunas. Para `Quarto`, podemos separar a identificação técnica (`id`) do número usado pelo hotel (`numero`). **Chave primária** identifica um registro; **`UNIQUE`** impede a repetição de um valor; **`NOT NULL`** exige que uma coluna tenha valor.

O comando `CREATE TABLE IF NOT EXISTS` permite criar uma tabela sem tentar recriá-la quando ela já existe. O uso de `Statement` é aceitável para executar um comando fixo de definição do esquema; para valores provenientes de usuários, priorizamos `PreparedStatement`.

### Exemplo guiado

```
String sql = """  
    CREATE TABLE IF NOT EXISTS quarto (  
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        numero INTEGER NOT NULL UNIQUE,  
        valor\_diaria REAL NOT NULL,  
        tipo TEXT NOT NULL,  
        disponibilidade TEXT NOT NULL  
    )  
    """;  
  
try (Connection conn = Conexao.abrir();  
     Statement stmt = conn.createStatement()) \{  
    stmt.execute(sql);  
\}
```

**Acompanhamento:** `id` é uma chave gerada pelo SQLite; `numero` é obrigatório e único; `valor\_diaria` é numérico; os valores dos `enum` podem ser armazenados como texto, por exemplo `DUPLO` e `DISPONIVEL`.

### Questões

**Questão 9 — Conceitual.** Por que é útil manter os campos `id` e `numero` separados na entidade `Quarto`? Explique a diferença entre `PRIMARY KEY`, `UNIQUE` e `NOT NULL` aplicada ao cadastro de quartos.

**Questão 10 — Criação de código.** Complete a definição abaixo, incluindo restrições para que `numero` seja obrigatório e único, e `disponibilidade` seja obrigatória. Não é necessário escrever o método Java:

```
CREATE TABLE quarto (  
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    numero INTEGER \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_,  
    disponibilidade TEXT \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
);
```


## Tópico 6 — `PreparedStatement`: parâmetros e inserção

### Conceito

Um **`PreparedStatement`** representa um comando SQL parametrizado. Os marcadores `?` são preenchidos com métodos como `setInt`, `setDouble` e `setString`. Isso separa os valores da estrutura da consulta, evita problemas comuns de concatenação e reduz o risco de SQL Injection. A numeração dos parâmetros JDBC começa em **1**.

Para comandos que alteram registros — `INSERT`, `UPDATE` e `DELETE` — usamos normalmente `executeUpdate()`. Seu retorno indica quantas linhas foram afetadas. Já o `executeQuery()` é utilizado para obter linhas de um `SELECT`.

### Exemplo guiado

```
String sql = """  
    INSERT INTO quarto (numero, valor\_diaria, tipo)  
    VALUES (?, ?, ?)  
    """;  
  
try (Connection conn = Conexao.abrir();  
     PreparedStatement ps = conn.prepareStatement(sql)) \{  
  
    ps.setInt(1, 101);  
    ps.setDouble(2, 180.0);  
    ps.setString(3, Tipo.SIMPLES.name());  
  
    int afetadas = ps.executeUpdate();  
    System.out.println("Linhas inseridas: " + afetadas);  
\}
```

**Acompanhamento:** o primeiro `?` corresponde a `numero`, o segundo a `valor\_diaria` e o terceiro a `tipo`. O valor de um `enum` foi convertido para texto com `name()` antes de ser armazenado.

### Questões

**Questão 11 — Conceitual.** Explique por que é inadequado construir um `INSERT` concatenando diretamente informações digitadas pelo usuário. Qual é a vantagem de um `PreparedStatement` em relação a esse procedimento?

**Questão 12 — Criação de código.** Para o SQL a seguir, escreva somente as **quatro chamadas `set...(...)`** que preenchem os parâmetros usando o objeto `quarto`. Considere que `getTipo()` e `getDisponibilidade()` retornam enums.

```
String sql = """  
    INSERT INTO quarto  
        (numero, valor\_diaria, tipo, disponibilidade)  
    VALUES (?, ?, ?, ?)  
    """;  
PreparedStatement ps = conn.prepareStatement(sql);  
// Complete aqui.
```


## Tópico 7 — `ResultSet`: converter registros em objetos

### Conceito

Ao executar um `SELECT`, o JDBC fornece um **`ResultSet`**. Ele mantém um cursor sobre as linhas retornadas; `next()` avança para a próxima linha e informa se ela existe. Os métodos `getInt`, `getDouble` e `getString` extraem os valores das colunas. Como o banco possui registros relacionais, o programa precisa reconstruir os objetos Java manualmente.

Essa conversão é uma parte importante de um DAO e costuma ser extraída para um método auxiliar, evitando repetir o mesmo código em `listarTodos()`, `buscarPorId()` e outras consultas.

### Exemplo guiado

Considere que o construtor de `Quarto` recebe `(id, numero, valorDiaria, tipo, disponibilidade)`:

```
private Quarto criarQuarto(ResultSet rs) throws SQLException \{  
    return new Quarto(  
        rs.getInt("id"),  
        rs.getInt("numero"),  
        rs.getDouble("valor\_diaria"),  
        Tipo.valueOf(rs.getString("tipo")),  
        Disponibilidade.valueOf(rs.getString("disponibilidade"))  
    );  
\}
```

A consulta percorre o resultado:

```
List\<Quarto\> encontrados = new ArrayList\<\>();  
try (ResultSet rs = ps.executeQuery()) \{  
    while (rs.next()) \{  
        encontrados.add(criarQuarto(rs));  
    \}  
\}
```

**Acompanhamento:** cada linha é transformada em um novo `Quarto`. Os textos armazenados como `SIMPLES` e `OCUPADO` voltam aos tipos Java correspondentes por meio de `valueOf()`.

### Questões

**Questão 13 — Conceitual.** Explique por que um `SELECT` que retorna cinco quartos precisa percorrer um `ResultSet` e por que `rs.next()` aparece antes da leitura das colunas. Qual vantagem existe em centralizar a conversão no método `criarQuarto(rs)`?

**Questão 14 — Análise/criação.** Observe o trecho:

```
while (rs.next()) \{  
    Tipo tipo = Tipo.valueOf(rs.getString("tipo"));  
    // Falta obter numero e valor\_diaria.  
\}
```

Escreva as duas linhas necessárias para obter `numero` e `valor\_diaria` nos tipos Java adequados. Explique o que aconteceria se a coluna `tipo` armazenasse um texto que não corresponde a nenhum valor do enum.


## Tópico 8 — `UPDATE`, `DELETE` e linhas afetadas

### Conceito

O `UPDATE` modifica os valores de linhas existentes e o `DELETE` remove registros. O predicado `WHERE` define **quais registros** serão alterados ou removidos. Em um CRUD, omitir essa condição em uma atualização ou exclusão por identificador pode afetar todos os registros da tabela.

Em JDBC, ambos os comandos são normalmente executados com `PreparedStatement` e `executeUpdate()`. Testar o número de linhas afetadas permite distinguir uma operação realizada de uma tentativa de modificar um registro inexistente.

### Exemplo guiado

Para alterar apenas o estado de um quarto específico:

```
String sql = "UPDATE quarto SET disponibilidade = ? WHERE id = ?";  
  
try (Connection conn = Conexao.abrir();  
     PreparedStatement ps = conn.prepareStatement(sql)) \{  
  
    ps.setString(1, Disponibilidade.OCUPADO.name());  
    ps.setInt(2, 7);  
  
    boolean atualizado = ps.executeUpdate() \> 0;  
    System.out.println("Atualizado: " + atualizado);  
\}
```

**Acompanhamento:** o comando altera o quarto cuja chave primária vale `7`. Se esse ID não estiver cadastrado, nenhuma linha será atualizada e a expressão `executeUpdate() \> 0` retornará `false`.

### Questões

**Questão 15 — Conceitual/análise.** Um aluno implementou `DELETE FROM quarto` para remover o quarto selecionado na interface Swing. Explique o erro, sua consequência e como o SQL deveria ser alterado. Discuta por que é importante verificar o retorno de `executeUpdate()`.

**Questão 16 — Criação de código.** Escreva somente o SQL parametrizado e as chamadas `set...(...)` para atualizar o **valor da diária** de um quarto a partir de seu `id`. Considere `double novoValor` e `int id`, já disponíveis; não é necessário criar a classe DAO inteira.


## Tópico 9 — DAO, separação de responsabilidades e recursos JDBC

### Conceito

O padrão **DAO (Data Access Object)** concentra o acesso aos dados em uma classe específica. Em vez de permitir que uma tela Swing abra conexões ou escreva SQL, a interface chama métodos como `inserir`, `listarTodos`, `buscarPorId`, `atualizar` e `remover`. O DAO contém a lógica de persistência, enquanto a interface cuida da interação com o usuário.

As conexões, os statements e os resultados são recursos que devem ser encerrados. O `try-with-resources` facilita esse cuidado. Exceções de banco também precisam ser tratadas ou propagadas de forma que a aplicação não informe sucesso quando a operação falhou.

### Exemplo guiado

A interface pode chamar um serviço ou, neste exemplo simplificado, o próprio DAO:

```
// Na ação do botão da tela Swing:  
Quarto quarto = lerDadosDaTela();  
quartoDAO.inserir(quarto);  
atualizarTabela(quartoDAO.listarTodos());
```

O DAO executa SQL sem depender de `JButton`, `JTextField` ou `JTable`:

```
public List\<Quarto\> listarTodos() throws SQLException \{  
    List\<Quarto\> lista = new ArrayList\<\>();  
    String sql = "SELECT \* FROM quarto ORDER BY numero";  
  
    try (Connection conn = Conexao.abrir();  
         PreparedStatement ps = conn.prepareStatement(sql);  
         ResultSet rs = ps.executeQuery()) \{  
  
        while (rs.next()) \{  
            lista.add(criarQuarto(rs));  
        \}  
    \}  
    return lista;  
\}
```

**Acompanhamento:** `Conexao` sabe **como abrir** o banco, `QuartoDAO` sabe **como persistir** quartos e a tela sabe **como interagir** com os usuários. Essa divisão facilita mudanças e testes.

### Questões

**Questão 17 — Conceitual.** Uma aplicação possui código SQL repetido em três botões Swing diferentes. Justifique a criação de um `QuartoDAO` e explique o que deve permanecer na tela e o que deve ser movido para o DAO. Inclua na resposta o motivo de utilizar `try-with-resources`.

**Questão 18 — Análise de arquitetura.** Considere o fluxo `JFrame → Connection → SQL → SQLite`. Proponha um fluxo mais organizado utilizando `QuartoDAO`. Apresente **duas assinaturas de métodos** que deveriam existir no DAO — uma para consulta e outra para alteração — e explique quem seria responsável por chamar esses métodos.


# Bloco III — Hibernate e Jakarta Persistence

## Tópico 10 — ORM: diferença entre Hibernate, JPA e JDBC

### Conceito

**ORM (Object-Relational Mapping)** é a técnica de relacionar objetos de uma linguagem orientada a objetos a registros de tabelas relacionais. **Hibernate** é um framework ORM que executa grande parte dessa tradução automaticamente. A **Jakarta Persistence (JPA)** define uma especificação e uma API para persistência de entidades, da qual Hibernate é uma implementação bastante conhecida.

A diferença em relação ao JDBC manual é a **camada de abstração**. Com JDBC, escrevemos diretamente o `INSERT`, preenchemos os parâmetros e reconstruímos os objetos via `ResultSet`. Com JPA/Hibernate, trabalhamos com entidades e com um `EntityManager`; Hibernate continua utilizando mecanismos como JDBC para se comunicar com o banco.

### Exemplo guiado

Compare os dois estilos:

```
// JDBC: comando SQL e parâmetros definidos manualmente.  
PreparedStatement ps = conn.prepareStatement(  
    "INSERT INTO quarto (numero, valor\_diaria) VALUES (?, ?)"  
);  
ps.setInt(1, 101);  
ps.setDouble(2, 180.0);  
ps.executeUpdate();

// JPA com Hibernate: entidade já mapeada.  
em.getTransaction().begin();  
em.persist(quarto);  
em.getTransaction().commit();
```

**Acompanhamento:** as duas abordagens gravam dados relacionais, mas a segunda deixa a geração do SQL de inserção para o ORM. Isso não dispensa conhecimento de SQL, tabelas, chaves ou transações.

### Questões

**Questão 19 — Conceitual.** Diferencie **JDBC**, **Jakarta Persistence** e **Hibernate**. Explique por que a afirmação “Hibernate elimina o uso de JDBC e a necessidade de conhecer SQL” está incorreta.

**Questão 20 — Análise.** Considere um objeto `Quarto` com os atributos `id`, `numero`, `tipo` e `valorDiaria`. Relacione cada elemento orientado a objetos com seu equivalente no banco relacional. Depois, explique qual trabalho é feito manualmente pelo programador com JDBC e qual pode ser automatizado por um ORM.


## Tópico 11 — Entidades e anotações JPA

### Conceito

Uma classe anotada com **`@Entity`** representa uma entidade persistente. **`@Table`** permite definir o nome da tabela; **`@Id`** marca o identificador; **`@GeneratedValue`** configura a geração do ID; **`@Column`** personaliza a coluna; e **`@Enumerated(EnumType.STRING)`** permite gravar um enum por seu nome, em vez de sua posição numérica.

Para o mapeamento básico com JPA, a entidade deve possuir um construtor sem argumentos `public` ou `protected`. Um identificador técnico `id` não precisa ser igual ao número do quarto exibido para os usuários.

### Exemplo guiado

```
@Entity  
@Table(name = "quartos")  
public class Quarto \{  
    @Id  
    @GeneratedValue(strategy = GenerationType.IDENTITY)  
    private Long id;  
  
    @Column(nullable = false, unique = true)  
    private int numero;  
  
    @Enumerated(EnumType.STRING)  
    private Tipo tipo;  
  
    protected Quarto() \{ \}  
  
    // Outros construtores, getters e setters.  
\}
```

**Acompanhamento:** `@Entity` permite que a classe participe do gerenciamento de persistência; `@Id` identifica a chave; `@GeneratedValue` delega a geração do identificador ao mecanismo configurado; `@Enumerated(EnumType.STRING)` favorece a leitura dos dados e evita problemas causados por mudança na ordem dos valores de um enum.

### Questões

**Questão 21 — Conceitual.** Explique o papel de `@Entity`, `@Id`, `@GeneratedValue` e `@Enumerated(EnumType.STRING)`. Por que gravar `Tipo.DUPLO` como texto costuma ser mais seguro que gravar sua posição numérica?

**Questão 22 — Criação de código.** O trecho a seguir deverá representar uma entidade JPA da tabela `hospedes`. Complete apenas as **anotações** necessárias para indicar entidade, nome da tabela, chave primária e geração automática do ID.

```
// Anotações aqui  
public class Hospede \{  
    // Anotações aqui  
    private Long id;  
  
    protected Hospede() \{ \}  
\}
```


## Tópico 12 — `EntityManager`, transações e ciclo de vida

### Conceito

O **`EntityManager`** administra entidades dentro de um contexto de persistência. Uma entidade recém-criada começa no estado **new/transient**; após `persist()`, passa a ser **managed**; ao encerrar o contexto, pode tornar-se **detached**; ao chamar `remove()` para uma entidade gerenciada, entra no estado **removed**.

O **dirty checking** permite ao Hibernate detectar alterações em entidades gerenciadas e sincronizá-las com o banco durante o `flush`/`commit`. Operações de escrita devem ser realizadas com transações apropriadas. Uma entidade desconectada do contexto não terá suas alterações automaticamente persistidas apenas porque um setter foi chamado.

### Exemplo guiado

```
EntityManager em = JPAUtil.criarEntityManager();  
try \{  
    em.getTransaction().begin();  
  
    Quarto quarto = em.find(Quarto.class, 1L);  
    if (quarto != null) \{  
        quarto.setValorDiaria(220.0);  
    \}  
  
    em.getTransaction().commit();  
\} catch (RuntimeException e) \{  
    if (em.getTransaction().isActive()) \{  
        em.getTransaction().rollback();  
    \}  
    throw e;  
\} finally \{  
    em.close();  
\}
```

**Acompanhamento:** `find()` carrega um objeto gerenciado; o setter modifica seu estado; no `commit()`, o ORM pode gerar o `UPDATE`. O bloco de erro realiza `rollback` quando ainda existe uma transação ativa.

### Questões

**Questão 23 — Conceitual.** Explique os estados **new**, **managed** e **detached**, utilizando o ciclo de vida de um objeto `Quarto`. Relacione o estado **managed** ao mecanismo de dirty checking.

**Questão 24 — Análise de código.** Um aluno escreveu:

```
EntityManager em = JPAUtil.criarEntityManager();  
Quarto q = em.find(Quarto.class, 1L);  
em.close();  
q.setValorDiaria(300.0);
```

O aluno espera que o novo valor seja automaticamente salvo no banco. Explique por que essa expectativa está errada e descreva a ordem correta de **transação, busca, alteração, commit e fechamento**.


## Tópico 13 — JPQL e mapeamento de relacionamentos

### Conceito

**JPQL** consulta **entidades e atributos** Java, enquanto o SQL tradicional consulta **tabelas e colunas**. Assim, uma consulta pode selecionar `Quarto` em vez de selecionar diretamente a tabela `quartos`. Para valores externos, também é possível utilizar parâmetros nomeados com `setParameter()`.

Nos relacionamentos, Hibernate/JPA mapeia referências a outros objetos como associações relacionais. Um campo `Reserva.quarto` anotado com **`@ManyToOne`** e **`@JoinColumn(name = "quarto\_id")`** indica uma referência a `Quarto` que pode ser representada por uma chave estrangeira na tabela de reservas.

### Exemplo guiado

Considere `Quarto` mapeado para a tabela `quartos`, com o atributo `valorDiaria` mapeado para a coluna `valor\_diaria`:

```
// SQL  
SELECT \* FROM quartos WHERE valor\_diaria \<= 300;

// JPQL  
List\<Quarto\> lista = em.createQuery(  
    "SELECT q FROM Quarto q WHERE q.valorDiaria \<= :maximo",  
    Quarto.class  
).setParameter("maximo", 300.0).getResultList();
```

E, em `Reserva`:

```
@ManyToOne  
@JoinColumn(name = "quarto\_id")  
private Quarto quarto;
```

**Acompanhamento:** a consulta usa `Quarto` e `valorDiaria` porque são nomes do modelo de objetos. A associação `Reserva → Quarto` é representada na aplicação por uma referência, e no banco pela coluna `quarto\_id`.

### Questões

**Questão 25 — Conceitual/análise.** Diferencie SQL e JPQL usando os exemplos apresentados. Explique por que `SELECT \* FROM quartos` não é uma consulta JPQL equivalente a `SELECT q FROM Quarto q` e qual o papel de `setParameter()`.

**Questão 26 — Criação de código.** Uma entidade `Reserva` deve guardar uma referência a um `Hospede`, e vários registros de reserva podem apontar para o mesmo hóspede. Escreva somente a declaração do atributo com as anotações de relacionamento adequadas, utilizando a coluna `hospede\_id`. Explique qual é o significado dessa coluna no banco relacional.


# Bloco IV — Spring Boot e APIs REST

> Este bloco retoma o trabalho guiado de pesquisa e implementação de Spring Boot. O exemplo mantém os dados em uma `List\<Quarto\>` para separar o estudo de HTTP e injeção de dependência do estudo de persistência em banco.

## Tópico 14 — Spring, Spring Boot, Beans e injeção de dependência

### Conceito

O **Spring Framework** oferece uma infraestrutura para organizar componentes e suas dependências. **Inversão de Controle (IoC)** significa que a criação e a ligação de componentes podem ser gerenciadas por um contêiner, em vez de ficarem inteiramente sob responsabilidade de cada classe. Um objeto gerenciado pelo Spring é chamado de **Bean**; **Injeção de Dependência (DI)** é o fornecimento de um objeto do qual outro componente precisa.

**Spring Boot** facilita a inicialização de aplicações Spring por meio de starters, auto-configuração e execução simplificada, frequentemente com um servidor Web embutido. Em uma API do hotel, o `QuartoController` pode receber um `QuartoService` por seu construtor, sem criar a dependência diretamente por `new`.

### Exemplo guiado

```
@Service  
public class QuartoService \{  
    public List\<Quarto\> listar() \{  
        return List.of(); // simplificação para o exemplo  
    \}  
\}

@RestController  
@RequestMapping("/quartos")  
public class QuartoController \{  
    private final QuartoService service;  
  
    public QuartoController(QuartoService service) \{  
        this.service = service;  
    \}  
  
    @GetMapping  
    public List\<Quarto\> listar() \{  
        return service.listar();  
    \}  
\}
```

**Acompanhamento:** `@Service` registra uma classe da camada de serviço como componente Spring; o `Controller` declara sua dependência no construtor; o contêiner fornece uma instância gerenciada. Assim, o Controller se concentra no acesso HTTP, enquanto o Service concentra as operações da aplicação.

### Questões

**Questão 27 — Conceitual.** Diferencie **Spring Framework** de **Spring Boot**. Explique o significado de **Bean** e **Injeção de Dependência**, indicando uma vantagem de receber o Service pelo construtor em vez de instanciá-lo diretamente dentro do Controller.

**Questão 28 — Análise/criação.** Considere que existe uma classe `ReservaService` anotada com `@Service`. Escreva somente o **atributo final** e o **construtor** necessários para que `ReservaController` receba essa dependência. Explique qual componente é responsável por fornecer a instância de `ReservaService`.


## Tópico 15 — REST, métodos HTTP, JSON e Controllers

### Conceito

Uma **API REST** expõe recursos por meio de URLs e requisições HTTP. Em um CRUD comum, `GET` consulta, `POST` cria, `PUT` substitui ou atualiza um recurso e `DELETE` o remove. O corpo de uma requisição pode conter **JSON**, que o Spring converte para um objeto Java com `@RequestBody`; os valores presentes no caminho da URL podem ser capturados com `@PathVariable`; parâmetros de consulta podem ser recebidos por `@RequestParam`.

A anotação **`@RestController`** identifica o componente responsável por responder às requisições. **`@GetMapping`**, **`@PostMapping`**, **`@PutMapping`** e **`@DeleteMapping`** associam métodos Java aos respectivos métodos HTTP. Respostas também possuem **status**, como `200 OK`, `201 Created`, `204 No Content`, `400 Bad Request` e `404 Not Found`.

### Exemplo guiado

```
@RestController  
@RequestMapping("/quartos")  
public class QuartoController \{  
    private final QuartoService service;  
  
    public QuartoController(QuartoService service) \{  
        this.service = service;  
    \}  
  
    @GetMapping("/\{id\}")  
    public Quarto buscar(@PathVariable Long id) \{  
        return service.buscarPorId(id);  
    \}  
  
    @PostMapping  
    public Quarto criar(@RequestBody Quarto quarto) \{  
        return service.adicionar(quarto);  
    \}  
\}
```

**Acompanhamento:** `GET /quartos/3` extrai o ID `3` e chama `buscarPorId(3L)`. Um `POST /quartos` com um JSON no corpo cria um objeto Java e o repassa ao Service. Numa implementação REST completa, é importante também tratar corretamente a ausência de um quarto, retornando `404`, e sinalizar a criação bem-sucedida com `201` quando apropriado.

A integração com os conteúdos anteriores permite implementar um filtro no Service:

```
public List\<Quarto\> buscarPorTipo(Tipo tipo) \{  
    return quartos.stream()  
        .filter(q -\> q.getTipo() == tipo)  
        .toList();  
\}
```

### Questões

**Questão 29 — Conceitual/análise.** Uma API possui os endpoints `GET /quartos`, `POST /quartos`, `PUT /quartos/7` e `DELETE /quartos/7`. Relacione cada um a uma operação de CRUD. Depois, explique quando seria apropriado responder com os status HTTP **201**, **204**, **400** e **404**.

**Questão 30 — Criação de código.** Considere que o Service já possui `List\<Quarto\> buscarPorTipo(Tipo tipo)`. No Controller com `@RequestMapping("/quartos")`, escreva apenas o método do endpoint que deve responder a `GET /quartos/tipo?tipo=DUPLO`, utilizando a anotação correta para receber o parâmetro `tipo` e delegando a consulta ao Service. Explique como o parâmetro textual `DUPLO` se relaciona com o enum `Tipo`.
