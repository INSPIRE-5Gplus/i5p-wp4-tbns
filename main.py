#!/usr/local/bin/python3.4


import os, sys, logging, json, argparse, time, datetime, requests, uuid
from flask import Flask, request, jsonify
from configparser import ConfigParser
from concurrent.futures import ThreadPoolExecutor
from web3 import Web3

from orchestrator import orchestrator as orch
from database import database as db

# Define inner applications
LOG = logging.getLogger(__name__)
app = Flask(__name__)

################################ ENVIRONMENT CONFIGURATION ##############################
with open('config_env.env') as f:
  for line in f:
      if 'export' not in line:
          continue
      if line.startswith('#'):
          continue
      # Remove leading `export `
      # then, split name / value pair
      key, value = line.replace('export ', '', 1).strip().split('=', 1)
      os.environ[key] = value

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
  return jsonify(response[0]), 200

# GETS specific local slice-subnet
@app.route('/pdl/slice/get_local/<slice_ID>', methods=['GET'])
def get_local_slice(slice_ID):
  response = orch.get_local_slice(slice_ID)
  return jsonify(response), 200

# add a slice-subnet in the Blockchain system
@app.route('/pdl/slice/share_in_blockchain', methods=['POST'])
def add_blockchain_slice():
  response = orch.share_slice(request.json)
  return response, 200

# GETS the shared slice-subnet in the Blockchain system
@app.route('/pdl/slice/get_blockchain', methods=['GET'])
def get_blockchain_slices():
  response = orch.get_all_blockchain_slices()
  return jsonify(response), 200

# GETS the shared slice-subnet in the Blockchain system
@app.route('/pdl/slice/get_blockchain/<slice_ID>', methods=['GET'])
def get_blockchain_slice(slice_ID):
  response = orch.get_blockchain_slice(slice_ID)
  return jsonify(response), 200

# E2E Slice deployment request
@app.route('/pdl/deploy_slice', methods=['POST'])
def deploy_e2e_slice():
  pass
  #executor.submit(orch.share_slice, request.json)
  return 200

# E2E Slice termination request
@app.route('/pdl/terminate_slice', methods=['POST'])
def terminate_e2e_slice():
  pass
  #executor.submit(orch.share_slice, request.json)
  return 200

################################## MAIN SERVER FUNCTION #################################
if __name__ == '__main__':
  # RUN THREAD POOL TO MANAGE INCOMING TASKS
  print('Thread pool created with 5 workers')
  executor = ThreadPoolExecutor(max_workers=5)

  # BLOCKCHAIN EVENT LISTENER (Thread)
  #TODO: define the thread that must listen for Blockchain events (/blockchain_node/events_manager.py)
  #TODO: once defined, declare and start it

  # RUN MAIN SERVER THREAD
  app.run(debug=False, host='localhost', port=os.environ.get("PDL_SLICE_PORT"))
