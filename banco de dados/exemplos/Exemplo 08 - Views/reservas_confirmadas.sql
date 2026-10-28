CREATE OR REPLACE VIEW vw_reservas_confirmadas AS 

SELECT * FROM vw_reservas_detalhadas 
WHERE status = 'Confirmada';