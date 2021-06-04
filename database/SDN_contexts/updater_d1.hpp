j/////////////////////////////////////////////////////////////////////////////////////////
/**
 * @file server/plugins/updaters/static_ols/updater_static_ols.hpp
 * @brief header file for the pce::plugin::te_updater::ols_static_updater class
 *
 *	@author Ramon Casellas <ramon.casellas@cttc.es>
 *	@date 2007-2021
 */
/////////////////////////////////////////////////////////////////////////////////////////

#ifndef CTTC_PCE_SERVER_UPDATER_STATIC_OLS_HPP
#define CTTC_PCE_SERVER_UPDATER_STATIC_OLS_HPP

#include <pce/config.hpp>
#include <pce/flexi_grid.hpp>
#include <pce/ipv4.hpp>
#include <pce/logging.hpp>
#include <pce/protocol/swcap.hpp>
#include <pce/uuid.hpp>

#include <server/server.hpp>
#include <server/ted/client_port.hpp>
#include <server/ted/constants.hpp>
#include <server/ted/core.hpp>
#include <server/ted/manager.hpp>
#include <server/ted/network_port.hpp>
#include <server/ted/service_port.hpp>
#include <server/ted/ted.hpp>
#include <server/ted/topology_summary.hpp>

#include <sstream>
#include <string>

#include <pce/flexi_grid/nominal_frequency.hpp>
#include <server/ted/node_info.hpp>

#include <boost/serialization/export.hpp>


BOOST_CLASS_EXPORT_GUID(pce::te::node_info, "pce::te::node_info")
BOOST_CLASS_EXPORT_GUID(pce::te::roadm, "pce::te::roadm")

namespace pce::plugin::te_updater
{
    using namespace pce::flexi_grid;

    /////////////////////////////////////////////////////////////////////////////////////////
    /**
     * @brief Class for the updater for the OLS TE database.
     */
    /////////////////////////////////////////////////////////////////////////////////////////
    class ols_static_updater
    {
        /////////////////////////////////////////////////////////////////////////////////////////
        /**
         * @brief class that models an Optical Link.
         */
        /////////////////////////////////////////////////////////////////////////////////////////
        class link
        {
        public:
            // source node index "1", "2", ...
            std::string src;

            // destination node index "1", "2", ...
            std::string dst;

            uint32_t local_ifid = 0;

            uint32_t remote_ifid = 0;

            // swtiching capability
            uint8_t swcap = static_cast<uint8_t>(pce::switching_capability::lsc);

            // Optical DWDM channels supported on the link (not flexi-grid)
            std::vector<int16_t> channels;

            // Channel Spacing
            pce::flexi_grid::channel_spacing cs = CS_100GHZ;
        };


        /////////////////////////////////////////////////////////////////////////////////////////
        /**
         * @brief class that models a Client port
         */
        /////////////////////////////////////////////////////////////////////////////////////////
        class client_portinfo
        {
        public:
            /// Unnumbered interface id for the client port (node scope)
            uint32_t id = 0;

            // GPS coordinated
            float longitude = 0.0f;
            float latitude = 0.0f;

            /// Channel spacing tunability
            pce::flexi_grid::channel_spacing cs = CS_6_25GHZ;

            /// If there is a constraint on the selected n
            std::optional<int16_t> fixed_n_input = std::nullopt;
            std::optional<int16_t> fixed_n_output = std::nullopt;

            /// Lower and upper frequency
            uint64_t lower_frequency = 191'700'000;
            uint64_t upper_frequency = 196'100'000;

            std::string layer_protocol_name = "PHOTONIC_MEDIA";
        };


    public:
        /////////////////////////////////////////////////////////////////////////////////////////
        /**
         * @brief Constructor, binds the object to the database manager and configuration settings
         *
         *  @param db - Database to be updated, loading the topology,
         *      extended ted and reachability info from the files specified in
         *      the configuration settings
         *
         *	@param config - configuration settings, stored as a reference within the updater
         */
        /////////////////////////////////////////////////////////////////////////////////////////
        ols_static_updater(const std::shared_ptr<te::db>& db, const pce::config& config)
        : db_(db)
        , cfg_(config)
        {
            (void) cfg_;
            try {
                // Generate the TED
                this->generate();

                // File
                std::ofstream file("ted.xml");
                boost::archive::xml_oarchive oa(file);
                std::unique_lock<std::shared_timed_mutex> lock(db_->mutex);
                db_->save(oa);
                topology_summary(db_);
            }
            catch (const std::exception& ex) {
                PCE_ERR("UPDATER", "[OLS_STATIC] std exception - {}", ex.what());
                std::unique_lock<std::shared_timed_mutex> write_lock(db_->mutex);
                db_->clear();
                throw;
            }
        }

    private:
        /////////////////////////////////////////////////////////////////////////////////////////
        /**
         * @brief Generate the topology programmatically
         *
         */
        /////////////////////////////////////////////////////////////////////////////////////////
        void generate()
        {
            using std::string;
            using std::to_string;
#if 0
            std::map<string, string> clli = {
              {"1", "UPC Campus Nord"}, {"2", "La Sagrada Familia"}, {"3", "La Casa Mila"}, {"4", "El Parc Guell"}};

            std::map<string, std::pair<float, float>> gps = {{"1", {2.1125, 41.3880}},  // Campus Nord
                                                             {"2", {2.1744, 41.4036}},  // sagrada familia
                                                             {"3", {2.1619, 41.3952}},  // casa mila
                                                             {"4", {2.1527, 41.4145}}}; // parc guell

            // clang-format off
            std::map<string, std::vector<client_portinfo>> node_clientports = {
                {"1", {

                          {13, 2.11787223815918f, 41.398423760008164f, CS_50GHZ, std::nullopt, std::nullopt},
                          // port 14,15    Flexigrid-
                          {14, 2.102787223815918f, 41.388423760008164f, CS_6_25GHZ, std::nullopt, std::nullopt},
                          {15, 2.134380344068632f, 41.37573512628367f, CS_6_25GHZ, std::nullopt, std::nullopt},
                          {17, 2.127285005408339f, 41.38249746977345f, CS_50GHZ, std::nullopt, std::nullopt}
                      }
                },
                {"2", {
                          // G.709 XFP de Menara de 50GHz, 10Gb/s: sintonizables de  191.6 THz hasta 196.1 THz
                          {13, 2.2138881753198807f, 41.405441245287186f, CS_50GHZ, std::nullopt, std::nullopt},
                          // port 14,15    Flexigrid-
                          {14, 2.185220704413951f, 41.394839605134365f, CS_6_25GHZ, std::nullopt, std::nullopt},
                          {15, 2.1832931588403885f, 41.414880230675534f, CS_6_25GHZ, std::nullopt, std::nullopt},
                          // port 17, PS-TFT SFP+ Fiberstore (50 GHz, 191.70 - 196.10)
                          {17,2.202787392307073f, 41.4122863251991f, CS_50GHZ, std::nullopt, std::nullopt}
                      }
                },
                {"3", {
                          // {12, CS_50GHZ, std::nullopt, std::nullopt},
                          // G.709 XFP de Menara de 50GHz, 10Gb/s: sintonizables de  191.6 THz hasta 196.1 THz
                          {13, 2.186994556104765f, 41.38243307182125f, CS_50GHZ, std::nullopt, std::nullopt},
                          {14, 2.1572971274144948f, 41.381595869054856f, CS_6_25GHZ, std::nullopt, std::nullopt},
                          {15, 2.1795272757299244f, 41.39355184307848f, CS_6_25GHZ, std::nullopt, std::nullopt},
                          {16, 2.1528339368524034f, 41.39056842380848f, CS_6_25GHZ, std::nullopt, std::nullopt},
                          // XFP de FS.COM de 50GHz, 10Gb/s: sintonizables 1563.863nm (191.70THz) a 1528.773nm (196.10THz))
                          {17, 2.1511745505267754f, 41.39926074315011f, CS_50GHZ, std::nullopt, std::nullopt},
                          // port 18, BCN-PS-TFT SFP+ Fiberstore (50 GHz, 191.70 - 196.10)
                          // XFP de FS.COM de 50GHz, 10Gb/s: sintonizables 1563.863nm (191.70THz) a 1528.773nm (196.10THz))
                          {18, 2.177181243896485f, 41.374425517838944f, CS_50GHZ, std::nullopt, std::nullopt}
                      }
                },
                {"4", {
                          // G.709 XFP de Menara de 50GHz, 10Gb/s: sintonizables de  191.6 THz hasta 196.1 THz
                          {13, 2.1348953386768703f, 41.42856998898639f, CS_50GHZ, std::nullopt, std::nullopt},
                          {14, 2.1442794869653885f, 41.43045768455642f, CS_6_25GHZ, std::nullopt, std::nullopt},
                          {15, 2.166938788723201f, 41.42942803458957f, CS_6_25GHZ, std::nullopt, std::nullopt},
                          {16, 2.1850204607471824f, 41.42376469733116f, CS_6_25GHZ, std::nullopt, std::nullopt},
                          {17, 2.15961457695812f, 41.42942804244521f, CS_50GHZ, std::nullopt, std::nullopt},
                          {21, 2.1160125662572686f, 41.416727713618336f, CS_100GHZ, 1, 0},
                          {22, 2.152433397131972f, 41.421040108469086f, CS_100GHZ, 3, 2},
                          {23, 2.122106545139104f, 41.421748081362594f, CS_6_25GHZ, std::nullopt, std::nullopt},
                          {24, 2.165565497707576f, 41.42299238276018f, CS_6_25GHZ, std::nullopt, std::nullopt},
                          {25, 2.188453667331487f, 41.41923795778598f, CS_6_25GHZ, std::nullopt, std::nullopt}

                      }
                }
            };
    #endif
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

            pce::uuid uuid;
            std::unique_lock<std::shared_timed_mutex> write_lock(db_->mutex);
            pce::te::graph& g = db_->get_graph();

            uuid = pce::generate_name_uuid("D1-context");
            g.properties["context-uuid"] = to_string(uuid);
            uuid = pce::generate_name_uuid("D1-graph");
            g.properties[UUID] = to_string(uuid);

            pce::te::node n;
            pce::te::link l;
            bool inserted;

            string prefix = "10.1.1.11";
            uint16_t domainid = 0;

            /*
             *
             * Generate the client ports.
             *   Each client port supports network media channels (NMC)
             */
            for (const auto& [src, cpv] : node_clientports) {
                string id = prefix + src;
                auto uuid = pce::generate_name_uuid(id);
                auto node_name = "node_" + src;
                auto node_local_name = "node_" + src;


                pce::te::node_attributes node_attributes;
                node_attributes.id = pce::make_address(id);
                node_attributes.set_name(node_name);
                node_attributes.domainid = domainid;
                node_attributes.properties[UUID] = to_string(uuid);
                node_attributes.properties["name"] = node_name;
                node_attributes.properties["local-name"] = node_local_name;
                node_attributes.properties["rest"] = id + ":5100";
                node_attributes.properties["nodeid"] = id;
                node_attributes.properties["longitude"] = to_string(gps[src].first);
                node_attributes.properties["latitude"] = to_string(gps[src].second);
                node_attributes.properties["clli"] = clli[src];
                node_attributes.properties[CTTC_NODE_TYPE] = CTTC_NODE_TYPE_ROADM;

                /**
                 * Add information
                 */
                auto roadm = std::make_unique<pce::te::roadm>();
                roadm->roadmid = 6;
                node_attributes.layer_info = std::move(roadm);



                PCE_INF("UPDATER", "[OLS_STATIC] generating client ports for {}", id);
                for (auto& scp : cpv) {
                    pce::te::client_port cp{node_name + "_port_" + to_string(scp.id), scp.id};
                    cp.properties[LAYER_PROTOCOL_NAME] = scp.layer_protocol_name;
                    cp.properties[LAYER_PROTOCOL_QUALIFIER] = LAYER_PROTOCOL_QUALIFIER_NMC;
                    cp.properties["longitude"] = to_string(scp.longitude);
                    cp.properties["latitude"] = to_string(scp.latitude);
                    if (scp.layer_protocol_name == PHOTONIC_MEDIA) {
                        cp.properties["types"] = "NMC";
                        cp.properties["lower-frequency"] = to_string(scp.lower_frequency);
                        cp.properties["upper-frequency"] = to_string(scp.upper_frequency);
                        if (scp.cs == CS_50GHZ) {
                            cp.properties[GRID_TYPE] = "DWDM";
                            cp.properties[ADJUSTMENT_GRANULARITY] = "G_50GHZ";
                        } else if (scp.cs == CS_100GHZ) {
                            cp.properties[GRID_TYPE] = "DWDM";
                            cp.properties[ADJUSTMENT_GRANULARITY] = "G_100GHZ";
                        } else if (scp.cs == CS_6_25GHZ) {
                            cp.properties[GRID_TYPE] = "FLEX";
                            cp.properties[ADJUSTMENT_GRANULARITY] = "G_6_25GHZ";
                        } else {
                            PCE_ERR("UPDATER", "[OLS_STATIC] cannot identify GRID_TYPE {}", id);
                            abort();
                        }
                        if (scp.fixed_n_input) {
                            cp.properties["fixed-n-input"] = to_string(*scp.fixed_n_input);
                        }
                        if (scp.fixed_n_output) {
                            cp.properties["fixed-n-output"] = to_string(*scp.fixed_n_output);
                        }
                    }
                    // Add service ports
                    {
                        /* This is the input SIP (service port) associated to the client-facing NEP */
                        pce::te::service_port service_port(cp.get_name() + "-input", cp.get_id());
                        service_port.properties[LAYER_PROTOCOL_NAME] = scp.layer_protocol_name;
                        service_port.properties[LAYER_PROTOCOL_QUALIFIER] = LAYER_PROTOCOL_QUALIFIER_NMC;
                        service_port.properties[DIRECTION] = "INPUT";
                        service_port.properties[TOPO_UUID] = g.get_property(UUID);
                        service_port.properties[NODE_UUID] = node_attributes.properties[UUID];
                        service_port.properties[NEP_UUID] = to_string(cp.get_uuid());
                        service_port.properties.insert(cp.properties.begin(), cp.properties.end());
                        cp.properties["sip-uuid-input"] = to_string(service_port.get_uuid());
                        g.service_ports.emplace(service_port.get_uuid(), std::move(service_port));
                    }
                    {
                        /* output SIP */
                        pce::te::service_port service_port(cp.get_name() + "-output", cp.get_id());
                        service_port.properties[LAYER_PROTOCOL_NAME] = scp.layer_protocol_name;
                        service_port.properties[LAYER_PROTOCOL_QUALIFIER] = LAYER_PROTOCOL_QUALIFIER_NMC;
                        service_port.properties[DIRECTION] = "OUTPUT";
                        service_port.properties[TOPO_UUID] = g.get_property(UUID);
                        service_port.properties[NODE_UUID] = node_attributes.properties[UUID];
                        service_port.properties[NEP_UUID] = to_string(cp.get_uuid());
                        service_port.properties.insert(cp.properties.begin(), cp.properties.end());
                        cp.properties["sip-uuid-output"] = to_string(service_port.get_uuid());
                        g.service_ports.emplace(service_port.get_uuid(), std::move(service_port));
                    }
                    node_attributes.client_ports.emplace(cp.get_id(), std::move(cp));
                }
                for (const auto& [k, v] : node_attributes.properties) {
                    PCE_DBG("UPDATER", "[OLS_STATIC] node {} -> {}", k, v);
                }
                std::tie(n, inserted) = db_->declare(node_attributes.id);
                if (inserted) {
                    g[n].update(std::move(node_attributes));
                    g(n);
                }
            }

            for (const auto& lk : links) {
                // LINK j->k
                const string& src = lk.src;
                const string& dst = lk.dst;
                auto id1 = prefix + src;
                auto id2 = prefix + dst;
                std::tie(n, inserted) = db_->declare(pce::make_address(id1));

                // Allocate a new network port based on data
                string node_name = "node_" + src;
                pce::te::network_port np{node_name + "_port_" + to_string(lk.local_ifid), lk.local_ifid};
                np.properties[LAYER_PROTOCOL_NAME] = PHOTONIC_MEDIA;
                np.properties[LAYER_PROTOCOL_QUALIFIER] = LAYER_PROTOCOL_QUALIFIER_NMC;
                auto& node_attributes = g[n];
                node_attributes.network_ports.emplace(lk.local_ifid, std::move(np));

                pce::te::link_attributes link_attributes;
                link_attributes.local_domainid = domainid;
                link_attributes.remote_domainid = domainid;
                link_attributes.source(pce::make_address(id1));
                link_attributes.target(pce::make_address(id2));
                link_attributes.local_ifid = lk.local_ifid;
                link_attributes.remote_ifid = lk.remote_ifid;
                link_attributes.te_metric = 1;
                link_attributes.max_bw = 0;
                link_attributes.max_resv_bw = 0;
                link_attributes.unresv_bw[0] = 0;
                link_attributes.unresv_bw[1] = 0;
                link_attributes.unresv_bw[2] = 0;
                link_attributes.unresv_bw[3] = 0;
                link_attributes.unresv_bw[4] = 0;
                link_attributes.unresv_bw[5] = 0;
                link_attributes.unresv_bw[6] = 0;
                link_attributes.unresv_bw[7] = 0;
                link_attributes.iscd.resize(1);
                auto uuid = pce::generate_name_uuid(link_attributes.name());
                link_attributes.properties["uuid"] = to_string(uuid);
                link_attributes.iscd[0].switching_cap = lk.swcap;
                PCE_INF("UPDATER", "[OLS_STATIC] Generating link {} -> {} {} {} - {}", id1, id2,
                        link_attributes.source(), link_attributes.target(), link_attributes.name());

                /*
                 * Fixed grid
                 * Channels are encoded using ITU-T fixed grid 32 bit NCFs.
                 */
                if (lk.swcap == static_cast<uint8_t>(pce::switching_capability::lsc)) {
                    link_attributes.iscd[0].encoding = 8;
                    link_attributes.channels.resize(lk.channels.size());
                    int16_t channel_index = 0;
                    for (auto& ch : link_attributes.channels) {
                        int16_t n = lk.channels[channel_index];
                        ch.g694_id = pce::flexi_grid::make_g694_id(GRID_DWDM, (enum channel_spacing) lk.cs, 0, n);
                        pce::frequency_t f = pce::flexi_grid::make_nominal_frequency(n, lk.cs);
                        PCE_VRB("UPDATER", "[OLS_STATIC] c: {} {} {}", n, ch.g694_id, GigaHertz{f}.value());
                        ch.state = pce::te::LRM_CHN_STATE_STANDBY;
                        channel_index++;
                    }
                }



                /*
                 * When modeling a WSS link, we have 386 slices each 12.5 GHz.
                 * One can configure from 1 to 40 slices, with an  allocation granularity: from 12.5 GHz to 500 GHz
                 *
                 * 191.33125 THz [ 191.3250 THz, 191.3375 THz]
                 * 196.14375 THz [ 196.1375 THz, 196.1500 THz]
                 *
                 * We declare the nominal central freq of each individual slice.
                 */
                // first slice n =  -283 [-284 .. -282]
                // last slice n  =   487 [ 486 .. 488]
                if (lk.swcap == static_cast<uint8_t>(pce::switching_capability::flexi_grid_lsc)) {
                    link_attributes.iscd[0].encoding = 8;
                    link_attributes.channels.resize(386);
                    int16_t channel_index = -283;
                    int16_t slice_index = 0;
                    for (auto& ch : link_attributes.channels) {
                        ch.g694_id = pce::flexi_grid::make_g694_id(GRID_FLEXI, CS_6_25GHZ, 0, channel_index);
                        ch.state = pce::te::LRM_CHN_STATE_STANDBY;
                        channel_index += 2;
                        slice_index++;
                    }
                    PCE_INF("UPDATER", "[OLS_STATIC] flexi with {} slices and {} n", slice_index, channel_index);
                    PCE_INF("UPDATER", "[OLS_STATIC] from {} to {}", // -
                            get_n(link_attributes.channels[0].g694_id), get_n(link_attributes.channels[385].g694_id));
                    PCE_INF("UPDATER", "[OLS_STATIC] from {} MHz to {} MHz",
                            get_n(link_attributes.channels[0].g694_id) * 6250 + 193100000,
                            get_n(link_attributes.channels[385].g694_id) * 6250 + 193100000);
                }

                // Update the attributes, set the origing and mark as updated
                std::tie(l, inserted) =
                  db_->declare(link_attributes.source(), link_attributes.target(), link_attributes.local_ifid);
                g[l].update(std::move(link_attributes));
                g(l);
            }
            PCE_INF("UPDATER", "[OLS_STATIC] loaded TED file with {} nodes and {} links", boost::num_vertices(g),
                    boost::num_edges(g));
        }

        /// The database to load
        const std::shared_ptr<te::db>& db_;

        /// PCE configuration settings
        const pce::config& cfg_;
    };

} // namespace pce::plugin::te_updater

#endif
