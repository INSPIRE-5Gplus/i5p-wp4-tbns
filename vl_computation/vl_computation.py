#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
import networkx as nx
from itertools import islice

from config_files import settings
from blockchain_node import blockchain_node as bl_mapper

# the graph with the E2E network topology...
# in VNode is composed with the interdomain links
# in VLink is composed with the interdomain links and domain contexts (nodes with SIPs & virtual links)
# in Transparent is composed with the interdomain links and domain contexts (all nodes & real links)
e2e_topology_graph = nx.MultiDiGraph()

# Virtual Node abstraction procedure
def vnode_abstraction(local_context):
    abstracted_context = {}
    tapi_common_context = {}
    tapi_topology_context = {}
    topology = []

    tapi_common_context["uuid"] = local_context["tapi-common:context"]["uuid"]
    tapi_common_context["name"] = local_context["tapi-common:context"]["name"]
    tapi_common_context["service-interface-point"] = local_context["tapi-common:context"]["service-interface-point"]

    tapi_topology_context["nw-topology-service"] = local_context["tapi-common:context"]["tapi-topology:topology-context"]["nw-topology-service"]
    for topology_item in local_context["tapi-common:context"]["tapi-topology:topology-context"]["topology"]:
        topology_element = {}
        node = []
        node_element = {}
        node_owned_nep = []
        topology_element["uuid"] = topology_item["uuid"]
        topology_element["layer-protocol-name"] = topology_item["layer-protocol-name"]
        topology_element["name"] = topology_item["name"]

        # wa want just a node from all the nodes in the reference context
        node_element["uuid"] = topology_item["uuid"]        # we identiy the node with the topology uuid it comes from
        node_element["name"] = topology_item["name"]        # for now we use tha topology name
        for node_item in topology_item["node"]:
            for owned_nep_item in node_item["owned-node-edge-point"]:
                if "mapped-service-interface-point" in owned_nep_item:
                    node_owned_nep.append(owned_nep_item)
        node_element["owned-node-edge-point"] = node_owned_nep
        node.append(node_element)
        topology_element["node"] = node
        topology_element["link"] = []
        topology.append(topology_element)

    tapi_topology_context["topology"] = topology
    tapi_common_context["tapi-topology:topology-context"] = tapi_topology_context

    connectivity_context = {}
    connectivity_context["connectivity-service"] = []
    connectivity_context["connection"] = []
    tapi_common_context["tapi-connectivity:connectivity-context"] = connectivity_context

    abstracted_context["tapi-common:context"] = tapi_common_context

    return abstracted_context

# Virtual Link abstraction procedure
def vlink_abstraction(local_context):
  abstracted_context = {}
  tapi_common_context = {}
  tapi_topology_context = {}
  topology = []

  # copies basic context information (uuid, name, SIPs lost)
  tapi_common_context["uuid"] = local_context["tapi-common:context"]["uuid"]
  tapi_common_context["name"] = local_context["tapi-common:context"]["name"]
  tapi_common_context["service-interface-point"] = local_context["tapi-common:context"]["service-interface-point"]
  tapi_topology_context["nw-topology-service"] = local_context["tapi-common:context"]["tapi-topology:topology-context"]["nw-topology-service"]

  # for each topology in the local context, selects thos ndoes with SIPs and creates the virtual links among them
  for topology_item in local_context["tapi-common:context"]["tapi-topology:topology-context"]["topology"]:
    topology_element = {}
    node_list = []
    nodes_sips_list = []
    link_list = []
    G = nx.MultiDiGraph()       #graph used to define the virtual links
    #G = nx.Graph()

    # copies basic topology information
    topology_element["uuid"] = topology_item["uuid"]
    topology_element["layer-protocol-name"] = topology_item["layer-protocol-name"]
    topology_element["name"] = topology_item["name"]

    # nodes selection based on having SIPs (selected) or not
    for node_item in topology_item["node"]:
      for owned_nep_item in node_item["owned-node-edge-point"]:
          if "mapped-service-interface-point" in owned_nep_item:
              node_list.append(node_item)
              nodes_sips_list.append(node_item["uuid"])
              G.add_node(node_item["uuid"])
              break

    topology_element["node"] = node_list

    # virtual links design among nodes with SIPs
    for link_item in topology_item["link"]:
      # adds all the existing links into de graph
        node1 = link_item["node-edge-point"][0]["node-uuid"]
        node_edge_point1 = link_item["node-edge-point"][0]["node-edge-point-uuid"]
        node2 = link_item["node-edge-point"][1]["node-uuid"]
        node_edge_point2 = link_item["node-edge-point"][1]["node-edge-point-uuid"]
        e2e_topology_graph.add_edge(node1, node2, n1=node1, nep1=node_edge_point1, n2=node2, nep2=node_edge_point2)

    # Creates the VLINKs based on shortest routes between nodes with SIPs
    for node_source_item in list(G.nodes):
      for node_destination_item in list(G.nodes):
          if (node_source_item != node_destination_item) and (node_source_item in nodes_sips_list) and (node_destination_item in nodes_sips_list):
              vlink = {}
              name = []
              neps = []
              
              # prepares the basic information definning the virtual link to be added
              vlink["uuid"] = str(uuid.uuid4())
              name.append({"value-name": "local-name", "value": node_source_item +"_"+ node_destination_item})
              vlink["name"] = name
              vlink["direction"] = "UNIDIRECTIONAL"
              lpn = []
              lpn.append("PHOTONIC_MEDIA")
              vlink["layer-protocol-name"] = lpn

              # generates the route between nodes with SIPs definning the virtual link to be added
              route = nx.shortest_path(G, source=node_source_item, target=node_destination_item)
              length_route = len(route)
              
              # extract information of first and last links in the route
              first_link = G.get_edge_data(route[0], route[1])
              first_link_info = first_link[0]
              first_node = {}
              first_node["topology-uuid"] = topology_item["uuid"]
              first_node["node-uuid"] = first_link_info["n1"]
              first_node["node-edge-point-uuid"] = first_link_info["nep1"]
              neps.append(first_node)

              last_link = G.get_edge_data(route [length_route-2], route[length_route-1])
              last_link_info = first_link[0]
              second_node = {}
              second_node["topology-uuid"] = topology_item["uuid"]
              second_node["node-uuid"] = first_link_info["n2"]
              second_node["node-edge-point-uuid"] = first_link_info["nep2"]
              neps.append(second_node)

              vlink["node-edge-point"] = neps
              link_list.append(vlink)

    topology_element["link"] = link_list
    topology.append(topology_element)

  # finsihes with the last details
  tapi_topology_context["topology"] = topology
  tapi_common_context["tapi-topology:topology-context"] = tapi_topology_context

  connectivity_context = {}
  connectivity_context["connectivity-service"] = []
  connectivity_context["connection"] = []
  tapi_common_context["tapi-connectivity:connectivity-context"] = connectivity_context

  abstracted_context["tapi-common:context"] = tapi_common_context
  return abstracted_context

# creates the initial e2e graph with its local domain information
def add_context_e2e_graph(context_json):
  for topology_item in context_json["tapi-common:context"]["tapi-topology:topology-context"]["topology"]:
    # adds all the nodes in the abstracted topology
    for node_item in topology_item["node"]:
      e2e_topology_graph.add_node(node_item["uuid"])
    
    # adds all the (unidirectional) links in the abstracted topology
    if topology_item["link"]:
      for link_item in topology_item["link"]:
        #e2e_topology_graph.add_edge(node_1["uuid"], node_2["uuid"], uuid=interdomain_link_item["uuid"])
        l_uuid = link_item["uuid"]
        topo = link_item["node-edge-point"][0]["topology-uuid"]
        node1 = link_item["node-edge-point"][0]["node-uuid"]
        node_edge_point1 = link_item["node-edge-point"][0]["node-edge-point-uuid"]
        node2 = link_item["node-edge-point"][1]["node-uuid"]
        node_edge_point2 = link_item["node-edge-point"][1]["node-edge-point-uuid"]
        e2e_topology_graph.add_edge(node1, node2, link_uuid = l_uuid, topology=topo, n1=node1, nep1=node_edge_point1, n2=node2, nep2=node_edge_point2)

# updates the e2e graph by adding new domains and itner-domains links.
def add_idl_e2e_graph(e2e_json):
    # adds all the SDN domains defined in the json
    for domain_item in e2e_json["e2e-topology"]["nodes-list"]:
        e2e_topology_graph.add_node(domain_item)
    
    # add the links interconnecting the SDN domains defined in the json
    for interdomain_link_item in e2e_json["e2e-topology"]["interdomina-links"]:
      # adding both unidirectional links for the routing process in the E2E MultiDiGraph
      node_1 = interdomain_link_item["nodes-involved"][0]
      node_2 = interdomain_link_item["nodes-involved"][1]
      uuid_idl = interdomain_link_item["link-options"][0]["uuid"]
      e2e_topology_graph.add_edge(node_1, node_2, interdomain_link_uuid=uuid_idl)

      node_1 = interdomain_link_item["nodes-involved"][1]
      node_2 = interdomain_link_item["nodes-involved"][0]
      uuid_idl = interdomain_link_item["link-options"][1]["uuid"]
      e2e_topology_graph.add_edge(node_1, node_2, interdomain_link_uuid=uuid_idl)

# computes the K-shortest simple path between two compute domains
def find_path(src, dst):
  path_nodes_list = []
  K = 7 # we will keep the 5 shortest paths generated
  #path_nodes_list = nx.shortest_path(e2e_topology_graph, src, dst)
  #simple_path_list = nx.all_simple_paths(e2e_topology_graph, src, dst, cutoff=8)
  #path_nodes_list = list(sorted(simple_path_list, key = len))
  simple_path_list = nx.shortest_simple_paths(e2e_topology_graph, src, dst)
  for path in islice(simple_path_list, K):
    path_nodes_list.append(path)
     
  return path_nodes_list

""" Example of interdomain_links_json
{
  "e2e-topology": {
    "nodes-list": [
      //it contains the uuids of those nodes with an inter-domain link
      // for VNODE is the ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["uuid"]
      // for VLINK is the ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"]["uuid"]
      // for TRANSPARENT is the ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"]["uuid"]
      "uuid_A",
      "uuid_B",
      "uuid_C"
    ],
    "interdomain-links": [
      {
        "name": "uuid_A-uuid_B",
        // key values to identify the link are the two nodes in nodes-involved
        "nodes-involved": [
          "uuid_A",
          "uuid_B,
        ],
        "link-options": [
          //there will be only two unidirectional options, each with the different physical links for the trick.
          {
            "uuid": "uuid",
            "direction": "UNIDIRECTIONAL",
            "nodes-direction": {
              "node-1": "uuid_A",
              "node-2": "uuid_B"
            },
            "layer-protocol-name": [
              "PHOTONIC_MEDIA"
            ],
            "physical-options": [
              {
                "node-edge-point":[
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_A",
                    // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                    // this NEP is one of those with SIPs in the domain
                    "nep-uuid": "nep_C1"
                  },
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_B",
                    "nep-uuid": "nep_D1"
                  }
                ] ,
                "occupied-spectrum": [
                ]
              },
              {
                "node-edge-point":[
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_A",
                    // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                    // this NEP is one of those with SIPs in the domain
                    "nep_uuid": "nep_C2"
                  },
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_B",
                    "nep-uuid": "nep_D2"
                  }
                ] ,
                "occupied-spectrum": [
                ]
              }
            ]
          },
          {
            "uuid": "uuid",
            "direction": "UNIDIRECTIONAL",
            "layer-protocol-name": [
              "PHOTONIC_MEDIA"
            ],
            "nodes-direction": {
              "node-1": "uuid_B",
              "node-2": "uuid_A"
            },
            "physical-options": [
              {
                "node-edge-point":[
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_B",
                    // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                    // this NEP is one of those with SIPs in the domain
                    "nep_uuid": "nep_D1"
                  },
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_A",
                    "nep-uuid": "nep_C1"
                  }
                ] ,
                "occupied-spectrum": [
                ]
              },
              {
                "node-edge-point":[
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_B",
                    // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                    // this NEP is one of those with SIPs in the domain
                    "nep_uuid": "nep_D2"
                  },
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_A",
                    "nep-uuid": "nep_C2"
                  }
                ] ,
                "occupied-spectrum": [
                ]
              }
            ]
          }
        ],
        "supportable_spectrum": [
          {
            "lower-frequency": 191700000,
            "upper-frequency": 196100000,
            "frequency-constraint": {
              "adjustment-granularity": "G_50GHZ",
              "grid-type": "DWDM"
            }
          }
        ],
        "available_spectrum": [
          {
            "lower-frequency": 191700000,
            "upper-frequency": 196100000,
            "frequency-constraint": {
              "adjustment-granularity": "G_50GHZ",
              "grid-type": "DWDM"
            }
          }
        ]
      },
      {
        "name": "uuid_A-uuid_B",
        // key values to identify the link are node-1 and node-2 (always as pair)
        "node-1": "uuid_A",
        "node-2": "uuid_B",
        "link_options": [
          //there will be only two unidirectional options, each with the different physical links for the trick.
          {
            "uuid": "uuid",
            "direction": "UNIDIRECTIONAL",
            "layer-protocol-name": [
              "PHOTONIC_MEDIA"
            ],
            "physical-options": [
              {
                "node-edge-point":[
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_A",
                    // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                    // this NEP is one of those with SIPs in the domain
                    "nep_uuid": "nep_C1"
                  },
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_B",
                    "nep-uuid": "nep_D1"
                  }
                ] ,
                "occupied-spectrum": [
                ]
              },
              {
                "node-edge-point":[
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_A",
                    // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                    // this NEP is one of those with SIPs in the domain
                    "nep_uuid": "nep_C1"
                  },
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_B",
                    "nep-uuid": "nep_D1"
                  }
                ] ,
                "occupied-spectrum": [
                ]
              }
            ]
          },
          {
            "uuid": "uuid",
            "direction": "UNIDIRECTIONAL",
            "layer-protocol-name": [
              "PHOTONIC_MEDIA"
            ],
            "physical-options": [
              {
                "node-edge-point":[
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_A",
                    // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                    // this NEP is one of those with SIPs in the domain
                    "nep_uuid": "nep_C1"
                  },
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_B",
                    "nep-uuid": "nep_D1"
                  }
                ] ,
                "occupied-spectrum": [
                ]
              },
              {
                "node-edge-point":[
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_A",
                    // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                    // this NEP is one of those with SIPs in the domain
                    "nep_uuid": "nep_C1"
                  },
                  {
                    "topology-uuid": "uuid",
                    "node-uuid": "uuid_B",
                    "nep-uuid": "nep_D1"
                  }
                ] ,
                "occupied-spectrum": [
                ]
              }
            ]
          }
        ],
        "supportable_spectrum": [
          {
            "lower-frequency": 191700000,
            "upper-frequency": 196100000,
            "frequency-constraint": {
              "adjustment-granularity": "G_50GHZ",
              "grid-type": "DWDM"
            }
          }
        ],
        "available_spectrum": [
          {
            "lower-frequency": 191700000,
            "upper-frequency": 196100000,
            "frequency-constraint": {
              "adjustment-granularity": "G_50GHZ",
              "grid-type": "DWDM"
            }
          }
        ]
      }
    ]
  }
}
"""
# Based on a given route, looks for the specific NEPs involved in the inter-domain links
def domain2nep_route_mapping(route, e2e_topology):
  route_neps = []
  route_interdominlinks = []

  """
    if os.environ.get("ABSTRACION_MODEL") == "vlink":
      pass
    elif os.environ.get("ABSTRACION_MODEL") == "transparent":
      pass
    else:
      pass
  """
  # it gets the list of neps involved for each link (two ndoes) in the route
  for idx, route_item  in enumerate(route):
    link_found = False
    if route[idx] != len(route-1):
      #response = get link information (node1,node2) from graph
      #if link is an idl --> check key "uuid_idl" in response
        #for idl_item in e2e_topology["interdomain-links"]:
          #if node1 in idl_item["nodes-involved"] and node2 in idl_item["nodes-involved"]:
            #check the available spectrum, no need to wait until the end to discard this route.
            #for link_option_item in idl_item["link-options"]:
              #if link_option_item["uuid"] == uuid_idl
                # for physical_option_item in link_option_item["physical-options"]:
                  # if physical_option_item["occupied-spectrum"] is empty
                    # get the topology, node, NEPs and direction (OUTPUT/INPUT) from the graph and add into the route-neps
      #else: #link belong to a context
        # get the link_uuid, topology, node, NEPs and direction (OUTPUT/INPUT) from the graph and add it into the route-neps

      for inter_link_item in e2e_topology["interdomain-links"]:
        if ((route_item == inter_link_item["domain-1"] and route[idx+1] == inter_link_item["domain-2"]) or \
          (route_item == inter_link_item["domain-2"] and route_item[idx+1] == inter_link_item["domain-1"])):
          # this FOR loop is to manage a set of physical links that share the spectrum as if they would be a single one with different SIPs
          for link_option_item in inter_link_item["link-options"]:
            # checks the directionality of the route.
            for option_direction_item in link_option_item["link-direction"]:
              if (route_item == option_direction_item["domain-1"] and \
                route[idx+1] == option_direction_item["domain-2"] and not option_direction_item["occupied-spectrum"]):
                link_found = True
                
                # prepares the list of interdomins links for the spectrum assignemt.
                route_element = {}
                spectrum_slot_list = []
                route_element["uuid"] = inter_link_item["uuid"]
                route_element["link-option-uuid"] = link_option_item["uuid"]
                if not inter_link_item["available_spectrum"]:
                  spectrum_slot = []
                  spectrum_slot.append(inter_link_item["supportable_spectrum"][0]["lower-frequency"])
                  spectrum_slot.append(inter_link_item["supportable_spectrum"][0]["upper-frequency"])
                  spectrum_slot_list.append(spectrum_slot)
                else:
                  for available_item in inter_link_item["available_spectrum"]:
                    spectrum_slot = []
                    spectrum_slot.append(available_item["lower-frequency"])
                    spectrum_slot.append(available_item["upper-frequency"])
                    spectrum_slot_list.append(spectrum_slot)
                route_element["available_spectrum"] = spectrum_slot_list
                route_interdominlinks.append(route_element)
                
                # selects the NEPs involved and defines their SIP directionality based on their position in the route.
                if route_item == link_option_item["domain-1"]["uuid"]:
                  route_nep = link_option_item["domain-1"]
                  route_nep["direction"] = "OUTPUT"
                  route_neps.append(route_nep)
                  route_nep = link_option_item["domain-2"]
                  route_nep["direction"] = "INPUT"
                  route_neps.append(route_nep)
                else:
                  route_nep = link_option_item["domain-2"]
                  route_nep["direction"] = "OUTPUT"
                  route_neps.append(route_nep)
                  route_nep = link_option_item["domain-1"]
                  route_nep["direction"] = "INPUT"
                  route_neps.append(route_nep)
                break
            if link_found == True:
              break
            else:
              print("Link-option not available, looking the next one to check if it is free to be used.")
        if link_found == True:
          break
        else:
          print("Looking if the next link is the good one and if it has available spectrum.")
      if link_found == False:
        print("Link blocked as the link has no options with spectrum available.")
        return [], []
  return route_neps, route_interdominlinks

"""
Example of route_neps = [
    {link_uuid, topology, node_uuid, nep_uuid, direction},
    {link_uuid, topology, node_uuid, nep_uuid, direction},
    {topology, node_uuid, nep_uuid, direction},
    {topology, node_uuid, nep_uuid, direction},
    {link_uuid, topology, node_uuid, nep_uuid, direction},
    {link_uuid, topology, node_uuid, nep_uuid, direction}
  ]
"""
# based on the NEPs route, it looks for the corresponding SIPs to define the CSs
def nep2sip_route_mapping(route_neps, e2e_cs_request):
  found_nep = {}
  route_sips = []
  transparent_links = []
  internal_neps = []
  # maps intermediate NEPs to intermediate SIPs
  for idx, nep_item  in enumerate(route_neps):
    if "link_uuid" in nep_item:
      # NOTE: this if will be accessed only in transparent abstraction mode
      next_nep = route_neps[idx+1]
      if "link_uuid" in next_nep and nep_item["link_uuid"] == next_nep["link_uuid"]:
        trans_link_item = {}
        trans_link_item["uuid"] = nep_item["link_uuid"]
        trans_link_item["topology"] = nep_item["topology"]
        transparent_links.append(trans_link_item)
        internal_neps.append(nep_item)
        internal_neps.append(next_nep)
      else:
        # NOTE: if it enters at this point, it means the nep_item is an internal nep and ...
        # ... its link has already been selected in the previous loop round
        pass 
    else:
      # get specific domain topology to discover the correct SIP to use
      response = bl_mapper.get_context_from_blockchain(nep_item["topology"])
      domain_context = response['context']
      # look inot all the nodes of the incoming context
      for node_item in domain_context["tapi-common:context"]["tapi-topology:topology-context"]["topology"][0]["node"]:
        for owned_nep_item in node_item["owned-node-edge-point"]:
          if owned_nep_item["uuid"] == nep_item["nep_uuid"]:
            found_nep = owned_nep_item
            break
        found_sip = False
        for mapped_sip_item in found_nep["mapped-service-interface-point"]:
          for sip_item in domain_context["tapi-common:context"]["service-interface-point"]:
            if mapped_sip_item["service-interface-point-uuid"] == sip_item["uuid"] and nep_item["direction"]==sip_item["direction"]:
              sip_item["topology"] = nep_item["topology"]
              sip_item["blockchain_owner"] = response['blockchain_owner']
              route_sips.append(sip_item)
              found_sip = True
              break
          if found_sip:
            break
        if found_sip:
          break
  
  # adds the FIRST SIP in the route
  response = bl_mapper.get_context_from_blockchain(e2e_cs_request["domain-source"]["uuid"])
  for sip_item in response["context"]["tapi-common:context"]["service-interface-point"]:
        if sip_item["uuid"] == e2e_cs_request["domain-source"]["sip"]:
          sip_item["blockchain_owner"] = response['blockchain_owner']
          route_sips.insert(0, sip_item)
  
  # adds the last SIP in the route
  response = bl_mapper.get_context_from_blockchain(e2e_cs_request["domain-destination"]["uuid"])
  for sip_item in response["context"]["tapi-common:context"]["service-interface-point"]:
        if sip_item["uuid"] == e2e_cs_request["domain-source"]["sip"]:
          sip_item["blockchain_owner"] = response['blockchain_owner']
          route_sips.append(sip_item)
  
  return route_sips, transparent_links, internal_neps

"""
Example of route_sips = [
  {sip_info, "topology", "blockchain_owner"},
  {sip_info, "topology", "blockchain_owner"}
]
Example of route_interdominlinks = [
    {"uuid", "link-option-uuid", "available_spectrum":[YYY, YYY]},
    {"uuid", "link-option-uuid", "available_spectrum"}
  ]
Example of internal_neps = [
    {link_uuid, topology, node_uuid, nep_uuid, direction},
    {link_uuid, topology, node_uuid, nep_uuid, direction},
    {link_uuid, topology, node_uuid, nep_uuid, direction},
    {link_uuid, topology, node_uuid, nep_uuid, direction}
  ]
"""
# Spectrum assignment --> We look for the exact-Fit, otherwise the Best-Fit
def spectrum_assignment(spectrum_list, capacity):  
  # it checks the availability of all the involved inter-domain links and extract the 
  # common available spectrum bigger than 75GHz
  ref_spectrum = spectrum_list[0]
  for idx, spectrum_item in enumerate(spectrum_list):
    # different than the first item as its the initial reference
      if idx != 0:
          ref_spectrum = intersections(ref_spectrum,spectrum_item)

  # among all the possibilities, keeps those bigger or equal than 75GHz
  final_spectrum_options = []
  for spectrum_item in ref_spectrum:
      resultant_spectrum = spectrum_item[1] - spectrum_item[0]
      if resultant_spectrum >= 75000: #a requested spectrum must be of at least 75GHz
          final_spectrum_options.append(spectrum_item)

  # decides the final spectrum slot
  selected_spectrum = []
  previous_difference = 0
  if final_spectrum_options:
    # Best-Fit selection procedure
    for spectrum_option_item in final_spectrum_options:
      spectrum_difference = spectrum_option_item[1] - spectrum_option_item[0]
      selected_spectrum = spectrum_option_item
      if spectrum_difference == capacity:
        # EXACT FIT, we take this slot
        break
      elif spectrum_difference > capacity:
        # BEST FIT
        if spectrum_difference < previous_difference or previous_difference == 0:
          previous_difference = spectrum_difference
          selected_spectrum = spectrum_option_item
      else:
        print("Looking the next spectrum possibility.")

  return selected_spectrum

# Used to find the common available spectrum slots, called by the spectrum_assignment function
# https://stackoverflow.com/questions/40367461/intersection-of-two-lists-of-ranges-in-python/40368603
def intersections(a,b):
  ranges = []
  i = j = 0
  while i < len(a) and j < len(b):
      a_left, a_right = a[i]
      b_left, b_right = b[j]

      if a_right < b_right:
          i += 1
      else:
          j += 1

      if a_right >= b_left and b_right >= a_left:
          end_pts = sorted([a_left, a_right, b_left, b_right])
          middle = [end_pts[1], end_pts[2]]
          ranges.append(middle)

  ri = 0
  while ri < len(ranges)-1:
      if ranges[ri][1] == ranges[ri+1][0]:
          ranges[ri:ri+2] = [[ranges[ri][0], ranges[ri+1][1]]]

      ri += 1
  
  return ranges

#To update the available spectrum ranges based on the supported and occupied
#https://stackoverflow.com/questions/51905210/python-delete-subinterval-from-an-interval