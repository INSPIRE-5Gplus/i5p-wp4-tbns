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
                          {15, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_A1 (Hospital de la Selva)
                          {16, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_B1
                          {17, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_C1
                          {18, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_D1
                          {19, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_E1
                          {20, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_F1
                          {21, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_G1
                          {22, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_H1
                          {23, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_I1
                          {24, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_J1
                          {25, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_K1
                          {26, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_L1
                          {27, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_M1
                          {28, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_N1
                          {29, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_O1
                          {30, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_P1
                          {31, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_Q1
                          {32, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_R1
                          {33, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_S1
                          {34, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_T1
                          {35, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_V1
                          {36, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_W1
                          {37, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_X1
                          {38, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_Y1
                          {39, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_Z1
                          {40, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_A2
                          {41, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_B2
                          {42, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_C2
                          {43, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_D2
                          {44, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_E2
                          {45, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_F2
                          {46, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_G2
                          {47, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_H2
                          {48, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_I2
                          {49, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_J2
                          {50, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_K2
                          {51, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_L2
                          {52, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_M2
                          {53, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_N2
                          {54, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_O2
                          {55, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_P2
                          {56, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_Q2
                          {57, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_R2
                          {58, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_S2
                          {59, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_T2
                          {60, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_V2
                          {61, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_W2
                          {62, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_X2
                          {63, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_Y2
                          {64, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_Z2
                          {65, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_A3
                          {66, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_B3
                          {67, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_C3
                          {68, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_D3
                          {69, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_E3
                          {70, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_F3
                          {71, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D2_G3
                          {72, 2.802401, 41.686493, CS_6_25GHZ, std::nullopt, std::nullopt}  // D1-D2_H3
                      }
                },
                {"3", {
                          {13, 2.190828, 42.20103, CS_6_25GHZ, std::nullopt, std::nullopt}, // Monestir Sta. Maria
                          {14, 2.192365, 42.199549, CS_6_25GHZ, std::nullopt, std::nullopt}, // Centre Cívic
                          {15, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_A1 (Estacio Tren)
                          {16, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_B1
                          {17, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_C1
                          {18, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_D1
                          {19, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_E1
                          {20, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_F1
                          {21, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_G1
                          {22, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_H1
                          {23, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_I1
                          {24, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_J1
                          {25, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_K1
                          {26, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_L1
                          {27, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_M1
                          {28, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_N1
                          {29, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_O1
                          {30, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_P1
                          {31, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_Q1
                          {32, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_R1
                          {33, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_S1
                          {34, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_T1
                          {35, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_V1
                          {36, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_W1
                          {37, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_X1
                          {38, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_Y1
                          {39, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_Z1
                          {40, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_A2
                          {41, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_B2
                          {42, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_C2
                          {43, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_D2
                          {44, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_E2
                          {45, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_F2
                          {46, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_G2
                          {47, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_H2
                          {48, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_I2
                          {49, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_J2
                          {50, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_K2
                          {51, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_L2
                          {52, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_M2
                          {53, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_N2
                          {54, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_O2
                          {55, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_P2
                          {56, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_Q2
                          {57, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_R2
                          {58, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_S2
                          {59, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_T2
                          {60, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_V2
                          {61, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_W2
                          {62, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_X2
                          {63, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_Y2
                          {64, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_Z2
                          {65, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_A3
                          {66, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_B3
                          {67, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_C3
                          {68, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_D3
                          {69, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_E3
                          {70, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_F3
                          {71, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D1-D3_G3
                          {72, 2.195744, 42.196095, CS_6_25GHZ, std::nullopt, std::nullopt}  // D1-D3_H3
                      }
                },
                {"4", {}},
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