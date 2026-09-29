DROP PROCEDURE IF EXISTS sp_criar_reserva(INTEGER, INTEGER, DATE, DATE, INTEGER);

CREATE OR REPLACE PROCEDURE sp_criar_reserva(
    p_id_hospede INTEGER,
    p_id_quarto INTEGER,
    p_checkin DATE,
    p_checkout DATE,
    p_quantidade_hospedes INTEGER)

LANGUAGE plpgsql
AS $$
BEGIN

    INSERT INTO reserva 
    (id_hospede, id_quarto, data_checkin, data_checkout, quantidade_hospedes, status)
    VALUES
    (p_id_hospede, p_id_quarto, p_checkin, p_checkout, p_quantidade_hospedes, 'Confirmada');

    RAISE NOTICE 'RESERVA CADASTRADA COM SUCESSO.';
END;
$$;