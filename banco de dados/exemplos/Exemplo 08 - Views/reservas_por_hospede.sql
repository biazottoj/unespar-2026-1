CREATE VIEW vw_resumo_hospedes AS 
SELECT h.nome,
h.id_hospede,
COUNT(r.id_reserva),
COALESCE(SUM(r.valor_total), 0) AS total_gasto,
COALESCE(AVG(r.valor_total), 0) AS media_reserva
FROM hospede as h
INNER JOIN reserva as r ON h.id_hospede = r.id_hospede
GROUP BY h.id_hospede, h.nome; 