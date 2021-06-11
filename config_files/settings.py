#!/usr/local/bin/python3.4
 
import os, sys, logging, json, argparse, time, datetime, requests, uuid
from concurrent.futures import ThreadPoolExecutor
from web3 import Web3
from sdn_mapper import sdn_mapper
from vl_computation import vl_computation
from database import database as db

def init_logging():
    global logger
    
    # Create a custom logger
    logger = logging.getLogger('PDL-Slicing/Transport')
    logger.setLevel(logging.INFO)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('log_file.log')
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

def init_environment_variables():
    with open('config_files/config_env.env') as f:
        for line in f:
            if 'export' not in line:
                continue
            if line.startswith('#'):
                continue
            # Remove leading `export `
            # then, split name / value pair
            key, value = line.replace('export ', '', 1).strip().split('=', 1)
            os.environ[key] = value

def init_blockchain():
    global slice_contract
    global transport_contract
    global web3

    # ETHEREUM (GANACHE) CHAIN CONNECTION
    bl_ip = os.environ.get("BLOCKCHAIN_IP")
    bl_port = os.environ.get("BLOCKCHAIN_PORT")
    ethereum_url = "http://" + str(bl_ip) + ":" + str(bl_port)
    print("Ethereum URL: " + ethereum_url)
    # web3.py instance
    web3 = Web3(Web3.HTTPProvider(ethereum_url))
    
    # checks connection and gets currentblockcnumber
    print("Connection with te blockchain ready: " + str(web3.isConnected()))
    print("Current Ethereum block number:" + str(web3.eth.blockNumber))

    # ETHEREUM SMART CONTRACT ASSOCIATION
    # uses ABI and contract_address within config_file
    with open('config_files/slice_blockchain.json', 'r') as slice_config_file:
        datastore = json.load(slice_config_file)
        slice_abi = datastore["abi"]
        slice_contract_address = datastore["contract_address"]
    
    with open('config_files/transport_blockchain.json', 'r') as transport_config_file:
        datastore = json.load(transport_config_file)
        transport_abi = datastore["abi"]
        transport_contract_address = datastore["contract_address"]

    # ETHEREUM NODE CONFIGURATION
    # defines peer account ID and selects smart contract to attack
    web3.eth.defaultAccount = web3.eth.accounts[int(os.environ.get("BL_ID"))]
    slice_contract = web3.eth.contract(address=slice_contract_address, abi=slice_abi)
    transport_contract = web3.eth.contract(address=transport_contract_address, abi=transport_abi)

def init_thread_pool(workers):
    global executor
    executor = ThreadPoolExecutor(max_workers=workers)

def init_abstract_context(sdn_ctrl_ip, sdn_ctrl_port, model):
    response = sdn_mapper.get_local_context(sdn_ctrl_ip, sdn_ctrl_port)
    print(model)
    if (model == "vnode"):
        abstracted_context = vl_computation.vnode_abstraction(response[0])
    elif (model == "vlink"):
        abstracted_context = vl_computation.vlink_abstraction(response[0])
    elif (model == "transparent"):
        abstracted_context = response[0]
    else:
        print("Wrong abstraction model selected. Validate [ABSTRACION_MODEL] in the configuration file to be one of these: vnode, vlink, transparent.")
        abstracted_context = {"msg": "Wrong abstraction model selected. It is not programmed."}
        pass
    response = db.add_element(abstracted_context, "context")

def init_e2e_topology():
    response = db.get_elements("context")
    vl_computation.add_context_e2e_graph(response)