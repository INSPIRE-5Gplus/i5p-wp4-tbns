#!/usr/local/bin/python3.4
 
import os, sys, logging, json, argparse, time, datetime, requests, uuid
from web3 import Web3

from config_files import settings

###################################### BLOCKCHAIN MAPPER #######################################
# adds slice-subnet (NST) information into the blockchain
def slice_to_blockchain(nst_json):
    settings.logger.info('BLOCKCHAIN_MAPPER: Distributes local slice-subnet template information with Blockchain peers.')
    # Add a slice template to make it available for other domains
    tx_hash = settings.contract.functions.addSliceTemplate(str(nst_json["id"]), nst_json["name"], nst_json["version"], nst_json["vendor"], nst_json["price"], nst_json["unit"]).transact()
    # Wait for transaction to be mined and check it's in the blockchain (get)
    settings.web3.eth.waitForTransactionReceipt(tx_hash)
    response = settings.contract.functions.getSliceTemplate(str(nst_json["id"])).call()
    nst_json['blockchain_owner'] = response[5]
    return nst_json, 200

#TODO: returns all slice-subnets (NSTs) information from other domains
def slices_from_blockchain():
    settings.logger.info('BLOCKCHAIN_MAPPER: Requests all blockahin slice-subnet template information.')
    pass 

# returns a specific slice-subnet (NST) information from another domain
def slice_from_blockchain(slice_ID):
    # TODO: IMPROVE this function when solidity will allow to return an array of strings (or multidimensional elements like json).
    settings.logger.info('BLOCKCHAIN_MAPPER: Requests blockahin slice-subnet template information. ID: ' + str(slice_ID))
    response = settings.contract.functions.getSliceTemplate(slice_ID).call()
    nst_json = {}
    nst_json['id'] = slice_ID
    nst_json['name'] = response[0]
    nst_json['version'] = response[1]
    nst_json['vendor'] = response[2]
    nst_json['price'] = response[3]
    nst_json['unit'] = response[4]
    nst_json['blockchain_owner'] = response[5]
    return nst_json, 200

# returns the number of slice-subnets (NSTs) in the blockchain db
def get_slices_counter():
    response = settings.contract.functions.getSliceTemplateCount().call()
    return response

# returns the slice-subnet (NST) ID based on the index position within the slice_subnets list in the blockchain
def get_slice_id(index):
    response = settings.contract.functions.getSliceTemplateId(index).call()
    return response

# requests the deployment of a slice-subnet (NST) from another domain
def deploy_blockchain_slice(ref_slice_subnet):
    settings.logger.info('BLOCKCHAIN_MAPPER: Distributes request to deploy slice-subnet in the Blockchain: ' + str(ref_slice_subnet))
    # instantiate slice
    tx_hash = settings.contract.functions.instantiateSlice(str(ref_slice_subnet["id"]), ref_slice_subnet["nst_ref"]).transact()
    
    # Wait for transaction to be mined and check it's in the blockchain (get)
    tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
    
    #listen the event associated to the transaction receipt
    rich_logs = settings.contract.events.slice_response().processReceipt(tx_receipt)
    
    #create json to send back to the user the initial instantiation request info.
    deployment_response = {}
    deployment_response["log"] = rich_logs[0]['args']['log']
    deployment_response["status"] = rich_logs[0]['args']['status']
    
    return deployment_response, 200

# requests to update a slice-subnet element in the Blockchain
def update_blockchain_slice(subnet_json):
    settings.logger.info('BLOCKCHAIN_MAPPER: Updates slice-subnet element within the Blockchain. Element ID: ' + str(subnet_json))
    # Add a service
    tx_hash = settings.contract.functions.updateInstance(subnet_json['id'], subnet_json['status'], subnet_json['log']).transact()

    # Wait for transaction to be mined and check it's in the blockchain (get)
    tx_receipt = settings.web3.eth.waitForTransactionReceipt(tx_hash)
    
    #listen the event associated to the transaction receipt
    rich_logs = settings.contract.events.slice_response().processReceipt(tx_receipt)

    deployment_response = {}
    deployment_response["log"] = rich_logs[0]['args']['log']
    deployment_response["status"] = rich_logs[0]['args']['status']
    
    return deployment_response, 200
###################################### BLOCKCHAIN EVENTS MANAGER #######################################

#TODO: create a class able to listen the events coming from the Bockchain and 
# request the correct action to the rchestrator