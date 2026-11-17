# Estudo guiado — Do zero ao MongoDB com Docker

**Disciplina:** Banco de Dados  
**Tema:** Introdução prática a bancos NoSQL orientados a documentos  
**Ambiente:** Ubuntu 22.04, 24.04 ou 26.04, terminal, Docker Engine, Docker Compose e MongoDB 8.0  
**Cenário:** Sistema de reservas de hotel  
**Modalidade:** Estudo individual guiado, com verificações de cada etapa

> **Objetivo:** ao concluir este material, você terá instalado o Docker, executado um servidor MongoDB em um contêiner e manipulado hóspedes, quartos e reservas utilizando a linguagem de consultas do MongoDB. Nenhuma instalação do MongoDB diretamente no Ubuntu será necessária.
>
> **Atenção:** este é um laboratório didático **local**. O usuário administrativo e a senha dos exemplos não devem ser reutilizados em sistemas reais. Os comandos foram planejados para não modificar o banco PostgreSQL das aulas anteriores.

## Como seguir este material

Execute as etapas **na ordem apresentada**. Os comandos identificados como **Terminal Ubuntu** são executados no terminal Linux. Os comandos identificados como **MongoDB / mongosh** são executados *depois de entrar no shell do MongoDB*. Não tente executar `db.hospedes.find()` no Bash nem `docker compose` no `mongosh`.

Ao longo do estudo há perguntas de reflexão e resultados esperados. Faça os testes em sua máquina, observe o retorno e registre o que mudou.

---

# Parte 1 — Entendendo o ambiente

## Etapa 1. Revisão: SQL e NoSQL

No PostgreSQL, você trabalhou com **tabelas**, **linhas**, **colunas** e **chaves estrangeiras**. Por exemplo, a tabela `reserva` guarda uma referência à tabela `hospede`.

O termo **NoSQL** é utilizado para uma família de bancos de dados que não se limita ao modelo relacional. Existem bancos chave-valor, orientados a documentos, a grafos e de outras categorias. **MongoDB** é um exemplo de banco orientado a **documentos**.

| Conceito familiar no PostgreSQL | Conceito no MongoDB | Observação |
|---|---|---|
| Database | Database | Contém os dados da aplicação |
| Table | Collection | Conjunto de documentos |
| Row | Document | Registro com campos e valores |
| Column | Field | Propriedade de um documento |
| Primary key | `_id` | Identificador único de cada documento |
| `SELECT` | `find()` | Consulta documentos |
| `INSERT` | `insertOne()` / `insertMany()` | Insere documentos |
| `UPDATE` | `updateOne()` / `updateMany()` | Modifica documentos |
| `DELETE` | `deleteOne()` / `deleteMany()` | Exclui documentos |

Em vez de um hóspede ocupar somente uma linha com colunas fixas, ele pode ser descrito assim:

```javascript
{
  _id: 1,
  nome: "Ana Martins",
  cidade: "Curitiba",
  contato: {
    email: "ana@exemplo.com",
    telefone: "41999990001"
  },
  tags: ["frequente", "corporativo"]
}
```

Repare que `contato` é um **objeto aninhado** e `tags` é um **array**. Isso permite representar dados relacionados dentro do próprio documento. O MongoDB armazena documentos em formato **BSON**, semelhante a JSON, mas com tipos adicionais, como datas.

**Para refletir:** no PostgreSQL, como você representaria vários telefones associados ao mesmo hóspede? Seria necessário criar outra tabela? E em um documento MongoDB?

## Etapa 2. O que é Docker?

Docker executa aplicações em **contêineres**. Neste laboratório:

- **Imagem:** pacote que contém o MongoDB e suas dependências (`mongo:8.0`).
- **Contêiner:** processo isolado iniciado a partir da imagem.
- **Docker Compose:** ferramenta que configura e inicia serviços a partir de um arquivo YAML.
- **Volume:** armazenamento persistente que preserva os dados do MongoDB mesmo quando o contêiner é removido.

```text
Seu computador Ubuntu
│
├── Docker Engine
│   └── Contêiner: mongo_hotel_aula
│       ├── MongoDB (servidor)
│       └── mongosh (cliente de terminal)
│
└── Volume Docker: mongo_hotel_dados
    └── Arquivos persistentes do banco
```

A diferença principal é: **o servidor MongoDB roda no contêiner**, mas os dados podem sobreviver à sua interrupção graças ao volume.

---

# Parte 2 — Instalando o Docker no Ubuntu

## Etapa 3. Conferir o sistema operacional

**Terminal Ubuntu:**

```bash
cat /etc/os-release
uname -m
```

Verifique se a distribuição é Ubuntu e identifique sua versão. Se você estiver usando Windows ou macOS, o caminho usual é instalar o **Docker Desktop** e continuar a partir da Parte 3. Se utilizar Linux Mint ou outro derivado, consulte as instruções específicas da distribuição.

## Etapa 4. Verificar se Docker já está instalado

**Terminal Ubuntu:**

```bash
docker --version
docker compose version
```

Se ambos os comandos retornarem versões e o serviço funcionar, **não reinstale o Docker**: avance para a Etapa 8.

Se aparecer `command not found`, siga com a instalação abaixo.

> **Antes de começar:** os comandos seguintes exigem permissão de administrador (`sudo`) e acesso à internet. Caso o computador seja gerenciado por um laboratório institucional, solicite autorização antes de modificar pacotes e repositórios.

## Etapa 5. Instalar as dependências necessárias

**Terminal Ubuntu:**

```bash
sudo apt update
sudo apt install -y ca-certificates curl
```

O `apt` é o gerenciador de pacotes do Ubuntu. A primeira linha atualiza o catálogo de pacotes; a segunda instala componentes usados na configuração do repositório oficial do Docker.

## Etapa 6. Adicionar o repositório oficial do Docker

**Terminal Ubuntu:**

```bash
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

Esses comandos criam o diretório de chaves, obtêm a chave oficial de assinatura e permitem sua leitura pelo gerenciador de pacotes.

Agora configure o repositório:

```bash
sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```

Finalmente:

```bash
sudo apt update
```

**O que aconteceu?** O Ubuntu agora sabe onde encontrar os pacotes oficiais do Docker e como verificar suas assinaturas.

> Se o `apt` indicar conflito com uma instalação preexistente de `docker.io`, `containerd` ou outro pacote, não remova pacotes às cegas. Siga a seção *Uninstall old versions* da documentação oficial: https://docs.docker.com/engine/install/ubuntu/.

## Etapa 7. Instalar Docker Engine e Compose

**Terminal Ubuntu:**

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin
```

Verifique o serviço:

```bash
sudo systemctl status docker
```

Se não estiver ativo:

```bash
sudo systemctl start docker
```

Use `q` para sair da visualização do `systemctl status` quando necessário.

## Etapa 8. Testar o Docker

**Terminal Ubuntu:**

```bash
sudo docker --version
sudo docker compose version
sudo docker run --rm hello-world
```

**Resultado esperado:** o contêiner `hello-world` exibe uma mensagem indicando que o Docker conseguiu obter e executar uma imagem.

### Por que utilizamos `sudo docker`?

No Ubuntu, é normal que uma instalação nova exija `sudo` para acessar o daemon do Docker. Neste estudo, todos os comandos Docker usam `sudo` para funcionar sem alterar grupos de usuários. O grupo `docker` fornece privilégios elevados e **não** deve ser habilitado indiscriminadamente.

**Checkpoint 1:** você conseguiu executar o `hello-world`? Se sim, o Docker está pronto.

---

# Parte 3 — Preparando um MongoDB com Docker Compose

## Etapa 9. Criar a pasta da atividade

**Terminal Ubuntu:**

```bash
mkdir -p ~/aula-nosql-hotel
cd ~/aula-nosql-hotel
pwd
```

O comando `pwd` deve mostrar o caminho da pasta criada. Vamos guardar ali os arquivos do laboratório.

## Etapa 10. Criar o arquivo de configuração

Crie um arquivo:

```bash
nano docker-compose-hotel-nosql.yml
```

Cole exatamente o conteúdo:

```yaml
# Ambiente didático, somente para a máquina local.
services:
  mongo:
    image: mongo:8.0
    container_name: mongo_hotel_aula
    restart: unless-stopped
    ports:
      - "127.0.0.1:27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin_aula
      MONGO_INITDB_ROOT_PASSWORD: AulaNoSQL_2026_Trocar
    volumes:
      - mongo_hotel_dados:/data/db

volumes:
  mongo_hotel_dados:
```

No editor `nano`, use **Ctrl+O**, **Enter** e **Ctrl+X** para salvar e sair.

**Entendendo o YAML:**

| Linha | Significado |
|---|---|
| `image: mongo:8.0` | Utiliza o MongoDB 8.0 |
| `container_name` | Nome do contêiner |
| `127.0.0.1:27017:27017` | Expõe a porta apenas no próprio computador |
| `MONGO_INITDB_ROOT_USERNAME` | Nome da conta administrativa inicial |
| `MONGO_INITDB_ROOT_PASSWORD` | Senha inicial de laboratório |
| `mongo_hotel_dados:/data/db` | Associa o banco a um volume persistente |

A senha de demonstração é visível no arquivo porque este é um exercício local. Não a utilize para dados reais. Em aplicações, prefira mecanismos de segredo apropriados. **Se o volume já tiver dados, alterar essas variáveis não redefine a senha antiga automaticamente.**

## Etapa 11. Iniciar o contêiner

**Terminal Ubuntu, dentro da pasta do projeto:**

```bash
sudo docker compose -f docker-compose-hotel-nosql.yml up -d
```

Na primeira execução, o Docker poderá precisar baixar a imagem. Depois, verifique:

```bash
sudo docker compose -f docker-compose-hotel-nosql.yml ps
```

**Resultado esperado:** o serviço `mongo` aparece com estado de execução (*running/up*).

Para ver mensagens recentes do servidor:

```bash
sudo docker compose -f docker-compose-hotel-nosql.yml logs --tail=30 mongo
```

**Checkpoint 2:** o contêiner `mongo_hotel_aula` está em execução?

## Etapa 12. Entrar no MongoDB

**Terminal Ubuntu:**

```bash
sudo docker compose -f docker-compose-hotel-nosql.yml exec mongo \
  mongosh --username admin_aula --authenticationDatabase admin
```

Quando o programa solicitar a senha, digite:

```text
AulaNoSQL_2026_Trocar
```

> Os caracteres podem não aparecer na tela enquanto você digita. Isso é normal. Não coloque a senha diretamente no comando do terminal.

A partir de agora você está no **mongosh**. Execute:

```javascript
db.runCommand({ ping: 1 })
```

**Resultado esperado:** um documento de resposta com `ok: 1`.

Confira o banco selecionado:

```javascript
db.getName()
```

Provavelmente será `test`. Isso não significa que você errou; ainda não selecionamos o banco do hotel.

**Checkpoint 3:** o comando `ping` retornou `ok: 1`?

---

# Parte 4 — Criando e conhecendo o banco do hotel

## Etapa 13. Selecionar o banco

**Dentro do mongosh:**

```javascript
use hotel_nosql
```

Confira:

```javascript
db.getName()
```

**Resultado esperado:** `hotel_nosql`.

No MongoDB, selecionar um banco com `use` não necessariamente cria imediatamente arquivos persistentes. O banco passa a existir efetivamente ao criar coleções ou gravar dados.

Veja os bancos disponíveis:

```javascript
show dbs
```

## Etapa 14. Criar uma coleção manualmente

Vamos criar a coleção `hospedes`:

```javascript
db.createCollection("hospedes")
```

Liste as coleções:

```javascript
show collections
```

A coleção deve aparecer na lista.

**Teoria:** uma coleção é análoga, de forma aproximada, a uma tabela. Entretanto, documentos de uma mesma coleção podem ter campos diferentes, desde que não haja regras de validação que restrinjam isso.

## Etapa 15. Inserir o primeiro hóspede

```javascript
db.hospedes.insertOne({
  _id: 1,
  nome: "Ana Martins",
  cidade: "Curitiba",
  estado: "PR",
  contato: {
    email: "ana@exemplo.com",
    telefone: "41999990001"
  },
  tags: ["frequente", "corporativo"]
})
```

**O que observar:** `insertOne()` insere um documento. O campo `_id` é o identificador único. Aqui usamos números para facilitar o estudo; o MongoDB também pode gerar identificadores `ObjectId` automaticamente.

Confira:

```javascript
db.hospedes.find()
```

**Resultado esperado:** o documento de Ana é retornado.

## Etapa 16. Inserir vários hóspedes

```javascript
db.hospedes.insertMany([
  {
    _id: 2,
    nome: "Bruno Lima",
    cidade: "Londrina",
    estado: "PR",
    contato: { email: "bruno@exemplo.com" },
    tags: ["lazer"]
  },
  {
    _id: 3,
    nome: "Carla Souza",
    cidade: "Curitiba",
    estado: "PR",
    contato: { email: "carla@exemplo.com" },
    tags: ["familia"]
  },
  {
    _id: 4,
    nome: "Diego Alves",
    cidade: "São Paulo",
    estado: "SP",
    contato: { email: "diego@exemplo.com" },
    tags: ["corporativo"]
  },
  {
    _id: 5,
    nome: "Elisa Rocha",
    cidade: "Maringá",
    estado: "PR",
    contato: { email: "elisa@exemplo.com" },
    tags: []
  },
  {
    _id: 6,
    nome: "Fábio Melo",
    cidade: "Curitiba",
    estado: "PR",
    contato: { email: "fabio@exemplo.com" },
    tags: ["novo"]
  }
])
```

Conte os documentos:

```javascript
db.hospedes.countDocuments({})
```

**Resultado esperado:** `6`.

### Atenção à execução duplicada

Como os `_id` são explícitos, reexecutar os `insertMany()` com os mesmos valores provoca erro de **chave duplicada**. Esse comportamento demonstra que `_id` é único na coleção. Não execute novamente a carga sem uma razão.

## Etapa 17. Criar a coleção de quartos

```javascript
db.quartos.insertMany([
  { _id: 101, numero: "101", tipo: "Standard", andar: 1,
    capacidade: 2, diaria: 180, status: "Disponível", amenidades: ["wifi", "tv"] },
  { _id: 102, numero: "102", tipo: "Standard", andar: 1,
    capacidade: 2, diaria: 180, status: "Ocupado", amenidades: ["wifi"] },
  { _id: 201, numero: "201", tipo: "Superior", andar: 2,
    capacidade: 3, diaria: 260, status: "Disponível", amenidades: ["wifi", "frigobar"] },
  { _id: 202, numero: "202", tipo: "Superior", andar: 2,
    capacidade: 3, diaria: 260, status: "Disponível", amenidades: ["wifi", "tv"] },
  { _id: 301, numero: "301", tipo: "Luxo", andar: 3,
    capacidade: 2, diaria: 420, status: "Disponível", amenidades: ["wifi", "tv"] },
  { _id: 401, numero: "401", tipo: "Família", andar: 4,
    capacidade: 5, diaria: 520, status: "Manutenção", amenidades: ["wifi", "cozinha"] }
])
```

Veja os registros:

```javascript
db.quartos.find()
db.quartos.countDocuments({})
```

**Resultado esperado:** `6` quartos.

> Note que o tipo de quarto, a capacidade e o preço estão dentro do próprio documento. Neste modelo de exemplo, não há uma coleção `tipo_quarto`. Em um sistema real, a decisão entre incorporar informações e utilizar referências depende das necessidades da aplicação.

## Etapa 18. Criar a coleção de reservas

```javascript
db.reservas.insertMany([
  { _id: 1001, hospedeId: 1, quartoId: 101,
    checkin: ISODate("2026-10-01T00:00:00Z"),
    checkout: ISODate("2026-10-03T00:00:00Z"),
    status: "Concluída", qtdHospedes: 2, valorTotal: 360,
    servicos: [{ nome: "cafe_da_manha", valor: 40 }] },
  { _id: 1002, hospedeId: 2, quartoId: 201,
    checkin: ISODate("2026-12-10T00:00:00Z"),
    checkout: ISODate("2026-12-12T00:00:00Z"),
    status: "Confirmada", qtdHospedes: 2, valorTotal: 520,
    servicos: [] },
  { _id: 1003, hospedeId: 1, quartoId: 301,
    checkin: ISODate("2026-12-20T00:00:00Z"),
    checkout: ISODate("2026-12-23T00:00:00Z"),
    status: "Confirmada", qtdHospedes: 2, valorTotal: 1260,
    servicos: [{ nome: "estacionamento", valor: 60 }] },
  { _id: 1004, hospedeId: 3, quartoId: 401,
    checkin: ISODate("2026-09-01T00:00:00Z"),
    checkout: ISODate("2026-09-04T00:00:00Z"),
    status: "Concluída", qtdHospedes: 4, valorTotal: 1560,
    servicos: [] },
  { _id: 1005, hospedeId: 5, quartoId: 102,
    checkin: ISODate("2026-12-15T00:00:00Z"),
    checkout: ISODate("2026-12-16T00:00:00Z"),
    status: "Cancelada", qtdHospedes: 1, valorTotal: 180,
    servicos: [] },
  { _id: 1006, hospedeId: 4, quartoId: 202,
    checkin: ISODate("2026-12-28T00:00:00Z"),
    checkout: ISODate("2026-12-30T00:00:00Z"),
    status: "Confirmada", qtdHospedes: 1, valorTotal: 520,
    servicos: [] }
])
```

Confira:

```javascript
db.reservas.countDocuments({})
show collections
```

**Resultado esperado:** `6` reservas e três coleções: `hospedes`, `quartos` e `reservas`.

**Importante:** neste exemplo, `hospedeId` e `quartoId` são referências convencionadas pela aplicação. **O MongoDB não cria automaticamente uma restrição de chave estrangeira** para esses campos, ao contrário de uma `FOREIGN KEY` no PostgreSQL.

**Checkpoint 4:** seu banco possui `6` hóspedes, `6` quartos e `6` reservas?

---

# Parte 5 — Consultando documentos

## Etapa 19. Consultar todos os documentos

No PostgreSQL você escreveria:

```sql
SELECT * FROM hospede;
```

No MongoDB:

```javascript
db.hospedes.find()
```

Para encontrar somente um:

```javascript
db.hospedes.findOne({ _id: 1 })
```

**Teoria:** `find()` devolve um cursor com resultados. `findOne()` devolve um documento correspondente ou `null` se não houver correspondência.

## Etapa 20. Filtrar por igualdade

No PostgreSQL:

```sql
SELECT * FROM hospede WHERE cidade = 'Curitiba';
```

No MongoDB:

```javascript
db.hospedes.find({ cidade: "Curitiba" })
```

**Resultado esperado:** Ana, Carla e Fábio (três hóspedes).

Agora faça outra consulta:

```javascript
db.quartos.find({ status: "Disponível" })
```

**Para refletir:** quais campos foram utilizados como filtros? O que significam as chaves `{}`?

## Etapa 21. Escolher as colunas que serão mostradas (projeção)

No SQL:

```sql
SELECT nome, cidade FROM hospede;
```

No MongoDB:

```javascript
db.hospedes.find({}, { nome: 1, cidade: 1, _id: 0 })
```

O primeiro documento `{}` indica ausência de filtro. O segundo define a **projeção**: `1` inclui campos e `_id: 0` oculta o identificador.

## Etapa 22. Consultar valores maiores ou menores

No SQL:

```sql
SELECT * FROM quarto WHERE diaria > 250;
```

No MongoDB:

```javascript
db.quartos.find({ diaria: { $gt: 250 } })
```

Outros operadores frequentes:

| Operador MongoDB | Significado | SQL aproximado |
|---|---|---|
| `$gt` | maior que | `>` |
| `$gte` | maior ou igual | `>=` |
| `$lt` | menor que | `<` |
| `$lte` | menor ou igual | `<=` |
| `$ne` | diferente | `<>` |
| `$in` | pertence a uma lista | `IN (...)` |

Teste:

```javascript
db.quartos.find({ diaria: { $gte: 260, $lte: 420 } })
```

**Resultado esperado:** quartos com diárias entre `260` e `420`, inclusive.

## Etapa 23. Combinar condições

As condições em um mesmo documento de filtro normalmente funcionam como um `AND`:

```javascript
db.quartos.find({ status: "Disponível", capacidade: { $gte: 3 } })
```

Para um `OR` explícito:

```javascript
db.quartos.find({
  $or: [
    { tipo: "Luxo" },
    { tipo: "Superior" }
  ]
})
```

**Para refletir:** um quarto `Standard` disponível satisfaria a segunda consulta? Por quê?

## Etapa 24. Ordenar e limitar

```javascript
db.quartos.find().sort({ diaria: -1 })
```

`-1` significa **decrescente**. `1` significa **crescente**.

Para obter somente os dois quartos mais caros:

```javascript
db.quartos.find().sort({ diaria: -1 }).limit(2)
```

No PostgreSQL, poderíamos usar `ORDER BY diaria DESC LIMIT 2`.

## Etapa 25. Consultar campos aninhados e arrays

Para consultar um campo dentro do objeto `contato`, utilize o **caminho pontilhado**:

```javascript
db.hospedes.find({ "contato.email": "ana@exemplo.com" })
```

Para documentos cujo array `tags` contém `corporativo`:

```javascript
db.hospedes.find({ tags: "corporativo" })
```

Para quartos que possuem `wifi` entre suas amenidades:

```javascript
db.quartos.find({ amenidades: "wifi" })
```

**Teoria:** no MongoDB, não é necessário desmembrar todas as informações em coleções diferentes. É possível consultar diretamente objetos aninhados e arrays.

---

# Parte 6 — Alterando e excluindo documentos

## Etapa 26. Inserir um hóspede de teste

Crie um documento novo, separado dos seis hóspedes iniciais:

```javascript
db.hospedes.insertOne({
  _id: 7,
  nome: "Gabriela Teste",
  cidade: "Apucarana",
  estado: "PR",
  contato: { email: "gabriela@exemplo.com" },
  tags: ["novo"]
})
```

Confirme:

```javascript
db.hospedes.findOne({ _id: 7 })
```

## Etapa 27. Modificar um campo com `$set`

No PostgreSQL:

```sql
UPDATE hospede SET cidade = 'Curitiba' WHERE id_hospede = 7;
```

No MongoDB:

```javascript
db.hospedes.updateOne(
  { _id: 7 },
  { $set: { cidade: "Curitiba" } }
)
```

Consulte novamente:

```javascript
db.hospedes.findOne({ _id: 7 })
```

**Resultado esperado:** o campo `cidade` foi alterado para `Curitiba`.

## Etapa 28. Adicionar um campo novo

```javascript
db.hospedes.updateOne(
  { _id: 7 },
  { $set: { "contato.telefone": "43999990007" } }
)
```

Observe que foi incluído `contato.telefone`, mesmo que o documento original não tivesse esse campo. **Documentos da mesma coleção não precisam ter exatamente a mesma estrutura**, salvo se houver validações configuradas.

## Etapa 29. Adicionar um elemento a um array

```javascript
db.hospedes.updateOne(
  { _id: 7 },
  { $push: { tags: "corporativo" } }
)
```

Confira:

```javascript
db.hospedes.findOne({ _id: 7 })
```

Agora `tags` deve conter `novo` e `corporativo`.

**Diferença:** `$set` atribui ou substitui valores; `$push` adiciona um elemento ao fim de um array.

## Etapa 30. Incrementar um valor numérico

```javascript
db.quartos.updateOne(
  { _id: 301 },
  { $inc: { diaria: 10 } }
)
```

Confira:

```javascript
db.quartos.findOne({ _id: 301 })
```

**Resultado esperado:** a diária do quarto `301` passa de `420` para `430`. O operador `$inc` soma o valor indicado ao número atual.

Para restaurar o valor original:

```javascript
db.quartos.updateOne({ _id: 301 }, { $set: { diaria: 420 } })
```

## Etapa 31. Remover um campo com `$unset`

```javascript
db.hospedes.updateOne(
  { _id: 7 },
  { $unset: { "contato.telefone": "" } }
)
```

Confira:

```javascript
db.hospedes.findOne({ _id: 7 })
```

O campo `telefone` deixa de fazer parte do documento.

## Etapa 32. Excluir o hóspede de teste

```javascript
db.hospedes.deleteOne({ _id: 7 })
```

Confirme:

```javascript
db.hospedes.findOne({ _id: 7 })
db.hospedes.countDocuments({})
```

**Resultado esperado:** `findOne()` retorna `null` e a coleção volta a ter `6` hóspedes.

> **Cuidado:** não utilize `deleteMany({})` neste laboratório: um filtro vazio excluiria todos os documentos de uma coleção.

**Checkpoint 5:** você conseguiu criar, consultar, atualizar e excluir um documento de teste?

---

# Parte 7 — Consultas semelhantes a relatórios SQL

## Etapa 33. Contar documentos

Quantos quartos estão disponíveis?

```javascript
db.quartos.countDocuments({ status: "Disponível" })
```

Quantas reservas estão confirmadas?

```javascript
db.reservas.countDocuments({ status: "Confirmada" })
```

**Resultado esperado no banco original:** `4` quartos disponíveis e `3` reservas confirmadas.

## Etapa 34. Agrupar por status de reserva

Em SQL, você já utilizou `GROUP BY`. No MongoDB podemos trabalhar com um **pipeline de agregação**:

```javascript
db.reservas.aggregate([
  {
    $group: {
      _id: "$status",
      quantidade: { $sum: 1 },
      valorTotal: { $sum: "$valorTotal" }
    }
  },
  { $sort: { quantidade: -1 } }
])
```

**Teoria:** em `$group`, `_id` representa a chave de agrupamento, não o `_id` dos documentos originais. `$sum: 1` conta documentos e `$sum: "$valorTotal"` soma os valores da coluna/campo informado.

## Etapa 35. Filtrar antes de agrupar

```javascript
db.reservas.aggregate([
  { $match: { status: "Confirmada" } },
  {
    $group: {
      _id: "$quartoId",
      quantidade: { $sum: 1 },
      faturamento: { $sum: "$valorTotal" }
    }
  },
  { $sort: { faturamento: -1 } }
])
```

`$match` filtra documentos e `$group` realiza os cálculos. A ordem das etapas altera o resultado.

## Etapa 36. Consultar dados de duas coleções com `$lookup`

Embora MongoDB incentive modelagem orientada aos acessos por documentos, também é possível relacionar coleções em consultas.

```javascript
db.reservas.aggregate([
  {
    $lookup: {
      from: "hospedes",
      localField: "hospedeId",
      foreignField: "_id",
      as: "dadosHospede"
    }
  },
  { $unwind: "$dadosHospede" },
  {
    $project: {
      _id: 0,
      reserva: "$_id",
      hospede: "$dadosHospede.nome",
      status: 1,
      valorTotal: 1
    }
  }
])
```

O `$lookup` é parecido, em finalidade, com um `JOIN`. O resultado associado aparece inicialmente em um array. `$unwind` permite trabalhar com cada elemento do array individualmente.

**Para refletir:** por que usar `$lookup` pode ser útil? E quando seria mais simples armazenar alguns dados do hóspede dentro do próprio documento da reserva?

## Etapa 37. Criar e inspecionar um índice

```javascript
db.hospedes.createIndex({ "contato.email": 1 }, { unique: true })
```

Liste os índices:

```javascript
db.hospedes.getIndexes()
```

Explique: um índice pode melhorar determinados filtros. `unique: true` também impõe unicidade aos valores indexados, conforme as regras do índice.

Analise a consulta:

```javascript
db.hospedes.find({ "contato.email": "ana@exemplo.com" })
  .explain("executionStats")
```

Procure informações como `IXSCAN` ou `COLLSCAN` no plano. **Com somente seis registros, não se pode concluir que o índice sempre será utilizado ou que será mais rápido**; o objetivo aqui é conhecer as ferramentas de inspeção.

---

# Parte 8 — Persistência, encerramento e reinício

## Etapa 38. Sair do mongosh

**Dentro do mongosh:**

```javascript
exit
```

Você retornará ao terminal Ubuntu.

## Etapa 39. Interromper os serviços

**Terminal Ubuntu, na pasta do projeto:**

```bash
sudo docker compose -f docker-compose-hotel-nosql.yml down
```

Esse comando para e remove o contêiner do projeto, **mas mantém o volume nomeado**.

Confira:

```bash
sudo docker volume ls
```

## Etapa 40. Iniciar novamente

```bash
sudo docker compose -f docker-compose-hotel-nosql.yml up -d
```

Entre no banco novamente:

```bash
sudo docker compose -f docker-compose-hotel-nosql.yml exec mongo \
  mongosh --username admin_aula --authenticationDatabase admin
```

Digite a senha e execute **dentro do mongosh**:

```javascript
use hotel_nosql
db.hospedes.countDocuments({})
db.quartos.countDocuments({})
db.reservas.countDocuments({})
```

**Resultado esperado:** `6`, `6` e `6`.

### Por que os dados não desapareceram?

Porque o Docker Compose configurou o volume:

```yaml
volumes:
  - mongo_hotel_dados:/data/db
```

**Atenção:** `docker compose down -v` também remove os volumes gerenciados pelo projeto e pode apagar os dados do laboratório. **Não utilize `-v` durante a atividade.**

**Checkpoint 6:** depois do reinício, os três conjuntos de documentos continuam disponíveis?

---

# Parte 9 — Exercícios para fazer sem copiar a resolução

Faça as consultas abaixo **sozinho**. Para cada questão, registre o comando e o resultado. Utilize o banco que acabou de construir.

**Questão 1.** Liste apenas o nome e a cidade de todos os hóspedes, sem mostrar `_id`.

**Questão 2.** Liste todos os quartos com diária maior que `250`, ordenados do mais barato para o mais caro.

**Questão 3.** Mostre somente os quartos que possuem a amenidade `wifi` e capacidade para pelo menos três pessoas.

**Questão 4.** Localize hóspedes de Curitiba ou de Maringá, utilizando `$in`.

**Questão 5.** Liste reservas com status `Confirmada` e valor total superior a `500`.

**Questão 6.** Localize todas as reservas do hóspede com `_id: 1`.

**Questão 7.** Crie um documento de hóspede com `_id: 8`, incluindo nome, cidade, contato e duas tags. Consulte-o e, depois, altere sua cidade.

**Questão 8.** Acrescente a tag `vip` ao hóspede de `_id: 8` sem substituir as tags anteriores.

**Questão 9.** Remova o hóspede de `_id: 8`, verificando antes e depois da exclusão.

**Questão 10.** Produza um relatório com a quantidade de reservas por status utilizando `aggregate()` e `$group`.

**Questão 11.** Produza uma consulta que mostre o identificador da reserva e o nome do hóspede correspondente utilizando `$lookup`.

**Questão 12.** Explique, em um parágrafo, as diferenças entre uma tabela PostgreSQL e uma coleção MongoDB, incluindo como representar campos opcionais, arrays e relacionamentos.

### Registro da atividade

Entregue um arquivo `.md` ou `.pdf` contendo os comandos das questões 1 a 11, resultados obtidos e a resposta da questão 12. Inclua também um registro de `docker compose ps` mostrando o contêiner executado com sucesso. Não divulgue senhas no material entregue.

---

# Parte 10 — Solução de problemas comuns

## O comando `docker` não existe

O Docker não foi instalado corretamente ou o terminal ainda não reconhece o programa. Volte às Etapas 4–8 e confira os pacotes.

## `permission denied while trying to connect to the Docker daemon socket`

Execute os comandos Docker com `sudo` como demonstrado no roteiro. A inclusão de um usuário no grupo `docker` deve ser feita somente por quem administra a máquina, pois concede acesso privilegiado.

## `Cannot connect to the Docker daemon`

Verifique:

```bash
sudo systemctl status docker
```

Se necessário:

```bash
sudo systemctl start docker
```

## `port is already allocated` ou `address already in use`

Outro processo pode estar usando a porta `27017`. No arquivo YAML, altere apenas a porta do computador:

```yaml
ports:
  - "127.0.0.1:27018:27017"
```

Depois recrie o serviço:

```bash
sudo docker compose -f docker-compose-hotel-nosql.yml up -d
```

O acesso ao `mongosh` **dentro do contêiner** continua igual.

## `Authentication failed`

Confira usuário, senha e `--authenticationDatabase admin`. Se você já tinha iniciado esse volume antes, a mudança da variável de senha no YAML não altera automaticamente a senha armazenada no banco. Não apague o volume sem avaliar a perda de dados.

## `E11000 duplicate key error`

Você tentou inserir um documento com `_id` já utilizado (ou outro campo protegido por índice único). Consulte primeiro:

```javascript
db.hospedes.find({ _id: 1 })
```

Escolha outro identificador para um documento novo; não repita a carga inicial.

## `show dbs` não apresenta `hotel_nosql`

Confira se você criou uma coleção ou inseriu documentos, e se está conectado ao mesmo servidor. A instrução `use` sozinha não garante que haverá um banco com dados a listar.

## `mongosh: command not found` no Ubuntu

Você não precisa instalar o `mongosh` no computador. Execute o cliente dentro do contêiner usando:

```bash
sudo docker compose -f docker-compose-hotel-nosql.yml exec mongo \
  mongosh --username admin_aula --authenticationDatabase admin
```

## Quero parar sem perder meus dados

```bash
sudo docker compose -f docker-compose-hotel-nosql.yml down
```

Não acrescente `-v`.

---

# Resumo de comandos

| Objetivo | Comando |
|---|---|
| Verificar Docker | `sudo docker --version` |
| Verificar Compose | `sudo docker compose version` |
| Subir MongoDB | `sudo docker compose -f docker-compose-hotel-nosql.yml up -d` |
| Ver contêiner | `sudo docker compose -f docker-compose-hotel-nosql.yml ps` |
| Parar sem apagar dados | `sudo docker compose -f docker-compose-hotel-nosql.yml down` |
| Selecionar banco | `use hotel_nosql` |
| Listar coleções | `show collections` |
| Inserir um documento | `db.hospedes.insertOne({...})` |
| Consultar | `db.hospedes.find({...})` |
| Atualizar | `db.hospedes.updateOne(filtro, {$set: {...}})` |
| Excluir um documento | `db.hospedes.deleteOne(filtro)` |
| Agrupar | `db.reservas.aggregate([...])` |
| Criar índice | `db.hospedes.createIndex({campo: 1})` |
| Sair do mongosh | `exit` |


## Referências oficiais para consulta

- Docker Engine no Ubuntu: https://docs.docker.com/engine/install/ubuntu/
- Docker Compose no Linux: https://docs.docker.com/compose/install/linux/
- Imagem oficial `mongo` no Docker Hub: https://hub.docker.com/_/mongo
- MongoDB Shell (`mongosh`): https://www.mongodb.com/docs/mongodb-shell/
- Métodos de consulta: https://www.mongodb.com/docs/manual/reference/method/db.collection.find/
- Métodos de atualização: https://www.mongodb.com/docs/manual/reference/method/db.collection.updateOne/
