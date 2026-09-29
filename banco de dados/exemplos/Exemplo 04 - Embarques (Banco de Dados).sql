PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS embarque;
DROP TABLE IF EXISTS sala;
DROP TABLE IF EXISTS disciplina;
DROP TABLE IF EXISTS peca;
DROP TABLE IF EXISTS fornecedor;
DROP TABLE IF EXISTS predio;
DROP TABLE IF EXISTS departamento;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Shippings;

CREATE TABLE fornecedor (
    cod_fornec      TEXT PRIMARY KEY,
    nome_fornec     TEXT NOT NULL,
    status_fornec   INTEGER NOT NULL CHECK (status_fornec >= 0),
    cidade_fornec   TEXT
);

CREATE TABLE peca (
    cod_peca        TEXT PRIMARY KEY,
    nome_peca       TEXT NOT NULL,
    cor_peca        TEXT NOT NULL,
    peso_peca       REAL NOT NULL CHECK (peso_peca > 0),
    cidade_peca     TEXT
);

CREATE TABLE embarque (
    cod_fornec      TEXT NOT NULL,
    cod_peca        TEXT NOT NULL,
    data_embarq     TEXT NOT NULL,
    qtde_embarq     INTEGER NOT NULL CHECK (qtde_embarq > 0),

    PRIMARY KEY (cod_fornec, cod_peca, data_embarq),

    FOREIGN KEY (cod_fornec)
        REFERENCES fornecedor (cod_fornec),

    FOREIGN KEY (cod_peca)
        REFERENCES peca (cod_peca)
);

INSERT INTO fornecedor
    (cod_fornec, nome_fornec, status_fornec, cidade_fornec)
VALUES
    ('F1', 'Silva',   20, 'Porto Alegre'),
    ('F2', 'Souza',   10, 'Curitiba'),
    ('F3', 'Santos',  30, 'Curitiba'),
    ('F4', 'Tavares', 20, 'Porto Alegre'),
    ('F5', 'Moraes',  30, NULL),
    ('F6', 'Pereira', 15, 'Rio'),
    ('F7', 'Almeida', 10, 'Rio');

INSERT INTO peca
    (cod_peca, nome_peca, cor_peca, peso_peca, cidade_peca)
VALUES
    ('P1', 'Eixo',       'Vermelho', 12.00, 'Rio'),
    ('P2', 'Pino',       'Verde',    17.00, 'Curitiba'),
    ('P3', 'Parafuso',   'Azul',     17.00, 'Rio'),
    ('P4', 'Parafuso',   'Vermelho', 14.00, 'Porto Alegre'),
    ('P5', 'Engrenagem', 'Azul',     22.00, 'rIo'),
    ('P6', 'Roda',       'Vermelho', 19.00, 'Curitiba'),
    ('P7', 'Porca',      'Preto',     8.00, 'Rio');

INSERT INTO embarque
    (cod_fornec, cod_peca, data_embarq, qtde_embarq)
VALUES
    ('F1', 'P3', '2026-03-01', 100),
    ('F2', 'P3', '2026-03-02', 200),
    ('F1', 'P4', '2026-03-03',  50),
    ('F3', 'P3', '2026-03-04', 150),
    ('F1', 'P1', '2026-03-05',  80),
    ('F4', 'P2', '2026-03-06', 120),
    ('F5', 'P6', '2026-03-07',  60),
    ('F1', 'P3', '2026-04-01',  75),
    ('F6', 'P7', '2026-04-02',  40);

CREATE TABLE predio (
    cod_predio      TEXT PRIMARY KEY,
    nome_predio     TEXT NOT NULL UNIQUE
);

CREATE TABLE sala (
    cod_predio      TEXT NOT NULL,
    num_sala        INTEGER NOT NULL,
    descricao_sala  TEXT NOT NULL,
    capacidade      INTEGER NOT NULL CHECK (capacidade > 0),

    PRIMARY KEY (cod_predio, num_sala),

    FOREIGN KEY (cod_predio)
        REFERENCES predio (cod_predio)
);

CREATE TABLE departamento (
    cod_depto       TEXT PRIMARY KEY,
    nome_depto      TEXT NOT NULL
);

CREATE TABLE disciplina (
    cod_depto       TEXT NOT NULL,
    num_disciplina  INTEGER NOT NULL,
    nome_disciplina TEXT NOT NULL,

    PRIMARY KEY (cod_depto, num_disciplina),

    FOREIGN KEY (cod_depto)
        REFERENCES departamento (cod_depto)
);

INSERT INTO predio (cod_predio, nome_predio)
VALUES
    ('PR1', 'Informática - aulas'),
    ('PR2', 'Engenharia - laboratórios'),
    ('PR3', 'Biblioteca Central');

INSERT INTO sala (cod_predio, num_sala, descricao_sala, capacidade)
VALUES
    ('PR1', 101, 'Laboratório de Banco de Dados', 40),
    ('PR1', 102, 'Sala Multimídia',                35),
    ('PR1', 201, 'Laboratório de Redes',           30),
    ('PR2',  10, 'Laboratório de Materiais',       25),
    ('PR3',   1, 'Auditório',                     120);

INSERT INTO departamento (cod_depto, nome_depto)
VALUES
    ('INF', 'Informática'),
    ('ENG', 'Engenharia'),
    ('ADM', 'Administração'),
    ('MAT', 'Matemática');

INSERT INTO disciplina (cod_depto, num_disciplina, nome_disciplina)
VALUES
    ('INF', 101, 'Programação I'),
    ('INF', 205, 'Banco de Dados'),
    ('ENG', 110, 'Comunicação Técnica'),
    ('ADM', 200, 'Gestão de Projetos'),
    ('MAT', 101, 'Cálculo I'),
    ('INF', 220, 'Automação Industrial'),
    ('INF', 310, 'ComputAÇÃO Gráfica');
  
SELECT * FROM peca