#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
import networkx as nx
import matplotlib.pyplot as plt
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
        node_element["uuid"] = local_context["tapi-common:context"]["uuid"]
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

# TODO: TO CHECK Virtual Link abstraction procedure
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
    
    #TEMPORAL graph used to define the virtual links
    G = nx.MultiDiGraph()

    for node_item in topology_item["node"]:
      G.add_node(node_item["uuid"])

    # virtual links design among nodes with SIPs
    for link_item in topology_item["link"]:
      # adds all the existing links into de graph
      node1 = link_item["node-edge-point"][0]["node-uuid"]
      node_edge_point1 = link_item["node-edge-point"][0]["node-edge-point-uuid"]
      node2 = link_item["node-edge-point"][1]["node-uuid"]
      node_edge_point2 = link_item["node-edge-point"][1]["node-edge-point-uuid"]
      G.add_edge(node1, node2, n1=node1, nep1=node_edge_point1, n2=node2, nep2=node_edge_point2)

    # Create abstracted vlink topology based on the transparent model
    topology_element["uuid"] = topology_item["uuid"]
    topology_element["layer-protocol-name"] = topology_item["layer-protocol-name"]
    topology_element["name"] = topology_item["name"]

    # nodes selection based on having SIPs (selected) or not
    for node_item in topology_item["node"]:
      for owned_nep_item in node_item["owned-node-edge-point"]:
          if "mapped-service-interface-point" in owned_nep_item:
              node_list.append(node_item)
              nodes_sips_list.append(node_item["uuid"])
              break
    topology_element["node"] = node_list

    # vlinks creation based on shortest routes between nodes with SIPs
    for node_source_item in list(G.nodes):
      for node_destination_item in list(G.nodes):
        if (node_source_item != node_destination_item) and (node_source_item in nodes_sips_list) and (node_destination_item in nodes_sips_list):
          vlink = {}
          name = []
          neps = []
          
          # prepares the basic information definning the virtual link to be added
          vlink["uuid"] = str(uuid.uuid4())
          name.append({"value-name": "local-name", "value": node_source_item +"_"+ node_destination_item})
          vlink["direction"] = "UNIDIRECTIONAL"
          lpn = []
          lpn.append("PHOTONIC_MEDIA")
          vlink["layer-protocol-name"] = lpn

          # generates the route between nodes with SIPs definning the virtual link to be added
          route = nx.shortest_path(G, source=node_source_item, target=node_destination_item)
          length_route = len(route)
          hops_number = len(route) - 1
          name.append({"value-name": "weight", "value": hops_number})
          vlink["name"] = name
          
          # extract information of first and last links in the route
          first_link = G.get_edge_data(route[0], route[1])
          first_link_info = first_link[0]
          first_node = {}
          first_node["topology-uuid"] = topology_item["uuid"]
          first_node["node-uuid"] = first_link_info["n1"]
          first_node["node-edge-point-uuid"] = first_link_info["nep1"]
          neps.append(first_node)

          last_link = G.get_edge_data(route [length_route-2], route[length_route-1])
          last_link_info = last_link[0]
          second_node = {}
          second_node["topology-uuid"] = topology_item["uuid"]
          second_node["node-uuid"] = last_link_info["n2"]
          second_node["node-edge-point-uuid"] = last_link_info["nep2"]
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
    #settings.logger.debug("VL_COMP: Topology within the received context.")
    # adds all the nodes in the abstracted topology
    for node_item in topology_item["node"]:
      #NOTE: the context-uuid is used to differentiate between nodes of different domains with equal uuid
      node_name = str(context_json["tapi-common:context"]["uuid"]+":"+node_item["uuid"])
      e2e_topology_graph.add_node(node_name)
    settings.logger.debug("VL_COMP: External context nodes added.")

    # adds all the (unidirectional) topology links in the abstracted VLINK and TRANSPARENT
    if topology_item["link"]:
      for link_item in topology_item["link"]:
        # e2e_topology_graph.add_edge(node_1["uuid"], node_2["uuid"], uuid=interdomain_link_item["uuid"])
        cont = context_json["tapi-common:context"]["uuid"]
        l_uuid = link_item["uuid"]
        topo = link_item["node-edge-point"][0]["topology-uuid"]
        node1 = link_item["node-edge-point"][0]["node-uuid"]
        node_edge_point1 = link_item["node-edge-point"][0]["node-edge-point-uuid"]
        node2 = link_item["node-edge-point"][1]["node-uuid"]
        node_edge_point2 = link_item["node-edge-point"][1]["node-edge-point-uuid"]

        #NOTE: the context-uuid is used to differentiat between nodes of different domains with equal uuid
        node_src = str(context_json["tapi-common:context"]["uuid"]+":"+node1)
        node_dst = str(context_json["tapi-common:context"]["uuid"]+":"+node2)

        # add unidirectional edges
        if os.environ.get("ABSTRACION_MODEL") == "vlink":
          # Each edge has a weight when using the VLINK mode
          for link_info in link_item["name"]:
            if link_info["value-name"] == "weight":
              weight_info = link_info["value"]
              e2e_topology_graph.add_edge(node_src, node_dst, weight = weight_info, link_uuid = l_uuid, context = cont, topology=topo, n1=node1, nep1=node_edge_point1, n2=node2, nep2=node_edge_point2)
        else:
          e2e_topology_graph.add_edge(node_src, node_dst, link_uuid = l_uuid, context = cont, topology=topo, n1=node1, nep1=node_edge_point1, n2=node2, nep2=node_edge_point2)
      settings.logger.debug("VL_COMP: External context links added.")  

  settings.logger.info("VL_COMP: External SDN context added.")

# updates the e2e graph by adding new domains and itner-domains links.
def add_idl_e2e_graph(e2e_json):
  settings.logger.debug("VL_COMP: Adding IDLs to the local E2E Context graph.")
  # adds all the SDN domains defined in the json
  for domain_item in e2e_json["e2e-topology"]["nodes-list"]:
    e2e_topology_graph.add_node(domain_item)

  settings.logger.debug("VL_COMP: Nodes added, adding links to E2E graph")
  # add the links interconnecting the SDN domains defined in the json IF 
  for interdomain_link_item in e2e_json["e2e-topology"]["interdomain-links"]:
    settings.logger.debug("IDL NAME: " +str(interdomain_link_item["name"]))
    for link_option_item in interdomain_link_item["link-options"]:
      node_1 = link_option_item["nodes-direction"]["node-1"]
      node_2 = link_option_item["nodes-direction"]["node-2"]
      uuid_idl = link_option_item["uuid"]
      response = e2e_topology_graph.has_edge(node_1, node_2)     
      if response == True:
        settings.logger.debug("IDL already existing.")
        pass
      else:
        # add edge with weight only for VLINK mode
        if os.environ.get("ABSTRACION_MODEL") == "vlink":
          e2e_topology_graph.add_edge(node_1, node_2, weight=1, interdomain_link_uuid=uuid_idl)
        else:
          e2e_topology_graph.add_edge(node_1, node_2, interdomain_link_uuid=uuid_idl)

  settings.logger.debug("VL_COMP: Added Edges to E2E Graph.")
  settings.logger.info("VL_COMP: Set of IDLs added.")

# paints the graph
def paint_graph(labels):
  if labels == "False":
    nx.draw_networkx(e2e_topology_graph, with_labels=False)
  else:
    nx.draw_networkx(e2e_topology_graph)
  
  plt.show()
  return {"msg":"Graph painted"}, 200

# give the node in the graph
def get_nodes():
  settings.logger.info("List of nodes: ")
  settings.logger.info(str(list(e2e_topology_graph.nodes)))
  settings.logger.info("List of edges: ")
  settings.logger.info(str(list(e2e_topology_graph.edges(data=True))))

# computes the K-shortest simple path between two compute domains
def find_path(src, dst):
  path_nodes_list = []
  K = 20 # we will keep the 20 shortest paths generated

  # calculates the route based on the virtual link weights. For the other abstraction models, the edges weight is 1.
  if os.environ.get("ABSTRACION_MODEL") == "vlink":
    settings.logger.debug("VL_COMP: Calculating routes for the VLINK")
    simple_path_list = ([p for p in nx.all_shortest_paths(e2e_topology_graph, source=src, target=dst, weight='weight')])
    simple_path_list.sort(key=len)
  else:
    #simple_path_list = ([p for p in nx.all_shortest_paths(e2e_topology_graph, source=src, target=dst)])
    simple_path_list = ([p for p in nx.all_simple_paths(e2e_topology_graph, source=src, target=dst)])
    simple_path_list.sort(key=len)
  #settings.logger.debug("VL_COMP: All the routes: " + str(simple_path_list))
  #if there are less than 20 paths, we take them all.
  if len(simple_path_list) < K:
    K = len(simple_path_list)
  for path in islice(simple_path_list, K):
    path_nodes_list.append(path)

  return path_nodes_list


# Based on a given route, looks for the specific NEPs involved in the inter-domain links
def node2nep_route_mapping(route, e2e_topology, capacity):
  settings.logger.debug("Starting the mapping from nodes to neps route.")
  route_neps = []
  route_interdominlinks = []
  idl_counter = 0       # it allows to identify if the E2E CS is composed of a single domain CS.
  # it gets the list of neps based on the order of nodes in the route
  for idx, route_item in enumerate(route):
    neps_found = False
    # as long as the current route_item is not the last, enters as it works in pairs.
    if idx < (len(route)-1):
      # gets the data of the edge defined by the source & destination
      response = e2e_topology_graph.get_edge_data(route_item, route[idx+1])
      settings.logger.debug("EDGE INFO: " + str(response))
      # link belongs to an interdomain link
      #NOTE: all this could be reduced and similar to the context (else) if the OLS would manage NEP with multiple SIPs
      if "interdomain_link_uuid" in response[0].keys():
        settings.logger.debug("VL_COMP: NEPs belonging to an IDL (with SIPS)")
        for idl_item in e2e_topology["e2e-topology"]["interdomain-links"]:
          # the correct IDL is found
          if route_item in idl_item["nodes-involved"] and route[idx+1] in idl_item["nodes-involved"]:
            # looks which on of the two direction link-option to take
            for link_option_item in idl_item["link-options"]:
              # the correct direction link is found (working with multi-digraph)
              if link_option_item["uuid"] == response[0]["interdomain_link_uuid"]:
                # checks if this NEP has enough available spectrum  to fit the requested capacity
                available_spectrum = link_option_item["available-spectrum"]
                availability = False
                for available_item in available_spectrum:
                  available_diff = available_item["upper-frequency"] - available_item["lower-frequency"]
                  if (available_diff >= capacity):
                    settings.logger.debug("There is available spectrum")
                    availability = True
                    break
                
                # if False, the NEp is not good, and another route is necessary
                if availability == False:
                  settings.logger.debug("This IDL has not enough available spectrum for the requested capacity.")
                  route_neps = []
                  route_interdominlinks = []
                  return route_neps, route_interdominlinks
                
                #NOTE: the physical-options are a list of NEPs sharing the same spectrum to simulate a NEp with multi-sips.
                # found the right IDL and direction, taking the first physical nep pair available among all the possibilities.
                for physical_option_item in link_option_item["physical-options"]:
                  # the first one without occupied-spectrum is good.
                  if physical_option_item["occupied-spectrum"] == []:
                    settings.logger.debug("Found free physical-option.")
                    # gets nep 1 info from the e2e_topology 6 adds it into the route-neps
                    new_nep_ouput = {}
                    new_nep_ouput["type_link"] = "IDL"
                    new_nep_ouput["link_uuid"] = link_option_item["uuid"]
                    new_nep_ouput["context_uuid"] = physical_option_item["node-edge-point"][0]["context-uuid"]
                    new_nep_ouput["node_uuid"] = physical_option_item["node-edge-point"][0]["node-uuid"]
                    new_nep_ouput["nep_uuid"] = physical_option_item["node-edge-point"][0]["nep-uuid"]
                    new_nep_ouput["direction"] = "OUTPUT"
                    route_neps.append(new_nep_ouput)
                    # gets nep 2 info from the e2e_topology 6 adds it into the route-neps
                    new_nep_inpout = {}
                    new_nep_inpout["type_link"] = "IDL"
                    new_nep_inpout["link_uuid"] = link_option_item["uuid"]
                    new_nep_inpout["context_uuid"] = physical_option_item["node-edge-point"][1]["context-uuid"]
                    new_nep_inpout["node_uuid"] = physical_option_item["node-edge-point"][1]["node-uuid"]
                    new_nep_inpout["nep_uuid"] = physical_option_item["node-edge-point"][1]["nep-uuid"]
                    new_nep_inpout["direction"] = "INPUT"
                    route_neps.append(new_nep_inpout)
                    # keeps the IDL spectrum availability so later we can validate the route spectrum continuity
                    available_spec_list = []
                    for available_spec_item in link_option_item["available-spectrum"]:
                      new_available = []
                      new_available.append(available_spec_item["lower-frequency"])
                      new_available.append(available_spec_item["upper-frequency"])
                      available_spec_list.append(new_available)

                    new_idl = {}
                    new_idl["link-option-uuid"] = link_option_item["uuid"]
                    new_idl["available-spectrum"] = available_spec_list
                    route_interdominlinks.append(new_idl)
                    idl_counter = idl_counter + 1
                    neps_found = True
                    break
                  else:
                    settings.logger.debug("NO physical-option available.")
              else:
                settings.logger.debug("VL_COMP: Looking the other link-option")
            
            # if nnone of the two link-options are good, we need another route.
            if neps_found == False:
              settings.logger.info("VL_COMP: Set of link-options not good. Check another route")
              route_neps = []
              route_interdominlinks = []
              return route_neps, route_interdominlinks
          else:
            settings.logger.debug("VL_COMP: Looking if the next IDL is the good one.")
          if neps_found:
            break
        if neps_found == False:
          settings.logger.debug("VL_COMP: NO link FOUND with this information.")
          route_neps = []
          route_interdominlinks = []
          return route_neps, route_interdominlinks
      else:
        settings.logger.debug("VL_COMP: NEPs belonging to an internal link")
        # link belongs to a context
        new_nep_output = {}
        new_nep_output["link_uuid"] = response[0]["link_uuid"]
        new_nep_output["context_uuid"] = response[0]["context"]
        new_nep_output["topology_uuid"] = response[0]["topology"]
        new_nep_output["node_uuid"] = response[0]["n1"]
        new_nep_output["nep_uuid"] = response[0]["nep1"]
        new_nep_output["direction"] = "OUTPUT"
        route_neps.append(new_nep_output)
        new_nep_inpout = {}
        new_nep_inpout["link_uuid"] = response[0]["link_uuid"]
        new_nep_inpout["context_uuid"] = response[0]["context"]
        new_nep_inpout["topology_uuid"] = response[0]["topology"]
        new_nep_inpout["node_uuid"] = response[0]["n2"]
        new_nep_inpout["nep_uuid"] = response[0]["nep2"]
        new_nep_inpout["direction"] = "INPUT"
        route_neps.append(new_nep_inpout)
  
  return route_neps, route_interdominlinks, idl_counter

"""
Example of route_neps = [
    {type_link, link_uuid, context_uuid, node_uuid, nep_uuid, direction},
    {type_link, link_uuid, context_uuid, node_uuid, nep_uuid, direction},
    {link_uuid, context_uuid, topology_uuid, node_uuid, nep_uuid, direction},
    {link_uuid, context_uuid, topology_uuid, node_uuid, nep_uuid, direction},
    {type_link, link_uuid, context_uuid, node_uuid, nep_uuid, direction},
    {type_link, link_uuid, context_uuid, node_uuid, nep_uuid, direction}
  ]
Example of route_interdominlinks = [
    {"link-option-uuid", "available_spectrum"},
    {"link-option-uuid":"uuid", "available_spectrum":[[low-freq, up-freq],[low-freq, up-freq]]}
  ]
"""
# based on the NEPs route, it looks for the corresponding SIPs to define the CSs
def nep2sip_route_mapping(route_neps, e2e_cs_request, capacity):
  settings.logger.debug("Starting the mappping from neps to sips route.")
  route_sips = []
  route_spectrum = []
  route_links = []        # used only in transparent abstraction mode
  route_nodes_info = []
  domain_context = {}
  
  # if source and destination are the same node, no need to clacluate internal nodes as there arent.
  if e2e_cs_request["source"]["context_uuid"] == e2e_cs_request["destination"]["context_uuid"] and e2e_cs_request["source"]["node_uuid"] == e2e_cs_request["destination"]["node_uuid"]:
    # does nothing and goes to the FIRST and LAST SIP (below)
    pass
  else:
    # maps intermediate NEPs to intermediate SIPs
    for idx, nep_item  in enumerate(route_neps):
      settings.logger.debug("Checking NEP item with id: " + str(nep_item["nep_uuid"]))
      # get the specific context to discover the correct SIP to use attached to the link under study
      # requests the context only when two followed neps belong to a different context.
      if domain_context == {} or nep_item["context_uuid"] != route_neps[idx-1]["context_uuid"]:
        response = bl_mapper.get_context_from_blockchain(nep_item["context_uuid"])
        domain_context = response[0]['context']
      
      # looks into all the nodes of the incoming context-topology (we consider there is only one topology per context)
      for node_item in domain_context["tapi-common:context"]["tapi-topology:topology-context"]["topology"][0]["node"]:
        # looks the neps in the node
        found_nep = False
        for owned_nep_item in node_item["owned-node-edge-point"]:
          if owned_nep_item["uuid"] == nep_item["nep_uuid"]:
            found_nep = True
            found_sip = False
            if 'mapped-service-interface-point' in owned_nep_item.keys():
              settings.logger.debug("Client NEP")
              # NOTE: VNODE will only enter in here, never in the associated else as it has only neps with sips
              # looks for the SIP info associated to the nep
              for mapped_sip_item in owned_nep_item["mapped-service-interface-point"]:
                for sip_item in domain_context["tapi-common:context"]["service-interface-point"]:
                  # validates the sips_uuid and their direction coincide
                  if mapped_sip_item["service-interface-point-uuid"] == sip_item["uuid"] and nep_item["direction"]==sip_item["direction"]:
                    # adds the sip element into the sips_route
                    sip_item["context_uuid"] = nep_item["context_uuid"]
                    sip_item["blockchain_owner"] = response[0]['blockchain_owner']
                    route_sips.append(sip_item)
                    found_sip = True
                    route_node_item = {}
                    route_node_item["context_uuid"] = nep_item["context_uuid"]
                    route_node_item["node_uuid"] = nep_item["node_uuid"]
                    route_node_item["nep_uuid"] = nep_item["nep_uuid"]
                    route_node_item["sip_uuid"] = sip_item["uuid"]
                    route_node_item["nep_direction"] = nep_item["direction"]
                    route_node_item["link"] = nep_item["link_uuid"]
                    route_nodes_info.append(route_node_item)
                    break
                if found_sip:
                  break
            else:
              settings.logger.debug("Internal NEP")
              # adds nep info for the complete route info (later saved in the E2E CS data object)
              route_node_item = {}
              route_node_item["context_uuid"] = nep_item["context_uuid"]
              route_node_item["node_uuid"] = nep_item["node_uuid"]
              route_node_item["nep_uuid"] = nep_item["nep_uuid"]
              route_node_item["sip_uuid"] = ""
              route_node_item["nep_direction"] = nep_item["direction"]
              route_node_item["link"] = nep_item["link_uuid"]
              route_nodes_info.append(route_node_item)
              # only the transmitter neps are interesting for the spectrum continuity
              if nep_item["direction"] == "OUTPUT":
                #NOTE: VLINK and TRANSPARENT will access the previous IF and this else as they have internal NEPs
                available_spectrum = owned_nep_item["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["available-spectrum"]
                
                # checks spectrum availability with respect requested capacity & gathers spectrums for the final slot selection.
                availability = False
                available_spec_list = []
                for available_item in available_spectrum:
                  available_diff = available_item["upper-frequency"] - available_item["lower-frequency"]
                  # checks if this NEP has at least one slot with enough available spectrum
                  if (available_diff >= capacity):
                    availability = True
                  
                  # gathers spectrum info, so later the final spectrum can be selected among all the neps.
                  new_available = []
                  new_available.append(available_item["lower-frequency"])
                  new_available.append(available_item["upper-frequency"])
                  available_spec_list.append(new_available)
                
                new_spectrum = {}
                new_spectrum["available-spectrum"] = available_spec_list
                route_spectrum.append(new_spectrum)

                # if it's false, returns no available slot in one of the neps in the route. Based on the previous "if (available_diff >= capacity)"
                if availability == False:
                  # if False, the NEP is not good, and another route is necessary
                  settings.logger.debug("This NEP has not enough available spectrum for the requested capacity.")
                  route_sips = []
                  route_spectrum = []
                  route_links = []
                  route_nodes_info = []
                  return route_sips, route_spectrum, route_links, route_nodes_info

              # adds the links to require their usage (only done in transparent abstraction mode)
              if os.environ.get("ABSTRACION_MODEL") == "transparent" and idx < (len(route_neps)-1):
                next_nep = route_neps[idx+1]
                if nep_item["link_uuid"] == next_nep["link_uuid"]:
                  link_item = {}
                  link_item["uuid"] = nep_item["link_uuid"]
                  link_item["context_uuid"] = nep_item["context_uuid"]
                  route_links.append(link_item)
          if found_nep:
            break
        if found_nep:
          break

  # adds the FIRST SIP in the route_sips, the info to the nodes_route and the spectrum info
  settings.logger.debug("Adding first SIP element.")
  sip_uuid = e2e_cs_request["source"]["context_uuid"]+":"+e2e_cs_request["source"]["sip_uuid"]
  response_json = bl_mapper.get_sip(sip_uuid)
  sip_item = response_json["sip_info"]
  sip_item["context_uuid"] = e2e_cs_request["source"]["context_uuid"]
  sip_item["blockchain_owner"] = response_json["owner"]
  route_sips.insert(0, sip_item)
  
  response_json = bl_mapper.get_node(e2e_cs_request["source"]["context_uuid"], e2e_cs_request["source"]["node_uuid"])
  found_nep = False
  for nep_item in response_json["owned-node-edge-point"]:
    settings.logger.debug("nep_item: "+str(nep_item))
    for sip_item2 in nep_item["mapped-service-interface-point"]:
      settings.logger.debug("sip_item2: "+str(sip_item2))
      settings.logger.debug("sip_item2[service-interface-point-uuid]: "+str(sip_item2["service-interface-point-uuid"]))
      settings.logger.debug("e2e_cs_request[source][sip_uuid]: " +str(e2e_cs_request["source"]["sip_uuid"]))
      if sip_item2["service-interface-point-uuid"] == e2e_cs_request["source"]["sip_uuid"]:
        settings.logger.debug("nep_item[uuid]: "+str(nep_item["uuid"]))
        nep_uuid = nep_item["uuid"]
        found_nep = True
        break
    if found_nep == True:
      break
  
  route_node_item = {}
  route_node_item["context_uuid"] = e2e_cs_request["source"]["context_uuid"]
  route_node_item["node_uuid"] = e2e_cs_request["source"]["node_uuid"]
  route_node_item["nep_uuid"] = nep_uuid
  route_node_item["sip_uuid"] = e2e_cs_request["source"]["sip_uuid"]
  route_node_item["nep_direction"] = "OUTPUT"
  route_nodes_info.insert(0, route_node_item)
  
  # adds the spectrum_info of each SIP (associated NEP) to solve the spectrum continuity later
  available_spec_list = []
  for available_item in sip_item["tapi-photonic-media:media-channel-service-interface-point-spec"]["mc-pool"]["available-spectrum"]:
    new_available = []
    new_available.append(available_item["lower-frequency"])
    new_available.append(available_item["upper-frequency"])
    available_spec_list.append(new_available)

  new_spectrum = {}
  new_spectrum["available-spectrum"] = available_spec_list
  route_spectrum.insert(0, new_spectrum)
  
  # adds the last SIP in the route_sips, the info in the nodes route and the spectrum info
  settings.logger.debug("Adding the last SIP element")
  sip_uuid = e2e_cs_request["destination"]["context_uuid"]+":"+e2e_cs_request["destination"]["sip_uuid"]
  response_json = bl_mapper.get_sip(sip_uuid)
  sip_item = response_json["sip_info"]
  sip_item["context_uuid"] = e2e_cs_request["destination"]["context_uuid"]
  sip_item["blockchain_owner"] = response_json["owner"]
  route_sips.append(sip_item)
  
  response_json = bl_mapper.get_node(e2e_cs_request["destination"]["context_uuid"], e2e_cs_request["destination"]["node_uuid"])
  found_nep = False
  for nep_item in response_json["owned-node-edge-point"]:
    for sip_item2 in nep_item["mapped-service-interface-point"]:
      #settings.logger.debug("sip_item2: "+str(sip_item2))
      #settings.logger.debug("sip_item2[service-interface-point-uuid]: "+str(sip_item2["service-interface-point-uuid"]))
      #settings.logger.debug("e2e_cs_request[source][sip_uuid]: " +str(e2e_cs_request["destination"]["sip_uuid"]))
      if sip_item2["service-interface-point-uuid"] == e2e_cs_request["destination"]["sip_uuid"]:
        nep_uuid = nep_item["uuid"]
        found_nep = True
        break
    if found_nep == True:
      break
  route_node_item = {}
  route_node_item["context_uuid"] = e2e_cs_request["destination"]["context_uuid"]
  route_node_item["node_uuid"] = e2e_cs_request["destination"]["node_uuid"]
  route_node_item["nep_uuid"] = nep_uuid
  route_node_item["sip_uuid"] = e2e_cs_request["destination"]["sip_uuid"]
  route_node_item["nep_direction"] = "INPUT"
  route_nodes_info.append(route_node_item)
  
  # adds the spectrum_info of each SIP (associated NEP) to solve the spectrum continuity later
  available_spec_list = []
  for available_item in sip_item["tapi-photonic-media:media-channel-service-interface-point-spec"]["mc-pool"]["available-spectrum"]:
    new_available = []
    new_available.append(available_item["lower-frequency"])
    new_available.append(available_item["upper-frequency"])
    available_spec_list.append(new_available)

  new_spectrum = {}
  new_spectrum["available-spectrum"] = available_spec_list
  route_spectrum.append(new_spectrum)
  
  return route_sips, route_spectrum, route_links, route_nodes_info

"""
Example of route_sips = [
  {sip_info, "context_uuid", "blockchain_owner"},
  {sip_info, "context_uuid", "blockchain_owner"}
]
# list of links to use in the transparnt mode.
Example of route_links = [
    {uuid, context_uuid},
    {uuid, context_uuid}
]
Example of route_spectrum = [
  {"available_spectrum},
  {"available_spectrum}
]
Example of interoute_nodes_infornal_neps = [
  {context_uuid, node_uuid, nep_uuid, sip_uuid},
  {context_uuid, node_uuid, nep_uuid, sip_uuid},
  {context_uuid, node_uuid, nep_uuid, sip_uuid},
  {context_uuid, node_uuid, nep_uuid, sip_uuid}
]
"""
# Spectrum assignment --> We look for the exact-Fit, otherwise the Best-Fit
def spectrum_assignment(spectrum_list, capacity):
  #spectrum_list = [[UUU,YYY],[ZZZ, TTT]]
  # it checks the availability of all the involved inter-domain links and extract the 
  # common available spectrum bigger than 75GHz
  ref_spectrum = spectrum_list[0]["available-spectrum"]
  for idx, spectrum_item in enumerate(spectrum_list):
    # different than the first item as its the initial reference
    if idx != 0:
      ref_spectrum = intersections(ref_spectrum,spectrum_item["available-spectrum"])

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
        settings.logger.info("Looking the next spectrum possibility.")

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

#Fins the available_spectrum looking the differente beteen the supportable_spectrum(a) and the occupied_spectrum(b)
#https://stackoverflow.com/questions/51905210/python-delete-subinterval-from-an-interval
def available_spectrum(a,b):
  d = []
  i=a[0]
  j=a[1]

  for idx, b_item in enumerate(b):
    start=b_item[0]
    end=b_item[1]
    if i == b_item[0]:
      i=end
    else:
      d.append([i,start])
      i=end
    
    if idx == len(b)-1 and b_item[1] < a[1]:
      d.append([end,j])

  return d
