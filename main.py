#!/usr/local/bin/python3.4
"""
## Copyright (c) 2015 SONATA-NFV, 2017 5GTANGO, 2020 INSPIRE5G-plus [, ANY ADDITIONAL AFFILIATION]
## ALL RIGHTS RESERVED.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## Neither the name of the SONATA-NFV, 5GTANGO, 2020 INSPIRE5G-plus [, ANY ADDITIONAL AFFILIATION]
## nor the names of its contributors may be used to endorse or promote
## products derived from this software without specific prior written
## permission.
##
## This work has been performed in the framework of the SONATA project,
## funded by the European Commission under Grant number 671517 through
## the Horizon 2020 and 5G-PPP programmes. The authors would like to
## acknowledge the contributions of their colleagues of the SONATA
## partner consortium (www.sonata-nfv.eu).
##
## This work has been performed in the framework of the 5GTANGO project,
## funded by the European Commission under Grant number 761493 through
## the Horizon 2020 and 5G-PPP programmes. The authors would like to
## acknowledge the contributions of their colleagues of the 5GTANGO
## partner consortium (www.5gtango.eu).
##
## This work has been performed in the framework of the INSPIRE5G-plus
##  project, funded by the European Commission under Grant number 871808
## through the Horizon 2020 and 5G-PPP programmes. The authors would like
## to acknowledge the contributions of their colleagues of the INSPIRE5G-plus
## partner consortium (https://www.inspire-5gplus.eu/).
"""

from flask import Flask, request, jsonify
import os, sys, logging, json, argparse, time, datetime, requests, uuid
from configparser import ConfigParser

from slice_mgmt import nst_management as nst_mgmt
from slice_mgmt import nsi_management as nsi_mgmt
from slice_subnet_mgmt import slice_mapper
from database import database as db

# TODO: improve logging
LOG = logging.getLogger(__name__)

app = Flask(__name__)

######################################### SONATA NFVO CONFIGURATION ###########################################
#url_nfvo = "http://" + NFVO_IP + ":32002/api/v3"
NFVO_IP = '10.1.7.19'
JSON_CONTENT_HEADER = {'Content-Type':'application/json'}

#Variables with the API path sections
API_ROOT="/slicing_api"
API_VERSION="/v1"
API_SERVICES="/services"
API_VIMS="/vims"
API_NST="/slice_template"
API_NSI="/slice_instance"

############################################# NETWORK SLICE PING ############################################
# PING function to validate if the slice-docker is active
@app.route('/pings', methods=['GET'])
def getPings():
  ping_response  = {'code creation date': '2020-09-29 11:00:00 UTC', 'current_time': str(datetime.datetime.now().isoformat())}

  return jsonify(ping_response), 200

########################################## NFVO INFORMATION (SERVICES/VIMS) #########################################
""" PATH OPTIONS
  "/slicing_api/v1/services(/<ns_id>)" --> GET
  "/slicing_api/v1/vims(/<vim_id>)" --> GET
"""
# GET all the available service descriptors in the NFVO
@app.route(API_ROOT+API_VERSION+API_SERVICES, methods=['GET'])
def get_all_services():
  # get current list of service descriptors
  resp = slice_mapper.get_services(NFVO_IP, JSON_CONTENT_HEADER)
  if resp[1] == 200:
    LOG.debug("Request for service descriptors returned with " + (str(200)))
    json_resp = json.loads(resp[0])
  else:
    LOG.debug("There's a problem to request the services with error code:" + (str(resp[1])))
  return jsonify(json_resp), resp[1]

# GET specific service descriptor in the NFVO
@app.route(API_ROOT+API_VERSION+API_SERVICES+'/<ns_id>', methods=['GET'])
def get_service(ns_id):
  #resp = requests.get(url_nfvo + '/services/'+ str(ns_id), timeout=timeout, headers=JSON_CONTENT_HEADER)
  resp = slice_mapper.get_service(NFVO_IP, JSON_CONTENT_HEADER, ns_id)
  if resp[1] == 200:
    LOG.debug("Request for service descriptor returned with " + (str(200)))
    json_resp = json.loads(resp[0])
  else:
    LOG.debug("There's a problem to request the services with error code:" + (str(resp[1])))
  return jsonify(json_resp), resp[1]

# GET all the available VIMs in the NFVO
@app.route(API_ROOT+API_VERSION+API_VIMS, methods=['GET'])
def get_all_vims():
  # get current list of vims associated ot the nfvo
  resp = slice_mapper.get_vims(NFVO_IP, JSON_CONTENT_HEADER)
  if resp[1] == 200:
    LOG.debug("Request for service descriptors returned with " + (str(200)))
    json_resp = json.loads(resp[0])
  else:
    LOG.debug("There's a problem to request the services with error code:" + (str(resp[1])))
  return jsonify(json_resp), resp[1]

# GET specific service descriptor in the NFVO
@app.route(API_ROOT+API_VERSION+API_VIMS+'/<vim_id>', methods=['GET'])
def get_vim(vim_id):
  #resp = requests.get(url_nfvo + '/services/'+ str(ns_id), timeout=timeout, headers=JSON_CONTENT_HEADER)
  resp = slice_mapper.get_vim(NFVO_IP, JSON_CONTENT_HEADER, vim_id)
  if resp[1] == 200:
    LOG.debug("Request for service descriptor returned with " + (str(200)))
    json_resp = json.loads(resp[0])
  else:
    LOG.debug("There's a problem to request the services with error code:" + (str(resp[1])))
  return jsonify(json_resp), resp[1]

######################################### NETSLICE TEMPLATE Actions #########################################
""" PATH OPTIONS
  "/slicing_api/v1/slice_template" --> GET, POST
  "/slicing_api/v1/slice_template/<nst_id>" --> GET, DELETE
"""
# CREATES a NetSlice template(NST)
@app.route(API_ROOT+API_VERSION+API_NST, methods=['POST']) 
def create_slice_template():
  resp = nst_mgmt.add_nst(request.json, NFVO_IP, JSON_CONTENT_HEADER)
  json_resp = json.loads(resp[0])
  return jsonify(json_resp), resp[1]

# GETS for all the NetSlice Templates (NST) information
@app.route(API_ROOT+API_VERSION+API_NST, methods=['GET'])
def get_all_slice_templates():
  resp = nst_mgmt.get_all_nst()

  return jsonify(resp[0]),resp[1]

# GETS for a specific NetSlice Template (NST) information
@app.route(API_ROOT+API_VERSION+API_NST+'/<nst_id>', methods=['GET'])
def get_slice_template(nst_id):
  resp = nst_mgmt.get_nst(nst_id)

  return jsonify(resp[0]), resp[1]

# DELETES a NetSlice Template
@app.route(API_ROOT+API_VERSION+API_NST+'/<nst_id>', methods=['DELETE'])
def delete_slice_template(nst_id):
  response = nst_mgmt.delete_nst(nst_id)

  return jsonify(response[0]), response[1]

######################################### NETSLICE INSTANCE Actions #########################################
""" PATH OPTIONS
  "/slicing_api/v1/slice_instance" --> GET, POST
  "/slicing-api/v1/slice_instance/<nsi_id>" --> GET, DELETE
  "/slicing_api/v1/slice_instance/<nsi_id>/terminate" --> POST
"""
# CREATES/INSTANTIATES a NetSlice instance (NSI)
@app.route(API_ROOT+API_VERSION+API_NSI, methods=['POST'])
def create_slice_instance():
  resp = nsi_mgmt.create_nsi(request.json, NFVO_IP, JSON_CONTENT_HEADER)
  if resp[1]==200:
    print("DEPLOYMENT READY")
  else:
    print ("ERROR!!!")
  return jsonify(resp[0]), resp[1]

# GETS ALL the NetSlice instances (NSI) information
@app.route(API_ROOT+API_VERSION+API_NSI, methods=['GET'])
def get_all_slice_instances():
    pass
    #return jsonify(allNSI[0]), allNSI[1]

# GETS a SPECIFIC NetSlice instances (NSI) information
@app.route(API_ROOT+API_VERSION+API_NSI+'/<nsi_id>', methods=['GET'])
def get_slice_instance(nsi_id):
    pass
    #return jsonify(returnedNSI[0]), returnedNSI[1]

# DELETEs from the ddbb the NetSlice Instance (NSI) record object
@app.route(API_ROOT+API_VERSION+API_NSI+'/<nsi_id>', methods=['DELETE'])
def delete_slice_instance(nsi_id):
    pass
    #return jsonify(deleted_NSIid[0]), deleted_NSIid[1]

# TERMINATES a NetSlice instance (NSI)
@app.route(API_ROOT+API_VERSION+API_NSI+'/<nsi_id>/terminate', methods=['POST'])
def create_slice_terminate(nsi_id):
    pass
    #return jsonify(terminating_nsi[0]), terminating_nsi[1]

########################################### MAIN SERVER FUNCTION ############################################
if __name__ == '__main__':
  # READ CONFIG
  conf_parser = argparse.ArgumentParser( description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True )
  conf_parser.add_argument("-c", "--conf_file", help="Specify config file", metavar="FILE", default='config.cfg')
  args, remaining_argv = conf_parser.parse_known_args()
  config = ConfigParser()
  config.read(args.conf_file)
  db.settings = config

  # RUN MAIN SERVER THREAD
  #app.run(debug=False, host='localhost', port=os.environ.get("SLICE_MGR_PORT"))
  app.run(debug=False, host='10.1.7.21', port=4444)
