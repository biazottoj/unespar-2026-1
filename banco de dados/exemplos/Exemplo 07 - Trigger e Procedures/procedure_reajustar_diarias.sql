DROP PROCEDURE IF EXISTS sp_reajustar_diarias(numeric,integer);

CREATE OR REPLACE PROCEDURE sp_reajustar_diarias(
    p_percentual NUMERIC,
    p_id_tipo INTEGER DEFAULT NULL)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_percentual <= -100 THEN
        RAISE EXCEPTION 'PERCENTUAL INVALIDO';
    END IF;

    UPDATE tipo_quarto
    SET valor_diaria = ROUND(valor_diaria * (1 + p_percentual/100), 2)
    WHERE p_id_tipo is NULL OR id_tipo = p_id_tipo;

    RAISE NOTICE 'REAJUSTE APLICADO';
END;
$$;