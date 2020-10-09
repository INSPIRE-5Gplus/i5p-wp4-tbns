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

import os, sys, logging, uuid, json, time
from slice_subnet_mgmt import slice_mapper as slice_mapper
from database import database as db

def add_nst(nst_json, host_ip, request_header):
    #TODO: validate if NSD exist in any of hte NFVOs associated
    nst_json['id'] = str(uuid.uuid4())
    
    # Get the current services list to get the uuid for each slice-subnet (NSD) reference
    #current_services_list = mapper.get_nsd_list()
    nfvo_ip = host_ip
    header = request_header
    resp = slice_mapper.get_services(nfvo_ip, header)
    current_services_list = json.loads(resp[0])
    if current_services_list:
        for subnet_item  in nst_json["slice-ns-subnets"]:
            for service_item in current_services_list:
                # Validates if NSDs exist in DDBB by comparing name/vendor/version
                #if (subnet_item["nsd-name"] == service_item["name"] and subnet_item["nsd-vendor"] == service_item["vendor"] and subnet_item["nsd-version"] == service_item["version"]):
                if (subnet_item["nsd-name"] == service_item["name"] and subnet_item["nsd-version"] == service_item["version"]):
                    subnet_item["nsd-ref"] = service_item["descriptor_uuid"]
    else:
        LOG.info("No Network Service Descriptors in the DB.")
        return_msg = {}
        return_msg['error'] = "The list of NSDs is empty."
        return return_msg, 400 
    
    db.nst_db.append(nst_json)
    
    return json.dumps(nst_json), 200

def get_all_nst():
    list_nst = db.nst_db
    if not list_nst:
        return '{"msg":"No NST in the DB."}', 200
    #NOTE: be carefull when having the good db how is the info returned
    return json.dumps(list_nst), 200

def get_nst(nst_id):
    list_nst = db.nst_db
    for nst_item in list_nst:
        print(type(nst_item))
        if nst_item['id'] == nst_id:
            return json.dumps(nst_item), 200
    
    return '{"msg":"No NST with thie ID available."}', 200

def delete_nst(nst_id):
    list_nst = db.nst_db
    for nst_item in list_nst:
        if nst_item['id'] == nst_id:
            db.nst_db.remove(nst_item)
            return '{"msg":"NST removed from the db."}', 200
    
    return '{"msg":"No NST with this ID available."}', 200