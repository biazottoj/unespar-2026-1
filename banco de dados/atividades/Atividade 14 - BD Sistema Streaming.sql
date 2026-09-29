-- ============================================================
-- BANCO DE DADOS - EXERCÍCIOS DE JOIN
-- Contexto: Sistema de Streaming
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
(5, 'Estudante', 19.90);

INSERT INTO usuario VALUES
(1, 'Ana', 'Curitiba', 2),
(2, 'Bruno', 'Londrina', 3),
(3, 'Carla', 'Curitiba', 1),
(4, 'Diego', 'Maringá', NULL),
(5, 'Elisa', 'Londrina', 2),
(6, 'Fábio', 'Cascavel', 3),
(7, 'Gabriela', 'Ponta Grossa', 4);

INSERT INTO conteudo VALUES
(101, 'Horizonte Perdido', 'Filme', 'Drama', 118),
(102, 'Código Fantasma', 'Série', 'Ficção Científica', 50),
(103, 'Receita de Família', 'Filme', 'Comédia', 102),
(104, 'Última Estação', 'Série', 'Suspense', 45),
(105, 'Oceano Azul', 'Documentário', 'Natureza', 80),
(106, 'Jogo de Poder', 'Filme', 'Drama', 130),
(107, 'Cidade Invisível', 'Série', 'Fantasia', 55),
(108, 'Som do Tempo', 'Documentário', 'Música', 70);

INSERT INTO visualizacao VALUES
(1, 1, 101, '2026-08-20', 118),
(2, 1, 102, '2026-08-21', 35),
(3, 2, 101, '2026-08-22', 80),
(4, 3, 103, '2026-08-22', 102),
(5, 5, 104, '2026-08-23', 45),
(6, 5, 101, '2026-08-24', 118),
(7, 2, 105, '2026-08-24', 80),
(8, 7, 107, '2026-08-25', 40),
(9, 1, 105, '2026-08-25', 60);

-- Conferência:
-- SELECT * FROM plano;
-- SELECT * FROM usuario;
-- SELECT * FROM conteudo;
-- SELECT * FROM visualizacao;
--
-- Observação: SQLite 3.39+ suporta RIGHT JOIN.
-- Caso a instância do Programiz utilizada em aula não aceite RIGHT JOIN,
-- a mesma lógica pode ser reescrita invertendo as tabelas e usando LEFT JOIN.
