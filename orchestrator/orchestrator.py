#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

from slice_subnet_mapper import slice_subnet_mapper as slice_mapper
from blockchain_node import blockchain_node as bl_mapper
from sdn_mapper import sdn_mapper
from database import database as db


#### LOCAL NETWORK SLICES FUNCTIONS
# returns the slices templates information in the local domain.
def get_all_local_slice():
    response = slice_mapper.get_all_slice_templates()
    print(str(response[0]))
    return response[0], 200

# returns the slice template information placed in the local domain with a specific ID.
def get_local_slice(slice_ID):
    response = slice_mapper.get_slice_template(slice_ID)
    return response, 200

#### BLOCKCHAIN NETWORK SLICES FUNCTIONS
# TODO: adds a slice template into the blockchain to be shared
def share_slice(request_json):
    # gets NST from local NSM
    response = slice_mapper.get_slice_template(slice_ID)
    
    #give the nst to the Blockchain mapper to distribute it with the other peers.
    response = bl_mapper.slice_to_blockchain(nst_json)
    return 200

# TODO: returns the slices templates information in the blockchain without those belonging to the local domain.
def get_all_blockchain_slices():
    return 200

# TODO: returns the slice template information placed in the blockchain with a specific ID.
def get_blockchain_slice(slice_ID):
    return 200


#### GLOBAL NETWORK SLICES FUNCTIONS
# TODO: manages all the E2E slice instantiation process
def instantiate_e2e_slice(e2e_slice_json):

    return 200

# TODO: manages all the E2E Slice termination process
def terminate_e2e_slice(e2e_slice_json):

    return 200