## Porta e Senha para o PostgreSQL
Senha: ccp0stgr3sql
Porta: 5432

## Script
 SQL – Criação e População do Banco de Streaming

Este arquivo contém os comandos SQL necessários para criar e popular o banco utilizado na aula de CRUD e Triggers com PostgreSQL.

> Antes de executar este script, crie e conecte-se ao banco `streaming_aula`.

```sql
DROP TABLE IF EXISTS log_auditoria CASCADE;
DROP TABLE IF EXISTS visualizacao CASCADE;
DROP TABLE IF EXISTS usuario CASCADE;
DROP TABLE IF EXISTS conteudo CASCADE;
DROP TABLE IF EXISTS plano CASCADE;

CREATE TABLE plano (
    id_plano INTEGER PRIMARY KEY,
    nome_plano VARCHAR(50) NOT NULL,
    preco_mensal NUMERIC(10,2) NOT NULL
);

CREATE TABLE usuario (
    id_usuario INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    cidade VARCHAR(80) NOT NULL,
    id_plano INTEGER,
    CONSTRAINT fk_usuario_plano
        FOREIGN KEY (id_plano)
        REFERENCES plano(id_plano)
);

CREATE TABLE conteudo (
    id_conteudo INTEGER PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    genero VARCHAR(50) NOT NULL,
    duracao_min INTEGER NOT NULL
);

CREATE TABLE visualizacao (
    id_visualizacao INTEGER PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    id_conteudo INTEGER NOT NULL,
    data_visualizacao DATE NOT NULL,
    minutos_assistidos INTEGER NOT NULL,
    CONSTRAINT fk_visualizacao_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario),
    CONSTRAINT fk_visualizacao_conteudo
        FOREIGN KEY (id_conteudo)
        REFERENCES conteudo(id_conteudo)
);

CREATE TABLE log_auditoria (
    id_log SERIAL PRIMARY KEY,
    tabela VARCHAR(50) NOT NULL,
    operacao VARCHAR(20) NOT NULL,
    descricao TEXT NOT NULL,
    data_log TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO plano
(id_plano, nome_plano, preco_mensal)
VALUES
(1, 'Básico', 24.90),
(2, 'Padrão', 39.90),
(3, 'Premium', 54.90);

INSERT INTO usuario
(id_usuario, nome, email, cidade, id_plano)
VALUES
(1, 'Ana', 'ana@email.com', 'Curitiba', 2),
(2, 'Bruno', 'bruno@email.com', 'Londrina', 3),
(3, 'Carla', 'carla@email.com', 'Curitiba', 1);

INSERT INTO conteudo
(id_conteudo, titulo, tipo, genero, duracao_min)
VALUES
(101, 'Horizonte Perdido', 'Filme', 'Drama', 118),
(102, 'Código Fantasma', 'Série', 'Ficção Científica', 50),
(103, 'Receita de Família', 'Filme', 'Comédia', 102);

INSERT INTO visualizacao
(id_visualizacao, id_usuario, id_conteudo, data_visualizacao, minutos_assistidos)
VALUES
(1, 1, 101, '2026-09-01', 118),
(2, 2, 102, '2026-09-02', 45);
```

## Conferência

Depois de executar o script, utilize:

```sql
SELECT * FROM plano;
SELECT * FROM usuario;
SELECT * FROM conteudo;
SELECT * FROM visualizacao;
SELECT * FROM log_auditoria;
```

No `psql`, você também pode verificar as tabelas com:

```text
\dt
```

E consultar a estrutura de uma tabela com:

```text
\d usuario
```
