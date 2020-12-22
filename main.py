#!/usr/local/bin/python3.4


import os, sys, logging, json, argparse, time, datetime, requests, uuid
from flask import Flask, request, jsonify
from configparser import ConfigParser
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Lock
from web3 import Web3

from config_files import settings
from orchestrator import orchestrator as orch
from blockchain_node import blockchain_node as bl_node
from blockchain_node import events_manager

# Define inner applications
#logging.basicConfig(level=logging.DEBUG)  #Trying setting.logger
app = Flask(__name__)

# initializes the logging
settings.init_logging()

#####################################################################################################
#####################                        API                          ###########################
#####################################################################################################
# PING function to validate if the slice-docker is active
@app.route('/pdl/pings', methods=['GET'])
def getPings():
  ping_response  = {'code creation date': '2020-04-12 11:00:00 UTC', 'current_time': str(datetime.datetime.now().isoformat())}
  return jsonify(ping_response), 200

########################################## PDL-SLICING API ##########################################
# GETS all local slice-subnets (NSTs)
@app.route('/pdl/slice/get_local_template', methods=['GET'])
def get_local_subnet_templates():
  response = orch.get_local_slicesubnet_templates()
  if response[1] == 200:
    return jsonify(response[0]), 200
  else:
    return response[0], response[1] 

# GETS specific local slice-subnet (NST)
@app.route('/pdl/slice/get_local_template/<slice_ID>', methods=['GET'])
def get_local_subnet_template(slice_ID):
  response = orch.get_local_slicesubnet_template(slice_ID)
  if response[1] == 200:
    return jsonify(response[0]), 200
  else:
    return response[0], response[1] 

# adds a slice-subnet in the Blockchain system
@app.route('/pdl/slice/share_in_blockchain/<slice_ID>', methods=['POST'])
def add_blockchain_subnet_template(slice_ID):
  response = orch.slicesubnet_template_to_bl(slice_ID)
  if response[1] == 200:
    return response[0], 200
  else:
    return response[0], response[1]

# TODO. GETS the slice-subnets (NSTs) in the Blockchain system
@app.route('/pdl/slice/get_blockchain_template', methods=['GET'])
def get_blockchain_subnets_templates():
  response = orch.get_bl_slicesubnet_templates()
  if response[1] == 200:
    return jsonify(response[0]), 200
  else:
    return response[0], response[1] 

# GETS a shared slice-subnet (NST) in the Blockchain system
@app.route('/pdl/slice/get_blockchain_template/<slice_ID>', methods=['GET'])
def get_blockchain_subnet_template(slice_ID):
  response = orch.get_bl_slicesubnet_template(slice_ID)
  if response[1] == 200:
    return jsonify(response[0]), 200
  else:
    return response[0], response[1] 

# GETS all local and blockchain slice-subnets (NSTs)
@app.route('/pdl/slice/get_all_templates', methods=['GET'])
def get_all_slice_subnets_templates():
  response = orch.get_slicessubnets_templates()
  if response[1] == 200:
    return jsonify(response[0]), 200
  else:
    return response[0], response[1] 

# GETS all E2E Network Slices Instances
@app.route('/pdl/slice/get_all_instances', methods=['GET'])
def get_all_e2e_slice_instances():
  response = orch.get_e2e_slice_instances()
  if response[1] == 200:
    return jsonify(response[0]), 200
  else:
    return response[0], response[1] 

# TODO: E2E Slice deployment request
@app.route('/pdl/slice/deploy', methods=['POST'])
def deploy_e2e_slice():
  settings.executor.submit(orch.instantiate_e2e_slice, request.json)
  response = {}
  response['log'] = "Request accepted, setting up the E2E Network Slice."
  return response, 200

# TODO:E2E Slice termination request
@app.route('/pdl/slice/terminate', methods=['POST'])
def terminate_e2e_slice():
  pass
  #settings.executor.submit(orch.terminate_e2e_slice, request.json)
  response = {}
  response['log'] = "Request accepted, terminating the selected E2E Network Slice."
  return response, 200

######################################### PDL-TRANSPORT API #########################################
# TODO: API FOR THE PDL-TRANSPORT NODES

#####################################################################################################
#######################               MAIN SERVER FUNCTION                    #######################
#####################################################################################################
if __name__ == '__main__':
  # initializes the environment variables for this application.
  settings.logger.info('Configuring environtment variables')
  settings.init_environment_variables()

  # triggers the blockchain configuration
  settings.logger.info('Configuring Blockchain connection')
  settings.init_blockchain()

  # BLOCKCHAIN EVENT LISTENER (Thread)
  event_filter = settings.contract.events.notifySliceInstanceActions.createFilter(fromBlock='latest')
  worker_blockchain_events = Thread(target=events_manager.event_loop, args=(event_filter, 10), daemon=True)

  # RUN THREAD POOL TO MANAGE INCOMING TASKS
  #settings.logger.info('Thread pool created with 5 workers')
  workers = 5
  settings.init_thread_pool(workers)

  # RUN MAIN SERVER THREAD
  app.run(debug=False, host='localhost', port=os.environ.get("PDL_SLICE_PORT"))
