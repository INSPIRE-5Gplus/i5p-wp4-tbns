#!/usr/local/bin/python3.4


import os, sys, logging, json, argparse, time, datetime, requests, uuid
from flask import Flask, request, jsonify
from configparser import ConfigParser
from concurrent.futures import ThreadPoolExecutor
from web3 import Web3

from config_files import settings
from orchestrator import orchestrator as orch
from blockchain_node import blockchain_node as bl_node
from database import database as db

# Define inner applications
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

########################################## API ##########################################
# PING function to validate if the slice-docker is active
@app.route('/pdl/pings', methods=['GET'])
def getPings():
  ping_response  = {'code creation date': '2020-04-12 11:00:00 UTC', 'current_time': str(datetime.datetime.now().isoformat())}
  return jsonify(ping_response), 200

# GETS all local slice-subnets
@app.route('/pdl/slice/get_local', methods=['GET'])
def get_all_local_slice():
  response = orch.get_all_local_slice()
  if response[1] == 200:
    return jsonify(response[0]), 200
  else:
    return response[0], response[1] 

# GETS specific local slice-subnet
@app.route('/pdl/slice/get_local/<slice_ID>', methods=['GET'])
def get_local_slice(slice_ID):
  response = orch.get_local_slice(slice_ID)
  if response[1] == 200:
    return jsonify(response[0]), 200
  else:
    return response[0], response[1] 

# TODO: add a slice-subnet in the Blockchain system
@app.route('/pdl/slice/share_in_blockchain/<slice_ID>', methods=['POST'])
def add_blockchain_slice(slice_ID):
  response = orch.share_slice(slice_ID)
  if response[1] == 200:
    return response[0], 200
  else:
    return response[0], response[1]

# TODO. GETS the shared slice-subnet in the Blockchain system
@app.route('/pdl/slice/get_blockchain', methods=['GET'])
def get_blockchain_slices():
  response = orch.get_all_blockchain_slices()
  return jsonify(response), 200

# TODO: GETS the shared slice-subnet in the Blockchain system
@app.route('/pdl/slice/get_blockchain/<slice_ID>', methods=['GET'])
def get_blockchain_slice(slice_ID):
  response = orch.get_blockchain_slice(slice_ID)
  return jsonify(response), 200

# TODO: E2E Slice deployment request
@app.route('/pdl/deploy_slice', methods=['POST'])
def deploy_e2e_slice():
  pass
  #executor.submit(orch.share_slice, request.json)
  return 200

# TODO:E2E Slice termination request
@app.route('/pdl/terminate_slice', methods=['POST'])
def terminate_e2e_slice():
  pass
  #executor.submit(orch.share_slice, request.json)
  return 200

################################## MAIN SERVER FUNCTION #################################
if __name__ == '__main__':
  # initializes the environtment variables for this application.
  logging.debug('Configuring environtment variables')
  settings.init_environment_variables()

  # triggers the blockchain configuration
  logging.debug('Configuring Blockchain connection')
  settings.init_blockchain()

  # RUN THREAD POOL TO MANAGE INCOMING TASKS
  logging.debug('Thread pool created with 5 workers')
  executor = ThreadPoolExecutor(max_workers=5)

  # BLOCKCHAIN EVENT LISTENER (Thread)
  #TODO: define the thread that must listen for Blockchain events (/blockchain_node/events_manager.py)
  #TODO: once defined, declare and start it

  # RUN MAIN SERVER THREAD
  app.run(debug=False, host='localhost', port=os.environ.get("PDL_SLICE_PORT"))
