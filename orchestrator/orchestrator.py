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
    if response[0] == "empty":
        e2e_topology = {}
        e2e_topo = {}
        e2e_nodes_list = []
        e2e_idl_list = []

        for node_item in idl_json["e2e-topology"]["nodes-list"]:
            e2e_nodes_list.append(node_item)
        e2e_topo["nodes-list"] = e2e_nodes_list
        
        for idl_item in idl_json["e2e-topology"]["interdomain-links"]:
            e2e_idl_list.append(idl_item)
        e2e_topo["interdomain-links"] = e2e_idl_list

        e2e_topology["e2e-topology"] = e2e_topo
    else:
        e2e_topology = response[0]
        e2e_nodes_list = e2e_topology["e2e-topology"]["nodes-list"]
        for node_item in idl_json["e2e-topology"]["nodes-list"]:
            if node_item not in e2e_nodes_list:
                e2e_nodes_list.append(node_item)
        e2e_topology["e2e-topology"]["nodes-list"] = e2e_nodes_list
        e2e_idl_list = e2e_topology["e2e-topology"]["interdomain-links"]
        for idl_item in idl_json["e2e-topology"]["interdomain-links"]:
            found_existing_idl = False
            for ref_idl in e2e_idl_list:
                if idl_item["name"] == ref_idl["name"]:
                    found_existing_idl = True
                    break
            if found_existing_idl == False:
                e2e_idl_list.append(idl_item)
        e2e_topology["e2e-topology"]["interdomain-links"] = e2e_idl_list
    
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
    
    print("ORCH: ------- A")
    response = bl_mapper.get_context_sips_nodes_links_from_blockchain(context_json)
    print("ORCH: ------- B")
    context_json = response[0]
    print("context_json_type: " + type(context_json))
    print("ORCH: ------- C")
    print(context_json["id"])
    tapi_common_context["uuid"] = context_json["id"]
    print("ORCH: ------- D")
    tapi_common_context["name"] = context_json["name_context"]
    print("ORCH: ------- E")
    tapi_common_context["service-interface-point"] = context_json["sip"]
    print("ORCH: ------- F")
    topo_metadata = json.loads(context_json["topo_metadata"])
    print("ORCH: ------- G")
    topology_element["uuid"] = topo_metadata["uuid"]
    print("ORCH: ------- H")
    topology_element["layer-protocol-name"] = topo_metadata["layer-protocol-name"]
    print("ORCH: ------- I")
    topology_element["name"] = topo_metadata["name"]
    print("ORCH: ------- J")
    topology_element["node"] = json.loads(context_json["node_topo"])
    print("ORCH: ------- K")
    topology_element["link"] = json.loads(context_json["link_topo"])
    print("ORCH: ------- L")
    topology.append(topology_element)
    print("ORCH: ------- M")
    tapi_topology_context["nw-topology-service"] = context_json["nw_topo_serv"]
    print("ORCH: ------- N")
    tapi_topology_context["topology"] = topology
    print("ORCH: ------- O")
    tapi_common_context["tapi-topology:topology-context"] = tapi_topology_context
    print("ORCH: ------- P")
    tapi_context_json["tapi-common:context"] = tapi_common_context
    print("ORCH: ------- Q")

    print(type(tapi_context_json))
    print(tapi_context_json)

    #vl_computation.add_context_e2e_graph(tapi_context_json)

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
def instantiate_local_connectivity_service(cs_json):
    settings.logger.info("ORCH: Received request to deploy a local CS: " +str(cs_json))
    response = sdn_mapper.instantiate_connectivity_service(cs_json)
    if response[1] != 200:
        # manage epossible errors by informing to the original requester
        pass   
    
    mutex_local_csdb_access.acquire()
    db.add_cs(cs_json)
    mutex_local_csdb_access.release()

    cs_json['status'] = "READY"
    response = bl_mapper.update_blockchain_cs(cs_json)

# updates a CS information belonging to another domain (Blockchain)
def update_connectivity_service_from_blockchain(cs_json):
    settings.logger.info("ORCH: Updating connectivity services information from another domain.")
    
    """
    # look in the local nsi db which nsi has the updated connectivity service of one of its virtual links.
    found_nsi = False
    response = db.get_elements("slices")

    for nsi_item in response:
        for slice_vl_item in nsi_item["slice_vls"]:
            if slice_vl_item["vl_id"] == cs_json['vl_ref']:
                for cs_item in slice_vl_item['cs_list']:
                    if cs_item['id'] == cs_json['id']:
                        cs_item['status'] = cs_json['status']
                        cs_item['blockchain_owner'] = cs_json['blockchain_owner']
                
                        # saves the nsi object into the db
                        mutex_slice2db_access.acquire()
                        db.update_db(nsi_item["id"], nsi_item, "slices")
                        mutex_slice2db_access.release()
                        
                        found_nsi = True
                        break
            if found_nsi:
                break
        if found_nsi:
            break
    """
    mutex_e2e_csdb_access.acquire()
    #db.add_element(e2e_cs_json, "e2e_cs")
    e2ecs_list = db.get_elements("e2e_cs")
    for e2ecs_item in e2ecs_list:
        for domaincs_item in e2ecs_item["domain-CS"]:
            if domaincs_item["uuid"] == cs_json["id"]:
                domaincs_item["status"] = "READY"
                found_cs = True
                break
        if found_cs == True:
            db.update_db(e2ecs_item["uuid"], e2ecs_item, "e2e_cs")
            break
    mutex_e2e_csdb_access.release()

"""
Example E2E_CS request 
    {
        "node-source": {
            "uuid": "SDN_domain_uuid",
            "sip": "sip_uuid",
        },
        "node-destination": {
            "uuid": "SDN_domain_uuid",
            "sip": "sip_destination_uuid",
        },
        "capacity": {
            "value": 150,
            "unit": "GHz"
        }
    }
Example E2E_CS data object 
    {
        "uuid": "uuid_e2e_cs",
        "status" : DEPLOYED/TERMINATED,
        "node-source": {
            "uuid": "node_uuid",
            "sip": "sip_uuid",
        },
        "node-destination": {
            "uuid": "node_uuid",
            "sip": "sip_destination_uuid",
        },
        "capacity": {
            "value": 150,
            "unit": "GHz"
        },
        "spectrum": {
            "higher-freq": 191700000,
            "lower-freq": 191850000
        },
        "route":[
            #info guardada amb el route_node_domain parameter
            "node_uuid",
            "node_uuid",
            "node_uuid
        ],
        "domain-CS":[
            {
                "uuid": "uuid_CS",
                "address_peer": "blockchain-peer_address"
            }
        ]
    }
"""
# manages the creation of an E2E CS
def instantiate_e2e_connectivity_service(e2e_cs_request):
    # defines e2e CS data object parameters
    e2e_cs_json = {}
    spectrum_list = []
    domain_CS = []
    e2e_topology_json = bl_mapper.get_e2etopology_from_blockchain()

    # assigns initial CS data object information
    e2e_cs_json["uuid"] = uuid.uuid4()
    e2e_cs_json["node-source"] = e2e_cs_request["node-source"]
    e2e_cs_json["node-destination"] = e2e_cs_request["node-destination"]
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
    src = e2e_cs_request["node-source"]["uuid"]
    dst = e2e_cs_request["node-destination"]["uuid"]
    route_nodes_list = vl_computation.find_path(src, dst)
    e2e_cs_json["route"] = route_nodes_list

    # SPECTRUM ASSIGNMENT procedure (first a SIPs route is created. Then, it checks their spectrum availability)    
    # if one route does not have a slot, passes to the next one
    for route_item in route_nodes_list:
        # idetifies the NEPs between inter-domain links
        response_nep_mapped = vl_computation.domain2nep_route_mapping(route_item, e2e_topology_json)
        if response_nep_mapped[0] and response_nep_mapped[1]:
            # identifies the SIP used for each NEP in the route
            route_sips = vl_computation.nep2sip_route_mapping(response_nep_mapped[0], e2e_cs_request)
            
            # generates available spectrums list from interdomain links & internal neps
            for interdomainlink_item in response_nep_mapped[1]:
                spectrum_list.append(interdomainlink_item["available_spectrum"])
            # it will access only when working in transparent abstraction mode
            if route_sips[2]: 
                for internal_nep_item in route_sips[2]:
                    # get specific domain topology to discover the correct SIP to use
                    response = bl_mapper.get_context_from_blockchain(internal_nep_item["topology"])
                    domain_context = response['context']
                    # look inot all the nodes of the incoming context
                    for node_item in domain_context["tapi-common:context"]["tapi-topology:topology-context"]["topology"][0]["node"]:
                        for owned_nep_item in node_item["owned-node-edge-point"]:
                            if owned_nep_item["uuid"] == internal_nep_item["nep_uuid"]:
                                available_slots = owned_nep_item["tapi-photonic-media:media-channel-node-edge-point-spec"]["mc-pool"]["available-spectrum"]
                                for available_item in available_slots:
                                    spectrum_slot = []
                                    spectrum_slot.append(available_item["lower-frequency"])
                                    spectrum_slot.append(available_item["upper-frequency"])
                                    spectrum_list.append(spectrum_slot)
            
            # checks if there is a common spectrum slot based on the available in all the neps and interdomain links in the route
            selected_spectrum = vl_computation.spectrum_assignment(spectrum_list, capacity)
        
        # rsa done is complete: routing path computed and spectrum slot selected
        if selected_spectrum:
            break

    # generates the domain CSs requests [{sip_info, "topology", "blockchain_owner"},{...},...]]
    # route_sips[0] -> route of SIPs 
    # route_sips[1] -> list of context links per each CS (only transparent abstraction) [{link_uuid, topology},{}...]
    # capacity
    # selected_spectrum --> frequency slots
    spectrum = {}
    spectrum["low-freq"] = selected_spectrum[0]
    spectrum["high-freq"] = selected_spectrum[1]
    e2e_cs_json["spectrum"] = spectrum    
    
    cs_list = []
    iter_sips = iter(route_sips[0]) #iter is used to work using pairs of elements
    for sip_item in iter_sips:
        # checks that each pair of sips belongs to the same owner, otherwise does not generate the cs_info
        if sip_item["topology"] == next(iter_sips["topology"]):
            cs_info = {}
            constrained_links = []
            cs_uuid = uuid.uuid4()
            cs_info["uuid"] = cs_uuid
            cs_info["address_owner"] = sip_item["address_owner"]
            cs_info["topology-uuid"] = sip_item["topology"]
            sip_list = []
            sip_list.append(sip_item["uuid"])
            sip_list.append(next(iter_sips["uuid"]))
            cs_info["sips"] = sip_list
            cs_info["capacity"] = e2e_cs_request["capacity"]
            cs_info["spectrum_slot"] = spectrum
            
            # adds the list of constrained links for the current domain CS
            # NOTE: this IF will be accessed only in transparent abstraction mode
            if route_sips[1]:
                for link_item in route_sips[1]:
                    if link_item["topology"] == sip_item["topology"]:
                        constrained_links.append(link_item["topology"])
            cs_info["constrained_links"] = constrained_links
            cs_list.append(cs_info)
        else:
            # if the two sips belong to two different domains, it passes to the next item.
            continue
    
    e2e_cs_json["domain-CS"] = cs_list
    mutex_e2e_csdb_access.acquire()
    db.add_elemente_db(e2e_cs_json, "e2e_cs")
    mutex_e2e_csdb_access.release()
    
    # FOR loop to send domain CSs requests
    for cs_item in cs_list:
        # decide whether the CS is for the local domain SDN controller or another domain
        if cs_item["address_owner"] == str(settings.web3.eth.defaultAccount):
            response = sdn_mapper.instantiate_connectivity_service(cs_item)
            if response[1] == 200:
                mutex_local_csdb_access.acquire()
                db.add_cs(response[1])
                mutex_local_csdb_access.release()
        else:
            response = bl_mapper.instantiate_blockchain_cs(cs_item["address_owner"], cs_item, cs_item["uuid"])
    
        if response[1] != 200:
            # ERROR!! NOTE: think how to manage it
            break

    # WHILE LOOP to validate all domain CSs composing the E2E CS are READY
    while  e2e_cs_ready == False:
        e2e_cs_ready = True
        mutex_e2e_csdb_access.acquire()
        e2e_cs = db.get_element(e2e_cs_json["uuid"], "e2e_cs")
        for domainCS_item in e2e_cs["domain-CS"]:
            if domainCS_item["status"] != "READY":
                e2e_cs_ready = False
                break
        mutex_e2e_csdb_access.release()
        time.sleep(10)  # awaits 10 seconds before it checks again

    e2e_cs_json["status"]  = "READY"
    mutex_e2e_csdb_access.acquire()
    db.update_db(e2e_cs_json["uuid"], e2e_cs_json, "e2e_cs")
    mutex_e2e_csdb_access.release()
    
    return e2e_cs_json,200

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
