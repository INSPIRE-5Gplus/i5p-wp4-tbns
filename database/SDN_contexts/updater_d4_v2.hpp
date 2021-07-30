std::map<string, string> clli = {
          {"1", "Tarragona"}, {"2", "Mora d'Ebre"}, {"3", "Tortosa"}};

std::map<string, std::pair<float, float>> gps = {{"1", {1.254606, 41.117236}},  // Tarragona
                                                  {"2", {0.641289, 41.089337}},  // Mora d'Ebre
                                                  {"3", {0.520933, 40.811016}}}; // Tortosa

// clang-format off
std::map<string, std::vector<client_portinfo>> node_clientports = {
    {"1", {
            {13, 1.252812, 41.111331, CS_6_25GHZ, std::nullopt, std::nullopt},  // Estació Trens Tarragona
            {14, 1.238516, 41.124461, CS_6_25GHZ, std::nullopt, std::nullopt}, // Hospital Joan XXIII
            {15, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_A1 (Port tarragona)
            {16, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_B1
            {17, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_C1
            {18, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_D1
            {19, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_E1
            {20, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_F1
            {21, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_G1
            {22, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_H1
            {23, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_I1
            {24, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_J1
            {25, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_K1
            {26, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_L1
            {27, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_M1
            {28, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_N1
            {29, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_O1
            {30, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_P1
            {31, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_Q1
            {32, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_R1
            {33, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_S1
            {34, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_T1
            {35, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_V1
            {36, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_W1
            {37, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_X1
            {38, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_Y1
            {39, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_Z1
            {40, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_A2
            {41, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_B2
            {42, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_C2
            {43, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_D2
            {44, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_E2
            {45, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_F2
            {46, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_G2
            {47, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_H2
            {48, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_I2
            {49, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_J2
            {50, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_K2
            {51, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_L2
            {52, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_M2
            {53, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_N2
            {54, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_O2
            {55, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_P2
            {56, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_Q2
            {57, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_R2
            {58, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_S2
            {59, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_T2
            {60, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_V2
            {61, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_W2
            {62, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_X2
            {63, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_Y2
            {64, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_Z2
            {65, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_A3
            {66, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_B3
            {67, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_C3
            {68, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_D3
            {69, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_E3
            {70, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_F3
            {71, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_G3
            {72, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}  // D4-D2_H3
          }
    },
    {"2", {
            {13, 0.641656, 41.093135, CS_6_25GHZ, std::nullopt, std::nullopt}, // Ajuntament More d'Ebre
            {14, 0.638803, 41.095093, CS_6_25GHZ, std::nullopt, std::nullopt}, // Hospital Comarcal
            {15, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_A1 (Estació Autobusos)
            {16, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_B1
            {17, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_C1
            {18, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_D1
            {19, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_E1
            {20, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_F1
            {21, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_G1
            {22, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_H1
            {23, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_I1
            {24, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_J1
            {25, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_K1
            {26, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_L1
            {27, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_M1
            {28, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_N1
            {29, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_O1
            {30, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_P1
            {31, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_Q1
            {32, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_R1
            {33, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_S1
            {34, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_T1
            {35, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_V1
            {36, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_W1
            {37, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_X1
            {38, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_Y1
            {39, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_Z1
            {40, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_A2
            {41, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_B2
            {42, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_C2
            {43, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_D2
            {44, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_E2
            {45, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_F2
            {46, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_G2
            {47, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_H2
            {48, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_I2
            {49, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_J2
            {50, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_K2
            {51, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_L2
            {52, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_M2
            {53, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_N2
            {54, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_O2
            {55, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_P2
            {56, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_Q2
            {57, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_R2
            {58, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_S2
            {59, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_T2
            {60, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_V2
            {61, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_W2
            {62, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_X2
            {63, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_Y2
            {64, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_Z2
            {65, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_A3
            {66, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_B3
            {67, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_C3
            {68, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_D3
            {69, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_E3
            {70, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_F3
            {71, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_G3
            {72, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}  // D4-D3_H3
          }
    },
    {"3", {
            {13, 0.524688, 40.811107, CS_6_25GHZ, std::nullopt, std::nullopt}, // Hospital Tortosa
            {14, 0.519487, 40.811128, CS_6_25GHZ, std::nullopt, std::nullopt}, // Mercat Central
            {15, 0.513451, 40.813403, CS_6_25GHZ, std::nullopt, std::nullopt} // Estadi Municipal
          }
    }
};

// clang-format on
std::vector<link> links = {
  {"1", "2", 2, 1, 152, {}, CS_6_25GHZ},
  {"1", "3", 3, 1, 152, {}, CS_6_25GHZ},
  {"2", "1", 1, 2, 152, {}, CS_6_25GHZ},
  {"2", "3", 3, 2, 152, {}, CS_6_25GHZ},
  {"3", "1", 1, 3, 152, {}, CS_6_25GHZ},
  {"3", "2", 2, 3, 152, {}, CS_6_25GHZ}
};