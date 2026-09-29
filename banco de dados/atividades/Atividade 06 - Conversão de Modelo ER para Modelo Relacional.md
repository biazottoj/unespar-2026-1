# Atividade 06 — Conversão de Modelo ER em Modelo Relacional

## Contexto

Uma empresa deseja desenvolver um sistema de streaming musical semelhante ao Spotify. O sistema permitirá que usuários escutem músicas, sigam artistas, criem playlists, curtam faixas e acessem álbuns publicados por artistas.

Sua tarefa é modelar esse sistema em duas etapas:

1. Criar um **Diagrama Entidade-Relacionamento (DER)**.
2. Transformar o DER em um **modelo relacional**.

---

## Descrição do sistema

O sistema deve armazenar informações sobre os **usuários**, incluindo nome, e-mail, data de nascimento e tipo de plano assinado. Cada usuário pode possuir um plano gratuito ou premium. Um plano possui nome, valor mensal e limite de recursos.

Os usuários podem criar **playlists**. Cada playlist possui título, data de criação e uma indicação se ela é pública ou privada. Uma playlist pertence a apenas um usuário, mas um usuário pode criar várias playlists.

As playlists são compostas por **músicas**. Uma música pode aparecer em várias playlists, e uma playlist pode conter várias músicas. Para cada música adicionada a uma playlist, deve-se registrar a data em que ela foi adicionada e a posição da música dentro da playlist.

Cada música possui título, duração, data de lançamento e número de reproduções. Uma música pertence a um **álbum**, mas um álbum pode conter várias músicas. Um álbum possui título, data de lançamento e tipo, que pode ser *single*, *EP* ou álbum completo.

Os álbuns são publicados por **artistas**. Um artista possui nome artístico, país de origem e data de início da carreira. Um artista pode publicar vários álbuns.

Além disso, uma música pode ter a participação de mais de um artista, como ocorre em colaborações musicais. Nesse caso, deve-se registrar o papel do artista na música, por exemplo: principal, participação especial ou produtor.

Os usuários também podem **seguir artistas**. Um usuário pode seguir vários artistas, e um artista pode ser seguido por vários usuários. Para cada relação de acompanhamento, deve-se armazenar a data em que o usuário começou a seguir o artista.

Além disso, os usuários podem **curtir músicas**. Um usuário pode curtir várias músicas, e uma música pode ser curtida por vários usuários. Para cada curtida, deve-se registrar a data da curtida.

---

## Parte 1 — Construção do DER

Com base na descrição anterior, construa um **Diagrama Entidade-Relacionamento** contendo:

a) As entidades do sistema.

b) Os atributos de cada entidade.

c) As chaves primárias de cada entidade.

d) Os relacionamentos entre as entidades.

e) As cardinalidades mínimas e máximas dos relacionamentos.

f) Os atributos de relacionamentos, quando existirem.

g) A identificação de relacionamentos muitos-para-muitos.

h) A indicação de entidades associativas, quando necessário.

---

## Parte 2 — Transformação para o Modelo Relacional

Transforme o DER criado na Parte 1 em um **modelo relacional**.

Para cada tabela, indique:

a) Nome da tabela.

b) Atributos da tabela.

c) Chave primária.

d) Chaves estrangeiras.

e) Restrições importantes, quando existirem.

---

## Regras mínimas que o modelo deve atender

O modelo criado deve representar, obrigatoriamente:

1. Usuários e seus planos.
2. Playlists criadas por usuários.
3. Músicas adicionadas a playlists.
4. Álbuns compostos por músicas.
5. Artistas responsáveis por álbuns.
6. Participação de artistas em músicas.
7. Usuários seguindo artistas.
8. Usuários curtindo músicas.

---

## Questões para reflexão

Após criar o modelo, responda:

1. Quais relacionamentos do sistema são muitos-para-muitos?
2. Quais tabelas surgiram a partir da transformação desses relacionamentos?
3. Por que a relação entre playlist e música não deve ser representada apenas com uma chave estrangeira em música?
4. Por que a relação entre usuário e música curtida precisa de uma tabela própria?
5. Qual seria o impacto de armazenar todas as músicas de uma playlist em um único atributo textual?
6. Em quais tabelas aparecem chaves estrangeiras? O que cada uma delas representa?

---

## Entrega esperada

A entrega deve conter:

1. O **DER completo**, feito em ferramenta digital ou à mão com boa legibilidade.
2. O **modelo relacional**, em formato textual ou tabela.
3. As respostas às questões de reflexão.
4. Uma breve justificativa das principais decisões de modelagem.

---

## Entrega
- A entrega pode ser feita até as 23:59 do dia 19/05/2026
- A entrega deve ser feita no link: [https://forms.gle/i2sSULcTLwj9FRyM6](https://forms.gle/i2sSULcTLwj9FRyM6)
