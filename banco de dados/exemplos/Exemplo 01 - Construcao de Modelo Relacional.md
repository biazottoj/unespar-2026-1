# Exemplo guiado — Construção de um esquema relacional

## Tema: Sistema de eventos acadêmicos

Neste exemplo, vamos transformar uma descrição textual de um sistema em um **esquema relacional**.  
O objetivo é identificar as tabelas, colunas, chaves primárias, chaves estrangeiras, chaves alternativas e algumas restrições de integridade.

---

## 1. Cenário do sistema

Uma instituição deseja criar um sistema para controlar eventos acadêmicos.

Cada evento possui:

- código;
- nome;
- data de início;
- data de fim;
- local.

Um evento pode ter várias atividades, como palestras, minicursos e mesas-redondas.

Cada atividade pertence a apenas um evento.

Uma atividade pode ter um ou mais palestrantes.

Um palestrante pode participar de várias atividades.

Participantes podem se inscrever em vários eventos.

Para cada inscrição, o sistema deve registrar:

- data da inscrição;
- tipo de inscrição;
- situação do pagamento.

---

## 2. Identificação das entidades principais

A primeira etapa é identificar os principais objetos sobre os quais o sistema precisa guardar informações.

Neste cenário, podemos identificar as seguintes entidades:

- Evento
- Atividade
- Palestrante
- Participante
- Inscrição

Uma primeira versão das tabelas seria:

```text
Evento(...)
Atividade(...)
Palestrante(...)
Participante(...)
Inscricao(...)
````

---

## 3. Análise dos relacionamentos

Agora precisamos analisar como essas entidades se relacionam.

---

### 3.1 Relacionamento entre Evento e Atividade

O enunciado diz:

> Um evento pode ter várias atividades.
> Cada atividade pertence a apenas um evento.

Isso representa um relacionamento **1:N**.

* Um evento pode ter várias atividades.
* Uma atividade pertence a um único evento.

Portanto, a chave estrangeira deve ficar na tabela do lado N, ou seja, na tabela `Atividade`.

Representação:

```text
Evento(CodigoEvento, NomeEvento, DataInicio, DataFim, Local)

Atividade(CodigoAtividade, CodigoEvento, Titulo, Tipo, DataHoraInicio, DataHoraFim)
```

Nesse caso:

```text
Atividade.CodigoEvento referencia Evento.CodigoEvento
```

---

### 3.2 Relacionamento entre Atividade e Palestrante

O enunciado diz:

> Uma atividade pode ter um ou mais palestrantes.
> Um palestrante pode participar de várias atividades.

Isso representa um relacionamento **N:N**.

* Uma atividade pode ter vários palestrantes.
* Um palestrante pode participar de várias atividades.

Uma solução incorreta seria criar uma coluna `Palestrantes` dentro da tabela `Atividade`.

Exemplo incorreto:

| CodigoAtividade | Titulo                              | Palestrantes          |
| --------------- | ----------------------------------- | --------------------- |
| A01             | Inteligência Artificial na Educação | Ana Souza, Bruno Lima |

Essa solução é inadequada porque a coluna `Palestrantes` possui vários valores no mesmo campo.

Problemas dessa solução:

* dificulta buscar todas as atividades de um palestrante específico;
* dificulta remover apenas um palestrante de uma atividade;
* dificulta garantir a integridade dos dados;
* viola a ideia de que os valores de uma coluna devem ser atômicos e monovalorados.

A solução adequada é criar uma tabela associativa:

```text
AtividadePalestrante(CodigoAtividade, CodigoPalestrante)
```

---

### 3.3 Relacionamento entre Participante e Evento

O enunciado diz:

> Participantes podem se inscrever em vários eventos.

Também podemos concluir que:

> Um evento pode ter vários participantes inscritos.

Logo, temos outro relacionamento **N:N**.

Nesse caso, a tabela associativa será `Inscricao`.

Além de ligar participantes e eventos, essa tabela também possui informações próprias, como data da inscrição, tipo de inscrição e situação do pagamento.

Representação:

```text
Inscricao(CodigoEvento, CodigoParticipante, DataInscricao, TipoInscricao, SituacaoPagamento)
```

---

## 4. Primeira versão do esquema relacional

A partir da análise anterior, podemos propor o seguinte conjunto de tabelas:

```text
Evento(CodigoEvento, NomeEvento, DataInicio, DataFim, Local)

Atividade(CodigoAtividade, CodigoEvento, Titulo, Tipo, DataHoraInicio, DataHoraFim)

Palestrante(CodigoPalestrante, NomePalestrante, Email, Instituicao)

AtividadePalestrante(CodigoAtividade, CodigoPalestrante)

Participante(CodigoParticipante, NomeParticipante, Email, CPF)

Inscricao(CodigoEvento, CodigoParticipante, DataInscricao, TipoInscricao, SituacaoPagamento)
```

---

## 5. Definição das chaves primárias

A chave primária identifica cada linha de forma única dentro de uma tabela.

---

### 5.1 Tabela Evento

```text
Evento(CodigoEvento, NomeEvento, DataInicio, DataFim, Local)
```

Chave primária:

```text
PK: CodigoEvento
```

Justificativa:

O nome do evento não é uma boa chave primária, pois podem existir eventos com nomes iguais ou parecidos em anos diferentes.

---

### 5.2 Tabela Atividade

```text
Atividade(CodigoAtividade, CodigoEvento, Titulo, Tipo, DataHoraInicio, DataHoraFim)
```

Chave primária:

```text
PK: CodigoAtividade
```

Justificativa:

Cada atividade precisa ter um identificador próprio, pois um evento pode possuir várias atividades.

---

### 5.3 Tabela Palestrante

```text
Palestrante(CodigoPalestrante, NomePalestrante, Email, Instituicao)
```

Chave primária:

```text
PK: CodigoPalestrante
```

Possível chave alternativa:

```text
AK: Email
```

Justificativa:

O código identifica o palestrante no sistema.
O email pode ser uma chave alternativa, desde que o sistema exija que cada palestrante tenha um email único.

---

### 5.4 Tabela Participante

```text
Participante(CodigoParticipante, NomeParticipante, Email, CPF)
```

Chave primária:

```text
PK: CodigoParticipante
```

Possíveis chaves alternativas:

```text
AK: Email
AK: CPF
```

Justificativa:

O sistema pode usar um código interno como chave primária.
CPF e email também podem ser únicos, mas não precisam ser escolhidos como chave primária.

---

### 5.5 Tabela AtividadePalestrante

```text
AtividadePalestrante(CodigoAtividade, CodigoPalestrante)
```

Chave primária composta:

```text
PK: CodigoAtividade, CodigoPalestrante
```

Justificativa:

A combinação dos dois campos identifica a participação de um palestrante em uma atividade.

Essa chave composta evita que o mesmo palestrante seja cadastrado duas vezes na mesma atividade.

---

### 5.6 Tabela Inscricao

```text
Inscricao(CodigoEvento, CodigoParticipante, DataInscricao, TipoInscricao, SituacaoPagamento)
```

Chave primária composta:

```text
PK: CodigoEvento, CodigoParticipante
```

Justificativa:

Essa chave indica que um participante só pode ter uma inscrição por evento.

Caso o sistema permitisse múltiplas inscrições do mesmo participante no mesmo evento, seria melhor criar uma coluna `CodigoInscricao`.

---

## 6. Definição das chaves estrangeiras

As chaves estrangeiras representam os relacionamentos entre as tabelas.

```text
Atividade.CodigoEvento referencia Evento.CodigoEvento

AtividadePalestrante.CodigoAtividade referencia Atividade.CodigoAtividade
AtividadePalestrante.CodigoPalestrante referencia Palestrante.CodigoPalestrante

Inscricao.CodigoEvento referencia Evento.CodigoEvento
Inscricao.CodigoParticipante referencia Participante.CodigoParticipante
```

Resumo:

| Chave estrangeira                                                      | Significado                                       |
| ---------------------------------------------------------------------- | ------------------------------------------------- |
| Atividade.CodigoEvento → Evento.CodigoEvento                           | Indica a qual evento a atividade pertence         |
| AtividadePalestrante.CodigoAtividade → Atividade.CodigoAtividade       | Indica a atividade associada ao palestrante       |
| AtividadePalestrante.CodigoPalestrante → Palestrante.CodigoPalestrante | Indica o palestrante associado à atividade        |
| Inscricao.CodigoEvento → Evento.CodigoEvento                           | Indica em qual evento o participante se inscreveu |
| Inscricao.CodigoParticipante → Participante.CodigoParticipante         | Indica qual participante fez a inscrição          |

---

## 7. Esquema relacional final

```text
Evento(CodigoEvento, NomeEvento, DataInicio, DataFim, Local)
PK: CodigoEvento

Atividade(CodigoAtividade, CodigoEvento, Titulo, Tipo, DataHoraInicio, DataHoraFim)
PK: CodigoAtividade
FK: CodigoEvento referencia Evento(CodigoEvento)

Palestrante(CodigoPalestrante, NomePalestrante, Email, Instituicao)
PK: CodigoPalestrante
AK: Email

AtividadePalestrante(CodigoAtividade, CodigoPalestrante)
PK: CodigoAtividade, CodigoPalestrante
FK: CodigoAtividade referencia Atividade(CodigoAtividade)
FK: CodigoPalestrante referencia Palestrante(CodigoPalestrante)

Participante(CodigoParticipante, NomeParticipante, Email, CPF)
PK: CodigoParticipante
AK: Email
AK: CPF

Inscricao(CodigoEvento, CodigoParticipante, DataInscricao, TipoInscricao, SituacaoPagamento)
PK: CodigoEvento, CodigoParticipante
FK: CodigoEvento referencia Evento(CodigoEvento)
FK: CodigoParticipante referencia Participante(CodigoParticipante)
```

---

## 8. Restrições de domínio

A integridade de domínio define quais valores são permitidos em uma coluna.

Exemplos:

| Coluna                | Domínio possível                           |
| --------------------- | ------------------------------------------ |
| Tipo da atividade     | Palestra, Minicurso, Mesa-redonda, Oficina |
| Tipo de inscrição     | Aluno, Professor, Comunidade externa       |
| Situação do pagamento | Pendente, Pago, Isento, Cancelado          |
| DataInicio            | Data válida                                |
| DataFim               | Data válida                                |
| Email                 | Texto em formato de email                  |
| CPF                   | Texto em formato válido de CPF             |

Exemplo de valor válido:

```text
Tipo = "Palestra"
```

Exemplo de valor inválido:

```text
Tipo = "Coisa acadêmica"
```

Esse valor é inválido porque não pertence ao domínio definido para o tipo da atividade.

---

## 9. Restrições de vazio

A integridade de vazio define quais colunas podem ou não aceitar valor nulo.

Exemplo para a tabela `Evento`:

| Coluna       | Obrigatória? | Justificativa                          |
| ------------ | ------------ | -------------------------------------- |
| CodigoEvento | Sim          | Identifica o evento                    |
| NomeEvento   | Sim          | Todo evento precisa ter nome           |
| DataInicio   | Sim          | Todo evento precisa ter data de início |
| DataFim      | Sim          | Todo evento precisa ter data de fim    |
| Local        | Sim          | Todo evento precisa ter local definido |

Exemplo para a tabela `Palestrante`:

| Coluna            | Obrigatória? | Justificativa                     |
| ----------------- | ------------ | --------------------------------- |
| CodigoPalestrante | Sim          | Identifica o palestrante          |
| NomePalestrante   | Sim          | Todo palestrante precisa ter nome |
| Email             | Sim          | Necessário para contato           |
| Instituicao       | Não          | Pode não ser informada            |

Exemplo para a tabela `Inscricao`:

| Coluna             | Obrigatória? | Justificativa                                         |
| ------------------ | ------------ | ----------------------------------------------------- |
| CodigoEvento       | Sim          | Toda inscrição deve estar associada a um evento       |
| CodigoParticipante | Sim          | Toda inscrição deve estar associada a um participante |
| DataInscricao      | Sim          | É necessário saber quando a inscrição foi feita       |
| TipoInscricao      | Sim          | Pode influenciar preço ou certificado                 |
| SituacaoPagamento  | Sim          | Necessário para controle da inscrição                 |

---

## 10. Restrições semânticas

Restrições semânticas representam regras de negócio do sistema.

Exemplos:

1. A data de fim do evento não pode ser anterior à data de início.
2. A data e hora de fim da atividade não pode ser anterior à data e hora de início.
3. Uma atividade não pode ocorrer fora do período do evento.
4. Um participante não pode se inscrever duas vezes no mesmo evento.
5. Um palestrante não pode estar em duas atividades no mesmo horário.
6. Uma inscrição cancelada não deve gerar certificado.
7. Uma inscrição com pagamento pendente pode impedir a emissão do certificado.

Algumas dessas regras podem ser garantidas diretamente pelo banco de dados.
Outras podem exigir validações adicionais na aplicação, triggers ou procedimentos armazenados.

---

## 11. Dados de exemplo

### Evento

| CodigoEvento | NomeEvento            | DataInicio | DataFim    | Local             |
| ------------ | --------------------- | ---------- | ---------- | ----------------- |
| E01          | Semana Acadêmica      | 10/06/2025 | 14/06/2025 | Auditório Central |
| E02          | Jornada de Tecnologia | 20/08/2025 | 22/08/2025 | Bloco B           |

---

### Atividade

| CodigoAtividade | CodigoEvento | Titulo                    | Tipo         |
| --------------- | ------------ | ------------------------- | ------------ |
| A01             | E01          | Banco de Dados na Prática | Palestra     |
| A02             | E01          | Introdução a SQL          | Minicurso    |
| A03             | E02          | IA na Educação            | Mesa-redonda |

---

### Palestrante

| CodigoPalestrante | NomePalestrante | Email                                     |
| ----------------- | --------------- | ----------------------------------------- |
| PL01              | Ana Souza       | [ana@email.com](mailto:ana@email.com)     |
| PL02              | Bruno Lima      | [bruno@email.com](mailto:bruno@email.com) |

---

### AtividadePalestrante

| CodigoAtividade | CodigoPalestrante |
| --------------- | ----------------- |
| A01             | PL01              |
| A02             | PL01              |
| A03             | PL01              |
| A03             | PL02              |

Nesse exemplo:

* Ana Souza participa de três atividades.
* A atividade `A03` possui dois palestrantes.
* Isso mostra a necessidade da tabela associativa `AtividadePalestrante`.

---

### Participante

| CodigoParticipante | NomeParticipante | Email                                     | CPF            |
| ------------------ | ---------------- | ----------------------------------------- | -------------- |
| P01                | João Silva       | [joao@email.com](mailto:joao@email.com)   | 111.111.111-11 |
| P02                | Maria Lima       | [maria@email.com](mailto:maria@email.com) | 222.222.222-22 |

---

### Inscricao

| CodigoEvento | CodigoParticipante | DataInscricao | TipoInscricao | SituacaoPagamento |
| ------------ | ------------------ | ------------- | ------------- | ----------------- |
| E01          | P01                | 01/06/2025    | Aluno         | Pago              |
| E01          | P02                | 02/06/2025    | Professor     | Isento            |
| E02          | P01                | 10/08/2025    | Aluno         | Pendente          |

Nesse exemplo:

* João Silva está inscrito em dois eventos.
* A Semana Acadêmica possui dois participantes inscritos.
* A tabela `Inscricao` representa o relacionamento N:N entre `Evento` e `Participante`.

---

## 12. Testes de consistência

Analise os casos abaixo e indique se são válidos ou inválidos.

---

### Caso 1

```text
Atividade(A10, E99, "Segurança da Informação", "Palestra")
```

Esse registro é válido?

Resposta:

Não.
O evento `E99` não existe na tabela `Evento`.

Restrição violada:

```text
Integridade referencial
```

---

### Caso 2

```text
Participante(P03, "Carlos Souza", "joao@email.com", "333.333.333-33")
```

Esse registro é válido?

Resposta:

Não, se `Email` for chave alternativa.
O email `joao@email.com` já pertence ao participante `P01`.

Restrição violada:

```text
Integridade de chave
```

---

### Caso 3

```text
Inscricao(E01, P03, 05/06/2025, "Aluno", "Pago")
```

Esse registro é válido?

Resposta:

Não.
O participante `P03` não existe na tabela `Participante`.

Restrição violada:

```text
Integridade referencial
```

---

### Caso 4

```text
Evento(E03, "Congresso de Software", 15/09/2025, 10/09/2025, "Auditório")
```

Esse registro é válido?

Resposta:

Não.
A data de fim é anterior à data de início.

Restrição violada:

```text
Restrição semântica
```

---

### Caso 5

```text
Inscricao(E01, P01, NULL, "Aluno", "Pago")
```

Esse registro é válido?

Resposta:

Não.
A data da inscrição deveria ser obrigatória.

Restrição violada:

```text
Integridade de vazio
```

---