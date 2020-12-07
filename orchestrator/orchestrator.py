#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

from slice_subnet_mapper import slice_subnet_mapper as slice_mapper
from sdn_mapper import sdn_mapper
from database import database as db


#### LOCAL NETWORK SLICES FUNCTIONS
def get_all_local_slice():
    response = slice_mapper.get_all_slice_templates()
    print(str(response[0]))
    return response[0], 200

def get_local_slice(slice_ID):
    response = slice_mapper.get_slice_template(slice_ID)
    return response, 200

#### BLOCKCHAIN NETWORK SLICES FUNCTIONS
def share_slice(slice_json):
    db.nsi_db.append(slice_json)
    return 200

def get_all_shared_slice():
    return 200

#### GLOBAL NETWORK SLICES FUNCTIONS
def instantiate_e2e_slice(e2e_slice_json):
    
    return 200

def terminate_e2e_slice(e2e_slice_json):

    return 200