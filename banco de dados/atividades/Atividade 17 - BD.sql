-- ============================================================
-- BANCO DE DADOS - SISTEMA DE RESERVAS DE HOTEL
-- PostgreSQL
-- Banco sugerido: hotel_aula
-- ============================================================

-- Caso queira criar o banco pelo terminal:
-- CREATE DATABASE hotel_aula;
-- \c hotel_aula

DROP TABLE IF EXISTS reserva CASCADE;
DROP TABLE IF EXISTS quarto CASCADE;
DROP TABLE IF EXISTS hospede CASCADE;
DROP TABLE IF EXISTS tipo_quarto CASCADE;
DROP TABLE IF EXISTS funcionario CASCADE;

-- ============================================================
-- TIPO DE QUARTO
-- ============================================================

CREATE TABLE tipo_quarto (
    id_tipo INTEGER PRIMARY KEY,
    nome_tipo VARCHAR(50) NOT NULL UNIQUE,
    valor_diaria NUMERIC(10,2) NOT NULL,
    capacidade INTEGER NOT NULL,
    descricao VARCHAR(200)
);

-- ============================================================
-- QUARTO
-- ============================================================

CREATE TABLE quarto (
    id_quarto INTEGER PRIMARY KEY,
    numero VARCHAR(10) NOT NULL UNIQUE,
    andar INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    vista VARCHAR(30),
    id_tipo INTEGER NOT NULL,
    CONSTRAINT fk_quarto_tipo
        FOREIGN KEY (id_tipo)
        REFERENCES tipo_quarto(id_tipo)
);

-- ============================================================
-- HÓSPEDE
-- ============================================================

CREATE TABLE hospede (
    id_hospede INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    cidade VARCHAR(80),
    estado CHAR(2),
    telefone VARCHAR(20)
);

-- ============================================================
-- RESERVA
-- ============================================================

CREATE TABLE reserva (
    id_reserva INTEGER PRIMARY KEY,
    id_hospede INTEGER NOT NULL,
    id_quarto INTEGER NOT NULL,
    data_checkin DATE NOT NULL,
    data_checkout DATE NOT NULL,
    quantidade_hospedes INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    valor_total NUMERIC(10,2),
    CONSTRAINT ck_datas_reserva
        CHECK (data_checkout > data_checkin),
    CONSTRAINT ck_quantidade_hospedes
        CHECK (quantidade_hospedes > 0),
    CONSTRAINT fk_reserva_hospede
        FOREIGN KEY (id_hospede)
        REFERENCES hospede(id_hospede),
    CONSTRAINT fk_reserva_quarto
        FOREIGN KEY (id_quarto)
        REFERENCES quarto(id_quarto)
);

-- ============================================================
-- FUNCIONÁRIO
-- Usada para exercícios de autorrelacionamento.
-- Um supervisor também é um funcionário.
-- ============================================================

CREATE TABLE funcionario (
    id_funcionario INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(60) NOT NULL,
    salario NUMERIC(10,2) NOT NULL,
    id_supervisor INTEGER,
    CONSTRAINT fk_funcionario_supervisor
        FOREIGN KEY (id_supervisor)
        REFERENCES funcionario(id_funcionario)
);

-- ============================================================
-- POPULAÇÃO - TIPOS DE QUARTO
-- ============================================================

INSERT INTO tipo_quarto
(id_tipo, nome_tipo, valor_diaria, capacidade, descricao)
VALUES
(1, 'Standard', 180.00, 2, 'Quarto econômico para até duas pessoas'),
(2, 'Superior', 260.00, 3, 'Quarto intermediário com espaço adicional'),
(3, 'Luxo', 420.00, 2, 'Quarto de alto padrão com vista privilegiada'),
(4, 'Família', 520.00, 5, 'Quarto amplo para famílias'),
(5, 'Presidencial', 1200.00, 4, 'Suíte premium com sala privativa'),
(6, 'Executivo', 350.00, 2, 'Categoria voltada a viagens corporativas');

-- ============================================================
-- POPULAÇÃO - QUARTOS
-- ============================================================

INSERT INTO quarto
(id_quarto, numero, andar, status, vista, id_tipo)
VALUES
(101, '101', 1, 'Disponível', 'Jardim', 1),
(102, '102', 1, 'Disponível', NULL, 1),
(201, '201', 2, 'Ocupado', 'Cidade', 2),
(202, '202', 2, 'Manutenção', 'Cidade', 2),
(301, '301', 3, 'Disponível', 'Mar', 3),
(302, '302', 3, 'Ocupado', 'Mar', 3),
(401, '401', 4, 'Disponível', 'Piscina', 4),
(402, '402', 4, 'Disponível', NULL, 4),
(501, '501', 5, 'Disponível', 'Mar', 5);

-- Tipo Executivo (6) não possui quarto cadastrado.

-- ============================================================
-- POPULAÇÃO - HÓSPEDES
-- ============================================================

INSERT INTO hospede
(id_hospede, nome, email, cidade, estado, telefone)
VALUES
(1, 'Ana Martins', 'ana@email.com', 'Curitiba', 'PR', '41999990001'),
(2, 'Bruno Lima', 'bruno@email.com', 'Londrina', 'PR', '43999990002'),
(3, 'Carla Souza', 'carla@email.com', 'Curitiba', 'PR', NULL),
(4, 'Diego Alves', 'diego@email.com', NULL, 'SP', '11999990004'),
(5, 'Elisa Rocha', 'elisa@email.com', 'São Paulo', 'SP', '11999990005'),
(6, 'Fábio Melo', 'fabio@email.com', 'Maringá', 'PR', NULL),
(7, 'Gabriela Nunes', 'gabriela@email.com', 'CURITIBA', 'PR', '41999990007'),
(8, 'Henrique Costa', 'henrique@email.com', 'Florianópolis', 'SC', '48999990008'),
(9, 'Isabela Prado', 'isabela@email.com', 'Londrina', 'PR', '43999990009'),
(10, 'João Ribeiro', 'joao@email.com', 'São Paulo', 'SP', '11999990010');

-- Fábio e João não possuem reservas.

-- ============================================================
-- POPULAÇÃO - RESERVAS
-- ============================================================

INSERT INTO reserva
(id_reserva, id_hospede, id_quarto, data_checkin, data_checkout,
 quantidade_hospedes, status, valor_total)
VALUES
(1, 1, 101, '2026-07-10', '2026-07-13', 2, 'Concluída', 540.00),
(2, 1, 301, '2026-08-20', '2026-08-23', 2, 'Concluída', 1260.00),
(3, 2, 201, '2026-08-05', '2026-08-08', 1, 'Concluída', 780.00),
(4, 2, 302, '2026-09-18', '2026-09-21', 2, 'Confirmada', 1260.00),
(5, 3, 102, '2026-06-15', '2026-06-17', 1, 'Concluída', 360.00),
(6, 4, 401, '2026-09-20', '2026-09-24', 4, 'Confirmada', 2080.00),
(7, 5, 301, '2026-05-12', '2026-05-15', 2, 'Concluída', 1260.00),
(8, 5, 501, '2026-10-01', '2026-10-04', 2, 'Confirmada', 3600.00),
(9, 7, 101, '2026-08-01', '2026-08-02', 1, 'Cancelada', 180.00),
(10, 7, 201, '2026-08-14', '2026-08-16', 2, 'Concluída', 520.00),
(11, 8, 402, '2026-07-22', '2026-07-27', 5, 'Concluída', 2600.00),
(12, 9, 102, '2026-09-25', '2026-09-28', 2, 'Confirmada', 540.00),
(13, 3, 301, '2026-09-10', '2026-09-12', 2, 'Concluída', 840.00);

-- Quarto 202 (Manutenção) nunca foi reservado.
-- Há quartos e tipos com situações úteis para LEFT/RIGHT JOIN.

-- ============================================================
-- POPULAÇÃO - FUNCIONÁRIOS
-- ============================================================

INSERT INTO funcionario
(id_funcionario, nome, cargo, salario, id_supervisor)
VALUES
(1, 'Marina Lopes', 'Gerente Geral', 9500.00, NULL),
(2, 'Paulo Mendes', 'Gerente de Hospedagem', 6800.00, 1),
(3, 'Renata Dias', 'Gerente de Operações', 7000.00, 1),
(4, 'Lucas Ferreira', 'Recepcionista', 3200.00, 2),
(5, 'Camila Barros', 'Recepcionista', 3300.00, 2),
(6, 'Rafael Moreira', 'Supervisor de Limpeza', 4100.00, 3),
(7, 'Bianca Freitas', 'Camareira', 2800.00, 6),
(8, 'Eduardo Tavares', 'Manutenção', 3500.00, 3);

-- ============================================================
-- CONSULTAS DE CONFERÊNCIA
-- ============================================================

-- SELECT * FROM tipo_quarto;
-- SELECT * FROM quarto;
-- SELECT * FROM hospede;
-- SELECT * FROM reserva;
-- SELECT * FROM funcionario;
