#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
from threading import Lock

from slice_subnet_mapper import slice_subnet_mapper as slice_mapper
from blockchain_node import blockchain_node as bl_mapper
from sdn_mapper import sdn_mapper
from database import database as db
from config_files import settings
from vl_computation import vl_computation


# mutex used to ensure a single access to each one of the three local DB (slices, blockchain_subnets, connectivity services)
mutex_slice2db_access = Lock()
mutex_slice2blockchaindb_access = Lock()
mutex_local_csdb_access = Lock()
mutex_e2e_csdb_access = Lock()

################################### NETWORK SLICE SUBNETS TEMPLATE FUNCTIONS ###################################
#### LOCAL DOMAIN
# NOTE: returns the slices templates information in the local domain.
def get_local_slicesubnet_templates():
    response = slice_mapper.get_all_slice_subnet_templates()
    return response[0], 200

# NOTE: returns the slice template information placed in the local domain with a specific ID.
def get_local_slicesubnet_template(slice_ID):
    response = slice_mapper.get_slice_subnet_template(slice_ID)
    return response[0], 200

#### BLOCKCHAIN DOMAIN
# NOTE: adds a slice template into the blockchain to be shared
def slicesubnet_template_to_bl(slice_ID):
    # gets NST from local NSM and selects the necessary information
    response = slice_mapper.get_slice_subnet_template(slice_ID)
    local_nst_json = json.loads(response[0])
    bl_nst_json = {}
    bl_nst_json['id'] = local_nst_json['uuid']
    bl_nst_json['name'] = local_nst_json['nstd']['name']
    bl_nst_json['version'] = local_nst_json['nstd']['version']
    bl_nst_json['vendor'] = local_nst_json['nstd']['vendor']
    bl_nst_json['price'] = 1
    bl_nst_json['unit'] = "eth"
    #give the nst to the Blockchain mapper to distribute it with the other peers.
    response = bl_mapper.slice_to_blockchain(bl_nst_json)
    return response[0], 200

# TODO: returns the slice-subnet templates information in the blockchain without those belonging to the local domain.
def get_bl_slicesubnet_templates():
    return 200

# NOTE: returns the slice-subnet template information placed in the blockchain with a specific ID.
def get_bl_slicesubnet_template(slice_ID):
    response = bl_mapper.slice_from_blockchain(slice_ID)
    return response, 200

# NOTE: returns all the slice-subnets (NSTs) available locally and in the blockchain peers.
def get_slicessubnets_templates():
    # gets local slice-subnets
    response = slice_mapper.get_all_slice_subnet_templates()
    local_slicesubnets_list = json.loads(response[0])

    # gets blockchain slice-subnets
    subnet_list_length = bl_mapper.get_slices_counter()
    blockchain_slicesubnets_list = []
    index_list = 0
    while (index_list < subnet_list_length):
        found = False
        subnet_ID_item = bl_mapper.get_slice_id(index_list)
        if local_slicesubnets_list:
            for subnet_item in local_slicesubnets_list:
                if subnet_item['uuid'] == subnet_ID_item:
                    found = True
                    break
        
        if found == False:
            nst_element = bl_mapper.slice_from_blockchain(subnet_ID_item)            
            blockchain_slicesubnets_list.append(nst_element[0])
        index_list += 1
    
    slicesubnets_list = local_slicesubnets_list + blockchain_slicesubnets_list
    return slicesubnets_list, 200


######################################## SDN TRANSPORT CONTEXT FUNCTIONS ########################################
# adds the Inter-domin links and distributes them and the domain context in the blockchain
def idl_to_bl(idl_json):
    settings.logger.info("ORCH: Received IDL and context to distribute.")
    # FIRST: updates the local graph containning the e2e tpology
    vl_computation.add_idl_e2e_graph(idl_json)
    
    settings.logger.info("ORCH: Get E2E topology from BL.")
    # SECOND: gets current e2e_topology, adds new nodes & IDLs (if they are not already in there) and distributes both json to the blockchain peers  
    response = bl_mapper.get_e2etopology_from_blockchain()
    e2e_nodes_list = []
    
    if response[0] == "empty":
        e2e_topology = {}
        e2e_topo = {}
        e2e_topo["nodes-list"] = []
        e2e_topo["interdomain-links"] = []
        temp_idls = []
        
        for node_item in idl_json["e2e-topology"]["nodes-list"]:
            e2e_nodes_list.append(node_item)
        e2e_topo["nodes-list"] = e2e_nodes_list
        
        
        for idl_item in idl_json["e2e-topology"]["interdomain-links"]:
            linkoptions_uuid_list = []
            temp_idl_item = {}
            for linkoption_item in idl_item["link-options"]:
                linkoptions_uuid_list.append(linkoption_item["uuid"])
                response = bl_mapper.linkoption_to_blockchain(linkoption_item)
            
            temp_idl_item["name"] = idl_item["name"]
            temp_idl_item["nodes-involved"] = idl_item["nodes-involved"]
            temp_idl_item["link-options"] = linkoptions_uuid_list
            temp_idls.append(temp_idl_item)            

        e2e_topo["interdomain-links"] = temp_idls
        e2e_topology["e2e-topology"] = e2e_topo
    else:
        e2e_topology = response[0]
        e2e_nodes_list = e2e_topology["e2e-topology"]["nodes-list"]
        # compares the nodes in the distributed e2e topology and the intcoming IDL
        for node_item in idl_json["e2e-topology"]["nodes-list"]:
            # if a node is not in the e2e_topology, it is added
            if node_item not in e2e_nodes_list:
                e2e_nodes_list.append(node_item)
        e2e_topology["e2e-topology"]["nodes-list"] = e2e_nodes_list

        # compares the existing IDl with those in the incoming idl_json
        e2e_idl_list = e2e_topology["e2e-topology"]["interdomain-links"]
        for idl_item in idl_json["e2e-topology"]["interdomain-links"]:
            linkoptions_uuid_list = []
            found_existing_idl = False
            for ref_idl in e2e_idl_list:
                if idl_item["name"] == ref_idl["name"]:
                    found_existing_idl = True
                    break
            if found_existing_idl == False:
                temp_idl_item = {}
                for linkoption_item in idl_item["link-options"]:
                    linkoptions_uuid_list.append(linkoption_item["uuid"])
                    response = bl_mapper.linkoption_to_blockchain(linkoption_item)

                temp_idl_item["name"] = idl_item["name"]
                temp_idl_item["nodes-involved"] = idl_item["nodes-involved"]
                temp_idl_item["link-options"] = linkoptions_uuid_list
                e2e_idl_list.append(temp_idl_item) 

        e2e_topology["e2e-topology"]["interdomain-links"]=e2e_idl_list

    settings.logger.info("ORCH: Local E2E graph updated, distributing it and the IDLs.")
    response = bl_mapper.interdomainlinks_to_blockchain(idl_json, e2e_topology)
    if response[1] != 200:
        return ({"msg":"ERROR - Something went wrong when distributing IDL info."}, 400)

    return ({"msg":"Interdomain-Links and Domain SDN Context distributed."}, 200)

# adds the Inter-domin links and distributes them and the domain context in the blockchain
def context_to_bl():
    settings.logger.info("ORCH: Preparing the context to be distributed.")
    # gets the local context
    abstracted_sdn_context = db.get_element("", "context")
    
    # divides the context in smaller parts (string) due to the Blockchain limitations with JSONs and string length
    context_json = {}
    context_json["id"] = abstracted_sdn_context["tapi-common:context"]["uuid"]
    context_json["name_context"] = json.dumps(abstracted_sdn_context["tapi-common:context"]["name"])
    context_json["sip"] = json.dumps(abstracted_sdn_context["tapi-common:context"]["service-interface-point"])
    context_json["nw_topo_serv"] = json.dumps(abstracted_sdn_context["tapi-common:context"]["tapi-topology:topology-context"]["nw-topology-service"])
    topo_metadata = {}
    topo_metadata["uuid"] = abstracted_sdn_context["tapi-common:context"]["tapi-topology:topology-context"]["topology"][0]["uuid"]
    topo_metadata["layer-protocol-name"] = abstracted_sdn_context["tapi-common:context"]["tapi-topology:topology-context"]["topology"][0]["layer-protocol-name"]
    topo_metadata["name"] = abstracted_sdn_context["tapi-common:context"]["tapi-topology:topology-context"]["topology"][0]["name"]
    context_json["topo_metadata"] = json.dumps(topo_metadata)
    context_json["node_topo"] = json.dumps(abstracted_sdn_context["tapi-common:context"]["tapi-topology:topology-context"]["topology"][0]["node"])
    context_json["link_topo"] = json.dumps(abstracted_sdn_context["tapi-common:context"]["tapi-topology:topology-context"]["topology"][0]["link"])

    # distributes the local sdn context with the other peers
    response = bl_mapper.context_to_blockchain(context_json)
    settings.logger.info("ORCH: Local context distributed.")
    msg = "Domain SDN Context distributed with status: " + str(response["status"])
    return ({"msg":msg}, 200)

# adds the inter-domain links information coming from another peer to the E2E local graph
def add_idl_info(blockchain_domain_json):
    settings.logger.info("ORCH: Adding inter-domain links to the E2E graph for path conmputation.")
    vl_computation.add_idl_e2e_graph(blockchain_domain_json)

# adds the SDN domain context information coming from another peer to the E2E local graph
def add_context_info(context_json):
    settings.logger.info("ORCH: Adding external SDN domain context information in the E2E Network graph." + str(context_json["uuid"]))
    tapi_context_json={}
    tapi_common_context = {}
    tapi_topology_context = {}
    topology = []
    topology_element = {}
    
    response = bl_mapper.get_context_sips_nodes_links_from_blockchain(context_json)
    response_json = response[0]
    tapi_common_context["uuid"] = response_json["uuid"]
    tapi_common_context["name"] = response_json["name_context"]
    sips = []
    for sip_item_string in response_json["sip"]:
        sip_item_json = json.loads(sip_item_string)
        sips.append(sip_item_json)
    tapi_common_context["service-interface-point"] = sips
    topo_metadata = json.loads(response_json["topo_metadata"])
    topology_element["uuid"] = topo_metadata["uuid"]
    topology_element["layer-protocol-name"] = topo_metadata["layer-protocol-name"]
    topology_element["name"] = topo_metadata["name"]
    nodes = []
    for node_item_string in response_json["node_topo"]:
        node_item_json = json.loads(node_item_string)
        nodes.append(node_item_json)
    topology_element["node"] = nodes
    links = []
    for link_item_string in response_json["link_topo"]:
        link_item_json = json.loads(link_item_string)
        links.append(link_item_json)
    topology_element["link"] = links
    topology.append(topology_element)
    tapi_topology_context["nw-topology-service"] = json.loads(response_json["nw_topo_serv"])
    tapi_topology_context["topology"] = topology
    tapi_common_context["tapi-topology:topology-context"] = tapi_topology_context
    tapi_context_json["tapi-common:context"] = tapi_common_context

    vl_computation.add_context_e2e_graph(tapi_context_json)

# returns the transport context information in the local domain
def get_context():
    sdn_ctrl_ip = os.environ.get("SDN_CONTROLLER_IP")
    sdn_ctrl_port = os.environ.get("SDN_CONTROLLER_PORT")
    response = sdn_mapper.get_local_context(sdn_ctrl_ip, sdn_ctrl_port)
    if response[1] == 200:
        return response[0], 200
    else:
        return response[0], 400 

# returns all (local + blockchain) the domain contexts information
def get_all_contexts():
    context_list = []
    
    # get local abstracted context
    local_sdn_context = db.get_element("", "context")
    context_list.append(local_sdn_context)

    # gets blockchain contexts
    context_list_length = bl_mapper.get_context_counter()
    index_list = 0
    while (index_list < context_list_length):
        context_ID_item = bl_mapper.get_context_id(index_list)

        if local_sdn_context["tapi-common:context"]["uuid"] != context_ID_item:
            nst_element = bl_mapper.get_context_from_blockchain(context_ID_item)  
            settings.logger.info('ORCH: Requests Blockchain context nst_element: ' + str(nst_element))          
            context_list.append(nst_element[0])
            
        index_list += 1
    
    settings.logger.info('ORCH: context_list: ' + str(context_list))     
    return context_list, 200

#TODO: get E2E topology function to show the E2E topology (draw with matplotlib)

# manages a local connectivity service configuration process
def instantiate_local_connectivity_service(event_json):
    settings.logger.info("ORCH: Received request to deploy a local CS: " +str(event_json["cs_info"]["uuid"]))
    response = sdn_mapper.instantiate_connectivity_service(event_json["cs_info"], event_json["spectrum"], event_json["capacity"])
    if response[1] == 200:  
        mutex_local_csdb_access.acquire()
        db.add_cs(response[0])
        mutex_local_csdb_access.release()
        event_json["cs_info"]['status'] = "DEPLOYED"
    else:
        settings.logger.error("ERROR deploying local domain CS.")
        event_json["cs_info"]['status'] = "ERROR"
    
    response = bl_mapper.update_blockchain_cs(event_json)

# updates a CS information belonging to another domain (Blockchain)
def update_connectivity_service_from_blockchain(event_json):
    settings.logger.info("ORCH: Updating connectivity services information from another domain.")
    mutex_e2e_csdb_access.acquire()
    e2e_cs_list = db.get_elements("e2e_cs")
    for e2e_cs_item in e2e_cs_list:
        for domain_cs_item in e2e_cs_item["domain-cs"]:
            if domain_cs_item["uuid"] == event_json["id"]:
                domain_cs_item["status"] = "DEPLOYED"
                db.update_db(e2e_cs_item["uuid"], e2e_cs_item, "e2e_cs")
                found_cs = True
                break
        if found_cs == True:
            break
    mutex_e2e_csdb_access.release()

"""
Example E2E_CS request 
    {
        "source": {
            "context_uuid": "uuid",
            "node_uuid": "uuid",
            "sip_uuid": "uuid",
        },
        "destination": {
            "context_uuid": "uuid",
            "node_uuid": "uuid",
            "sip_uuid": "uuid",
        },
        "capacity": {
            "value": 75,
            "unit": "GHz"
        }
    }
Example E2E_CS data object  
  {
    "uuid": "uuid_e2e_cs",
    "status" : "INSTANTIATING/DEPLOYED/TERMINATED",
    "source": {
      "context_uuid": "uuid",
      "node_uuid": "uuid",
      "sip_uuid": "uuid",d",
    },
    "destination": {
      "context_uuid": "uuid",
      "node_uuid": "uuid",
      "sip_uuid": "uuid",
    },
    "capacity": {
      "value": 75,
      "unit": "GHz"
    },
    "spectrum": {
      "upper-frequency": 191700000,
      "lower-frequency": 191850000
    },
    "route-nodes":[
        {context_uuid, node_uuid, nep_uuid, sip_uuid},
        {context_uuid, node_uuid, nep_uuid, sip_uuid}
    ]
    "domain-cs":[
      {
        "uuid": "uuid_CS",
        "context-uuid" : "uuid,
        "address-owner": "blockchain-peer_address",
        "status": "INSTANTIATING/DEPLOYED/TERMINATED",
        "sip-source": "sip_uuid",
        "sip-destination": "sip_uuid",
        "internal-links":[
          "link_uuid",
          "link_uuid"
        ]
      }
    ]
  }
"""
# manages the creation of an E2E CS
#TODO: Create the JSON to send the request to the SDN Controllers.
def instantiate_e2e_connectivity_service(e2e_cs_request):
    settings.logger.info("ORCH: Received E2E request info. Let's process it.")
    # defines e2e CS data object parameters
    e2e_cs_json = {}
    selected_spectrum = []
    sips_route = []
    internal_links_route = []
    
    # gets and prepares the e2e_topology (the set of IDLs definning how the SDN domains are linked)
    response = bl_mapper.get_e2etopology_from_blockchain()
    e2e_topology_json = response[0]
    if e2e_topology_json == "empty":
        return {"msg":"There is no e2e_topology to work with."}
    else:
        # prepares the intedomain-links to compare the existing with the new ones in the IDL json
        for idl_item in e2e_topology_json["e2e-topology"]["interdomain-links"]:
            linkoptions_list = []
            for linkoption_uuid_item in idl_item["link-options"]:
                response = bl_mapper.get_linkOption_from_blockchain(linkoption_uuid_item)
                linkoptions_list.append(response[0])
            idl_item["link-options"] = linkoptions_list
    
    # assigns initial CS data object information
    e2e_cs_json["uuid"] = str(uuid.uuid4())
    e2e_cs_json["source"] = e2e_cs_request["source"]
    e2e_cs_json["destination"] = e2e_cs_request["destination"]
    e2e_cs_json["status"]  = "INSTANTIATING"
    e2e_cs_json["capacity"] = e2e_cs_request["capacity"]
    if e2e_cs_request["capacity"]["unit"] == "GHz":
        capacity = e2e_cs_request["capacity"]["value"] * 1000
    elif e2e_cs_request["capacity"]["unit"] == "THz":
        capacity = e2e_cs_request["capacity"]["value"] * 1000000
    else:
        #Unit is MHz
        capacity = e2e_cs_request["capacity"]["value"]
    
    # ROUTING PATH COMPUTATION options based based on source and destination domains
    if str(os.environ.get("ABSTRACION_MODEL")) == "vnode":
        src = e2e_cs_request["source"]["context_uuid"]+":"+e2e_cs_request["source"]["context_uuid"]
        dst = e2e_cs_request["destination"]["context_uuid"]+":"+e2e_cs_request["destination"]["context_uuid"]
    elif str(os.environ.get("ABSTRACION_MODEL")) == "transparent":
        src = e2e_cs_request["source"]["context_uuid"]+":"+e2e_cs_request["source"]["node_uuid"]
        dst = e2e_cs_request["destination"]["context_uuid"]+":"+e2e_cs_request["destination"]["node_uuid"]
    elif str(os.environ.get("ABSTRACION_MODEL")) == "vlink":
        src = e2e_cs_request["source"]["context_uuid"]+":"+e2e_cs_request["source"]["node_uuid"]
        dst = e2e_cs_request["destination"]["context_uuid"]+":"+e2e_cs_request["destination"]["node_uuid"]
    else:
        settings.logger.info("ORCH: ERROR!!!")

    # we find the k-shortest path (K=7)
    route_nodes_list = vl_computation.find_path(src, dst)
    settings.logger.debug("The best 20 routes are: " + str(route_nodes_list))

    # SPECTRUM ASSIGNMENT procedure (first a SIPs route is created. Then, it checks their spectrum availability)
    for route_item in route_nodes_list:
        # maps the route from the nodes to the neps involved.
        response_nep_mapped = vl_computation.node2nep_route_mapping(route_item, e2e_topology_json, capacity)
        neps_route = response_nep_mapped[0]
        idl_route = response_nep_mapped[1]
        settings.logger.debug("neps_route: " + str(neps_route))
        settings.logger.debug("idl_route: "+str(idl_route))
        if neps_route == [] and idl_route == []:
            settings.logger.info("No NEP or link available in the itnerdomain links. Looking for the next route.")
            continue
        # identifies the SIP used for each NEP in the route
        response_sip_mapped = vl_computation.nep2sip_route_mapping(neps_route, e2e_cs_request, capacity)
        sips_route = response_sip_mapped[0]
        spectrums_available = response_sip_mapped[1]
        internal_links_route = response_sip_mapped[2]
        complete_route_nodes = response_sip_mapped[3]
        settings.logger.debug("sips_route: "+str(sips_route))
        settings.logger.debug("spectrums_available: "+str(spectrums_available))
        settings.logger.debug("internal_links_route: "+str(internal_links_route))

        if sips_route == [] and spectrums_available == []:
            settings.logger.debug("No spectrum availability in NEP. Looking for the next route.")
            continue
        # generates available spectrums list from interdomain links & internal neps
        for idl_item in idl_route:
            new_spectrum = {}
            new_spectrum["available-spectrum"] = idl_item["available-spectrum"]
            spectrums_available.append(new_spectrum)
        
        settings.logger.debug("spectrums_available: "+str(spectrums_available))
        settings.logger.debug("capacity: " + str(capacity))
        # checks if there is a common spectrum slot based on the available in all the neps and interdomain links in the route
        selected_spectrum = vl_computation.spectrum_assignment(spectrums_available, capacity)
        settings.logger.debug("selected_spectrum: "+str(selected_spectrum))

        # rsa done is complete or if empty, starts with the next route
        if selected_spectrum == []:
            settings.logger.info("No spectrum continuity. Looking for the next route.")
            continue
        else:
            selected_route = complete_route_nodes
            break
    
    # if no route is found, returns to inform
    if selected_route == []:
        settings.logger.error("ERROR - NO route available between these two SIPs.")
        e2e_cs_json["status"]  = "ERROR - no route available."
        return e2e_cs_json, 200

    settings.logger.debug("selected_route: " + str(selected_route))
    # adds more generic info into the e2e_cs data object
    spectrum = {}
    spectrum["lower-frequency"] = selected_spectrum[0]
    spectrum["upper-frequency"] = selected_spectrum[0] + capacity
    e2e_cs_json["spectrum"] = spectrum
    e2e_cs_json["route-nodes"] = selected_route
    
    # creates a list of domain-CSs and adds thir information in the e2e_cs data object
    cs_list = []
    for idx, sip_item in enumerate(sips_route):
        if idx < (len(sips_route)-1):
            # checks that each pair of sips belongs to the same owner, otherwise does not generate the cs_info
            if sip_item["context_uuid"] == sips_route[idx+1]["context_uuid"]:
                cs_info = {}
                internal_links = []
                cs_info["uuid"] = str(uuid.uuid4())
                cs_info["context-uuid"] = sip_item["context_uuid"]
                cs_info["address-owner"] = sip_item["blockchain_owner"]
                cs_info["status"] = "INSTANTIATING"
                cs_info["sip-source"] = sip_item["uuid"]
                cs_info["sip-destination"] = sips_route[idx+1]["uuid"]
                # adds the list of internal (constrained) links for the current domain CS
                # NOTE: ONLY accessed in transparent abstraction mode
                if internal_links_route != [] and os.environ.get("ABSTRACION_MODEL") == "transparent":
                    for link_item in internal_links_route:
                        if link_item["context_uuid"] == sip_item["context_uuid"]:
                            internal_links.append(link_item["uuid"])
                cs_info["internal-links"] = internal_links
                cs_list.append(cs_info)
            else:
                # if the two sips belong to two different domains, it passes to the next item.
                continue
    e2e_cs_json["domain-cs"] = cs_list
    
    # saves the first version of the new e2e_cs data object
    mutex_e2e_csdb_access.acquire()
    db.add_element(e2e_cs_json, "e2e_cs")
    mutex_e2e_csdb_access.release()
    
    # distribuïm domain CSs requests
    settings.logger.debug("cs_list: " + str(cs_list))
    for cs_item in cs_list:
        # decide whether the CS is for the local domain SDN controller or another domain
        if cs_item["address-owner"] == str(settings.web3.eth.defaultAccount):
            settings.logger.debug("Sending domain CS request to the local SDN controller.")
            response = sdn_mapper.instantiate_connectivity_service(cs_item, spectrum, e2e_cs_json["capacity"])
            if response[1] == 200 and response[0]["status"] == "DEPLOYED":
                #saves the domain CS information
                mutex_local_csdb_access.acquire()
                db.add_cs(response[0])
                mutex_local_csdb_access.release()
                # saves the reference domain CS information int eh E2E CS data object.
                mutex_e2e_csdb_access.acquire()
                e2e_cs = db.get_element(e2e_cs_json["uuid"], "e2e_cs")
                for domain_cs_item in e2e_cs["domain-cs"]:
                    if domain_cs_item["uuid"] == cs_item["uuid"]:
                        domain_cs_item["status"] = "DEPLOYED"
                        break
                db.update_db(e2e_cs["uuid"], e2e_cs, "e2e_cs")
                mutex_e2e_csdb_access.release()
            else:
                #TODO: manage this error
                settings.logger.error("ERROR requesting local domain CS.")
                return e2e_cs_json,400
        else:
            response = bl_mapper.instantiate_blockchain_cs(cs_item["address-owner"], cs_item, spectrum, e2e_cs_json["capacity"])
    
    # deployment management to validate all domain CSs composing the E2E CS are READY
    settings.logger.debug("Waiting all the domains CS from other domains to be deployed.")
    e2e_cs_ready = False
    while  e2e_cs_ready == False:
        e2e_cs_ready = True
        mutex_e2e_csdb_access.acquire()
        e2e_cs = db.get_element(e2e_cs_json["uuid"], "e2e_cs")
        for domainCS_item in e2e_cs["domain-cs"]:
            if domainCS_item["status"] != "DEPLOYED":
                e2e_cs_ready = False
                break
        mutex_e2e_csdb_access.release()
        time.sleep(10)  # awaits 10 seconds before it checks again
    
    #prepare the new occupied spectrum information item
    freq_const = {}
    freq_const["adjustment-granularity"] = "G_6_25GHZ"
    freq_const["grid-type"] = "FLEX"
    new_ocuppied_item = {}
    new_ocuppied_item["frequency-constraint"] =  freq_const
    new_ocuppied_item["lower-frequency"] = e2e_cs_json["spectrum"]["lower-frequency"]
    new_ocuppied_item["upper-frequency"] = e2e_cs_json["spectrum"]["upper-frequency"]

    settings.logger.debug("Updating data objects in DDBBs.")
    # update the spectrum information for each internal NEP (transmitter) or IDL used in the route
    settings.logger.debug("Updating available spectrums in the internal NEPs of each SDN Context and the IDLs.")
    for idx, nep_item in enumerate(neps_route):
        if "type_link" not in nep_item.keys() and nep_item["direction"] == "OUTPUT":
            settings.logger.debug("Internal NEP: updating a NEP belonging to an SDN context.")
            # updates the internal NEPsinformation
            # gets the nep info
            requested_uuid = nep_item["context_uuid"]+":"+nep_item["node_uuid"]+":"+nep_item["nep_uuid"]
            requested_nep = bl_mapper.get_nep(requested_uuid)
            # modifies the occupied-spectrum key
            temp_list = requested_nep["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["occupied-spectrum"]
            temp_list.append(new_ocuppied_item)
            requested_nep["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["occupied-spectrum"] = temp_list
            # modifies the value in the available-spectrum key in the nep info

            occupied_slots = []
            available_slots = []
            # there only a single element in the "supportable-spectrum" block info.
            low_suportable = requested_nep["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["supportable-spectrum"][0]["lower-frequency"]
            up_suportable = requested_nep["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["supportable-spectrum"][0]["upper-frequency"]
            supportable_range = []
            supportable_range.append(low_suportable)
            supportable_range.append(up_suportable)
            occupied_spectrum = requested_nep["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["occupied-spectrum"]
            for spectrum_item in occupied_spectrum:
                occupied_slots.append([spectrum_item["lower-frequency"],spectrum_item["upper-frequency"]])
            if occupied_slots:
                available_slots = vl_computation.available_spectrum(supportable_range, occupied_slots)
                available_slots_json = []
                for slot_item in available_slots:
                    #append pair of available frequency slots to the list
                    freq_const = {}
                    freq_const["adjustment-granularity"] = "G_6_25GHZ"
                    freq_const["grid-type"] = "FLEX"
                    new_available_item = {}
                    new_available_item["frequency-constraint"] =  freq_const
                    new_available_item["lower-frequency"] = slot_item[0]
                    new_available_item["upper-frequency"] = slot_item[1]
                    available_slots_json.append(new_available_item)
                requested_nep["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["available-spectrum"] = available_slots_json
            else:
                settings.logger.error("There is a problem with the occupied spectrums. They are empty, why?")
            
            # sends the new info to the BL
            response_update = bl_mapper.update_nep(requested_uuid, requested_nep)
            if response_update[1]!= 200:
                settings.logger.error("Error when saving updated data object.")
                pass
        #elif "type_link" in nep_item.keys() and nep_item["link_uuid"] == neps_route[idx+1]["link_uuid"] and idx < (len(neps_route)-1):
        elif "type_link" in nep_item.keys() and idx < (len(neps_route)-1):
            if nep_item["link_uuid"] == neps_route[idx+1]["link_uuid"]:
                #These NEPs are update in the IDL files and later in their corresponding SIPs in the SDN contexts.
                settings.logger.debug("NEP belonging to an IDL.")
                # composes the uuids based on the asbtraction model is being used.
                if os.environ.get("ABSTRACION_MODEL") in ["transparent", "vlink"]:
                    node_involved_1 = nep_item["context_uuid"]+":"+nep_item["node_uuid"]
                    node_involved_2 = neps_route[idx+1]["context_uuid"]+":"+neps_route[idx+1]["node_uuid"]
                else:
                    node_involved_1 = nep_item["context_uuid"]+":"+nep_item["context_uuid"]
                    node_involved_2 = neps_route[idx+1]["context_uuid"]+":"+neps_route[idx+1]["context_uuid"]
                
                # first updates the occupied spectrum in the right physical link (remember the IDL trick to have multiple NEPs/SIPs as one NEP with multiple SIPs)
                occupied_slots = []
                for idl_item in e2e_topology_json["e2e-topology"]["interdomain-links"]:
                    spectrum_added = False
                    if node_involved_1 in idl_item["nodes-involved"] and node_involved_2 in idl_item["nodes-involved"]:
                        for link_option_item in idl_item["link-options"]:
                            if link_option_item["nodes-direction"]["node-1"] == node_involved_1 and link_option_item["nodes-direction"]["node-2"] == node_involved_2:
                                for physical_option_item in link_option_item["physical-options"]:
                                    # IDL physical-option being used found
                                    if physical_option_item["node-edge-point"][0]["nep-uuid"] == nep_item["nep_uuid"] and physical_option_item["node-edge-point"][1]["nep-uuid"] == neps_route[idx+1]["nep_uuid"]:
                                        new_occupied_list = []
                                        new_occupied_list.append(new_ocuppied_item)
                                        physical_option_item["occupied-spectrum"] = new_occupied_list
                                        spectrum_added = True

                                    if physical_option_item["occupied-spectrum"] != []:
                                        low_freq = physical_option_item["occupied-spectrum"][0]["lower-frequency"]
                                        up_freq = physical_option_item["occupied-spectrum"][0]["upper-frequency"]
                                        occupied_slots.append([low_freq,up_freq])
                            if spectrum_added and occupied_slots!=[]:
                                low_suportable = link_option_item["supportable-spectrum"][0]["lower-frequency"]
                                up_suportable = link_option_item["supportable-spectrum"][0]["upper-frequency"]
                                supportable_slot = [low_suportable, up_suportable]
                                available_slots = vl_computation.available_spectrum(supportable_slot, occupied_slots)
                                available_slots_json = []
                                for slot_item in available_slots:
                                    #append pair of available frequency slots to the list
                                    freq_const = {}
                                    freq_const["adjustment-granularity"] = "G_6_25GHZ"
                                    freq_const["grid-type"] = "FLEX"
                                    new_available_item = {}
                                    new_available_item["frequency-constraint"] =  freq_const
                                    new_available_item["lower-frequency"] = slot_item[0]
                                    new_available_item["upper-frequency"] = slot_item[1]
                                    available_slots_json.append(new_available_item)
                                link_option_item["available-spectrum"] = available_slots_json
                                break
                    if spectrum_added:
                        settings.logger.debug("Saving and distributing the updated link-option info.")
                        settings.logger.debug("link_option_item: " + str(link_option_item))
                        response = bl_mapper.update_link_option(link_option_item)
                        break   
        else:
            settings.logger.debug("This NEP is neither an internal output or in an IDL.")
    
    # update the spectrum information for each SIP used in the route
    #settings.logger.debug("Updating available spectrums in the SIPs of each SDN Context.")
    settings.logger.debug("Saving and distributing the updated SIPs info.")
    for sip_item in sips_route:
        # gets the sip element from the BL
        sip_uuid = sip_item["context_uuid"] + ":" + sip_item["uuid"]
        response = bl_mapper.get_sip(sip_uuid)
        sip_json = response["sip_info"]
        settings.logger.debug("SIP to udpate: " + str(sip_json))

        # adds the occupied spectrum info
        occ_spec = []
        occ_spec.append(new_ocuppied_item)
        sip_json["tapi-photonic-media:media-channel-service-interface-point-spec"]["mc-pool"]["occupied-spectrum"] = occ_spec

        # generate the new ranges of available spectrum for this sip
        available_slots = []
        occupied_slots = []
        low_suportable = sip_json["tapi-photonic-media:media-channel-service-interface-point-spec"]["mc-pool"]["supportable-spectrum"][0]["lower-frequency"]
        upp_suportable = sip_json["tapi-photonic-media:media-channel-service-interface-point-spec"]["mc-pool"]["supportable-spectrum"][0]["upper-frequency"]
        low_occupied = sip_json["tapi-photonic-media:media-channel-service-interface-point-spec"]["mc-pool"]["occupied-spectrum"][0]["lower-frequency"]
        upp_occupied = sip_json["tapi-photonic-media:media-channel-service-interface-point-spec"]["mc-pool"]["occupied-spectrum"][0]["upper-frequency"]
        supportable_range = [low_suportable, upp_suportable]
        occupied_slots.append([low_occupied, upp_occupied])
        available_slots = vl_computation.available_spectrum(supportable_range, occupied_slots)

        available_slots_json = []
        for slot_item in available_slots:
            #append pair of available frequency slots to the list
            freq_const = {}
            freq_const["adjustment-granularity"] = "G_6_25GHZ"
            freq_const["grid-type"] = "FLEX"
            new_available_item = {}
            new_available_item["frequency-constraint"] =  freq_const
            new_available_item["lower-frequency"] = slot_item[0]
            new_available_item["upper-frequency"] = slot_item[1]
            available_slots_json.append(new_available_item)
        sip_json["tapi-photonic-media:media-channel-service-interface-point-spec"]["mc-pool"]["available-spectrum"] = available_slots_json
        response = bl_mapper.update_sip(sip_uuid, sip_json)  

    # saves the e2e_cs data object to confirm full deployment.
    e2e_cs_json["status"]  = "DEPLOYED"
    mutex_e2e_csdb_access.acquire()
    db.update_db(e2e_cs_json["uuid"], e2e_cs_json, "e2e_cs")
    mutex_e2e_csdb_access.release()
    settings.logger.info("ORCH: E2E CS request processed.")
    settings.logger.info("e2e_cs_json: " + str(e2e_cs_json))
    
    #return e2e_cs_json,200

# manages the termination of an E2E CS
#TODO: pensar com gestionar els returns tant d'aqui com de l'instantiate per quan es faci el test amb l'script de poisson.
def terminate_e2e_connectivity_service(cs_uuid):
    settings.logger.info("ORCH: Received E2E request info to terminate CS. Let's process it.")   
    # gets the e2e CS to terminate
    e2e_cs_json = db.get_element(cs_uuid, "e2e_cs")
                
    # distribuïm domain CSs requests
    settings.logger.debug("cs_list: " + str(e2e_cs_json["domain-cs"]))
    for cs_item in e2e_cs_json["domain-cs"]:
        # decide whether the CS is for the local domain SDN controller or another domain
        if cs_item["address-owner"] == str(settings.web3.eth.defaultAccount):
            settings.logger.debug("Sending domain CS request to the local SDN controller.")
            response = sdn_mapper.terminate_connectivity_service(cs_item["uuid"])
            if response[1] == 200 and response[0]["status"] == "TERMINATED":
                #TODO: update local domain CS information
                mutex_local_csdb_access.acquire()
                #update here
                cs_info = {}
                cs_info["uuid"] = cs_item["uuid"]
                cs_info["status"] = "TERMINATED"
                db.update_cs(cs_info)
                mutex_local_csdb_access.release()
                
                # saves the reference domain CS information in the E2E CS data object.
                mutex_e2e_csdb_access.acquire()
                e2e_cs = db.get_element(e2e_cs_json["uuid"], "e2e_cs")
                for domain_cs_item in e2e_cs["domain-cs"]:
                    if domain_cs_item["uuid"] == cs_item["uuid"]:
                        domain_cs_item["status"] = "TERMINATED"
                        break
                db.update_db(e2e_cs["uuid"], e2e_cs, "e2e_cs")
                mutex_e2e_csdb_access.release()
            else:
                #TODO: manage this error
                settings.logger.error("ERROR requesting local domain CS.")
                return e2e_cs_json,400
        else:
            response = bl_mapper.terminate_blockchain_cs(cs_item["uuid"], cs_item["address-owner"])
    
    # deployment management to validate all domain CSs composing the E2E CS are READY
    settings.logger.debug("Waiting all the domains CS from other domains to be terminated.")
    e2e_cs_terminated = False
    while  e2e_cs_terminated == False:
        e2e_cs_terminated = True
        mutex_e2e_csdb_access.acquire()
        e2e_cs = db.get_element(e2e_cs_json["uuid"], "e2e_cs")
        for domainCS_item in e2e_cs["domain-cs"]:
            if domainCS_item["status"] != "TERMINATED":
                e2e_cs_terminated = False
                break
        mutex_e2e_csdb_access.release()
        time.sleep(10)  # awaits 10 seconds before it checks again

    
    # gets and prepares the e2e_topology (the set of IDLs definning how the SDN domains are linked)
    response = bl_mapper.get_e2etopology_from_blockchain()
    e2e_topology_json = response[0]
    if e2e_topology_json == "empty":
        return {"msg":"There is no e2e_topology to work with."}
    else:
        # prepares the intedomain-links to compare the existing with the new ones in the IDL json
        for idl_item in e2e_topology_json["e2e-topology"]["interdomain-links"]:
            linkoptions_list = []
            for linkoption_uuid_item in idl_item["link-options"]:
                response = bl_mapper.get_linkOption_from_blockchain(linkoption_uuid_item)
                linkoptions_list.append(response[0])
            idl_item["link-options"] = linkoptions_list
    
    settings.logger.debug("Updating data objects in DDBBs.")
    # update the spectrum information for each internal NEP (transmitter) or IDL used in the route
    #settings.logger.debug("Updating available spectrums in the internal NEPs of each SDN Context and the IDLs.")
    for idx, route_item in enumerate(e2e_cs_json["route-nodes"]):
        if route_item["sip_uuid"] == "":
            settings.logger.debug("Internal NEP: updating the NEP info.")
            # updates the internal NEPsinformation
            # gets the nep info
            requested_uuid = route_item["context_uuid"]+":"+route_item["node_uuid"]+":"+route_item["nep_uuid"]
            requested_nep = bl_mapper.get_nep(requested_uuid)
            
            # modifies the occupied-spectrum key
            spec_list = requested_nep["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["occupied-spectrum"]

            for spec_idx, spectrum_item in enumerate(spec_list):
                if spectrum_item["lower-frequency"] == e2e_cs_json["spectrumm"]["lower-frequency"] and spectrum_item["upper-frequency"] == e2e_cs_json["spectrum"]["upper-frequency"]:
                    found_index = spec_idx
                    break
            
            # removes the occupied slot
            del spec_list[found_index]

            requested_nep["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["occupied-spectrum"] = spec_list
            # modifies the value in the available-spectrum key in the nep info

            occupied_slots = []
            available_slots = []
            # there only a single element in the "supportable-spectrum" block info.
            low_suportable = requested_nep["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["supportable-spectrum"][0]["lower-frequency"]
            up_suportable = requested_nep["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["supportable-spectrum"][0]["upper-frequency"]
            supportable_range = []
            supportable_range.append(low_suportable)
            supportable_range.append(up_suportable)
            occupied_spectrum = requested_nep["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["occupied-spectrum"]
            if occupied_spectrum != []:
                for spectrum_item in occupied_spectrum:
                    occupied_slots.append([spectrum_item["lower-frequency"],spectrum_item["upper-frequency"]])
            if occupied_slots != []:
                available_slots = vl_computation.available_spectrum(supportable_range, occupied_slots)
                available_slots_json = []
                for slot_item in available_slots:
                    #append pair of available frequency slots to the list
                    freq_const = {}
                    freq_const["adjustment-granularity"] = "G_6_25GHZ"
                    freq_const["grid-type"] = "FLEX"
                    new_available_item = {}
                    new_available_item["frequency-constraint"] =  freq_const
                    new_available_item["lower-frequency"] = slot_item[0]
                    new_available_item["upper-frequency"] = slot_item[1]
                    available_slots_json.append(new_available_item)
                requested_nep["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["available-spectrum"] = available_slots_json
            else:
                # if no occupied slots, then available equals supportable
                av_spec = requested_nep["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["supportable-spectrum"][0]
                requested_nep["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["available-spectrum"] = av_spec
            
            # sends the new info to the BL
            response_update = bl_mapper.update_nep(requested_uuid, requested_nep)
            if response_update[1]!= 200:
                settings.logger.error("Error when saving updated data object.")
                pass
        else:
            if idx < (len(e2e_cs_json["route-nodes"])-1):
                #These NEPs are update in the IDL files and later in their corresponding SIPs in the SDN contexts.
                settings.logger.debug("NEP belonging to an IDL.")
                # composes the uuids based on the asbtraction model is being used.
                if os.environ.get("ABSTRACION_MODEL") in ["transparent", "vlink"]:
                    node_involved_1 = route_item["context_uuid"]+":"+route_item["node_uuid"]
                    node_involved_2 = route_item[idx+1]["context_uuid"]+":"+route_item[idx+1]["node_uuid"]
                else:
                    node_involved_1 = route_item["context_uuid"]+":"+route_item["context_uuid"]
                    node_involved_2 = route_item[idx+1]["context_uuid"]+":"+route_item[idx+1]["context_uuid"]
                
                # first updates the occupied spectrum in the right physical link (remember the IDL trick to have multiple NEPs/SIPs as one NEP with multiple SIPs)
                occupied_slots = []
                for idl_item in e2e_topology_json["e2e-topology"]["interdomain-links"]:
                    spectrum_removed = False
                    if node_involved_1 in idl_item["nodes-involved"] and node_involved_2 in idl_item["nodes-involved"]:
                        for link_option_item in idl_item["link-options"]:
                            if link_option_item["nodes-direction"]["node-1"] == node_involved_1 and link_option_item["nodes-direction"]["node-2"] == node_involved_2:
                                for physical_option_item in link_option_item["physical-options"]:
                                    # IDL physical-option being used found
                                    if physical_option_item["node-edge-point"][0]["nep-uuid"] == route_item["nep_uuid"] and physical_option_item["node-edge-point"][1]["nep-uuid"] == route_item[idx+1]["nep_uuid"]:
                                        physical_option_item["occupied-spectrum"] = []
                                        spectrum_removed = True
                                    # the other occupied spectrums are added (if there are) to calculate the IDL available spectrum
                                    if physical_option_item["occupied-spectrum"] != []:
                                        low_freq = physical_option_item["occupied-spectrum"][0]["lower-frequency"]
                                        up_freq = physical_option_item["occupied-spectrum"][0]["upper-frequency"]
                                        occupied_slots.append([low_freq,up_freq])
                            if spectrum_removed and occupied_slots!=[]:
                                low_suportable = link_option_item["supportable-spectrum"][0]["lower-frequency"]
                                up_suportable = link_option_item["supportable-spectrum"][0]["upper-frequency"]
                                supportable_slot = [low_suportable, up_suportable]
                                available_slots = vl_computation.available_spectrum(supportable_slot, occupied_slots)
                                available_slots_json = []
                                for slot_item in available_slots:
                                    #append pair of available frequency slots to the list
                                    freq_const = {}
                                    freq_const["adjustment-granularity"] = "G_6_25GHZ"
                                    freq_const["grid-type"] = "FLEX"
                                    new_available_item = {}
                                    new_available_item["frequency-constraint"] =  freq_const
                                    new_available_item["lower-frequency"] = slot_item[0]
                                    new_available_item["upper-frequency"] = slot_item[1]
                                    available_slots_json.append(new_available_item)
                                link_option_item["available-spectrum"] = available_slots_json
                                break
                            else:
                                link_option_item["available-spectrum"] = link_option_item["supportable-spectrum"]
                    if spectrum_removed:
                        settings.logger.debug("Saving and distributing the updated link-option info.")
                        settings.logger.debug("link_option_item: " + str(link_option_item))
                        response = bl_mapper.update_link_option(link_option_item)
                        break   

    
            # update the spectrum information for each SIP used in the route
            #settings.logger.debug("Updating available spectrums in the SIPs of each SDN Context.")
            # gets the sip element from the BL
            sip_uuid = route_item["context_uuid"] + ":" + route_item["sip_uuid"]
            response = bl_mapper.get_sip(sip_uuid)
            sip_json = response["sip_info"]
            settings.logger.debug("SIP to udpate: " + str(sip_json))

            # empties the occupied spectrum info
            sip_json["tapi-photonic-media:media-channel-service-interface-point-spec"]["mc-pool"]["occupied-spectrum"] = []

            # no CS means available spectrum euqal to the supportable
            sup_spectrum = sip_json["tapi-photonic-media:media-channel-service-interface-point-spec"]["mc-pool"]["supportable-spectrum"]
            sip_json["tapi-photonic-media:media-channel-service-interface-point-spec"]["mc-pool"]["available-spectrum"] = sup_spectrum
            response = bl_mapper.update_sip(sip_uuid, sip_json)  

    # saves the e2e_cs data object to confirm full deployment.
    e2e_cs_json["status"]  = "TERMINATED"
    mutex_e2e_csdb_access.acquire()
    db.update_db(e2e_cs_json["uuid"], e2e_cs_json, "e2e_cs")
    mutex_e2e_csdb_access.release()
    settings.logger.info("ORCH: E2E CS request processed.")
    settings.logger.info("e2e_cs_json: " + str(e2e_cs_json))
    
    #return e2e_cs_json,200
    return 200

################################### E2E NETWORK SLICE INSTANCES FUNCTIONS #######################################
# NOTE: returns all the e2e slice instances (E2E NSI)
def get_e2e_slice_instances():
    settings.logger.info("ORCH: Received request to get E2E Network Slices information.")
    response = db.get_elements("slices")
    return response, 200

# NOTE: manages all the E2E slice instantiation process
# NOTE: add the E2E CS process using the already working process.
def instantiate_e2e_slice(incoming_data):
    settings.logger.info("ORCH: Received request to deploy an E2E Network Slice (TIME 1): " + str(time.time_ns()))
    # creates the NSI instance object based on the request
    nsi_element = {}
    nsi_element["id"] = str(uuid.uuid4()) #ID for the E2E slice object
    nsi_element["name"] = incoming_data["name"]
    nsi_element["instantiation_params"] = incoming_data["instantiation_params"]

    # gets local slice-subnets
    response = slice_mapper.get_all_slice_subnet_templates()
    local_slicesubnets_list = json.loads(response[0])
    
    # prepares e2e slice data object
    slice_subnets_list = []
    for subnet_item in incoming_data["slice_subnets"]:
        subslice_element= {}
        found_local = False
        # gets the local slice-subnet information
        for slicesubnet_element in local_slicesubnets_list:
            if slicesubnet_element["uuid"] == subnet_item["nst_ref"]:
                subslice_element["id"] = str(uuid.uuid4())          #id to find the slice subnet
                subslice_element["nst_ref"] = slicesubnet_element["uuid"]     #nstId
                subslice_element["name"] = slicesubnet_element["nstd"]["name"]
                subslice_element["version"] = slicesubnet_element["nstd"]["version"]
                subslice_element["vendor"] = slicesubnet_element["nstd"]["vendor"]
                subslice_element["price"] = 4
                subslice_element["unit"] = "eth"
                found_local = True
                break
        # gets hte blockchain slice-subnet information
        if found_local == False:
            blockchain_nst = bl_mapper.slice_from_blockchain(subnet_item["nst_ref"])
            subslice_element["id"] = str(uuid.uuid4())  #nsiId
            subslice_element["nst_ref"] = blockchain_nst[0]["id"]    #nstId
            subslice_element["name"] = blockchain_nst[0]["name"]
            subslice_element["version"] = blockchain_nst[0]["version"]
            subslice_element["vendor"] = blockchain_nst[0]["vendor"]
            subslice_element["price"] = blockchain_nst[0]["price"]
            subslice_element["unit"] = blockchain_nst[0]["unit"]
            subslice_element["blockchain_owner"] = blockchain_nst[0]["blockchain_owner"]
        
        slice_subnets_list.append(subslice_element)

    nsi_element["slice_subnets"]=slice_subnets_list
    nsi_element["status"] = "INSTANTIATING"

    # starts the instantiation procedure
    for slice_subnet_item in nsi_element["slice_subnets"]:
        # if there's a blockchain owner, the request towards blockchain else, local domain
        if "blockchain_owner" in slice_subnet_item.keys():
            response = bl_mapper.deploy_blockchain_slice(slice_subnet_item)
            slice_subnet_item["log"] = response[0]['log']
            slice_subnet_item["status"] = response[0]['status']
        else:
            # LOCAL INSTANTIATION PROCESS IS CALLED
            data_json = {}
            data_json['nst_id'] = slice_subnet_item["nst_ref"]
            data_json['name'] = subslice_element["name"]
            data_json['request_type'] = 'CREATE_SLICE'
            data_json['description'] = 'Slice-subnet instance based on the NST: ' + slice_subnet_item["nst_ref"]
            response = slice_mapper.instantiate_slice_subnet(data_json)

            if (response[1] == 200 or response[1] == 201):
                slice_subnet_item['log'] = "This slice-subnet is being instantiated."
                slice_subnet_item['status'] = "INSTANTIATING"
                slice_subnet_item['request_id'] = response[0]['id']  #jsonresponse['id']   

    # saves the nsi object into the db
    mutex_slice2db_access.acquire()
    nsi_element["log"] = "E2E Slice instance designed, deploying slice-subnets."
    response = db.add_element(nsi_element, "slices")
    if response != 200:
        pass                # TODO: trigger exception/error
    mutex_slice2db_access.release()
    
    # awaits for all the slice-subnets to be instantiated
    settings.logger.info("ORCH: Waiting for all slice-subnets instantes to be deployed. E2E SLICE ID: " +str(nsi_element["id"]))
    all_subnets_ready = False
    while(all_subnets_ready == False):
        subnets_instantiated = 0        # used to check how many subnets are in instantiated and change e2e slice status
        for slice_subnet_item in nsi_element["slice_subnets"]:
            if (slice_subnet_item['status'] == 'INSTANTIATING'):
                if ('blockchain_owner' not in slice_subnet_item):
                    response = slice_mapper.get_slice_subnet_instance_request(slice_subnet_item['request_id'])
                    jsonresponse = response[0]
                    if (jsonresponse['status'] == "INSTANTIATED"):
                        slice_subnet_item['instance_id'] = jsonresponse['instance_uuid']
                        slice_subnet_item['status'] = jsonresponse['status']
                        slice_subnet_item['log'] = "Slice_subnet instantiated."
                        subnets_instantiated = subnets_instantiated + 1
                        settings.logger.info('SUBNET_MAPPER: Finished local deployment (TIME 2): ' + str(time.time_ns()))
            elif(slice_subnet_item['status'] == 'INSTANTIATED'):
                # all slice-subnets deployed in other domains, are updated by the blockchain event thread.
                subnets_instantiated = subnets_instantiated + 1
            else:
                #TODO: ERROR management
                pass
        
        # if the number of slice-subnets instantiated = total number in the e2e slice, finishes while
        if (subnets_instantiated == len(nsi_element['slice_subnets'])):
            all_subnets_ready = True
    
    settings.logger.info("ORCH: SUBNETS READY, GOING FOR THE CSs (TIME 1): " + str(time.time_ns()))
    # *************************
    # NOTE: HARDCODED SIPS
    # TODO: think how to get them in real deployments coming from the orchestrators (NFVO, SDN) below.
    counter = 0
    sip_edge = "Edge:1"
    sip_core = "Core:1"
    for subnet_item in nsi_element['slice_subnets']:
        if ('blockchain_owner' in subnet_item):
            ip_string = "10.121.0."+str(counter)+"/24"
            subnet_item['nfvicp_cidr'] = ip_string
            subnet_item['nfvicp_sip'] = sip_core
        else:
            ip_string = "10.121.0."+str(counter)+"/24"
            subnet_item["nfvicp_cidr"] = ip_string
            subnet_item["nfvicp_sip"] = sip_edge
        counter = counter + 1
    # *************************
    
    # saves the nsi object into the db
    mutex_slice2db_access.acquire()
    nsi_element["log"] = "Slice-subnets ready, deploying virtual links between slice-subnets."
    db.update_db(nsi_element["id"], nsi_element, "slices")
    mutex_slice2db_access.release()

    #------------------------------------------------------------------------------
    # VL CREATION PROCEDURE
    # TODO: once it works, create a new function with this piece of code
    settings.logger.info("ORCH: Designing all the VLs. E2E SLICE ID: " +str(nsi_element["id"]))
    slice_vl_list = []
    response = get_all_contexts()
    contexts_list = response[0]
    for connection_item in incoming_data['instantiation_params']['slice_vl']:
        nst_ref_src = connection_item['nst_ref_src']
        nst_ref_dst = connection_item['nst_ref_dst']

        # declares and defines a vl object
        slice_vl_item = {}
        slice_vl_item['vl_id'] = str(uuid.uuid4())
        slice_vl_item['direction'] = connection_item['direction']
        slice_vl_item['status'] = "NEW"

        # gets source/destination sips from the instantiated subnets to interconnect them based on the instant_params
        for subnet_item in nsi_element['slice_subnets']:
            if subnet_item['nst_ref'] == nst_ref_src:
                slice_vl_item["cidr_1"] = subnet_item['nfvicp_cidr']
                slice_vl_item["source_sip"] = subnet_item["nfvicp_sip"]
            elif subnet_item['nst_ref'] == nst_ref_dst:
                slice_vl_item["cidr_2"] = subnet_item['nfvicp_cidr']
                slice_vl_item["destination_sip"] = subnet_item["nfvicp_sip"]
            else:
                continue
        # based on the two found sips, looks for the shortest path between their network nodes
        path_nodes_list = vl_computation.find_path(slice_vl_item["source_sip"], slice_vl_item["destination_sip"])
        settings.logger.info("ORCH: THE PATH DESIGNED: " +str(path_nodes_list))
        
        # creates a json with all the connectivity services to compose the VL between subnets
        cs_list = []
        for index_item, node_item in enumerate(path_nodes_list):
            settings.logger.info("ORCH: ******** node_item --> " +str(node_item))
            # access unless is the last element
            if node_item != path_nodes_list[-1]:
                for context_item in contexts_list:
                    if node_item == context_item["topology"]["node_name"]:
                        if index_item == 0:   # the first cs depends on the source sip
                            settings.logger.info("ORCH: ******** FIRST NODE IN THE PATH ********")
                            for port_item in context_item["topology"]["ports"]:
                                if port_item["port_id"] == slice_vl_item["source_sip"]:
                                    cs_element_json = {}
                                    cs_element_json['id'] = str(uuid.uuid4())
                                    cs_element_json['domain_manager'] = node_item
                                    cs_element_json['source_sip'] = port_item["port_id"]
                                    cs_element_json['destination_sip'] = port_item['destination']
                                    cs_element_json['destination_cidr'] = slice_vl_item["cidr_2"]
                                    cs_list.append(cs_element_json)

                                    if slice_vl_item['direction'] == "Bidirectional":
                                        cs_element_json_bi = {}
                                        cs_element_json_bi['id'] = str(uuid.uuid4())
                                        domain_manager = port_item['destination'].split(':')
                                        cs_element_json_bi['domain_manager'] = domain_manager[0]
                                        cs_element_json_bi['source_sip'] = port_item['destination']
                                        cs_element_json_bi['destination_sip'] = port_item["port_id"]
                                        cs_element_json_bi['destination_cidr'] = slice_vl_item["cidr_1"]
                                        cs_list.append(cs_element_json_bi)
                                    
                                    settings.logger.info("ORCH: cs_list: " +str(cs_list))
                        
                        elif (index_item == len(path_nodes_list) - 1):    # the cs depends on the destination_sip
                            settings.logger.info("ORCH: ******** LAST NODE IN THE PATH ********")
                            for port_item in context_item["topology"]["ports"]:
                                if port_item["destination"] == slice_vl_item["destination_sip"]:
                                    cs_element_json = {}
                                    cs_element_json['id'] = str(uuid.uuid4())
                                    cs_element_json['domain_manager'] = node_item
                                    cs_element_json['source_sip'] = port_item["port_id"]
                                    cs_element_json['destination_sip'] = port_item['destination']
                                    cs_element_json['destination_cidr'] = slice_vl_item["cidr_2"]
                                    cs_list.append(cs_element_json)

                                    if slice_vl_item['direction'] == "Bidirectional":
                                        cs_element_json_bi = {}
                                        cs_element_json_bi['id'] = str(uuid.uuid4())
                                        domain_manager = port_item['destination'].split(':')
                                        cs_element_json_bi['domain_manager'] = domain_manager[0]
                                        cs_element_json_bi['source_sip'] = port_item['destination']
                                        cs_element_json_bi['destination_sip'] = port_item["port_id"]
                                        cs_element_json_bi['destination_cidr'] = slice_vl_item["cidr_1"]
                                        cs_list.append(cs_element_json_bi)

                                    settings.logger.info("ORCH: cs_list: " +str(cs_list))
                        
                        else:
                            settings.logger.info("ORCH: ******** A MIDDLE NODE IN THE PATH ********")
                            for port_item in context_item["topology"]["ports"]:
                                settings.logger.info("ORCH: cs_list: " +str(cs_list))
                                dst_node = port_item["destination"].split(":")
                                settings.logger.info("ORCH: port_item[destination]: " +str(port_item["destination"]))
                                settings.logger.info("ORCH: dst_node: " +str(dst_node))
                                settings.logger.info("ORCH: dst_node[0]: " +str(dst_node[0]))
                                settings.logger.info("ORCH: path_nodes_list[index_item + 1]: " +str(path_nodes_list[index_item + 1]))
                                if dst_node[0] == path_nodes_list[index_item + 1]:
                                    cs_element_json = {}
                                    cs_element_json['id'] = str(uuid.uuid4())
                                    cs_element_json['domain_manager'] = node_item
                                    cs_element_json['source_sip'] = port_item["port_id"]
                                    cs_element_json['destination_sip'] = port_item['destination']
                                    cs_element_json['destination_cidr'] = slice_vl_item["cidr_2"]
                                    cs_list.append(cs_element_json)

                                    if slice_vl_item['direction'] == "Bidirectional":
                                        cs_element_json_bi = {}
                                        cs_element_json_bi['id'] = str(uuid.uuid4())
                                        domain_manager = port_item['destination'].split(':')
                                        cs_element_json_bi['domain_manager'] = domain_manager[0]
                                        cs_element_json_bi['source_sip'] = port_item['destination']
                                        cs_element_json_bi['destination_sip'] = port_item["port_id"]
                                        cs_element_json_bi['destination_cidr'] = slice_vl_item["cidr_1"]
                                        cs_list.append(cs_element_json_bi)
                                    
                                    settings.logger.info("ORCH: cs_list: " +str(cs_list))
            
            else:
                settings.logger.info("ORCH: ******** LAST node_item ********")
        
        # adds the cs list composing the vl
        slice_vl_item['cs_list'] = cs_list
        slice_vl_list.append(slice_vl_item)
    
    nsi_element["slice_vls"] = slice_vl_list

    # saves the nsi object into the db
    mutex_slice2db_access.acquire()
    db.update_db(nsi_element["id"], nsi_element, "slices")
    mutex_slice2db_access.release()

    # request each CS deployment
    settings.logger.info("ORCH: Requesting all the VLs. E2E SLICE ID: " +str(nsi_element["id"]))
    for vl_item in nsi_element["slice_vls"]:
        vl_ref = vl_item['vl_id']
        for cs_item in vl_item['cs_list']:
            if cs_item['domain_manager'] == os.environ.get("SDN_DOMAIN"):
                # call SDN MAPPER
                response = sdn_mapper.instantiate_connectivity_service(cs_item)
                cs_item['id'] = response[0]['instance_id']
            else:
                # call BLOCKCHAIN MAPPER
                for context_item in contexts_list:
                    # looks for the blokchain address of the context owner
                    if context_item['domain_id'] == cs_item['domain_manager']:
                        response = bl_mapper.instantiate_blockchain_cs(context_item['blockchain_owner'], vl_ref, cs_item)
            if response[1] == 200:
                cs_item['status'] = response[0]['status']
            else:
                #TODO: manage error
                pass
    
    # saves the nsi object into the db
    mutex_slice2db_access.acquire()
    db.update_db(nsi_element["id"], nsi_element, "slices")
    mutex_slice2db_access.release()

    # awaits for all the slice-subnets to be instantiated
    settings.logger.info("ORCH: Waiting for all VLs to be deployed. E2E SLICE ID: " +str(nsi_element["id"]))
    all_vl_ready = False
    while(all_vl_ready == False):
        nsi_element = db.get_element(nsi_element["id"], "slices")

        vl_ready = 0        # used to check how many VLs are ready
        for vl_item in nsi_element["slice_vls"]:
            if (vl_item['status'] == 'NEW'):
                cs_ready = 0
                for cs_item in vl_item['cs_list']:
                    '''
                    #NOTE: it checks only the local CS as those from the Blockchain are update by another thread (worker)
                    if cs_item['domain_manager'] == os.environ.get("SDN_DOMAIN"):
                        response = sdn_mapper.get_connectivity_service(cs_item['id'])
                        if response[0]['status'] == 'READY':
                            cs_item['status'] = response[0]['status']
                    '''
                    if cs_item['status'] == 'READY':
                        cs_ready = cs_ready + 1
                if cs_ready == len(vl_item['cs_list']):
                    vl_item['status'] = 'READY'
                    vl_ready = vl_ready + 1        
            elif(vl_item['status'] == 'READY'):
                # all slice-subnets deployed in other domains, are updated by the blockchain event thread.
                vl_ready = vl_ready + 1
            else:
                #TODO: ERROR management
                pass
        # if the number of slice-subnets instantiated = total number in the e2e slice, finishes while
        if vl_ready == len(nsi_element['slice_vls']):
            all_vl_ready = True   
    #------------------------------------------------------------------------------
    settings.logger.info("ORCH: VLs READY (TIME 1): " + str(time.time_ns()))
    nsi_element["status"] = "INSTANTIATED"
    nsi_element["log"] = "E2E Network Slice INSTANTIATED."

    # saves the nsi object into the db
    mutex_slice2db_access.acquire()
    db.update_db(nsi_element["id"], nsi_element, "slices")
    mutex_slice2db_access.release()
    settings.logger.info('E2E Network Slice INSTANTIATED. E2E Slice ID: ' + str(nsi_element["id"]))
    settings.logger.info("ORCH: E2E READY (TIME 1): " + str(time.time_ns()))

# NOTE: manages a local slice-subnet instantiation process
def instantiate_local_slicesubnet(subnet_json):
    settings.logger.info("ORCH: STARTTING LOCAL DEPLOYMENT (TIME 2): " + str(time.time_ns()))
    settings.logger.info("ORCH: Received slice-subnet from Blockchain request. NST Ref:: " +str(subnet_json['nst_ref']))
    
    #gets specific NST information
    response = slice_mapper.get_slice_subnet_template(subnet_json['nst_ref'])
    jsonresponse = json.loads(response[0])

    # LOCAL INSTANTIATION PROCESS IS CALLED
    data_json = {}
    data_json['nst_id'] = subnet_json['nst_ref']
    data_json['name'] = "BL_"+ jsonresponse['nstd']['name'] + jsonresponse['uuid']   # Default name
    data_json['request_type'] = 'CREATE_SLICE'
    data_json['description'] = 'Slice-subnet instance based on the NST: ' + jsonresponse['uuid'] # Default description
    
    response = slice_mapper.instantiate_slice_subnet(data_json)  # NOTE: response is emulated while developing.
    if (response[1] != 200 or response[1] != 201):
        # TODO: exception/error management
        pass
    
    # creates the NSI instance object with mapping between the Blockchain element and the local element
    subnet_element = {}
    subnet_element["id"] = subnet_json['id']
    subnet_element['log'] = "Slice-subnet being instantiated."
    subnet_element['status'] = subnet_json['status']
    subnet_element["nst_ref"] = subnet_json['nst_ref']
    subnet_element['request_id'] = response[0]['id']
    
    # saves the nsi object into the db
    mutex_slice2blockchaindb_access.acquire()
    response = db.add_element(subnet_element, "blockchain_subnets")
    if response[1] != 200:
        # TODO: exception/error management
        pass
    mutex_slice2blockchaindb_access.release()

    # Instantiation procedure control
    subnet_ready = False
    while(subnet_ready == False):
        response = slice_mapper.get_slice_subnet_instance_request(subnet_element['request_id'])
        jsonresponse = response[0]
        if (jsonresponse['status'] == "INSTANTIATED"):
            subnet_ready = True
        elif (jsonresponse['status'] == "INSTANTIATING"):
            continue
        else:
            # TODO: exception/error management
            pass
    
    # Once instantiation is done, updates Blockchain and local DB
    subnet_element['instance_id'] = jsonresponse['instance_uuid']
    subnet_element['status'] = jsonresponse['status']
    subnet_element['log'] = "Slice-subnet instantiated."

    settings.logger.info("ORCH: FINISHING LOCAL DEPLOYMENT (TIME 2): " + str(time.time_ns()))
    response = bl_mapper.update_blockchain_slice(subnet_element)
    if response[1] != 200:
        # TODO: exception/error management
        pass
    
    mutex_slice2blockchaindb_access.acquire()
    response = db.update_db(subnet_element["id"], subnet_element, "blockchain_subnets")
    if response[1] != 200:
        # TODO: exception/error management
        pass
    mutex_slice2blockchaindb_access.release()

# NOTE: updates a slice-subnet information belonging to another domain (Blockchain)
def update_slicesubnet_from_blockchain(subnet_json):
    settings.logger.info("ORCH: Updating slice-subnet information from another domain. Slice-Subnet ID: " +str(subnet_json['instanceId']))
    
    # look in the local nsi db which nsi has the updated slice subnet
    found_nsi = False
    response = db.get_elements("slices")

    for nsi_item in response:
        for slice_subnet_item in nsi_item["slice_subnets"]:
            if slice_subnet_item["id"] == subnet_json['instanceId']:
                slice_subnet_item["status"] = subnet_json['status']
                slice_subnet_item["log"] = "Slice-subnet (from another domain)" + str(subnet_json['status'])
                
                # saves the nsi object into the db
                mutex_slice2db_access.acquire()
                db.update_db(nsi_item["id"], nsi_item, "slices")
                mutex_slice2db_access.release()
                
                found_nsi = True
                break
        if found_nsi:
            break

# TODO: manages all the E2E Slice termination process
def terminate_e2e_slice(e2e_slice_json):
    # gets nsi based on an ID
    nsi_element = db.get_element(e2e_slice_json['id'], "slices")
    nsi_element["status"] = "TERMINATING"
    #nsi_element["log"] = "Requesting to remove VLs."
   
    # TODO checks e2e_vl sections
    #   FOR LOOP to request VL removal
    #   WAITS until their are all removed
    
    # TODO: (once Vl removal works) updates nsi data object (log)
    
    
    # checks slice-subnets
    for slice_subnet_item in nsi_element["slice_subnets"]:
        # if it has a blockchain owner, the request must be towards the blockchain environment
        if "blockchain_owner" in slice_subnet_item.keys():
            settings.logger.info("ORCH: Request slice-subnet termination to BL NSM")
            response = bl_mapper.terminate_blockchain_slice(slice_subnet_item)
            slice_subnet_item["log"] = response[0]['log']
            slice_subnet_item["status"] = response[0]['status']
        else:
            #LOCAL TERMINATION PROCESS IS CALLED
            data_json = {}
            data_json['instance_uuid'] = slice_subnet_item["instance_id"]
            data_json['request_type'] = 'TERMINATE_SLICE'
            settings.logger.info("ORCH: Request slice-subnet termination to local NSM")
            response = slice_mapper.terminate_slice_subnet(data_json)                         # TODO: response is emulated while developing.
            
            if (response[1] == 200 or response[1] == 201):
                slice_subnet_item["log"] = "This slice subnet is being terminated."
                slice_subnet_item["status"] = "TERMINATING"
                slice_subnet_item['request_id'] = response[0]['id']   #jsonresponse['id']
    
    # saves the nsi object into the db
    mutex_slice2db_access.acquire()
    nsi_element["log"] = "VLs removed. Requesting to terminate slice-subnets."
    response = db.add_element(nsi_element, "slices")
    if response != 200:
        pass                # TODO: trigger exception/error
    mutex_slice2db_access.release()
    
    # awaits for all the slice-subnets to be instantiated
    settings.logger.info("ORCH: Waiting for al slice-subnets instantes to be terminated. E2E SLICE ID: " +str(nsi_element["id"]))
    all_subnets_ready = False
    while(all_subnets_ready == False):
        #time.sleep(30)                  # sleep of 30s (maybe a minute?) to let all the process begin
        subnets_terminated = 0        # used to check how many subnets are in instantiated and change e2e slice status
        for slice_subnet_item in nsi_element["slice_subnets"]:
            if (slice_subnet_item['status'] == 'TERMINATING'):
                if ('blockchain_owner' not in slice_subnet_item):
                    response = slice_mapper.get_slice_subnet_instance(slice_subnet_item['instance_id'])
                    jsonresponse = response[0]
                    if (jsonresponse['status'] == "TERMINATED"):
                        slice_subnet_item['status'] = jsonresponse['status']
                        slice_subnet_item['log'] = "Slice_subnet terminated."
                        subnets_terminated = subnets_terminated + 1
            elif(slice_subnet_item['status'] == 'TERMINATED'):
                # all slice-subnets deployed in other domains, are updated by the blockchain event thread.
                subnets_terminated = subnets_terminated + 1
            else:
                #TODO: ERROR management
                pass
        
        # if the number of slice-subnets instantiated = total number in the e2e slice, finishes while
        if (subnets_terminated == len(nsi_element['slice_subnets'])):
            all_subnets_ready = True
    
    nsi_element["status"] = "TERMINATED"
    nsi_element["log"] = "E2E Network Slice TERMINATED."

    # saves the nsi object into the db
    mutex_slice2db_access.acquire()
    db.update_db(nsi_element["id"], nsi_element, "slices")
    mutex_slice2db_access.release()
    settings.logger.info('E2E Network Slice INSTANTIATED. E2E Slice ID: ' + str(nsi_element["id"]))

# TODO: manages a local slice-subnet termination process
def terminate_local_slicesubnet(subnet_json):
    settings.logger.info("ORCH: Received slice-subnet termination request from Blockchain. NSI Ref:: " +str(subnet_json['nst_ref']))
    
    #gets specific NST information
    blockchain_subnet = db.get_element(subnet_json['id'], "blockchain_subnets")

    # LOCAL INSTANTIATION PROCESS IS CALLED
    data_json = {}
    data_json['instance_uuid'] = blockchain_subnet["instance_id"]
    data_json['request_type'] = 'TERMINATE_SLICE'
    settings.logger.info("ORCH: Request slice-subnet termination to local NSM")
    response = slice_mapper.terminate_slice_subnet(data_json)                         # TODO: response is emulated while developing.
    if (response[1] != 200 or response[1] != 201):
        # TODO: exception/error management
        pass
    
    blockchain_subnet['request_id'] = response[0]['id']
    blockchain_subnet['status'] = subnet_json['status']
    blockchain_subnet['log'] = "Terminating Slice-subnet."
    
    # saves the nsi object into the db
    mutex_slice2blockchaindb_access.acquire()
    response = db.add_element(blockchain_subnet, "blockchain_subnets")
    if response[1] != 200:
        # TODO: exception/error management
        pass
    mutex_slice2blockchaindb_access.release()

    # Instantiation procedure control
    subnet_ready = False
    while(subnet_ready == False):
        response = slice_mapper.get_slice_subnet_instance_request(blockchain_subnet['request_id'])
        jsonresponse = response[0]
        if (jsonresponse['status'] == "TERMINATED"):
            subnet_ready = True
        else:
            # TODO: exception/error management
            pass
    
    # Once termination is done, updates Blockchain and local DB
    blockchain_subnet['instance_id'] = jsonresponse['instance_uuid']
    blockchain_subnet['status'] = jsonresponse['status']
    blockchain_subnet['log'] = "Slice-subnet terminated."

    response = bl_mapper.update_blockchain_slice(blockchain_subnet)
    if response[1] != 200:
        # TODO: exception/error management
        pass
    
    mutex_slice2blockchaindb_access.acquire()
    response = db.update_db(blockchain_subnet["id"], blockchain_subnet, "blockchain_subnets")
    if response[1] != 200:
        # TODO: exception/error management
        pass
    mutex_slice2blockchaindb_access.release()
    settings.logger.info("ORCH: Deployed slice-subnet from Blocckhain request. NSI Ref: " +str(blockchain_subnet['id']))
