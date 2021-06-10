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
from vl_computation import vl_computation
from database import database as db

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
# NOTE: GETS all E2E Network Slices Instances
@app.route('/pdl-slice', methods=['GET'])
def get_all_e2e_slice_instances():
  response = orch.get_e2e_slice_instances()
  if response[1] == 200:
    return jsonify(response[0]), 200
  else:
    return response[0], response[1] 

# NOTE: E2E Slice deployment request  # NOTE: MISSING VL CREATION (PATH COMPUTATION)
@app.route('/pdl-slice', methods=['POST'])
def deploy_e2e_slice():
  settings.executor.submit(orch.instantiate_e2e_slice, request.json)
  response = {}
  response['log'] = "Request accepted, setting up the E2E Network Slice."
  return response, 200

#TODO: GET Specific Slice Instance
#@app.route('/pdl-slice/<slice_id>', methods=['GET'])

# NOTE: instead of POST, use /pdl-slice/<netslice_id> + DELETE. If not, update swagger
# TODO: compelte the E2E Slice termination request as it misses the VL removal
# TODO #@app.route('/pdl-slice/<slice_id>', methods=['DELETE'])
@app.route('/pdl-slice/terminate', methods=['POST'])
def terminate_e2e_slice():
  settings.executor.submit(orch.terminate_e2e_slice, request.json)
  response = {}
  response['log'] = "Request accepted, terminating the selected E2E Network Slice."
  return response, 200

# NOTE: GETS all local and blockchain slice-subnets (NSTs)
@app.route('/pdl-slice/slice-subnets', methods=['GET'])
def get_all_slice_subnets_templates():
  response = orch.get_slicessubnets_templates()
  if response[1] == 200:
    return jsonify(response[0]), 200
  else:
    return response[0], response[1] 

# NOTE: adds a slice-subnet in the Blockchain system
@app.route('/pdl-slice/slice-subnets/<subnet_id>', methods=['POST'])
def add_blockchain_subnet_template(subnet_id):
  response = orch.slicesubnet_template_to_bl(subnet_id)
  if response[1] == 200:
    return response[0], 200
  else:
    return response[0], response[1]

# NOTE: GETS all local slice-subnets (NSTs)
@app.route('/pdl-slice/slice-subnets/local', methods=['GET'])
def get_local_subnet_templates():
  response = orch.get_local_slicesubnet_templates()
  if response[1] == 200:
    return jsonify(response[0]), 200
  else:
    return response[0], response[1] 

# NOTE: GETS specific local slice-subnet (NST)
@app.route('/pdl-slice/slice-subnets/local/<subnet_id>', methods=['GET'])
def get_local_subnet_template(subnet_id):
  response = orch.get_local_slicesubnet_template(subnet_id)
  if response[1] == 200:
    return jsonify(response[0]), 200
  else:
    return response[0], response[1] 


# TODO: GETS the slice-subnets (NSTs) in the Blockchain system
@app.route('/pdl-slice/slice-subnets/blockchain', methods=['GET'])
def get_blockchain_subnets_templates():
  #response = orch.get_bl_slicesubnet_templates()
  #if response[1] == 200:
    #return jsonify(response[0]), 200
  #else:
    #return response[0], response[1] 
  pass

# NOTE: GETS a shared slice-subnet (NST) in the Blockchain system
@app.route('/pdl-slice/slice-subnets/blockchain/<subnet_id>', methods=['GET'])
def get_blockchain_subnet_template(subnet_id):
  response = orch.get_bl_slicesubnet_template(subnet_id)
  if response[1] == 200:
    return jsonify(response[0]), 200
  else:
    return response[0], response[1] 


######################################### PDL-TRANSPORT API #########################################
# GETS the local context
@app.route('/pdl-transport', methods=['GET'])
def get_context():
  response = db.get_element("", "context")
  return response, 200

"""
Example of the json to pass:
  {
    "e2e-topology": {
      "nodes-list": [
        //it contains the uuids of those nodes with an inter-domain link
        // for VNODE is the ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["uuid"]
        // for VLINK is the ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"]["uuid"]
        // for TRANSPARENT is the ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"]["uuid"]
        "uuid_A",
        "uuid_B",
        "uuid_C"
      ],
      "interdomain-links": [
        {
          "name": "uuid_A-uuid_B",
          // key values to identify the link are the two nodes in nodes-involved
          "nodes-involved": [
            "uuid_A",
            "uuid_B,
          ],
          "link-options": [
            //there will be only two unidirectional options, each with the different physical links for the trick.
            {
              "uuid": "uuid",
              "direction": "UNIDIRECTIONAL",
              "nodes-direction": {
                "node-1": "uuid_A",
                "node-2": "uuid_B"
              },
              "layer-protocol-name": [
                "PHOTONIC_MEDIA"
              ],
              "physical-options": [
                {
                  "node-edge-point":[
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_A",
                      // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                      // this NEP is one of those with SIPs in the domain
                      "nep-uuid": "nep_C1"
                    },
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_B",
                      "nep-uuid": "nep_D1"
                    }
                  ] ,
                  "occupied-spectrum": [
                  ]
                },
                {
                  "node-edge-point":[
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_A",
                      // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                      // this NEP is one of those with SIPs in the domain
                      "nep_uuid": "nep_C2"
                    },
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_B",
                      "nep-uuid": "nep_D2"
                    }
                  ] ,
                  "occupied-spectrum": [
                  ]
                }
              ]
            },
            {
              "uuid": "uuid",
              "direction": "UNIDIRECTIONAL",
              "layer-protocol-name": [
                "PHOTONIC_MEDIA"
              ],
              "nodes-direction": {
                "node-1": "uuid_B",
                "node-2": "uuid_A"
              },
              "physical-options": [
                {
                  "node-edge-point":[
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_B",
                      // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                      // this NEP is one of those with SIPs in the domain
                      "nep_uuid": "nep_D1"
                    },
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_A",
                      "nep-uuid": "nep_C1"
                    }
                  ] ,
                  "occupied-spectrum": [
                  ]
                },
                {
                  "node-edge-point":[
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_B",
                      // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                      // this NEP is one of those with SIPs in the domain
                      "nep_uuid": "nep_D2"
                    },
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_A",
                      "nep-uuid": "nep_C2"
                    }
                  ] ,
                  "occupied-spectrum": [
                  ]
                }
              ]
            }
          ],
          "supportable_spectrum": [
            {
              "lower-frequency": 191700000,
              "upper-frequency": 196100000,
              "frequency-constraint": {
                "adjustment-granularity": "G_50GHZ",
                "grid-type": "DWDM"
              }
            }
          ],
          "available_spectrum": [
            {
              "lower-frequency": 191700000,
              "upper-frequency": 196100000,
              "frequency-constraint": {
                "adjustment-granularity": "G_50GHZ",
                "grid-type": "DWDM"
              }
            }
          ]
        },
        {
          "name": "uuid_A-uuid_B",
          // key values to identify the link are node-1 and node-2 (always as pair)
          "node-1": "uuid_A",
          "node-2": "uuid_B",
          "link_options": [
            //there will be only two unidirectional options, each with the different physical links for the trick.
            {
              "uuid": "uuid",
              "direction": "UNIDIRECTIONAL",
              "layer-protocol-name": [
                "PHOTONIC_MEDIA"
              ],
              "physical-options": [
                {
                  "node-edge-point":[
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_A",
                      // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                      // this NEP is one of those with SIPs in the domain
                      "nep_uuid": "nep_C1"
                    },
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_B",
                      "nep-uuid": "nep_D1"
                    }
                  ] ,
                  "occupied-spectrum": [
                  ]
                },
                {
                  "node-edge-point":[
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_A",
                      // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                      // this NEP is one of those with SIPs in the domain
                      "nep_uuid": "nep_C1"
                    },
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_B",
                      "nep-uuid": "nep_D1"
                    }
                  ] ,
                  "occupied-spectrum": [
                  ]
                }
              ]
            },
            {
              "uuid": "uuid",
              "direction": "UNIDIRECTIONAL",
              "layer-protocol-name": [
                "PHOTONIC_MEDIA"
              ],
              "physical-options": [
                {
                  "node-edge-point":[
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_A",
                      // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                      // this NEP is one of those with SIPs in the domain
                      "nep_uuid": "nep_C1"
                    },
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_B",
                      "nep-uuid": "nep_D1"
                    }
                  ] ,
                  "occupied-spectrum": [
                  ]
                },
                {
                  "node-edge-point":[
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_A",
                      // same uuid than the one in ["tapi-common:context"]["tapi-topology:topology-context"]["topology"]["node"][“owned-node-edge-point"][“uuid”]
                      // this NEP is one of those with SIPs in the domain
                      "nep_uuid": "nep_C1"
                    },
                    {
                      "topology-uuid": "uuid",
                      "node-uuid": "uuid_B",
                      "nep-uuid": "nep_D1"
                    }
                  ] ,
                  "occupied-spectrum": [
                  ]
                }
              ]
            }
          ],
          "supportable_spectrum": [
            {
              "lower-frequency": 191700000,
              "upper-frequency": 196100000,
              "frequency-constraint": {
                "adjustment-granularity": "G_50GHZ",
                "grid-type": "DWDM"
              }
            }
          ],
          "available_spectrum": [
            {
              "lower-frequency": 191700000,
              "upper-frequency": 196100000,
              "frequency-constraint": {
                "adjustment-granularity": "G_50GHZ",
                "grid-type": "DWDM"
              }
            }
          ]
        }
      ]
    }
  }
"""
# distributes the domain context in the Blockchain
@app.route('/pdl-transport', methods=['POST'])
def distribute_context_blockchain():
  # with this command we share the local context and the local view of the e2e topology (request.json)
  response = orch.context_to_bl(request.json)
  if response[1] == 200:
    return response[0], 200
  else:
    return response[0], response[1]

#  GET all the contexts (local and blockchain)
@app.route('/pdl-transport/all_contexts', methods=['GET'])
def get_all_contexts():
  response = orch.get_all_contexts()
  if response[1] == 200:
    return jsonify(response[0]), 200
  else:
    return response[0], response[1]

"""
Example E2E_CS request 
  {
      "domain-source": {
          "uuid": "SDN_domain_uuid",
          "sip": "sip_uuid",
      },
      "domain-destination": {
          "uuid": "SDN_domain_uuid",
          "sip": "sip_destination_uuid",
      },
          "capacity": {
          "value": 150,
          "unit": "GHz"
      }
  }
"""
# requests a CS based on a set of two SIPs and a capacity
@app.route('/pdl-transport/connectivity_service', method=['POST'])
def request_e2e_cs():
  settings.executor.submit(orch.instantiate_e2e_connectivity_service(request.json), request.json)
  response = {}
  response['log'] = "Request accepted, creating the E2E CS."
  return response, 200

#####################################################################################################
#######################               MAIN SERVER FUNCTION                    #######################
#####################################################################################################
if __name__ == '__main__':
  # initializes the environment variables for this application.
  settings.logger.info('Configuring environment variables')
  settings.init_environment_variables()

  # triggers the blockchain configuration
  settings.logger.info('Configuring Blockchain connection')
  settings.init_blockchain()

  # triggers local context abstraction based on the model configured
  settings.logger.info("Abstraction process of the SDN local context.")
  sdn_ctrl_ip = os.environ.get("SDN_CONTROLLER_IP")
  sdn_ctrl_port = os.environ.get("SDN_CONTROLLER_PORT")
  abstraction_model = os.environ.get("ABSTRACION_MODEL")
  settings.init_abstract_context(sdn_ctrl_ip, sdn_ctrl_port, abstraction_model)
  
  # triggers the initial E2E graph only with its own existence (not even the inter-domain-links)
  # NOTE: at this point, nothing is distributed in the BL
  settings.logger.info("Internal E2E graph initalization for path computation.")
  settings.init_e2e_topology()

  # BLOCKCHAIN EVENT LISTENERS (Threads)
  settings.logger.info('Configuring permanent threads to manage Blockchain events (slicing and transport)')
  # event thread for slicing actions
  slicing_event_filter = settings.slice_contract.events.notifySliceInstanceActions.createFilter(fromBlock='latest')
  worker_slicing_blockchain_events = Thread(target=events_manager.slice_event_loop, args=(slicing_event_filter, 1), daemon=True)
  worker_slicing_blockchain_events.start()
  #event thread for transport actions
  transport_event_filter = settings.transport_contract.events.notifyTopologyActions.createFilter(fromBlock='latest')
  worker_transport_blockchain_events = Thread(target=events_manager.transport_event_loop, args=(transport_event_filter, 1), daemon=True)
  worker_transport_blockchain_events.start()

  # RUN THREAD POOL TO MANAGE INCOMING TASKS
  settings.logger.info('Thread pool created with 5 workers')
  workers = 5
  settings.init_thread_pool(workers)

  # RUN MAIN SERVER THREAD
  app.run(debug=False, host='localhost', port=os.environ.get("PDL_PORT"))
