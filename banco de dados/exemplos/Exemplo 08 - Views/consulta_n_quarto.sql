SELECT r.id_reserva,
h.nome as hospede,
q.numero as quarto,
tq.nome_tipo,
r.data_checkin,
r.data_checkout,
r.status,
r.valor_total
FROM reserva as r 
INNER JOIN hospede AS h ON r.id_hospede = h.id_hospede
INNER JOIN quarto as q ON q.id_quarto = r.id_quarto
INNER JOIN tipo_quarto as tq ON tq.id_tipo = q.id_tipo
WHERE q.numero = '401';