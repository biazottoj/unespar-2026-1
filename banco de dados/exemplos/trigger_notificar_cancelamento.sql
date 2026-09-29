DROP TRIGGER IF EXISTS trg_notificar_cancelamento ON reserva;
DROP FUNCTION IF EXISTS fn_notificar_cancelamento();

CREATE OR REPLACE FUNCTION fn_notificar_cancelamento()
RETURNS TRIGGER
LANGUAGE plpgsql

AS $$
BEGIN

    INSERT INTO notificacao (id_reserva, mensagem)
    VALUES
    (NEW.id_reserva, 'RESERVA ' || NEW.id_reserva || ' foi cancelada.');
    RETURN NEW;

END;
$$;

CREATE TRIGGER trg_notificar_cancelamento
AFTER UPDATE OF status
ON reserva
FOR EACH ROW
WHEN (OLD.status <> 'Cancelada' AND new.status = 'Cancelada')
EXECUTE FUNCTION fn_notificar_cancelamento();    




CREATE OR REPLACE FUNCTION fn_notificar_confirmacao()
RETURNS TRIGGER
LANGUAGE plpgsql

AS $$
BEGIN

    INSERT INTO notificacao (id_reserva, mensagem)
    VALUES
    (NEW.id_reserva, 'RESERVA ' || NEW.id_reserva || ' foi cancelada.');
    RETURN NEW;

END;
$$;


CREATE TRIGGER trg_notificar_confirmacao
AFTER UPDATE OF status
ON reserva
FOR EACH ROW
WHEN (OLD.status <> 'Cancelada' AND new.status = 'Cancelada')
EXECUTE FUNCTION fn_notificar_cancelamento();    
