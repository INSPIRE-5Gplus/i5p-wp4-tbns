    std::map<string, string> clli = {
              {"1", "Barcelona"}, {"2", "Mataró"}, {"3", "Vic"}, {"4", "Manresa"}, {"5", "Vilanova i la Geltrú"}, {"6", "Sabadell"}};
 
            std::map<string, std::pair<float, float>> gps = {{"1", {2.15899, 41.38879}},  // Barcelona
                                                             {"2", {2.4445, 41.54211}},   // Mataró
                                                             {"3", {2.25486, 41.93012}},  // Vic
                                                             {"4", {1.82399, 41.72815}},  // Manresa
                                                             {"5", 1.725633, 41.224199}},  // Vilanova i la Geltrú
                                                             {"6", {2.113898, 41.542101}}}; // Sabadell
 
            // clang-format off
            std::map<string, std::vector<client_portinfo>> node_clientports = {
                {"1", {
                          
                          {13, 2.240927935, 41.774261475,  CS_6_25GHZ, std::nullopt, std::nullopt},  // Hospital Sant Pau
                          {14, 2.1574095, 41.3653259, CS_6_25GHZ, std::nullopt, std::nullopt}, // Estadi Olímpic
                          {15, 2.2002900, 41.3870000, CS_6_25GHZ, std::nullopt, std::nullopt}, // Port Olímpic
                          {17, 2.0790474, 41.2969439, CS_6_25GHZ, std::nullopt, std::nullopt}, // Aeroport
                          {16, 2.1325814, 41.3636994, CS_6_25GHZ, std::nullopt, std::nullopt}, // Ciutat de la Justicia
                          {17, 2.2301443, 41.4123053, CS_6_25GHZ, std::nullopt, std::nullopt}, // Port Besòs
                          {21, 2.16191f, 41.39550f, CS_6_25GHZ, std::nullopt, std::nullopt}, // La Pedrera-Casa Milà
                          {22, 2.17437f, 41.40397f, CS_6_25GHZ, std::nullopt, std::nullopt}, // La Sagrada Familia
                          {23, 2.17670f, 41.38287f, CS_6_25GHZ, std::nullopt, std::nullopt}, // Palau de la Generalitat de Catalunya
                          {24, 2.18863f, 41.38823f, CS_6_25GHZ, std::nullopt, std::nullopt}, // Parlament de Catalunya
                          {25, 2.12286f, 41.38141f, CS_6_25GHZ, std::nullopt, std::nullopt} // Camp Nou
                      }
                },
                {"2", {
                          {13, 2.4450762, 41.5310119, CS_6_25GHZ, std::nullopt, std::nullopt}, // Port Mataró
                          {14, 2.4448946, 41.539828, CS_6_25GHZ, std::nullopt, std::nullopt}, // Ajuntament mataró
                          {15, 2.4349323, 41.528072, CS_6_25GHZ, std::nullopt, std::nullopt}, // TecnoCampus Mataró
                          {17, 2.430846, 41.554998, CS_6_25GHZ, std::nullopt, std::nullopt} // Hospital Mataró
                      }
                },
                {"3", {
                          {11, 2.250452, 41.927211, CS_6_25GHZ, std::nullopt, std::nullopt}, // Hospital Santa Creu
                          {12, 2.244564, 41.930188, CS_6_25GHZ, std::nullopt, std::nullopt}, // El Sucre
                          {13, 2.256896, 41.935722, CS_6_25GHZ, std::nullopt, std::nullopt}, // Seminari de Vic
                          {14, 2.254358, 41.930419, CS_6_25GHZ, std::nullopt, std::nullopt}, // Ajuntament Vic
                          {15, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt},  // D2-D1_A (Estacio Tren)
                          {16, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt},  // D2-D1_B
                          {17, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt},  // D2-D1_C
                          {18, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt},  // D2-D1_D
                          {19, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}  // D2-D1_E
                      }
                },
                {"4", {
                          {13, 1.826862, 41.73738, CS_6_25GHZ, std::nullopt, std::nullopt}, // Zona universitaria
                          {14, 1.826789, 41.722932, CS_6_25GHZ, std::nullopt, std::nullopt}, // Ajuntament Manresa
                          {15, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_A (El Vell Congost)
                          {16, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_B
                          {17, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_C
                          {18, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_D
                          {19, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt} // D2-D3_E
        
                      }
                },
                {"5", {
                          {13, 1.730649, 41.220198, CS_6_25GHZ, std::nullopt, std::nullopt}, // Estació de Tren Vilanova
                          {14, 1.731484, 41.215406, CS_6_25GHZ, std::nullopt, std::nullopt}, // Port
                          {15, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_A (Ajuntament)
                          {16, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_B
                          {17, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_C
                          {18, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_D
                          {19, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt} // D2-D4_E
        
                      }
                },
                {"6", {}}
            };

            // clang-format on
            std::vector<link> links = {
              {"1", "2", 2, 1, 152, {}, CS_6_25GHZ},
              {"1", "3", 3, 1, 152, {}, CS_6_25GHZ},
              {"1", "4", 4, 1, 152, {}, CS_6_25GHZ},
              {"1", "5", 5, 1, 152, {}, CS_6_25GHZ},
              {"1", "6", 6, 1, 152, {}, CS_6_25GHZ},
              {"2", "1", 1, 2, 152, {}, CS_6_25GHZ},
              {"2", "6", 6, 2, 152, {}, CS_6_25GHZ},
              {"3", "1", 1, 3, 152, {}, CS_6_25GHZ},
              {"3", "4", 4, 3, 152, {}, CS_6_25GHZ},
              {"3", "6", 6, 3, 152, {}, CS_6_25GHZ},
              {"4", "1", 1, 4, 152, {}, CS_6_25GHZ},
              {"4", "3", 3, 4, 152, {}, CS_6_25GHZ},
              {"4", "5", 5, 4, 152, {}, CS_6_25GHZ},
              {"5", "1", 1, 5, 152, {}, CS_6_25GHZ},
              {"5", "4", 4, 5, 152, {}, CS_6_25GHZ},
              {"6", "1", 1, 6, 152, {}, CS_6_25GHZ},
              {"6", "2", 2, 6, 152, {}, CS_6_25GHZ},
              {"6", "3", 3, 6, 152, {}, CS_6_25GHZ}
            };