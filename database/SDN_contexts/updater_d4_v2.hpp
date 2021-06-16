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
              {15, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_A (Port tarragona)
              {16, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_B
              {17, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_C
              {18, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D2_D
              {19, 1.232718, 41.105505, CS_6_25GHZ, std::nullopt, std::nullopt} // D4-D2_E
          }
    },
    {"2", {
              {13, 0.641656, 41.093135, CS_6_25GHZ, std::nullopt, std::nullopt}, // Ajuntament More d'Ebre
              {14, 0.638803, 41.095093, CS_6_25GHZ, std::nullopt, std::nullopt}, // Hospital Comarcal
              {15, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_A (Estació Autobusos)
              {16, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_B
              {17, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_C
              {18, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt}, // D4-D3_D
              {19, 0.644494, 41.088381, CS_6_25GHZ, std::nullopt, std::nullopt} // D4-D3_E
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