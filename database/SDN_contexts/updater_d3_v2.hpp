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
                        {15, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_A1 (Camp d'Esports)
                        {16, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_B1
                        {17, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_C1
                        {18, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_D1
                        {19, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_E1
                        {20, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_F1
                        {21, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_G1
                        {22, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_H1
                        {23, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_I1
                        {24, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_J1
                        {25, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_K1
                        {26, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_L1
                        {27, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_M1
                        {28, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_N1
                        {29, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_O1
                        {30, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_P1
                        {31, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_Q1
                        {32, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_R1
                        {33, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_S1
                        {34, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_T1
                        {35, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_V1
                        {36, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_W1
                        {37, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_X1
                        {38, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_Y1
                        {39, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_Z1
                        {40, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_A2
                        {41, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_B2
                        {42, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_C2
                        {43, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_D2
                        {44, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_E2
                        {45, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_F2
                        {46, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_G2
                        {47, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_H2
                        {48, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_I2
                        {49, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_J2
                        {50, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_K2
                        {51, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_L2
                        {52, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_M2
                        {53, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_N2
                        {54, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_O2
                        {55, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_P2
                        {56, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_Q2
                        {57, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_R2
                        {58, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_S2
                        {59, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_T2
                        {60, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_V2
                        {61, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_W2
                        {62, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_X2
                        {63, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_Y2
                        {64, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_Z2
                        {65, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_A3
                        {66, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_B3
                        {67, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_C3
                        {68, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_D3
                        {69, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_E3
                        {70, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_F3
                        {71, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D4_G3
                        {72, 0.614417, 41.621296, CS_6_25GHZ, std::nullopt, std::nullopt}  // D3-D4_H3
                    }
              },
              {"2", {
                        {13, 1.519713, 41.994169, CS_6_25GHZ, std::nullopt, std::nullopt}, // Catedral Solsona
                        {14, 1.517154, 41.99471, CS_6_25GHZ, std::nullopt, std::nullopt}, // Ajuntament Solsona
                        {15, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_A1 (Estació Autobusos)
                        {16, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_B1
                        {17, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_C1
                        {18, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_D1
                        {19, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_E1
                        {20, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_F1
                        {21, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_G1
                        {22, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_H1
                        {23, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_I1
                        {24, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_J1
                        {25, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_K1
                        {26, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_L1
                        {27, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_M1
                        {28, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_N1
                        {29, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_O1
                        {30, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_P1
                        {31, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_Q1
                        {32, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_R1
                        {33, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_S1
                        {34, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_T1
                        {35, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_V1
                        {36, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_W1
                        {37, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_X1
                        {38, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_Y1
                        {39, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_Z1
                        {40, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_A2
                        {41, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_B2
                        {42, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_C2
                        {43, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_D2
                        {44, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_E2
                        {45, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_F2
                        {46, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_G2
                        {47, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_H2
                        {48, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_I2
                        {49, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_J2
                        {50, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_K2
                        {51, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_L2
                        {52, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_M2
                        {53, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_N2
                        {54, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_O2
                        {55, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_P2
                        {56, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_Q2
                        {57, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_R2
                        {58, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_S2
                        {59, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_T2
                        {60, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_V2
                        {61, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_W2
                        {62, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_X2
                        {63, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_Y2
                        {64, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_Z2
                        {65, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_A3
                        {66, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_B3
                        {67, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_C3
                        {68, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_D3
                        {69, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_E3
                        {70, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_F3
                        {71, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D2_G3
                        {72, 1.515932, 41.996128, CS_6_25GHZ, std::nullopt, std::nullopt}  // D3-D2_H3
                    }
              },
              {"3", {
                        {13, 1.411231, 42.34281, CS_6_25GHZ, std::nullopt, std::nullopt}, // Aeroport Seu urgell
                        {14, 1.462059, 42.357637, CS_6_25GHZ, std::nullopt, std::nullopt}, // Catedral
                        {15, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_A1 (Ajuntament)
                        {16, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_B1
                        {17, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_C1
                        {18, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_D1
                        {19, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_E1
                        {20, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_F1
                        {21, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_G1
                        {22, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_H1
                        {23, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_I1
                        {24, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_J1
                        {25, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_K1
                        {26, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_L1
                        {27, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_M1
                        {28, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_N1
                        {29, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_O1
                        {30, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_P1
                        {31, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_Q1
                        {32, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_R1
                        {33, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_S1
                        {34, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_T1
                        {35, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_V1
                        {36, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_W1
                        {37, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_X1
                        {38, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_Y1
                        {39, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_Z1
                        {40, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_A2
                        {41, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_B2
                        {42, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_C2
                        {43, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_D2
                        {44, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_E2
                        {45, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_F2
                        {46, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_G2
                        {47, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_H2
                        {48, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_I2
                        {49, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_J2
                        {50, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_K2
                        {51, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_L2
                        {52, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_M2
                        {53, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_N2
                        {54, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_O2
                        {55, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_P2
                        {56, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_Q2
                        {57, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_R2
                        {58, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_S2
                        {59, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_T2
                        {60, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_V2
                        {61, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_W2
                        {62, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_X2
                        {63, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_Y2
                        {64, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_Z2
                        {65, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_A3
                        {66, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_B3
                        {67, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_C3
                        {68, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_D3
                        {69, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_E3
                        {70, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_F3
                        {71, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}, // D3-D1_G3
                        {72, 1.462526, 42.357916, CS_6_25GHZ, std::nullopt, std::nullopt}  // D3-D1_H3
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