-- =====================================================================
-- BANCO DE DADOS: SISTEMA DE STREAMING
-- Compatível com SQLite / Programiz
--
-- Conteúdos exercitados:
--   SELECT, projeção, WHERE, operadores relacionais, AND, OR,
--   valores NULL, UPPER, LOWER, LIKE, consultas com várias tabelas,
--   ALL e DISTINCT.
-- =====================================================================

PRAGMA foreign_keys = ON;

-- Faz com que o operador LIKE diferencie letras maiúsculas e minúsculas.
PRAGMA case_sensitive_like = ON;

-- Permite executar novamente o script sem conflitos.
DROP TABLE IF EXISTS visualizacao;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS conteudo;
DROP TABLE IF EXISTS plano;

-- =====================================================================
-- TABELAS
-- =====================================================================

CREATE TABLE plano (
    id_plano            INTEGER PRIMARY KEY,
    nome_plano          TEXT NOT NULL UNIQUE,
    preco_mensal        REAL NOT NULL CHECK (preco_mensal > 0),
    qualidade_video     TEXT NOT NULL,
    telas_simultaneas   INTEGER NOT NULL CHECK (telas_simultaneas > 0)
);

CREATE TABLE usuario (
    id_usuario          INTEGER PRIMARY KEY,
    nome_usuario        TEXT NOT NULL,
    email               TEXT NOT NULL UNIQUE,
    cidade              TEXT,
    id_plano            INTEGER NOT NULL,

    FOREIGN KEY (id_plano)
        REFERENCES plano (id_plano)
);

CREATE TABLE conteudo (
    id_conteudo             INTEGER PRIMARY KEY,
    titulo                  TEXT NOT NULL,
    tipo                    TEXT NOT NULL,
    genero                  TEXT NOT NULL,
    ano_lancamento          INTEGER NOT NULL,
    classificacao_indicativa INTEGER NOT NULL CHECK (classificacao_indicativa >= 0),
    duracao_minutos         INTEGER NOT NULL CHECK (duracao_minutos > 0),
    pais_origem             TEXT,
    idioma_original         TEXT
);

CREATE TABLE visualizacao (
    id_visualizacao         INTEGER PRIMARY KEY,
    id_usuario              INTEGER NOT NULL,
    id_conteudo             INTEGER NOT NULL,
    data_visualizacao       TEXT NOT NULL,
    percentual_assistido    INTEGER NOT NULL
                            CHECK (percentual_assistido BETWEEN 0 AND 100),

    FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario),

    FOREIGN KEY (id_conteudo)
        REFERENCES conteudo (id_conteudo)
);

-- =====================================================================
-- DADOS DOS PLANOS
-- =====================================================================

INSERT INTO plano
    (id_plano, nome_plano, preco_mensal, qualidade_video, telas_simultaneas)
VALUES
    (1, 'Básico',   19.90, 'HD',       1),
    (2, 'Padrão',   29.90, 'Full HD',  2),
    (3, 'Premium',  39.90, '4K',       4),
    (4, 'Família',  49.90, '4K',       6);

-- =====================================================================
-- DADOS DOS USUÁRIOS
-- =====================================================================

INSERT INTO usuario
    (id_usuario, nome_usuario, email, cidade, id_plano)
VALUES
    (1,  'Ana Souza',       'ana.souza@email.com',       'Curitiba',     3),
    (2,  'Bruno Lima',      'bruno.lima@email.com',      'São Paulo',    2),
    (3,  'Carla Mendes',    'carla.mendes@email.com',    'Curitiba',     1),
    (4,  'Diego Alves',     'diego.alves@email.com',     NULL,           2),
    (5,  'Elisa Costa',     'elisa.costa@email.com',     'Rio',          4),
    (6,  'Felipe Rocha',    'felipe.rocha@email.com',    'são paulo',    3),
    (7,  'Gabriela Nunes',  'gabriela.nunes@email.com',  'Recife',       1),
    (8,  'Henrique Silva',  'henrique.silva@email.com',  NULL,           4),
    (9,  'Amanda Reis',     'amanda.reis@email.com',     'Porto Alegre', 3),
    (10, 'Otávio Martins',  'otavio.martins@email.com',  'São Paulo',    2),
    (11, 'alana Prado',     'alana.prado@email.com',     'Salvador',     1),
    (12, 'André Barbosa',   'andre.barbosa@email.com',   'Curitiba',     4);

-- =====================================================================
-- CATÁLOGO DE CONTEÚDOS
-- =====================================================================

INSERT INTO conteudo
    (id_conteudo, titulo, tipo, genero, ano_lancamento,
     classificacao_indicativa, duracao_minutos, pais_origem,
     idioma_original)
VALUES
    (1,  'Horizonte Perdido',    'Filme',       'Drama',              2019, 14, 128, 'Brasil',         'Português'),
    (2,  'Ação Final',            'Filme',       'Ação',               2024, 16, 110, 'Estados Unidos', 'Inglês'),
    (3,  'O Último Acordo',       'Filme',       'Suspense',           2022, 14, 117, 'Espanha',        'Espanhol'),
    (4,  'Dark',                  'Série',       'Ficção científica',  2017, 16,  50, 'Alemanha',       'Alemão'),
    (5,  'Loki',                  'Série',       'Ação',               2021, 12,  48, 'Estados Unidos', 'Inglês'),
    (6,  'Harmonia',              'Filme',       'Musical',            2021,  0, 102, 'Brasil',         'Português'),
    (7,  'Planeta Azul',          'Documentário','Natureza',           2020,  0,  88, 'Reino Unido',    'Inglês'),
    (8,  'Coração em Jogo',       'Série',       'Romance',            2023, 12,  45, 'Brasil',         'Português'),
    (9,  'Aventura na Lua',       'Filme',       'Animação',           2025,  0,  95, 'França',         'Francês'),
    (10, 'Código Oculto',         'Série',       'Suspense',           2020, 16,  52, 'Canadá',         'Inglês'),
    (11, 'Educação Digital',      'Documentário','Educação',           2022,  0,  75, 'Brasil',         'Português'),
    (12, 'Onda',                  'Série',       'Drama',              2020, 12,  40, 'Portugal',       'Português'),
    (13, 'Roma',                  'Filme',       'Drama',              2018, 16, 135, 'México',         'Espanhol'),
    (14, 'Chef em Casa',          'Série',       'Culinária',          2021,  0,  30, 'Brasil',         'Português'),
    (15, 'Silêncio',              'Filme',       'Drama',              2022, 18, 145, 'Japão',          'Japonês'),
    (16, 'Brasil em Movimento',   'Documentário','História',           2024, 10,  92, 'Brasil',         NULL),
    (17, 'Viagem Fantástica',     'Filme',       'Animação',           2023,  0, 105, NULL,             'Português'),
    (18, 'O Mistério do Lago',    'Filme',       'Suspense',           2020, 14, 122, 'Argentina',      'Espanhol');

-- =====================================================================
-- HISTÓRICO DE VISUALIZAÇÕES
-- Datas armazenadas no formato AAAA-MM-DD.
-- =====================================================================

INSERT INTO visualizacao
    (id_visualizacao, id_usuario, id_conteudo, data_visualizacao,
     percentual_assistido)
VALUES
    (1,  1,  1,  '2026-07-01', 100),
    (2,  2,  1,  '2026-07-02',  85),
    (3,  3,  4,  '2026-07-02',  60),
    (4,  1,  7,  '2026-07-03', 100),
    (5,  4,  2,  '2026-07-03',  45),
    (6,  5,  8,  '2026-07-04',  90),
    (7,  6,  1,  '2026-07-04', 100),
    (8,  7,  9,  '2026-07-05',  80),
    (9,  8,  11, '2026-07-05', 100),
    (10, 9,  3,  '2026-07-06',  75),
    (11, 10, 4,  '2026-07-06', 100),
    (12, 11, 12, '2026-07-07',  55),
    (13, 12, 1,  '2026-07-07', 100),
    (14, 1,  11, '2026-07-08',  95),
    (15, 2,  15, '2026-07-08',  30),
    (16, 3,  7,  '2026-07-09', 100),
    (17, 4,  10, '2026-07-09',  70),
    (18, 5,  6,  '2026-07-10', 100),
    (19, 6,  4,  '2026-07-10',  88),
    (20, 7,  16, '2026-07-11',  92),
    (21, 8,  7,  '2026-07-11', 100),
    (22, 9,  11, '2026-07-12',  85),
    (23, 10, 18, '2026-07-12',  65),
    (24, 12, 14, '2026-07-13',  98),
    (25, 1,  4,  '2026-07-14',  40),
    (26, 3,  11, '2026-07-14', 100),
    (27, 5,  1,  '2026-07-15',  72),
    (28, 12, 7,  '2026-07-15', 100),
    (29, 2,  5,  '2026-07-16',  90),
    (30, 6,  2,  '2026-07-16', 100);

-- =====================================================================
-- CONSULTA DE VERIFICAÇÃO
-- Deve listar as quatro tabelas criadas.
-- Apague ou comente esta consulta antes de resolver a atividade.
-- =====================================================================

SELECT name AS tabela_criada
FROM sqlite_master
WHERE type = 'table'
  AND name NOT LIKE 'sqlite_%'
ORDER BY name;
