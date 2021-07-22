#!/usr/local/bin/python3.4
 
import os, sys, logging, json, argparse, time, datetime, requests, uuid
from web3 import Web3

from config_files import settings

###################################### BLOCKCHAIN MAPPER FOR NETWORK SLICES #######################################
# NOTE: adds slice-subnet (NST) information into the blockchain
def slice_to_blockchain(nst_json):
    settings.logger.info('BLOCKCHAIN_MAPPER: Distributes local slice-subnet template information with Blockchain peers.')
    # Add a slice template to make it available for other domains
    tx_hash = settings.slice_contract.functions.addSliceTemplate(str(nst_json["id"]), nst_json["name"], nst_json["version"], nst_json["vendor"], nst_json["price"], nst_json["unit"]).transact()
    
    # Wait for transaction to be mined and check it's in the blockchain (get)
    settings.web3.eth.waitForTransactionReceipt(tx_hash)
    
    response = settings.slice_contract.functions.getSliceTemplate(str(nst_json["id"])).call()
    
    nst_json['blockchain_owner'] = response[5]
    return nst_json, 200

#TODO: returns all slice-subnets (NSTs) information from other domains
def slices_from_blockchain():
    settings.logger.info('BLOCKCHAIN_MAPPER: Requests all Blockchain slice-subnet template information.')
    pass 

# NOTE: returns a specific slice-subnet (NST) information from another domain
def slice_from_blockchain(slice_ID):
    # TODO: IMPROVE this function when solidity will allow to return an array of strings (or multidimensional elements like json).
    settings.logger.info('BLOCKCHAIN_MAPPER: Requests Blockchain slice-subnet template information. ID: ' + str(slice_ID))
    response = settings.slice_contract.functions.getSliceTemplate(slice_ID).call()
    nst_json = {}
    nst_json['id'] = slice_ID
    nst_json['name'] = response[0]
    nst_json['version'] = response[1]
    nst_json['vendor'] = response[2]
    nst_json['price'] = response[3]
    nst_json['unit'] = response[4]
    nst_json['blockchain_owner'] = response[5]
    return nst_json, 200

# NOTE: returns the number of slice-subnets (NSTs) in the blockchain db
def get_slices_counter():
    response = settings.slice_contract.functions.getSliceTemplateCount().call()
    return response

# NOTE: returns the slice-subnet (NST) ID based on the index position within the slice_subnets list in the blockchain
def get_slice_id(index):
    response = settings.slice_contract.functions.getSliceTemplateId(index).call()
    return response

# NOTE: requests the deployment of a slice-subnet template (NST) from another domain
def deploy_blockchain_slice(ref_slice_subnet):
    settings.logger.info('BLOCKCHAIN_MAPPER: Starts Blockchain deployment (TIME 3): ' + str(time.time_ns()))
    settings.logger.info('BLOCKCHAIN_MAPPER: Distributes request to deploy slice-subnet in the Blockchain: ' + str(ref_slice_subnet))
    # instantiate slice-subnet
    tx_hash = settings.slice_contract.functions.instantiateSlice(str(ref_slice_subnet["id"]), ref_slice_subnet["nst_ref"]).transact()
    
    # Wait for transaction to be added and check it's in the blockchain (get)
    tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
    
    #listen the event associated to the transaction receipt
    rich_logs = settings.slice_contract.events.slice_response().processReceipt(tx_receipt)
    
    #create json to send back to the user the initial instantiation request info.
    deployment_response = {}
    deployment_response["log"] = rich_logs[0]['args']['log']
    deployment_response["status"] = rich_logs[0]['args']['status']
    
    return deployment_response, 200

# NOTE: requests the termination of a slice-subnet instance (NSI) from another domain
def terminate_blockchain_slice(ref_slice_subnet):
    settings.logger.info('BLOCKCHAIN_MAPPER: Distributes request to terminate slice-subnet in the Blockchain: ' + str(ref_slice_subnet))
    # terminate slice-subnet
    tx_hash = settings.slice_contract.functions.terminateSlice(ref_slice_subnet['id']).transact()
    
    # Wait for transaction to be added and check it's in the blockchain (get)
    tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
    
    #listen the event associated to the transaction receipt
    rich_logs = settings.slice_contract.events.slice_response().processReceipt(tx_receipt)
    
    #create json to send back to the user the initial instantiation request info.
    deployment_response = {}
    deployment_response["log"] = rich_logs[0]['args']['log']
    deployment_response["status"] = rich_logs[0]['args']['status']
    
    return deployment_response, 200

# NOTE: requests to update a slice-subnet element in the Blockchain
def update_blockchain_slice(subnet_json):
    settings.logger.info("BLOCKCHAIN_MAPPER: Updating information about local deployment (TIME 3): " + str(time.time_ns()))
    settings.logger.info('BLOCKCHAIN_MAPPER: Updates slice-subnet element inside Blockchain. Element ID: ' + str(subnet_json))
    # Add a service
    tx_hash = settings.slice_contract.functions.updateInstance(subnet_json['id'], subnet_json['status'], subnet_json['log']).transact()

    # Wait for transaction to be mined and check it's in the blockchain (get)
    tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
    
    #listen the event associated to the transaction receipt
    rich_logs = settings.slice_contract.events.slice_response().processReceipt(tx_receipt)

    deployment_response = {}
    deployment_response["log"] = rich_logs[0]['args']['log']
    deployment_response["status"] = rich_logs[0]['args']['status']
    
    return deployment_response, 200

###################################### BLOCKCHAIN MAPPER FOR IDLs, SDN CONTEXT & CSs #######################################
# distributes the domain associated inter-domain links (IDL) with the other peers
def interdomainlinks_to_blockchain(idl_json, e2e_topology):
    settings.logger.info('BLOCKCHAIN_MAPPER: Distributes known IDLs & updates the e2e topology element saved in the Blockchain.')
    idl_string = json.dumps(idl_json)
    e2e_topology_string = json.dumps(e2e_topology)
    
    # Add a connectivity service template to make it available for other domains
    tx_hash = settings.transport_contract.functions.addIDLContext(idl_string, e2e_topology_string).transact()
    settings.logger.info('BLOCKCHAIN_MAPPER: Transaction for new IDL done.')
    
    # Wait for transaction to be mined and check it's in the blockchain (get)
    tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
    settings.logger.info('BLOCKCHAIN_MAPPER: Transaction receipt.')

    msg = {}
    msg["msg"] = "Everything OK"
        
    return msg, 200

# distributes link-option to the BL
def linkoption_to_blockchain(linkoption_json):
    id = linkoption_json["uuid"]
    dir = linkoption_json["direction"]
    nodesdir = json.dumps(linkoption_json["nodes-direction"])
    lpn = json.dumps(linkoption_json["layer-protocol-name"])
    phyopt = json.dumps(linkoption_json["physical-options"])
    sup = json.dumps(linkoption_json["supportable-spectrum"])
    av = json.dumps(linkoption_json["available-spectrum"])
    tx_hash = settings.transport_contract.functions.addLinkOption(id, dir, nodesdir, lpn, phyopt,sup, av).transact()
    
    # Wait for transaction to be mined and check it's in the blockchain (get)
    tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
    
    msg = {}
    msg["msg"] = "Everything OK"
        
    return msg, 200

# returns the number of slice-subnets (NSTs) in the blockchain db
def get_idl_counter():
    response = settings.transport_contract.functions.getIDLContextCount().call()
    return response

# returns the slice-subnet (NST) ID based on the index position within the slice_subnets list in the blockchain
def get_idl_id(index):
    response = settings.transport_contract.functions.getIDLContextId(index).call()
    return response

# returns IDLs information from blockchain
def get_e2etopology_from_blockchain():
    # TODO: IMPROVE this function when solidity will allow to return an array of strings (or multidimensional elements like json).
    settings.logger.info('BLOCKCHAIN_MAPPER: Requests Blockchain E2E Topology information.')
    response = settings.transport_contract.functions.getE2EContext().call()
    if (not response):
        context_json = "empty"
    else:
        converted_response = response.replace("'", "\"")
        context_json = json.loads(converted_response)
    return context_json, 200

# returns a link-option belonging to an IDL from blockchain
def get_linkOption_from_blockchain(link_option_uuid):
    # TODO: IMPROVE this function when solidity will allow to return an array of strings (or multidimensional elements like json).
    response = settings.transport_contract.functions.getLinkOption(link_option_uuid).call()
    linkoption_json = {}
    linkoption_json["uuid"] = link_option_uuid
    linkoption_json["direction"] = response[0]
    linkoption_json["nodes-direction"] = json.loads(response[1])
    linkoption_json["layer-protocol-name"] = json.loads(response[2])
    linkoption_json["physical-options"] = json.loads(response[3])
    linkoption_json["supportable-spectrum"] = json.loads(response[4])
    linkoption_json["available-spectrum"] = json.loads(response[5])
    return linkoption_json, 200

# update e2e_topology in the BL
def update_e2e_topology(e2e_topo):
    settings.logger.info('BLOCKCHAIN_MAPPER: Updating E2E Topology.')
    e2e_string = json.dumps(e2e_topo)
    response = settings.transport_contract.functions.updateE2EContext(e2e_string).call()

    return '{"msg":"E2E topology updated in the BL."}', 200

# distributes the domain SDN context with the other peers
def context_to_blockchain(context_json):
    settings.logger.info('BLOCKCHAIN_MAPPER: Distributes local SDN context information with Blockchain peers.')
    id_string = context_json["id"]
    name_context = context_json["name_context"]
    nw_topo_serv = context_json["nw_topo_serv"]
    topo_metadata = context_json["topo_metadata"]
    sip_uuid_list = []
    node_uuid_list = []
    link_uuid_list = []
    
    # Distributes the sips in the SDN context.
    settings.logger.info('BLOCKCHAIN_MAPPER: Distributing SIPs.') 
    for sip_item in json.loads(context_json["sip"]):
        bl_sip_uuid = context_json["id"]+":"+sip_item["uuid"]
        sip_string = json.dumps(sip_item)
        tx_hash = settings.transport_contract.functions.addSip(bl_sip_uuid, sip_string).transact()
        tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
        
        sip_uuid_list.append(sip_item["uuid"])
    
    # Distributes the nodes and their NEPs in the SDN context.
    settings.logger.info('BLOCKCHAIN_MAPPER: Distributing Node.')
    node_topo = json.loads(context_json["node_topo"])
    for node_item in node_topo:
        #TODO: distribution of NEPS for each node
        neps_uuid_list = []
        for nep_item in node_item["owned-node-edge-point"]:
            bl_nep_uuid = context_json["id"]+":"+node_item["uuid"]+":"+nep_item["uuid"]
            nep_string = json.dumps(nep_item)
            tx_hash = settings.transport_contract.functions.addNep(bl_nep_uuid, nep_string).transact()
            tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
            neps_uuid_list.append(nep_item["uuid"])

        bl_node_uuid = context_json["id"]+":"+node_item["uuid"]        
        tx_hash = settings.transport_contract.functions.addNode(bl_node_uuid, json.dumps(node_item["name"]), json.dumps(neps_uuid_list)).transact()
        tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
        node_uuid_list.append(node_item["uuid"])
    
    # Distributes the links in the SDN context if there are.
    if json.loads(context_json["link_topo"]) == []:
        settings.logger.info('BLOCKCHAIN_MAPPER: There are NO Links to distribute.')
    else:
        settings.logger.info('BLOCKCHAIN_MAPPER: Distributing Links.')
        for link_item in json.loads(context_json["link_topo"]):
            bl_link_uuid = context_json["id"]+":"+link_item["uuid"]
            link_string = json.dumps(link_item)
            tx_hash = settings.transport_contract.functions.addLink(bl_link_uuid, link_string).transact()
            tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
            
            link_uuid_list.append(link_item["uuid"])
    
    # Add a connectivity service template to make it available for other domains
    settings.logger.info('BLOCKCHAIN_MAPPER: Triggering transaction for new context.')
    tx_hash = settings.transport_contract.functions.addContextTemplate(id_string, name_context, json.dumps(sip_uuid_list), nw_topo_serv, topo_metadata, json.dumps(node_uuid_list), json.dumps(link_uuid_list)).transact()
    
    # Wait for transaction to be mined and check it's in the blockchain (get)
    tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
    settings.logger.info('BLOCKCHAIN_MAPPER: Transaction for new context done.')

    #rich_logs = settings.transport_contract.events.topology_response().processReceipt(tx_receipt)
    #settings.logger.info('BLOCKCHAIN_MAPPER: topology_event.' + str(rich_logs))

    #response = settings.transport_contract.functions.getContextTemplate(str(context_json["id"])).call()
    #create json to send back to the user the initial instantiation request info.
    #deployment_response = {}
    #deployment_response["log"] = rich_logs[0]['args']['log']
    #deployment_response["status"] = rich_logs[0]['args']['status']
    #deployment_response["owner"] = rich_logs[0]['args']['requester']
    #print(str(deployment_response))

    msg = {}
    msg["msg"] = "Everything OK"
    
    return msg, 200

# gets specific context info and returns a JSON
def get_context_from_blockchain(context_ID):
    #settings.logger.info('BLOCKCHAIN_MAPPER: Requests Blockchain context information (sips, nodes and links).' )
    response = settings.transport_contract.functions.getContextTemplate(context_ID).call()
    context_json = {}
    context_json["uuid"] =  context_ID
    context_json["name_context"] =  response[0]
    context_json["sip"] =  response[1]
    context_json["nw_topo_serv"] =  response[2]
    context_json["topo_metadata"] =  response[3]
    context_json["node_topo"] =  response[4]
    context_json["link_topo"] =  response[5]
    context_owner = response[6]

    #contstruct the context information as a single json.
    sdn_json = {}
    tapi_context_json={}
    tapi_common_context = {}
    tapi_topology_context = {}
    topology = []
    topology_element = {}

    response = get_context_sips_nodes_links_from_blockchain(context_json)
    response_json = response[0]
    tapi_common_context["uuid"] = response_json["uuid"]
    tapi_common_context["name"] = json.loads(response_json["name_context"])

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
    
    sdn_json["context"] = tapi_context_json
    sdn_json["blockchain_owner"] = context_owner

    return sdn_json, 200

# return all the sips, nodes and links belonging to a specific context to build the json with the complete TAPI format
def get_context_sips_nodes_links_from_blockchain(context_json):
    # GETs and prepares the SIPs info
    sips_list = []
    for sip_uuid in json.loads(context_json["sip"]):
        sip_ref = context_json["uuid"]+":"+sip_uuid
        response = settings.transport_contract.functions.getSIP(sip_ref).call() 
        sips_list.append(response[0])
    context_json["sip"] = sips_list
    
    # GETs and prepares the nodes info
    nodes_list = []
    for node_uuid in json.loads(context_json["node_topo"]):
        # the nodes info comes in a 2-step process, first the node and then its neps
        node_ref = context_json["uuid"]+":"+node_uuid
        node_response = settings.transport_contract.functions.getNode(node_ref).call()
        node_item = {}
        node_item["uuid"] = node_uuid
        node_item["name"] = json.loads(node_response[0])
        neps_uuid_list = json.loads(node_response[1])
        string_neps_list = []
        for nep_uuid in neps_uuid_list:
            nep_ref = context_json["uuid"]+":"+node_uuid+":"+nep_uuid
            nep_esponse = settings.transport_contract.functions.getNep(nep_ref).call()
            string_neps_list.append(json.loads(nep_esponse))
        node_item["owned-node-edge-point"] = string_neps_list
        nodes_list.append(json.dumps(node_item))
    context_json["node_topo"] = nodes_list

    # GETs and prepares the links info
    links_list = []
    linklist = json.loads(context_json["link_topo"])
    if linklist:
        for link_uuid in linklist:
            link_ref = context_json["uuid"]+":"+link_uuid
            response = settings.transport_contract.functions.getLink(link_ref).call() 
            links_list.append(response)
    context_json["link_topo"] = links_list
    
    return context_json, 200

# returns the number of slice-subnets (NSTs) in the blockchain db
def get_context_counter():
    response = settings.transport_contract.functions.getContextTemplateCount().call()
    return response

# returns the slice-subnet (NST) ID based on the index position within the slice_subnets list in the blockchain
def get_context_id(index):
    response = settings.transport_contract.functions.getContextTemplateId(index).call()
    return response

# returns the slice-subnet (NST) ID based on the index position within the slice_subnets list in the blockchain
def get_sip(index):
    response = settings.transport_contract.functions.getSIP(index).call()
    response_json = {}
    response_json["sip_info"] = json.loads(response[0])
    response_json["owner"] = response[1]
    return response_json

# updates a specific NEP info in the BL
def update_sip(sip_id, sip_json):
    sip_string = json.dumps(sip_json)
    tx_hash = settings.transport_contract.functions.updateNep(sip_id, sip_string).transact()
    tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
    return sip_id, 200

# returns a specific NEP info
def get_nep(index):
    response = settings.transport_contract.functions.getNep(index).call()
    nep_json = response.loads()
    return nep_json

# updates a specific NEP info in the BL
def update_nep(nep_id, nep_json):
    nep_string = json.dumps(nep_json)
    tx_hash = settings.transport_contract.functions.updateNep(nep_id, nep_string).transact()
    tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
    return nep_id, 200

# requests the deployment of a CS between domains
def instantiate_blockchain_cs(address, cs_json, spectrum, capacity):
    settings.logger.info('BLOCKCHAIN_MAPPER: Distributes request to configure connectivity service in the Blockchain')
    cs_string = json.dumps(cs_json)
    spectrum_string = json.dumps(spectrum)
    capacity_string = json.dumps(capacity)
    
    print("Before distributing domain CS.")
    # instantiate slice-subnet
    tx_hash = settings.transport_contract.functions.instantiateConnectivityService(address, cs_json["uuid"], cs_string, spectrum_string, capacity_string).transact()
    print("After distributing domain CS.")
    # Wait for transaction to be added and check it's in the blockchain (get)
    tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
    
    #listen the event associated to the transaction receipt
    rich_logs = settings.transport_contract.events.topology_response().processReceipt(tx_receipt)
    
    #create json to send back to the user the initial instantiation request info.
    deployment_response = {}
    deployment_response["log"] = rich_logs[0]['args']['log']
    deployment_response["status"] = rich_logs[0]['args']['status']
    print("Domain CS requests distributed.")
    
    return deployment_response, 200

# TODO: requests the termination of a CS between domains
def terminate_blockchain_cs(ref_cs):
    pass

# NOTE: requests to update a connectivity service element in the Blockchain
def update_blockchain_cs(cs_json):
    settings.logger.info('BLOCKCHAIN_MAPPER: Updates connectivity service element within the Blockchain.')
    cs_uuid = cs_json["cs_info"]['uuid']
    cs_string = json.dumps(cs_json)
    cs_status = cs_json["cs_info"]['status']
    print("Before distributing updated domain CS.")
    # distribute the updated domain CS information
    tx_hash = settings.transport_contract.functions.updateConnectivityService(cs_uuid, cs_string, cs_status).transact()
    print("After distributing updated domain CS.")
    # Wait for transaction to be mined and check it's in the blockchain (get)
    tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
    
    #listen the event associated to the transaction receipt
    rich_logs = settings.transport_contract.events.topology_response().processReceipt(tx_receipt)

    deployment_response = {}
    deployment_response["log"] = rich_logs[0]['args']['log']
    deployment_response["status"] = rich_logs[0]['args']['status']
    print("Updated Domain CS requests distributed.")
    return deployment_response, 200
