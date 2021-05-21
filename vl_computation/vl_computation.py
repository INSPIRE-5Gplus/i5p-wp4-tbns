#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
import networkx as nx

from config_files import settings
from blockchain_node import blockchain_node as bl_mapper

# NOTE: e2e_topology is the sum of all SDN topologies to create the E2E topology of the network
e2e_topology_graph = nx.Graph()

""" Example of e2e_topology_json
{
  "e2e-topology": {
    "domain-list": [
      #same uuid than the one in ["tapi-common:context"]["uuid"](abstractedcontextjson)
      "uuid_SDN1",
      "uuid_SDN2",
      "uuid_SDN3"
    ],
    "interdomain-links": [
      {
        "uuid": "uuid",
        "name": "SDN1-SDN2",
        "domain-1": "SDN1",
        "domain-2": "SDN2",
        "link_options": [
          {
            "uuid": "uuid_CD1",
            "domain-1": {
              "uuid": "uuid_SDN1",
              # same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
              "nep_uuid": "nep_C1"
            },
            "domain-2": {
              "uuid": "uuid_SDN2",
              "nep-uuid": "nep_D1"
            },
            "link-direction": [
              {
                "domain-1": "uuid_SDN1",
                "domain-2": "uuid_SDN2",
                "occupied-spectrum": [
                ]
              },
              {
                "domain-1": "uuid_SDN2",
                "domain-2": "uuid_SDN1",
                "occupied-spectrum": [
                ]
              }
            ]
          },
          {
            "uuid": "uuid_CD2",
            "domain-1": {
              "uuid": "uuid_SDN1",
              "nep_uuid": "nep_C2"
            },
            "domain-2": {
              "uuid": "uuid_SDN2",
              "nep-uuid": "nep_D2"
            },
            "link-direction": [
              {
                "domain-1": "uuid_SDN1",
                "domain-2": "uuid_SDN2",
                "occupied-spectrum": [
                ]
              },
              {
                "domain-1": "uuid_SDN2",
                "domain-2": "uuid_SDN1",
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
        "uuid": "uuid",
        "name": "SDN2-SDN4",
        "domain-1": "SDN2",
        "domain-2": "SDN4",
        "link_options": [
          {
            "uuid": "uuid_HM1",
            "domain-1": {
              "uuid": "uuid_SDN2",
              # same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
              "nep_uuid": "nep_H1"
            },
            "domain-2": {
              "uuid": "uuid_SDN4",
              "nep-uuid": "nep_M1"
            },
            "link-direction": [
              {
                "domain-1": "uuid_SDN2",
                "domain-2": "uuid_SDN4",
                "occupied-spectrum": [
                ]
              },
              {
                "domain-1": "uuid_SDN4",
                "domain-2": "uuid_SDN2",
                "occupied-spectrum": [
                ]
              }
            ]
          },
          {
            "uuid": "uuid_HM2",
            "domain-1": {
              "uuid": "uuid_SDN2",
              "nep_uuid": "nep_H2"
            },
            "domain-2": {
              "uuid": "uuid_SDN4",
              "nep-uuid": "nep_M2"
            },
            "link-direction": [
              {
                "domain-1": "uuid_SDN2",
                "domain-2": "uuid_SDN4",
                "occupied-spectrum": [
                ]
              },
              {
                "domain-1": "uuid_SDN4",
                "domain-2": "uuid_SDN2",
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
              "adjustment-granularity": "G_75GHZ",
              "grid-type": "DWDM"
            }
          }
        ],
        "available_spectrum": [
          {
            "lower-frequency": 191700000,
            "upper-frequency": 196100000,
            "frequency-constraint": {
              "adjustment-granularity": "G_75GHZ",
              "grid-type": "DWDM"
            }
          }
        ]
      }
    ]
  }
}
"""

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
    #TODO: solve error, there are duplicated nodes... WHY???
    for node_item in topology_item["node"]:
      G.add_node(node_item["uuid"])
      for owned_nep_item in node_item["owned-node-edge-point"]:
          if "mapped-service-interface-point" in owned_nep_item:
              node_list.append(node_item)
              nodes_sips_list.append(node_item["uuid"])
              break

    topology_element["node"] = node_list

    # virtual links design among nodes with SIPs
    for link_item in topology_item["link"]:
      # adds all the existing links into de graph
      node1 = link_item["node-edge-point"][0]["node-uuid"]
      node2 = link_item["node-edge-point"][1]["node-uuid"]
      G.add_edge(node1, node2, n1=node1, nep1= link_item["node-edge-point"][0]["node-edge-point-uuid"], n2=node2, nep2=link_item["node-edge-point"][1]["node-edge-point-uuid"])

    # Creates the VLINKs based on shortest routes between nodes with SIPs
    for node_source_item in list(G.nodes):
      for node_destination_item in list(G.nodes):
          #TODO: VALIDAR QUE TAN UN COM L?ALTRE SÓN NODES AMB SIPS
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

# creates the initial e2e graph with itself as a single node
def init_e2e_graph(context_json):
  for topology_item in context_json["tapi-common:context"]["tapi-topology:topology-context"]["topology"]:
    e2e_topology_graph.add_node(topology_item["uuid"])

# updates the e2e graph by adding new domains and itner-domains links.
def add_node_e2e_graph(e2e_json):
    # adds all the SDN domains defined in the json
    for domain_item in e2e_json["e2e-topology"]["domain-list"]:
        e2e_topology_graph.add_node(domain_item)
    
    # add the links interconnecting the SDN domains defined in the json
    for interdomain_link_item in e2e_json["e2e-topology"]["interdomina-links"]:
        node_1 = interdomain_link_item["node-1"]
        node_2 = interdomain_link_item["node-2"]
        e2e_topology_graph.add_edge(node_1["uuid"], node_2["uuid"], uuid=interdomain_link_item["uuid+"])

# computes the path between two compute domains
def find_path(src, dst):
    #path_nodes_list = nx.shortest_path(e2e_topology_graph, src, dst)
    simple_path_list = nx.all_simple_paths(e2e_topology_graph, src, dst, cutoff=4)
    path_nodes_list = list(sorted(simple_path_list, key = len))   
    return path_nodes_list

# Based on a given route, looks for the specific NEPs involved in the inter-domain links
def domain2nep_route_mapping(route_domain, e2e_topology):
  route_neps = []
  route_interdominlinks = []
  for idx, route_domain_item in enumerate(route_domain):
    link_found = False
    if route_domain[idx] != len(route_domain-1):
      for inter_link_item in e2e_topology["interdomain-links"]:
        if ((route_domain_item == inter_link_item["domain-1"] and route_domain[idx+1] == inter_link_item["domain-2"]) or \
          (route_domain_item == inter_link_item["domain-2"] and route_domain_item[idx+1] == inter_link_item["domain-1"])):
          #NOTE: this FOR loop is to manage a set of physical links that share the spectrum as if they would be a single one with different SIPs
          for link_option_item in inter_link_item["link-options"]:
            # Checking the directionality of the route.
            for option_direction_item in link_option_item["link-direction"]:
              if (route_domain_item == option_direction_item["domain-1"] and \
                route_domain[idx+1] == option_direction_item["domain-2"] and not option_direction_item["occupied-spectrum"]):
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
                if route_domain_item == link_option_item["domain-1"]["uuid"]:
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
    {contextdomain_uuid, nep_uuid, direction},
    {contextdomain_uuid, nep_uuid, direction},
    {contextdomain_uuid, nep_uuid, direction},
    {contextdomain_uuid, nep_uuid, direction}
  ]
"""
# Based the route of NEPs, looks for the corresponding SIPs to define the CSs
def nep2sip_route_mapping(route_neps, e2e_cs_request):
  found_nep = {}
  route_sips = []
  #maps intermediate NEPs to intermediate SIPs
  for nep_item in route_neps:
    #get specific domain topology to discover the correct SIP to use
    response = bl_mapper.context_from_blockchain(nep_item["contextdomain_uuid"])
    domain_context = response['context']
    owned_nep_list = domain_context["tapi-common:context"]["tapi-topology:topology-context"]["topology"][0]["node"][0]["owned-node-edge-point"]
    for owned_nep_item in owned_nep_list:
      if owned_nep_item["uuid"] == nep_item["nep_uuid"]:
        found_nep = owned_nep_item
        break
    found_sip = False
    for mapped_sip_item in found_nep["mapped-service-interface-point"]:
      for sip_item in domain_context["tapi-common:context"]["service-interface-point"]:
        if mapped_sip_item["service-interface-point-uuid"] == sip_item["uuid"] and nep_item["direction"]==sip_item["direction"]:
          sip_item["blockchain_owner"] = response['blockchain_owner']
          route_sips.append(sip_item)
          found_sip = True
          break
      if found_sip:
        break
  
  #adds the FIRST SIP in the route
  response = bl_mapper.context_from_blockchain(e2e_cs_request["domain-source"]["uuid"])
  for sip_item in response["context"]["tapi-common:context"]["service-interface-point"]:
        if sip_item["uuid"] == e2e_cs_request["domain-source"]["sip"]:
          sip_item["blockchain_owner"] = response['blockchain_owner']
          route_sips.insert(0, sip_item)
  
  #adds the last SIP in the route
  response = bl_mapper.context_from_blockchain(e2e_cs_request["domain-destination"]["uuid"])
  for sip_item in response["context"]["tapi-common:context"]["service-interface-point"]:
        if sip_item["uuid"] == e2e_cs_request["domain-source"]["sip"]:
          sip_item["blockchain_owner"] = response['blockchain_owner']
          route_sips.append(sip_item)
  
  return route_sips

"""
Example of route_interdominlinks = [
    {"uuid", "link-option-uuid", "available_spectrum"},
    {"uuid", "link-option-uuid", "available_spectrum"}
  ]
"""
# Spectrum assignment --> We look for the exact-Fit, otherwise the Best-Fit
def spectrum_assignment(route_interdominlinks, capacity):  
  # it checks the availability of all the involved inter-domain links and extract the 
  # common available spectrum bigger than 75GHz
  ref_spectrum = route_interdominlinks[0]["available_spectrum"]
  for idx, route_interdomainlink_item in enumerate(route_interdominlinks):
      if idx != 0:
          spectrum_item = route_interdomainlink_item["available_spectrum"]
          ref_spectrum = intersections(ref_spectrum,spectrum_item)

  final_spectrum_options = []
  for spectrum_item in ref_spectrum:
      resultant_spectrum = spectrum_item[1] - spectrum_item[0]
      if resultant_spectrum >= 75000: #a requested spectrum must be of at least 75GHz
          final_spectrum_options.append(spectrum_item)

  # final_spectrum_options is a list of possible spectrum_slots to be used
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