# Trabalho Guiado — Introdução ao Spring Boot e APIs REST


## Equipes

O trabalho poderá ser realizado individualmente ou em grupos de até 3 alunos.


## Entregáveis

O aluno deverá entregar:

### Parte teórica

Documento contendo as respostas das pesquisas.


### Parte prática

Link para um repositório no Github com o código do projeto.


O projeto deverá possuir no mínimo:

```
GET    /quartos  
GET    /quartos/\{id\}  
POST   /quartos  
PUT    /quartos/\{id\}  
DELETE /quartos/\{id\}
```

Além de pelo menos:

```
1 endpoint de consulta/filtro
```


## Data da entrega

30/11/2026 até 23:59


## Entrega via Google Forms

Realize a entrega do trabalho utilizando o link: [https://forms.gle/cACBL5SdjMiy85Fz8](https://forms.gle/cACBL5SdjMiy85Fz8)


# 1. Objetivo

Neste trabalho, você irá pesquisar os principais conceitos do **Spring Boot** e, em seguida, construir gradualmente uma API REST para o SistemaHotel.

Utilize as entidades que foram criadas nas últimas aulas. Os códigos estão disponíveis na pasta [códigos](https://github.com/biazottoj/unespar-2026-1/tree/main/programacao%20orientada%20a%20objetos/codigos).

O trabalho possui duas partes:

```
Parte 1  
Pesquisa conceitual  
  
Parte 2  
Walkthrough prático
```

Ao final, você deverá compreender:

```
Spring  
Spring Boot  
API REST  
HTTP  
JSON  
Controller  
Service  
Injeção de Dependência  
Endpoints
```

e deverá possuir uma aplicação funcional.


# Parte 1 — Pesquisa

# 2. O que é Spring?

Pesquise e explique com suas próprias palavras:

> O que é o Spring Framework?

Sua resposta deverá explicar pelo menos:

- qual problema o Spring procura resolver;

- o que significa Inversão de Controle;

- o que significa Injeção de Dependência;

- o que é um Bean.


# 3. O que é Spring Boot?

Pesquise:

> Qual é a diferença entre Spring Framework e Spring Boot?

Inclua na resposta:

- auto-configuração;

- starters;

- servidor embutido;

- redução de configurações;

- execução de aplicações standalone.


# 4. Spring não é Spring Boot

Uma maneira simplificada de pensar:

```
Spring Framework  
→ infraestrutura e recursos  
  
Spring Boot  
→ facilita configuração e inicialização  
  de aplicações Spring
```

Spring Boot utiliza o ecossistema Spring.

Ele não substitui o Spring Framework.


# 5. O que é uma API?

Pesquise:

> O que significa API?

Depois explique:

> O que caracteriza uma API REST?

Inclua os conceitos:

```
recurso  
endpoint  
requisição  
resposta  
HTTP  
JSON
```


# 6. Métodos HTTP

Pesquise o papel de:

| Método | Operação comum |
| - | - |
| GET | Consultar |
| POST | Criar |
| PUT | Atualizar |
| DELETE | Remover |


Depois relacione com CRUD:

```
CREATE → POST  
READ → GET  
UPDATE → PUT  
DELETE → DELETE
```


# 7. Status HTTP

Pesquise e explique:

```
200 OK  
201 Created  
204 No Content  
400 Bad Request  
404 Not Found  
500 Internal Server Error
```

Dê um exemplo de situação em que cada status poderia ocorrer no SistemaHotel.


# 8. JSON

Uma API normalmente não envia objetos Java diretamente pela rede.

Os dados são representados em formatos como JSON.

Objeto:

```
Quarto quarto =  
    new Quarto(  
        101,  
        180.0,  
        Tipo.SIMPLES  
    );
```

Possível JSON:

```
\{  
    "numero": 101,  
    "valorDiaria": 180.0,  
    "tipo": "SIMPLES"  
\}
```

Pesquise:

> Qual biblioteca é normalmente utilizada pelo Spring Boot para conversão entre objetos Java e JSON?


# Parte 2 — Walkthrough Prático

# 9. O que vamos construir

Vamos construir:

```
Cliente HTTP  
      ↓  
API REST  
      ↓  
Controller  
      ↓  
Service  
      ↓  
List\<Quarto\>
```

Nesta primeira atividade não utilizaremos banco de dados.

O objetivo é compreender Spring Boot e REST antes de adicionar persistência.


# 10. Requisitos

Utilize:

```
Java 17 ou superior  
Maven  
Spring Boot  
Spring Web
```

A versão estável de referência deste material original é:

```
Spring Boot 4.1.2
```


# 11. Spring Initializr

Acesse:

```
https://start.spring.io
```

Configure:

```
Project:  
Maven  
  
Language:  
Java  
  
Spring Boot:  
versão estável  
  
Group:  
br.edu.unespar  
  
Artifact:  
hotel-api  
  
Packaging:  
Jar  
  
Java:  
17 ou superior
```

Adicione:

```
Spring Web
```

Gere o projeto.


# 12. Estrutura inicial

O projeto deverá possuir algo semelhante a:

```
src/main/java  
└── br.edu.unespar.hotel  
    └── HotelApiApplication.java
```

E:

```
src/main/resources  
└── application.properties
```


# 13. Classe principal

O Spring Initializr gera:

```
@SpringBootApplication  
public class HotelApiApplication \{  
  
    public static void main(  
            String\[\] args) \{  
  
        SpringApplication.run(  
            HotelApiApplication.class,  
            args  
        );  
    \}  
\}
```


# 14. `@SpringBootApplication`

Essa anotação reúne funcionalidades importantes.

Podemos pensar nela como uma combinação de:

```
@Configuration  
@EnableAutoConfiguration  
@ComponentScan
```

Para esta primeira aula, a ideia principal é:

> Esta é a classe de inicialização da aplicação Spring Boot.


# 15. Executando

No terminal:

```
./mvnw spring-boot:run
```

Ou execute a classe:

```
HotelApiApplication
```

diretamente pela IDE.

Por padrão, uma aplicação Web utilizará:

```
localhost:8080
```


# 16. Nosso primeiro endpoint

Crie:

```
package br.edu.unespar.hotel.controller;  
  
import org.springframework.web.bind.annotation.GetMapping;  
import org.springframework.web.bind.annotation.RestController;  
  
@RestController  
public class TesteController \{  
  
    @GetMapping("/teste")  
    public String teste() \{  
  
        return "SistemaHotel funcionando";  
    \}  
\}
```


# 17. Testando

Abra:

```
http://localhost:8080/teste
```

Resposta:

```
SistemaHotel funcionando
```


# 18. O que aconteceu?

```
Navegador  
↓  
GET /teste  
↓  
Spring Boot  
↓  
TesteController  
↓  
teste()  
↓  
String  
↓  
HTTP Response
```


# 19. `@RestController`

A anotação:

```
@RestController
```

indica que a classe recebe requisições HTTP e que os valores retornados pelos métodos fazem parte da resposta.


# 20. `@GetMapping`

```
@GetMapping("/teste")
```

significa:

> Quando chegar uma requisição HTTP GET para `/teste`, execute este método.


# 21. Criando `Tipo`

```
package br.edu.unespar.hotel.model;  
  
public enum Tipo \{  
  
    SIMPLES,  
    DUPLO,  
    COBERTURA  
\}
```


# 22. Criando `Quarto`

```
package br.edu.unespar.hotel.model;  
  
public class Quarto \{  
  
    private Long id;  
  
    private int numero;  
  
    private double valorDiaria;  
  
    private Tipo tipo;  
  
    public Quarto() \{  
    \}  
  
    public Quarto(  
            Long id,  
            int numero,  
            double valorDiaria,  
            Tipo tipo) \{  
  
        this.id = id;  
        this.numero = numero;  
        this.valorDiaria =  
            valorDiaria;  
        this.tipo = tipo;  
    \}  
  
    public Long getId() \{  
        return id;  
    \}  
  
    public void setId(Long id) \{  
        this.id = id;  
    \}  
  
    public int getNumero() \{  
        return numero;  
    \}  
  
    public void setNumero(  
            int numero) \{  
  
        this.numero = numero;  
    \}  
  
    public double getValorDiaria() \{  
        return valorDiaria;  
    \}  
  
    public void setValorDiaria(  
            double valorDiaria) \{  
  
        this.valorDiaria =  
            valorDiaria;  
    \}  
  
    public Tipo getTipo() \{  
        return tipo;  
    \}  
  
    public void setTipo(  
            Tipo tipo) \{  
  
        this.tipo = tipo;  
    \}  
\}
```


# 23. Retornando um objeto

Crie:

```
@GetMapping("/quarto")  
public Quarto obterQuarto() \{  
  
    return new Quarto(  
        1L,  
        101,  
        180.0,  
        Tipo.SIMPLES  
    );  
\}
```

Acesse:

```
GET /quarto
```

Resposta semelhante:

```
\{  
    "id": 1,  
    "numero": 101,  
    "valorDiaria": 180.0,  
    "tipo": "SIMPLES"  
\}
```


# 24. Quem criou o JSON?

Nós não escrevemos:

```
"\{\\"id\\":1,...\}"
```

Spring Boot utiliza conversores HTTP para transformar o objeto em JSON automaticamente.

Fluxo:

```
Quarto  
↓  
Spring  
↓  
Jackson  
↓  
JSON
```


# 25. Controller não deve fazer tudo

Uma arquitetura comum é:

```
Controller  
↓  
Service  
↓  
Repository
```

Responsabilidades:

```
Controller  
→ HTTP  
  
Service  
→ regras de negócio  
  
Repository  
→ persistência
```

Nesta atividade ainda não teremos banco de dados.


# 26. Criando o Service

```
package br.edu.unespar.hotel.service;  
  
import java.util.ArrayList;  
import java.util.List;  
  
import org.springframework.stereotype.Service;  
  
import br.edu.unespar.hotel.model.\*;  
  
@Service  
public class QuartoService \{  
  
    private final List\<Quarto\> quartos =  
        new ArrayList\<\>();  
  
    private long proximoId = 1;  
  
    public QuartoService() \{  
  
        quartos.add(  
            new Quarto(  
                proximoId++,  
                101,  
                180,  
                Tipo.SIMPLES  
            )  
        );  
  
        quartos.add(  
            new Quarto(  
                proximoId++,  
                102,  
                250,  
                Tipo.DUPLO  
            )  
        );  
    \}  
  
    public List\<Quarto\> listar() \{  
  
        return quartos;  
    \}  
\}
```


# 27. `@Service`

```
@Service
```

informa ao Spring:

> Esta classe representa um componente da camada de serviço.

Spring cria e gerencia uma instância dela.

Essa instância é um:

```
Bean
```


# 28. Injeção de Dependência

Controller:

```
@RestController  
@RequestMapping("/quartos")  
public class QuartoController \{  
  
    private final QuartoService service;  
  
    public QuartoController(  
            QuartoService service) \{  
  
        this.service = service;  
    \}  
\}
```

Observe:

```
Controller precisa de Service
```

Mas não fazemos:

```
new QuartoService()
```

Spring fornece a dependência.


# 29. Por que isso é importante?

Sem injeção:

```
QuartoService service =  
    new QuartoService();
```

O Controller decide:

```
qual implementação  
como criar  
quando criar
```

Com Spring:

```
Spring  
↓  
cria QuartoService  
↓  
injeta no Controller
```

Isso reduz acoplamento.


# 30. Listando quartos

```
@GetMapping  
public List\<Quarto\> listar() \{  
  
    return service.listar();  
\}
```

Como a classe possui:

```
@RequestMapping("/quartos")
```

o endpoint será:

```
GET /quartos
```


# 31. Teste

Acesse:

```
http://localhost:8080/quartos
```

Resultado:

```
\[  
    \{  
        "id": 1,  
        "numero": 101,  
        "valorDiaria": 180.0,  
        "tipo": "SIMPLES"  
    \},  
    \{  
        "id": 2,  
        "numero": 102,  
        "valorDiaria": 250.0,  
        "tipo": "DUPLO"  
    \}  
\]
```


# 32. Buscar por ID

No Service:

```
public Quarto buscarPorId(  
        Long id) \{  
  
    return quartos.stream()  
        .filter(  
            q -\>  
                q.getId()  
                .equals(id)  
        )  
        .findFirst()  
        .orElse(null);  
\}
```

Observe a integração com conteúdos anteriores:

```
Collection  
Stream  
Lambda  
Predicate  
Optional
```


# 33. Endpoint com parâmetro na URL

Controller:

```
@GetMapping("/\{id\}")  
public Quarto buscar(  
        @PathVariable Long id) \{  
  
    return service.buscarPorId(id);  
\}
```

Teste:

```
GET /quartos/1
```


# 34. `@PathVariable`

Temos:

```
/quartos/\{id\}
```

e:

```
@PathVariable Long id
```

Spring extrai o valor da URL.

Por exemplo:

```
/quartos/10
```

resulta em:

```
id = 10
```


# 35. CREATE — POST

No Service:

```
public Quarto adicionar(  
        Quarto quarto) \{  
  
    quarto.setId(  
        proximoId++  
    );  
  
    quartos.add(  
        quarto  
    );  
  
    return quarto;  
\}
```

Controller:

```
@PostMapping  
public Quarto adicionar(  
        @RequestBody Quarto quarto) \{  
  
    return service.adicionar(  
        quarto  
    );  
\}
```


# 36. `@RequestBody`

Quando enviamos:

```
\{  
    "numero": 201,  
    "valorDiaria": 450,  
    "tipo": "COBERTURA"  
\}
```

Spring transforma:

```
JSON  
↓  
Quarto
```

Isso ocorre por causa:

```
@RequestBody
```


# 37. Testando POST

Utilize:

- Postman;

- Insomnia;

- Bruno;

- `curl`;

- cliente HTTP da IDE.

Requisição:

```
POST /quartos
```

Body:

```
\{  
    "numero": 201,  
    "valorDiaria": 450,  
    "tipo": "COBERTURA"  
\}
```


# 38. UPDATE — PUT

Service:

```
public Quarto atualizar(  
        Long id,  
        Quarto novosDados) \{  
  
    Quarto quarto =  
        buscarPorId(id);  
  
    if (quarto == null) \{  
  
        return null;  
    \}  
  
    quarto.setNumero(  
        novosDados.getNumero()  
    );  
  
    quarto.setValorDiaria(  
        novosDados  
            .getValorDiaria()  
    );  
  
    quarto.setTipo(  
        novosDados.getTipo()  
    );  
  
    return quarto;  
\}
```

Controller:

```
@PutMapping("/\{id\}")  
public Quarto atualizar(  
        @PathVariable Long id,  
        @RequestBody Quarto quarto) \{  
  
    return service.atualizar(  
        id,  
        quarto  
    );  
\}
```


# 39. Testando PUT

```
PUT /quartos/1
```

Body:

```
\{  
    "numero": 101,  
    "valorDiaria": 220,  
    "tipo": "DUPLO"  
\}
```


# 40. DELETE

Service:

```
public boolean remover(  
        Long id) \{  
  
    return quartos.removeIf(  
        q -\>  
            q.getId()  
             .equals(id)  
    );  
\}
```

Controller:

```
@DeleteMapping("/\{id\}")  
public void remover(  
        @PathVariable Long id) \{  
  
    service.remover(id);  
\}
```


# 41. CRUD completo

| Operação | HTTP | Endpoint |
| - | - | - |
| Listar | GET | `/quartos` |
| Buscar | GET | `/quartos/\{id\}` |
| Criar | POST | `/quartos` |
| Atualizar | PUT | `/quartos/\{id\}` |
| Excluir | DELETE | `/quartos/\{id\}` |



# 42. HTTP versus método Java

Observe:

```
GET /quartos  
↓  
listar()  
  
GET /quartos/1  
↓  
buscar(1)  
  
POST /quartos  
↓  
adicionar(...)  
  
PUT /quartos/1  
↓  
atualizar(...)  
  
DELETE /quartos/1  
↓  
remover(1)
```

Spring faz o mapeamento entre:

```
HTTP  
↔  
Java
```


# 43. Adicionando filtros

Queremos:

```
GET /quartos?tipo=DUPLO
```

Controller:

```
@GetMapping("/tipo")  
public List\<Quarto\> buscarPorTipo(  
        @RequestParam Tipo tipo) \{  
  
    return service  
        .buscarPorTipo(tipo);  
\}
```

Service:

```
public List\<Quarto\> buscarPorTipo(  
        Tipo tipo) \{  
  
    return quartos.stream()  
        .filter(  
            q -\>  
                q.getTipo()  
                == tipo  
        )  
        .toList();  
\}
```


# 44. `@RequestParam`

Exemplo:

```
/quartos/tipo?tipo=DUPLO
```

Spring lê:

```
tipo=DUPLO
```

e converte para:

```
Tipo.DUPLO
```


# 45. Camadas

Ao final temos:

```
HTTP  
↓  
Controller  
↓  
Service  
↓  
Collection
```

Responsabilidade:

```
Controller  
→ traduz HTTP para chamadas Java  
  
Service  
→ executa regras  
  
Collection  
→ armazena os dados
```


# 46. Não coloque regra de negócio no Controller

Evite:

```
@PostMapping  
public Quarto adicionar(  
        @RequestBody Quarto quarto) \{  
  
    // validar preço  
    // verificar duplicidade  
    // adicionar  
    // calcular tarifa  
    // etc.  
\}
```

Prefira:

```
Controller  
↓  
Service  
↓  
regras
```


# 47. Atividade de pesquisa — Anotações

Pesquise e explique, em uma frase cada:

```
@SpringBootApplication  
@RestController  
@RequestMapping  
@GetMapping  
@PostMapping  
@PutMapping  
@DeleteMapping  
@PathVariable  
@RequestParam  
@RequestBody  
@Service
```

Para cada uma, indique:

```
Onde é utilizada?  
Para que serve?
```


# 48. Atividade prática 1

Implemente:

```
GET /quartos
```


# 49. Atividade prática 2

Implemente:

```
GET /quartos/\{id\}
```


# 50. Atividade prática 3

Implemente:

```
POST /quartos
```


# 51. Atividade prática 4

Implemente:

```
PUT /quartos/\{id\}
```


# 52. Atividade prática 5

Implemente:

```
DELETE /quartos/\{id\}
```


# 53. Atividade prática 6

Implemente:

```
GET /quartos/tipo?tipo=DUPLO
```

utilizando:

```
Stream  
+  
Predicate/Lambda
```


# 54. Pesquisa — Arquitetura

Pesquise:

> Qual a diferença entre Controller, Service e Repository em uma aplicação Spring?

Produza uma tabela:

| Camada | Responsabilidade |
| - | - |
| Controller |  |
| Service |  |
| Repository |  |



# 55. Pesquisa — IoC e DI

Explique a diferença entre:

```
Inversão de Controle
```

e:

```
Injeção de Dependência
```

Depois responda:

> Por que o `QuartoController` não precisa executar `new QuartoService()`?


# 56. Pesquisa — servidor embutido

Responda:

> Por que não precisamos instalar manualmente um servidor Tomcat para executar essa aplicação?

Relacione a resposta com Spring Boot e servidor embutido.


# 57. Pesquisa — auto-configuração

Investigue:

> O que significa auto-configuration no Spring Boot?

Depois identifique pelo menos duas configurações que Spring Boot realizou automaticamente neste projeto.


# 58. Desafio — Disponibilidade

Adicione:

```
public enum Disponibilidade \{  
  
    DISPONIVEL,  
    OCUPADO,  
    MANUTENCAO  
\}
```

Inclua em `Quarto`.

Crie:

```
GET /quartos/disponiveis
```


# 59. Desafio — filtros combinados

Implemente:

```
GET /quartos/consulta
```

aceitando opcionalmente:

```
tipo  
valorMaximo  
disponibilidade
```

Exemplo:

```
/quartos/consulta  
    ?tipo=DUPLO  
    &valorMaximo=300  
    &disponibilidade=DISPONIVEL
```

Utilize:

```
Predicate  
+  
Stream
```

para combinar os critérios.


# 60. Desafio — Strategy

Reutilize o conhecimento do trabalho anterior.

Crie:

```
EstrategiaPreco
```

com pelo menos:

```
PrecoNormal  
PrecoPromocional
```

Crie um endpoint:

```
GET /quartos/\{id\}/preco
```

com:

```
dias  
tipoTarifa
```

Exemplo:

```
/quartos/1/preco  
    ?dias=5  
    &tipoTarifa=PROMOCIONAL
```


# 61. Próximo passo: banco de dados

Neste walkthrough os dados estão em:

```
List\<Quarto\>
```

Portanto:

```
encerrou aplicação  
↓  
dados desaparecem
```

Um próximo passo natural será substituir:

```
List\<Quarto\>
```

por:

```
Repository  
↓  
Banco de dados
```

utilizando:

```
Spring Data JPA
```


# 62. O que Spring Boot automatizou?

Ao longo do projeto, nós não configuramos manualmente:

```
servidor HTTP  
conversão JSON  
roteamento básico  
ciclo de vida dos componentes  
injeção das dependências
```

Spring Boot cuidou de grande parte dessa infraestrutura.


# 63. Comparação com Swing

Na aplicação Swing:

```
Usuário  
↓  
JButton  
↓  
ActionListener  
↓  
Service
```

Na API:

```
Cliente  
↓  
HTTP  
↓  
Controller  
↓  
Service
```

Observe que:

```
Service
```

continua representando as regras do sistema.

O que muda principalmente é a camada de entrada.


# 64. Swing versus Spring Boot

| Swing | Spring Boot REST |
| - | - |
| Interface desktop | Interface HTTP |
| `JButton` | Endpoint |
| ActionListener | Controller |
| Campos | JSON |
| JTable | Resposta JSON |
| Usuário local | Cliente HTTP |



