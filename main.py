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
from database import database as db

# TODO: improve logging
LOG = logging.getLogger(__name__)

app = Flask(__name__)

######################################### SONATA NFVO CONFIGURATION ###########################################
NFVO_IP = '10.1.7.19'
url_nfvo = "http://" + NFVO_IP + ":32002/api/v3"
JSON_CONTENT_HEADER = {'Content-Type':'application/json'}
timeout = 15.0

#Variables with the API path sections
API_ROOT="/slicing-api"
API_VERSION="/v1"
API_NST="/slice_template"
API_NSI="/slice_instance"

############################################# NETWORK SLICE PING ############################################
# PING function to validate if the slice-docker is active
@app.route('/pings', methods=['GET'])
def getPings():
  ping_response  = {'code creation date': '2020-09-29 11:00:00 UTC', 'current_time': str(datetime.datetime.now().isoformat())}

  return jsonify(ping_response), 200

########################################## NETWORK SERVICES Actions #########################################
# GET all the available service descriptors available in the NFVO
@app.route(API_ROOT+API_VERSION+'/services', methods=['GET'])
def get_all_services():
  """Returns info on all available service descriptors.
  :returns: A tuple. [0] is a bool with the result. [1] is a 
  list of dictionaries. Each dictionary contains an nsd.
  """
  # get current list of service descriptors
  resp = requests.get(url_nfvo + "/services", timeout=timeout, headers=JSON_CONTENT_HEADER)

  if resp.status_code != 200:
    LOG.debug("Request for service descriptors returned with " + (str(resp.status_code)))
    return [], resp.status_code

  services = json.loads(resp.text)

  services_res = []
  for service in services:
    if service['platform'] != '5gtango':
        continue
    dic = {'descriptor_uuid': service['uuid'],
            'name': service['nsd']['name'],
            'version': service['nsd']['version'],
            'created_at': service['created_at']}
    LOG.debug(str(dic))
    services_res.append(dic)
  
  LOG.debug("Request for service descriptors returned with " + (str(200)))
  return jsonify(services_res), 200

# GET specific service descriptor in the NFVO
@app.route(API_ROOT+API_VERSION+'/services/<ns_id>', methods=['GET'])
def get_service(ns_id):
  resp = requests.get(url_nfvo + '/services/'+ str(ns_id), timeout=timeout, headers=JSON_CONTENT_HEADER)
  if resp.status_code != 200:
    LOG.debug("Request for service descriptor returned with " + (str(resp.status_code)))
    return json.loads(resp.text), resp.status_code
  
  LOG.debug("Request for service descriptor returned with " + (str(200)))
  return jsonify(resp.text), 200

######################################### NETSLICE TEMPLATE Actions #########################################
""" PATH OPTIONS
  "/slicing-api/v1/slice_template" --> OPTIONS, GET, POST
  "/slicing-api/v1/slice_template/<nst_id>" --> OPTIONS, GET, DELETE
"""
# CREATES a NetSlice template(NST)
@app.route(API_ROOT+API_VERSION+API_NST, methods=['POST']) 
def create_slice_template():
  resp = nst_mgmt.add_nst(request.json)
  return resp[0], resp[1]

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
  "/slicing-api/v1/slice_instance" --> OPTIONS, GET, POST
  "/slicing-api/v1/slice_instance/<nsi_id>" --> OPTIONS, GET, DELETE
  "/slicing-api/v1/slice_instance/<nsi_id>/terminate" --> OPTIONS, POST
"""
# CREATES/INSTANTIATES a NetSlice instance (NSI)
@app.route(API_ROOT+API_VERSION+API_NSI, methods=['POST'])
def create_slice_instance():
    pass
    #return jsonify(instantiating_nsi[0]), instantiating_nsi[1]

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
