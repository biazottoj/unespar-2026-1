DROP PROCEDURE IF EXISTS sp_processar_notificacao(INTEGER);

CREATE OR REPLACE PROCEDURE sp_processar_notificacao(
    p_id_notificacao BIGINT)

LANGUAGE plpgsql

AS $$
BEGIN

UPDATE notificacao
SET processada = TRUE
WHERE id_notificacao = p_id_notificacao;

IF NOT FOUND THEN
    RAISE EXCEPTION
        'Notificaco % não encontrada', p_id_notificacao;
END IF;

RAISE NOTICE
    'Notificaco % marcada como processada.', p_id_notificacao;

END
$$;