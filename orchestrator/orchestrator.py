#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
from threading import Lock

from slice_subnet_mapper import slice_subnet_mapper as slice_mapper
from blockchain_node import blockchain_node as bl_mapper
from sdn_mapper import sdn_mapper
from database import database as db


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
# adds a slice template into the blockchain to be shared            #TODO: a parameters selection to distribute must be done
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
# returns all the slice-subnets (NSTs) availablae locally and in the blockchain peers.
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
                    logging.debug ("NST already in local DB, no need to get it from BL.")
                    break
        
        if found == False:
            nst_element = bl_mapper.slice_from_blockchain(subnet_ID_item)            
            blockchain_slicesubnets_list.append(nst_element[0])
        index_list += 1
    
    slicesubnets_list = local_slicesubnets_list + blockchain_slicesubnets_list
    #available_slicesubnets = json.loads(slicesubnets_list)
    return slicesubnets_list, 200

# TODO: manages all the E2E slice instantiation process
def instantiate_e2e_slice(e2e_slice_json):
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
                subslice_element["unit"] = "ETH"
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
            jsonresponse = json.loads(response[0])

            if (response[1] == 200) or (response[1] == 201):
                slice_subnet_item['log'] = "This slice-subnet is being instantiated."
                slice_subnet_item['status'] = "INSTANTIATING"
                slice_subnet_item['request_id'] = jsonresponse['id']
    
    # saves the nsi object into the db
    mutex_slice2db_access.acquire()
    nsi_element["log"] = "E2E Slice instance designed, deploying slice-subnets."
    db.nsi_db.append(nsi_element) 
    mutex_slice2db_access.release()

    # awaits for all the slice-subnets to be instantiated
    all_subnets_ready = False
    while(all_subnets_ready == False):
        #time.sleep(30)                  # sleep of 30s (maybe a minute?) to let all the process begin
        subnets_instantiated = 0        # used to check how many subnets are in instantiated and change e2e slice status
        for slice_subnet_item in nsi_element["slice_subnets"]:
            if (slice_subnet_item['status'] == 'INSTANTIATING'):
                if ('blockchain_owner' not in slice_subnet_item):
                    response = slice_mapper.get_slice_subnet_instance_request(slice_subnet_item['request_id'])
                    jsonresponse = json.loads(response[0])
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
            #nsi_element["status"] = "INSTANTIATED"
            #nsi_element["log"] = "E2E Network Slice INSTANTIATED."
            all_subnets_ready = True
    
    # saves the nsi object into the db
    # TODO: uncomment once the path computation procedure is done
    #mutex_slice2db_access.acquire()
    #nsi_element["log"] = "Slice-subnets ready, applying path computation."
    #db.update_db(nsi_element["id"], nsi_element, "slices")
    #mutex_slice2db_access.release()

    # VL CREATION PROCEDURE
    # TODO: (future work) improve the code with a real path computation action
    # TODO:  VL design, connectivity services composition

    nsi_element["status"] = "INSTANTIATED"
    nsi_element["log"] = "E2E Network Slice INSTANTIATED."

    # saves the nsi object into the db
    mutex_slice2db_access.acquire()
    db.update_db(nsi_element["id"], nsi_element, "slices")
    mutex_slice2db_access.release()
    logging.debug('E2E Network Slice INSTANTIATED. E2E Slice ID: ' + str(nsi_element["id"]))  

# TODO: manages a local slice-subnet instantiation process
def instantiate_local_slicesubnet():
    pass

# TODO: manages all the E2E Slice termination process
def terminate_e2e_slice(e2e_slice_json):
    pass

# TODO: manages a local slice-subnet termination process
def terminate_local_slicesubnet():
    pass