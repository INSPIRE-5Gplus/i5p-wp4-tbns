#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
from threading import Lock

from slice_subnet_mapper import slice_subnet_mapper as slice_mapper
from blockchain_node import blockchain_node as bl_mapper
from sdn_mapper import sdn_mapper
from database import database as db
from config_files import settings


# mutex used to ensure one single access to DBs
mutex_slice2db_access = Lock()
mutex_slice2blockchaindb_access = Lock()

#### LOCAL NETWORK SLICES FUNCTIONS
# returns the slices templates information in the local domain.
def get_local_slicesubnet_templates():
    response = slice_mapper.get_all_slice_subnet_templates()
    return response[0], 200

# returns the slice template information placed in the local domain with a specific ID.
def get_local_slicesubnet_template(slice_ID):
    response = slice_mapper.get_slice_subnet_template(slice_ID)
    return response[0], 200

#### BLOCKCHAIN NETWORK SLICES FUNCTIONS
# adds a slice template into the blockchain to be shared
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

# returns the slice-subnet template information placed in the blockchain with a specific ID.
def get_bl_slicesubnet_template(slice_ID):
    response = bl_mapper.slice_from_blockchain(slice_ID)
    return response, 200

#### GLOBAL NETWORK SLICES FUNCTIONS
# returns all the slice-subnets (NSTs) available locally and in the blockchain peers.
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
    #available_slicesubnets = json.loads(slicesubnets_list)
    return slicesubnets_list, 200

# returns all the e2e slice instances (E2E NSI)
def get_e2e_slice_instances():
    response = db.get_elements("slices")
    return response, 200

# manages all the E2E slice instantiation process  NOTE: missing VL creation (path computation)
def instantiate_e2e_slice(e2e_slice_json):
    settings.logger.info("ORCH: Received request to deploy an E2E Network Slice.")
    # creates the NSI instance object based on the request
    incoming_data = e2e_slice_json
    nsi_element = {}
    nsi_element["id"] = str(uuid.uuid4()) #ID for the E2E slice object
    nsi_element["name"] = incoming_data["name"]

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
            settings.logger.info("ORCH: Request slice-subnte to BL NSM")
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
            settings.logger.info("ORCH: Request slice-subnte to local NSM")
            response = slice_mapper.instantiate_slice_subnet(data_json)                         # TODO: response is emulated while developing.

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
    settings.logger.info("ORCH: Waiting for al slice-subnets instantes to be deployed. E2E SLICE ID: " +str(nsi_element["id"]))
    all_subnets_ready = False
    while(all_subnets_ready == False):
        #time.sleep(30)                  # sleep of 30s (maybe a minute?) to let all the process begin
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
            elif(slice_subnet_item['status'] == 'INSTANTIATED'):
                # all slice-subnets deployed in other domains, are updated by the blockchain event thread.
                subnets_instantiated = subnets_instantiated + 1
            else:
                #TODO: ERROR management
                pass
        
        # if the number of slice-subnets instantiated = total number in the e2e slice, finishes while
        if (subnets_instantiated == len(nsi_element['slice_subnets'])):
            all_subnets_ready = True
    
    # saves the nsi object into the db
    mutex_slice2db_access.acquire()
    nsi_element["log"] = "Slice-subnets ready, deploying virtual links between slice-subnets."
    db.update_db(nsi_element["id"], nsi_element, "slices")
    mutex_slice2db_access.release()

    # VL CREATION PROCEDURE
    # TODO: (future work) improve the code with a real path computation action
    # TODO:  VL design, connectivity services composition

    nsi_element["status"] = "INSTANTIATED"
    nsi_element["log"] = "E2E Network Slice INSTANTIATED."

    # saves the nsi object into the db
    mutex_slice2db_access.acquire()
    db.update_db(nsi_element["id"], nsi_element, "slices")
    mutex_slice2db_access.release()
    settings.logger.info('E2E Network Slice INSTANTIATED. E2E Slice ID: ' + str(nsi_element["id"]))  

# manages a local slice-subnet instantiation process
def instantiate_local_slicesubnet(subnet_json):
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
        #elif (jsonresponse['status'] == "INSTANTIATING"):
            #time.sleep(30)
        else:
            # TODO: exception/error management
            pass
    
    # Once instantiation is done, updates Blockchain and local DB
    subnet_element['instance_id'] = jsonresponse['instance_uuid']
    subnet_element['status'] = jsonresponse['status']
    subnet_element['log'] = "Slice-subnet instantiated."

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
    settings.logger.info("ORCH: Deployed slice-subnet from Blocckhain request. NST Ref:: " +str(subnet_json['nst_ref']))

# updates a slice-subnet information belonging to another domain (Blockchain)
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

# manages all the E2E Slice termination process
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
