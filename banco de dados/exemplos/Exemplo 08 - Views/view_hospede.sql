CREATE OR REPLACE VIEW vw_hospedes_pr AS

SELECT 
id_hospede, 
nome,
email,
cidade,
estado, 
telefone
FROM hospede
WHERE estado = 'PR';