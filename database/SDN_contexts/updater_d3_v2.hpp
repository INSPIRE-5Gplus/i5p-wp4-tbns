    std::map<string, string> clli = {
              {"1", "Lleida"}, {"2", "Solsona"}, {"3", "Seu d'Urgell"}, {"4", "Tremp"}};
 
            std::map<string, std::pair<float, float>> gps = {{"1", {0.626784, 41.614761}},  // Lleida
                                                             {"2", {1.518404, 41.994576}},  // Solsona
                                                             {"3", {1.456007, 42.357572}},  // Seu d'Urgell
                                                             {"4", {0.894618, 42.166368}}}; // Tremp
 
            // clang-format off
            std::map<string, std::vector<client_portinfo>> node_clientports = {
                {"1", {
                          
                          {13, 0.626392, 41.617779,  CS_6_25GHZ, std::nullopt, std::nullopt},  // La Seu Vella
                          {14, 0.613214, 41.62653, CS_6_25GHZ, std::nullopt, std::nullopt}, // Hospital Arnau de Vilanova
                          {15, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_A (Camp d'Esports)
                          {16, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_B
                          {17, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_C
                          {18, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_D
                          {19, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt} // D3-D4_E
                      }
                },
                {"2", {
                          {13, 1.519713, 41.994169, CS_6_25GHZ, std::nullopt, std::nullopt}, // Catedral Solsona
                          {14, 1.517154, 41.99471, CS_6_25GHZ, std::nullopt, std::nullopt}, // Ajuntament Solsona
                          {15, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_A (Estació Autobusos)
                          {16, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_B
                          {17, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_C
                          {18, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_D
                          {19, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt} // D3-D2_E
                      }
                },
                {"3", {
                          {13, 1.411231, 42.34281, CS_6_25GHZ, std::nullopt, std::nullopt}, // Aeroport Seu urgell
                          {14, 1.462059, 42.357637, CS_6_25GHZ, std::nullopt, std::nullopt}, // Catedral
                          {15, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_A (Ajuntament)
                          {16, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_B
                          {17, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_C
                          {18, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_D
                          {19, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt} // D3-D1_E
                      }
                },
                {"4", {}}
            };

            // clang-format on
            std::vector<link> links = {
              {"1", "2", 2, 1, 152, {}, CS_6_25GHZ},
              {"1", "4", 4, 1, 152, {}, CS_6_25GHZ},
              {"2", "1", 1, 2, 152, {}, CS_6_25GHZ},
              {"2", "3", 3, 2, 152, {}, CS_6_25GHZ},
              {"2", "4", 4, 2, 152, {}, CS_6_25GHZ},
              {"3", "2", 2, 3, 152, {}, CS_6_25GHZ},
              {"3", "4", 4, 3, 152, {}, CS_6_25GHZ},
              {"4", "1", 1, 4, 152, {}, CS_6_25GHZ},
              {"4", "2", 2, 4, 152, {}, CS_6_25GHZ},
              {"4", "3", 3, 4, 152, {}, CS_6_25GHZ}
            };