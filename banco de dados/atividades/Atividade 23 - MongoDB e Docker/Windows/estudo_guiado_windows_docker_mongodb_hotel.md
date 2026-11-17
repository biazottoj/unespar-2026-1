# Estudo guiado — MongoDB com Docker no Windows

**Disciplina:** Banco de Dados  
**Tema:** Introdução a bancos NoSQL orientados a documentos  
**Ambiente:** Windows 10/11 compatível, Docker Desktop, WSL 2, PowerShell e MongoDB 8.0  
**Cenário:** Sistema de reservas de hotel  
**Modalidade:** Estudo individual com comandos, teoria, verificações e exercícios

> **Objetivo geral:** ao concluir o estudo, você deverá conseguir instalar e utilizar o Docker Desktop, executar o MongoDB em um contêiner, criar e consultar documentos, atualizar e excluir dados, realizar agregações e preservar o banco entre reinicializações.
>
> **Importante:** este material é para um **laboratório local**. A senha apresentada é somente didática. Não reutilize essa configuração em produção e não publique senhas em trabalhos ou repositórios.

## Antes de começar: onde cada comando deve ser executado?

Ao longo do material você encontrará dois tipos de blocos:

- **PowerShell:** comandos do Windows, como `docker compose up -d`, `wsl --status` e `docker cp`.
- **MongoDB (`mongosh`):** comandos JavaScript de banco de dados, como `db.hospedes.find()` e `db.reservas.aggregate()`.

**Não execute comandos `mongosh` no PowerShell e nem comandos `docker` dentro do `mongosh`.** Você saberá que entrou no `mongosh` quando o prompt mudar para algo parecido com `test>` ou `hotel_nosql>`.

### Arquivos fornecidos com a aula

O pacote da atividade contém três arquivos:

| Arquivo | Finalidade |
|---|---|
| `estudo_guiado_windows_docker_mongodb_hotel.md` | Instruções, explicações e exercícios |
| `docker-compose-hotel-nosql.yml` | Define o contêiner MongoDB |
| `carga_inicial_hotel_nosql_recriada.js` | Insere os dados fictícios do hotel |

Você também poderá criar o `.yml` manualmente, seguindo a etapa correspondente.

---

# Parte 1 — Introdução ao NoSQL

## Etapa 1. O que significa NoSQL?

Na disciplina você já trabalhou com o **PostgreSQL**, um banco relacional. Nele, os dados normalmente estão organizados em tabelas, com linhas, colunas, chaves primárias e chaves estrangeiras.

**NoSQL** é um termo usado para uma família de bancos que não se restringe ao modelo relacional. Existem bancos orientados a documentos, chave-valor, grafos e outras abordagens. Neste laboratório usaremos o **MongoDB**, um banco **orientado a documentos**.

Comparação aproximada:

| PostgreSQL | MongoDB | Significado |
|---|---|---|
| Banco de dados | Database | Conjunto de informações de uma aplicação |
| Tabela | Collection | Conjunto de registros/documentos |
| Linha | Document | Registro armazenado |
| Coluna | Field | Propriedade de um registro |
| Chave primária | `_id` | Identificador único do documento |
| `SELECT` | `find()` | Consultar |
| `INSERT` | `insertOne()` / `insertMany()` | Inserir |
| `UPDATE` | `updateOne()` / `updateMany()` | Atualizar |
| `DELETE` | `deleteOne()` / `deleteMany()` | Excluir |

Considere um hóspede representado como documento:

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

Perceba que `contato` é um **objeto aninhado** e `tags` é um **array**. Documentos MongoDB usam o formato **BSON**, que é semelhante ao JSON, mas suporta tipos adicionais, como datas.

**Para refletir:** no modelo relacional, como poderíamos representar várias tags de um hóspede? No MongoDB, como elas aparecem no documento?

## Etapa 2. Por que utilizar Docker?

O Docker permite executar aplicações em **contêineres**, sem instalar diretamente todas as suas dependências no sistema hospedeiro.

Neste estudo:

```text
Seu computador com Windows
│
├── Docker Desktop
│   └── Ambiente Linux via WSL 2
│       └── Contêiner mongo_hotel_aula
│           ├── Servidor MongoDB
│           └── Cliente mongosh
│
└── Volume Docker: mongo_hotel_dados
    └── Dados persistidos do MongoDB
```

**Imagem** é a base usada para criar o contêiner; **contêiner** é a instância em execução; **Docker Compose** descreve os serviços em um arquivo YAML; e **volume** mantém os dados além do ciclo de vida do contêiner.

---

# Parte 2 — Preparação do Windows

## Etapa 3. Conferir o Windows e a virtualização

Abra o **PowerShell**: pressione a tecla Windows, procure por **PowerShell** e abra o programa.

Execute:

```powershell
winver
```

Confira a versão do Windows. Docker Desktop requer versões compatíveis do Windows 10 ou 11; consulte os requisitos atuais na documentação oficial ao final do material.

Verifique se a virtualização está disponível:

1. Abra o **Gerenciador de Tarefas** (`Ctrl + Shift + Esc`).
2. Acesse **Desempenho → CPU**.
3. Localize a indicação **Virtualização**.

Ela deve estar **Habilitada**. Em computadores de laboratório, mudanças de BIOS/UEFI podem depender da equipe de TI. Não altere configurações de firmware sem orientação.

## Etapa 4. Verificar o WSL 2

**WSL (Windows Subsystem for Linux)** permite executar componentes Linux no Windows. O Docker Desktop pode utilizá-lo como mecanismo de execução de contêineres Linux.

No **PowerShell**:

```powershell
wsl --status
```

E, se desejar consultar distribuições instaladas:

```powershell
wsl --list --verbose
```

Se o WSL não estiver instalado, abra **PowerShell como Administrador** e execute:

```powershell
wsl --install
```

Reinicie o computador caso seja solicitado. Depois, execute:

```powershell
wsl --update
wsl --status
```

> **Observação:** não é necessário instalar manualmente o MongoDB ou executar o estudo dentro de uma distribuição Ubuntu. Os comandos a seguir serão executados no **PowerShell do Windows**; o Docker Desktop utilizará o mecanismo Linux configurado.

**Verificação 1:** o WSL foi instalado/atualizado com sucesso? Se o computador não permite ativá-lo, consulte o professor ou a equipe responsável.

## Etapa 5. Instalar o Docker Desktop

Abra a página oficial:

**https://docs.docker.com/desktop/setup/install/windows-install/**

Baixe o instalador adequado ao computador e siga as instruções. Na configuração, escolha a opção de usar o **WSL 2** como mecanismo de execução dos contêineres Linux, quando apresentada.

Se preferir instalar pelo gerenciador de pacotes do Windows e ele estiver disponível, uma alternativa é, no PowerShell:

```powershell
winget install -e --id Docker.DockerDesktop
```

**Basta utilizar um dos métodos de instalação**, não os dois.

Após a instalação:

1. Reinicie o Windows, se solicitado.
2. Abra **Docker Desktop** no menu Iniciar.
3. Conclua as telas iniciais necessárias.
4. Aguarde a indicação de que o mecanismo Docker está em execução.
5. Confirme que está utilizando **Linux containers**, não Windows containers.

> Se você já tem Docker Desktop funcionando, não precisa reinstalá-lo. Vá para a etapa seguinte.

## Etapa 6. Testar a instalação

Abra **um novo PowerShell normal** (não precisa ser administrador) e execute:

```powershell
docker --version
docker compose version
```

Em seguida:

```powershell
docker run --rm hello-world
```

**Resultado esperado:** o Docker baixa (se necessário) e executa uma imagem de teste que informa que a instalação está funcionando.

Se `docker` não for reconhecido, feche e reabra o PowerShell; verifique também se o Docker Desktop foi instalado e iniciado.

Se surgir `Cannot connect to the Docker daemon`, abra o Docker Desktop e aguarde o mecanismo iniciar.

**Verificação 2:** o comando `hello-world` funcionou? Somente avance se a resposta for positiva.

---

# Parte 3 — Subindo o MongoDB com Docker Compose

## Etapa 7. Criar a pasta de trabalho

No **PowerShell**:

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\aula-nosql-hotel"
Set-Location "$HOME\aula-nosql-hotel"
Get-Location
```

Todos os arquivos deste laboratório devem ficar nessa pasta. Você pode abri-la no Explorador de Arquivos digitando:

```powershell
explorer .
```

## Etapa 8. Preparar o arquivo Compose

Copie o arquivo `docker-compose-hotel-nosql.yml` fornecido com a aula para a pasta `aula-nosql-hotel`.

Se não tiver o arquivo, crie-o:

```powershell
notepad .\docker-compose-hotel-nosql.yml
```

Se o Bloco de Notas perguntar se deseja criar o arquivo, confirme e cole o conteúdo abaixo:

```yaml
# Ambiente didático local. A senha é apenas de demonstração.
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

Salve e feche o arquivo. **A extensão deve ser `.yml`, não `.yml.txt`.** No Explorador, habilite a exibição de extensões de nomes de arquivos para conferir.

No PowerShell, verifique:

```powershell
Get-ChildItem
Get-Content .\docker-compose-hotel-nosql.yml
```

E valide a estrutura do Compose:

```powershell
docker compose -f .\docker-compose-hotel-nosql.yml config
```

### O que significa cada parte?

- `image: mongo:8.0`: seleciona a imagem MongoDB 8.0.
- `container_name`: nome que utilizaremos nos comandos.
- `127.0.0.1:27017:27017`: publica a porta no **próprio computador**, sem expô-la deliberadamente à rede externa.
- `MONGO_INITDB_ROOT_USERNAME` e `MONGO_INITDB_ROOT_PASSWORD`: criam uma conta administrativa **na primeira inicialização com dados vazios**.
- `mongo_hotel_dados:/data/db`: usa um volume para persistir os arquivos do banco.

A configuração não cria ainda as coleções `hospedes`, `quartos` e `reservas`; isso será feito posteriormente.

## Etapa 9. Iniciar o MongoDB

No PowerShell, dentro da pasta do projeto:

```powershell
docker compose -f .\docker-compose-hotel-nosql.yml up -d
```

Na primeira vez, o Docker deverá baixar a imagem. Verifique o contêiner:

```powershell
docker compose -f .\docker-compose-hotel-nosql.yml ps
```

**Resultado esperado:** o serviço `mongo` está em execução (`Up` / `running`).

Você também pode visualizar as mensagens recentes:

```powershell
docker compose -f .\docker-compose-hotel-nosql.yml logs --tail=30 mongo
```

**Verificação 3:** você consegue visualizar `mongo_hotel_aula` em execução no Docker Desktop ou no terminal?

## Etapa 10. Entrar no MongoDB

**Ainda no PowerShell:**

```powershell
docker compose -f .\docker-compose-hotel-nosql.yml exec mongo mongosh --username admin_aula --authenticationDatabase admin
```

Quando solicitar a senha, digite:

```text
AulaNoSQL_2026_Trocar
```

Os caracteres digitados podem ficar invisíveis. Não é necessário instalar o `mongosh` separadamente no Windows: ele será executado dentro do contêiner.

Agora você está no **mongosh**. Teste:

```javascript
db.runCommand({ ping: 1 })
```

**Resultado esperado:** uma resposta contendo `ok: 1`.

Veja o nome do banco selecionado:

```javascript
db.getName()
```

Ele pode ser `test`. Na próxima parte vamos selecionar o banco da atividade.

**Verificação 4:** `ping` retornou `ok: 1`?

---

# Parte 4 — Criando e populando o banco do hotel

## Etapa 11. Selecionar o banco

**Dentro do mongosh:**

```javascript
use hotel_nosql
```

Confira:

```javascript
db.getName()
```

O nome deverá ser `hotel_nosql`.

O comando `use` seleciona um banco; ele passa a aparecer como banco persistente quando forem criados objetos/dados.

## Etapa 12. Entender as coleções

Usaremos três coleções:

```text
hotel_nosql
├── hospedes
│   ├── _id, nome, cidade, estado
│   ├── contato: { email, telefone? }
│   └── tags: [ ... ]
├── quartos
│   ├── _id, numero, tipo, andar
│   ├── capacidade, diaria, status
│   └── amenidades: [ ... ]
└── reservas
    ├── _id, hospedeId, quartoId
    ├── checkin, checkout, status
    ├── qtdHospedes, valorTotal
    └── servicos: [ { nome, valor }, ... ]
```

No banco relacional, `hospedeId` e `quartoId` seriam candidatos a chaves estrangeiras. Neste exemplo, são referências armazenadas como campos dos documentos: **o MongoDB não cria automaticamente uma restrição equivalente à `FOREIGN KEY` do PostgreSQL**.

## Etapa 13. Carregar os dados com um arquivo JavaScript

**Primeiro saia do mongosh:**

```javascript
exit
```

Agora, no **PowerShell**, copie o arquivo `carga_inicial_hotel_nosql_recriada.js` (fornecido com a aula) para a pasta `aula-nosql-hotel`.

Se ele estiver na pasta Downloads, por exemplo:

```powershell
Copy-Item "$HOME\Downloads\carga_inicial_hotel_nosql_recriada.js" .
```

> Se o navegador salvou o arquivo em outra pasta, localize-o no Explorador e copie-o para `aula-nosql-hotel`. Confirme que a extensão é `.js`, e não `.js.txt`.

Verifique a presença do arquivo:

```powershell
Get-ChildItem
```

Copie o script para o contêiner:

```powershell
docker cp .\carga_inicial_hotel_nosql_recriada.js mongo_hotel_aula:/tmp/carga_inicial_hotel_nosql_recriada.js
```

Entre novamente no MongoDB:

```powershell
docker compose -f .\docker-compose-hotel-nosql.yml exec mongo mongosh --username admin_aula --authenticationDatabase admin
```

Digite a senha quando solicitada. **Dentro do mongosh**, execute:

```javascript
load("/tmp/carga_inicial_hotel_nosql_recriada.js")
```

O script insere os dados do hotel. Ele foi preparado para ser **reexecutável**, criando os documentos de exemplo ausentes sem duplicar `_id` nem sobrescrever registros que já foram modificados.

Em um banco vazio, o resultado esperado é:

```text
Total de hóspedes: 6
Total de quartos: 6
Total de reservas: 6
```

Selecione o banco e confira:

```javascript
use hotel_nosql
show collections

db.hospedes.countDocuments({})
db.quartos.countDocuments({})
db.reservas.countDocuments({})
```

O resultado inicial é `6`, `6` e `6`. Se você já realizou exercícios ou inseriu outros documentos, os totais poderão ser maiores.

**Verificação 5:** as coleções `hospedes`, `quartos` e `reservas` existem e contêm dados?

---

# Parte 5 — Consultando documentos (`find`)

## Etapa 14. Ler documentos

No PostgreSQL:

```sql
SELECT * FROM hospede;
```

No **mongosh**:

```javascript
db.hospedes.find()
```

Para obter apenas um documento:

```javascript
db.hospedes.findOne({ _id: 1 })
```

**Teoria:** `find()` retorna um *cursor* de resultados, enquanto `findOne()` retorna um documento ou `null`.

## Etapa 15. Filtrar por igualdade

```javascript
db.hospedes.find({ cidade: "Curitiba" })
```

**Resultado esperado:** Ana, Carla e Fábio.

Agora filtre quartos:

```javascript
db.quartos.find({ status: "Disponível" })
```

**Resultado esperado:** quartos `101`, `201`, `202` e `301`, caso ninguém tenha modificado a carga inicial.

No MongoDB, `{ cidade: "Curitiba" }` é um documento que descreve a condição de busca.

## Etapa 16. Selecionar somente alguns campos (projeção)

No SQL, você pode escrever:

```sql
SELECT nome, cidade FROM hospede;
```

No MongoDB:

```javascript
db.hospedes.find({}, { nome: 1, cidade: 1, _id: 0 })
```

O primeiro `{}` significa **sem filtro**. O segundo define quais campos serão exibidos. Normalmente, `1` inclui um campo e `_id: 0` remove o identificador da saída.

## Etapa 17. Comparar valores

```javascript
db.quartos.find({ diaria: { $gt: 250 } })
```

O operador `$gt` significa **maior que**.

| Operador | Significado | SQL aproximado |
|---|---|---|
| `$gt` | Maior que | `>` |
| `$gte` | Maior ou igual | `>=` |
| `$lt` | Menor que | `<` |
| `$lte` | Menor ou igual | `<=` |
| `$ne` | Diferente | `<>` |
| `$in` | Pertence a uma lista | `IN (...)` |

Teste um intervalo:

```javascript
db.quartos.find({ diaria: { $gte: 260, $lte: 420 } })
```

## Etapa 18. Combinar condições

Duas condições no mesmo objeto funcionam, normalmente, como um `AND`:

```javascript
db.quartos.find({ status: "Disponível", capacidade: { $gte: 3 } })
```

Para um `OR`:

```javascript
db.quartos.find({
  $or: [
    { tipo: "Luxo" },
    { tipo: "Superior" }
  ]
})
```

## Etapa 19. Ordenar e limitar

```javascript
db.quartos.find().sort({ diaria: -1 })
```

`-1` representa ordem decrescente; `1` representa crescente.

```javascript
db.quartos.find().sort({ diaria: -1 }).limit(2)
```

Retorna os dois quartos mais caros, segundo o campo `diaria`.

## Etapa 20. Campos aninhados e arrays

Para consultar o email de um hóspede:

```javascript
db.hospedes.find({ "contato.email": "ana@exemplo.com" })
```

Para encontrar hóspedes com a tag `corporativo`:

```javascript
db.hospedes.find({ tags: "corporativo" })
```

Para encontrar quartos com `wifi`:

```javascript
db.quartos.find({ amenidades: "wifi" })
```

**Teoria:** a notação com ponto permite acessar campos aninhados; consultar um array por valor permite encontrar documentos cujo array contenha o elemento desejado.

**Verificação 6:** você conseguiu buscar por cidade, por intervalo de diária e por um elemento do array?

---

# Parte 6 — Inserir, atualizar e excluir (`CRUD`)

## Etapa 21. Inserir um novo hóspede

Dentro do **mongosh**:

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

Confira:

```javascript
db.hospedes.findOne({ _id: 7 })
```

**Teoria:** `insertOne()` adiciona um documento. O campo `_id` é único; tentar inserir outro documento com o mesmo `_id` gera erro.

## Etapa 22. Atualizar um valor com `$set`

```javascript
db.hospedes.updateOne(
  { _id: 7 },
  { $set: { cidade: "Curitiba" } }
)
```

Confira:

```javascript
db.hospedes.findOne({ _id: 7 })
```

`$set` altera ou cria o campo informado sem substituir o documento completo.

## Etapa 23. Criar um campo aninhado

```javascript
db.hospedes.updateOne(
  { _id: 7 },
  { $set: { "contato.telefone": "43999990007" } }
)
```

Observe que o documento agora possui o campo `contato.telefone`, mesmo que ele não estivesse presente na inserção original.

## Etapa 24. Adicionar uma tag com `$push`

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

**Teoria:** `$push` acrescenta um valor ao final de um array. É diferente de `$set`, que poderia substituir o array inteiro.

## Etapa 25. Incrementar um número com `$inc`

```javascript
db.quartos.updateOne(
  { _id: 301 },
  { $inc: { diaria: 10 } }
)
```

A diária do quarto `301` deve passar de `420` para `430`.

Verifique:

```javascript
db.quartos.findOne({ _id: 301 })
```

E restaure o valor original para manter os exemplos:

```javascript
db.quartos.updateOne({ _id: 301 }, { $set: { diaria: 420 } })
```

## Etapa 26. Remover um campo com `$unset`

```javascript
db.hospedes.updateOne(
  { _id: 7 },
  { $unset: { "contato.telefone": "" } }
)
```

O campo `telefone` será removido do documento.

## Etapa 27. Excluir o hóspede de teste

```javascript
db.hospedes.deleteOne({ _id: 7 })
```

Confira:

```javascript
db.hospedes.findOne({ _id: 7 })
db.hospedes.countDocuments({})
```

**Resultado esperado:** `findOne()` retorna `null` e a coleção volta a ter `6` hóspedes, se não houve outras inserções.

> **Cuidado:** `deleteMany({})` remove **todos** os documentos da coleção. Não execute esse comando neste laboratório.

**Verificação 7:** você consegue explicar a diferença entre `$set`, `$push`, `$inc` e `$unset`?

---

# Parte 7 — Relatórios, agregações e índices

## Etapa 28. Contar documentos

```javascript
db.quartos.countDocuments({ status: "Disponível" })
db.reservas.countDocuments({ status: "Confirmada" })
```

Nos dados iniciais, o resultado esperado é `4` quartos disponíveis e `3` reservas confirmadas.

## Etapa 29. Agrupar reservas por status

No PostgreSQL, você estudou `GROUP BY`. No MongoDB, podemos utilizar um **pipeline de agregação**:

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

**Teoria:** `$group` define a chave de agrupamento em `_id`; `$sum: 1` conta documentos; `$sum: "$valorTotal"` soma o valor dos registros. O `$sort` organiza a saída.

## Etapa 30. Filtrar antes de agrupar

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

`$match` filtra e `$group` agrega. **A ordem das etapas pode alterar o resultado.**

## Etapa 31. Relacionar coleções com `$lookup`

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

**Teoria:** `$lookup` é semelhante, na finalidade, a um `JOIN`: procura documentos correspondentes em outra coleção. Inicialmente, o resultado do relacionamento aparece como um array. O `$unwind` permite tratar os itens separadamente e o `$project` seleciona os campos de saída.

## Etapa 32. Criar e inspecionar um índice

```javascript
db.hospedes.createIndex({ "contato.email": 1 }, { unique: true })
```

Liste os índices:

```javascript
db.hospedes.getIndexes()
```

Analise uma consulta:

```javascript
db.hospedes.find({ "contato.email": "ana@exemplo.com" })
  .explain("executionStats")
```

Procure indicadores como `IXSCAN` e `COLLSCAN`. **Com seis documentos, o MongoDB pode considerar uma leitura completa bastante eficiente**, portanto não é esperado demonstrar grandes ganhos de tempo nesse exemplo.

**Verificação 8:** você compreendeu como `$group`, `$lookup` e índices correspondem a conceitos já estudados no PostgreSQL?

---

# Parte 8 — Persistência dos dados no Windows

## Etapa 33. Sair do mongosh

Dentro do `mongosh`:

```javascript
exit
```

Você retornará ao **PowerShell**.

## Etapa 34. Parar e remover o contêiner sem apagar dados

Na pasta do laboratório:

```powershell
docker compose -f .\docker-compose-hotel-nosql.yml down
```

Esse comando remove o contêiner, mas **mantém o volume nomeado** com os dados.

Confira os volumes:

```powershell
docker volume ls
```

O nome efetivo do volume pode conter um prefixo derivado da pasta/projeto do Compose.

## Etapa 35. Iniciar novamente

```powershell
docker compose -f .\docker-compose-hotel-nosql.yml up -d
```

Entre no banco:

```powershell
docker compose -f .\docker-compose-hotel-nosql.yml exec mongo mongosh --username admin_aula --authenticationDatabase admin
```

Dentro do `mongosh`:

```javascript
use hotel_nosql

db.hospedes.countDocuments({})
db.quartos.countDocuments({})
db.reservas.countDocuments({})
```

**Resultado esperado:** os dados continuam presentes, pois estão armazenados no volume Docker.

> **Nunca use `docker compose down -v` durante a atividade.** A opção `-v` remove volumes do projeto e pode apagar os dados. Alterar a senha no arquivo YAML também **não muda automaticamente** a senha de um MongoDB já inicializado com um volume existente.

**Verificação 9:** os registros permaneceram depois de remover e recriar o contêiner?

---

# Parte 9 — Atividade para os alunos

Resolva as questões a seguir **sem copiar os comandos dos exemplos**. Para cada questão prática, registre o comando que executou e uma breve descrição do resultado. Utilize o banco `hotel_nosql` com os dados do script fornecido.

**Questão 1.** Consulte somente `nome` e `cidade` dos hóspedes, sem exibir `_id`.

**Questão 2.** Consulte os quartos com diária superior a `250` e ordene da menor para a maior diária.

**Questão 3.** Liste os quartos que oferecem `wifi` e possuem capacidade para pelo menos três pessoas.

**Questão 4.** Consulte os hóspedes de Curitiba **ou** Maringá utilizando `$in`.

**Questão 5.** Consulte reservas confirmadas cujo `valorTotal` seja superior a `500`.

**Questão 6.** Consulte todas as reservas associadas ao hóspede com `_id: 1`.

**Questão 7.** Crie um hóspede com `_id: 8`, nome, cidade, estado, contato e pelo menos duas tags. Consulte-o para confirmar a inserção.

**Questão 8.** Atualize a cidade do hóspede 8; em seguida acrescente a tag `vip`, sem remover as anteriores.

**Questão 9.** Exclua somente o hóspede 8. Registre o resultado de uma consulta antes e depois da exclusão.

**Questão 10.** Produza a quantidade de reservas por status usando `aggregate()` e `$group`.

**Questão 11.** Utilize `$lookup` para gerar uma consulta com o identificador da reserva e o nome do hóspede correspondente.

**Questão 12.** Explique, com suas palavras, três diferenças entre o armazenamento de dados no PostgreSQL e no MongoDB, incluindo documentos aninhados, arrays ou relacionamentos.

### Entrega sugerida

Entregue um arquivo `.md` ou `.pdf` com os comandos e resultados obtidos, a resposta da questão 12 e uma evidência de que o contêiner está funcionando (saída de `docker compose ps`). Não inclua senhas.

---

# Parte 10 — Solucionando problemas comuns no Windows

### 1. `docker` não é reconhecido

Abra novamente o PowerShell depois de instalar o Docker Desktop. Confirme que o programa foi instalado e que está em execução. Verifique `docker --version`.

### 2. `Cannot connect to the Docker daemon`

Abra o **Docker Desktop** e aguarde a inicialização do mecanismo. Verifique a configuração do WSL 2 e o modo **Linux containers**.

### 3. O WSL 2 não funciona

No PowerShell:

```powershell
wsl --status
wsl --update
```

Pode ser necessário reiniciar o Windows, atualizar componentes ou habilitar virtualização. Em computadores institucionais, solicite assistência à equipe de TI.

### 4. O arquivo `.yml` virou `.yml.txt`

No Explorador de Arquivos, habilite **Exibir → Extensões de nomes de arquivos**. Corrija o nome para `docker-compose-hotel-nosql.yml`. Confira com `Get-ChildItem`.

### 5. `no configuration file provided`

Você provavelmente não está na pasta correta. Execute:

```powershell
Set-Location "$HOME\aula-nosql-hotel"
Get-ChildItem
```

Confira se o YAML está presente e use `-f .\docker-compose-hotel-nosql.yml` nos comandos.

### 6. `port is already allocated` / porta 27017 em uso

Altere **somente a porta do Windows** no YAML:

```yaml
ports:
  - "127.0.0.1:27018:27017"
```

Salve e execute:

```powershell
docker compose -f .\docker-compose-hotel-nosql.yml up -d
```

O acesso ao `mongosh` **dentro do contêiner** continua funcionando da mesma forma.

### 7. `Authentication failed`

Confira `admin_aula`, a senha da aula e `--authenticationDatabase admin`. Se o volume já existia, alterar as variáveis no arquivo YAML não redefine automaticamente as credenciais já persistidas. Não apague volumes sem autorização e sem verificar se há dados a preservar.

### 8. `mongosh` não é reconhecido no PowerShell

Você não precisa instalar o cliente no Windows. Execute-o **dentro do contêiner**:

```powershell
docker compose -f .\docker-compose-hotel-nosql.yml exec mongo mongosh --username admin_aula --authenticationDatabase admin
```

### 9. `E11000 duplicate key error`

Existe outro documento com o mesmo `_id` (ou valor de índice único). Consulte antes de inserir:

```javascript
db.hospedes.findOne({ _id: 7 })
```

A carga fornecida usa inserção condicional para evitar duplicação quando reexecutada.

### 10. O MongoDB não aparece na lista de bancos

Certifique-se de que executou a carga e selecionou `use hotel_nosql`. O comando `use` sozinho não cria documentos nem garante que o banco seja listado.

### 11. O download do JavaScript não abre no navegador

Baixe a versão `.zip` disponibilizada com a aula, extraia o arquivo `.js` e coloque-o na pasta do laboratório. O JavaScript é **um script de banco de dados**, não precisa ser aberto como página da web.

---

# Resumo dos comandos

| Ação | Comando / local de execução |
|---|---|
| Conferir WSL | `wsl --status` — PowerShell |
| Conferir Docker | `docker --version` — PowerShell |
| Conferir Compose | `docker compose version` — PowerShell |
| Testar Docker | `docker run --rm hello-world` — PowerShell |
| Subir MongoDB | `docker compose -f .\docker-compose-hotel-nosql.yml up -d` — PowerShell |
| Ver serviço | `docker compose -f .\docker-compose-hotel-nosql.yml ps` — PowerShell |
| Copiar carga | `docker cp .\carga_inicial_hotel_nosql_recriada.js mongo_hotel_aula:/tmp/carga_inicial_hotel_nosql_recriada.js` — PowerShell |
| Entrar no banco | `docker compose -f .\docker-compose-hotel-nosql.yml exec mongo mongosh --username admin_aula --authenticationDatabase admin` — PowerShell |
| Executar carga | `load("/tmp/carga_inicial_hotel_nosql_recriada.js")` — mongosh |
| Selecionar banco | `use hotel_nosql` — mongosh |
| Consultar | `db.hospedes.find({})` — mongosh |
| Inserir | `db.hospedes.insertOne({...})` — mongosh |
| Atualizar | `db.hospedes.updateOne(filtro, { $set: {...} })` — mongosh |
| Excluir | `db.hospedes.deleteOne(filtro)` — mongosh |
| Agrupar | `db.reservas.aggregate([...])` — mongosh |
| Sair do cliente | `exit` — mongosh |
| Parar preservando dados | `docker compose -f .\docker-compose-hotel-nosql.yml down` — PowerShell |

---

# Conclusão

Neste estudo, você percorreu o caminho completo:

```text
Windows → WSL 2 → Docker Desktop → contêiner MongoDB
           → mongosh → documentos → CRUD → agregações → persistência
```

Além de aprender comandos novos, você viu como o MongoDB organiza e consulta informações em **documentos**, com objetos aninhados e arrays, diferentemente das estruturas relacionais utilizadas anteriormente no PostgreSQL.

## Documentação oficial

- Docker Desktop para Windows: https://docs.docker.com/desktop/setup/install/windows-install/
- Docker Desktop com WSL 2: https://docs.docker.com/desktop/features/wsl/
- Página oficial da imagem MongoDB no Docker Hub: https://hub.docker.com/_/mongo
- Documentação do MongoDB Shell: https://www.mongodb.com/docs/mongodb-shell/
- Consultas com `find()`: https://www.mongodb.com/docs/manual/reference/method/db.collection.find/
- Atualização com `updateOne()`: https://www.mongodb.com/docs/manual/reference/method/db.collection.updateOne/
- Docker Compose: https://docs.docker.com/compose/
