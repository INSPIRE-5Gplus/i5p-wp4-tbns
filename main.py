#!/usr/local/bin/python3.4


import os, sys, logging, json, argparse, time, datetime, requests, uuid
from flask import Flask, request, jsonify
from configparser import ConfigParser
from concurrent.futures import ThreadPoolExecutor

from orchestrator import orchestrator as orch
from database import database as db

# Define inner applications
LOG = logging.getLogger(__name__)
app = Flask(__name__)

########################################## API ##########################################
# PING function to validate if the slice-docker is active
@app.route('/pings', methods=['GET'])
def getPings():
  ping_response  = {'code creation date': '2020-04-12 11:00:00 UTC', 'current_time': str(datetime.datetime.now().isoformat())}
  return jsonify(ping_response), 200

# GETS all local slice-subnets
@app.route('/pdl_slicing/get_local_slice', methods=['GET'])
def get_all_local_slice():
  response = orch.get_all_local_slice()
  print(str(response[0]))
  return jsonify(response[0]), 200

# GETS specific local slice-subnet
@app.route('/pdl_slicing/get_local_slice/<slice_ID>', methods=['GET'])
def get_local_slice(slice_ID):
  local_slice = orch.get_local_slice(slice_ID)
  return jsonify(local_slice), 200

# share a slice-subnet with the Blockchain peers
@app.route('/pdl_slicing/share_slice', methods=['POST'])
def add_slice():
  #resp = orch.share_slice (request.json)
  executor.submit(orch.share_slice, request.json)
  return {"message":"Processing your request"}, 200

# GETS the shared slice-subnet in the Blockchain system
@app.route('/pdl_slicing/share_slice', methods=['GET'])
def get_shared_slices():
  shared_slices_list = orch.get_all_shared_slice()
  return jsonify(shared_slices_list), 200

########################################## MAIN SERVER FUNCTION ##########################################
if __name__ == '__main__':
  # READ CONFIG to set environment variables
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

  # RUN THREAD POOL TO MANAGE INCOMING TASKS
  print('Thread pool created with 5 workers')
  executor = ThreadPoolExecutor(max_workers=5)

  # RUN MAIN SERVER THREAD
  app.run(debug=False, host='localhost', port=os.environ.get("PDL_SLICE_PORT"))
