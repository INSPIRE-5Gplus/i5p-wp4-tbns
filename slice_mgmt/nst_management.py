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
from database import database as db

def add_nst(nst_json):
    nst_json['id'] = str(uuid.uuid4())
    db.nst_db.append(nst_json)
        
    if db.nst_db is not []:
        return_text = "NST added correctly."
        return_code = 200
    else:
        return_text = "NST NOT added correctly."
        return_code = 400
    
    return return_text, return_code

def get_all_nst():
    list_nst = db.nst_db
    if not list_nst:
        return '{"msg":"No NST in the DB."}', 200
    #NOTE: be carefull when having the good db how is the info returned
    return str(list_nst), 200

def get_nst(nst_id):
    list_nst = db.nst_db
    for nst_item in list_nst:
      if nst_item['id'] == nst_id:
        return str(nst_item), 200
    
    return '{"msg":"No NST with thie ID available."}', 200

def delete_nst(nst_id):
    for nst_item in db.nst_db:
      if nst_item['id'] == nst_id:
        db.nst_db.remove(nst_item)
        return '{"msg":"NST removed from the db."}', 200
    
    return '{"msg":"No NST with this ID available."}', 200