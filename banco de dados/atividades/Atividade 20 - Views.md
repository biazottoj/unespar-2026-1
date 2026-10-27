# Atividade — Views no PostgreSQL

## Contexto

Utilize o banco de dados do sistema de reservas de hotel utilizado nas aulas.

A atividade tem como objetivo praticar:

- criação de views;
- consultas sobre views;
- views com filtros;
- views envolvendo `JOIN`;
- views com agregação;
- manutenção de views;
- análise de vantagens e limitações.

---

# Parte I — Reconhecimento

## Exercício 1

Liste todas as views existentes no banco utilizando um comando do `psql`.

Depois, liste as mesmas views utilizando `information_schema.views`.

---

## Exercício 2

Explique com suas palavras a diferença entre:

```text
tabela
view
```

---

## Exercício 3

Explique duas vantagens de utilizar views em um banco de dados.

---

# Parte II — Views simples

## Exercício 4

Crie uma view chamada `vw_quartos_disponiveis`.

Ela deve apresentar:

- id do quarto;
- número;
- andar;
- vista;
- status.

A view deve conter apenas quartos com status `Disponível`.

Depois consulte todos os registros da view.

---

## Exercício 5

Utilizando `vw_quartos_disponiveis`, liste apenas quartos a partir do terceiro andar.

Ordene pelo número do quarto.

---

## Exercício 6

Crie uma view `vw_hospedes_pr` contendo hóspedes cujo estado seja `PR`.

Mostre:

- id;
- nome;
- cidade;
- email.

---

## Exercício 7

Consulte `vw_hospedes_pr` mostrando apenas hóspedes de Curitiba.

---

# Parte III — Views com JOIN

## Exercício 8

Crie `vw_quartos_com_tipo`.

A view deve apresentar:

- id do quarto;
- número;
- andar;
- status;
- tipo do quarto;
- capacidade;
- valor da diária.

Utilize `INNER JOIN`.

---

## Exercício 9

A partir de `vw_quartos_com_tipo`, liste quartos cuja diária seja superior a `300.00`.

Ordene do maior para o menor valor.

---

## Exercício 10

Crie `vw_reservas_detalhadas`.

Ela deve combinar:

```text
reserva
hospede
quarto
tipo_quarto
```

Apresente:

- id da reserva;
- hóspede;
- quarto;
- tipo;
- check-in;
- checkout;
- quantidade de hóspedes;
- status;
- valor total.

---

## Exercício 11

Utilizando apenas `vw_reservas_detalhadas`, liste reservas com status `Confirmada`.

---

## Exercício 12

Utilizando apenas `vw_reservas_detalhadas`, liste reservas com valor superior a `1000.00`.

Ordene do maior para o menor valor.

---

# Parte IV — Views com agregação

## Exercício 13

Crie `vw_resumo_hospedes`.

Ela deve apresentar uma linha por hóspede contendo:

- id;
- nome;
- quantidade de reservas;
- total gasto;
- média do valor das reservas.

Hóspedes sem reservas também devem aparecer.

---

## Exercício 14

Utilizando `vw_resumo_hospedes`, liste hóspedes que possuem pelo menos duas reservas.

---

## Exercício 15

Utilizando `vw_resumo_hospedes`, apresente os cinco hóspedes com maior total gasto.

---

## Exercício 16

Crie `vw_reservas_por_status`.

A view deve apresentar:

- status;
- quantidade de reservas;
- soma dos valores;
- média dos valores.

---

## Exercício 17

Consulte `vw_reservas_por_status` ordenando da maior para a menor quantidade de reservas.

---

## Exercício 18

Crie `vw_faturamento_tipo_quarto`.

Ela deve apresentar:

- tipo do quarto;
- quantidade de reservas;
- faturamento total;
- valor médio das reservas.

Tipos de quarto sem reservas também devem aparecer.

---

# Parte V — Views para ausência de relacionamento

## Exercício 19

Crie `vw_hospedes_sem_reserva` contendo apenas hóspedes que nunca fizeram uma reserva.

Utilize `LEFT JOIN`.

---

## Exercício 20

Crie `vw_quartos_sem_reserva` contendo quartos que nunca participaram de uma reserva.

---

## Exercício 21

Crie `vw_tipos_sem_quarto` contendo tipos de quarto que não possuem nenhum quarto cadastrado.

---

# Parte VI — Manutenção de Views

## Exercício 22

Utilize `CREATE OR REPLACE VIEW` para alterar `vw_quartos_disponiveis`.

Além das colunas anteriores, a view deve apresentar:

- nome do tipo;
- valor da diária;
- capacidade.

---

## Exercício 23

Consulte a estrutura da view atualizada utilizando comandos do PostgreSQL/`psql`.

---

## Exercício 24

Crie uma view temporária de exercício chamada `vw_teste`.

Depois remova utilizando `DROP VIEW`.

---

## Exercício 25

Repita a remoção utilizando `DROP VIEW IF EXISTS`.

Explique a vantagem do uso de `IF EXISTS`.

---

# Parte VII — Views atualizáveis

## Exercício 26

Crie `vw_hospedes_curitiba` com os registros da tabela `hospede` cuja cidade seja `Curitiba`.

Inclua as colunas necessárias para identificar e atualizar um hóspede.

---

## Exercício 27

Tente alterar o telefone de um hóspede através de `vw_hospedes_curitiba`.

Depois consulte diretamente a tabela `hospede`.

Explique o resultado.

---

## Exercício 28

Recrie `vw_hospedes_curitiba` utilizando `WITH CHECK OPTION`.

Depois tente alterar a cidade de um hóspede de `Curitiba` para `Londrina` através da view.

Observe e explique o comportamento.

---

# Parte VIII — Views e segurança

## Exercício 29

Crie `vw_funcionarios_publico` apresentando:

- id;
- nome;
- cargo;
- supervisor.

Não apresente o salário.

Explique como essa view poderia contribuir para o controle de acesso aos dados.

---

# Parte IX — Análise conceitual

## Exercício 30

Explique a diferença entre `view` e `subconsulta`.

---

## Exercício 31

Explique por que uma view com `GROUP BY`, `COUNT` e `SUM` normalmente não pode ser atualizada diretamente da mesma maneira que uma view simples.

---

## Exercício 32

Explique o que acontece com o resultado de uma view quando os dados das tabelas utilizadas por ela são alterados.

---

## Exercício 33

Explique uma situação em que criar uma view seria desnecessário.

---

## Exercício 34

Explique um possível problema de um banco que possua muitas views dependendo umas das outras.

---

## Exercício 35

Explique a diferença básica entre `VIEW` e `MATERIALIZED VIEW`.

---

# Parte X — Desafio integrador

## Exercício 36

Crie uma view chamada `vw_dashboard_hotel`.

Ela deve apresentar uma linha por tipo de quarto contendo:

- nome do tipo;
- quantidade de quartos cadastrados;
- quantidade de quartos disponíveis;
- quantidade total de reservas;
- quantidade de reservas confirmadas;
- faturamento total;
- valor médio das reservas.

Tipos de quarto sem reservas devem continuar aparecendo.

Depois utilize a view para:

1. ordenar os tipos por faturamento;
2. mostrar apenas tipos com pelo menos uma reserva;
3. identificar o tipo com maior faturamento;
4. identificar tipos sem reservas.

Ao final, explique quais partes da consulta ficaram escondidas dentro da view e por que isso facilita a criação de novos relatórios.

## Entrega 

Entrega via link: [https://forms.gle/e3EoJS4bQs7r6GBC8](https://forms.gle/e3EoJS4bQs7r6GBC8)

Entrega ate 03/11/2026