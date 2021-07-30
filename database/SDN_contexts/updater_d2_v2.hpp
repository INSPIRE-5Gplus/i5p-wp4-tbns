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
                        {15, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_A1 (Estacio Tren)
                        {16, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_B1
                        {17, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_C1
                        {18, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_D1
                        {19, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_E1
                        {20, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_F1
                        {21, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_G1
                        {22, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_H1
                        {23, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_I1
                        {24, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_J1
                        {25, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_K1
                        {26, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_L1
                        {27, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_M1
                        {28, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_N1
                        {29, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_O1
                        {30, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_P1
                        {31, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_Q1
                        {32, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_R1
                        {33, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_S1
                        {34, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_T1
                        {35, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_V1
                        {36, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_W1
                        {37, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_X1
                        {38, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_Y1
                        {39, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_Z1
                        {40, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_A2
                        {41, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_B2
                        {42, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_C2
                        {43, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_D2
                        {44, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_E2
                        {45, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_F2
                        {46, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_G2
                        {47, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_H2
                        {48, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_I2
                        {49, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_J2
                        {50, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_K2
                        {51, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_L2
                        {52, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_M2
                        {53, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_N2
                        {54, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_O2
                        {55, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_P2
                        {56, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_Q2
                        {57, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_R2
                        {58, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_S2
                        {59, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_T2
                        {60, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_V2
                        {61, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_W2
                        {62, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_X2
                        {63, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_Y2
                        {64, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_Z2
                        {65, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_A3
                        {66, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_B3
                        {67, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_C3
                        {68, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_D3
                        {69, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_E3
                        {70, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_F3
                        {71, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D1_G3
                        {72, 2.248772, 41.930926, CS_6_25GHZ, std::nullopt, std::nullopt}  // D2-D1_H3
                      }
                },
                {"4", {
                        {13, 1.826862, 41.73738, CS_6_25GHZ, std::nullopt, std::nullopt}, // Zona universitaria
                        {14, 1.826789, 41.722932, CS_6_25GHZ, std::nullopt, std::nullopt}, // Ajuntament Manresa
                        {15, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_A (El Vell Congost)
                        {16, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_B1
                        {17, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_C1
                        {18, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_D1
                        {19, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_E1
                        {20, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_F1
                        {21, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_G1
                        {22, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_H1
                        {23, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_I1
                        {24, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_J1
                        {25, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_K1
                        {26, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_L1
                        {27, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_M1
                        {28, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_N1
                        {29, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_O1
                        {30, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_P1
                        {31, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_Q1
                        {32, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_R1
                        {33, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_S1
                        {34, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_T1
                        {35, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_V1
                        {36, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_W1
                        {37, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_X1
                        {38, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_Y1
                        {39, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_Z1
                        {40, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_A2
                        {41, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_B2
                        {42, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_C2
                        {43, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_D2
                        {44, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_E2
                        {45, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_F2
                        {46, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_G2
                        {47, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_H2
                        {48, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_I2
                        {49, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_J2
                        {50, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_K2
                        {51, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_L2
                        {52, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_M2
                        {53, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_N2
                        {54, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_O2
                        {55, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_P2
                        {56, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_Q2
                        {57, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_R2
                        {58, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_S2
                        {59, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_T2
                        {60, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_V2
                        {61, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_W2
                        {62, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_X2
                        {63, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_Y2
                        {64, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_Z2
                        {65, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_A3
                        {66, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_B3
                        {67, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_C3
                        {68, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_D3
                        {69, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_E3
                        {70, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_F3
                        {71, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D3_G3
                        {72, 1.811321, 41.726004, CS_6_25GHZ, std::nullopt, std::nullopt}  // D2-D3_H3
                      }
                },
                {"5", {
                        {13, 1.730649, 41.220198, CS_6_25GHZ, std::nullopt, std::nullopt}, // Estació de Tren Vilanova
                        {14, 1.731484, 41.215406, CS_6_25GHZ, std::nullopt, std::nullopt}, // Port
                        {15, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_A (Ajuntament)
                        {16, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_B1
                        {17, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_C1
                        {18, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_D1
                        {19, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_E1
                        {20, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_F1
                        {21, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_G1
                        {22, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_H1
                        {23, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_I1
                        {24, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_J1
                        {25, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_K1
                        {26, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_L1
                        {27, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_M1
                        {28, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_N1
                        {29, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_O1
                        {30, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_P1
                        {31, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_Q1
                        {32, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_R1
                        {33, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_S1
                        {34, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_T1
                        {35, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_V1
                        {36, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_W1
                        {37, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_X1
                        {38, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_Y1
                        {39, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_Z1
                        {40, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_A2
                        {41, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_B2
                        {42, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_C2
                        {43, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_D2
                        {44, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_E2
                        {45, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_F2
                        {46, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_G2
                        {47, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_H2
                        {48, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_I2
                        {49, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_J2
                        {50, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_K2
                        {51, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_L2
                        {52, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_M2
                        {53, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_N2
                        {54, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_O2
                        {55, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_P2
                        {56, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_Q2
                        {57, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_R2
                        {58, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_S2
                        {59, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_T2
                        {60, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_V2
                        {61, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_W2
                        {62, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_X2
                        {63, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_Y2
                        {64, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_Z2
                        {65, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_A3
                        {66, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_B3
                        {67, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_C3
                        {68, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_D3
                        {69, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_E3
                        {70, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_F3
                        {71, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}, // D2-D4_G3
                        {72, 1.726008, 41.224095, CS_6_25GHZ, std::nullopt, std::nullopt}  // D2-D4_H3
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