#!/usr/local/bin/python3.4
 
import os, sys, logging, json, argparse, time, datetime, requests, uuid
from web3 import Web3

###################################### BLOCKCHAIN CONFIGURATION #######################################
# ETHEREUM (GANACHE) CHAIN CONNECTION
# web3.py instance
bl_ip = os.environ.get("BLOCKCHAIN_IP")
bl_port = os.environ.get("BLOCKCHAIN_PORT")
ethereum_url = "http://" + str(bl_ip) + ":" + str(bl_port)
web3 = Web3(Web3.HTTPProvider(ethereum_url))

# ETHEREUM SMART CONTRACT ASSOCIATION
# uses ABI and contract_address within config_file
with open('config_blockchain.json', 'r') as config_file:
    datastore = json.load(config_file)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]

# checks connection and gets currentblockcnumber
print("Connection with te blockchain ready: " + str(web3.isConnected()))
print("Current Ethereum block number:" + str(web3.eth.blockNumber))

# ETHEREUM NODE CONFIGURATION
# defines peer account ID and selects smart contract to attack
web3.eth.defaultAccount = web3.eth.accounts[0]
contract = web3.eth.contract(address=contract_address, abi=abi)

###################################### BLOCKCHAIN MAPPER #######################################
def slice_to_blockchain(nst_json):
    # Add a slice template to make it available for other domains
    tx_hash = contract.functions.addSliceTemplate(str(nst_json["id"]), nst_json["name"], nst_json["version"], nst_json["vendor"], nst_json["price"], nst_json["unit"]).transact()

    # Wait for transaction to be mined and check it's in the blockchain (get)
    web3.eth.waitForTransactionReceipt(tx_hash)
    response = contract.functions.getSliceTemplate(str(nst_json["id"])).call()

    return response

###################################### BLOCKCHAIN EVENTS MANAGER #######################################

#TODO: create a class able to listen the events coming from the Bockchain and 
# request the correct action to the rchestrator