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

import os, sys, logging, uuid, json, time, requests

from slice_subnet_mgmt.nfvo_libs.tng_cli.src.tnglib import env as env
from slice_subnet_mgmt.nfvo_libs.tng_cli.src.tnglib import services as sonata_services
from slice_subnet_mgmt.nfvo_libs.tng_cli.src.tnglib import requests as sonata_requests
from slice_subnet_mgmt.nfvo_libs.tng_cli.src.tnglib import infrastructure as sonata_infrastructure
from database import database as db

# REQUESTS TO GET THE NFVO SERVICES/VIMS
def get_services(nfvo_ip, header):
    url_nfvo = "http://" + nfvo_ip
    env.set_sp_path(url_nfvo)
    env.set_return_header(header)
    resp = sonata_services.get_service_descriptors()

    if resp[0]:
        response = json.dumps(resp[1])
    else:
        response = {"msg": "There are no services available."}
    
    return response, 200

def get_service(nfvo_ip, header, service_id):
    url_nfvo = "http://" + nfvo_ip
    env.set_sp_path(url_nfvo)
    env.set_return_header(header)
    resp = sonata_services.get_service_descriptor(service_id)

    if resp[0]:
        response = json.dumps(resp[1])
    else:
        response = {"msg": "There is NO service available with the requested ID."}
    
    return response, 200

def get_vims(nfvo_ip, header):
    url_nfvo = "http://" + nfvo_ip
    env.set_sp_path(url_nfvo)
    env.set_return_header(header)
    resp = sonata_infrastructure.get_vims()

    if resp[0]:
        response = json.dumps(resp[1])
    else:
        response = {"msg": "There is NO VIM available with the requested ID."}
    
    return response, 200

def get_vim(nfvo_ip, header, vim_id):
    url_nfvo = "http://" + nfvo_ip
    env.set_sp_path(url_nfvo)
    env.set_return_header(header)
    resp = sonata_infrastructure.get_vim(vim_id)

    if resp[0]:
        response = json.dumps(resp[1])
    else:
        response = {"msg": "There is NO VIM available with the requested ID."}
    
    return response, 200

# REQUESTS TO DEPLOY NFVO SERVICES
def deploy_service(nfvo_ip, header, service_id):
    #sonata_requests.service_instantiate(service_uuid, sla_uuid=None, mapping=None, params=None, name=None)

    #return {"msg": "There is NO service available with the requested ID."}, 200
    pass