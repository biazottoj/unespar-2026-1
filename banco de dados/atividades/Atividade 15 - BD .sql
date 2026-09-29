-- ============================================================
-- BANCO DE DADOS - REVISÃO GERAL DE SQL
-- Contexto: Plataforma de Streaming
-- Compatível com SQLite / Programiz
-- ============================================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS visualizacao;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS conteudo;
DROP TABLE IF EXISTS plano;

CREATE TABLE plano (
    id_plano INTEGER PRIMARY KEY,
    nome_plano TEXT NOT NULL,
    preco_mensal REAL NOT NULL
);

CREATE TABLE usuario (
    id_usuario INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    cidade TEXT NOT NULL,
    id_plano INTEGER,
    FOREIGN KEY (id_plano) REFERENCES plano(id_plano)
);

CREATE TABLE conteudo (
    id_conteudo INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    tipo TEXT NOT NULL,
    genero TEXT NOT NULL,
    duracao_min INTEGER NOT NULL
);

CREATE TABLE visualizacao (
    id_visualizacao INTEGER PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    id_conteudo INTEGER NOT NULL,
    data_visualizacao TEXT NOT NULL,
    minutos_assistidos INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_conteudo) REFERENCES conteudo(id_conteudo)
);

INSERT INTO plano VALUES
(1, 'Básico', 24.90),
(2, 'Padrão', 39.90),
(3, 'Premium', 54.90),
(4, 'Família', 69.90),
(5, 'Estudante', 19.90),
(6, 'Cinema+', 79.90);

INSERT INTO usuario VALUES
(1, 'Ana', 'Curitiba', 2),
(2, 'Bruno', 'Londrina', 3),
(3, 'Carla', 'Curitiba', 1),
(4, 'Diego', 'Maringá', NULL),
(5, 'Elisa', 'Londrina', 2),
(6, 'Fábio', 'Cascavel', 3),
(7, 'Gabriela', 'Ponta Grossa', 4),
(8, 'Henrique', 'Curitiba', 5),
(9, 'Isabela', 'Maringá', 4);

INSERT INTO conteudo VALUES
(101, 'Horizonte Perdido', 'Filme', 'Drama', 118),
(102, 'Código Fantasma', 'Série', 'Ficção Científica', 50),
(103, 'Receita de Família', 'Filme', 'Comédia', 102),
(104, 'Última Estação', 'Série', 'Suspense', 45),
(105, 'Oceano Azul', 'Documentário', 'Natureza', 80),
(106, 'Jogo de Poder', 'Filme', 'Drama', 130),
(107, 'Cidade Invisível', 'Série', 'Fantasia', 55),
(108, 'Som do Tempo', 'Documentário', 'Música', 70),
(109, 'Conexões', 'Filme', 'Drama', 110),
(110, 'Tempo de Voltar', 'Filme', 'Drama', 95);

INSERT INTO visualizacao VALUES
(1, 1, 101, '2026-08-20', 118),
(2, 1, 102, '2026-08-21', 35),
(3, 1, 105, '2026-08-25', 60),
(4, 2, 101, '2026-08-22', 80),
(5, 2, 105, '2026-08-24', 80),
(6, 2, 106, '2026-08-26', 120),
(7, 3, 103, '2026-08-22', 102),
(8, 3, 109, '2026-08-27', 90),
(9, 5, 104, '2026-08-23', 45),
(10, 5, 101, '2026-08-24', 118),
(11, 5, 109, '2026-08-27', 100),
(12, 7, 107, '2026-08-25', 40),
(13, 7, 110, '2026-08-28', 90),
(14, 8, 102, '2026-08-28', 50),
(15, 8, 107, '2026-08-29', 55),
(16, 9, 101, '2026-08-29', 100);

-- Diego e Fábio não possuem visualizações.
-- Cinema+ não possui usuários.
-- Som do Tempo nunca foi visualizado.
