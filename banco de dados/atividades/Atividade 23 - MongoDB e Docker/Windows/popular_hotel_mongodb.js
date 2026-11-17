// POPULAÇÃO DO BANCO HOTEL_NOSQL — MongoDB / mongosh
// Compatível com o estudo guiado "Do zero ao MongoDB com Docker".
//
// Coleções: hospedes (6), quartos (6), reservas (6).
// Este script pode ser executado mais de uma vez:
// - insere os documentos de exemplo que ainda NÃO existem;
// - preserva documentos já existentes, sem sobrescrever alterações de alunos.
//
// Execute dentro do contêiner MongoDB, usando o mongosh:
//   load("/tmp/carga_inicial_hotel_nosql_recriada.js");
//
// ATENÇÃO: este é um banco fictício para atividades didáticas.

(function popularHotelNoSQL() {
  const hotel = db.getSiblingDB("hotel_nosql");

  // ---------------------------------------------------------------------------
  // 1. HÓSPEDES — documentos com objeto aninhado (contato) e array (tags).
  // ---------------------------------------------------------------------------
  const hospedes = [
    {
      _id: 1, nome: "Ana Martins", cidade: "Curitiba", estado: "PR",
      contato: { email: "ana@exemplo.com", telefone: "41999990001" },
      tags: ["frequente", "corporativo"]
    },
    {
      _id: 2, nome: "Bruno Lima", cidade: "Londrina", estado: "PR",
      contato: { email: "bruno@exemplo.com" },
      tags: ["lazer"]
    },
    {
      _id: 3, nome: "Carla Souza", cidade: "Curitiba", estado: "PR",
      contato: { email: "carla@exemplo.com" },
      tags: ["familia"]
    },
    {
      _id: 4, nome: "Diego Alves", cidade: "São Paulo", estado: "SP",
      contato: { email: "diego@exemplo.com" },
      tags: ["corporativo"]
    },
    {
      _id: 5, nome: "Elisa Rocha", cidade: "Maringá", estado: "PR",
      contato: { email: "elisa@exemplo.com" },
      tags: []
    },
    {
      _id: 6, nome: "Fábio Melo", cidade: "Curitiba", estado: "PR",
      contato: { email: "fabio@exemplo.com" },
      tags: ["novo"]
    }
  ];

  // ---------------------------------------------------------------------------
  // 2. QUARTOS — cada documento contém tipo, capacidade, diária e amenidades.
  // ---------------------------------------------------------------------------
  const quartos = [
    {
      _id: 101, numero: "101", tipo: "Standard", andar: 1,
      capacidade: 2, diaria: 180, status: "Disponível",
      amenidades: ["wifi", "tv"]
    },
    {
      _id: 102, numero: "102", tipo: "Standard", andar: 1,
      capacidade: 2, diaria: 180, status: "Ocupado",
      amenidades: ["wifi"]
    },
    {
      _id: 201, numero: "201", tipo: "Superior", andar: 2,
      capacidade: 3, diaria: 260, status: "Disponível",
      amenidades: ["wifi", "frigobar"]
    },
    {
      _id: 202, numero: "202", tipo: "Superior", andar: 2,
      capacidade: 3, diaria: 260, status: "Disponível",
      amenidades: ["wifi", "tv"]
    },
    {
      _id: 301, numero: "301", tipo: "Luxo", andar: 3,
      capacidade: 2, diaria: 420, status: "Disponível",
      amenidades: ["wifi", "tv"]
    },
    {
      _id: 401, numero: "401", tipo: "Família", andar: 4,
      capacidade: 5, diaria: 520, status: "Manutenção",
      amenidades: ["wifi", "cozinha"]
    }
  ];

  // ---------------------------------------------------------------------------
  // 3. RESERVAS — hospedeId e quartoId referenciam documentos por convenção.
  //    ISODate registra datas com o tipo Date do MongoDB (BSON).
  // ---------------------------------------------------------------------------
  const reservas = [
    {
      _id: 1001, hospedeId: 1, quartoId: 101,
      checkin: ISODate("2026-10-01T00:00:00Z"),
      checkout: ISODate("2026-10-03T00:00:00Z"),
      status: "Concluída", qtdHospedes: 2, valorTotal: 360,
      servicos: [{ nome: "cafe_da_manha", valor: 40 }]
    },
    {
      _id: 1002, hospedeId: 2, quartoId: 201,
      checkin: ISODate("2026-12-10T00:00:00Z"),
      checkout: ISODate("2026-12-12T00:00:00Z"),
      status: "Confirmada", qtdHospedes: 2, valorTotal: 520,
      servicos: []
    },
    {
      _id: 1003, hospedeId: 1, quartoId: 301,
      checkin: ISODate("2026-12-20T00:00:00Z"),
      checkout: ISODate("2026-12-23T00:00:00Z"),
      status: "Confirmada", qtdHospedes: 2, valorTotal: 1260,
      servicos: [{ nome: "estacionamento", valor: 60 }]
    },
    {
      _id: 1004, hospedeId: 3, quartoId: 401,
      checkin: ISODate("2026-09-01T00:00:00Z"),
      checkout: ISODate("2026-09-04T00:00:00Z"),
      status: "Concluída", qtdHospedes: 4, valorTotal: 1560,
      servicos: []
    },
    {
      _id: 1005, hospedeId: 5, quartoId: 102,
      checkin: ISODate("2026-12-15T00:00:00Z"),
      checkout: ISODate("2026-12-16T00:00:00Z"),
      status: "Cancelada", qtdHospedes: 1, valorTotal: 180,
      servicos: []
    },
    {
      _id: 1006, hospedeId: 4, quartoId: 202,
      checkin: ISODate("2026-12-28T00:00:00Z"),
      checkout: ISODate("2026-12-30T00:00:00Z"),
      status: "Confirmada", qtdHospedes: 1, valorTotal: 520,
      servicos: []
    }
  ];

  // Usa upsert + $setOnInsert para permitir reexecução sem duplicar
  // registros e sem reverter alterações feitas durante as atividades.
  function inserirAusentes(nomeColecao, documentos) {
    let inseridos = 0;
    for (const documento of documentos) {
      const resultado = hotel.getCollection(nomeColecao).updateOne(
        { _id: documento._id },
        { $setOnInsert: documento },
        { upsert: true }
      );
      if (resultado.upsertedCount === 1) {
        inseridos++;
      }
    }
    print(nomeColecao + ": " + inseridos + " novo(s) registro(s)");
  }

  inserirAusentes("hospedes", hospedes);
  inserirAusentes("quartos", quartos);
  inserirAusentes("reservas", reservas);

  print("\nBANCO: " + hotel.getName());
  print("Total de hóspedes: " + hotel.hospedes.countDocuments({}));
  print("Total de quartos: " + hotel.quartos.countDocuments({}));
  print("Total de reservas: " + hotel.reservas.countDocuments({}));
  print("Carga finalizada! Nenhum registro existente foi sobrescrito.");
})();
