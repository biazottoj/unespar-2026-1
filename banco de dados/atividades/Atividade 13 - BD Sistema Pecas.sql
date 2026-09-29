-- =====================================================================
-- BANCO DE DADOS - CAPÍTULO 7 (páginas 59 até 103)
-- Compatível com Programiz / SQLite
--
-- Exemplos contemplados:
--   7.15 - INTERSECT
--   7.16 - UNION ALL
--   7.17 - aliases de tabelas
--   7.18 - alias de coluna
--   7.19 - coluna resultante de expressão
--   7.20 - autorrelacionamento / mesma tabela usada duas vezes
--   7.21 - subconsulta no FROM
--   7.22 - subconsulta escalar
-- =====================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- Limpeza para permitir executar/importar o script novamente
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS embarque;
DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS empregado;
DROP TABLE IF EXISTS peca;
DROP TABLE IF EXISTS fornecedor;
DROP TABLE IF EXISTS depto;

-- =====================================================================
-- 1. BANCO DE DADOS DE EMBARQUES
--    Usado nos exemplos 7.15 a 7.19 e 7.21
-- =====================================================================

CREATE TABLE fornecedor (
    cod_fornec      TEXT PRIMARY KEY,
    nome_fornec     TEXT NOT NULL,
    status_fornec   INTEGER NOT NULL,
    cidade_fornec   TEXT
);

CREATE TABLE peca (
    cod_peca        TEXT PRIMARY KEY,
    nome_peca       TEXT NOT NULL,
    cor_peca        TEXT NOT NULL,
    peso_peca       REAL NOT NULL,
    cidade_peca     TEXT
);

CREATE TABLE embarque (
    cod_fornec      TEXT NOT NULL,
    cod_peca        TEXT NOT NULL,
    data_embarq     TEXT NOT NULL,
    qtde_embarq     INTEGER NOT NULL,

    PRIMARY KEY (cod_fornec, cod_peca, data_embarq),

    FOREIGN KEY (cod_fornec)
        REFERENCES fornecedor (cod_fornec),

    FOREIGN KEY (cod_peca)
        REFERENCES peca (cod_peca)
);

-- Há cidades repetidas propositalmente para permitir demonstrar
-- duplicatas, INTERSECT e UNION ALL.
INSERT INTO fornecedor
    (cod_fornec, nome_fornec, status_fornec, cidade_fornec)
VALUES
    ('F1', 'Silva',    20, 'Porto Alegre'),
    ('F2', 'Souza',    10, 'Curitiba'),
    ('F3', 'Santos',   30, 'Curitiba'),
    ('F4', 'Tavares',  20, 'Porto Alegre'),
    ('F5', 'Moraes',   30, NULL),
    ('F6', 'Pereira',  15, 'Rio'),
    ('F7', 'Almeida',  10, 'Florianópolis');

INSERT INTO peca
    (cod_peca, nome_peca, cor_peca, peso_peca, cidade_peca)
VALUES
    ('P1', 'Eixo',       'Vermelho', 12.0, 'Rio'),
    ('P2', 'Pino',       'Verde',    17.0, 'Curitiba'),
    ('P3', 'Parafuso',   'Azul',     17.0, 'Rio'),
    ('P4', 'Parafuso',   'Vermelho', 14.0, 'Porto Alegre'),
    ('P5', 'Engrenagem', 'Azul',     22.0, 'Campinas'),
    ('P6', 'Roda',       'Vermelho', 19.0, 'Curitiba'),
    ('P7', 'Porca',      'Preto',     8.0, 'Londrina');

-- Datas são armazenadas como TEXT no formato ISO (AAAA-MM-DD),
-- formato adequado para uso didático no SQLite/Programiz.
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
    -- Segundo embarque da mesma peça pelo fornecedor F1.
    -- Isso faz o DISTINCT do Exemplo 7.17 ter efeito observável.
    ('F1', 'P3', '2026-04-01',  75),
    ('F6', 'P7', '2026-04-02',  40),
    ('F7', 'P5', '2026-04-03',  90);

-- =====================================================================
-- 2. TABELA EMPREGADO
--    Usada no Exemplo 7.20
--
-- Os dados abaixo reproduzem os valores mostrados no slide:
--   10 Pereira  NULL
--   21 Tavares  10
--   30 Santos   10
--   55 Almeida  21
-- =====================================================================

CREATE TABLE empregado (
    codigo_emp      INTEGER PRIMARY KEY,
    nome            TEXT NOT NULL,
    cod_emp_chefe   INTEGER,

    FOREIGN KEY (cod_emp_chefe)
        REFERENCES empregado (codigo_emp)
);

INSERT INTO empregado (codigo_emp, nome, cod_emp_chefe)
VALUES
    (10, 'Pereira', NULL),
    (21, 'Tavares', 10),
    (30, 'Santos',  10),
    (55, 'Almeida', 21);

-- =====================================================================
-- 3. BANCO ACADÊMICO - DEPARTAMENTOS E PROFESSORES
--    Usado no Exemplo 7.22 (subconsulta escalar)
-- =====================================================================

CREATE TABLE depto (
    cod_depto       TEXT PRIMARY KEY,
    nome_depto      TEXT NOT NULL
);

CREATE TABLE professor (
    cod_prof        TEXT PRIMARY KEY,
    nome_prof       TEXT NOT NULL,
    cod_depto       TEXT NOT NULL,

    FOREIGN KEY (cod_depto)
        REFERENCES depto (cod_depto)
);

INSERT INTO depto (cod_depto, nome_depto)
VALUES
    ('INF', 'Informática'),
    ('MAT', 'Matemática'),
    ('ADM', 'Administração'),
    ('ENG', 'Engenharia');

INSERT INTO professor (cod_prof, nome_prof, cod_depto)
VALUES
    ('PR01', 'Ana Martins',     'INF'),
    ('PR02', 'Carlos Oliveira', 'INF'),
    ('PR03', 'Beatriz Lima',    'MAT'),
    ('PR04', 'Daniel Souza',    'ADM'),
    ('PR05', 'Marina Costa',    'ENG');

-- =====================================================================
-- CONSULTAS DOS EXEMPLOS - deixadas comentadas para teste em aula
-- Descomente uma consulta por vez no Programiz.
-- =====================================================================

-- ---------------------------------------------------------------------
-- Exemplo 7.15
-- Obter as cidades em que há tanto uma peça quanto um fornecedor.
-- ---------------------------------------------------------------------
-- SELECT cidade_fornec
-- FROM fornecedor
-- INTERSECT
-- SELECT cidade_peca
-- FROM peca;

-- ---------------------------------------------------------------------
-- Exemplo 7.16
-- Obter as cidades nas quais se encontra uma peça ou um fornecedor.
-- O resultado pode conter duplicatas.
-- ---------------------------------------------------------------------
-- SELECT cidade_fornec
-- FROM fornecedor
-- UNION ALL
-- SELECT cidade_peca
-- FROM peca;

-- ---------------------------------------------------------------------
-- Exemplo 7.17
-- Obter código, nome e peso das peças para as quais existe ao menos
-- um embarque realizado pelo fornecedor F1.
-- ---------------------------------------------------------------------
-- SELECT DISTINCT
--     p.cod_peca,
--     p.nome_peca,
--     p.peso_peca
-- FROM peca AS p,
--      embarque AS e
-- WHERE p.cod_peca = e.cod_peca
--   AND e.cod_fornec = 'F1';

-- ---------------------------------------------------------------------
-- Exemplo 7.18
-- Mesmo objetivo do 7.15, mas a coluna resultante deve se chamar cidade.
-- ---------------------------------------------------------------------
-- SELECT cidade_fornec AS cidade
-- FROM fornecedor
-- INTERSECT
-- SELECT cidade_peca
-- FROM peca;

-- ---------------------------------------------------------------------
-- Exemplo 7.19
-- Obter o peso das peças em libras.
-- ---------------------------------------------------------------------
-- SELECT
--     cod_peca,
--     nome_peca,
--     peso_peca * 2.2046 AS peso_peca_libras
-- FROM peca;

-- ---------------------------------------------------------------------
-- Exemplo 7.20
-- Para cada empregado que possui chefe, mostrar empregado e chefe.
-- ---------------------------------------------------------------------
-- SELECT
--     empregado.nome AS empregado,
--     chefe.nome AS chefe
-- FROM empregado,
--      empregado AS chefe
-- WHERE empregado.cod_emp_chefe = chefe.codigo_emp;

-- ---------------------------------------------------------------------
-- Exemplo 7.21
-- Para cada embarque de uma peça chamada Parafuso, obter o código da
-- peça, o código do fornecedor, o nome do fornecedor e a data.
-- ---------------------------------------------------------------------
-- SELECT
--     parafuso.cod_peca,
--     embarque.cod_fornec,
--     fornecedor.nome_fornec,
--     embarque.data_embarq
-- FROM (
--     SELECT cod_peca
--     FROM peca
--     WHERE nome_peca = 'Parafuso'
-- ) AS parafuso,
-- embarque,
-- fornecedor
-- WHERE parafuso.cod_peca = embarque.cod_peca
--   AND fornecedor.cod_fornec = embarque.cod_fornec;

-- ---------------------------------------------------------------------
-- Exemplo 7.22
-- Para cada professor, obter código, nome e nome do departamento.
-- ---------------------------------------------------------------------
-- SELECT
--     cod_prof,
--     nome_prof,
--     (
--         SELECT nome_depto
--         FROM depto
--         WHERE depto.cod_depto = professor.cod_depto
--     ) AS nome_depto
-- FROM professor;

-- =====================================================================
-- Verificação da criação das tabelas.
-- Deve listar: depto, empregado, embarque, fornecedor, peca e professor.
-- =====================================================================
SELECT name AS tabela_criada
FROM sqlite_master
WHERE type = 'table'
  AND name NOT LIKE 'sqlite_%'
ORDER BY name;
