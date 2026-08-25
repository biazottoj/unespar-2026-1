-- ============================================================
-- BANCO DE DADOS - AULA SOBRE JOIN
-- Contexto: Sistema de Streaming
-- Compatível com SQLite / Programiz
-- ============================================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS visualizacao;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS conteudo;
DROP TABLE IF EXISTS plano;

-- ------------------------------------------------------------
-- Tabela: plano
-- ------------------------------------------------------------
CREATE TABLE plano (
    id_plano INTEGER PRIMARY KEY,
    nome_plano TEXT NOT NULL,
    preco_mensal REAL NOT NULL
);

-- ------------------------------------------------------------
-- Tabela: usuario
-- id_plano pode ser NULL para permitir exemplos de usuários
-- ainda sem plano associado.
-- ------------------------------------------------------------
CREATE TABLE usuario (
    id_usuario INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    id_plano INTEGER,
    FOREIGN KEY (id_plano) REFERENCES plano(id_plano)
);

-- ------------------------------------------------------------
-- Tabela: conteudo
-- ------------------------------------------------------------
CREATE TABLE conteudo (
    id_conteudo INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    tipo TEXT NOT NULL,
    genero TEXT NOT NULL,
    duracao_min INTEGER NOT NULL
);

-- ------------------------------------------------------------
-- Tabela: visualizacao
-- Cada linha representa uma visualização feita por um usuário.
-- ------------------------------------------------------------
CREATE TABLE visualizacao (
    id_visualizacao INTEGER PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    id_conteudo INTEGER NOT NULL,
    data_visualizacao TEXT NOT NULL,
    minutos_assistidos INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_conteudo) REFERENCES conteudo(id_conteudo)
);

-- ============================================================
-- DADOS
-- ============================================================

INSERT INTO plano (id_plano, nome_plano, preco_mensal) VALUES
(1, 'Básico', 24.90),
(2, 'Padrão', 39.90),
(3, 'Premium', 54.90),
(4, 'Família', 69.90);

INSERT INTO usuario (id_usuario, nome, email, id_plano) VALUES
(1, 'Ana',   'ana@email.com',   2),
(2, 'Bruno', 'bruno@email.com', 3),
(3, 'Carla', 'carla@email.com', 1),
(4, 'Diego', 'diego@email.com', NULL),
(5, 'Elisa', 'elisa@email.com', 2),
(6, 'Fábio', 'fabio@email.com', 3);

INSERT INTO conteudo (id_conteudo, titulo, tipo, genero, duracao_min) VALUES
(101, 'Horizonte Perdido', 'Filme',        'Drama',             118),
(102, 'Código Fantasma',    'Série',        'Ficção Científica',  50),
(103, 'Receita de Família', 'Filme',        'Comédia',            102),
(104, 'Última Estação',     'Série',        'Suspense',            45),
(105, 'Oceano Azul',        'Documentário', 'Natureza',            80),
(106, 'Jogo de Poder',      'Filme',        'Drama',              130);

INSERT INTO visualizacao
(id_visualizacao, id_usuario, id_conteudo, data_visualizacao, minutos_assistidos)
VALUES
(1, 1, 101, '2026-08-20', 118),
(2, 1, 102, '2026-08-21', 35),
(3, 2, 101, '2026-08-22', 80),
(4, 3, 103, '2026-08-22', 102),
(5, 5, 104, '2026-08-23', 45),
(6, 5, 101, '2026-08-24', 118),
(7, 2, 105, '2026-08-24', 80);

-- ============================================================
-- CONSULTAS ÚTEIS PARA CONFERÊNCIA
-- Descomente uma por vez no Programiz.
-- ============================================================

-- SELECT * FROM plano;
-- SELECT * FROM usuario;
-- SELECT * FROM conteudo;
-- SELECT * FROM visualizacao;

-- INNER JOIN
-- SELECT u.nome, p.nome_plano
-- FROM usuario AS u
-- INNER JOIN plano AS p
--     ON u.id_plano = p.id_plano;

-- LEFT JOIN
-- SELECT u.nome, v.id_visualizacao, v.data_visualizacao
-- FROM usuario AS u
-- LEFT JOIN visualizacao AS v
--     ON u.id_usuario = v.id_usuario
-- ORDER BY u.id_usuario, v.id_visualizacao;

-- RIGHT JOIN
-- SQLite 3.39+ oferece suporte a RIGHT JOIN.
-- SELECT c.id_conteudo, c.titulo, v.id_visualizacao, v.id_usuario
-- FROM visualizacao AS v
-- RIGHT JOIN conteudo AS c
--     ON v.id_conteudo = c.id_conteudo
-- ORDER BY c.id_conteudo, v.id_visualizacao;

-- Forma equivalente ao RIGHT JOIN acima usando LEFT JOIN:
-- SELECT c.id_conteudo, c.titulo, v.id_visualizacao, v.id_usuario
-- FROM conteudo AS c
-- LEFT JOIN visualizacao AS v
--     ON v.id_conteudo = c.id_conteudo
-- ORDER BY c.id_conteudo, v.id_visualizacao;
