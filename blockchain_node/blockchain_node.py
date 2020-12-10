#!/usr/local/bin/python3.4
 
import os, sys, logging, json, argparse, time, datetime, requests, uuid
from web3 import Web3

from config_files import settings

logging.basicConfig(level=logging.DEBUG)

###################################### BLOCKCHAIN MAPPER #######################################
# adds slice-subnet template information into the blockchain
def slice_to_blockchain(nst_json):
    print("Before distributing...")
    # Add a slice template to make it available for other domains
    tx_hash = settings.contract.functions.addSliceTemplate(str(nst_json["id"]), nst_json["name"], nst_json["version"], nst_json["vendor"], nst_json["price"], nst_json["unit"]).transact()
    print("After distributing...")
    # Wait for transaction to be mined and check it's in the blockchain (get)
    settings.web3.eth.waitForTransactionReceipt(tx_hash)
    response = settings.contract.functions.getSliceTemplate(str(nst_json["id"])).call()
    nst_json['blockchain_owner'] = response[5]
    print("Sending response: " + str(nst_json))
    return nst_json, 200

#TODO: return all slice-subnets template information from other domains
def slices_from_blockchain():
    pass 

# returns a specific slice-subnet template information from another domain
def slice_from_blockchain(slice_ID):
    response = settings.contract.functions.getSliceTemplate(slice_ID).call()
    nst_json['blockchain_owner'] = response[5]
    print("Sending response: " + str(nst_json))
    return nst_json, 200

#TODO: requests the deployment of a slice-subnet from another domain
def deploy_blockchain_slice():
    pass
###################################### BLOCKCHAIN EVENTS MANAGER #######################################

#TODO: create a class able to listen the events coming from the Bockchain and 
# request the correct action to the rchestrator