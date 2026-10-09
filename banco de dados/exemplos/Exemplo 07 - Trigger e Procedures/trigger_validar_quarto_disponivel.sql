DROP TRIGGER IF EXISTS trg_validar_quarto_disponivel ON reserva;
DROP FUNCTION IF EXISTS fn_validar_quarto_disponivel();

CREATE OR REPLACE FUNCTION fn_validar_quarto_disponivel()
RETURNS TRIGGER
LANGUAGE plpgsql

AS $$
DECLARE
    v_status VARCHAR(20);

BEGIN

SELECT status
INTO v_status
FROM quarto
WHERE id_quarto = NEW.id_quarto;

IF v_status IS NULL THEN
    RAISE EXCEPTION
        'Quarto % nao encontrado', NEW.id_quarto;
END IF;

IF v_status != 'Disponível' THEN
    RAISE EXCEPTION
        'Quarto % não disponível', NEW.id_quarto;
END IF;

RETURN NEW;
END;
$$;


CREATE TRIGGER trg_validar_quarto_disponivel
BEFORE INSERT
ON reserva
FOR EACH ROW
EXECUTE FUNCTION fn_validar_quarto_disponivel();