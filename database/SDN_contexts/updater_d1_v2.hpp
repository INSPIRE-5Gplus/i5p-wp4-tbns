    std::map<string, string> clli = {
              {"1", "Figueres"}, {"2", "Blanes"}, {"3", "Ripoll"}, {"4", "St. Feliu de Guíxols"}, {"5", "Girona"}};
 
            std::map<string, std::pair<float, float>> gps = {{"1", {2.963843, 42.266631}},  // Figueres
                                                             {"2", {2.793239, 41.675618}},   // Blanes
                                                             {"3", {2.19325, 42.198239}},  // Ripoll
                                                             {"4", {3.02832, 41.783883}},  // St. Feliu de Guíxols
                                                             {"5", {2.819944, 41.979301}}}; // Girona
 
            // clang-format off
            std::map<string, std::vector<client_portinfo>> node_clientports = {
                {"1", {
                          {13, 2.968713, 42.265095,  CS_6_25GHZ, std::nullopt, std::nullopt},  // Estació Tren
                          {14, 2.95968, 42.267931, CS_6_25GHZ, std::nullopt, std::nullopt}, // Museu Dalí
                          {15, 2.960315, 42.267363, CS_6_25GHZ, std::nullopt, std::nullopt} // Ajuntament Figueres
                      }
                },
                {"2", {
                          {13, 2.799083, 41.67362, CS_6_25GHZ, std::nullopt, std::nullopt}, // Port Blanes
                          {14, 2.792101, 41.674029, CS_6_25GHZ, std::nullopt, std::nullopt}, // Ajuntament Blanes
                          {15, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_A (Hospital de la Selva)
                          {16, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_B
                          {17, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_C
                          {18, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_D
                          {19, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}  // D1-D2_E
                      }
                },
                {"3", {
                          {13, 2.190828, 42.20103, CS_6_25GHZ, std::nullopt, std::nullopt}, // Monestir Sta. Maria
                          {14, 2.192365, 42.199549, CS_6_25GHZ, std::nullopt, std::nullopt}, // Centre Cívic
                          {15, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_A (Estacio Tren)
                          {16, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_B
                          {17, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_C
                          {18, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_D
                          {19, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt} // D1-D3_E
                      }
                },
                {"4", {},
                {"5", {}}
            };

            // clang-format on
            std::vector<link> links = {
              {"1", "3", 3, 1, 152, {}, CS_6_25GHZ},
              {"1", "5", 5, 1, 152, {}, CS_6_25GHZ},
              {"2", "3", 3, 2, 152, {}, CS_6_25GHZ},
              {"2", "4", 4, 2, 152, {}, CS_6_25GHZ},
              {"3", "1", 1, 3, 152, {}, CS_6_25GHZ},
              {"3", "2", 2, 3, 152, {}, CS_6_25GHZ},
              {"3", "5", 5, 3, 152, {}, CS_6_25GHZ},
              {"4", "2", 2, 4, 152, {}, CS_6_25GHZ},
              {"4", "5", 5, 4, 152, {}, CS_6_25GHZ},
              {"5", "1", 1, 5, 152, {}, CS_6_25GHZ},
              {"5", "3", 3, 5, 152, {}, CS_6_25GHZ},
              {"5", "4", 4, 5, 152, {}, CS_6_25GHZ}
            };